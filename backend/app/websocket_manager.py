import os
import json
import logging
from typing import Dict, Optional, Any, List
import jwt
from fastapi import WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session

from .models.provided import Trip, TripMember, Itinerary, ItineraryItem, Proposal, Vote, User
from .models.additive import SlotConsensus, Branch, BranchMember

logger = logging.getLogger("wandermatch.websocket")

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY", "sk_test_default")
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL", "https://clerk.your-domain.accounts.dev/.well-known/jwks.json")


def verify_websocket_token(token: Optional[str]) -> Optional[str]:
    """
    Verifies Clerk JWT token from WebSocket query param or header.
    Validates signature and claims.
    Derives authenticated identity directly from the token's 'sub' claim.
    Returns authenticated user_id on success, or None on failure.
    """
    if not token or token in ["null", "undefined", ""]:
        return None

    # Strip Bearer if passed
    if token.startswith("Bearer "):
        token = token[7:].strip()

    # 1. First attempt: Verify using CLERK_SECRET_KEY (HS256) for backend/test tokens
    try:
        payload = jwt.decode(token, CLERK_SECRET_KEY, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub:
            return str(sub)
    except jwt.InvalidSignatureError:
        pass  # Try RS256 JWKS below
    except jwt.ExpiredSignatureError:
        logger.warning("WebSocket JWT has expired")
        return None
    except Exception:
        pass

    # 2. Second attempt: Verify using Clerk JWKS (RS256) for production Clerk frontend tokens
    try:
        import httpx
        from functools import lru_cache

        # Fetch JWKS
        jwks_client = jwt.PyJWKClient(CLERK_JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(token, signing_key.key, algorithms=["RS256"])
        sub = payload.get("sub")
        if sub:
            return str(sub)
    except Exception as e:
        # If signature verification fails or JWKS unreachable, reject
        logger.warning(f"WebSocket token RS256 verification failed: {e}")

    return None


class ConnectionManager:
    def __init__(self):
        # trip_id -> { user_id: WebSocket }
        self.active_rooms: Dict[str, Dict[str, WebSocket]] = {}

    def is_user_authorized(self, trip_id: str, user_id: str, db: Session) -> bool:
        """Verify user is the trip owner or an accepted trip member in Neon PostgreSQL."""
        trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
        if not trip:
            return False
        if trip.owner_user_id == user_id:
            return True
        member = db.query(TripMember).filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == user_id,
            TripMember.status == "accepted"
        ).first()
        return member is not None

    def get_trip_snapshot(self, trip_id: str, db: Session) -> Dict[str, Any]:
        """Build an authoritative state snapshot directly from Neon PostgreSQL."""
        trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
        if not trip:
            return {}
        itinerary = db.query(Itinerary).filter(Itinerary.trip_id == trip_id).first()
        if not itinerary:
            return {"trip_id": trip_id, "mode": trip.mode, "slots": []}

        items = db.query(ItineraryItem).filter(
            ItineraryItem.itinerary_id == itinerary.itinerary_id
        ).order_by(ItineraryItem.day_index, ItineraryItem.sort_order).all()

        slots_data = []
        for item in items:
            consensus = db.query(SlotConsensus).filter(SlotConsensus.item_id == item.item_id).first()
            proposals = db.query(Proposal).filter(Proposal.target_item_id == item.item_id).order_by(Proposal.created_at.desc()).all()

            proposals_list = []
            for p in proposals:
                votes = db.query(Vote).filter(Vote.proposal_id == p.proposal_id).all()
                yes_count = sum(1 for v in votes if v.value == "yes")
                no_count = sum(1 for v in votes if v.value == "no")
                proposals_list.append({
                    "proposal_id": p.proposal_id,
                    "proposed_by_user_id": p.proposed_by_user_id,
                    "title": p.title,
                    "rationale": p.rationale,
                    "cost_delta": float(p.cost_delta) if p.cost_delta is not None else 0.0,
                    "currency": p.currency,
                    "status": p.status,
                    "closes_at": p.closes_at.isoformat() if p.closes_at else None,
                    "yes_votes": yes_count,
                    "no_votes": no_count,
                    "total_votes": len(votes),
                    "votes": [{"user_id": v.user_id, "value": v.value, "comment": v.comment} for v in votes]
                })

            branches = db.query(Branch).filter(Branch.item_id == item.item_id).all()
            branches_list = []
            for b in branches:
                bm = db.query(BranchMember).filter(BranchMember.branch_id == b.branch_id).all()
                branches_list.append({
                    "branch_id": b.branch_id,
                    "title": b.title,
                    "status": b.status,
                    "members": [m.user_id for m in bm]
                })

            slots_data.append({
                "item_id": item.item_id,
                "title": item.title,
                "day_index": item.day_index,
                "sort_order": item.sort_order,
                "slot_status": consensus.slot_status if consensus else "draft",
                "current_round": consensus.current_round if consensus else 0,
                "proposals": proposals_list,
                "branches": branches_list,
            })

        return {
            "trip_id": trip_id,
            "mode": trip.mode,
            "title": trip.title,
            "status": trip.status,
            "slots": slots_data
        }

    async def authenticate_and_connect(
        self,
        websocket: WebSocket,
        trip_id: str,
        path_user_id: Optional[str],
        token: Optional[str],
        db: Session
    ) -> Optional[str]:
        """
        1. Verifies token signature and claims.
        2. Derives authenticated identity directly from token 'sub'.
        3. Detects and rejects forged identity if path_user_id != token_user_id.
        4. Verifies trip membership in Neon PostgreSQL before accepting connection or delivering snapshot.
        Returns authenticated user_id on success, or None on failure (closing socket).
        """
        # Step 1: Verify token
        auth_user_id = verify_websocket_token(token)
        if not auth_user_id:
            logger.warning(f"WebSocket connection rejected: invalid or missing token for trip {trip_id}")
            await websocket.close(code=4401, reason="Unauthorized: Invalid or missing authentication token")
            return None

        # Step 2: Check for forged identity attempt
        if path_user_id and path_user_id != auth_user_id:
            logger.warning(f"WebSocket forged identity detected: token is {auth_user_id} but URL specified {path_user_id}")
            await websocket.close(code=4403, reason="Forbidden: Authenticated identity does not match URL identity")
            return None

        # Step 3: Check trip membership in Neon DB
        if not self.is_user_authorized(trip_id, auth_user_id, db):
            logger.warning(f"WebSocket rejected: user {auth_user_id} is not an accepted member of trip {trip_id}")
            await websocket.close(code=4403, reason="Forbidden: Not an authorized member of this trip")
            return None

        # Step 4: Accept and register in room
        await websocket.accept()
        if trip_id not in self.active_rooms:
            self.active_rooms[trip_id] = {}
        self.active_rooms[trip_id][auth_user_id] = websocket

        # Step 5: Deliver authoritative state snapshot resync
        snapshot = self.get_trip_snapshot(trip_id, db)
        await websocket.send_json({
            "type": "resyncSnapshot",
            "trip_id": trip_id,
            "user_id": auth_user_id,
            "snapshot": snapshot
        })
        return auth_user_id

    def disconnect(self, trip_id: str, user_id: str):
        if trip_id in self.active_rooms and user_id in self.active_rooms[trip_id]:
            del self.active_rooms[trip_id][user_id]
            if not self.active_rooms[trip_id]:
                del self.active_rooms[trip_id]

    async def broadcast_to_trip(self, trip_id: str, message: Dict[str, Any], exclude_user_id: Optional[str] = None):
        if trip_id not in self.active_rooms:
            return
        dead_users = []
        for uid, ws in list(self.active_rooms[trip_id].items()):
            if exclude_user_id and uid == exclude_user_id:
                continue
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send ws message to user {uid} in trip {trip_id}: {e}")
                dead_users.append(uid)
        for du in dead_users:
            self.disconnect(trip_id, du)

ws_manager = ConnectionManager()
