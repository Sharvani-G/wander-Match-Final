from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.provided import Trip, TripMember, Itinerary, ItineraryItem, Proposal, Vote, User
from ..models.additive import SlotConsensus, Branch, BranchMember, RevisionHistory
from ..websocket_manager import ws_manager


router = APIRouter(prefix="/api", tags=["consensus & proposals"])


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# --- Schemas ---

class CreateProposalRequest(BaseModel):
    itm_id: str = Field(..., description="Target itinerary item ID")
    proposed_by_user_id: str = Field(..., description="User ID proposing the change")
    title: str = Field(..., min_length=1)
    rationale: Optional[str] = Field(default="")
    cost_delta: Optional[float] = Field(default=0.0)
    currency: Optional[str] = Field(default="USD")


class CastVoteRequest(BaseModel):
    prp_id: str = Field(..., description="Proposal ID")
    user_id: str = Field(..., description="User casting vote")
    value: str = Field(..., description="'yes' or 'no'")
    comment: Optional[str] = Field(default=None)


class BatchVoteItem(BaseModel):
    user_id: str
    value: str
    comment: Optional[str] = None


class BatchVoteRequest(BaseModel):
    itm_id: str
    prp_id: str
    votes: List[BatchVoteItem]


class ModeAInvokeRequest(BaseModel):
    itm_id: str
    user_id: str


class ModeAAcceptRequest(BaseModel):
    itm_id: str
    user_id: str
    proposal_id: Optional[str] = None


class ModeAForceBranchRequest(BaseModel):
    itm_id: str
    user_id: str


class ModeAExtendRequest(BaseModel):
    itm_id: str
    user_id: str
    extend_minutes: Optional[int] = 10


class ModeADirectConfirmRequest(BaseModel):
    itm_id: str
    user_id: str
    proposal_id: str


class ReconcileRequest(BaseModel):
    prp_id: str
    user_id: Optional[str] = None


class CheckTimerRequest(BaseModel):
    prp_id: str
    advance_minutes: Optional[float] = 0.0


# --- Helpers ---

def _get_item_and_trip(db: Session, item_id: str):
    item = db.query(ItineraryItem).filter(ItineraryItem.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Itinerary slot '{item_id}' not found")
    itinerary = db.query(Itinerary).filter(Itinerary.itinerary_id == item.itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    trip = db.query(Trip).filter(Trip.trip_id == itinerary.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return item, itinerary, trip


def _verify_member(db: Session, trip_id: str, user_id: str):
    trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.owner_user_id == user_id:
        return True
    member = db.query(TripMember).filter(
        TripMember.trip_id == trip_id,
        TripMember.user_id == user_id,
        TripMember.status == 'accepted'
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail=f"User '{user_id}' is not an authorized member of trip '{trip_id}'")
    return True


def _verify_owner(trip: Trip, user_id: str):
    if trip.owner_user_id != user_id:
        raise HTTPException(status_code=403, detail="Action gated to trip owner/admin only")


# --- Endpoints ---

@router.post("/proposals")
async def create_proposal(req: CreateProposalRequest, db: Session = Depends(get_db)):
    """Submits an initial activity proposal for a slot. closes_at starts as NULL in Mode A or Mode NA until NO."""
    item, itinerary, trip = _get_item_and_trip(db, req.itm_id)
    _verify_member(db, trip.trip_id, req.proposed_by_user_id)

    prp_id = generate_id("prp")
    proposal = Proposal(
        proposal_id=prp_id,
        itinerary_id=itinerary.itinerary_id,
        proposed_by_user_id=req.proposed_by_user_id,
        action="replace",
        target_item_id=req.itm_id,
        title=req.title,
        rationale=req.rationale or "",
        cost_delta=Decimal(str(req.cost_delta or 0.0)),
        currency=req.currency or "USD",
        status="open",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(proposal)

    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == req.itm_id).first()
    if not consensus:
        consensus = SlotConsensus(
            consensus_id=generate_id("cns"),
            item_id=req.itm_id,
            slot_status="in_consensus",
            current_round=1,
            consensus_cycle=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(consensus)
    else:
        consensus.slot_status = "in_consensus"
        consensus.current_round = (consensus.current_round or 0) + 1
        consensus.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(proposal)

    # Broadcast to trip room
    await ws_manager.broadcast_to_trip(trip.trip_id, {
        "type": "proposalCreated",
        "trip_id": trip.trip_id,
        "itm_id": req.itm_id,
        "proposal": {
            "proposal_id": proposal.proposal_id,
            "title": proposal.title,
            "rationale": proposal.rationale,
            "cost_delta": float(proposal.cost_delta) if proposal.cost_delta is not None else 0.0,
            "currency": proposal.currency,
            "status": proposal.status,
            "proposed_by_user_id": proposal.proposed_by_user_id,
        }
    })

    return {
        "message": "Proposal created. Status is IN_CONSENSUS.",
        "proposal": {
            "proposal_id": proposal.proposal_id,
            "itm_id": proposal.target_item_id,
            "title": proposal.title,
            "rationale": proposal.rationale,
            "cost_delta": float(proposal.cost_delta) if proposal.cost_delta is not None else 0.0,
            "currency": proposal.currency,
            "status": proposal.status,
            "proposed_by_user_id": proposal.proposed_by_user_id,
            "created_at": proposal.created_at.isoformat(),
        }
    }


@router.get("/slots/{itm_id}/active-proposal")
def get_active_proposal_for_slot(itm_id: str, db: Session = Depends(get_db)):
    """Returns the current active proposal open for voting on an itinerary slot."""
    item, itinerary, trip = _get_item_and_trip(db, itm_id)
    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == itm_id).first()
    
    active_proposal = db.query(Proposal).filter(
        Proposal.target_item_id == itm_id,
        Proposal.status == "open"
    ).order_by(Proposal.created_at.desc()).first()

    votes_list = []
    if active_proposal:
        votes = db.query(Vote).filter(Vote.proposal_id == active_proposal.proposal_id).all()
        votes_list = [{"user_id": v.user_id, "value": v.value, "comment": v.comment} for v in votes]

    return {
        "slot_id": itm_id,
        "slot_status": consensus.slot_status if consensus else "draft",
        "current_round": consensus.current_round if consensus else 0,
        "active_proposal_id": active_proposal.proposal_id if active_proposal else None,
        "active_proposal": {
            "proposal_id": active_proposal.proposal_id,
            "title": active_proposal.title,
            "rationale": active_proposal.rationale,
            "cost_delta": float(active_proposal.cost_delta) if active_proposal.cost_delta is not None else 0.0,
            "currency": active_proposal.currency,
            "status": active_proposal.status,
            "closes_at": active_proposal.closes_at.isoformat() if active_proposal.closes_at else None,
        } if active_proposal else None,
        "votes_count": len(votes_list),
        "votes": votes_list,
    }


@router.get("/slots/{itm_id}/history")
def get_slot_history(itm_id: str, db: Session = Depends(get_db)):
    """Returns full chronological proposal and voting history for an itinerary slot."""
    item, itinerary, trip = _get_item_and_trip(db, itm_id)
    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == itm_id).first()
    proposals = db.query(Proposal).filter(Proposal.target_item_id == itm_id).order_by(Proposal.created_at.asc()).all()

    history = []
    for p in proposals:
        votes = db.query(Vote).filter(Vote.proposal_id == p.proposal_id).all()
        yes_count = sum(1 for v in votes if v.value == "yes")
        no_count = sum(1 for v in votes if v.value == "no")
        history.append({
            "proposal_id": p.proposal_id,
            "proposed_by_user_id": p.proposed_by_user_id,
            "title": p.title,
            "rationale": p.rationale,
            "cost_delta": float(p.cost_delta) if p.cost_delta is not None else 0.0,
            "status": p.status,
            "created_at": p.created_at.isoformat(),
            "votes": [{"user_id": v.user_id, "value": v.value, "comment": v.comment} for v in votes],
            "yes_count": yes_count,
            "no_count": no_count,
            "total_votes": len(votes),
        })

    return {
        "item_id": itm_id,
        "current_slot_status": consensus.slot_status if consensus else "draft",
        "current_round": consensus.current_round if consensus else 0,
        "proposals_count": len(history),
        "history": history
    }


@router.post("/votes")
async def cast_vote(req: Union[CastVoteRequest, List[CastVoteRequest]], db: Session = Depends(get_db)):
    """
    Casts one or more votes on a proposal.
    - Pass single vote or list.
    - If all members vote YES: confirms immediately (fast-path)!
    - In Mode NA: First NO starts 10-minute timer.
    - In Mode A: NO votes do NOT start a timer; admin retains final say.
    """
    votes_in = [req] if isinstance(req, CastVoteRequest) else req
    if not votes_in:
        raise HTTPException(status_code=400, detail="Empty vote list")

    first_req = votes_in[0]
    proposal = db.query(Proposal).filter(Proposal.proposal_id == first_req.prp_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Proposal '{first_req.prp_id}' not found")
    item, itinerary, trip = _get_item_and_trip(db, proposal.target_item_id)

    # Get total trip member count (accepted members + owner)
    accepted_members = db.query(TripMember).filter(
        TripMember.trip_id == trip.trip_id,
        TripMember.status == "accepted"
    ).all()
    member_ids = set([m.user_id for m in accepted_members] + [trip.owner_user_id])
    total_members_count = max(len(member_ids), 1)

    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == item.item_id).first()
    if not consensus:
        consensus = SlotConsensus(
            consensus_id=generate_id("cns"),
            item_id=item.item_id,
            slot_status="in_consensus",
            current_round=1,
            consensus_cycle=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(consensus)

    now = datetime.now(timezone.utc)
    for v_in in votes_in:
        _verify_member(db, trip.trip_id, v_in.user_id)
        # Check single active vote (retraction / update)
        existing_vote = db.query(Vote).filter(
            Vote.proposal_id == proposal.proposal_id,
            Vote.user_id == v_in.user_id
        ).first()
        if existing_vote:
            existing_vote.value = v_in.value.lower()
            existing_vote.comment = v_in.comment
            existing_vote.updated_at = now
        else:
            vote = Vote(
                vote_id=generate_id("vot"),
                proposal_id=proposal.proposal_id,
                user_id=v_in.user_id,
                value=v_in.value.lower(),
                weight=Decimal("1.0"),
                comment=v_in.comment,
                cast_at=now,
                updated_at=now,
            )
            db.add(vote)

    db.commit()

    # Re-evaluate all votes on proposal
    all_votes = db.query(Vote).filter(Vote.proposal_id == proposal.proposal_id).all()
    yes_votes = [v for v in all_votes if v.value == "yes"]
    no_votes = [v for v in all_votes if v.value == "no"]

    unanimous_confirmed = False
    is_mode_a = (trip.mode or "").strip().lower() in ["mode a", "mode_a", "admin"]

    # 1. Fast-path Unanimous YES: all trip members voted YES
    if len(yes_votes) >= total_members_count and len(no_votes) == 0:
        unanimous_confirmed = True
        proposal.status = "accepted"
        consensus.slot_status = "confirmed"
        item.title = proposal.title
        if proposal.cost_delta is not None and proposal.cost_delta != Decimal("0.0"):
            item.cost = (item.cost or Decimal("0.0")) + proposal.cost_delta
        item.status = "confirmed"

    # 2. If NO vote exists and Mode NA: start 10-minute timer if not started
    elif len(no_votes) > 0 and not is_mode_a:
        if consensus.first_no_at is None:
            consensus.first_no_at = now
            proposal.closes_at = now + timedelta(minutes=10)
        consensus.slot_status = "in_consensus"

    consensus.updated_at = now
    proposal.updated_at = now
    db.commit()

    # Broadcast voteCast and status changed
    await ws_manager.broadcast_to_trip(trip.trip_id, {
        "type": "voteCast",
        "trip_id": trip.trip_id,
        "itm_id": item.item_id,
        "proposal_id": proposal.proposal_id,
        "total_votes": len(all_votes),
        "yes_count": len(yes_votes),
        "no_count": len(no_votes),
        "unanimous_confirmed": unanimous_confirmed,
        "slot_status": consensus.slot_status,
    })

    if unanimous_confirmed:
        await ws_manager.broadcast_to_trip(trip.trip_id, {
            "type": "slotStatusChanged",
            "trip_id": trip.trip_id,
            "itm_id": item.item_id,
            "slot_status": "confirmed",
            "accepted_proposal_id": proposal.proposal_id,
            "title": item.title,
        })

    return {
        "status": "success",
        "proposal_id": proposal.proposal_id,
        "unanimous_fast_path": unanimous_confirmed,
        "yes_count": len(yes_votes),
        "no_count": len(no_votes),
        "total_members": total_members_count,
        "slot_status": consensus.slot_status,
        "closes_at": proposal.closes_at.isoformat() if proposal.closes_at else None,
    }


@router.post("/votes/batch")
async def cast_votes_batch(req: BatchVoteRequest, db: Session = Depends(get_db)):
    """Batch multi-member voting for simulated or simultaneous member actions."""
    votes_list = [CastVoteRequest(prp_id=req.prp_id, user_id=v.user_id, value=v.value, comment=v.comment) for v in req.votes]
    return await cast_vote(votes_list, db)


# --- Mode A Admin Controls ---

@router.post("/consensus/mode-a/invoke")
async def mode_a_invoke_ai(req: ModeAInvokeRequest, db: Session = Depends(get_db)):
    """Admin explicitly triggers AI reconciliation advice for a slot in Mode A. Gated to owner."""
    item, itinerary, trip = _get_item_and_trip(db, req.itm_id)
    _verify_owner(trip, req.user_id)

    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == req.itm_id).first()
    if not consensus:
        consensus = SlotConsensus(
            consensus_id=generate_id("cns"),
            item_id=req.itm_id,
            slot_status="in_consensus",
            current_round=1,
            consensus_cycle=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(consensus)

    active_proposal = db.query(Proposal).filter(
        Proposal.target_item_id == req.itm_id,
        Proposal.status == "open"
    ).order_by(Proposal.created_at.desc()).first()

    prop_title = active_proposal.title if active_proposal else item.title
    recommendation = {
        "advisory": True,
        "proposed_title": f"Harmonized {prop_title} & Cultural Walk",
        "rationale": "AI synthesized compromise balancing sightseeing and activity pacing for group members.",
        "cost_delta": 15.0,
        "currency": "USD",
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

    consensus.updated_at = datetime.now(timezone.utc)
    db.commit()

    await ws_manager.broadcast_to_trip(trip.trip_id, {
        "type": "aiRecommendationReady",
        "trip_id": trip.trip_id,
        "itm_id": req.itm_id,
        "recommendation": recommendation
    })

    return {
        "status": "advisory_ready",
        "itm_id": req.itm_id,
        "admin_recommendation": recommendation
    }


@router.post("/consensus/mode-a/accept")
async def mode_a_accept(req: ModeAAcceptRequest, db: Session = Depends(get_db)):
    """Admin accepts the recommendation or proposal, locking it into the itinerary (CONFIRMED)."""
    item, itinerary, trip = _get_item_and_trip(db, req.itm_id)
    _verify_owner(trip, req.user_id)

    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == req.itm_id).first()
    if not consensus:
        consensus = SlotConsensus(
            consensus_id=generate_id("cns"),
            item_id=req.itm_id,
            slot_status="confirmed",
            current_round=1,
            consensus_cycle=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(consensus)

    if req.proposal_id:
        proposal = db.query(Proposal).filter(Proposal.proposal_id == req.proposal_id).first()
        if proposal:
            proposal.status = "accepted"
            item.title = proposal.title
            if proposal.cost_delta:
                item.cost = (item.cost or Decimal("0.0")) + proposal.cost_delta

    consensus.slot_status = "confirmed"
    consensus.updated_at = datetime.now(timezone.utc)
    item.status = "confirmed"
    db.commit()

    await ws_manager.broadcast_to_trip(trip.trip_id, {
        "type": "slotStatusChanged",
        "trip_id": trip.trip_id,
        "itm_id": req.itm_id,
        "slot_status": "confirmed",
        "title": item.title
    })

    return {"status": "confirmed", "itm_id": req.itm_id, "title": item.title}


@router.post("/consensus/mode-a/force-branch")
async def mode_a_force_branch(req: ModeAForceBranchRequest, db: Session = Depends(get_db)):
    """Admin overrides consensus and creates parallel branches for the slot."""
    item, itinerary, trip = _get_item_and_trip(db, req.itm_id)
    _verify_owner(trip, req.user_id)

    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == req.itm_id).first()
    if not consensus:
        consensus = SlotConsensus(
            consensus_id=generate_id("cns"),
            item_id=req.itm_id,
            slot_status="branched",
            current_round=1,
            consensus_cycle=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(consensus)
    else:
        consensus.slot_status = "branched"
        consensus.updated_at = datetime.now(timezone.utc)

    # Create 2 branches
    branch_a = Branch(
        branch_id=generate_id("brn"),
        item_id=req.itm_id,
        title=f"{item.title} (Branch A)",
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    branch_b = Branch(
        branch_id=generate_id("brn"),
        item_id=req.itm_id,
        title=f"{item.title} (Branch B)",
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(branch_a)
    db.add(branch_b)
    db.commit()

    await ws_manager.broadcast_to_trip(trip.trip_id, {
        "type": "slotStatusChanged",
        "trip_id": trip.trip_id,
        "itm_id": req.itm_id,
        "slot_status": "branched",
        "branches": [
            {"branch_id": branch_a.branch_id, "title": branch_a.title},
            {"branch_id": branch_b.branch_id, "title": branch_b.title},
        ]
    })

    return {
        "status": "branched",
        "itm_id": req.itm_id,
        "branches": [
            {"branch_id": branch_a.branch_id, "title": branch_a.title},
            {"branch_id": branch_b.branch_id, "title": branch_b.title},
        ]
    }


@router.post("/consensus/mode-a/extend")
async def mode_a_extend(req: ModeAExtendRequest, db: Session = Depends(get_db)):
    """Admin extends voting round without auto-branching."""
    item, itinerary, trip = _get_item_and_trip(db, req.itm_id)
    _verify_owner(trip, req.user_id)

    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == req.itm_id).first()
    if not consensus:
        consensus = SlotConsensus(
            consensus_id=generate_id("cns"),
            item_id=req.itm_id,
            slot_status="in_consensus",
            current_round=1,
            consensus_cycle=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(consensus)
    else:
        consensus.current_round = (consensus.current_round or 1) + 1
        consensus.updated_at = datetime.now(timezone.utc)

    db.commit()

    await ws_manager.broadcast_to_trip(trip.trip_id, {
        "type": "slotStatusChanged",
        "trip_id": trip.trip_id,
        "itm_id": req.itm_id,
        "slot_status": consensus.slot_status,
        "current_round": consensus.current_round,
    })

    return {"status": "extended", "itm_id": req.itm_id, "current_round": consensus.current_round}


@router.post("/consensus/mode-a/direct-confirm")
async def mode_a_direct_confirm(req: ModeADirectConfirmRequest, db: Session = Depends(get_db)):
    """Admin directly confirms any open proposal into the itinerary slot without waiting."""
    item, itinerary, trip = _get_item_and_trip(db, req.itm_id)
    _verify_owner(trip, req.user_id)

    proposal = db.query(Proposal).filter(Proposal.proposal_id == req.proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Proposal '{req.proposal_id}' not found")

    proposal.status = "accepted"
    item.title = proposal.title
    if proposal.cost_delta:
        item.cost = (item.cost or Decimal("0.0")) + proposal.cost_delta
    item.status = "confirmed"

    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == req.itm_id).first()
    if not consensus:
        consensus = SlotConsensus(
            consensus_id=generate_id("cns"),
            item_id=req.itm_id,
            slot_status="confirmed",
            current_round=1,
            consensus_cycle=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(consensus)
    else:
        consensus.slot_status = "confirmed"
        consensus.updated_at = datetime.now(timezone.utc)

    db.commit()

    await ws_manager.broadcast_to_trip(trip.trip_id, {
        "type": "slotStatusChanged",
        "trip_id": trip.trip_id,
        "itm_id": req.itm_id,
        "slot_status": "confirmed",
        "title": item.title,
    })

    return {"status": "confirmed", "itm_id": req.itm_id, "title": item.title}


@router.post("/consensus/reconcile")
async def consensus_reconcile(req: ReconcileRequest, db: Session = Depends(get_db)):
    """Unified consensus reconciliation endpoint per PANCHAMI.md line 771."""
    proposal = db.query(Proposal).filter(Proposal.proposal_id == req.prp_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    item, itinerary, trip = _get_item_and_trip(db, proposal.target_item_id)

    is_mode_a = (trip.mode or "").strip().lower() in ["mode a", "mode_a", "admin"]
    user_id = req.user_id or trip.owner_user_id

    if is_mode_a:
        return await mode_a_invoke_ai(ModeAInvokeRequest(itm_id=item.item_id, user_id=user_id), db)
    else:
        # Mode NA automatic reconcile
        consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == item.item_id).first()
        round_num = (consensus.current_round or 1) + 1 if consensus else 2
        if consensus:
            consensus.current_round = round_num
            consensus.updated_at = datetime.now(timezone.utc)
            db.commit()

        # Mode NA synthesis
        compromise = {
            "mode": "Mode NA",
            "round": round_num,
            "compromise_title": f"Collaborative Plan: {proposal.title} with Group Lunch",
            "status": "in_consensus",
            "closes_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
        }

        await ws_manager.broadcast_to_trip(trip.trip_id, {
            "type": "aiRecommendationReady",
            "trip_id": trip.trip_id,
            "itm_id": item.item_id,
            "recommendation": compromise
        })

        return compromise


@router.post("/proposals/check-timer")
async def check_timer(req: CheckTimerRequest, db: Session = Depends(get_db)):
    """
    Evaluates the 10-minute voting window for a proposal (Mode NA).
    advance_minutes simulates advancing clock. If window expired with 0 NO votes -> auto-confirms!
    """
    proposal = db.query(Proposal).filter(Proposal.proposal_id == req.prp_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    item, itinerary, trip = _get_item_and_trip(db, proposal.target_item_id)
    consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == item.item_id).first()

    now = datetime.now(timezone.utc) + timedelta(minutes=req.advance_minutes or 0.0)
    votes = db.query(Vote).filter(Vote.proposal_id == proposal.proposal_id).all()
    no_votes = [v for v in votes if v.value == "no"]

    expired = proposal.closes_at is not None and now >= proposal.closes_at.replace(tzinfo=timezone.utc) if proposal.closes_at.tzinfo is None else now >= proposal.closes_at

    auto_confirmed = False
    if expired and len(no_votes) == 0 and proposal.status == "open":
        auto_confirmed = True
        proposal.status = "accepted"
        item.title = proposal.title
        item.status = "confirmed"
        if consensus:
            consensus.slot_status = "confirmed"
            consensus.updated_at = datetime.now(timezone.utc)
        db.commit()

        await ws_manager.broadcast_to_trip(trip.trip_id, {
            "type": "slotStatusChanged",
            "trip_id": trip.trip_id,
            "itm_id": item.item_id,
            "slot_status": "confirmed",
            "title": item.title,
            "reason": "10-minute timer expired with zero NO votes"
        })

    return {
        "proposal_id": proposal.proposal_id,
        "closes_at": proposal.closes_at.isoformat() if proposal.closes_at else None,
        "simulated_now": now.isoformat(),
        "expired": expired,
        "auto_confirmed": auto_confirmed,
        "no_votes_count": len(no_votes),
        "slot_status": consensus.slot_status if consensus else "draft"
    }
