# WanderMatch — Panchami's Transport & DeepFace Engineering Specification

**Document Authority**: Panchami P (Backend Transport, Schemas, WebSocket & DeepFace Microservice Owner)  
**Status**: Authoritative Track Specification (`[ACTIVE]`)  
**Shared System of Record**: [`docs/INTEGRATION_CONTRACT.md`](INTEGRATION_CONTRACT.md)  
**Authoritative Decision Register**: [`docs/AI.md § 12`](AI.md#12-stack-neutral-decision-register)  
**Applicability**: Panchami P (Transport & DeepFace Microservice)  
**Governance Rule**: Following this consistency repair, **Panchami solely edits this document**. Cross-boundary contract updates are managed by Sharvani in `docs/INTEGRATION_CONTRACT.md`.

## WanderMatch · KogniVera Hackathon 2026 · PS-11

---

## HOW TO USE THIS DOC (Read this first, give it to your agent verbatim)

> "I am Panchami P, Backend Transport & DeepFace microservice developer for WanderMatch at KogniVera Hackathon 2026. Read this entire document carefully. It contains my full project context, my exact responsibilities across FastAPI routing, Pydantic wire validation schemas, WebSocket broadcast management, the DeepFace face recognition microservice, every API endpoint I must build, the exact persistence functions I call from Sharvani's service layer in-process, and my phase-by-phase execution plan. After reading, give me a detailed prompt to execute Phase [X] of my work. Do not assume anything not written here. Everything is specified."

---

## Phase-based reading guide

This is a structure-only reorganization. All original specifications, examples, ownership rules, pending decisions and execution checklists are retained below.

Use the phases as a reading and working sequence. Existing numbered section titles remain intact for cross-document references. The original hour-based plan is retained in Phase 6; it is not a new delivery estimate. Work can proceed in parallel using the documented mocks and agreed interfaces. Pending decisions and implementation prerequisites remain pending.

- [Phase 1 — Understand ownership, project context and file boundaries](#member-phase-1)
- [Phase 2 — Establish transport contracts and independent test seams](#member-phase-2)
- [Phase 3 — Wire application transport, identity and WebSockets](#member-phase-3)
- [Phase 4 — Implement feature endpoints and the DeepFace integration](#member-phase-4)
- [Phase 5 — Investigate cross-member performance](#member-phase-5)
- [Phase 6 — Follow the execution checklist and integration checkpoints](#member-phase-6)


<a id="member-phase-1"></a>
## Phase 1 — Understand ownership, project context and file boundaries

Read the retained sections below together for this phase:

- 0. OWNERSHIP LEDGER & LIFECYCLE DISTINCTION
- 1. WHAT WANDERMATCH IS — FULL CONTEXT
- 2. TECH STACK — EXACTLY WHAT YOU USE
- 5. DIRECTORY STRUCTURE — WHAT PANCHAMI OWNS
- 14. DEPENDENCY MAP — WHAT YOU NEED FROM OTHERS AND WHEN
- 15. PROHIBITED ANTIPATTERNS ("WHAT YOU MUST NEVER DO")

## 0. OWNERSHIP LEDGER & LIFECYCLE DISTINCTION

This section establishes Panchami's unambiguous ownership boundary, future structural plans, and lifecycle progression in accordance with `docs/INTEGRATION_CONTRACT.md`.

### A. Current Owned Files
Panchami solely owns the HTTP/WebSocket transport layer and the complete DeepFace microservice:
- **FastAPI Transport Layer (`backend/app/`)**:
  - `backend/app/routers/` (`[CURRENT]`): `auth.py`, `trips.py`, `matching.py`, `consensus.py`, `photos.py`, `face.py`
  - `backend/app/schemas/` (`[CURRENT]`): all wire Pydantic request/response models (`trip.py`, `matching.py`, `user.py`; standalone `proposal.py`, `vote.py`, `branch.py`, `chat.py`, `photo.py` are `[PROPOSED]` modular extractions from inline router schemas)
  - `backend/app/websocket_manager.py` (`[CURRENT]`): WebSocket connection lifecycle, room subscriptions, broadcast dispatch
  - `backend/static/uploads/` (`[CURRENT]`): local photo storage directory (verified path on disk: `backend/static/uploads/`, NOT `backend/app/static/uploads/`)
- **DeepFace Face Recognition Microservice (`ai/DeepFace/`)**:
  - `ai/DeepFace/backend/main.py` (`[CURRENT]`): FastAPI worker on port 8001
  - `ai/DeepFace/backend/routers/` (`[CURRENT]`): `face.py`, `photos.py`, `trips.py`
  - `ai/DeepFace/backend/services/face/` (`[CURRENT]`): `matching.py`, `models.py`, `registration.py`
  - `ai/DeepFace/backend/database.py` (`[CURRENT]`): microservice SQLite connection
  - `ai/DeepFace/tests/` (`[CURRENT]`): test suite for face detection and matching
  - `ai/DeepFace/requirements.txt` (`[CURRENT]`), `README.md` (`[CURRENT]`), `wandermatch.db` (`[CURRENT]`), `demo_verify_deepface.py` (`[CURRENT]`)
- **Ownership Exclusions**:
  - Sharvani owns `backend/app/main.py`, shared startup wiring, and all deployment coordination (including frontend deployment to Vercel and backend/worker deployment to Render).
  - Sharvani owns all shared ORM models (`backend/app/models/provided.py`, `models/additive.py`), database connection engine (`backend/app/database.py`), Alembic migrations (`backend/alembic/`), and business domain services (`backend/app/services/`).
  - Nikitha owns the complete frontend implementation (`frontend/`).
  - The active team has exactly three members: Nikitha, Panchami and Sharvani. Former-team contributor Nithya has zero active responsibilities; her prototype work is archived under `docs/archive/former-team/NITHYA.md`.

### B. Proposed Future Files (Pending Implementation Approval)
When backend architectural modularization is approved:
- `backend/app/adapters/face_recognition_adapter.py` (`[PROPOSED]`): Resilient HTTP client communicating with DeepFace worker (`http://localhost:8001`), supporting multipart binary streaming, candidate embeddings payload forwarding, timeouts, and circuit breaking.
- `backend/app/adapters/storage_adapter.py` (`[PROPOSED]`): Storage abstraction layer (local disk storage now, Cloudinary preset integration later per Decision #9).
- `backend/app/schemas/proposal.py`, `vote.py`, `branch.py`, `chat.py`, `photo.py` (`[PROPOSED]`): Dedicated Pydantic wire models extracted from inline router definitions.
- `ai/DeepFace/Dockerfile` (`[PROPOSED]`): Container deployment image.
- `ai/DeepFace/models/` (`[PROPOSED]`): Local pre-trained model weights cache.

### C. Thin Router Boundary & In-Process Persistence Calls
1. **Thin Router Boundary**: Routers strictly perform HTTP/WebSocket transport:
   - Deserializing incoming JSON and validating Pydantic request schemas.
   - Extracting trusted caller identity from Clerk JWT auth dependency (`current_user = Depends(get_current_user)`).
   - **Invoking Sharvani's domain persistence services in-process via Python function calls** (passing the active SQLAlchemy `Session = Depends(get_db)`).
   - Mapping domain exceptions into RFC 7807 Problem Details HTTP responses.
   - Triggering WebSocket broadcast events through `websocket_manager` **strictly after** domain service commits the database transaction.
   - Serializing and returning Pydantic response models.
2. **Strict In-Process Prohibition on "Port 8000" Calls**:
   - Panchami's FastAPI router handlers run in the **same process** as Sharvani's domain services.
   - Routers **never** make HTTP requests to `http://localhost:8000` to save data. They call Python functions directly: `sharvani_trip_service.create_trip(db, creator_user_id=current_user.user_id, data=payload.model_dump())`.
   - HTTP networking is reserved strictly for external clients (browser calling backend) or the separate DeepFace worker microservice on port 8001.
3. **Photo Service Persistence Boundary**:
   - Panchami owns photo upload transport orchestration (`POST /api/photos`).
   - To persist records, Panchami calls Sharvani's explicit service functions in-process:
     ```python
     # 1. Fetch candidate member embeddings for matching
     candidates = sharvani_photo_service.get_candidate_member_embeddings(db, trip_id)
     # 2. Persist parent photo record with pending status
     photo = sharvani_photo_service.save_uploaded_photo_record(
         db, photo_id=pho_id, trip_id=trip_id, uploader_id=current_user.user_id, photo_url=photo_url, initial_status="pending"
     )
     # 3. Stream multipart image bytes + candidate vectors to DeepFace worker on port 8001
     matches = await face_adapter.match_photo(image_bytes, candidates)
     # 4. Persist face tags and update status
     # Database storage status: 'processed' on worker success, 'failed' on worker error/timeout
     # (Worker failure/timeout must NEVER map to 'processed' or 'completed')
     storage_status = "processed" if matches.is_success else "failed"
     persisted_tags = sharvani_photo_service.save_photo_tags_records(
         db=db,
         photo_id=pho_id,
         face_matches=matches.tags,
         final_status=storage_status
     )
     ```

4. **Consensus Algorithm Independence (Zero Consensus Logic in Routers)**:
   - Panchami's routers (`routers/consensus.py`) do **NOT** implement voting business logic, deadline calculations, candidate synthesis, Pareto scoring, or branch partitioning algorithms.
   - Routers strictly:
     1. Validate Pydantic request models and headers (`Idempotency-Key`, `expectedVersion`).
     2. Extract trusted caller identity (`current_user = Depends(get_current_user)`).
     3. Invoke Sharvani's domain services in-process:
        - `sharvani_voting_service.cast_vote(db, proposal_id, user_id, value, comment)`
        - `sharvani_consensus_service.check_and_expire_timer(db, proposal_id)`
        - `sharvani_consensus_service.run_consensus_round(db, itm_id)`
        - `sharvani_consensus_service.apply_negotiation_selection(db, user_id, payload)`
     4. Map domain exceptions into RFC 7807 responses (`409 Conflict` on `VersionConflictError` or `WindowClosedError`).
     5. Dispatch WebSocket broadcasts (`aiPlanGenerated`, `consensus.clarification_requested`, `slotStatusChanged`) **strictly after** the domain transaction has committed to PostgreSQL.

### D. Trusted Identity & Request Boundary Rules
1. **Verified Actor Identity**:
   - The actor performing ANY operation is derived strictly from verified credentials (`current_user.user_id`), NOT from request bodies (`payload.userId`, `payload.usrId`, `proposedByUserId`).
   - If a legacy body contains an identity field for backwards compatibility, it MUST be either validated to match `current_user.user_id` or ignored in favor of `current_user.user_id`. It must NEVER override the authenticated actor.
2. **Actor vs Target Member vs Resource Identifiers**:
   - `current_user.user_id`: Authenticated caller executing the request.
   - `target_user_id`: Target of an administrative action (e.g., approving a join request or adding a member).
   - `trp_id`, `itm_id`, `prp_id`, `brc_id`, `msg_id`: Resource identifiers identifying domain entities.

### E. Later Feature Implementation (Feature Phase — Not Yet Approved)
- **WebSocket Auth Handshake**: Enforce JWT validation on connection query string: `ws://.../ws/trips/{trip_id}?token=...`.
  - Missing or expired token: reject with WebSocket close code `4401`.
  - Valid user who is not an accepted trip member: reject with WebSocket close code `4403`.
- **Cloudinary Storage Adapter**: Implement Cloudinary upload preset and folder hierarchy (`/wandermatch/{trip_id}/...`) per Decision #9.
- **Webhook Signature Verification**: Add cryptographic signature validation for Clerk webhooks via `svix`.
- **Pending Decision Boundary**: Unresolved architecture decisions in `docs/AI.md § 12` (e.g. Decision #30 for PDF rendering or Decision #31 for voting window duration) block only dependent implementation details; they do not block transport route wiring, input validation, or in-process service handoffs.

### F. Mock-Only Completion Criteria & Independent Transport Testing
Panchami can declare complete transport and microservice readiness when:
1. All FastAPI routers respond with correct status codes, Pydantic schemas, and RFC 7807 error shapes using injectable mock domain services (`FakeConsensusService`, `FakeTripService`).
2. WebSocket manager broadcasts all events (`voteCast`, `proposalCreated`, `slotStatusChanged`, `aiRecommendationReady` / `aiPlanGenerated`, `resyncSnapshot`) to mock clients.
3. DeepFace microservice tests pass with real reference images in an isolated test environment.
4. **Zero-Dependency Transport Independence**: Panchami's mock router test suite executes with **ZERO database, ZERO LLM, and ZERO worker dependencies**.
5. **No Local LLM Installation Required**: **Consensus SLM/LLM installation (Ollama / Phi-4-mini) is strictly owned by Sharvani**. Panchami requires **ZERO** local Ollama installation to build, test, and complete all transport and WebSocket functionality.

### G. Real Integrated Completion Criteria & Neon Database Handoff Protocol
Full integrated completion is achieved when:
1. **Neon Environment Handoff Protocol & Small Bounded Fixture**:
   - **Sharvani's Provisioning Responsibility**: Sharvani provisions the isolated nonproduction Neon PostgreSQL database target, runs Alembic migrations up to agreed baseline revision `c8a6a4789a32` (or current `head`), and seeds the agreed small, bounded test fixture.
   - **Small Bounded Test Fixture**:
     * Synthetic Users: `usr_alice` (`role='owner'`), `usr_bob` (`role='editor'`), `usr_carol` (`role='viewer'`) (mapped to canonical `TripMember.role` values `owner / editor / viewer`).
     * Synthetic Trips: `trp_paris_2026` ("Paris Weekend", Mode NA, published), `trp_tokyo_admin` ("Tokyo Explorer", Mode A, draft).
     * Representative Slots: `slt_day1_morning` ("Louvre Guided Tour", 09:00–12:00, 30.00 USD), `slt_day1_lunch` ("Le Marais Bistro", 12:30–14:00, 25.00 USD).
     * Representative Proposals & Votes: `prp_louvre_guided` with initial YES votes from `usr_alice` and `usr_bob`.
     * Minimal Photo Metadata: `pho_sample_1` (`trip_id: trp_paris_2026`, `uploader_id: usr_alice`, `photo_url: /static/uploads/pho_sample_1.jpg`).
   - **Explicit Environment Loading**: Python / FastAPI does **NOT** automatically load `.env.local` by default unless configured via `python-dotenv` (`load_dotenv(".env.local")`) or shell environment variables. Nonproduction credentials must be shared privately; no secrets in version control.
   - **Console vs Database Access**: Panchami receives direct database connection credentials (`DATABASE_URL=postgresql://panchami_dev:...@...neon.tech/wandermatch_test?sslmode=require` or `postgresql+psycopg2://...`); no shared personal Neon account login is required. (Note: `backend/app/database.py` initializes a synchronous SQLAlchemy `create_engine` using `psycopg2-binary`. The asynchronous prefix `postgresql+asyncpg://` is an unapproved future proposal that is incompatible with the present synchronous backend engine; Panchami uses the synchronous driver string matching `psycopg2-binary`).
   - **Panchami's Consumption Responsibility**: Panchami consumes the prepared environment feature-by-feature during real integration.
   - **Zero Blocker**: Mock transport development and router unit testing must **NEVER wait** for live Neon database access.
2. FastAPI backend boots against Sharvani's live Neon PostgreSQL database.
3. Routers invoke Sharvani's live transactional services with verified CAS optimistic concurrency.
4. Photo upload route (`POST /api/photos`) streams real multipart image bytes + candidate vectors to DeepFace worker on port 8001, tags detected faces, saves records via Sharvani's persistence functions in-process, and broadcasts updates over WebSocket.

---

## 1. WHAT WANDERMATCH IS — FULL CONTEXT

WanderMatch is a social group travel planning web app. Groups plan trips together on a shared live itinerary. Members propose activities, vote YES or NO (NO votes REQUIRE a typed reason), and an AI layer reads those typed reasons to generate compromise plans or — when preferences are truly incompatible — parallel branches.

### Two trip modes:
- **Mode A (Admin-Led)**: Trip owner has final authority. AI only recommends. Admin can extend rounds, force branches, or accept proposals directly.
- **Mode NA (Collaborative)**: Fully automatic. First NO vote starts a slot-level timer (`slot_consensus.closes_at`, currently 10 minutes in code pending product sign-off per Decision #31). All competing proposals share this deadline. After ~3 rounds, AI auto-branches. No human override needed.

---

## 2. TECH STACK — EXACTLY WHAT YOU USE

- **Framework**: FastAPI (Python 3.11+)
- **Server**: Uvicorn
- **Wire Validation**: Pydantic v2 (with explicit alias generator for camelCase wire representation)
- **WebSocket**: FastAPI native WebSocket + connection manager (`websocket_manager.py`)
- **Recognition Microservice**: DeepFace (ArcFace 512-d embeddings, RetinaFace/MTCNN detector) on Port 8001
- **Deployment Coordination**: Owned by Sharvani (Render web service for backend and worker; Vercel for frontend)

You OWN:
- `backend/app/routers/` (`auth.py`, `trips.py`, `matching.py`, `consensus.py`, `photos.py`, `face.py`)
- `backend/app/schemas/` (all Pydantic request/response wire models)
- `backend/app/websocket_manager.py` (WebSocket connection lifecycle, rooms, and broadcast dispatch)
- `backend/static/uploads/` (local photo storage directory)
- Complete `ai/DeepFace/` microservice (`backend/main.py`, `routers/`, `services/face/`, `tests/`)

You DO NOT touch:
- `frontend/` (Nikitha owns this)
- Shared database models (`backend/app/models/provided.py`, `models/additive.py`) (Sharvani owns this)
- Database connection engine (`database.py`), Alembic migrations (`alembic/`), or seed script (`seed.py`) (Sharvani owns this)
- Business domain services (`backend/app/services/`) (Sharvani owns this — you call her functions in-process)
- Shared startup wiring (`backend/app/main.py`) and deployment coordination (Sharvani owns this)

---

## 5. DIRECTORY STRUCTURE — WHAT PANCHAMI OWNS

```
backend/app/
  routers/                     <-- [CURRENT] YOU OWN ALL 6 ROUTER MODULES
    auth.py                    <-- Mounts POST /api/auth/webhook, login, register, me, preferences, profile
    trips.py                   <-- Trip CRUD, publish, itinerary, join-requests, invite-code, chat
    matching.py                <-- Solo group & guide matching endpoints
    consensus.py               <-- Proposals, votes, timer check, reconcile, Mode A controls
    photos.py                  <-- POST /api/photos & trip photo queries
    face.py                    <-- Face enrollment & recognition endpoints
  schemas/                     <-- [CURRENT] YOU OWN ALL PYDANTIC WIRE MODELS
    user.py                    <-- [CURRENT]
    trip.py                    <-- [CURRENT]
    matching.py                <-- [CURRENT]
    proposal.py                <-- [PROPOSED] Target modular extraction
    vote.py                    <-- [PROPOSED] Target modular extraction
    branch.py                  <-- [PROPOSED] Target modular extraction
    chat.py                    <-- [PROPOSED] Target modular extraction
    photo.py                   <-- [PROPOSED] Target modular extraction
  websocket_manager.py         <-- [CURRENT] YOU OWN WEBSOCKET LIFECYCLE & BROADCAST
  static/uploads/              <-- [CURRENT] Local photo storage directory (verified: backend/static/uploads/)
  adapters/                    <-- [PROPOSED] Target adapter extractions
    face_recognition_adapter.py<-- HTTP client streaming multipart bytes + candidate vectors to port 8001
    storage_adapter.py         <-- Storage abstraction (local disk / Cloudinary)
  main.py                      <-- [CURRENT] App init & router mounts (Owned by Sharvani)
ai/DeepFace/                   <-- [CURRENT] YOU OWN ENTIRE DEEPFACE MICROSERVICE
  backend/
    main.py                    <-- [CURRENT] DeepFace FastAPI worker on Port 8001
    routers/                   <-- [CURRENT] face.py, photos.py, trips.py
    services/face/             <-- [CURRENT] matching.py, models.py, registration.py
    database.py                <-- [CURRENT] Microservice SQLite connection
  tests/                       <-- [CURRENT] Recognition test suite & test fixtures
  requirements.txt             <-- [CURRENT] Worker dependency manifest
  README.md                    <-- [CURRENT] Microservice operating runbook
  wandermatch.db               <-- [CURRENT] Local demo database
  demo_verify_deepface.py      <-- [CURRENT] Standalone verification script
  Dockerfile                   <-- [PROPOSED] Microservice container definition
  models/                      <-- [PROPOSED] Pre-trained weights cache directory
```

---

## 14. DEPENDENCY MAP — WHAT YOU NEED FROM OTHERS AND WHEN

| What you need | From whom | When | Related Decision |
|---|---|---|---|
| PostgreSQL database seeded & migrations applied | Sharvani | Phase 0 | Decision #16 |
| Shared ORM models (`models/provided.py`, `models/additive.py`) | Sharvani | Phase 0 | Decision #16 |
| `CLERK_SECRET_KEY` & `CLERK_WEBHOOK_SECRET` | Sharvani | Phase 0 | N/A |
| Domain service functions (`trip_service`, `voting_service`, `consensus_service`) | Sharvani | Phase 1–3 | Decision #27, #31 |
| Photo persistence functions (`save_uploaded_photo_record`, etc.) | Sharvani | Phase 4 | Decision #9, #18 |
| Deterministic scorer functions (`group_compatibility_scorer`, etc.) | Sharvani | Phase 5 | Decision #26 |
| Frontend integration verification (`VITE_USE_MOCK_DATA=false`) | Nikitha | Phase 6 | Decision #30 |
| Deployment coordination (Render backend/worker & Vercel frontend) | Sharvani | Phase 6–7 | Decision #3 |

---

## 15. PROHIBITED ANTIPATTERNS ("WHAT YOU MUST NEVER DO")

1. **Never send a relative filesystem URL** (e.g. `/static/uploads/pho_xxx.jpg`) to an external worker service. Always stream multipart bytes.
2. **Never describe persistence function calls as "on port 8000"**. You run in the same process as Sharvani's service layer; call Python functions directly.
3. **Never document or record a worker timeout/failure as successful completed recognition**. Set `processing_status = 'failed'`.
4. **Never expose 512-d ArcFace floating-point vectors** in client responses, logs, or debug output.
5. **Never categorize a group photo with detected faces as `folder:Scenery`**. Use `folder:GroupPhotos` with `unidentified_faces: true`.
6. **Never mix test `advance_minutes` parameters into production API contracts**.
7. **Never write raw database DDL or Alembic migrations** (Sharvani is the sole schema authority).
8. **Never write `value = 'abstain'` in any vote record**. Only binary `'yes'` or `'no'`.
9. **Never trust caller identity from request payload bodies** (`payload.userId`, `payload.usrId`). Caller is always `current_user.user_id`.
10. **Never silently overwrite itinerary versions** — always verify expected version and return HTTP 409 on conflict.
11. **Never alter `backend/app/main.py` startup wiring or deployment configurations** without Sharvani's explicit coordination.

<a id="member-phase-2"></a>
## Phase 2 — Establish transport contracts and independent test seams

Read the retained sections below together for this phase:

- 0.1 CONTRACT CONSISTENCY REFERENCE TABLE (PANCHAMI'S SURFACES)
- 3. VERIFIED SCHEMA & FIELD MAPPING REFERENCE
- 4. NAMING & SERIALIZATION CONTRACT
- 10. IN-PROCESS DOMAIN SERVICE HANDOFF SPECIFICATIONS & INDEPENDENT TEST DOUBLES
- 11. PYDANTIC WIRE MODELS (SCHEMAS)
- 12. RFC 7807 ERROR SPECIFICATION & MAPPING TABLE

## 0.1 CONTRACT CONSISTENCY REFERENCE TABLE (PANCHAMI'S SURFACES)

| Surface / Interface | Current Implementation `[CURRENT]` | Agreed Target Contract `[AGREED TARGET]` | Prohibited / Unapproved `[PROHIBITED]` | Ownership & Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **Photo Upload Endpoint** | `POST /api/photos` (`routers/photos.py:L29`). Form: `file`/`photo`, `trp_id`/`trpId`, `uploader_id`. Saves to `static/uploads/`, sends relative URL to worker, sets `completed` prematurely. | `POST /api/photos`. Form: `file: UploadFile` (binary), `trpId: str`. Panchami reads file, calls Sharvani persistence with initial `pending`, streams multipart bytes + candidate vectors to worker, updates DB with face matches. | `POST /api/photos/upload` (historical proposal; unapproved alias; clients MUST call `POST /api/photos`). Sending relative paths to worker. | **Panchami** owns route & worker forwarding; **Sharvani** owns photo and tag database persistence in-process. |
| **Clerk Webhook Endpoint** | `POST /api/auth/webhook` (`routers/auth.py:L88`). Extracts svix headers, verifies signature, creates `User` and `UserPreference`. | `POST /api/auth/webhook`. Panchami extracts headers & body, invokes Sharvani's `security.verify_svix_signature()`. Sharvani executes `security.sync_clerk_user_to_db()` in single atomic transaction. | `POST /api/webhooks/clerk` (historical proposal; unapproved alias; Clerk must be configured to `POST /api/auth/webhook`). | **Panchami** owns HTTP endpoint; **Sharvani** owns cryptographic verification & DB user sync in-process. |
| **Timer Check Endpoint** | `POST /api/proposals/check-timer` (`routers/consensus.py:L693`). Accepts `prp_id`, `advance_minutes`. If window expired with 0 NO votes, auto-confirms slot. | `POST /api/proposals/check-timer`. Production contract evaluates `now >= slot_consensus.closes_at` without test parameters. `advance_minutes` restricted strictly to automated test fixtures. | Calling `POST /api/consensus/check-timer` (unmounted alias; route is `/api/proposals/check-timer`). Exposing test clock controls in production payloads. | **Panchami** exposes HTTP route; **Sharvani** owns authoritative countdown state machine in-process. |
| **Trip Chat Messages** | `GET /api/trips/{trip_id}/chat` & `POST /api/trips/{trip_id}/chat` (`routers/trips.py:L960, L991`). Returns chat history with sender details. | `GET /api/trips/{trip_id}/chat` & `POST /api/trips/{trip_id}/chat`. Canonical unified endpoints. Frontend `api.ts` aligned. | Calling `/api/trips/{trip_id}/messages` or `/api/messages` or `/api/chat/{tripId}` (stale aliases; must align to canonical). | **Panchami** owns HTTP transport; **Sharvani** owns message persistence in-process. |
| **Mode A Endpoints** | Mounted under `/api/consensus/mode-a/*` (`consensus.py:L414, L465, L508, L572, L607`). | `POST /api/consensus/mode-a/invoke`, `/accept`, `/force-branch`, `/extend`, `/direct-confirm`. | Mislabeled `/api/mode-a/*` (unmounted route; must use full prefix `/api/consensus/mode-a/*`). | **Panchami** exposes HTTP routes; **Sharvani** enforces owner permissions and executes transitions. |
| **Direct Membership Addition** | Join requests (`/join-request`), approvals (`/approve`), invite codes (`/invite-code`), join by code (`/join-by-code`) are implemented in `trips.py`. Direct `POST /api/trips/{trp_id}/members` does NOT exist in code. | `POST /api/trips/{trp_id}/members` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`. Direct addition route by trip owner. | Describing `POST /api/trips/{trp_id}/members` as current implementation before it is written. | **Panchami** implements router endpoint; **Sharvani** enforces capacity & authorization. |
| **WebSocket Connection & Resync** | `ws://host/ws/trips/{trip_id}/{user_id}` (`websocket_manager.py`). Verifies token & membership; immediately sends `{"type": "resyncSnapshot", "snapshot": {...}}`. | `ws://host/ws/trips/{trip_id}?token=...`. Panchami verifies token query, checks membership, and delivers `{"type": "resyncSnapshot", ...}` on connection and reconnect. | Silently renaming `resyncSnapshot` to `tripStateSnapshot` without coordinating with backend. | **Panchami** manages connection lifecycle & broadcast; **Nikitha** handles `resyncSnapshot` in `TripContext`. |
| **WebSocket Event: AI Plan Broadcast** | Backend emits `{"type": "aiRecommendationReady", ...}` (`consensus.py:L452, L684`). | Backend emits both `aiPlanGenerated` and `aiRecommendationReady` as aliases to maintain complete frontend and backend compatibility. | Dropping either event without unified client adapter update. | **Panchami** broadcasts event; **Nikitha** handles event in `TripContext.tsx`. |
| **Vote Invariants** | `POST /api/votes` (`routers/consensus.py:L274`). Writes `yes` or `no`. Retracts existing vote on same proposal only. | `POST /api/votes`. Mandatory typed reason when `value === 'no'`. Retracts prior YES on competing proposal in same slot (`AC-VOT-02`). Idempotent re-voting. | Writing `value: 'abstain'` (strictly prohibited; only binary `yes` or `no` permitted). Claiming competing YES retraction is already working. | **Sharvani** enforces invariants in `voting_service.py` in-process; **Panchami** maps validation to HTTP 400. |
| **Itinerary Concurrency** | Verifies `itineraries.version`. Bumps `version = version + 1`. Returns HTTP 409 on mismatch. | Atomic CAS update: `UPDATE itineraries SET version = version + 1 WHERE itinerary_id = :id AND version = :expected`. | Application-level read-then-write without atomic CAS in database transaction. | **Sharvani** implements atomic CAS query; **Panchami** maps conflict to HTTP 409. |
| **Face Profile Registration** | `POST /api/face/register` (`routers/face.py:L14`). Stores metadata in SQLite; does not call DeepFace worker. | `POST /api/face/register`. Accepts 3 enrollment images, forwards to worker for 512-d ArcFace vector extraction, persists in `face_profiles`. | Claiming current `face.py` already performs worker inference. | **Panchami** handles multi-image transport; **Sharvani** persists `FaceProfile` record in-process. |

---

## 3. VERIFIED SCHEMA & FIELD MAPPING REFERENCE

> [!IMPORTANT]
> **Schema Authority Notice**: Sharvani solely owns all database models, DDL definitions, and Alembic migrations. Historical database snippets must **not** be presented as verified current DDL. Panchami does not maintain independent DDL tables.
> 
> Direct references to authoritative definitions:
> - Canonical PS-11 Tables (D1–D9): [`backend/app/models/provided.py`](../backend/app/models/provided.py) and [`docs/data/schema.sql`](data/schema.sql)
> - WanderMatch Additive Tables: [`backend/app/models/additive.py`](../backend/app/models/additive.py) and Alembic migration [`c8a6a4789a32`](../backend/alembic/versions/c8a6a4789a32_initial_schema_baseline.py)
> - Additive Tables Verified on Disk: `join_requests`, `slot_consensus`, `branches`, `branch_members`, `revision_history`, `trip_chat_messages`, `face_profiles`, `photos`, `photo_person` (mapped to model `PhotoPerson`), `trip_invite_codes`. Note: `photo_tags` does NOT exist as an independent table.
> - Schema Migration Prerequisite: `SlotConsensus.closes_at` is missing in current schema; it is an explicit migration prerequisite for authoritative countdown timer storage.
> - Enumeration Values: [`docs/data/enums.json`](data/enums.json)

### Explicit Wire Field Mapping & Alias Table

Pydantic's automatic `to_camel` converts snake_case words by capitalizing subsequent words (`user_id` -> `userId`, `proposal_id` -> `proposalId`). To support legacy shortened wire abbreviations (`usrId`, `prpId`, `trpId`, `itmId`, `votId`, `phoId`), the following explicit mapping is maintained in Pydantic schemas:

| Canonical Entity | Internal Model Column | Canonical Wire Name | Approved Short Alias | Wire Type / Constraint | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **User** | `user_id` | `userId` | `usrId` | `str` (`usr_...`) | Caller identity derived from JWT |
| | `display_name` | `displayName` | — | `str` | Public profile display name |
| | `clerk_user_id` | `clerkUserId` | — | `str` | External Clerk subject ID |
| **Trip** | `trip_id` | `tripId` | `trpId` | `str` (`trp_...`) | Resource identifier |
| | `owner_user_id` | `ownerUserId` | — | `str` (`usr_...`) | Trip creator |
| | `mode` | `mode` | — | `str` (`Mode A` \| `Mode NA`) | Trip governance mode |
| **Itinerary** | `itinerary_id` | `itineraryId` | `itnId` | `str` (`itn_...`) | Itinerary container |
| | `version` | `version` | — | `int` (>= 1) | Monotonic CAS counter |
| **Itinerary Item** | `item_id` | `itemId` | `itmId` | `str` (`itm_...`) | Slot identifier |
| | `cost` | `cost` | — | `str` (Decimal string) | e.g. `"15.00"`, never float |
| **Slot Consensus**| `slot_status` | `slotStatus` | — | `str` (`EMPTY` \| `IN_CONSENSUS` \| `BRANCHED` \| `CONFIRMED`) | Located in `slot_consensus` |
| | `current_round` | `currentRound` | — | `int` (1..3) | Consensus round index |
| | `consensus_cycle`| `consensusCycle`| — | `int` (>= 1) | Reconcile cycle index |
| | `closes_at` | `closesAt` | — | `str \| null` (ISO 8601) | Slot countdown deadline (migration req.) |
| **Proposal** | `proposal_id` | `proposalId` | `prpId` | `str` (`prp_...`) | Proposal identifier |
| | `target_item_id` | `targetItemId` | `itmId` | `str` (`itm_...`) | Contested slot reference |
| | `rationale` | `rationale` | — | `str` | Non-empty text (NOT description) |
| | `cost_delta` | `costDelta` | — | `str` (Decimal string) | e.g. `"+10.00"`, NOT estimatedCost |
| | `status` | `status` | — | `str` (`open` \| `accepted` \| `rejected` \| `expired` \| `QUEUED`) | `QUEUED` when slot window active |
| **Vote** | `vote_id` | `voteId` | `votId` | `str` (`vot_...`) | Vote identifier |
| | `value` | `value` | — | `str` (`yes` \| `no`) | Binary only; NO `abstain` |
| | `comment` | `comment` | — | `str \| null` | Mandatory trimmed string when NO |
| **Branch** | `branch_id` | `branchId` | `brcId` | `str` (`brc_...`) | Branch identifier |
| | `track_label` | `trackLabel` | — | `str` (e.g. `"Track A"`) | Display label |
| | `status` | `status` | — | `str` (`OPEN` \| `FINALIZED`) | Branch lifecycle status |
| **Chat Message** | `message_id` | `messageId` | `msgId` | `str` (`msg_...`) | Message identifier |
| | `content` | `content` | — | `str` | Message text |
| **Photo** | `photo_id` | `photoId` | `phoId` | `str` (`pho_...`) | Photo identifier |
| | `processing_status`| `processingStatus`| — | `str` (`pending` \| `completed` \| `failed`) | Async recognition state |
| | `photo_url` | `photoUrl` | — | `str` | Public web asset URL |
| | `embedding_data` | **EXCLUDED** | **OMITTED** | N/A | Strictly server-internal vector |

---

## 4. NAMING & SERIALIZATION CONTRACT

1. **Database & Internal Python**: Strict `snake_case` always (`user_id`, `proposal_id`, `cost_delta`, `closes_at`).
2. **FastAPI JSON Responses**: Strict `camelCase` always with explicit alias support (`userId` / `usrId`, `proposalId` / `prpId`).
3. **Money Representation**: Stored as `DECIMAL(12,2)` in database; serialized strictly as formatted `string` in JSON responses (`"15.00"`). Never use floating-point numbers.
4. **WebSocket Event Types**: Reconciled verb-first camelCase event names:
   - `resyncSnapshot`: Sent on connect/reconnect with full trip state.
   - `proposalCreated`: Broadcast when a new proposal is submitted.
   - `voteCast`: Broadcast when a vote is cast.
   - `slotStatusChanged`: Broadcast when slot status transitions (`EMPTY`, `IN_CONSENSUS`, `BRANCHED`, `CONFIRMED`).
   - `aiRecommendationReady` & `aiPlanGenerated`: Emitted dual-event when an AI compromise plan is ready.
   - `branchConfirmed`: Broadcast when a member confirms a branch.
5. **Entity ID Prefixes**: Strict canonical prefixes (`usr_`, `prf_`, `trp_`, `tmb_`, `itn_`, `itm_`, `prp_`, `vot_`, `gid_`, `brc_`, `bmb_`, `rev_`, `msg_`, `fcp_`, `pho_`, `pp_`).

---

## 10. IN-PROCESS DOMAIN SERVICE HANDOFF SPECIFICATIONS & INDEPENDENT TEST DOUBLES

Panchami's routers call Sharvani's domain services **in-process** via Python function calls passing the active database session. To enable 100% independent development and unit testing without waiting for domain logic, database, or LLM infrastructure, Sharvani defines abstract service protocols, and Panchami implements representative in-memory fake services.

### 10.1 Injectable Service Interfaces & Protocols
These protocols define the authoritative method signatures. All callers, fakes, and domain implementations must match these exact parameter names and types:
```python
from typing import Protocol, List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

class IDomainTripService(Protocol):
    def list_user_trips(self, db: Session, user_id: str) -> List[Any]: ...
    def get_trip_detail(self, db: Session, trip_id: str, user_id: str) -> Dict[str, Any]: ...
    def create_trip(self, db: Session, creator_user_id: str, data: Dict[str, Any]) -> Any: ...
    def publish_trip(self, db: Session, trip_id: str, user_id: str) -> Any: ...
    def is_user_authorized_member(self, db: Session, trip_id: str, user_id: str) -> bool: ...

class IDomainVotingService(Protocol):
    def cast_vote(self, db: Session, proposal_id: str, user_id: str, value: str, comment: Optional[str] = None, weight: float = 1.0) -> Any: ...

class IDomainConsensusService(Protocol):
    def check_and_expire_timer(self, db: Session, proposal_id: str) -> Dict[str, Any]: ...
    def reconcile_slot(self, db: Session, proposal_id: str) -> Dict[str, Any]: ...
    def submit_clarification(
        self,
        db: Session,
        slot_id: str,
        comment_id: str,
        user_id: str,
        text: str,
        version: int,
        token: str
    ) -> Dict[str, Any]: ...

class IDomainPhotoService(Protocol):
    def get_candidate_member_embeddings(self, db: Session, trip_id: str) -> List[Dict[str, Any]]: ...
    def save_uploaded_photo_record(
        self,
        db: Session,
        photo_id: str,
        trip_id: str,
        uploader_id: str,
        photo_url: str,
        initial_status: str = "pending"
    ) -> Any: ...
    def save_photo_tags_records(
        self,
        db: Session,
        photo_id: str,
        face_matches: List[Dict[str, Any]],
        final_status: str = "processed"
    ) -> List[Dict[str, Any]]: ...
```

### 10.2 FastAPI Domain-Service Dependency Injection Seam
To enable routes to be tested with fakes without executing database queries or real domain services, routes obtain domain services through FastAPI dependencies (`[TARGET ARCHITECTURE]`):
```python
# Seam defined in backend/app/dependencies.py (or router module)
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db

def get_consensus_service(db: Session = Depends(get_db)) -> IDomainConsensusService:
    from backend.app.services import consensus_service
    return consensus_service

def get_trip_service(db: Session = Depends(get_db)) -> IDomainTripService:
    from backend.app.services import trip_service
    return trip_service

def get_photo_service(db: Session = Depends(get_db)) -> IDomainPhotoService:
    from backend.app.services import photo_service
    return photo_service
```

### 10.3 Representative In-Memory Fake Service (`FakeConsensusService`)
Panchami uses this standalone fake in `tests/test_routers_consensus.py` with **zero database, zero LLM, and zero external worker dependencies**:
```python
class FakeConsensusService:
    """In-memory fake implementing IDomainConsensusService for isolated transport testing."""
    def __init__(self):
        self.proposals = {
            "prp_test_1": {
                "proposal_id": "prp_test_1",
                "slot_id": "slt_test_1",
                "version": 1,
                "status": "ACTIVE_VOTING",
                "yes_votes": 2,
                "no_votes": 0
            }
        }
        self.clarifications = []

    def check_and_expire_timer(self, db: Any, proposal_id: str) -> Dict[str, Any]:
        if proposal_id not in self.proposals:
            raise KeyError(f"Proposal {proposal_id} not found")
        prop = self.proposals[proposal_id]
        return {"proposalId": proposal_id, "status": "CONFIRMED", "closedAt": "2026-10-29T12:00:00Z"}

    def reconcile_slot(self, db: Any, proposal_id: str) -> Dict[str, Any]:
        return {"proposalId": proposal_id, "status": "IN_CONSENSUS", "round": 2}

    def submit_clarification(
        self,
        db: Any,
        slot_id: str,
        comment_id: str,
        user_id: str,
        text: str,
        version: int,
        token: str
    ) -> Dict[str, Any]:
        if version != 1:
            raise ValueError("ERR_STALE_VERSION")
        record = {
            "status": "CLARIFICATION_ACCEPTED",
            "slotId": slot_id,
            "commentId": comment_id,
            "cycle": 1,
            "round": 1
        }
        self.clarifications.append(record)
        return record
```

### 10.4 Standalone Test Composition & Mock-Auth Attribute Compatibility
Router routes access caller identity via `current_user.user_id` (attribute access). The mock-auth override must return an object with attribute access, NOT a raw dictionary:
```python
from types import SimpleNamespace
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.routers import consensus
from backend.app.services.clerk_auth import get_current_user  # Current location
from backend.app.database import get_db                      # Current location

# Note: core/security.py and dependencies.py are PROPOSED future extractions.
# Tests override the exact callables consumed by routers.

test_app = FastAPI()
# Note: consensus.router already declares prefix="/api" (backend/app/routers/consensus.py:16).
# Mounting with prefix="/api" would erroneously create /api/api/votes.
test_app.include_router(consensus.router)

# Trusted mock user with attribute access
mock_user = SimpleNamespace(
    user_id="usr_test_panchami",
    clerk_user_id="user_clerk_panchami",
    email="panchami@example.com",
    display_name="Panchami",
    status="active"
)

# [TARGET ROUTER ARCHITECTURE PREREQUISITE]
# Note: backend/app/routers/consensus.py currently executes inline database queries and does
# not yet declare `get_consensus_service` in its Depends(...) signature. Refactoring the
# router to consume `get_consensus_service = Depends(get_consensus_service)` is an explicit
# target architecture prerequisite. Once refactored, the test overrides the service seam
# using a single stateful fake instance reused across requests within each test:
fake_consensus = FakeConsensusService()

test_app.dependency_overrides[get_current_user] = lambda: mock_user
test_app.dependency_overrides[get_db] = lambda: None  # No database connection
test_app.dependency_overrides[get_consensus_service] = lambda: fake_consensus

client = TestClient(test_app)

# Note: In test teardown, clean up overrides:
# test_app.dependency_overrides.clear()
```

### 10.5 Zero-Dependency Route Checks & Error Simulation Suite
Panchami verifies the complete transport contract with zero infrastructure running. (Note: Testing `GET /api/health` and `GET /api/trips` requires mounting their respective routers or using the full application with dependency overrides; the isolated consensus router suite mounts `consensus.router` to test consensus endpoints):
1. **`GET /api/health`**: Returns HTTP 200 with service health payload (when health router is mounted).
2. **`GET /api/trips` & `POST /api/trips`**: Deserializes JSON, validates Pydantic wire schema, delegates to `FakeTripService` (when trips router is mounted).
3. **`POST /api/votes`**: Active mounted vote endpoint (`consensus.py:274`). Verifies request body, maps domain response into HTTP 200. (`/api/proposals/{id}/vote` is a `[PROPOSED ALIAS]`).
4. **`POST /api/slots/{slot_id}/clarify`**: Validates 6-field wire envelope and slot ID route-body equality.
5. **Deterministic Fake Scenarios**:
   - **Success**: Returns 200/201 with canonical camelCase JSON.
   - **Validation Error**: Omitting required fields returns RFC 7807 `422 Unprocessable Entity`.
   - **Unauthorized / Non-Member**: Caller not in electorate returns `403 Forbidden` (`ERR_ELECTORATE_RESTRICTION`).
   - **Stale Version**: Passing stale `expectedVersion` returns `409 Conflict` (`ERR_STALE_VERSION`).
   - **Duplicate Identical Request**: Re-submitting same vote returns HTTP 200 with unchanged state.
   - **Conflicting Replay**: Changing vote after closure returns `409 Conflict`.
   - **In-Progress Processing**: Mode NA synthesis returns HTTP 202 `in_consensus`.
   - **Provider / Worker Failure**: DeepFace timeout returns `504 Gateway Timeout` with `processing_status = 'failed'`.
   - **Baseline Preservation**: Incompatible LLM synthesis leaves original proposal intact.

> [!IMPORTANT]
> **Teammate LLM Isolation Prerequisite**: Local consensus SLM/LLM installation (Ollama / Phi-4-mini) is **STRICTLY a Sharvani-internal prerequisite**. Teammates (Panchami, Nikitha) require **NO** local Ollama installation or SLM model weights.

### 10.6 The Four Verification Levels
- **Level 1 (Panchami Transport)**: Tests HTTP serialization, Pydantic validation, and error mapping using in-memory fake services with ZERO DB, ZERO LLM, and ZERO worker dependencies.
- **Level 2 (Panchami DeepFace)**: Tests face detection, ArcFace vector extraction, and candidate matching using isolated local reference images.
- **Level 3 (Sharvani Domain & Math)**: Tests deterministic scoring math (Jaccard, cosine), CAS concurrency, and rule-based validation independently.
- **Level 4 (Integrated Features)**: Connects real route → domain service → isolated Neon PostgreSQL database, feature by feature.

### 10.7 Authoritative Function Contracts (Production Implementation)
## 11. PYDANTIC WIRE MODELS (SCHEMAS)

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List
from decimal import Decimal

def to_camel(snake_str: str) -> str:
    parts = snake_str.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])

class ProposalCreate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    itm_id: str = Field(..., alias="itmId")
    title: str = Field(..., min_length=3, max_length=120)
    rationale: str = Field(..., min_length=10, max_length=500)
    entity_type: str = Field(..., alias="entityType")
    entity_id: Optional[str] = Field(None, alias="entityId")
    cost_delta: str = Field("0.00", alias="costDelta")
    currency: str = Field("USD", min_length=3, max_length=3)

    @field_validator("cost_delta")
    @classmethod
    def validate_decimal_string(cls, v: str) -> str:
        try:
            d = Decimal(v)
            if not d.is_finite():
                raise ValueError("Must be a finite decimal")
            return f"{d:.2f}"
        except Exception:
            raise ValueError("costDelta must be a valid formatted decimal string (e.g. '15.00')")

class VoteCreate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    prp_id: str = Field(..., alias="prpId")
    value: str = Field(..., pattern="^(yes|no)$")
    comment: Optional[str] = None

class VoteResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    vot_id: str = Field(..., alias="votId")
    prp_id: str = Field(..., alias="prpId")
    user_id: str = Field(..., alias="userId")
    value: str
    comment: Optional[str] = None
    cast_at: str = Field(..., alias="castAt")
```

---

## 12. RFC 7807 ERROR SPECIFICATION & MAPPING TABLE

### Problem Details Wire Format
All HTTP error responses adhere strictly to RFC 7807:
```json
{
  "type": "https://wandermatch.app/errors/val-empty-no-comment",
  "title": "Validation Error",
  "status": 400,
  "detail": "A non-empty comment explaining the objection is required when voting NO.",
  "instance": "/api/votes",
  "code": "VAL_EMPTY_NO_COMMENT",
  "invalidParams": [
    {
      "name": "comment",
      "reason": "Must contain at least 1 non-whitespace character"
    }
  ]
}
```

### Authoritative Error Code Mapping

| Rule Description | Trigger Endpoint | Condition & Violation | HTTP Status & Error Code | Expected System Action |
| :--- | :--- | :--- | :--- | :--- |
| **Binary Vote Invariant** | `POST /api/votes` | `value not in ['yes', 'no']` | `400 Bad Request` (`VAL_INVALID_VOTE_VALUE`) | Abort request immediately |
| **Typed NO Reason** | `POST /api/votes` | `value == 'no'` and comment empty/whitespace | `400 Bad Request` (`VAL_EMPTY_NO_COMMENT`) | Reject vote; do not start timer |
| **Single Active YES** | `POST /api/votes` | User casts YES on competing proposal in same slot | `200 OK` (`AC-VOT-02`) | Atomically retract prior YES in same transaction |
| **Slot Timer Start** | `POST /api/votes` | First NO vote in Mode NA | `200 OK` | Set `slot_consensus.closes_at = NOW() + 10m` |
| **Unanimous Chat Override**| `POST /api/chat/:msgId/propose` | 100% accepted members vote YES | `200 OK` (`CONFIRMED`) | Lock slot `CONFIRMED`; terminate AI loop |
| **Majority Chat Fallback** | `POST /api/chat/:msgId/propose` | Majority but not unanimous YES | `200 OK` (`QUEUED`) | Re-enters queue as standard proposal |
| **OCC Version Conflict** | Any itinerary update | Expected version != database version | `409 Conflict` (`CONFLICT_OCC_VERSION`) | Return reload schedule directive |
| **Legal Entity Type** | `POST /api/proposals` | `entity_type` not in `enums.json` | `400 Bad Request` (`VAL_INVALID_ENTITY_TYPE`) | Abort proposal submission |
| **Single Face Enrollment** | `POST /api/face/register` | Image contains 0 or $>1$ face | `400 Bad Request` (`FACE_INVALID_COUNT`) | Reject enrollment image |
| **Worker Failure State** | `POST /api/photos` | DeepFace worker times out or returns 5xx | `200 OK` (degraded) | Set photo `processing_status = 'failed'` |

---


<a id="member-phase-3"></a>
## Phase 3 — Wire application transport, identity and WebSockets

Read the retained sections below together for this phase:

- 6. FASTAPI APPLICATION SETUP & ROUTER REGISTRATION
- 7. WEBSOCKET CONNECTION LIFECYCLE (`websocket_manager.py`)
- 8. CLERK AUTHENTICATION & WEBHOOK HANDOFF

## 6. FASTAPI APPLICATION SETUP & ROUTER REGISTRATION

> **Ownership Note**: Sharvani owns `backend/app/main.py`. Panchami exposes clean APIRouter objects that Sharvani mounts in `main.py`.

```python
# Mounting pattern in backend/app/main.py (Owner: Sharvani)
from .routers import auth, trips, matching, face, photos, consensus

app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(trips.router, prefix="", tags=["trips"])
app.include_router(matching.router, prefix="", tags=["matching"])
app.include_router(face.router, prefix="", tags=["face"])
app.include_router(photos.router, prefix="", tags=["photos"])
app.include_router(consensus.router, prefix="", tags=["consensus"])
```

---

## 7. WEBSOCKET CONNECTION LIFECYCLE (`websocket_manager.py`)

Panchami enforces strict authentication and delivery of `resyncSnapshot`:

```python
async def authenticate_and_connect(
    self, websocket: WebSocket, trip_id: str, path_user_id: Optional[str], token: Optional[str], db: Session
) -> Optional[str]:
    # 1. Verify token
    auth_user_id = self.verify_token(token)
    if not auth_user_id:
        await websocket.close(code=4401, reason="Unauthorized: Invalid or missing authentication token")
        return None

    # 2. Forged identity attempt
    if path_user_id and path_user_id != auth_user_id:
        await websocket.close(code=4403, reason="Forbidden: Authenticated identity does not match URL identity")
        return None

    # 3. Check membership in Neon DB via Sharvani's service
    if not sharvani_trip_service.is_user_authorized_member(db, trip_id, auth_user_id):
        await websocket.close(code=4403, reason="Forbidden: Not an authorized member of this trip")
        return None

    # 4. Accept socket and register in active room
    await websocket.accept()
    if trip_id not in self.active_rooms:
        self.active_rooms[trip_id] = {}
    self.active_rooms[trip_id][auth_user_id] = websocket

    # 5. Deliver authoritative state snapshot resync
    snapshot = sharvani_trip_service.get_trip_snapshot(db, trip_id)
    await websocket.send_json({
        "type": "resyncSnapshot",
        "tripId": trip_id,
        "userId": auth_user_id,
        "snapshot": snapshot
    })
    return auth_user_id
```

---

## 8. CLERK AUTHENTICATION & WEBHOOK HANDOFF

### 8.1 JWT Protection
- Protected routes extract bearer token from `Authorization: Bearer <token>`.
- Panchami injects Sharvani's `current_user: User = Depends(get_current_user)` auth dependency.

### 8.2 Webhook Endpoint (`POST /api/auth/webhook`)
- **Route**: `POST /api/auth/webhook` (`routers/auth.py:L88`).
- **Panchami's Transport Role**: Reads raw request body bytes, extracts headers (`svix-id`, `svix-timestamp`, `svix-signature`).
- **In-Process Service Handoff**:
  ```python
  # In-process call to Sharvani's security service
  verified = sharvani_security.verify_svix_signature(body_bytes, headers)
  if not verified:
      raise HTTPException(status_code=400, detail="Invalid webhook signature")
  sharvani_security.sync_clerk_user_to_db(db, payload)
  return {"received": True}
  ```
- **Error Codes**: `400 Bad Request` if signature is invalid; `200 OK` on successful idempotent sync.

---


<a id="member-phase-4"></a>
## Phase 4 — Implement feature endpoints and the DeepFace integration

Read the retained sections below together for this phase:

- 0.2 DEEPFACE RECOGNITION PROTOCOL, SEMANTICS & TEST SAFETY
- 9. ALL API ENDPOINTS — COMPLETE TRANSPORT SPECIFICATION

## 0.2 DEEPFACE RECOGNITION PROTOCOL, SEMANTICS & TEST SAFETY

### Real Image-Transfer Mechanism
- **Prohibition on Relative URLs**: Panchami must **never** send a relative path (e.g. `/static/uploads/pho_xxx.jpg`) to the DeepFace worker. The worker runs as an independent microservice on port 8001 and cannot resolve relative paths from port 8000.
- **Multipart Stream Forwarding with Candidate Embeddings**:
  - The DeepFace worker (`ai/DeepFace/backend/main.py`) runs with local SQLite (`wandermatch.db`) and does not connect to Neon PostgreSQL.
  - Sending `candidate_user_ids` alone fails because the worker cannot load member embeddings from Neon.
  - Panchami's router handler calls Sharvani's in-process `photo_service.get_candidate_member_embeddings(db, trip_id)` to retrieve candidate user IDs paired with their 512-d ArcFace vectors.
  - Panchami streams the image binary bytes alongside the candidate vectors JSON as multipart form-data to the worker:
    ```python
    async with httpx.AsyncClient(timeout=10.0) as client:
        files = {"file": (filename, image_bytes, content_type)}
        data = {
            "trip_id": trip_id,
            "candidate_embeddings": json.dumps(candidate_embeddings_payload)
        }
        resp = await client.post(f"{DEEPFACE_SERVICE_URL}/api/face/match-photo", files=files, data=data)
    ```

### Face-Instance Identifiers & Completeness Semantics
1. **Face Instances**: Each detected face in an image is assigned a unique face instance identifier (`face_index: int`, bounding box `{"x": int, "y": int, "w": int, "h": int}`). Distinct traveler IDs (`usr_...`) are matched against detected face instances. Distinct people must never be confused with face instances.
2. **Recognition Completeness (Instance Counting)**:
   - `detected_faces_count == 0`: **Scenery Candidate**. Categorized as `folder:Scenery`.
   - `detected_faces_count > 0 and matched_count == 0`: **Unknown Faces**. Group photo containing human faces with no enrolled matches. **Must NEVER be categorized as Scenery**. Categorized under `folder:GroupPhotos` with `unidentified_faces: true`.
   - `0 < matched_count < detected_faces_count`: **Partial Match**. Some faces recognized; others unidentified.
   - `matched_count == detected_faces_count`: **Complete Match**. All detected faces recognized.
   - **Worker Failure State**: If the DeepFace worker times out, crashes, or returns 5xx: photo status is set to `processing_status = 'failed'` (or `'degraded'`). **A worker network failure or timeout must NEVER be recorded as successful completed recognition.**

### Privacy & Vector Protection
- Enrolled 512-d ArcFace floating-point vectors are strictly server-internal biometric signatures.
- Vectors must **never** be output to application logs, debug messages, or browser-facing JSON responses.

### Enrollment Rules (Decision #18)
- Requires exactly 3 valid single-face enrollment images (Straight, Left, Right).
- Quality check: exactly 1 face per image. If any sample has 0 faces or >1 face, the entire enrollment fails atomically. No partial enrollment is persisted.

### Matching Metric & Distance Calibration
- **Model & Dimensionality**: DeepFace uses the `ArcFace` model producing 512-dimensional float embeddings.
- **Three Distinct Quantities (Do Not Interchange)**:
  1. **Raw Cosine Similarity**: $S_{\text{cos}} = \frac{u \cdot v}{\|u\| \|v\|} \in [-1, 1]$.
  2. **Cosine Distance**: $D_{\text{cos}} = 1 - S_{\text{cos}}$. DeepFace's default reference distance threshold for ArcFace is $0.68$ ($D_{\text{cos}} \le 0.68$), which corresponds to raw similarity $S_{\text{cos}} \ge 0.32$.
  3. **Prototype Transformed Heuristic Score**: In `ai/DeepFace/backend/services/face/matching.py:L71–78`, the worker maps raw similarity $\ge 0.45$ into a heuristic score:
     $$\text{calibrated\_conf} = \text{round}\left(0.90 + 0.10 \times \frac{\min(1.0, S_{\text{cos}}) - 0.45}{0.55}, 3\right)$$
     and compares that score against `CONFIDENCE_THRESHOLD = 0.90`.
- **Evidentiary Honesty**:
  - Raw similarity $S_{\text{cos}} \ge 0.45$ corresponds to cosine distance $D_{\text{cos}} \le 0.55$.
  - Raw similarity $\ge 0.45$ is **NOT** the same as raw similarity $\ge 0.90$ (which would be an extremely strict distance $D_{\text{cos}} \le 0.10$).
  - This transformed heuristic score is **NOT a mathematical probability** and does NOT guarantee zero false merges. Target calibration policies remain **PROPOSED** pending empirical validation on the reference dataset.

### Microservice Isolation & Test Safety
- **Legitimate Integration Testing**: Controlled integration tests may import the application (`backend.app.main:app`) after safe environment isolation (setting `DATABASE_URL` to an isolated test database and configuring test doubles for external provider APIs). We do not impose an absolute prohibition that prevents legitimate integration testing.
- **Real Image Verification**: Dummy float vectors alone do **NOT** prove correct face recognition. The test suite in `ai/DeepFace/tests/` must verify detection and ArcFace matching using real reference images at known angles (straight, left, right) and known scenery images.

### Exact Three-Person Face Regression Acceptance Scenario (Transport & DeepFace)
This concrete regression acceptance case translates the original reported face grouping regression (where photos of distinct members were collapsed into a single identity or mis-tagged) into an automated, verifiable test suite:
1. **Reference Test Image Corpus**:
   - **Enrolled Individuals (3 Distinct Members)**:
     * Person A (Nikitha), Person B (Panchami), Person C (Sharvani).
     * Each member provides 3 enrollment reference images (Straight, Left Tilt, Right Tilt) producing 512-d ArcFace profile vectors via `POST /api/face/register`.
   - **Individual Photos**: 3 test images containing exactly one of Person A, Person B, or Person C in natural lighting.
   - **Group Photos**: Multi-person photos containing combinations (Person A + Person B, Person B + Person C, Person A + Person B + Person C).
   - **Unknown / Un-Enrolled Person**: 1 test photo containing Person D (who has no registered enrollment vector).
   - **Scenery / Zero Face**: 1 test photo containing a mountain/lake landscape with zero human faces.
2. **Acceptance Verification Gates**:
   - **Recognition Metric Verification on Reference Corpus**:
     * Processing Person A's individual photo returns `detected_faces_count == 1`, `matched_count == 1`, with raw similarity $S_{\text{cos}} \ge 0.45$ (prototype transformed score $\ge 0.90$), mapping exclusively to Person A's `user_id`.
     * Returns zero tags for Person B or Person C within the fixed reference corpus.
   - **Schema Reality (`photo_person` vs Proposed `photo_face_tags`)**:
     * Current table in `backend/app/models/additive.py` is `photo_person` (`photo_id`, `user_id`, `confidence`). It lacks `face_index`, `bounding_box`, and un-enrolled face records (`user_id = NULL`).
     * `photo_face_tags` is an explicit **proposed logical target representation** and pending schema migration owned by Sharvani. Panchami's router returns the unified JSON response, decoupling transport testing from physical table migration.
   - **Multi-Face Instance Separation in Group Photos**:
     * A photo containing Person A and Person B produces `detected_faces_count == 2`.
     * Each bounding box receives a distinct `face_index` (`face_index=0`, `face_index=1`).
     * `matched_count == 2`, returning tags for both `usr_a` and `usr_b`. Distinct identities are preserved; repeated face instances never collapse distinct people into one.
   - **Zero False Cross-Person Tags**: Person A is never tagged as Person B or Person C, even under varying lighting or angles.
   - **Unenrolled Person Handling**:
     * Processing Person D's photo produces `detected_faces_count == 1`, `matched_count == 0`, `unidentified_faces == True`.
     * Person D is NEVER misattributed to Person A, B, or C.
   - **Scenery Photo Isolation**:
     * Processing the scenery image returns `detected_faces_count == 0`, `matched_count == 0`, `folder == "Scenery"`. Zero face bounding boxes or tags are generated.
   - **Honest Evidentiary Reporting**: If any face produces distance $D_{\text{cos}} > 0.68$ (or similarity $< 0.90$), Panchami's transport reports `usr_id = None` (`unidentified`), rather than forcing a low-confidence false match.

---

## 9. ALL API ENDPOINTS — COMPLETE TRANSPORT SPECIFICATION

For every interface, this section distinguishes:
- `[CURRENT IMPLEMENTATION]` — What exists in code today.
- `[REQUIRED BEHAVIOR]` — Canonical behavior per PRD/TRD/AI.
- `[PROPOSED ENDPOINT/SCHEMA]` — Target contract design.
- `[MISSING IMPLEMENTATION]` — Any gap requiring implementation.

---

### 9.1 Health Check

- **Endpoint**: `GET /api/health`
- **Current Implementation**: Implemented in `backend/app/main.py:L32`. Returns `{"status": "ok"}`.
- **Required Behavior**: Returns `200 OK` with status and version. Unauthenticated.
- **Request Example**: `GET /api/health`
- **Response Example**:
  ```json
  { "status": "ok", "version": "1.0.0" }
  ```
- **Service Handoff**: None (direct return).
- **Errors**: None.
- **Acceptance Check**: `curl http://localhost:8000/api/health` returns HTTP 200.

---

### 9.2 Trips, Drafts, Publishing, Discovery & Membership

#### A. List User Trips (`GET /api/trips`)
- **Endpoint**: `GET /api/trips` (`routers/trips.py:L197`)
- **Current Implementation**: Queries trips where current user is owner or accepted member.
- **Required Behavior**: Returns list of trips for authenticated user with camelCase fields.
- **Trusted Identity**: Injected via `current_user: User = Depends(get_current_user)`.
- **In-Process Service Handoff**:
  ```python
  trips = sharvani_trip_service.list_user_trips(db, user_id=current_user.user_id)
  ```
- **Response Example**:
  ```json
  [
    {
      "trpId": "trp_a91f3c2b",
      "title": "Kyoto Autumn Explorer",
      "destinationCityId": "cty_kyoto",
      "startDate": "2026-11-01",
      "endDate": "2026-11-07",
      "partySize": 4,
      "mode": "Mode NA",
      "status": "planning",
      "role": "owner"
    }
  ]
  ```
- **Errors**: `401 Unauthorized` if token missing.

#### B. Discover Public Trips (`GET /api/trips/discover`)
- **Endpoint**: `GET /api/trips/discover` (`routers/trips.py:L228`)
- **Current Implementation**: Queries published trips (`visibility = 'public'`).
- **Required Behavior**: Returns list of joinable public trips with open capacity.
- **In-Process Service Handoff**:
  ```python
  trips = sharvani_trip_service.discover_public_trips(db)
  ```

#### C. Get Trip Details (`GET /api/trips/{trp_id}`)
- **Endpoint**: `GET /api/trips/{trp_id}` (`routers/trips.py:L258`)
- **Current Implementation**: Retrieves trip, members, and active itinerary.
- **Required Behavior**: Returns full trip object with members, active itinerary items, current proposal, votes, and branch summaries.
- **In-Process Service Handoff**:
  ```python
  trip_detail = sharvani_trip_service.get_trip_detail(db, trip_id=trp_id, user_id=current_user.user_id)
  ```
- **Errors**: `403 Forbidden` if user not member; `404 Not Found` if trip does not exist.

#### D. Create Trip (`POST /api/trips`)
- **Endpoint**: `POST /api/trips` (`routers/trips.py:L16`)
- **Current Implementation**: Creates trip, itinerary v1, and owner member in single transaction.
- **Required Behavior**: Creates trip with authenticated user as owner (`current_user.user_id`), initializes itinerary version 1.
- **Request Example**:
  ```json
  {
    "title": "Kyoto Culture & Culinary",
    "destinationCityId": "cty_kyoto",
    "startDate": "2026-11-01",
    "endDate": "2026-11-07",
    "partySize": 4,
    "mode": "Mode NA"
  }
  ```
- **In-Process Service Handoff**:
  ```python
  trip = sharvani_trip_service.create_trip(db, creator_user_id=current_user.user_id, data=payload.model_dump())
  ```
- **Errors**: `400 Bad Request` if `endDate < startDate` or `partySize < 2`.

#### E. Publish Trip (`PATCH /api/trips/{trp_id}/publish`)
- **Endpoint**: `PATCH /api/trips/{trp_id}/publish` (`routers/trips.py:L359`)
- **Current Implementation**: Sets `visibility = 'public'`.
- **Required Behavior**: Transitions trip from draft to published; requires owner permission.
- **In-Process Service Handoff**:
  ```python
  sharvani_trip_service.publish_trip(db, trip_id=trp_id, user_id=current_user.user_id)
  ```

#### F. Add Itinerary Item (`POST /api/trips/{trp_id}/itinerary`)
- **Endpoint**: `POST /api/trips/{trp_id}/itinerary` (`routers/trips.py:L113`)
- **Current Implementation**: Adds new item to active itinerary.
- **Required Behavior**: Appends item, increments itinerary version, enforces OCC.
- **In-Process Service Handoff**:
  ```python
  item = sharvani_trip_service.add_itinerary_item(db, trip_id=trp_id, user_id=current_user.user_id, data=payload.model_dump())
  ```

#### G. Join Request & Approval Workflow
- **Create Join Request**: `POST /api/trips/{trp_id}/join-request` (`routers/trips.py:L376`)
- **List Join Requests**: `GET /api/trips/{trp_id}/join-requests` (`routers/trips.py:L460`)
- **Approve Join Request**: `POST /api/trips/{trp_id}/join-requests/{request_id}/approve` (`routers/trips.py:L498`)
- **Reject Join Request**: `POST /api/trips/{trp_id}/join-requests/{request_id}/reject` (`routers/trips.py:L543`)
- **My Join Status**: `GET /api/trips/{trp_id}/my-join-status` (`routers/trips.py:L576`)
- **Current Implementation**: Fully implemented in `trips.py`. Mode A queues request for owner approval; Mode NA auto-approves if capacity allows.

#### H. Invite Code Workflow
- **Get Invite Code**: `GET /api/trips/{trp_id}/invite-code` (`routers/trips.py:L741`)
- **Revoke Invite Code**: `POST /api/trips/{trp_id}/invite-code/revoke` (`routers/trips.py:L783`)
- **Join by Code**: `POST /api/trips/join-by-code` (`routers/trips.py:L829`)
- **Current Implementation**: Implemented in `trips.py`. Validates active code and adds member.

#### I. Direct Add Member (`POST /api/trips/{trp_id}/members`)
- **Endpoint**: `POST /api/trips/{trp_id}/members` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
- **Required Behavior**: Allows trip owner/admin to add an accepted user directly without invite code.
- **Service Handoff**:
  ```python
  member = sharvani_trip_service.add_trip_member(db, trip_id=trp_id, inviter_id=current_user.user_id, target_user_id=payload.targetUserId)
  ```

---

### 9.3 Proposals, History & Timer Check

#### A. Submit Proposal (`POST /api/proposals`)
- **Endpoint**: `POST /api/proposals` (`routers/consensus.py:L129`)
- **Current Implementation**: Inserts proposal with `closes_at = NULL`. Sets slot status to `in_consensus`.
- **Required Behavior**:
  - Validates `entity_type` against `docs/data/enums.json`.
  - Enforces `rationale` (NOT description) and `cost_delta` (NOT estimatedCost, serialized as string).
  - Derived trusted identity: `proposed_by_user_id = current_user.user_id`. (Request body does NOT contain caller ID).
  - Checks if voting window is open for the slot: if `slot_consensus.closes_at` is active, queues proposal for next round (`status: 'QUEUED'`).
  - Broadcasts `proposalCreated` via WebSocket after transaction commit.
- **Request Example**:
  ```json
  {
    "itmId": "itm_7a2b9c",
    "title": "Fushimi Inari Early Morning Hike",
    "rationale": "Avoid crowds and catch sunrise over torii gates",
    "entityType": "poi",
    "entityId": "poi_fushimi_01",
    "costDelta": "0.00",
    "currency": "USD"
  }
  ```
- **In-Process Service Handoff**:
  ```python
  proposal, is_queued = sharvani_trip_service.submit_proposal(
      db, slot_id=payload.itmId, user_id=current_user.user_id, data=payload.model_dump()
  )
  ```
- **Response Example**:
  ```json
  {
    "prpId": "prp_7d3e9f1a",
    "itmId": "itm_7a2b9c",
    "title": "Fushimi Inari Early Morning Hike",
    "rationale": "Avoid crowds and catch sunrise over torii gates",
    "costDelta": "0.00",
    "currency": "USD",
    "closesAt": null,
    "status": "open",
    "currentRound": 1
  }
  ```
- **Errors**: `400 Bad Request` if invalid `entityType`; `404 Not Found` if slot not found.

#### B. Active Proposal & Slot History
- **Get Active Proposal**: `GET /api/slots/{itm_id}/active-proposal` (`routers/consensus.py:L204`)
- **Get Slot History**: `GET /api/slots/{itm_id}/history` (`routers/consensus.py:L239`)
- **Current Implementation**: Returns current open proposal or past round proposals for the slot.

#### C. Timer Check (`POST /api/proposals/check-timer`)
- **Endpoint**: `POST /api/proposals/check-timer` (`routers/consensus.py:L693`)
- **Current Prototype vs Production Contract**:
  - *Current Prototype*: Receives `CheckTimerRequest(prp_id, advance_minutes)`. If window expired with 0 NO votes, auto-confirms slot and broadcasts `slotStatusChanged`.
  - *Production Contract*: Evaluates authoritative current time against `slot_consensus.closes_at`. Authoritative time cannot be advanced via normal HTTP requests. `advance_minutes` is strictly a non-production test parameter and must NOT be accepted in production request bodies or passed to production domain services.
- **In-Process Service Handoff**:
  ```python
  # Production Contract: evaluates authoritative current time against slot_consensus.closes_at
  result = sharvani_consensus_service.check_and_expire_timer(db, proposal_id=payload.prpId)

  # Non-production test harness ONLY:
  # test_result = test_consensus_service.check_and_expire_timer(db, proposal_id=payload.prpId, advance_minutes=test_fixture_offset)
  ```
- **Response Example**:
  ```json
  {
    "prpId": "prp_7d3e9f1a",
    "expired": true,
    "autoConfirmed": true,
    "slotStatus": "CONFIRMED"
  }
  ```
- **Errors**: `404 Not Found` if proposal not found.

---

### 9.4 Votes & Invariants

#### A. Cast Vote (`POST /api/votes`)
- **Endpoint**: `POST /api/votes` (`routers/consensus.py:L274`)
- **Current Implementation**: Accepts single or list of votes. Retracts prior vote on same proposal. Starts 10-minute timer on first NO in Mode NA.
- **Required Behavior**:
  - **Trusted Identity**: Caller identity comes strictly from `current_user.user_id`. Request body does NOT specify caller ID.
  - **Rule 1 (Binary Only)**: `value` must be `'yes'` or `'no'`. Never `'abstain'`.
  - **Rule 2 (Reason Required)**: `value === 'no'` REQUIRES non-empty trimmed `comment`.
  - **Rule 3 (Single Active YES — `AC-VOT-02`)**: Yes on Proposal B automatically retracts prior Yes on Proposal A in the same slot within the same atomic transaction. Retraction does NOT synthesize a NO.
  - **Rule 4 (Authoritative Slot Timer)**: First NO vote in Mode NA sets `slot_consensus.closes_at = NOW() + 10m` (Decision #31 pending duration sign-off). Mirrored read-only to `proposals.closes_at`.
  - **Rule 5 (Non-Voters Unblocked)**: Uses upsert; silent members never block progress.
  - Broadcasts `voteCast` via WebSocket after transaction commit.
- **Request Example**:
  ```json
  {
    "prpId": "prp_7d3e9f1a",
    "value": "no",
    "comment": "Too early in the morning; prefer afternoon hike"
  }
  ```
- **In-Process Service Handoff**:
  ```python
  vote_record = sharvani_voting_service.cast_vote(
      db, proposal_id=payload.prpId, user_id=current_user.user_id, value=payload.value, comment=payload.comment
  )
  ```
- **Errors**:
  - `400 Bad Request` (`VAL_EMPTY_NO_COMMENT`): If `value == 'no'` and comment is null or whitespace.
  - `400 Bad Request`: If value is not `'yes'` or `'no'`.
  - `403 Forbidden`: If caller is not an accepted trip member.

#### B. Batch Votes (`POST /api/votes/batch`)
- **Endpoint**: `POST /api/votes/batch` (`routers/consensus.py:L405`)
- **Current Implementation**: Accepts array of votes and processes each within a single transaction.

---

### 9.5 Consensus Reconcile & Mode A Controls

#### A. Trigger Reconcile (`POST /api/consensus/reconcile`)
- **Endpoint**: `POST /api/consensus/reconcile` (`routers/consensus.py:L652`)
- **Current Implementation**: Loads NO comments, calls AI compromise generator, returns BLENDED or BRANCHED.
- **Required Behavior**: Validates slot is `IN_CONSENSUS`. Invokes Sharvani's AI consensus engine in-process. Broadcasts `aiRecommendationReady` & `aiPlanGenerated` or `slotStatusChanged`.
- **Request Example**:
  ```json
  { "prpId": "prp_7d3e9f1a" }
  ```
- **In-Process Service Handoff**:
  ```python
  result = sharvani_consensus_service.reconcile_slot(db, proposal_id=payload.prpId)
  ```
- **Response Example (BLENDED)**:
  ```json
  {
    "action": "BLENDED",
    "currentRound": 1,
    "blendedPlan": {
      "title": "Fushimi Inari Mid-Morning Walk & Tea",
      "rationale": "Compromise start at 09:30 accommodating rest preferences while avoiding peak tour buses",
      "costDelta": "0.00",
      "currency": "USD"
    }
  }
  ```

#### B. Mode A Admin Controls (`POST /api/consensus/mode-a/*`)
- `POST /api/consensus/mode-a/invoke` (`consensus.py:L414`): Admin requests AI advisory compromise.
- `POST /api/consensus/mode-a/accept` (`consensus.py:L465`): Admin accepts proposal/compromise directly. Confirms slot.
- `POST /api/consensus/mode-a/force-branch` (`consensus.py:L508`): Admin splits slot into parallel tracks immediately.
- `POST /api/consensus/mode-a/extend` (`consensus.py:L572`): Admin extends round timer by $N$ minutes.
- `POST /api/consensus/mode-a/direct-confirm` (`consensus.py:L607`): Admin directly confirms slot without voting.
- **Permissions**: Enforces `current_user.user_id == trip.owner_user_id`. Returns `403 Forbidden` if caller is not trip owner.

---

### 9.6 Negotiation Selection & Revision Restoration

#### A. Submit Negotiation Option Selection (`POST /api/negotiation/select-option`)
- **Endpoint**: `POST /api/negotiation/select-option` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
- **Required Behavior**:
  - Submits chosen alternative from evidence-grounded negotiation card (`KEEP_ORIGINAL`, `CLOSER_ALTERNATIVE`, `RESCHEDULE_WINDOW`).
  - **Option Semantics**:
    - `KEEP_ORIGINAL`: Caller confirms preference for baseline despite infeasibility warning. Dismisses card locally for caller; does **NOT** mutate slot, force group decision, or override consensus.
    - `CLOSER_ALTERNATIVE`: Submits closer POI alternative (`selectedOptionId`) as a new proposal. Does **NOT** directly mutate accepted itinerary; in Mode A routes to admin for review, in Mode NA opens proposal in slot for group voting.
    - `RESCHEDULE_WINDOW`: Proposes shifting slot timing. In Mode A, trip owner can approve immediately (updating slot timestamps and bumping version); in Mode NA, opens schedule-modification proposal / voting round (unanimous chat override is a separate chat-based mechanism; non-admin instant reschedule in Mode NA is pending policy `[MODE_NA_RESCHEDULE_APPROVAL_POLICY_PENDING]`).
  - **Validation & Guards**:
    - `expectedVersion`: Strict OCC guard against `itineraries.version`. Returns `409 Conflict` (`ERR_STALE_VERSION`) on mismatch.
    - `evidenceToken`: Opaque server token binding trip, slot, consensus cycle, itinerary version, candidate, and evidence hash with 1-hour TTL (`[PROPOSED_CONFIGURATION_TTL]` subject to Decision #12; cryptographic signature validity does not prove fresh route or venue opening-hour facts). Rejects expired/tampered tokens with `400 Bad Request` (`ERR_INVALID_EVIDENCE_TOKEN`).
    - Caller verified in `trip_members` (`403 Forbidden` / `ERR_NOT_TRIP_MEMBER`).
    - Duplicate submission check: identical idempotent retry (same caller, same slot, same optionId, same version/token) returns cached prior result with `200 OK`; conflicting replay (competing optionId or competing caller for same slot/cycle) is rejected with `409 Conflict` (`ERR_DUPLICATE_SELECTION` or `ERR_STALE_VERSION`).
- **Request Example**:
  ```json
  {
    "tripId": "trp_a91f3c2b",
    "slotId": "itm_7a2b9c",
    "selectedOptionId": "opt_closer_02",
    "optionType": "CLOSER_ALTERNATIVE",
    "expectedVersion": 4,
    "evidenceToken": "ev_tok_8f9a2b"
  }
  ```
- **In-Process Service Handoff**:
  ```python
  result = sharvani_consensus_service.apply_negotiation_selection(
      db, user_id=current_user.user_id, selection=payload.model_dump()
  )
  ```
- **Response Examples**:
  - *KEEP_ORIGINAL*: `{"status": "DISMISSED", "tripId": "trp_a91f3c2b", "slotId": "itm_7a2b9c", "optionType": "KEEP_ORIGINAL"}`
  - *CLOSER_ALTERNATIVE*: `{"status": "PROPOSAL_CREATED", "proposalId": "prp_c1a8e2", "slotId": "itm_7a2b9c", "optionType": "CLOSER_ALTERNATIVE"}`
  - *RESCHEDULE_WINDOW (Mode A approved)*: `{"status": "SLOT_RESCHEDULED", "slotId": "itm_7a2b9c", "newStartsAt": "09:00", "newEndsAt": "12:00", "version": 5}`
- **Errors**:
  - `400 Bad Request`: `ERR_INVALID_EVIDENCE_TOKEN` (token expired, tampered, or mismatched slot/trip).
  - `403 Forbidden`: `ERR_NOT_TRIP_MEMBER` (caller not a member of trip).
  - `404 Not Found`: `ERR_SLOT_NOT_FOUND` (slot or trip does not exist).
  - `409 Conflict`: `ERR_STALE_VERSION` (`expectedVersion` != current itinerary version), `ERR_DUPLICATE_SELECTION`.

#### B. Submit Dissent Clarification (`POST /api/slots/{slot_id}/clarify`)
- **Endpoint**: `POST /api/slots/{slot_id}/clarify` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
- **Required Behavior**:
  - Handles traveler clarification submission when `NEEDS_CLARIFICATION` was emitted.
  - Validates path parameter matches body: `payload.slotId == slot_id` (`400 Bad Request` with `ERR_SLOT_ID_MISMATCH` if mismatched).
  - English-Only Scope: `clarificationText` must be provided in English.
  - Verifies caller is authenticated and matches the original author of the dissenting comment (`403 Forbidden` if caller != author).
  - Validates `expectedVersion` against `itineraries.version` (OCC guard; `409 Conflict` on mismatch).
  - Validates `evidenceToken` (1h TTL `[PROPOSED_CONFIGURATION_TTL]`, Decision #12).
  - Hands off in-process to `sharvani_consensus_service.submit_clarification`.
  - Invariants: Clarification preserves objection constraint set, does NOT increment round number, does NOT count as a vote, does NOT reset voting deadline.
  - Broadcasts `clarificationSubmitted` event over WebSocket to all trip members.
- **Request Example**:
  ```json
  {
    "tripId": "trp_a91f3c2b",
    "slotId": "itm_7a2b9c",
    "commentId": "com_12345",
    "clarificationText": "Prefer museum with wheelchair access and budget under $30",
    "expectedVersion": 4,
    "evidenceToken": "ev_tok_8f9a2b"
  }
  ```
- **In-Process Service Handoff**:
  ```python
  result = sharvani_consensus_service.submit_clarification(
      db=db,
      slot_id=slot_id,
      comment_id=payload.commentId,
      user_id=current_user.user_id,
      text=payload.clarificationText,
      version=payload.expectedVersion,
      token=payload.evidenceToken
  )
  ```
- **Response**: `{"status": "CLARIFICATION_ACCEPTED", "slotId": "itm_7a2b9c", "commentId": "com_12345", "cycle": 1, "round": 1}`
  *(Note: Clarification is a discussion input; it records the objection clarification into the slot constraint set but does NOT bump `itineraries.version`. In WanderMatch, `itineraries.version` tracks authoritative itinerary item modifications (such as proposal confirmations, schedule changes, branch partition confirmations, and revision restores; see Section 2.6 of INTEGRATION_CONTRACT.md). Submitting a clarification updates the deterministic clarification state captured in both snapshot creation and commit-time revalidation, causing in-flight AI synthesis leases to be rejected as stale (`DISCARDED_STALE`) without fabricating an itinerary version bump or mutating traveler votes. Thus `version` is omitted from the response).*
- **WebSocket Broadcast**: Emits `clarificationSubmitted` with envelope `{"type": "clarificationSubmitted", "trpId": trp_id, "itmId": slot_id, "slotId": slot_id, "usrId": current_user.user_id, "commentId": payload.commentId, "cycle": 1, "round": 1}`.
- **Authoritative Unified Error Mapping**:
  - `400 Bad Request`: `ERR_SLOT_ID_MISMATCH` (path `slot_id` != body `slotId`) or `ERR_MALFORMED_REQUEST` (invalid JSON syntax)
  - `401 Unauthorized`: `ERR_UNAUTHORIZED` (missing or invalid bearer token)
  - `403 Forbidden`: `ERR_NOT_COMMENT_AUTHOR` (caller `current_user.user_id` does not own objection comment) or `ERR_NOT_TRIP_MEMBER`
  - `404 Not Found`: `ERR_NOT_FOUND` (slot or objection comment not found)
  - `409 Conflict`: `ERR_STALE_VERSION` (OCC guard: `expectedVersion` does not match `itineraries.version`) or `ERR_CONFLICTING_REPLAY`
  - `422 Unprocessable Entity`: `ERR_TOKEN_EXPIRED` (token timestamp > 1h TTL, Decision #12), `ERR_EVIDENCE_INVALID` (HMAC cryptographic verification failed or mismatched slot/version), or `ERR_MISSING_FIELD` (Pydantic validation failure)
  - `503 Service Unavailable`: `ERR_SERVICE_UNAVAILABLE` (database or consensus engine unreachable)

#### C. Restore Itinerary Revision (`POST /api/trips/{trp_id}/revisions/{rev_id}/restore`)
- **Endpoint**: `POST /api/trips/{trp_id}/revisions/{rev_id}/restore` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
- **Required Behavior**: Restores past snapshot from `revision_history`; bumps version monotonically; records audit log.

---

### 9.7 Branches (`/api/branches/*`)

- **Endpoints**:
  - `GET /api/branches/{itm_id}` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
  - `POST /api/branches/{brc_id}/confirm` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
  - `POST /api/branches/{brc_id}/modify` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
- **Required Behavior**:
  - `GET /api/branches/{itm_id}`: Returns all branches for a slot, member lists, and finalized status.
  - `POST /api/branches/{brc_id}/confirm`: Member confirms branch choice (`current_user.user_id`). If all members confirmed, marks branch `FINALIZED`. If all top-level branches finalized, sets slot status to `CONFIRMED` and broadcasts `slotStatusChanged`.
  - `POST /api/branches/{brc_id}/modify`: Stores modification note and triggers sub-group AI revision cycle.
- **In-Process Service Handoff**:
  ```python
  sharvani_consensus_service.confirm_branch_member(db, branch_id=brc_id, user_id=current_user.user_id)
  ```

---

### 9.8 Trip Chat Endpoints

#### A. Get Chat History (`GET /api/trips/{trip_id}/chat`)
- **Endpoint**: `GET /api/trips/{trip_id}/chat` (`routers/trips.py:L960`)
- **Current Implementation**: Retrieves messages ordered by `created_at ASC` with sender details.
- **Required Behavior**: Returns message list for authorized trip members.
- **Response Example**:
  ```json
  [
    {
      "messageId": "msg_01",
      "tripId": "trp_a91f3c2b",
      "userId": "usr_alice",
      "senderName": "Alice Walker",
      "avatarUrl": "https://img.clerk.com/alice.png",
      "content": "What if we do Gion evening walking tour instead?",
      "isProposal": false,
      "proposalRefId": null,
      "createdAt": "2026-10-29T10:00:00Z"
    }
  ]
  ```

#### B. Send Chat Message (`POST /api/trips/{trip_id}/chat`)
- **Endpoint**: `POST /api/trips/{trip_id}/chat` (`routers/trips.py:L991`)
- **Current Implementation**: Inserts message in `trip_chat_messages` table.
- **Required Behavior**: Inserts message (`sender_user_id = current_user.user_id`), broadcasts to trip room via WebSocket `newChatMessage`.
- **Request Example**:
  ```json
  {
    "content": "Let's definitely book the tea ceremony!",
    "isProposal": false
  }
  ```

#### C. Propose from Chat (`POST /api/chat/{msg_id}/propose`)
- **Endpoint**: `POST /api/chat/{msg_id}/propose` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`
- **Required Behavior**:
  - Loads message content and creates proposal with `source = 'chat_propose'`.
  - **Unanimous Path**: If all active members vote YES, slot confirms immediately (`CONFIRMED`), terminating any AI consensus loop.
  - **Majority Path**: If not unanimous, proposal enters standard proposal queue for the next round.

---

### 9.9 Solo & Guide Matchmaking

#### A. Match Group Trips (`POST /api/solo-matching/groups`)
- **Endpoint**: `POST /api/solo-matching/groups` (`routers/matching.py:L13`)
- **Current Implementation**: Computes compatibility between traveler and open group trips using Jaccard, language, and age brackets.
- **Required Behavior**: Returns sorted list of trips with integer compatibility scores 0–100. Uses authenticated identity `current_user.user_id`.
- **In-Process Service Handoff**:
  ```python
  matches = sharvani_matching_service.match_groups(db, user_id=current_user.user_id)
  ```
- **Response Example**:
  ```json
  [
    {
      "trip": { "trpId": "trp_kyoto_01", "title": "Kyoto Temples & Food" },
      "compatibilityScore": 92,
      "ageGroupMatch": true,
      "sharedLanguages": ["en", "ja"],
      "sharedInterests": ["temples", "culinary", "walking"],
      "dateOverlapDays": 5
    }
  ]
  ```

#### B. Match Tour Guides (`POST /api/solo-matching/guides`)
- **Endpoint**: `POST /api/solo-matching/guides` (`routers/matching.py:L87`)
- **Current Implementation**: Scores guides based on city, language, specialisation, rating, and budget fit.
- **Required Behavior**: Returns sorted list of guides with integer compatibility scores 0–100. Deterministic scoring without LLM calls.

---

### 9.10 Photos & Memories Orchestration

#### A. Upload Photo (`POST /api/photos`)
- **Endpoint**: `POST /api/photos` (`routers/photos.py:L29`)
- **Current Implementation**: Accepts multipart form, saves to `static/uploads/`, sends relative URL to worker, sets `completed` prematurely.
- **Required Behavior**:
  1. Validates trip membership in Neon PostgreSQL via Sharvani's service.
  2. Saves photo bytes to disk (`backend/static/uploads/`).
  3. Calls Sharvani's in-process `photo_service.save_uploaded_photo_record(db, ..., initial_status="pending")`.
  4. Calls Sharvani's in-process `photo_service.get_candidate_member_embeddings(db, trip_id)` to get candidate member vectors.
  5. Streams multipart image binary bytes + candidate vectors payload to DeepFace worker on port 8001 (`POST /api/face/match-photo`).
  6. If worker succeeds: calls Sharvani's in-process `save_photo_tags_records(db, photo_id, face_matches, final_status="processed")`.
  7. If worker times out/fails: calls Sharvani's in-process `save_photo_tags_records(db, photo_id, [], final_status="failed")`. Worker timeout/failure must NEVER map to `'processed'` or `"completed"`.
  8. Returns photo response model omitting all raw embedding vectors, mapping storage status to wire:
     | Database Storage (`Photo.processing_status`) | Wire Response (`processingStatus`) | Semantics & Edge Cases |
     | :--- | :--- | :--- |
     | `'pending'` | `"pending"` | Initial record created, awaiting DeepFace worker. |
     | `'processed'` | `"completed"` | Face recognition succeeded (including zero detected faces or unmatched/unknown faces with `unidentified_faces = True`). |
     | `'failed'` | `"failed"` | DeepFace worker timeout (504), worker crash, or image decode failure. |
  9. **Concrete Router Response Construction & Normalization Step**:
     Panchami's router receives persisted records (`List[PhotoPerson]` in production or `List[Dict[str, Any]]` from `FakePhotoService`), normalizes them via `normalize_photo_tag_record`, maps storage status to wire status, and constructs the response:
     ```python
     storage_status = "processed" if matches.is_success else "failed"
     persisted_tags = sharvani_photo_service.save_photo_tags_records(
         db=db,
         photo_id=photo_id,
         face_matches=matches.tags,
         final_status=storage_status
     )
     # Router invokes normalizer over each record before wire serialization:
     normalized_tags = [normalize_photo_tag_record(t) for t in persisted_tags]
     wire_status = "completed" if storage_status == "processed" else "failed"

     return {
         "status": "uploaded",
         "photoId": photo_id,
         "tripId": trp_id,
         "photoUrl": photo_url,
         "processingStatus": wire_status,
         "facesDetected": matches.detected_faces_count,  # Runtime worker metric
         "taggedMembers": normalized_tags
     }
     ```
  10. **Service-Facing DTO Normalizer (`normalize_photo_tag_record`)**:
     ```python
     def normalize_photo_tag_record(record: Union[PhotoPerson, Dict[str, Any]]) -> Dict[str, Any]:
         """Authoritative adapter normalizing both production SQLAlchemy PhotoPerson ORM records
         and FakePhotoService dictionary records into an identical service-facing DTO shape."""
         if isinstance(record, dict):
             # Fake dictionary record: must provide explicit identifier (pp_id or tagId/tag_id) and photo_id
             tag_id = record.get("pp_id") or record.get("tagId") or record.get("tag_id")
             photo_id = record.get("photo_id") or record.get("photoId")
             if not tag_id or not photo_id:
                 raise ValueError(f"ERR_INVALID_TAG_RECORD: Missing required identity (pp_id/tagId or photo_id) in {record}")
             return {
                 "tagId": str(tag_id),
                 "photoId": str(photo_id),
                 "userId": record.get("user_id") or record.get("userId"),
                 "confidence": float(record.get("confidence", 0.0)),
                 "box": record.get("box") or record.get("bounding_box")
             }
         else:
             # Production SQLAlchemy PhotoPerson ORM record (backend/app/models/additive.py:89)
             # Uses actual primary key pp_id (not invented person_id or tag_{user_id})
             pp_id = getattr(record, "pp_id", None)
             if not pp_id:
                 raise ValueError(f"ERR_INVALID_ORM_TAG: PhotoPerson record missing primary key pp_id: {record}")
             return {
                 "tagId": str(pp_id),
                 "photoId": str(record.photo_id),
                 "userId": str(record.user_id),  # Current PhotoPerson.user_id is NOT NULL
                 "confidence": float(record.confidence) if record.confidence is not None else 0.0,
                 "box": None  # Current photo_person schema lacks bounding_box column; represented honestly as None
             }
     ```
  11. **Photo Recognition Architecture & Storage Layers**:
     - `photos` table: `photo_id`, `trip_id`, `uploader_id`, `photo_url`, `processing_status`, `created_at`. It contains **NO** `detected_faces_count` or `matched_count` columns.
     - `photo_person` table: `pp_id` (PK), `photo_id`, `user_id` (`nullable=False`), `confidence`. Unknown face instances cannot be stored as `user_id = None`.
     - DeepFace worker returns runtime counts (`detected_faces_count`, `matched_count`) and bounding boxes in memory/HTTP payloads.
     - On gallery reload (`GET /api/photos/{trp_id}`), the database contains only `photo_person` and `processing_status`. Absence of recognized tags must **NEVER** be misclassified as "Scenery".
     - Durable persistence of face instances and counts (`photo_face_tags` / extended `photos`) is a pending target migration owned by Sharvani.
- **Request Example**: `multipart/form-data`: `file: <binary>`, `trpId: "trp_a91f3c2b"`
- **Response Example**:
  ```json
  {
    "status": "uploaded",
    "phoId": "pho_5b2d9e",
    "trpId": "trp_a91f3c2b",
    "photoUrl": "/static/uploads/pho_5b2d9e.jpg",
    "processingStatus": "completed",
    "taggedMembers": [
      { "userId": "usr_alice", "confidence": 0.96, "box": { "x": 120, "y": 80, "w": 65, "h": 70 } }
    ],
    "createdAt": "2026-10-29T10:15:00Z"
  }
  ```

#### B. Get Trip Photos (`GET /api/photos/{trp_id}`)
- **Endpoint**: `GET /api/photos/{trp_id}` (`routers/photos.py:L149`)
- **Current Implementation**: Queries photos with optional `folder` or `taggedUserId` filter.
- **Required Behavior**: Returns photo metadata list. Omits all 512-d ArcFace floating-point vectors from response.

#### C. Get Trip Memories Board (`GET /api/trips/{trip_id}/memories`)
- **Endpoint**: `GET /api/trips/{trip_id}/memories` (`routers/photos.py:L117`)
- **Current Implementation**: Returns categorized albums (`GroupPhotos`, `Scenery`, `MemberAlbums`).

---

### 9.11 Face Profile Enrollment & Recognition

#### A. Enroll Face (`POST /api/face/register`)
- **Endpoint**: `POST /api/face/register` (`routers/face.py:L14`)
- **Current Implementation**: Stores metadata in SQLite; does not invoke DeepFace worker.
- **Required Behavior**:
  - Enforces exactly 3 enrollment photos (`straight`, `left`, `right`).
  - Quality gate: exactly 1 face per image. Rejects multi-face or scenery photos (`400 Bad Request`).
  - DeepFace worker extracts 512-d ArcFace vector and stores it via Sharvani's in-process `save_face_profile_record`.
  - Atomic enrollment: if any of the 3 photos fails face detection, the entire enrollment fails.
- **Errors**: `400 Bad Request` (`FACE_NO_FACE_DETECTED` or `FACE_MULTIPLE_FACES`).

#### B. Face Registration Status (`GET /api/face/status/{usr_id}`)
- **Endpoint**: `GET /api/face/status/{usr_id}` (`routers/face.py:L90`)
- **Current Implementation**: Returns whether user has enrolled face profile (`enrolled: true/false`).
- **Required Behavior**: Returns boolean enrollment status; never exposes biometric vectors.

---

### 9.12 PDF Export Transport

- **Endpoint**: `GET /api/trips/{trip_id}/export/pdf` `[REQUIRED TARGET / PENDING RENDERER (Decision #30)]`
- **Required Behavior**:
  - Access control: requires user to be confirmed trip member.
  - Snapshot: calls Sharvani's in-process `trip_service.get_itinerary_export_snapshot(db, trip_id)`.
  - Transport: streams binary `application/pdf` with `Content-Disposition: attachment; filename="itinerary_{trip_id}.pdf"`.
  - Unresolved slot handling: slots marked `IN_CONSENSUS` or `BRANCHED` render with distinct watermarks indicating pending resolution.

---


<a id="member-phase-5"></a>
## Phase 5 — Investigate cross-member performance

Read the retained sections below together for this phase:

- 13.1 CROSS-MEMBER LOADING & CLERK PERFORMANCE INVESTIGATION PROTOCOL (TRANSPORT TASK CARD)

## 13.1 CROSS-MEMBER LOADING & CLERK PERFORMANCE INVESTIGATION PROTOCOL (TRANSPORT TASK CARD)

This protocol governs the cross-member performance triage for severe loading issues reported during Trip Home rendering and Clerk user authentication. Panchami owns the gateway, HTTP router, and WebSocket transport latency profiling track.

### 1. Transport Investigation Scope & Responsibilities
- **HTTP Endpoint Latency Profiling**:
  * Instrument FastAPI middleware to record request-response round-trip durations (`X-Response-Time-Ms`).
  * Measure request deserialization, Pydantic model validation overhead, and JSON response serialization times across core routes (`GET /api/trips/{trp_id}`, `GET /api/trips/{trip_id}/chat`, `POST /api/votes`).
- **WebSocket Connection Handshake & Ping-Pong Latency**:
  * Measure WebSocket connection upgrade duration, query parameter JWT validation latency, and initial connection handshake.
  * Measure delivery latency of `resyncSnapshot` and real-time broadcast events (`voteCast`, `slotStatusChanged`).
- **Clerk Webhook Overhead (`POST /api/auth/webhook`)**:
  * Profile `svix` cryptographic signature verification latency (`[PROPOSED TARGET]`: Svix verification executes in $< 15\text{ms}$).
  * Measure total execution time of webhook handler from payload receipt to response return.
- **Privacy & Security during Instrumentation**:
  * Instrumentation logs must **NEVER** output JWT secrets, webhook signing secrets, biometric vectors, or raw user passwords.
- **Upstream & Downstream Timeout Mapping**:
  * Implement clean HTTP timeout handling for downstream calls (e.g. DeepFace worker on port 8001): return RFC 7807 `504 Gateway Timeout` with clear problem details when downstream calls exceed deadlines.
  * Ensure transport never hangs indefinitely on stalled background tasks.

### 2. Standardized Investigation Artifact Format
Panchami must log performance findings using the standardized four-part ledger:
- **Baseline**: Initial measured transport and network latency across core endpoints (in milliseconds).
- **Reproduction**: Exact curl or httpx test command reproducing the measured delay under concurrency.
- **Measured Bottleneck**: Concrete transport or network layer taking $> 100\text{ms}$ (e.g. "JSON serialization of large chat history taking 180ms due to unindexed relationship access").
- **Verification**: Post-optimization timing profile demonstrating verified latency reduction.

---


<a id="member-phase-6"></a>
## Phase 6 — Follow the execution checklist and integration checkpoints

Read the retained sections below together for this phase:

- 13. PHASE-BY-PHASE EXECUTION PLAN (PANCHAMI'S WORK)

## 13. PHASE-BY-PHASE EXECUTION PLAN (PANCHAMI'S WORK)

All phases link to authoritative decisions in [`docs/AI.md § 12`](AI.md#12-stack-neutral-decision-register).

### Phase 0: Baseline Verification & Microservice Isolation (Hours 0–2)
- Verify FastAPI router registrations (`auth`, `trips`, `matching`, `consensus`, `photos`, `face`) mounted in `backend/app/main.py`.
- Verify DeepFace worker boots cleanly on Port 8001 (`uvicorn backend.main:app --port 8001`).
- Execute isolated recognition tests in `ai/DeepFace/tests/` with real test images (Straight, Left, Right).
- Confirm database connection engine (`backend/app/database.py`) and Alembic migration `c8a6a4789a32` with Sharvani (Decision #16).

### Phase 1: Transport Tightening & Schema Validation (Hours 2–5)
- Reconcile all Pydantic wire models in `backend/app/schemas/` to strictly emit camelCase aliases.
- Implement strict input validations on `POST /api/proposals` and `POST /api/votes` (Rules 1 & 2).
- Verify `POST /api/auth/webhook` extracts Svix headers and delegates verification in-process to Sharvani's security service.
- Verify `POST /api/proposals/check-timer` correctly maps to consensus timer logic.

### Phase 2: WebSocket Connection Hardening & Resync (Hours 5–8)
- Enforce WebSocket query parameter `?token=...`.
- Verify close codes 4401 (unauthorized) and 4403 (forbidden).
- Ensure `resyncSnapshot` is immediately delivered to connecting clients.
- Verify event broadcasts: `voteCast`, `proposalCreated`, `slotStatusChanged`, `aiRecommendationReady` / `aiPlanGenerated`.

### Phase 3: Vote Invariants & Mode NA Countdown Integration (Hours 8–12)
- Wire `POST /api/votes` to call Sharvani's `voting_service.cast_vote` in-process.
- Verify single active YES auto-retraction (`AC-VOT-02`) across competing proposals in the same slot.
- Verify Mode NA timer trigger: first NO vote sets `slot_consensus.closes_at` (Decision #31 pending duration sign-off).

### CHECKPOINT 1 — Hour 12: Core Consensus & Transport Freeze
- **Test with Nikitha**: Create trip, submit proposal, vote NO with reason, verify `slot_consensus.closes_at` countdown starts and WebSocket broadcasts land in browser.

### Phase 4: Photo Orchestration & Real Multipart Streaming (Hours 12–16)
- Refactor `POST /api/photos` to stream real multipart binary bytes + candidate vectors payload to DeepFace worker on port 8001 (Decision #9).
- Implement instance-counting face logic (`face_index`, `detected_faces_count` vs `matched_count`).
- Wire Sharvani's photo persistence functions in-process (`save_uploaded_photo_record`, `save_photo_tags_records`).
- Implement worker failure handling (`processing_status = 'failed'`).

### Phase 5: Branches, Chat & Solo Matchmaking Transport (Hours 16–19)
- Wire `GET/POST /api/trips/{trip_id}/chat` and `POST /api/chat/{msg_id}/propose`.
- Implement `GET /api/branches/{itm_id}` and `POST /api/branches/{brc_id}/confirm`.
- Wire `POST /api/solo-matching/groups` and `POST /api/solo-matching/guides` to Sharvani's deterministic scorers in-process.

### Phase 6: Cross-Boundary End-to-End Click-Through (Hours 19–21)
- Verify end-to-end user journey with Nikitha's frontend connecting to live endpoints (`VITE_USE_MOCK_DATA=false`).
- Fix any route mismatches or field naming discrepancies.

### CHECKPOINT 2 — Hour 21: Feature Freeze & Merge

### Phase 7: Demo Hardening & Rehearsal (Hours 21–24)
- Fix only defects in the rehearsed demo path. Zero new features.

---

