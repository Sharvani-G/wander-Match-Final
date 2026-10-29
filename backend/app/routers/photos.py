import os
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.provided import Trip, TripMember, User
from ..models.additive import Photo, PhotoPerson

logger = logging.getLogger("wandermatch.photos")

router = APIRouter(prefix="/api", tags=["photos & memories"])

# Directory for static photo uploads
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

DEEPFACE_SERVICE_URL = os.getenv("DEEPFACE_SERVICE_URL", "http://127.0.0.1:8001")


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@router.post("/photos")
async def upload_photo(
    file: Optional[UploadFile] = File(None),
    photo: Optional[UploadFile] = File(None),
    trp_id: Optional[str] = Form(None),
    trpId: Optional[str] = Form(None),
    uploader_id: Optional[str] = Form(None),
    uploaderId: Optional[str] = Form(None),
    caption: Optional[str] = Form(""),
    title: Optional[str] = Form("Trip Memory"),
    folder: Optional[str] = Form("All"),
    db: Session = Depends(get_db),
):
    """
    Trip Photo Upload & Metadata Persistence:
    1. Validates trip and authorized uploader in Neon PostgreSQL.
    2. Persists photo file to storage and creates record in `photos` table.
    3. Scopes face recognition strictly to trip members.
    4. Connects to separate DeepFace service if reachable, otherwise safely degrades without failing upload.
    """
    trip_id = trp_id or trpId
    user_id = uploader_id or uploaderId
    upload_file = file or photo

    if not trip_id:
        raise HTTPException(status_code=400, detail="Missing required trip ID (trp_id or trpId)")

    trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip '{trip_id}' not found")

    # If uploader_id is given, verify user or default to owner
    if not user_id:
        user_id = trip.owner_user_id
    else:
        # Check membership
        is_member = trip.owner_user_id == user_id or db.query(TripMember).filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == user_id
        ).first() is not None
        if not is_member:
            raise HTTPException(status_code=403, detail="Uploader is not an authorized member of this trip")

    # Generate photo ID and save file
    pho_id = generate_id("pho")
    saved_filename = f"{pho_id}.jpg"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    photo_url = f"/static/uploads/{saved_filename}"

    if upload_file:
        contents = await upload_file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    else:
        # Minimal empty JPEG header for demonstration if no binary was passed
        with open(file_path, "wb") as f:
            f.write(b"")

    # Persist in Neon DB photos table
    db_photo = Photo(
        photo_id=pho_id,
        trip_id=trip_id,
        uploader_id=user_id,
        photo_url=photo_url,
        processing_status="completed",
        created_at=datetime.now(timezone.utc),
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    # Trip-scoped member matching
    # Query only members of this specific trip to preserve privacy and bounded scope
    trip_members = db.query(TripMember).filter(TripMember.trip_id == trip_id).all()
    candidate_user_ids = list(set([m.user_id for m in trip_members] + [trip.owner_user_id]))

    tagged_members: List[Dict[str, Any]] = []

    # Safe call to separate DeepFace service if available
    try:
        import httpx
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.post(
                f"{DEEPFACE_SERVICE_URL}/api/face/match-trip-photo",
                json={"photo_url": photo_url, "candidate_user_ids": candidate_user_ids}
            )
            if resp.status_code == 200:
                matches = resp.json().get("matches", [])
                for m in matches:
                    matched_uid = m.get("user_id")
                    confidence = m.get("confidence", 0.95)
                    pp = PhotoPerson(
                        pp_id=generate_id("pp"),
                        photo_id=pho_id,
                        user_id=matched_uid,
                        confidence=confidence,
                        created_at=datetime.now(timezone.utc),
                    )
                    db.add(pp)
                    tagged_members.append({"user_id": matched_uid, "confidence": confidence})
                db.commit()
    except Exception as e:
        # DeepFace is a separate service; if offline, log and degrade gracefully
        logger.info(f"DeepFace service skipped or offline at {DEEPFACE_SERVICE_URL}: {e}")

    return {
        "status": "uploaded",
        "phoId": db_photo.photo_id,
        "photo_id": db_photo.photo_id,
        "trpId": db_photo.trip_id,
        "trip_id": db_photo.trip_id,
        "uploader_id": db_photo.uploader_id,
        "photo_url": db_photo.photo_url,
        "caption": caption or title or "Trip Memory",
        "processing_status": db_photo.processing_status,
        "tagged_members": tagged_members,
        "created_at": db_photo.created_at.isoformat(),
    }


@router.get("/photos/{trp_id}")
def get_trip_photos(
    trp_id: str,
    folder: Optional[str] = None,
    taggedUserId: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve all photos for a trip directly from Neon PostgreSQL."""
    trip = db.query(Trip).filter(Trip.trip_id == trp_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip '{trp_id}' not found")

    query = db.query(Photo).filter(Photo.trip_id == trp_id).order_by(Photo.created_at.desc())
    photos = query.all()

    results = []
    for p in photos:
        uploader = db.query(User).filter(User.user_id == p.uploader_id).first()
        tagged = db.query(PhotoPerson).filter(PhotoPerson.photo_id == p.photo_id).all()
        tagged_users = []
        for t in tagged:
            u = db.query(User).filter(User.user_id == t.user_id).first()
            tagged_users.append({
                "user_id": t.user_id,
                "name": u.full_name if (u and hasattr(u, "full_name")) else t.user_id,
                "confidence": float(t.confidence) if t.confidence is not None else 0.95
            })

        if taggedUserId and not any(t["user_id"] == taggedUserId for t in tagged_users):
            continue

        results.append({
            "photo_id": p.photo_id,
            "trip_id": p.trip_id,
            "photo_url": p.photo_url,
            "processing_status": getattr(p, "processing_status", "completed"),
            "uploader_id": p.uploader_id,
            "uploader_name": uploader.full_name if (uploader and hasattr(uploader, "full_name")) else "Traveler",
            "created_at": p.created_at.isoformat(),
            "tagged_users": tagged_users,
        })

    return results


@router.get("/photos/memories/{trp_id}")
def get_memories_boards(trp_id: str, usrId: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve categorized Memories boards for a trip."""
    trip = db.query(Trip).filter(Trip.trip_id == trp_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail=f"Trip '{trp_id}' not found")

    photos = db.query(Photo).filter(Photo.trip_id == trp_id).order_by(Photo.created_at.desc()).all()

    all_board = []
    my_board = []
    folders: Dict[str, List[Any]] = {"GroupPhotos": [], "Scenery": []}

    for p in photos:
        tagged = db.query(PhotoPerson).filter(PhotoPerson.photo_id == p.photo_id).all()
        tagged_uids = [t.user_id for t in tagged]

        photo_item = {
            "photo_id": p.photo_id,
            "photo_url": p.photo_url,
            "processing_status": getattr(p, "processing_status", "completed"),
            "uploader_id": p.uploader_id,
            "created_at": p.created_at.isoformat(),
            "tagged_user_ids": tagged_uids,
        }
        all_board.append(photo_item)

        if usrId and (p.uploader_id == usrId or usrId in tagged_uids):
            my_board.append(photo_item)

        if len(tagged_uids) >= 2:
            folders["GroupPhotos"].append(photo_item)
        elif len(tagged_uids) == 0:
            folders["Scenery"].append(photo_item)

    return {
        "trpId": trp_id,
        "boards": {
            "all": all_board,
            "my": my_board,
            "folders": folders,
        }
    }
