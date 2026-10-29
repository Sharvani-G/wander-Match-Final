import os
import json
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from . import models  # ensure all ORM models are registered
from .websocket_manager import ws_manager

# Ensure Base metadata is loaded
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WanderMatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://wandermatch.vercel.app", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static uploads directory
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
os.makedirs(os.path.join(static_dir, "uploads"), exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Health check
@app.get("/api/health")
def health():
    return {"status": "ok"}

# Authenticated Trip-Scoped WebSocket Hub with Token Verification, Anti-Forgery & Snapshot Resync
@app.websocket("/ws/trips/{trip_id}/{user_id}")
@app.websocket("/ws/trips/{trip_id}")
async def websocket_trip_endpoint(
    websocket: WebSocket,
    trip_id: str,
    user_id: Optional[str] = None,
    token: Optional[str] = Query(None)
):
    if not token:
        token = websocket.query_params.get("token")
    if not token:
        auth_hdr = websocket.headers.get("authorization")
        if auth_hdr and auth_hdr.startswith("Bearer "):
            token = auth_hdr[7:].strip()

    db: Session = next(get_db())
    auth_uid = None
    try:
        auth_uid = await ws_manager.authenticate_and_connect(
            websocket=websocket,
            trip_id=trip_id,
            path_user_id=user_id,
            token=token,
            db=db
        )
        if not auth_uid:
            return  # Connection closed with 4401 or 4403

        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif msg.get("type") == "chat":
                    await ws_manager.broadcast_to_trip(trip_id, msg)
            except Exception:
                pass
    except WebSocketDisconnect:
        if auth_uid:
            ws_manager.disconnect(trip_id, auth_uid)
    finally:
        db.close()

# Import & register routers
from .routers import auth, trips, matching, face, photos, consensus
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(trips.router, prefix="", tags=["trips"])
app.include_router(matching.router, prefix="", tags=["matching"])
app.include_router(face.router, prefix="", tags=["face"])
app.include_router(photos.router, prefix="", tags=["photos"])
app.include_router(consensus.router, prefix="", tags=["consensus"])
