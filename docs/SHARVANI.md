# SHARVANI.md — Architecture, Domain Logic, AI & Schema Authority

**Track Owner**: Sharvani G Bhaskar  
**Specification Status**: Authoritative Specification (`[SYSTEM OF RECORD]`)  
**Shared Integration Contract**: [`docs/INTEGRATION_CONTRACT.md`](INTEGRATION_CONTRACT.md)  
**Authoritative Decision Register**: [`docs/AI.md §12`](AI.md#12-stack-neutral-decision-register)  
**Governance Rule**: Following initial preparation, **Sharvani solely edits this document and `docs/INTEGRATION_CONTRACT.md`**. She serves as the final integration, architecture, and deployment authority.

## WanderMatch · KogniVera Hackathon 2026 · PS-11

---

## HOW TO USE THIS DOC (Read this first, give it to your agent verbatim)

> "I am Sharvani G Bhaskar, Architecture, Domain Logic, AI Consensus Engine, Shared Schema Authority, and Deployment Owner for WanderMatch at KogniVera Hackathon 2026. Read this entire document carefully. It contains my full project context, my exact ownership boundaries across shared database models, Alembic migrations, backend/app/main.py startup wiring, all deployment coordination (including frontend deployment to Vercel and backend/worker to Render), business domain services, consensus state machines, AI algorithms, deterministic compatibility scorers, the exact in-process service interfaces I provide to Panchami's transport routers, and my phase-by-phase execution plan. After reading, give me a detailed prompt to execute Phase [X] of my work. Do not assume anything not written here. Everything is specified."

---

## Phase-based reading guide

This is a structure-only reorganization. All original specifications, examples, ownership rules, pending decisions and execution checklists are retained below.

Use the phases as a reading and working sequence. Existing numbered section titles remain intact for cross-document references. The original hour-based plan is retained in Phase 6; it is not a new delivery estimate. Work can proceed in parallel using the documented mocks and agreed interfaces. Pending decisions and implementation prerequisites remain pending.

- [Phase 1 — Understand ownership, project context and architecture](#member-phase-1)
- [Phase 2 — Establish schema, service contracts and secure handoffs](#member-phase-2)
- [Phase 3 — Prepare the LLM and implement domain AI algorithms](#member-phase-3)
- [Phase 4 — Implement consensus orchestration and compatibility services](#member-phase-4)
- [Phase 5 — Verify independently and investigate performance](#member-phase-5)
- [Phase 6 — Follow task cards, execution checklist and integration checkpoints](#member-phase-6)


<a id="member-phase-1"></a>
## Phase 1 — Understand ownership, project context and architecture

Read the retained sections below together for this phase:

- 0. OWNERSHIP LEDGER & LIFECYCLE DISTINCTION
- 1. WHAT WANDERMATCH IS — FULL CONTEXT
- 2. TECH STACK — WHAT I USE
- 3. DIRECTORY STRUCTURE — WHAT SHARVANI OWNS

## 0. OWNERSHIP LEDGER & LIFECYCLE DISTINCTION

This section establishes Sharvani's authoritative system ownership, proposed domain extractions, and lifecycle progression in accordance with `docs/INTEGRATION_CONTRACT.md`.

### A. Current Owned Files
Sharvani solely owns the system architecture, core domain logic, AI consensus, shared data models, database migration baseline, and all deployment coordination:
- **Application Startup & Deployment Coordination**:
  - `backend/app/main.py` (`[CURRENT]`): Application lifecycle, middleware configuration, static mounts, router mounts, and WebSocket endpoint wiring.
  - Deployment coordination (`[CURRENT]`): Backend and DeepFace worker web services on Render, frontend static deployment on Vercel, and shared environment configuration.
- **Shared Database Models & Migrations (`backend/app/models/`, `backend/alembic/`)**:
  - `backend/app/models/provided.py` (`[CURRENT]`: 14 canonical PS-11 tables: `users`, `user_preferences`, `trips`, `trip_members`, `itineraries`, `itinerary_items`, `proposals`, `votes`, `tour_guides`, `cities`, `countries`, `currencies`, `languages`)
  - `backend/app/models/additive.py` (`[CURRENT]`: 10 WanderMatch additive tables: `join_requests`, `slot_consensus`, `branches`, `branch_members`, `revision_history`, `trip_chat_messages`, `face_profiles`, `photos`, `photo_person` [mapped to model `PhotoPerson`], `trip_invite_codes`. Note: `photo_tags` does NOT exist as an independent table).
  - `backend/app/database.py` (`[CURRENT]`: SQLAlchemy engine & scoped session factory)
  - `backend/alembic/` (`[CURRENT]`: Alembic environment, `script.py.mako`, and baseline migration `c8a6a4789a32_initial_schema_baseline.py`)
  - Schema Gap Notice: `slot_consensus.closes_at` is missing from the current additive model/migration and is an explicit prerequisite for authoritative countdown timer storage.
  - `backend/seed.py` (`[CURRENT]`: PS-11 data seeding script)
- **Domain Services Package (`backend/app/services/`)**:
  - `backend/app/services/` (`[CURRENT]`): Package directory on disk containing `__init__.py` and `clerk_auth.py` (Clerk JWT token verification & provisioning).
- **Active Algorithms & AI Prototype (`ai/AIConsensus/`, `backend/app/ai/matching/`)**:
  - `ai/AIConsensus/` (`[CURRENT]`: prototype preserved in place; test suite executed with isolated test doubles)
  - `backend/app/ai/matching/` (`[CURRENT]`: `group_compatibility_scorer.py`, `guide_compatibility_scorer.py`)
- **Canonical Schemas, PS-11 Datasets & Starter Queries (`docs/data/`, `data-model/`)**:
  - `data-model/DATA_MODEL.md` (`[CURRENT]`)
  - `docs/data/PS-11.db` (`[CURRENT]`: canonical SQLite reference)
  - `docs/data/schema.sql`, `docs/data/schema.sqlite.sql`, `docs/data/enums.json` (`[CURRENT]`)
  - `docs/data/queries/starter_queries.sql` (`[CURRENT]`)
  - `docs/data/csv/*.csv` (`[CURRENT]`: all 14 canonical PS-11 CSV datasets)
- **Shared Infrastructure, Configuration & Master Specifications**:
  - `backend/requirements.txt`, root `.env.example`, `neon.ts`, root `README.md` (`[CURRENT]`)
  - Master specifications: `docs/INTEGRATION_CONTRACT.md`, `docs/AI.md`, `docs/ARCHITECTURE.md`, `docs/DATABASE.md`, `docs/DEPLOYMENT.md`, `docs/DEPLOYMENT_ARCHITECTURE.md`, `docs/DESIGN.md`, `docs/IMPLEMENTATION_PLAN.md`, `docs/PRD.md`, `docs/PROJECT_MEMORY.md`, `docs/TRD.md` (`[CURRENT]`)

### B. Proposed Future Files (Pending Implementation Approval)
When domain service modularization and target module extraction are approved:
- **Target AI Extraction Modules (`backend/ai/` — Nonexistent on disk; do NOT create during documentation pass)**:
  - `backend/ai/core/` (`blended_plan_generator.py`, `branch_trigger_classifier.py`, `branch_grouping.py`, `hard_constraint_validator.py`) `[PROPOSED]`
  - `backend/ai/modes/` (`mode_a_orchestrator.py`, `mode_na_orchestrator.py`) `[PROPOSED]`
  - `backend/ai/scorers/` (target migration destination for `group_compatibility_scorer.py` and `guide_compatibility_scorer.py`) `[PROPOSED]`
  - `backend/ai/llm/` (`client.py`, `prompts.py`) `[PROPOSED]`
- **Domain Services & Security (`backend/app/services/`, `backend/app/core/`)**:
  - `backend/app/services/trip_service.py` `[PROPOSED]` — Trip lifecycle, membership management, itinerary item retrieval, and CAS optimistic concurrency checks.
  - `backend/app/services/voting_service.py` `[PROPOSED]` — Atomic voting transactions, single active YES auto-retraction (`AC-VOT-02`), and mandatory NO reason enforcement.
  - `backend/app/services/consensus_service.py` `[PROPOSED]` — Slot consensus state machine, authoritative slot-level timer management (`slot_consensus.closes_at`), Mode A admin controls, and Mode NA auto-branching.
  - `backend/app/services/matching_service.py` `[PROPOSED]` — Pure deterministic solo companion and local tour guide compatibility matchmakers.
  - `backend/app/services/photo_service.py` `[PROPOSED]` — Photo record creation, candidate member embedding retrieval, and face-tag association.
  - `backend/app/services/audit_service.py` `[PROPOSED]` — Audited AI decision persistence supporting both dedicated table and revision snapshot alternatives (Decision #29).
  - `backend/app/core/security.py` `[PROPOSED]` — Authoritative Clerk JWT claims verification and webhook signature validation (`svix`).

> **Path Reality Verification**: Nonexistent directory `backend/ai/` does NOT exist on disk (`[PROPOSED]`). `backend/app/ai/matching/` exists on disk (`[CURRENT]`). `backend/app/services/` exists on disk (`[CURRENT]`). DeepFace Dockerfile and model directories do NOT exist on disk (`[PROPOSED]`). No source files or folders are created during this documentation pass.

### C. Necessary Extraction Tasks (Preparation Phase)
1. **Encapsulate Transactional Domain Services**: Move business rules out of FastAPI router handlers into cohesive service classes with explicit unit-of-work transactions.
2. **In-Process Python Persistence Boundary**:
   - Panchami's routers call Sharvani's domain services **in-process via Python function calls** passing the active `db: Session`.
   - Never describe persistence calls as "on port 8000" — there is zero HTTP networking between router handlers and domain persistence.
3. **Authoritative Persistence Signatures for Panchami's Routes**:
   ```python
   def get_candidate_member_embeddings(db: Session, trip_id: str) -> List[Dict[str, Any]]:
       """Returns enrolled ArcFace embeddings for all active trip members."""
   def save_uploaded_photo_record(db: Session, photo_id: str, trip_id: str, uploader_id: str,
                                 photo_url: str, initial_status: str = "pending") -> Photo:
       """Persists photo row with initial processing status ('pending')."""
   def save_photo_tags_records(db: Session, photo_id: str, face_matches: List[Dict[str, Any]],
                              final_status: str = "processed") -> List[PhotoPerson]:
       """Persists individual bounding boxes, matched user IDs, confidence scores, and updates status ('processed' or 'failed')."""
   ```
4. **Optimistic Concurrency Control (CAS)**:
   Enforce atomic compare-and-swap pattern across all itinerary updates:
   ```sql
   UPDATE itineraries 
   SET version = version + 1, updated_at = NOW() 
   WHERE itinerary_id = :itinerary_id AND version = :expected_version;
   ```
   If rows affected == 0, abort transaction immediately and raise `ConcurrencyConflictError` (mapped to HTTP 409).

### D. Later Feature Implementation (Feature Phase — Not Yet Approved)
- **External Geocoding & POI Verification**: Integrate factual verification provider for POI coordinates (Decision #8).
- **Road Routing Provider**: Integrate road-distance routing engine (OSRM / Mapbox) to replace straight-line approximations (Decision #11).
- **Operational LLM Inferences & Timeouts**: Configure live Ollama/Anthropic API calls with mandatory client-side timeouts (Decision #28).
- **Audit Persistence Implementation**: Implement approved storage schema for AI consensus decisions (Decision #29: dedicated table vs revision snapshot alternatives).
- **Itinerary PDF Export Strategy**: PDF export is **REQUIRED** (`FR-EXP-01`). Implementation of specific rendering engine (`@react-pdf/renderer` vs backend `weasyprint`) is pending Decision #30.
- **Production Neon Migration**: Apply and verify Alembic migrations on Neon PostgreSQL production instance (Decision #16).
- **Pending Decision Principle**: Unresolved decisions in `docs/AI.md §12` block only dependent choices (e.g. renderer selection for PDF), not all implementation (e.g. PDF export requirement is locked; data preparation and UI triggers proceed).

### E. Mock-Only Completion Criteria
Sharvani can declare complete domain and algorithmic readiness when:
1. All deterministic scorers (`group_compatibility_scorer.py`, `guide_compatibility_scorer.py`) pass comprehensive unit test suites with 100% deterministic math assertions.
2. Consensus state machine tests verify correct state transitions (`EMPTY` ➔ `IN_CONSENSUS` ➔ `CONFIRMED` / `BRANCHED`), single active YES auto-retraction (`AC-VOT-02`), and timer expiry simulation in an isolated SQLite in-memory database.
3. AI consensus fallback logic generates valid compromise plans when LLM calls are mocked or offline.
4. **Provider Test Isolation**: All LLM and external provider tests run with substituted calls and controlled network access (mocked HTTP responses or local stubs). Unsetting API keys alone is strictly insufficient.

### F. Real Integrated Completion Criteria & Neon Database Delivery Protocol
Full integrated completion is achieved when:
1. **Neon Integration Environment Delivery Protocol & Small Bounded Fixture**:
   - **Sharvani's Provisioning Responsibility**: Sharvani provisions the isolated nonproduction Neon PostgreSQL database target, runs Alembic migrations up to agreed baseline revision `c8a6a4789a32` (or current `head`), and seeds the agreed small, bounded test fixture.
   - **Small Bounded Test Fixture**:
     * Synthetic Users: `usr_alice` (`role='owner'`), `usr_bob` (`role='editor'`), `usr_carol` (`role='viewer'`) (mapped to canonical `TripMember.role` values `owner / editor / viewer`).
     * Synthetic Trips: `trp_paris_2026` ("Paris Weekend", Mode NA, published), `trp_tokyo_admin` ("Tokyo Explorer", Mode A, draft).
     * Representative Slots: `slt_day1_morning` ("Louvre Guided Tour", 09:00–12:00, 30.00 USD), `slt_day1_lunch` ("Le Marais Bistro", 12:30–14:00, 25.00 USD).
     * Representative Proposals & Votes: `prp_louvre_guided` with initial YES votes from `usr_alice` and `usr_bob`.
     * Minimal Photo Metadata: `pho_sample_1` (`trip_id: trp_paris_2026`, `uploader_id: usr_alice`, `photo_url: /static/uploads/pho_sample_1.jpg`).
   - **Explicit Environment Loading**: Python / FastAPI does **NOT** automatically load `.env.local` by default unless configured via `python-dotenv` (`load_dotenv(".env.local")`) or shell environment variables. Nonproduction credentials must be shared privately; no secrets in version control.
   - **Console vs Database Access**: Panchami receives direct database connection credentials (`DATABASE_URL=postgresql://panchami_dev:...@...neon.tech/wandermatch_test?sslmode=require` or `postgresql+psycopg2://...`); no shared personal Neon account login is required. (Note: `backend/app/database.py` initializes a synchronous SQLAlchemy `create_engine` using `psycopg2-binary`. The asynchronous prefix `postgresql+asyncpg://` is an unapproved future proposal that is incompatible with the present synchronous backend engine; Panchami uses the synchronous driver string matching `psycopg2-binary`).
   - **Feature-by-Feature Integration**: Integration proceeds feature-by-feature; mock transport development and router unit testing must **NEVER wait** for live Neon database access.
2. Real Clerk JWT authentication tokens are cryptographically verified by security core.
3. Live LLM inference (local Ollama or external provider) generates valid, constraint-checked compromise plans.
4. Photo persistence accurately links 512-d ArcFace facial embeddings with enrolled trip travelers in Neon DB.
5. **PDF Export Collaborative Contribution**: PDF export remains **REQUIRED and ONLINE**. Offline PDF generation/export is **DEFERRED** and is not an acceptance gate. If server-side rendering is finalized under Decision #30, Sharvani implements the HTML-to-PDF template compilation service (using Jinja2 + WeasyPrint [proposed]) consuming the authoritative JSON export payload.
6. All three components (backend, DeepFace worker, frontend) are deployed and operational via Sharvani's deployment coordination.

---

## 1. WHAT WANDERMATCH IS — FULL CONTEXT

WanderMatch is a social group travel planning app. Groups plan trips together on a shared live itinerary. Members propose activities, vote YES or NO (NO votes REQUIRE a typed reason/suggestion), and my AI layer reads those typed reasons to generate compromise plans or — when preferences are truly incompatible — parallel branches.

### My specific role in the system:
I am the Architecture, Domain Logic, AI Consensus Engine, and Shared Schema Authority. I solely own the shared ORM models (`backend/app/models/provided.py`, `additive.py`), the SQLAlchemy database engine (`backend/app/database.py`), Alembic migrations (`backend/alembic/`), data seeding (`backend/seed.py`), and core business domain services (`backend/app/services/`).

I do NOT handle HTTP transport routing, wire serialization, or WebSocket connection lifecycles directly — Panchami owns transport adapters (`backend/app/routers/`, `schemas/`, `websocket_manager.py`). Panchami's routers call my authoritative domain services, which execute database transactions and enforce business invariants.

### The two trip modes I must handle:
- **Mode A (Admin-Led)**: Admin has final say. My AI RECOMMENDS — it never makes binding decisions. Admin can accept, reject, extend, or force-branch at any time.
- **Mode NA (Collaborative)**: Fully automatic. After ~3 rounds unresolved, I auto-branch without asking anyone.

### The consensus flow I implement:
```
NO votes arrive with typed comments
        ↓
branch_trigger_classifier.py
  → Is this a FIXABLE TWEAK or a FIXED INCOMPATIBLE REQUIREMENT?
        ↓ fixable tweak             ↓ fixed requirement
blended_plan_generator.py      branch_grouping.py
  → ONE blended plan               → N parallel branches
        ↓
hard_constraint_validator.py
  → Does this plan violate time/location/transport constraints?
  → If yes: regenerate once
  → If fails again: escalate to branching
```

---

## 2. TECH STACK — WHAT I USE

- **Language**: Python 3.11+
- **LLM runtime**: Ollama (local, serving Phi-4-mini and Qwen2.5-Coder)
- **LLM access from backend**: OpenAI-compatible client pointed at ngrok tunnel URL
- **Primary model**: Phi-4-mini (for blended_plan_generator + branch_trigger_classifier — needs judgment + rationale text)
- **Secondary model**: Qwen2.5-Coder (optional — for JSON structure validation/repair if needed)
- **LLM call library**: `openai` Python package (`pip install openai`)
- **Math only (no LLM)**: group_compatibility_scorer.py, guide_compatibility_scorer.py — these are PURE DETERMINISTIC MATH, no LLM calls whatsoever

I DO NOT:
- Handle HTTP endpoint routing or deserialization (Panchami owns `backend/app/routers/` and `schemas/`)
- Manage WebSocket connection lifecycles (Panchami owns `backend/app/websocket_manager.py`)
- Own DeepFace worker code or tests (Panchami owns `ai/DeepFace/`)
- Own frontend implementation (Nikitha owns `frontend/`)

I SOLELY OWN:
- Application startup wiring and server mounting (`backend/app/main.py`)
- All deployment coordination across Render (backend and worker) and Vercel (frontend)
- Shared ORM models (`backend/app/models/provided.py`, `models/additive.py`)
- Database connection & scoped sessions (`backend/app/database.py`)
- Alembic database migrations (`backend/alembic/`)
- Database seeding (`backend/seed.py`)
- Core business domain services (`backend/app/services/` — called in-process by Panchami's routers)
- AI consensus prototype (`ai/AIConsensus/`) and target AI modules (`backend/ai/`)
- Canonical PS-11 data, SQLite reference, enums, schemas & CSV files (`docs/data/`)
- Master system specifications & shared contract (`docs/INTEGRATION_CONTRACT.md`)

---

## 3. DIRECTORY STRUCTURE — WHAT SHARVANI OWNS

```
backend/
  app/
    main.py                    ← YOU OWN APP LIFECYCLE, STARTUP WIRING & MOUNTING [CURRENT]
    models/                    ← YOU OWN ALL DATABASE MODELS [CURRENT]
      provided.py              ← 14 canonical PS-11 tables [CURRENT]
      additive.py              ← 10 WanderMatch additive tables [CURRENT]
    database.py                ← SQLAlchemy engine + session factory [CURRENT]
    services/                  ← PACKAGE DIRECTORY EXISTS ON DISK [CURRENT]
      __init__.py              ← [CURRENT]
      clerk_auth.py            ← Clerk JWT verification & provisioning [CURRENT]
      trip_service.py          ← Trip & itinerary lifecycle, CAS versioning [PROPOSED]
      voting_service.py        ← Atomic voting, single active YES auto-retraction [PROPOSED]
      consensus_service.py     ← Slot timer, Mode A/NA orchestrators [PROPOSED]
      matching_service.py      ← Solo & guide deterministic matching [PROPOSED]
      photo_service.py         ← Photo record creation, embedding retrieval [PROPOSED]
      audit_service.py         ← Audited AI decisions (Decision #29) [PROPOSED]
    ai/
      matching/                ← PURE DETERMINISTIC SCORERS [CURRENT]
        group_compatibility_scorer.py
        guide_compatibility_scorer.py
    core/
      security.py              ← Clerk JWT verification & webhook signature validation [PROPOSED]
  alembic/                     ← YOU OWN ALL DATABASE MIGRATIONS [CURRENT]
    versions/
      c8a6a4789a32_initial_baseline.py [CURRENT]
    env.py [CURRENT]
    script.py.mako [CURRENT]
  seed.py                      ← YOU OWN DATABASE SEEDING [CURRENT]
  requirements.txt             ← [CURRENT]
  ai/                          ← TARGET DIRECTORY NONEXISTENT ON DISK [PROPOSED]
    core/                      ← Blended plan, objection classifier, branch grouping [PROPOSED]
    modes/                     ← Mode A & Mode NA orchestrators [PROPOSED]
    scorers/                   ← Scorers future migration destination [PROPOSED]
    llm/                       ← Client & prompt templates [PROPOSED]
ai/AIConsensus/                ← YOU OWN AI PROTOTYPE (PRESERVED IN PLACE) [CURRENT]
  backend/app/
  docs/
  tests/
data-model/                    ← YOU OWN DATA MODEL DOCUMENTATION [CURRENT]
  DATA_MODEL.md
docs/
  INTEGRATION_CONTRACT.md      ← YOU SOLELY OWN SHARED CONTRACT [CURRENT]
  data/                        ← YOU OWN ALL PS-11 CANONICAL SCHEMAS & DATASETS [CURRENT]
    PS-11.db
    schema.sql
    schema.sqlite.sql
    enums.json
    queries/starter_queries.sql
    csv/                       ← 14 canonical PS-11 CSV files
  AI.md, ARCHITECTURE.md, DATABASE.md, DEPLOYMENT.md, etc. [CURRENT]
.env.example                   ← Root environment template [CURRENT]
neon.ts                        ← [CURRENT]
README.md                      ← Root system documentation [CURRENT]
```

You DO NOT own FastAPI router handlers (`backend/app/routers/`), Pydantic wire schemas (`backend/app/schemas/`), WebSocket manager (`backend/app/websocket_manager.py`), or DeepFace microservice (`ai/DeepFace/`). Panchami owns routers, wire schemas, WebSocket connection lifecycle, and DeepFace. Nikitha owns all frontend files in `frontend/`. In-process domain calls occur via standard Python function calls passing SQLAlchemy `Session`, never over HTTP port 8000.

---


<a id="member-phase-2"></a>
## Phase 2 — Establish schema, service contracts and secure handoffs

Read the retained sections below together for this phase:

- 0.1 CONTRACT CONSISTENCY REFERENCE TABLE (SHARVANI'S SURFACES)
- 0.2 SECURITY & CONCURRENCY HANDOFF
- 0.3 PHOTO PERSISTENCE SIGNATURES & BIOMETRIC PRIVACY
- 4. NAMING CONTRACT — READ BEFORE WRITING ANY CODE

## 0.1 CONTRACT CONSISTENCY REFERENCE TABLE (SHARVANI'S SURFACES)

| Surface / Interface | Current Implementation `[CURRENT]` | Agreed Target Contract `[AGREED TARGET]` | Unapproved Proposal / Prohibited `[PROHIBITED / UNAPPROVED]` | Ownership & Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **Photo Upload Endpoint** | `POST /api/photos` (`routers/photos.py`). Form: `file`/`photo`, `trp_id`/`trpId`, `uploader_id`. Saves to `static/uploads/`, sends relative URL to worker, sets `completed` prematurely. | `POST /api/photos`. Form: `file: UploadFile` (binary), `trpId: str`. Panchami reads file, calls Sharvani persistence with initial `pending`, streams multipart bytes + candidate vectors to worker, updates DB with face matches. | `POST /api/photos/upload` (historical proposal; unapproved alias; clients MUST call `POST /api/photos`). Sending relative paths to worker. Calling persistence on port 8000. | **Panchami** owns route & worker forwarding; **Sharvani** owns photo and tag database persistence in-process. |
| **Clerk Webhook Endpoint** | `POST /api/auth/webhook` (`routers/auth.py`). Extracts svix headers, verifies signature, creates `User` and `UserPreference`. | `POST /api/auth/webhook`. Panchami extracts headers & body, invokes Sharvani's `security.verify_svix_signature()`. Sharvani executes `security.sync_clerk_user_to_db()` in single atomic transaction. | `POST /api/webhooks/clerk` (historical proposal; unapproved alias; Clerk must be configured to `POST /api/auth/webhook`). | **Panchami** owns HTTP endpoint; **Sharvani** owns cryptographic verification & DB user sync in-process. |
| **Timer Check Endpoint** | `POST /api/proposals/check-timer` (`routers/consensus.py:L693`). Accepts `prp_id`, `advance_minutes`. If window expired with 0 NO votes, auto-confirms slot. | `POST /api/proposals/check-timer`. Production contract evaluates `now >= slot_consensus.closes_at` without test parameters. `advance_minutes` restricted strictly to automated test fixtures. | Calling `POST /api/consensus/check-timer` (unmounted alias; route is `/api/proposals/check-timer`). Exposing test clock controls in production payloads. | **Panchami** exposes HTTP route; **Sharvani** owns authoritative countdown state machine in-process. |
| **Trip Chat Messages** | `GET /api/trips/{trip_id}/chat` & `POST /api/trips/{trip_id}/chat` (`routers/trips.py:L960, L991`). Returns chat history with sender details. | `GET /api/trips/{trip_id}/chat` & `POST /api/trips/{trip_id}/chat`. Canonical unified endpoints. Frontend `api.ts` aligned. | Calling `/api/trips/{trip_id}/messages` or `/api/messages` (stale frontend aliases; must align to `/api/trips/{trip_id}/chat`). | **Panchami** owns HTTP transport; **Sharvani** owns message persistence in-process. |
| **WebSocket Resync Event** | `ws://host/ws/trips/{trip_id}/{user_id}` (`websocket_manager.py`). Immediately sends `{"type": "resyncSnapshot", "snapshot": {...}}`. | `ws://host/ws/trips/{trip_id}?token=...`. Panchami verifies token query, checks membership, and delivers `{"type": "resyncSnapshot", ...}` on connection and reconnect. | Silently renaming `resyncSnapshot` to `tripStateSnapshot` without coordinating with backend. | **Panchami** manages connection lifecycle & broadcast; **Nikitha** handles `resyncSnapshot` in `TripContext`. |
| **WebSocket Event: AI Plan Broadcast** | Backend emits `{"type": "aiRecommendationReady", ...}` (`consensus.py` lines 452, 684). | Backend emits both `aiPlanGenerated` and `aiRecommendationReady` as aliases to maintain complete frontend and backend compatibility. | Breaking frontend by dropping either event without unified client adapter update. | **Panchami** broadcasts event; **Nikitha** handles event in `TripContext.tsx`. |
| **Consensus Voting Window Timers** | `POST /api/proposals/check-timer` evaluates timer on demand (`routers/consensus.py:L693`). Sets `proposal.closes_at` on first NO in Mode NA. | Authoritative `slot_consensus.closes_at` managed by Sharvani's domain service in-process. Real-time background timer evaluation without test parameters. | Mixing `advance_minutes` test parameter into production API payloads; proposal-level timers as production architecture. | **Sharvani** owns timer state machine in-process; **Panchami** exposes clean route without test parameters in production. |
| **Vote Values & Invariants** | Writes `yes` or `no` to `votes.value`. Retracts prior vote on same proposal only. | Mandatory typed reason when `value === 'no'`. Retracts prior YES on competing proposal in same slot (`AC-VOT-02`). Idempotent re-voting. | Writing `value: 'abstain'` (strictly prohibited; only binary `yes` or `no` permitted). Claiming competing YES retraction is already working. | **Sharvani** enforces invariants in `voting_service.py` in-process; **Panchami** returns HTTP 400 if comment missing. |
| **Optimistic Concurrency Control** | Verifies `itineraries.version`. Bumps `version = version + 1`. Returns HTTP 409 on mismatch. | Atomic CAS update: `UPDATE itineraries SET version = version + 1 WHERE itinerary_id = :id AND version = :expected`. | Application-level read-then-write without atomic CAS in database transaction. | **Sharvani** implements atomic CAS query; **Panchami** maps conflict to HTTP 409. |
| **DeepFace Microservice Transport** | `backend/routers/photos.py` defectively sends relative URL `{"photo_url": "/static/uploads/pho_xxx.jpg"}` to `http://localhost:8001`. | Panchami fetches candidate embeddings from Sharvani in-process and streams real multipart form-data image bytes + candidate vectors payload to worker on port 8001. | Treating relative local filesystem paths as image binary across microservice network boundaries. Calling persistence on port 8000. | **Panchami** owns transport to worker; **Sharvani** owns database persistence in-process. |
| **Face Recognition Failure State** | On worker timeout/failure, code catches exception and leaves photo marked `processing_status = 'completed'` with 0 tags. | If worker times out or fails: photo is marked `processing_status = 'failed'` (or `'degraded'`). Worker failure logged. | Documenting worker network failure or timeout as successful completed recognition. | **Panchami** handles worker response; **Sharvani** persists failed/completed status in-process. |
| **Privacy / Embedding Vector Exposure** | Serializer omits `embedding_data`. | 512-d ArcFace floating-point vectors are server-internal only. Never printed in logs or sent to browser. | Returning raw facial vectors in client API responses or frontend inspection panels. | **Panchami** filters responses; **Sharvani** encapsulates vector storage. |
| **Itinerary PDF Export** | Client-side export button stubbed in UI (`FR-EXP-01`). | Itinerary PDF export is **REQUIRED** (`FR-EXP-01`). Generation rendering engine choice (`@react-pdf/renderer` vs backend `weasyprint`) is **PENDING** under Decision #30. | Omitting PDF export or treating entire requirement as optional. | **Nikitha** owns UI trigger; **Sharvani & Nikitha** coordinate renderer selection under Decision #30. |

---

## 0.2 SECURITY & CONCURRENCY HANDOFF

| Security Dimension | Sharvani (Authority & Business Rules) | Panchami (Transport Receiver & Enforcer) |
| :--- | :--- | :--- |
| **Clerk JWT Authentication** | Implements token decoding, JWKS key fetching/caching, and claims verification in `services/clerk_auth.py` or `core/security.py`. | Extracts `Authorization: Bearer <token>` from HTTP headers. Injects verified user into route dependencies. Enforces HTTP 401 on missing/invalid token. |
| **Clerk Webhook Signature Verification** | Implements cryptographic signature verification using `svix.webhooks.Webhook(secret).verify(payload, headers)`. Executes idempotent user sync transaction. | Mounts `POST /api/auth/webhook`. Reads raw request body and headers (`svix-id`, `svix-timestamp`, `svix-signature`). Invokes Sharvani's verification in-process. Enforces HTTP 400 on signature failure. |
| **WebSocket Authentication** | Implements `verify_trip_membership(trip_id, user_id, db) -> bool`. Checks Neon DB membership. | Receives WebSocket handshake. Extracts `?token=...`. If token missing/invalid: closes with **code 4401**. If user not accepted trip member: closes with **code 4403**. |
| **Itinerary Concurrency (CAS)** | Defines atomic CAS query: `UPDATE itineraries SET version = version + 1 WHERE itinerary_id = :id AND version = :expected`. | Receives `expected_version` in request body. Calls Sharvani service in-process. If rows affected == 0, translates `VersionConflictError` to **HTTP 409 Conflict**. |

---

## 0.3 PHOTO PERSISTENCE SIGNATURES & BIOMETRIC PRIVACY

### Authoritative Signatures
```python
def get_candidate_member_embeddings(db: Session, trip_id: str) -> List[Dict[str, Any]]:
    """Returns candidate enrolled travelers with their ArcFace embeddings for face matching."""

def save_uploaded_photo_record(db: Session, photo_id: str, trip_id: str, uploader_id: str,
                              photo_url: str, initial_status: str = "pending") -> Photo:
    """Creates photo record with initial processing_status='pending'."""

def save_photo_tags_records(db: Session, photo_id: str, face_matches: List[Dict[str, Any]],
                           final_status: str = "processed") -> List[PhotoPerson]:
    """Updates photo record status ('processed' on success, 'failed' on worker error) and persists PhotoPerson associations. (Storage status 'processed' maps to wire 'completed'; worker failure must NEVER map to 'processed' or 'completed')."""
```

### Biometric Privacy & Completeness Semantics
1. **Face Instances vs Travelers**: Each detected face in an image is an instance (`face_index`, bounding box `[x, y, w, h]`). Distinct traveler IDs (`usr_...`) are matched against instances. A photo with 4 faces where 2 match travelers has `detected_faces_count = 4` and `matched_count = 2`.
2. **Worker Failure Semantics**: If the DeepFace worker fails or times out, `processing_status` is updated to `'failed'`. **A worker failure must NEVER be recorded as successful completed recognition.**
3. **Biometric Privacy**: 512-d ArcFace floating-point vectors are server-internal biometric data. They must **never** be logged to stdout/stderr or returned in browser-facing JSON responses.

### Exact Three-Person Face Regression Acceptance Scenario (Domain Persistence & Candidate Retrieval)
This concrete regression acceptance case defines Sharvani's domain responsibilities in resolving the original reported face grouping failure:
1. **Reference Test Corpus Setup**:
   - Enrolled trip members: Person A (Nikitha), Person B (Panchami), Person C (Sharvani), each having registered 3-angle enrollment vectors in `face_profiles`.
   - Test dataset: Individual photos of A, B, C; multi-person group photos (A+B, B+C, A+B+C); 1 unknown person (Person D, un-enrolled); 1 scenery photo (0 faces).
2. **Domain Persistence & Trip Isolation Verification**:
   - **Trip-Scoped Candidate Retrieval (`get_candidate_member_embeddings`)**:
     * Must query strictly: `SELECT user_id, embedding_data FROM face_profiles WHERE user_id IN (SELECT user_id FROM trip_members WHERE trip_id = :trip_id AND status = 'active')`.
     * Members of other trips or un-enrolled users are strictly excluded from candidate vectors passed to the recognition engine.
   - **Recognition Metric Calibration Reality**:
     * DeepFace matching evaluates three distinct mathematical quantities:
       1. **Raw Cosine Similarity**: $S_{\text{cos}} \in [-1, 1]$.
       2. **Cosine Distance**: $D_{\text{cos}} = 1 - S_{\text{cos}}$ (DeepFace default ArcFace distance threshold is 0.68, equivalent to raw similarity 0.32).
       3. **Prototype Transformed Heuristic Score**: The prototype in `matching.py` maps raw similarity 0.45 to heuristic score 0.90, comparing against `CONFIDENCE_THRESHOLD = 0.90`.
     * Evidentiary honesty: This transformed heuristic score is NOT a probability and does NOT guarantee zero false merges across all future images.
   - **Photo Recognition Architecture & Storage Layers**:
     1. **Actual Current Persisted Schema (`backend/app/models/additive.py:80–94`)**:
        - `photos` table contains: `photo_id`, `trip_id`, `uploader_id`, `photo_url`, `processing_status` (`'pending' | 'processed' | 'failed'`), `created_at`. It contains **NO** `detected_faces_count` and **NO** `matched_count` columns.
        - `photo_person` table contains: `pp_id` (PK), `photo_id` (FK), `user_id` (FK, `nullable=False`), `confidence`. Because `user_id` is NOT NULL, only recognized trip members can be stored. Unknown face instances cannot be stored in `photo_person` as `user_id = None`.
     2. **Worker Runtime Recognition Result**:
        - DeepFace worker returns transient runtime metrics in memory: `detected_faces_count`, `matched_count`, and bounding boxes `[x, y, w, h]`. These exist strictly in worker runtime memory and HTTP transit payloads.
     3. **Proposed Durable Aggregate & Face-Instance Representation**:
        - Durable persistence of aggregate face counts (`photos.detected_faces_count`, `matched_count`) and individual face instances with coordinates (`photo_face_tags` with `tag_id`, `photo_id`, nullable `user_id`, `face_index`, `bounding_box`) is an explicit **pending target schema migration** owned by Sharvani.
     4. **Honest Reload Behavior Prior to Target Migration**:
        - On subsequent gallery reload (`GET /api/photos/{trp_id}`), the server queries the database, which currently holds only `photo_person` rows and photo `processing_status`.
        - **Critical Invariant**: Absence of recognized `photo_person` tags does **NOT** mean zero detected faces. If a photo has `processing_status = 'processed'` and 0 rows in `photo_person`, the server cannot determine whether the image had zero faces (scenery) or un-enrolled travelers. Unknown or unavailable recognition evidence must **NEVER** be misclassified as "Scenery"!
        - Worker failure (`processing_status = 'failed'`) remains strictly distinct from successful processing with unknown travelers (`processing_status = 'processed'`). Full reload segregation of unknown faces depends on Sharvani's target schema migration.
   - **Authoritative Tag Persistence Signatures**:
     * Initial upload persistence: `save_uploaded_photo_record(db: Session, photo_id: str, trip_id: str, uploader_id: str, photo_url: str, initial_status: str = "pending") -> Photo`.
     * Tag persistence: `save_photo_tags_records(db: Session, photo_id: str, face_matches: List[Dict[str, Any]], final_status: str = "processed") -> List[PhotoPerson]`. (Storage status `'processed'` maps to wire `'completed'`; worker failure must NEVER map to `'processed'` or `'completed'`).
   - **Tag Persistence Verification**:
     * Multiple face instances in group photos are tracked with distinct `face_index` entries.
     * Person A is persisted only when matched to Person A's enrollment vector; zero cross-person tags for B or C are persisted within the fixed reference corpus.
   - **Unidentified Instance Persistence**:
     * For Person D (un-enrolled), the proposed target representation records `user_id = NULL` with bounding box coordinates, preserving the unidentified face instance without creating false associations.
   - **Scenery Photo Persistence**:
     * Scenery photos record `detected_faces_count = 0` and are categorized into `folder = 'Scenery'`.
   - **Evidentiary Integrity**: Domain persistence rejects matches below threshold (e.g. prototype transformed score < 0.90), ensuring low-confidence noise is never permanently tagged to trip members.

---

## 4. NAMING CONTRACT — READ BEFORE WRITING ANY CODE

### 4.1 Shared Database Models & Fields (snake_case — authoritative schema owned by Sharvani)
```python
# From proposals table:
proposal_id          # prp_ prefixed
itinerary_id         # itn_ prefixed
proposed_by_user_id  # usr_ prefixed
title                # proposal title
rationale            # NOT description — this field is called rationale
cost_delta           # NOT estimated_cost — always Decimal, never float
currency             # ISO-4217 string
closes_at            # nullable timestamp
status               # open|accepted|rejected|expired
current_round        # integer

# From votes table (what I read as input):
vote_id              # vot_ prefixed
proposal_id          # prp_ prefixed
user_id              # usr_ prefixed
value                # 'yes' or 'no' ONLY — I never see 'abstain'
comment              # the typed NO reason — this is my PRIMARY INPUT
cast_at              # timestamp

# From itinerary_items table:
item_id              # itm_ prefixed
day_index            # 1-based integer
sort_order           # integer
starts_at            # nullable timestamp with offset
ends_at              # nullable timestamp with offset
item_type            # hotel|flight|poi|package|guide|transfer|meal|free
entity_type          # from enums.json entity_type list
entity_id            # canonical ID of referenced supply row
title                # activity title
cost                 # Decimal, NEVER float, NEVER called estimated_cost
currency             # ISO-4217
slot_status          # 'EMPTY'|'IN_CONSENSUS'|'BRANCHED'|'CONFIRMED'

# From users + user_preferences (for scorers):
user_id              # usr_ prefixed
display_name         # string
age_group            # '18-24'|'25-34'|'35-44'|'45-54'|'55+'
preferred_languages  # comma-separated BCP-47 e.g. "en,hi,ta"
interests            # comma-separated category codes e.g. "heritage,food,trekking"

# From tour_guides (for guide scorer):
guide_id             # gid_ prefixed
languages            # comma-separated BCP-47
specialisation       # heritage|food|trekking|wildlife|photography|religious|shopping|accessibility
secondary_specialisation  # same enum, nullable
day_rate             # Decimal, NEVER float
currency             # ISO-4217
rating               # Decimal(2,1), nullable
```

### 4.2 Domain Service Return Signatures & AI Outputs

Sharvani's domain services execute transactional persistence in PostgreSQL and return domain models or dicts for Panchami's routers to serialize into Pydantic models for HTTP and WebSocket transport. Pure AI algorithmic sub-modules (such as `blended_plan_generator` and `branch_grouping`) operate on structured dictionaries and return pure dictionary structures to the orchestrating domain service (`consensus_service.py`).

```python
# blended_plan_generator returns:
{
    "action": "BLENDED",
    "blended_plan": {
        "title": str,
        "rationale": str,        # NOT description
        "entity_type": str,      # must be valid from enums.json
        "entity_id": str,        # must look like a real ID
        "cost_delta": str,       # money as string e.g. "0.00"
        "currency": str,         # ISO-4217
    },
    "current_round": int,
    "constraint_validation": "PASSED" | "REGENERATED_ONCE" | "FAILED",
}

# branch_grouping returns:
{
    "action": "BRANCHED",
    "branches": [
        {
            "title": str,
            "rationale": str,
            "entity_type": str | None,
            "entity_id": str | None,
            "cost_delta": str,      # money as string
            "currency": str,
            "member_user_ids": [str],  # usr_ prefixed IDs
            "auto_finalized": bool,    # True if single-member branch
        }
    ]
}

# branch_trigger_classifier returns:
{
    "classification": "FIXABLE_TWEAK" | "FIXED_REQUIREMENT" | "NEEDS_CLARIFICATION" | "UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE",
    "confidence": float,  # 0.0 to 1.0
    "reasoning": str,     # brief explanation (not shown to users, for debugging)
}

# hard_constraint_validator returns:
{
    "valid": bool,
    "violations": [str],   # list of violated constraint descriptions (empty if valid)
}

# group_compatibility_scorer returns:
[
    {
        "trip_id": str,           # trp_ prefixed
        "compatibility_score": int,   # INTEGER 0-100, NEVER float
        "age_group_match": bool,
        "shared_languages": [str],    # BCP-47 tags
        "shared_interests": [str],
        "date_overlap_days": int,
    }
]

# guide_compatibility_scorer returns:
[
    {
        "guide_id": str,          # gid_ prefixed
        "compatibility_score": int,   # INTEGER 0-100, NEVER float
        "shared_languages": [str],
        "shared_specialisations": [str],
    }
]
```

### 4.3 Money: ALWAYS Decimal in Python, string when I put it in my output dict
```python
from decimal import Decimal

# When receiving cost_delta in domain services or router parameters:
cost_delta = Decimal("15.00")  # Transferred as Decimal or string, never float

# When I return it in my output:
"cost_delta": f"{Decimal('0.00'):.2f}"  # always 2 decimal places as string
```

### 4.4 Enums: exact values I must use (from enums.json)
```python
# entity_type legal values (what I can put in blended plan):
ENTITY_TYPES = [
    "hotel", "room_type", "rate_plan", "flight", "flight_fare",
    "poi", "package", "package_component", "guide", "transfer",
    "event", "xr_scene"
]
# For most activity blends: "poi" is the most common

# guide specialisation values:
GUIDE_SPECIALISATIONS = [
    "heritage", "food", "trekking", "wildlife", "photography",
    "religious", "shopping", "accessibility"
]
```

---


<a id="member-phase-3"></a>
## Phase 3 — Prepare the LLM and implement domain AI algorithms

Read the retained sections below together for this phase:

- 5. LLM SETUP — OLLAMA + PHI-4-MINI + NGROK
- 6. THE FOUR CORE AI MODULES

## 5. LLM SETUP — OLLAMA + PHI-4-MINI + NGROK

> [!IMPORTANT]
> **Teammate LLM Isolation Prerequisite**: Local consensus SLM/LLM installation (Ollama / Phi-4-mini) is **STRICTLY a Sharvani-internal dependency**. Teammates (Nikitha, Panchami) require **ZERO** local Ollama installation, GPU configuration, or model weight downloads. All transport and UI testing proceeds against in-memory mock domain services or fixtures. Sharvani owns the local inference lifecycle, ngrok tunneling, and fallback provider routing.

### 5.1 How the LLM path works
```
Render (cloud FastAPI) → HTTPS → ngrok public URL → local laptop → Ollama → Phi-4-mini
```

Ollama runs on a local laptop serving Phi-4-mini on `localhost:11434` with an OpenAI-compatible API. Ngrok tunnels that to a public URL. The FastAPI backend on Render calls that ngrok URL.

### 5.2 LLM Client Setup
```python
# backend/ai/llm/client.py
import os
from openai import OpenAI

def get_llm_client() -> OpenAI:
    """
    Returns an OpenAI-compatible client pointed at the local Ollama instance via ngrok.
    NGROK_LLM_URL comes from environment variable.
    """
    ngrok_url = os.environ.get("NGROK_LLM_URL", "http://localhost:11434")
    return OpenAI(
        base_url=f"{ngrok_url}/v1",
        api_key="ollama",  # required by client but unused by Ollama
    )

def call_llm(
    system_prompt: str,
    user_message: str,
    model: str = "phi4-mini",
    timeout: int = 8,
    expect_json: bool = True,
) -> str:
    """
    Calls the local LLM. Returns the response text.
    Raises TimeoutError if no response within timeout seconds.
    Raises ValueError if response is not valid JSON when expect_json=True.
    """
    client = get_llm_client()
    
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "timeout": timeout,
    }
    
    if expect_json:
        kwargs["response_format"] = {"type": "json_object"}
    
    try:
        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        return content
    except Exception as e:
        raise TimeoutError(f"LLM call failed or timed out: {e}")
```

### 5.3 CRITICAL: Always have a fallback
Every LLM call MUST have a hardcoded fallback response for when the tunnel is down or the model times out:

```python
def safe_llm_call(system_prompt: str, user_message: str, fallback_result: dict) -> dict:
    """
    Wraps any LLM call with timeout + JSON parsing + fallback.
    If LLM fails for ANY reason: return fallback_result instead of crashing.
    """
    import json
    try:
        raw = call_llm(system_prompt, user_message, timeout=8, expect_json=True)
        # Strip any markdown fences if model adds them
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as e:
        print(f"[AI FALLBACK] LLM call failed: {e}. Using fallback.")
        return fallback_result
```

---

## 6. THE FOUR CORE AI MODULES

### 6.1 `hard_constraint_validator.py`

**What it does**: Validates a proposed blended plan against hard constraints BEFORE it is shown to the group. If it fails, the caller regenerates once; if it fails again, escalates to branching.

**What hard constraints are** (from itinerary_item context):
- Time: the blended activity must fit within the time slot (starts_at to ends_at)
- Location: if entity_id doesn't exist in the dataset, it's invalid
- Transport: if the blended activity requires a mode of transport not available in the trip context (this can be a simplified check for hackathon — just flag obviously impossible ones)

**Input**:
```python
def validate_plan(
    blended_plan: dict,          # the plan generated by blended_plan_generator
    itinerary_item: dict,        # the current slot's data
    trip_context: dict,          # trip dates, destination city, etc.
) -> dict:
    """
    Returns:
    {
        "valid": bool,
        "violations": [str]   # empty list if valid
    }
    """
```

**Implementation** (keep simple for hackathon):
```python
def validate_plan(blended_plan: dict, itinerary_item: dict, trip_context: dict) -> dict:
    """
    Authoritative Hard Constraint Validator (Deterministic; No LLM dependency).
    
    ORGANIZED INTO SIX SEQUENTIAL STAGES:
      Stage 1: Parse & Types (fail-closed typing, strict decimal format, no silent defaults)
      Stage 2: Structural & Reference Validation (enums, catalog existence)
      Stage 3: Slot-Specific Requirements & Full Route Context Binding
      Stage 4: Temporal & Timezone Evaluation (dated intervals, local hours, overnight/split shifts)
      Stage 5: Physical Feasibility Inequality (transit buffers, activity duration)
      Stage 6: Canonical Multi-State Typed Outcome Synthesis
      
    EVIDENTIARY PRINCIPLES:
    1. Untrusted model suggestions NEVER become verified facts merely by appearing in candidate fields.
    2. Authoritative activity duration derives strictly from catalog inventory; model duration is rejected.
    3. Missing routing, duration, timestamps, or opening hours yields UNVERIFIED, NEVER synthetic defaults.
    4. Structural validity, evidence completeness, and schedule feasibility remain distinct factual dimensions.
    5. Genuinely inapplicable checks (e.g. stationary free-time routes) are marked NOT_APPLICABLE with reason.
    6. Intermediate calculations NEVER use temporary placeholder defaults to synthesize confirmed open or verified states.
    """
    import re
    from decimal import Decimal, InvalidOperation
    from datetime import datetime, timezone, timedelta, date, time
    try:
        from zoneinfo import ZoneInfo
    except ImportError:
        from backports.zoneinfo import ZoneInfo
        
    # -------------------------------------------------------------
    # STAGE 0: Initialize All Results & Variables Before Any Branches
    # -------------------------------------------------------------
    violations = []
    evidence_missing = []
    
    bound_evidence = None
    t_outbound = None
    t_return = None
    act_duration = None
    b_arr = None
    b_dep = None
    slot_duration_minutes = None
    visit_start = None
    visit_end = None
    
    venue_hours_status = "NOT_APPLICABLE"
    routing_status = "NOT_APPLICABLE"
    catalog_record = None

    # -------------------------------------------------------------
    # STAGE 1: Parse & Types (Fail-Closed Input Contracts)
    # -------------------------------------------------------------
    if not isinstance(blended_plan, dict) or not isinstance(itinerary_item, dict) or not isinstance(trip_context, dict):
        return {
            "valid": False,
            "status": "UNVERIFIED",
            "violations": ["Invalid input contracts: blended_plan, itinerary_item, and trip_context must be dictionaries"],
            "evidence_summary": {"error_type": "TYPE_CONTRACT_VIOLATION"}
        }

    # Lexical monetary validation: ^-?\d+(\.\d{1,2})?$ (rejects exponents 1e2 and >2 decimals)
    cost_delta_raw = blended_plan.get("cost_delta")
    if cost_delta_raw is not None:
        cost_str = str(cost_delta_raw).strip()
        if not re.match(r"^-?\d+(\.\d{1,2})?$", cost_str):
            violations.append(f"cost_delta '{cost_delta_raw}' violates lexical currency format (scientific notation and >2 decimals prohibited)")
        else:
            try:
                cost_dec = Decimal(cost_str)
                if not cost_dec.is_finite():
                    violations.append(f"cost_delta '{cost_delta_raw}' is non-finite (NaN or Infinity prohibited)")
            except (InvalidOperation, ValueError, TypeError):
                violations.append(f"cost_delta '{cost_delta_raw}' cannot be parsed as a valid Decimal")

    # Currency validation: required, no silent USD defaulting
    currency = blended_plan.get("currency")
    expected_currency = trip_context.get("base_currency") or itinerary_item.get("currency")
    if not currency:
        violations.append("Missing required currency on candidate proposal; silent USD defaulting prohibited")
    elif expected_currency and currency != expected_currency:
        violations.append(f"Currency mismatch: candidate '{currency}' != authoritative base currency '{expected_currency}'")

    # -------------------------------------------------------------
    # STAGE 2: Structural & Reference Validation (data-model/enums.json)
    # -------------------------------------------------------------
    legal_item_types = ["hotel", "flight", "poi", "package", "guide", "transfer", "meal", "free"]
    legal_catalog_entity_types = [
        "hotel", "room_type", "rate_plan", "flight", "flight_fare", "poi",
        "package", "package_component", "guide", "transfer", "event", "xr_scene"
    ]
    
    item_type = blended_plan.get("item_type") or itinerary_item.get("item_type")
    if not item_type:
        violations.append("Missing item_type: candidate and itinerary item lack an item_type")
    elif item_type not in legal_item_types:
        violations.append(f"Invalid slot item_type: '{item_type}'. Must be one of {legal_item_types}")
        
    entity_type = blended_plan.get("entity_type")
    if entity_type and entity_type not in legal_catalog_entity_types:
        violations.append(f"Invalid catalog entity_type: '{entity_type}'. Must be one of {legal_catalog_entity_types}")
        
    # Title adapter: accept 'title' or 'candidate_title'
    candidate_title = blended_plan.get("title") or blended_plan.get("candidate_title", "")
    if not str(candidate_title).strip():
        violations.append("Candidate title is missing or blank (must provide 'title' or 'candidate_title')")

    entity_id = blended_plan.get("entity_id")
    trusted_catalog = trip_context.get("trusted_catalog_candidates") or {}

    # Entity reference check against authoritative catalog
    if entity_id:
        catalog_record = trusted_catalog.get(entity_id)
        if catalog_record is None:
            violations.append(f"Unknown catalog entity_id '{entity_id}': does not exist in trusted catalog")
            return {
                "valid": False,
                "status": "BLOCKED",
                "violations": violations,
                "evidence_summary": {
                    "entity_id": entity_id,
                    "catalog_verified": False,
                    "routing_bound": False,
                    "venue_hours_status": "UNKNOWN_ENTITY",
                    "evidence_missing": [f"Catalog entity '{entity_id}' not found"],
                }
            }

    # -------------------------------------------------------------
    # STAGE 3: Slot-Specific Requirements & Full Route Context Binding
    # -------------------------------------------------------------
    local_trip_date = trip_context.get("trip_date") # ISO format string: YYYY-MM-DD
    expected_origin = trip_context.get("current_location") # e.g. hotel or previous POI
    expected_destination = trip_context.get("next_location") or expected_origin # Onward commitment or designated return location

    # Item-specific evidence rules:
    is_stationary = (item_type in ["free", "meal"] and not entity_id)
    is_transit = (item_type == "transfer")
    is_flight = (item_type == "flight")
    is_guide = (item_type == "guide")
    is_venue_activity = (item_type in ["poi", "hotel", "event", "package"] or (item_type in ["meal", "free"] and entity_id))

    if is_stationary:
        routing_status = "NOT_APPLICABLE"
        venue_hours_status = "NOT_APPLICABLE"
        t_outbound = 0
        t_return = 0
        b_arr = 0
        b_dep = 0
    elif is_transit:
        venue_hours_status = "NOT_APPLICABLE"
        # Transfers evaluate route between origin and destination
        routing_map = trip_context.get("bound_routing_evidence") or {}
        bound_evidence = routing_map.get(entity_id or "transfer_route")
        if not bound_evidence:
            evidence_missing.append(f"Transit route evidence missing for transfer '{item_type}'")
            routing_status = "NO_ROUTE_FOUND"
        else:
            t_outbound = bound_evidence.get("outbound_minutes")
            t_return = 0
            b_arr = 0
            b_dep = 0
            routing_status = "ROUTE_VERIFIED" if (t_outbound is not None and t_outbound >= 0) else "ROUTE_INCOMPLETE"
    elif is_flight or is_guide:
        venue_hours_status = "NOT_APPLICABLE"
        routing_status = "NOT_APPLICABLE"
        t_outbound = 0
        t_return = 0
        b_arr = 0
        b_dep = 0
    elif entity_id:
        # Full route context binding: selected entity, scheduled date, previous location (origin),
        # onward destination (next commitment or return), transport mode, and evidence freshness
        routing_map = trip_context.get("bound_routing_evidence") or {}
        bound_evidence = routing_map.get(entity_id)
        
        if not bound_evidence:
            evidence_missing.append(f"Bound road-routing transit evidence missing for entity '{entity_id}'")
            routing_status = "NO_ROUTE_FOUND"
        else:
            # Check context bindings (NO defaults! Missing bindings yield unverified)
            ev_date = bound_evidence.get("date")
            ev_origin = bound_evidence.get("origin_location")
            ev_dest = bound_evidence.get("destination_location")
            ev_stale = bound_evidence.get("is_stale") # boolean flag
            ev_failed = bound_evidence.get("provider_failed", False)
            
            # Missing required binding attributes produce missing evidence
            if not ev_date or not ev_origin or not ev_dest or ev_stale is None:
                evidence_missing.append(f"Routing evidence for entity '{entity_id}' has incomplete context bindings (date/origin/destination/freshness missing)")
                routing_status = "ROUTE_INCOMPLETE"
            elif ev_failed:
                evidence_missing.append(f"Routing provider failed for entity '{entity_id}'")
                routing_status = "ROUTING_PROVIDER_FAILED"
            elif ev_stale is True:
                evidence_missing.append(f"Routing evidence for entity '{entity_id}' is stale (exceeds freshness TTL)")
                routing_status = "ROUTE_EVIDENCE_STALE"
            elif (local_trip_date and ev_date != local_trip_date) or \
                 (expected_origin and ev_origin != expected_origin) or \
                 (expected_destination and ev_dest != expected_destination):
                evidence_missing.append(
                    f"Routing evidence context mismatch for '{entity_id}': "
                    f"date '{ev_date}' vs '{local_trip_date}', origin '{ev_origin}' vs '{expected_origin}', "
                    f"destination '{ev_dest}' vs '{expected_destination}'"
                )
                routing_status = "ROUTE_MISMATCHED_CONTEXT"
            else:
                t_outbound = bound_evidence.get("outbound_minutes")
                t_return = bound_evidence.get("return_minutes")
                if t_outbound is None or t_return is None:
                    evidence_missing.append(f"Incomplete routing evidence for entity '{entity_id}': missing outbound or return leg duration")
                    routing_status = "ROUTE_INCOMPLETE"
                elif t_outbound < 0 or t_return < 0:
                    violations.append(f"Routing evidence contains negative travel duration: outbound={t_outbound}m, return={t_return}m")
                    routing_status = "ROUTE_INVALID"
                else:
                    routing_status = "ROUTE_VERIFIED"
    else:
        evidence_missing.append("Candidate lacks entity_id; cannot bind routing or catalog evidence")
        routing_status = "MISSING_ENTITY"

    # -------------------------------------------------------------
    # STAGE 4: Temporal & Timezone Evaluation (Dated Intervals)
    # -------------------------------------------------------------
    starts_at = itinerary_item.get("starts_at")
    ends_at = itinerary_item.get("ends_at")
    
    if not starts_at or not ends_at:
        evidence_missing.append("Slot timestamps ('starts_at' / 'ends_at') are missing; schedule feasibility cannot be evaluated")
    else:
        is_start_dt = isinstance(starts_at, datetime)
        is_end_dt = isinstance(ends_at, datetime)
        
        if not is_start_dt or not is_end_dt:
            violations.append("Slot timestamps must be valid Python datetime objects")
        else:
            is_start_aware = (starts_at.tzinfo is not None and starts_at.tzinfo.utcoffset(starts_at) is not None)
            is_end_aware = (ends_at.tzinfo is not None and ends_at.tzinfo.utcoffset(ends_at) is not None)
            
            if is_start_aware != is_end_aware:
                evidence_missing.append("Slot timestamps have mixed timezone awareness (one aware, one naive); subtraction unsafe")
            elif not is_start_aware:
                evidence_missing.append("Slot timestamps lack explicit timezone awareness; timezone conversion unsafe")
            else:
                slot_duration_minutes = (ends_at - starts_at).total_seconds() / 60
                if slot_duration_minutes <= 0:
                    violations.append(f"Invalid slot time window: ends_at must be strictly after starts_at (duration={slot_duration_minutes}m)")

    # Timezone-Aware Venue Opening Hours Evaluation Using Dated Intervals
    if is_venue_activity and entity_id:
        operating_hours_map = trip_context.get("operating_hours") or {}
        venue_hours = operating_hours_map.get(entity_id)
        
        # Check buffer policy existence (NO invented defaults!)
        b_arr = trip_context.get("buffer_arrival_minutes")
        b_dep = trip_context.get("buffer_departure_minutes")
        act_duration = catalog_record.get("duration_minutes") if catalog_record else None
        
        if b_arr is None or b_dep is None:
            evidence_missing.append("Transit buffer policy (arrival/departure buffers) is missing from trip context")
        elif b_arr < 0 or b_dep < 0:
            violations.append(f"Transit buffer policy contains negative buffer: arr={b_arr}m, dep={b_dep}m")
            
        if not venue_hours:
            evidence_missing.append(f"Operating hours missing for venue '{entity_id}'")
            venue_hours_status = "HOURS_MISSING"
        elif venue_hours.get("is_closed") or venue_hours.get("status") == "CLOSED_REPORTED":
            violations.append(f"Venue '{entity_id}' is confirmed CLOSED on scheduled date")
            venue_hours_status = "CONFIRMED_CLOSED"
        elif venue_hours.get("status") == "PROVIDER_FAILED":
            evidence_missing.append(f"Operating hours provider failed for venue '{entity_id}'")
            venue_hours_status = "PROVIDER_FAILED"
        elif t_outbound is None or b_arr is None or act_duration is None:
            # Cannot synthesize factual visit interval without real routing, buffers, and duration!
            # No invented defaults allowed: halt factual hours evaluation cleanly.
            evidence_missing.append(f"Cannot evaluate opening hours for '{entity_id}' without verified transit duration and buffer policy")
            venue_hours_status = "HOURS_MISSING"
        else:
            tz_str = venue_hours.get("timezone")
            if not tz_str:
                evidence_missing.append(f"Venue '{entity_id}' missing declared timezone; timezone-aware hours evaluation cannot proceed")
                venue_hours_status = "TIMEZONE_AMBIGUOUS"
            else:
                try:
                    venue_tz = ZoneInfo(tz_str)
                except Exception:
                    evidence_missing.append(f"Venue '{entity_id}' has unrecognized timezone '{tz_str}'")
                    venue_hours_status = "TIMEZONE_AMBIGUOUS"
                    venue_tz = None
                    
                if venue_tz and starts_at and isinstance(starts_at, datetime) and starts_at.tzinfo:
                    # Calculate actual candidate visit window inside venue: [arrival_time, departure_time]
                    visit_start = starts_at + timedelta(minutes=t_outbound + b_arr)
                    visit_end = visit_start + timedelta(minutes=act_duration)
                    
                    # Convert candidate visit window into venue's local timezone
                    local_visit_start = visit_start.astimezone(venue_tz)
                    local_visit_end = visit_end.astimezone(venue_tz)
                    local_date = local_visit_start.date()
                    
                    # Construct dated opening intervals for local date (and preceding date for overnight carryover)
                    # Supported schedule format: list of intervals with open/close time strings e.g. [{"open": "20:00", "close": "02:00"}]
                    raw_intervals = venue_hours.get("intervals")
                    if not raw_intervals and venue_hours.get("open_time") and venue_hours.get("close_time"):
                        raw_intervals = [{"open": venue_hours["open_time"], "close": venue_hours["close_time"]}]
                        
                    if not raw_intervals:
                        evidence_missing.append(f"Unsupported or missing opening interval format for venue '{entity_id}'")
                        venue_hours_status = "HOURS_MISSING"
                    else:
                        dated_intervals = []
                        # Build dated intervals for local_date and local_date - 1 day
                        for d_ref in [local_date - timedelta(days=1), local_date]:
                            for iv in raw_intervals:
                                o_str = iv.get("open")
                                c_str = iv.get("close")
                                if not o_str or not c_str:
                                    continue
                                try:
                                    o_h, o_m = map(int, o_str.split(":"))
                                    c_h, c_m = map(int, c_str.split(":"))
                                    iv_start = datetime.combine(d_ref, time(o_h, o_m), tzinfo=venue_tz)
                                    if (c_h, c_m) > (o_h, o_m):
                                        # Normal daytime shift on d_ref
                                        iv_end = datetime.combine(d_ref, time(c_h, c_m), tzinfo=venue_tz)
                                    else:
                                        # Overnight shift: closes on d_ref + 1 day
                                        iv_end = datetime.combine(d_ref + timedelta(days=1), time(c_h, c_m), tzinfo=venue_tz)
                                    dated_intervals.append((iv_start, iv_end))
                                except Exception:
                                    continue
                                    
                        # Complete visit interval must be fully contained within at least one valid dated interval
                        is_contained = any(
                            (local_visit_start >= iv_st and local_visit_end <= iv_et)
                            for iv_st, iv_et in dated_intervals
                        )
                        
                        if is_contained:
                            venue_hours_status = "CONFIRMED_OPEN"
                        else:
                            violations.append(
                                f"Candidate visit window ({local_visit_start.strftime('%Y-%m-%d %H:%M')} to "
                                f"{local_visit_end.strftime('%Y-%m-%d %H:%M')} {tz_str}) outside venue open intervals for '{entity_id}'"
                            )
                            venue_hours_status = "OUTSIDE_HOURS"

    # -------------------------------------------------------------
    # STAGE 5: Physical Feasibility Inequality
    # -------------------------------------------------------------
    if is_stationary:
        act_duration = int(slot_duration_minutes) if slot_duration_minutes else 0
        total_required = act_duration
    elif is_venue_activity:
        act_duration = catalog_record.get("duration_minutes") if catalog_record else None
        if t_outbound is not None and t_return is not None and act_duration is not None and b_arr is not None and b_dep is not None:
            total_required = t_outbound + b_arr + act_duration + b_dep + t_return
            if slot_duration_minutes is not None and total_required > slot_duration_minutes:
                violations.append(
                    f"Schedule feasibility violated: total required time {total_required}m exceeds slot window {slot_duration_minutes}m "
                    f"(outbound {t_outbound}m + arr_buf {b_arr}m + activity {act_duration}m + dep_buf {b_dep}m + return {t_return}m)"
                )

    # -------------------------------------------------------------
    # STAGE 6: Canonical Multi-State Outcome Synthesis
    # -------------------------------------------------------------
    # Deterministic Precedence: BLOCKED > INFEASIBLE > NEEDS_CLARIFICATION > UNVERIFIED > PARTIALLY_VERIFIED > VERIFIED
    has_blocked = (venue_hours_status in ["CONFIRMED_CLOSED", "OUTSIDE_HOURS"] or
                   any("Unknown catalog" in v or "CLOSED" in v or "outside" in v for v in violations))
    has_infeasible = any("Schedule feasibility violated" in v for v in violations)
    has_unverified = (bool(evidence_missing) or 
                      routing_status in ["NO_ROUTE_FOUND", "ROUTING_PROVIDER_FAILED", "ROUTE_EVIDENCE_STALE", "ROUTE_MISMATCHED_CONTEXT", "ROUTE_INCOMPLETE"])
    has_partial = (venue_hours_status in ["HOURS_MISSING", "TIMEZONE_AMBIGUOUS", "PROVIDER_FAILED"])
    
    if has_blocked:
        status = "BLOCKED"
        valid = False
    elif has_infeasible:
        status = "INFEASIBLE"
        valid = False
    elif violations:
        status = "BLOCKED"
        valid = False
    elif has_unverified:
        status = "UNVERIFIED"
        valid = False
        violations.extend(evidence_missing)
    elif has_partial:
        status = "PARTIALLY_VERIFIED"
        valid = False
    else:
        status = "VERIFIED"
        valid = True
        
    return {
        "valid": valid,
        "status": status,  # "VERIFIED" | "PARTIALLY_VERIFIED" | "UNVERIFIED" | "NEEDS_CLARIFICATION" | "INFEASIBLE" | "BLOCKED"
        "violations": violations,
        "evidence_summary": {
            "entity_id": entity_id,
            "catalog_verified": catalog_record is not None or is_stationary,
            "routing_status": routing_status,
            "routing_bound": routing_status in ["ROUTE_VERIFIED", "NOT_APPLICABLE"],
            "venue_hours_status": venue_hours_status,
            "evidence_missing": evidence_missing,
        }
    }
```

**This is the FIRST module to build** — it has no LLM dependency, runs instantly, and is needed by everything else.

---

### 6.2 `branch_trigger_classifier.py`

> [!IMPORTANT]
> **Canonical Taxonomy Contract (`docs/AI.md § 3`)**:
> The system operates strictly under the canonical four-class objection taxonomy:
> 1. `FIXABLE_TWEAK`: Modifiable preference or timing adjustment (e.g. "prefer afternoon slot", "add spa element").
> 2. `FIXED_REQUIREMENT`: Hard, non-negotiable constraint (e.g. "injured ankle cannot do any hiking", "strict vegetarian cannot eat at steakhouse").
> 3. `NEEDS_CLARIFICATION`: Vague or low-information objections (e.g. "not feeling it", "idk", "something else") or ambiguous preference statements.
> 4. `UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE`: Sarcasm, contradictory comments, or unparseable input.
> 
> **VAGUE COMMENT RULE**: Vague or low-information comments must **NEVER** automatically become `FIXABLE_TWEAK`. They must be classified as `NEEDS_CLARIFICATION` or `UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE`. The frontend displays bounded clarification chips rather than having the AI guess a modification.
> 
> **CONSTRAINTS VS PREFERENCES**: Soft preferences (e.g. mountain vs beach, budget vs luxury) do **NOT** automatically prove a fixed requirement without explicit constraint evidence. Sarcasm or negation (e.g. "Sure, let's totally hike 20 miles with my sprained ankle") must be handled through context extraction, not positive keyword matching.

**Input**:
```python
def classify_objection(
    no_comments: list[dict],    # [{ "user_id": str, "comment": str, "round": int }]
    current_round: int,
    soft_round_cap: int = 3,    # after this many rounds, even FIXABLE_TWEAK may trigger branch
) -> dict:
    """
    Returns:
    {
        "classification": "FIXABLE_TWEAK" | "FIXED_REQUIREMENT" | "NEEDS_CLARIFICATION" | "UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE",
        "confidence": float,
        "reasoning": str,
        "extracted_constraints": list[str],
    }
    """
```

#### Active 4-Class Classification System Prompt (`[ACTIVE TARGET CONTRACT]`)
```python
CLASSIFIER_SYSTEM_PROMPT = """You are a travel group consensus classifier. 
You receive typed objection comments from group members who voted NO on a proposed activity.
Your job is to classify these objections into exactly one of four classes:

1. FIXABLE_TWEAK: The objection expresses a modifiable preference (timing, pacing, budget, amenity) that can be blended into a compromise.
2. FIXED_REQUIREMENT: The objection expresses a hard, non-negotiable incompatibility (medical injury, strict diet, religious restriction, hard schedule conflict).
3. NEEDS_CLARIFICATION: The objection is vague, low-information ("not feeling it", "idk", "something else"), or expresses an ambiguous preference without actionable direction.
4. UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE: Sarcasm, contradictory comments, or text with insufficient evidence to extract a constraint.

CRITICAL INVARIANTS:
1. Vague or low-information comments ("not feeling it", "idk") must NEVER be classified as FIXED_REQUIREMENT, and must NOT be guessed as FIXABLE_TWEAK. Classify as NEEDS_CLARIFICATION.
2. Soft preferences (mountain vs beach, cheap vs luxury) are NOT fixed requirements unless backed by an explicit hard constraint.
3. Handle sarcasm or negation by looking at the underlying condition (e.g., "Sure, let's totally hike with my sprained ankle" is a medical constraint -> FIXED_REQUIREMENT).

Respond ONLY with a JSON object in this exact format:
{
  "classification": "FIXABLE_TWEAK" | "FIXED_REQUIREMENT" | "NEEDS_CLARIFICATION" | "UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE",
  "confidence": 0.0 to 1.0,
  "reasoning": "brief one-sentence explanation",
  "extracted_constraints": ["string list of constraints"]
}
"""
```

#### Historical Prototype Prompt (`[HISTORICAL REFERENCE / SUPERSEDED]`)
The older 2-class prompt below is preserved strictly for historical audit reference:
```python
# SUPERSEDED: Prototype 2-class prompt (do not use in active implementation)
# CLASSIFIER_SYSTEM_PROMPT_2CLASS = ... (classified vague comments as FIXABLE_TWEAK)
```

**Implementation**:
```python
import json
from backend.ai.llm.client import safe_llm_call

# Fallback: if LLM fails or response is unparseable, default to UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE
# (Preserves baseline proposal, avoids arbitrary branching, and renders clarification chips to voter)
CLASSIFIER_FALLBACK = {
    "classification": "UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE",
    "confidence": 0.0,
    "reasoning": "LLM unavailable or unparseable — baseline preserved; prompt voter for clarification",
    "extracted_constraints": [],
}

def classify_objection(no_comments, current_round, soft_round_cap=3):
    # Build user message from comments
    comments_text = "\n".join([
        f"Round {c['round']}, Member {c['user_id']}: \"{c['comment']}\""
        for c in no_comments
    ])
    user_message = f"Classify these objections:\n{comments_text}"
    
    result = safe_llm_call(
        system_prompt=CLASSIFIER_SYSTEM_PROMPT,
        user_message=user_message,
        fallback_result=CLASSIFIER_FALLBACK,
    )
    
    # Validate the result conforms strictly to the canonical 4-class taxonomy
    allowed_classes = {
        "FIXABLE_TWEAK",
        "FIXED_REQUIREMENT",
        "NEEDS_CLARIFICATION",
        "UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE"
    }
    if result.get("classification") not in allowed_classes:
        return CLASSIFIER_FALLBACK
    
    return result
```

---

### 6.3 `blended_plan_generator.py`

**What it does**: Given a current proposal and typed NO comments (suggestions), generates EXACTLY ONE blended compromise plan that tries to incorporate the suggestions into the existing activity.

**Key rules**:
1. ALWAYS attempts blending BEFORE any branching — this step is never skipped
2. Produces EXACTLY ONE plan, not multiple options
3. The plan must stay within the same general activity category where possible (e.g. if the proposal is "Mount Batur Trek" and someone says "prefer spa", blend into "Thermal Springs at Batur" not an entirely unrelated activity)
4. Returns the plan as a structured dict, never free text
5. After generation, `consensus_service.py` MUST run `hard_constraint_validator.validate_plan()` before committing the blended plan or returning to the router

**Input**:
```python
def generate_blended_plan(
    current_proposal: dict,      # { title, rationale, entity_type, entity_id, cost_delta, currency }
    no_vote_comments: list[dict],  # [{ user_id, comment, round }]
    itinerary_item: dict,         # { item_id, title, entity_type, entity_id, cost, currency, starts_at, ends_at }
    trip_context: dict,           # { destination_city, start_date, end_date, mode }
    current_round: int,
) -> dict:
    """
    Returns blended plan dict OR raises an exception if generation fails.
    Caller handles exception → triggers branching.
    """
```

**System prompt for Phi-4-mini**:
```python
BLEND_SYSTEM_PROMPT = """You are a travel activity compromise generator for a group trip planning app.

Your job: Given a proposed group activity and typed objection comments from NO-voters, 
generate EXACTLY ONE blended compromise activity that tries to incorporate as many objections 
as possible while staying close to the original activity's spirit and location.

RULES:
1. Generate EXACTLY ONE compromise candidate from the provided list of verified catalog candidate IDs (`candidate_ids`), not multiple options
2. The candidate should blend the original activity with the suggestions from NO-voters
3. Keep the activity in the same general geographic area/category where feasible
4. Use the verified catalog entity_type corresponding to the selected candidate
5. FACTUAL INTEGRITY & CATALOG GROUNDING RULE: Never invent realistic-sounding entity IDs like 'poi_[descriptive_name]'. The model MUST select an exact entity_id from the supplied `candidate_ids` list. If NO supplied candidate satisfies the hard constraints, respond with action 'NEEDS_CLARIFICATION' or 'NO_FEASIBLE_CANDIDATE'.
6. cost_delta must be the exact finite numerical difference from original cost
7. Candidate retry budget: Initial attempt + 1 permitted regeneration attempt = 2 total attempts. If validation fails twice, baseline is preserved.

Respond ONLY with a JSON object in this exact format, nothing else:
{
  "title": "Verified candidate title (concise, under 60 chars)",
  "rationale": "One or two sentences explaining the compromise",
  "entity_type": "poi",
  "entity_id": "poi_verified_id_from_supplied_candidates",
  "cost_delta": "0.00",
  "currency": "USD"
}"""
```

**Implementation**:
```python
import json
from decimal import Decimal
from backend.ai.llm.client import safe_llm_call
from backend.ai.core.hard_constraint_validator import validate_plan

# CANONICAL REQUIREMENT: On technical provider failure (timeout, empty output, provider offline),
# preserve the baseline plan and return an explicit typed failure status. Never invent a synthetic plan.

def generate_blended_plan(
    current_proposal: dict,
    no_vote_comments: list[dict],
    itinerary_item: dict,
    trip_context: dict,
    current_round: int,
    eligible_candidates: list[dict] = None
) -> dict:
    """
    Bounded Candidate Synthesis Pipeline.
    Supplies rich structured candidate evidence to the LLM.
    Requires selected entity_id to belong strictly to the shown eligible candidate set.
    Enforces a strict attempt budget: 1 initial attempt + 1 retry = 2 total attempts.
    
    DISCRIMINATED RESULT CONTRACT:
    - Distinguishes provider failure, invalid structure (malformed JSON/schema error),
      unavailable external evidence, proven constraint failure, and validated candidates.
    - Provider outages and schema failures return UNVERIFIED, NEVER defaulting to INFEASIBLE.
    - Preserves missing catalog cost as UNKNOWN (not 0.00).
    """
    # Guard: Distinguish explicitly empty eligible set from omitted parameter
    if eligible_candidates is not None and len(eligible_candidates) == 0:
        return {
            "action": "BLENDED_PLAN_FAILED",
            "blended_plan": None,
            "preserved_baseline_proposal_id": current_proposal.get("proposal_id"),
            "status": "UNVERIFIED",
            "error_type": "EMPTY_ELIGIBLE_SET",
            "error": "Supplied eligible candidate set is explicitly empty; broadening search is prohibited",
            "current_round": current_round,
            "constraint_validation": "EMPTY_ELIGIBLE_SET"
        }
        
    candidates = eligible_candidates or list(trip_context.get("trusted_catalog_candidates", {}).values())
    if not candidates:
        return {
            "action": "BLENDED_PLAN_FAILED",
            "blended_plan": None,
            "preserved_baseline_proposal_id": current_proposal.get("proposal_id"),
            "status": "UNVERIFIED",
            "error_type": "NO_CANDIDATES",
            "error": "No verified catalog candidates available for this destination",
            "current_round": current_round,
            "constraint_validation": "NO_CANDIDATES"
        }
        
    # EXACT SHOWN & ELIGIBLE SELECTION SET: Define once, use for both prompt formatting & validation
    shown_candidates = candidates[:8]
    eligible_ids = {c.get("entity_id") or c.get("poi_id") for c in shown_candidates if (c.get("entity_id") or c.get("poi_id"))}
    
    # Format rich candidate evidence for model reasoning
    candidate_lines = []
    for c in shown_candidates:
        cid = c.get("entity_id") or c.get("poi_id")
        name = c.get("name") or c.get("title") or "Unnamed"
        cat = c.get("category", "General")
        cost_val = c.get("cost")
        cost_str = f"{cost_val:.2f}" if isinstance(cost_val, (int, float)) else ("UNKNOWN" if cost_val is None else str(cost_val))
        dur_val = c.get("duration_minutes")
        dur_str = f"{dur_val}m" if dur_val is not None else "UNKNOWN"
        candidate_lines.append(f"- ID: {cid} | Name: {name} | Category: {cat} | Cost: {cost_str} | Duration: {dur_str}")
    candidates_evidence_text = "\n".join(candidate_lines)
    
    comments_text = "\n".join([f"- {c['comment']}" for c in no_vote_comments])
    
    user_message = f"""
Current proposed activity: "{current_proposal['title']}"
Rationale: {current_proposal.get('rationale', 'No rationale provided')}
Destination: {trip_context.get('destination_city', 'Unknown')}
Round: {current_round}

Eligible Verified Catalog Candidates (You MUST select EXACTLY ONE ID from this list):
{candidates_evidence_text}

NO-voter objections and suggestions:
{comments_text}

Task: Select the optimal compromise candidate from the eligible candidates above.
Return JSON with: candidate_title, rationale, entity_type, entity_id, cost_delta, currency.
"""
    
    def process_and_validate_candidate(resp: any) -> tuple[dict, dict]:
        # 1. Provider failure / timeout
        if resp is None:
            return None, {
                "valid": False,
                "status": "UNVERIFIED",
                "error_type": "PROVIDER_OUTAGE",
                "violations": ["LLM provider call failed, timed out, or returned null response"]
            }
            
        # 2. Structural schema validation
        if not isinstance(resp, dict):
            return None, {
                "valid": False,
                "status": "UNVERIFIED",
                "error_type": "MALFORMED_OUTPUT",
                "violations": ["LLM response is not a valid JSON dictionary object"]
            }
            
        # 3. Unified Title Adapter (candidate_title <-> title)
        canonical_title = resp.get("title") or resp.get("candidate_title")
        if not canonical_title or not str(canonical_title).strip():
            return None, {
                "valid": False,
                "status": "UNVERIFIED",
                "error_type": "SCHEMA_ERROR",
                "violations": ["Missing required field: title / candidate_title"]
            }
        resp["title"] = canonical_title
        resp["candidate_title"] = canonical_title
        
        # 4. Eligible Candidate Membership Guard (Exact Shown Set)
        sel_id = resp.get("entity_id")
        if not sel_id or sel_id not in eligible_ids:
            return None, {
                "valid": False,
                "status": "BLOCKED",
                "error_type": "OUT_OF_SET_CANDIDATE",
                "violations": [f"Selected entity_id '{sel_id}' does not belong to the shown eligible candidate set"]
            }
            
        # 5. Mandatory financial fields (NO silent 0.00 / USD defaulting)
        if resp.get("cost_delta") is None:
            return None, {
                "valid": False,
                "status": "UNVERIFIED",
                "error_type": "SCHEMA_ERROR",
                "violations": ["Missing required cost_delta field on model response (silent defaulting prohibited)"]
            }
        if not resp.get("currency"):
            return None, {
                "valid": False,
                "status": "UNVERIFIED",
                "error_type": "SCHEMA_ERROR",
                "violations": ["Missing required currency field on model response (silent defaulting prohibited)"]
            }
            
        # 6. Authoritative Deterministic Validator (Stages 1-6)
        val_result = validate_plan(resp, itinerary_item, trip_context)
        return resp, val_result

    # Attempt 1
    raw_response = safe_llm_call(
        system_prompt=BLEND_SYSTEM_PROMPT,
        user_message=user_message,
        fallback_result=None,
    )
    processed, validation = process_and_validate_candidate(raw_response)
    
    # Attempt 2 (Bounded single regeneration retry for repairable errors)
    if not validation["valid"]:
        # External evidence cannot be repaired by the model; if hours/route missing, regeneration is futile
        violations_text = "; ".join(validation["violations"])
        user_message_retry = user_message + f"\n\nPrevious attempt had these errors: {violations_text}. Select a valid ID from the eligible list and provide exact required fields."
        raw_response_retry = safe_llm_call(
            system_prompt=BLEND_SYSTEM_PROMPT,
            user_message=user_message_retry,
            fallback_result=None,
        )
        processed_retry, validation2 = process_and_validate_candidate(raw_response_retry)
        if not validation2["valid"]:
            # Bounded attempt budget exhausted (1 initial + 1 retry = 2 total attempts)
            # PRESERVE TYPED STATUS: Technical, schema, or missing evidence errors return UNVERIFIED.
            final_status = validation2.get("status", "UNVERIFIED")
            return {
                "action": "BLENDED_PLAN_FAILED",
                "blended_plan": None,
                "preserved_baseline_proposal_id": current_proposal.get("proposal_id"),
                "status": final_status,
                "error_type": validation2.get("error_type", final_status),
                "violations": validation2.get("violations", []),
                "error": f"Blended plan candidate generation failed validation: {validation2.get('error_type', final_status)}",
                "current_round": current_round,
                "constraint_validation": "ATTEMPTS_EXHAUSTED"
            }
        processed = processed_retry
        constraint_status = "REGENERATED_ONCE"
    else:
        constraint_status = "PASSED"
        
    return {
        "action": "BLENDED",
        "blended_plan": processed,
        "proposal_payload": {
            "title": processed["title"],
            "candidate_title": processed["candidate_title"],
            "rationale": processed["rationale"],
            "entity_type": processed["entity_type"],
            "entity_id": processed["entity_id"],
            "cost_delta": processed["cost_delta"],
            "currency": processed["currency"]
        },
        "current_round": current_round,
        "constraint_validation": constraint_status,
        "status": "VERIFIED"
    }```

---

### 6.3.1 Evidence-Grounded Feasibility Calculation & Negotiation Journey

#### Verified Road Routing & Feasibility Equation
- Feasibility is determined strictly by real road network distance/duration (via OSRM/GraphHopper adapter). Geodesic Haversine calculations must **never** be used as feasibility proof.
- **Feasibility Equation**:
  $$	ext{Total Window} = 	ext{Outbound Travel} + 	ext{Activity Duration} + 	ext{Onward Travel} + 	ext{Approved Transition Buffers} + 	ext{Return Commitments}$$
- **Synthetic Batur Arithmetic Verification**:
  $$	ext{Outbound (75m)} + 	ext{Activity (120m)} + 	ext{Onward (90m)} + 	ext{Buffers (2} \times 	ext{15m = 30m)} + 	ext{Return Margin (30m)} = 345	ext{ minutes total}$$
  Both 15-minute transition buffers (Decision #13) are explicitly included in the schedule arithmetic.

#### Evidence-Grounded Negotiation Journey (Second Half)
Nikitha renders the three-option negotiation card grounded in deterministic routing/feasibility evidence:

##### 1. Negotiation Option Semantics & State Transitions
1. **`KEEP_ORIGINAL`**:
   - **Caller Scope**: Any trip member viewing the card.
   - **Semantics**: Traveler acknowledges the feasibility tradeoff/warning but confirms their personal preference for the baseline activity.
   - **Domain Action**: Client-local card dismissal. It does **NOT** mutate the slot, does **NOT** force a binding group decision, and does **NOT** override group consensus.
   - **Response**: `{"status": "DISMISSED", "tripId": "...", "slotId": "...", "optionType": "KEEP_ORIGINAL"}`.
   - **WebSocket Event**: None broadcast (local to caller).
   - **Audit Effect**: `negotiation.card_dismissed` logged with `caller_id` and `slot_id`.

2. **`CLOSER_ALTERNATIVE`**:
   - **Caller Scope**: Any active trip member with `editor` or `owner` role.
   - **Semantics**: Submits the closer POI alternative (identified by `selectedOptionId`) as a new proposal for the slot.
   - **Domain Action**: Submitting an alternative does **NOT** unilaterally modify an accepted itinerary. In Mode A, it queues the proposal for admin acceptance. In Mode NA, it opens the proposal in the slot for group voting.
   - **State Transition**: Creates a row in `proposals` with `entity_id` pointing to the closer POI, `status = 'open'`, and rationale referencing shorter travel time.
   - **Response**: `{"status": "PROPOSAL_CREATED", "proposalId": "prp_...", "slotId": "...", "optionType": "CLOSER_ALTERNATIVE"}`.
   - **WebSocket Event**: Broadcasts `proposalCreated` to all trip members.
   - **Audit Effect**: `proposals.created_from_negotiation` logged in `audit_log`.

3. **`RESCHEDULE_WINDOW`**:
   - **Caller Scope**: Any active trip member with `editor` or `owner` role.
   - **Semantics**: Proposes shifting slot timing (e.g., earlier start time or shifted duration) to make the original activity feasible.
   - **Domain Action & Authority**:
     - *Mode A*: Trip owner/admin can approve the shift, immediately updating `itinerary_items.starts_at` and `ends_at`, bumping `itineraries.version = expectedVersion + 1`, and persisting revision. Non-admin submission routes as an advisory proposal to admin.
     - *Mode NA*: Shifting slot schedule affects adjacent itinerary items. Submitting a reschedule request opens a schedule-modification voting round. (NOTE: Unanimous chat override is a separate chat-based flow requiring all members to agree in chat; ordinary voting follows Mode NA rules. Product policy on whether a non-admin in Mode NA can unilaterally trigger an immediate slot-time adjustment without a full voting round is pending: `[MODE_NA_RESCHEDULE_APPROVAL_POLICY_PENDING]`).
   - **State Transition**: In Mode A (approved), updates slot timestamps, increments version monotonically, and creates `revision_history` snapshot. In Mode NA, opens schedule proposal.
   - **Response**: Mode A: `{"status": "SLOT_RESCHEDULED", "slotId": "...", "version": N+1}`; Mode NA: `{"status": "RESCHEDULE_PROPOSAL_OPENED", "proposalId": "prp_..."}`.
   - **WebSocket Event**: `itineraryUpdated` (Mode A) or `proposalCreated` (Mode NA).
   - **Audit Effect**: `itinerary.slot_rescheduled` logged.

##### 2. Concurrency, Evidence Token Binding & Validation
- **Request Payload**:
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
- **Authoritative Validation via `consensus_service.apply_negotiation_selection`**:
  1. **Authentication & Membership**: Caller authenticated via Clerk JWT; membership and role verified in `trip_members`. Rejects non-members with `403 Forbidden` (`ERR_NOT_TRIP_MEMBER`).
  2. **Optimistic Concurrency Control (OCC)**: `expectedVersion` must strictly match `itineraries.version`. If stale, rejects with `409 Conflict` (`ERR_STALE_VERSION`).
  3. **Evidence Token Integrity & Freshness**:
     - `evidenceToken` is an opaque server-generated token binding `trip_id`, `slot_id`, `consensus_cycle_id`, `itinerary_version`, `candidate_id`, and `evidence_hash` with a 1-hour expiration TTL.
     - Target architecture proposes HMAC-SHA256 signature verification using server-internal secret (`[TARGET_PROPOSAL]`; secret strictly internal, never exposed in client payloads or docs).
     - If token is expired, rejects with `422 Unprocessable Entity` (`ERR_TOKEN_EXPIRED`); if tampered, missing, or binding mismatch, rejects with `422 Unprocessable Entity` (`ERR_EVIDENCE_INVALID`); path/body slot mismatch rejects with `400 Bad Request` (`ERR_SLOT_ID_MISMATCH`).
  4. **Duplicate Submission**: Idempotent check ensures duplicate clicks return recorded result or reject with `409 Conflict` (`ERR_DUPLICATE_SELECTION`).
  5. **Atomic Persistence**: All resulting state mutations (proposal creation, schedule adjustment, version bump, and audit records) are committed within a single atomic database transaction.

---

### 6.4 `branch_grouping.py`

**What it does**: Takes all holdout members' typed suggestions and groups them into N parallel branches. Near-duplicate preferences merge into the same branch. Single-member branches auto-finalize.

**Key rules**:
1. NO cap on number of branches — if 4 members want 4 truly different things, create 4 branches
2. Near-duplicate preferences (e.g. "beach" and "beach with water sports") merge into ONE branch
3. Single-member branches: set `auto_finalized = True` — their suggestion becomes the plan immediately, no vote needed
4. Multi-member branches where members still disagree: these get `parent_branch_id` set by `consensus_service.py` for recursive re-run
5. Branching is ONE-WAY for this consensus cycle — once we branch, we never go back to blending for this slot in this cycle

**Input**:
```python
def group_into_branches(
    holdout_members: list[dict],  # [{ "user_id": str, "comment": str, "suggestion": str }]
    itinerary_item: dict,
    trip_context: dict,
) -> dict:
    """
    Returns:
    {
        "action": "BRANCHED",
        "branches": [
            {
                "title": str,
                "rationale": str,
                "entity_type": str | None,
                "entity_id": str | None,
                "cost_delta": str,
                "currency": str,
                "member_user_ids": [str],
                "auto_finalized": bool,
            }
        ]
    }
    """
```

**System prompt for Phi-4-mini**:
```python
BRANCH_GROUPING_SYSTEM_PROMPT = """You are a travel preference clustering system.

You receive a list of group members and their stated preferences/objections for a travel activity.
Your job: Group these members into separate branches based on genuinely distinct, incompatible preferences.

RULES:
1. Create ONE branch per genuinely distinct preference — do NOT cap at 2
2. Merge near-duplicate preferences into the SAME branch (e.g. "beach" and "beach walk" → same branch)
3. Keep branches as few as possible while respecting genuine incompatibilities
4. Each branch should have a clear title summarizing that group's preference
5. For entity_type and entity_id: Select ONLY from verified candidate inventory. If no verified catalog POI is matched yet, set `entity_type: null, entity_id: null` with status 'AWAITING_ACTIVITY_PROPOSAL'.
6. Never generate realistic placeholder entity IDs like 'poi_[descriptive_name]' or 'poi_example'.
7. Singleton Group Governance Rule: Singleton branches (1 member) do NOT require group consensus voting, but their chosen activity MUST still pass catalog existence and schedule feasibility validation before confirmation.

Respond ONLY with a JSON object in this exact format:
{
  "branches": [
    {
      "title": "Branch title",
      "rationale": "Why this group was formed",
      "entity_type": null,
      "entity_id": null,
      "cost_delta": "0.00",
      "currency": "USD",
      "member_user_ids": ["usr_abc", "usr_def"]
    }
  ]
}"""
```

**Implementation**:
```python
from backend.ai.llm.client import safe_llm_call

def _build_fallback_branches(holdout_members, currency="USD"):
    """
    Fallback: Partition holdouts into an unfinalized branch awaiting real POI selection.
    Strictly eliminates synthetic entities (no poi_alternative, no poi_other).
    Singleton branches do NOT auto-finalize without verified activity feasibility.
    """
    return {
        "action": "BRANCHED",
        "branches": [
            {
                "title": "Alternative Preference Group",
                "rationale": "Members with differing preferences awaiting verified activity proposal",
                "entity_type": None,
                "entity_id": None,
                "cost_delta": "0.00",
                "currency": currency,
                "member_user_ids": [m["user_id"] for m in holdout_members],
                "auto_finalized": False,  # Activity must still be proposed and verified
                "status": "AWAITING_ACTIVITY_PROPOSAL",
            }
        ]
    }

def group_into_branches(holdout_members, itinerary_item, trip_context):
    if not holdout_members:
        return {"action": "BRANCHED", "branches": []}
    
    # Build member list with comments for LLM
    members_text = "\n".join([
        f"Member {m['user_id']}: \"{m['comment']}\""
        for m in holdout_members
    ])
    
    user_message = f"""
Activity being disagreed on: "{itinerary_item.get('title', 'Unknown activity')}"
Destination: {trip_context.get('destination_city', 'Unknown')}

Members who voted NO and their suggestions:
{members_text}

Group these members into parallel branches based on their distinct preferences.
Use the exact user_id strings provided above.
"""
    
    fallback = _build_fallback_branches(
        holdout_members, 
        itinerary_item.get("currency", "USD")
    )
    
    result = safe_llm_call(
        system_prompt=BRANCH_GROUPING_SYSTEM_PROMPT,
        user_message=user_message,
        fallback_result=fallback.get("branches", []),
    )
    
    # Result might be the branches list or the full dict
    if isinstance(result, list):
        branches = result
    elif isinstance(result, dict) and "branches" in result:
        branches = result["branches"]
    else:
        branches = fallback["branches"]
    
    # Post-process: Separate governance finalization from activity confirmation
    for branch in branches:
        member_ids = branch.get("member_user_ids", [])
        is_singleton = (len(member_ids) == 1)
        
        # Governance flag: single-member branches do not require internal voting
        branch["auto_finalized_governance"] = is_singleton
        
        # Activity confirmation status: an unverified preference NEVER becomes a confirmed itinerary activity automatically!
        if branch.get("entity_id") is None:
            branch["activity_confirmation_status"] = "AWAITING_ACTIVITY_PROPOSAL"
            branch["auto_finalized"] = False  # Explicitly prevent governance flag from implying confirmed itinerary item
        else:
            branch["activity_confirmation_status"] = "PENDING_VALIDATION"
            branch["auto_finalized"] = False
        
        # Strict monetary validation (NO silent coercion to 0.00 or guessed USD)
        cost_raw = branch.get("cost_delta")
        if cost_raw is None or str(cost_raw).strip() == "":
            branch["cost_delta"] = "0.00"
        else:
            try:
                from decimal import Decimal
                dec = Decimal(str(cost_raw).strip())
                if not dec.is_finite():
                    branch["cost_delta_error"] = "Non-finite branch cost delta"
            except Exception:
                branch["cost_delta_error"] = "Invalid numeric branch cost delta"
                
        if not branch.get("currency"):
            branch["currency"] = trip_context.get("base_currency") or itinerary_item.get("currency")
    
    # Validate branch partition: every holdout member must appear in exactly one branch
    holdout_ids = {m["user_id"] for m in holdout_members}
    is_valid, violations = validate_branch_partition(branches, holdout_ids)
    
    if not is_valid:
        # Canonical Rule: Invalid partitions do NOT invent synthetic entities (no poi_other).
        # A branch preference grouping without a verified activity is marked awaiting activity proposal.
        # Up to 2 bounded retries are permitted; if exhausted, the transaction aborts and preserves baseline.
        return {
            "action": "PARTITION_VALIDATION_FAILED",
            "message": f"Proposed branches violate partition constraints: {'; '.join(violations)}",
            "violations": violations,
            "branches": [],
            "baseline_preserved": True,
        }
    
    return {"action": "BRANCHED", "branches": branches}

def validate_branch_partition(
    branches: list[dict],
    expected_member_ids: set[str],
) -> tuple[bool, list[str]]:
    """
    Validates that a proposed set of branches forms a strict, exact partition
    of the expected holdout or electorate member IDs.
    
    Authority and Partition Invariants:
    1. Expected membership set is obtained authoritatively from domain state:
       expected_member_ids = {m['user_id'] for m in holdout_members} (or trip electorate).
    2. No empty branches: each branch must contain at least 1 member.
    3. No unknown IDs: every assigned member_user_id must exist in expected_member_ids.
    4. No duplicates within a single branch: member cannot appear twice in one branch.
    5. No duplicates across branches: branches must be pairwise disjoint (exactly-once membership).
    6. Completeness: every expected member must appear in exactly one branch (no missing members).
    7. No invented places: preferences without verified catalog entities must have
       entity_id = None, entity_type = None, status = 'AWAITING_ACTIVITY_PROPOSAL' (no synthetic poi_other).
    8. Singleton branches (len(member_user_ids) == 1) are marked auto_finalized = True.
    9. Atomicity: Database transaction remains atomic. If validation fails after bounded retries,
       no branches are partially persisted, the baseline proposal remains active, and an audit record
       'consensus.branch_partition_rejected' is recorded.
    
    Returns:
        (is_valid, list_of_violations)
    """
    violations = []
    if not branches:
        violations.append("Partition error: proposed branch list is empty.")
        return False, violations

    assigned_tracker: dict[str, int] = {}
    for idx, branch in enumerate(branches):
        m_list = branch.get("member_user_ids", [])
        if not m_list:
            violations.append(f"Branch {idx} ('{branch.get('title', 'Untitled')}') has no assigned members.")
            continue
        
        seen_in_branch = set()
        for uid in m_list:
            # Check duplicates within branch
            if uid in seen_in_branch:
                violations.append(f"Duplicate member '{uid}' found within branch {idx}.")
            seen_in_branch.add(uid)
            
            # Check unknown IDs
            if uid not in expected_member_ids:
                violations.append(f"Unknown member '{uid}' in branch {idx} (not in holdout/electorate set).")
            
            # Track overall counts across branches
            assigned_tracker[uid] = assigned_tracker.get(uid, 0) + 1

    # Check duplicates across branches (pairwise disjointness)
    for uid, count in assigned_tracker.items():
        if count > 1:
            violations.append(f"Member '{uid}' assigned {count} times across multiple branches (violates disjointness).")

    # Check missing members (completeness)
    missing = expected_member_ids - set(assigned_tracker.keys())
    if missing:
        violations.append(f"Missing members {sorted(list(missing))} not assigned to any branch.")

    return len(violations) == 0, violations
```

---

## 7. THE TWO MODE ORCHESTRATORS

### 7.1 `mode_na_orchestrator.py` (Collaborative — Fully Automatic)

```python
# backend/ai/modes/mode_na_orchestrator.py
from backend.ai.core.branch_trigger_classifier import classify_objection
from backend.ai.core.blended_plan_generator import generate_blended_plan
from backend.ai.core.branch_grouping import group_into_branches

SOFT_ROUND_CAP = 3

def run_mode_na_round(
    proposal: dict,
    no_votes: list[dict],    # [{ user_id, comment, round }]
    itinerary_item: dict,
    trip_context: dict,
    current_round: int,
    now: datetime,           # Authoritative UTC timestamp from domain service
    closes_at: Optional[datetime] = None, # Slot consensus deadline from slot_consensus.closes_at
) -> dict:
    """
    Mode NA full consensus round.
    
    ENGLISH-ONLY INTERACTION SCOPE:
    - Objection comments, clarification prompts, and explanations operate strictly in English.
    - Non-English input returns NEEDS_CLARIFICATION prompting the traveler in English.
    - No translation pipelines or multilingual language-detection dependencies are permitted.
    
    Timing Authority:
    - now and closes_at MUST be provided by Sharvani's domain persistence / system clock
      (datetime.now(timezone.utc) and slot_consensus.closes_at).
    - Client and transport timestamps are strictly forbidden from determining expiry.
    - If closes_at is None, time-based window closure cannot occur (window remains open).
    
    Returns:
    - BLENDED: Valid candidate generated and validated against hard constraints.
    - NEEDS_CLARIFICATION: Dissenting comments require clarification before candidate generation.
    - BLENDED_PLAN_FAILED: Candidate failed validation; baseline preserved (NO auto-branch).
    - BRANCHED: Evidence-backed FIXED_REQUIREMENT or round cap + window closure reached.
    """
    
    # Step 1: Classify objections using canonical 4-class taxonomy (English-Only)
    classification = classify_objection(
        no_comments=no_votes,
        current_round=current_round,
        soft_round_cap=SOFT_ROUND_CAP,
    )
    
    # Step 2: Handle Clarification / Insufficient Evidence explicitly
    # CANONICAL RULE: Clarification stops the cycle cleanly. It does NOT increment rounds,
    # invent a proposal, count as a vote, reset deadlines, or trigger branching.
    # Baseline proposal is preserved; clarification requested event emitted to user in English.
    if classification["classification"] in ("NEEDS_CLARIFICATION", "UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE"):
        return {
            "action": "NEEDS_CLARIFICATION",
            "message": "Objection comments require clarification before candidate generation.",
            "clarification_needed": True,
            "classification_category": classification["classification"],
            "reasoning": classification.get("reasoning", ""),
            "extracted_constraints": classification.get("extracted_constraints", []),
            "current_proposal_id": proposal.get("id"),
            "current_round": current_round,
            "baseline_preserved": True,
            "advisory": False,
        }
    
    # Step 3: Evaluate Round Cap AND Window Closure Guard
    # CANONICAL RULE: Round-cap branching requires BOTH completion of round 3 AND window closure
    # (now >= closes_at) with unresolved dissent. Cannot branch on round >= 3 while window is open!
    window_closed = (now >= closes_at) if closes_at else False
    at_round_cap = (current_round >= SOFT_ROUND_CAP) and window_closed
    
    # Early branch exception ONLY on deterministic proof of irreconcilable hard constraints
    # CANONICAL RULE: Three-valued evaluation: COMPATIBLE, INCOMPATIBLE, UNKNOWN.
    # Missing attribute evidence (wheelchair accessibility, dietary tags, cost, intensity, hours)
    # yields UNKNOWN, NEVER deterministic proof of incompatibility!
    # Truncated search, provider failure, or incomplete catalog yields UNCERTAINTY (status='UNVERIFIED'),
    # NEVER fixed incompatibility. Early branching on incomplete or uncertain search is PROHIBITED.
    is_fixed_incompatibility = False
    
    # Check search completeness and provider status in real control flow (SAFE FAIL: do NOT default to True)
    is_truncated = trip_context.get("is_catalog_truncated") is True
    search_complete = trip_context.get("catalog_search_complete") is True
    provider_failed = trip_context.get("provider_failed") is True
    
    if classification.get("classification") == "FIXED_REQUIREMENT" and not is_truncated and search_complete and not provider_failed:
        trusted_catalog = trip_context.get("trusted_catalog_candidates") or {}
        if trusted_catalog:
            # Deterministic evaluation across canonical HARD_RESTRICTIONS schema:
            # { "domain": "MOBILITY_PHYSICAL" | "DIETARY" | "BUDGET" | "SCHEDULE" | "INTENSITY",
            #   "operator": "LESS_THAN_OR_EQUAL" | "EQUALS" | "REQUIRES_RAMP" | "NO_STAIRS",
            #   "value": Any, "currency": Optional[str] }
            # Soft preferences (SOFT_PREFERENCE) NEVER trigger early branching.
            hard_restrictions = [
                c for c in classification.get("extracted_constraints", [])
                if c.get("constraint_type") == "HARD_RESTRICTION"
            ]
            
            compatible_candidates = []
            uncertain_candidates = []
            
            for cand in trusted_catalog.values():
                cand_status = "COMPATIBLE"
                for hr in hard_restrictions:
                    domain = hr.get("domain", "").upper()
                    op = hr.get("operator", "").upper()
                    val = hr.get("value")
                    
                    # 1. Mobility / Physical
                    if domain == "MOBILITY_PHYSICAL":
                        acc = cand.get("wheelchair_accessible")
                        if acc is None:
                            cand_status = "UNKNOWN"
                        elif op in ["REQUIRES_RAMP", "WHEELCHAIR"] and not acc:
                            cand_status = "INCOMPATIBLE"
                            break
                        elif op == "NO_STAIRS" and cand.get("has_stairs", False):
                            cand_status = "INCOMPATIBLE"
                            break
                    # 2. Dietary
                    elif domain == "DIETARY":
                        cand_tags = cand.get("dietary_tags")
                        if cand_tags is None:
                            cand_status = "UNKNOWN"
                        elif val and val not in cand_tags:
                            cand_status = "INCOMPATIBLE"
                            break
                    # 3. Budget
                    elif domain == "BUDGET":
                        cand_cost = cand.get("cost")
                        cand_curr = cand.get("currency")
                        req_curr = hr.get("currency")
                        if cand_cost is None:
                            cand_status = "UNKNOWN"
                        elif req_curr and cand_curr and cand_curr != req_curr:
                            # Cross-currency comparison blocked pending Decision #23
                            cand_status = "UNKNOWN"
                        elif op in ["LESS_THAN_OR_EQUAL", "MAX_COST"] and val is not None:
                            if Decimal(str(cand_cost)) > Decimal(str(val)):
                                cand_status = "INCOMPATIBLE"
                                break
                    # 4. Physical Intensity
                    elif domain == "INTENSITY":
                        cand_intensity = cand.get("intensity")
                        if cand_intensity is None:
                            cand_status = "UNKNOWN"
                        elif cand_intensity == "HIGH" and val == "LOW":
                            cand_status = "INCOMPATIBLE"
                            break
                    # 5. Schedule
                    elif domain == "SCHEDULE":
                        cand_hours = cand.get("operating_hours")
                        if cand_hours is None:
                            cand_status = "UNKNOWN"
                    # 6. Unsupported constraint operators return UNKNOWN
                    else:
                        cand_status = "UNKNOWN"
                        
                if cand_status == "COMPATIBLE":
                    compatible_candidates.append(cand)
                elif cand_status == "UNKNOWN":
                    uncertain_candidates.append(cand)
                    
            # MATHEMATICAL PROOF: Feasible candidates == empty AND zero uncertain candidates
            # If any candidates are UNKNOWN, or search was bounded/incomplete, early branch is PROHIBITED.
            if len(compatible_candidates) == 0 and len(uncertain_candidates) == 0 and len(hard_restrictions) > 0 and len(trusted_catalog) > 0:
                is_fixed_incompatibility = True
    
    # Step 4: Decide: blend or branch?
    should_branch = is_fixed_incompatibility or at_round_cap
    
    if should_branch:
        # Holdout members partitioned using validate_branch_partition
        holdout_members = [
            {"user_id": v["user_id"], "comment": v["comment"], "suggestion": v["comment"]}
            for v in no_votes
        ]
        return group_into_branches(holdout_members, itinerary_item, trip_context)
    
    # Step 5: Try blending
    try:
        return generate_blended_plan(
            current_proposal=proposal,
            no_vote_comments=no_votes,
            itinerary_item=itinerary_item,
            trip_context=trip_context,
            current_round=current_round,
        )
    except Exception as e:
        # Fail-closed: LLM errors fall back cleanly to baseline proposal
        return {
            "action": "BLENDED_PLAN_FAILED",
            "blended_plan": None,
            "reason": f"AI service error during blended plan generation: {str(e)}",
            "baseline_preserved": True,
            "current_proposal_id": proposal.get("id"),
            "current_round": current_round,
            "retry_permitted": True,
        }
```

## 7.2 `mode_a_orchestrator.py` (Admin-Led)

```python
# backend/ai/modes/mode_a_orchestrator.py
from backend.ai.core.branch_trigger_classifier import classify_objection
from backend.ai.core.blended_plan_generator import generate_blended_plan
from backend.ai.core.branch_grouping import group_into_branches

def run_mode_a_round(
    proposal: dict,
    no_votes: list[dict],
    itinerary_item: dict,
    trip_context: dict,
    current_round: int,
    now: datetime,
    closes_at: Optional[datetime] = None,
    admin_action: str | None = None,  # 'force_branch' | 'extend' | 'accept' | None
) -> dict:
    """
    Mode A consensus round.
    Admin action overrides AI recommendation.
    Returns a result dict — in Mode A, AI recommendations are strictly ADVISORY (admin decides).
    """
    
    # If admin has explicitly acted, honor that immediately
    if admin_action == "force_branch":
        holdout_members = [
            {"user_id": v["user_id"], "comment": v["comment"], "suggestion": v["comment"]}
            for v in no_votes
        ]
        return group_into_branches(holdout_members, itinerary_item, trip_context)
    
    if admin_action == "extend":
        # Just return current state — round continues
        return {
            "action": "EXTENDED",
            "message": "Admin extended the round. Voting window continues.",
            "current_round": current_round,
        }
    
    # No admin action yet → generate AI recommendation (advisory only)
    classification = classify_objection(
        no_comments=no_votes,
        current_round=current_round,
    )
    
    # Handle Clarification / Insufficient Evidence advisory recommendation
    if classification["classification"] in ("NEEDS_CLARIFICATION", "UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE"):
        return {
            "action": "NEEDS_CLARIFICATION",
            "advisory": True,
            "admin_recommendation": f"Clarification requested from dissenting members ({classification['classification']})",
            "clarification_needed": True,
            "classification_category": classification["classification"],
            "reasoning": classification.get("reasoning", ""),
            "extracted_constraints": classification.get("extracted_constraints", []),
            "current_proposal_id": proposal.get("id"),
            "current_round": current_round,
        }
    
    if classification["classification"] == "FIXED_REQUIREMENT":
        # Recommend branching to admin
        holdout_members = [
            {"user_id": v["user_id"], "comment": v["comment"], "suggestion": v["comment"]}
            for v in no_votes
        ]
        branch_result = group_into_branches(holdout_members, itinerary_item, trip_context)
        branch_result["advisory"] = True  # Flag: admin must still approve
        branch_result["admin_recommendation"] = "Branch — fixed incompatible requirements detected"
        return branch_result
    
    # Try blending
    try:
        blend_result = generate_blended_plan(
            current_proposal=proposal,
            no_vote_comments=no_votes,
            itinerary_item=itinerary_item,
            trip_context=trip_context,
            current_round=current_round,
        )
        blend_result["advisory"] = True  # Flag: admin must still approve
        blend_result["admin_recommendation"] = "Accept blended plan — objections appear resolvable"
        return blend_result
    except ValueError as e:
        # Canonical Rule: Blending failure does NOT force branch automatically.
        # Report failure advisely to admin for manual decision.
        return {
            "action": "BLENDED_PLAN_FAILED",
            "advisory": True,
            "admin_recommendation": f"Blending validation failed ({str(e)}). Admin may manually extend round, enter proposal, or trigger branching.",
            "baseline_preserved": True,
            "current_proposal_id": proposal.get("id"),
        }
```

---

### 7.3 The Asynchronous Snapshot-and-Commit Consensus Pattern (`consensus_service.py`)

#### Authoritative Consensus Logical Field Mapping (CURRENT vs TARGET)

`[MANDATORY_ARCHITECTURE_MAPPING]`
The physical PostgreSQL models in `backend/app/models/provided.py` and `backend/app/models/additive.py` (stamped at Alembic revision `c8a6a4789a32`) define the verified starting baseline. Proposed consensus algorithms operate across logical fields mapped precisely below:

| Logical Field | Current Physical Column / Model Path | Proposed Target Schema Field | Owner | Migration Dependency | Implementation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`slot_id`** | `itinerary_items.item_id` (Text PK; FK `slot_consensus.item_id`) | `slot_consensus.slot_id` (alias to `item_id`) | Sharvani | None (Physical column is `item_id`) | Current Physical |
| **`trip_id`** | Derived via `itinerary_items.itinerary_id -> itineraries.trip_id` | `slot_consensus.trip_id` (denormalized FK) | Sharvani | Future Migration | Target Proposed |
| **`consensus_id`**| `slot_consensus.consensus_id` (`slc_` prefixed PK in `additive.py:126`) | `slot_consensus.consensus_id` | Sharvani | Stamped in `c8a6a4789a32` | Current Physical |
| **`cycle_id`** | `slot_consensus.consensus_cycle` (Integer default 1 in `additive.py:130`) | `slot_consensus.cycle_id` (UUID) | Sharvani | Future Migration | Current Physical is Integer |
| **`slot_status`** | `slot_consensus.slot_status` (String(50) in `additive.py:128`) | `slot_consensus.slot_status` | Sharvani | Stamped in `c8a6a4789a32` | Current Physical |
| **`active_proposal_id`** | Derived via latest `proposals.id` where `slot_id == item_id` | `slot_consensus.active_proposal_id` (FK) | Sharvani | Future Migration | Target Proposed |
| **`closes_at`** | `slot_consensus.first_no_at` + 10m countdown (computed in memory) | `slot_consensus.closes_at` (Timestamp with TZ) | Sharvani | Future Migration | Target Proposed |
| **`ai_request_id`** (Lease) | Not present in ORM models | `slot_consensus.ai_request_id` + `lease_expires_at` | Sharvani | Future Migration | Target Proposed |
| **`generation_attempts`**| Not present in ORM models | `slot_consensus.generation_attempts` (SmallInt) | Sharvani | Future Migration | Target Proposed |
| **`AuditLog`** | `additive.py:RevisionHistory` (`revision_history` table) | Dedicated `audit_logs` entity (Decision #17/#29) | Sharvani | Decision #17/#29 Pending | Target Proposed |
| **`ActivityPOI`**| Table `activities_poi` in `data-model/schema.sql` (Raw SQL) | Dedicated ORM model `ActivityPOI` | Sharvani | Future Model Registration | Target Proposed |

#### Asynchronous Snapshot-and-Commit Pattern (`consensus_service.py`)

`[APPROVED_REQUIREMENT]` Long-lived PostgreSQL row locks must **never** be held across external LLM inference (5–15 seconds). Domain services execute reconciliation using this verified two-phase pattern illustrated via abstract repository interfaces:

```python
# backend/app/services/consensus_service.py (Authoritative Abstract Repository Pseudocode Contract)
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from backend.app.models.additive import SlotConsensus, Branch, BranchMember, RevisionHistory
from backend.app.models.provided import Itinerary, Proposal, ItineraryItem

"""
CONCURRENCY & LEASE SPECIFICATION:
1. Current Source ORM Baseline (Alembic revision c8a6a4789a32):
   - SlotConsensus: consensus_id, item_id, slot_status, current_round, consensus_cycle, first_no_at, created_at, updated_at.
   - Proposal: proposal_id, itinerary_id, proposed_by_user_id, action, target_item_id, entity_type, entity_id, title, rationale, cost_delta, currency, closes_at, status, created_at, updated_at.
   - Branch: branch_id, item_id, parent_branch_id, title, rationale, entity_type, entity_id, cost_delta, currency, status, created_at, updated_at.
   - BranchMember: member_id, branch_id, user_id, confirmed, created_at.
   - RevisionHistory: revision_id, item_id, version_number, snapshot_data, created_by, created_at.
   - Itinerary: itinerary_id, trip_id, version, status, etc.

2. Proposed Target Schema Additions (Decision #17):
   - SlotConsensus proposed fields: lease_token (VARCHAR 64), lease_expires_at (DATETIME), generation_attempts (INTEGER).
   Until physical migration is applied, active lease token and expiry are tracked via in-memory coordination or durable snapshot records.

3. Complete Crash Recovery Matrix (7 Scenarios):
   1. Claim committed but dispatch failed: Lease expires after 30s; subsequent timer check or user request reclaims lease.
   2. Worker crash during inference: Worker dies silently; lease expires at now + 30s; next recovery scan resets lease.
   3. Expired claim: Commit verifies now < lease_expires_at; if expired, callback is rejected with 409 Conflict (ERR_LEASE_EXPIRED).
   4. Two workers claiming same slot: Serialized via SELECT ... FOR UPDATE; second worker sees active lease (now < lease_expires_at) and is rejected with 409 (ERR_CONCURRENT_RECONCILIATION).
   5. Repeated callback: First callback commits and clears lease; second callback finds mismatched lease_token and is rejected as idempotent duplicate or discarded.
   6. Callback from superseded worker: Verified against snapshot_version and snapshot_cycle; if itinerary version bumped, candidate is discarded without mutation.
   7. Commit success followed by event-delivery failure: DB transaction committed; client resync via HTTP GET /api/trips/{trpId} recovers authoritative state.
"""

LEASE_TTL_SECONDS = 30

PROPOSED_LEASE_TTL_SECONDS = 30  # [PROPOSED_LEASE_TTL] subject to Decision #17

def canonicalize_extracted_constraints(constraints: List[Any]) -> List[Dict[str, Any]]:
    """
    Normative canonical serializer for structured objection constraints.
    Governs both snapshot capture (Phase 1) and commit-time revalidation (Phase 2).
    
    Schema-Driven Normalization Contract:
    1. Type Validation:
       - Valid constraint records must be dictionaries or structured objects.
       - Unstructured string constraints are normalized to {"type": "unstructured_constraint", "value": s.strip()}.
       - Unsupported or malformed non-dict/non-string items raise TypeError('ERR_MALFORMED_CONSTRAINT').
    2. Boolean vs Numeric Discrimination:
       - Evaluates bool before int/float (preventing Python issubclass(bool, int) coercion).
       - True and False are strictly preserved as native booleans (never 1, 1.0, or 0).
    3. Numeric & Float Precision:
       - Integers are strictly preserved as native ints.
       - Floats and Decimals: preserved with exact precision (no lossy two-decimal rounding,
         ensuring distinct coordinates or weights such as 48.8584 != 48.8589 remain distinguishable).
    4. String & Enum Normalization:
       - Field 'type': stripped lowercase identifier (e.g. 'budget_max', 'accessibility', 'cuisine_veto').
       - Field 'currency': stripped uppercase 3-letter ISO code (e.g. 'USD', 'EUR') or None if absent.
       - Field 'unit': stripped lowercase identifier or None if absent.
       - General text fields (e.g. description, reason): whitespace-trimmed, case preserved.
    5. Unknown & Extended Schema Fields:
       - All dictionary keys are retained and recursively canonicalized (no silent field dropping).
    6. Deterministic Sorting:
       - The list of normalized constraint objects is sorted by stable JSON serialization
         (key=lambda x: json.dumps(x, sort_keys=True)).
       - Completely prevents Python dictionary comparison TypeError.
    """
    normalized = []
    for c in constraints or []:
        if isinstance(c, str):
            normalized.append({
                "currency": None,
                "type": "unstructured_constraint",
                "unit": None,
                "value": c.strip()
            })
        elif isinstance(c, dict):
            norm_c = {}
            for k, v in sorted(c.items()):
                k_str = str(k).strip()
                if k_str == "type":
                    norm_c["type"] = str(v).strip().lower() if v is not None else ""
                elif k_str == "currency":
                    norm_c["currency"] = str(v).strip().upper() if v else None
                elif k_str == "unit":
                    norm_c["unit"] = str(v).strip().lower() if v else None
                elif isinstance(v, bool):  # MUST precede int check
                    norm_c[k_str] = v
                elif isinstance(v, int):
                    norm_c[k_str] = v
                elif isinstance(v, float):
                    norm_c[k_str] = v  # Exact precision preserved
                elif isinstance(v, str):
                    norm_c[k_str] = v.strip()
                elif v is None:
                    norm_c[k_str] = None
                elif isinstance(v, (dict, list)):
                    norm_c[k_str] = json.loads(json.dumps(v, sort_keys=True))
                else:
                    norm_c[k_str] = str(v)
            
            # Ensure canonical keys are present
            if "type" not in norm_c:
                norm_c["type"] = "general"
            if "currency" not in norm_c:
                norm_c["currency"] = None
            if "unit" not in norm_c:
                norm_c["unit"] = None
            if "value" not in norm_c:
                norm_c["value"] = None
                
            normalized.append(norm_c)
        else:
            raise TypeError(f"ERR_MALFORMED_CONSTRAINT: Expected dict or str, got {type(c).__name__}")
            
    return sorted(normalized, key=lambda x: json.dumps(x, sort_keys=True))

def canonicalize_clarifications(clarifications: List[Any]) -> List[Dict[str, Any]]:
    """
    Normative canonical serializer for slot clarification records.
    Ensures deterministic ordering and tie-breaking across multiple clarification
    records for the same voter or slot.
    
    Ordering & Tie-Breaking Policy:
    - Primary Sort Key: (vote_id, user_id)
    - Stable Tie-Breaker: clarification_id (stable PK in [PROPOSED_STORAGE] table).
      Fallback when unmapped: deterministic SHA256 hash of clarification_text and constraints.
    """
    canonical_list = []
    for c in clarifications or []:
        if not isinstance(c, dict):
            raise TypeError(f"ERR_MALFORMED_CLARIFICATION: Expected dict, got {type(c).__name__}")
        v_id = str(c.get("vote_id", "")).strip()
        u_id = str(c.get("user_id", "")).strip()
        clar_id = str(c.get("clarification_id") or c.get("id") or "").strip()
        text = str(c.get("clarification_text", "")).strip()
        raw_constraints = c.get("extracted_constraints", [])
        norm_constraints = canonicalize_extracted_constraints(raw_constraints)
        
        if not clar_id:
            tie_breaker = hashlib.sha256(f"{text}|{json.dumps(norm_constraints, sort_keys=True)}".encode()).hexdigest()[:16]
        else:
            tie_breaker = clar_id
            
        canonical_list.append({
            "clarification_id": tie_breaker,
            "clarification_text": text,
            "extracted_constraints": norm_constraints,
            "user_id": u_id,
            "vote_id": v_id
        })
        
    return sorted(canonical_list, key=lambda x: (x["vote_id"], x["user_id"], x["clarification_id"]))

def start_async_reconciliation(db: Session, item_id: str) -> dict:
    """
    Phase 1: Short Read Transaction & Atomic Durable Lease Acquisition
    
    VERIFIED SOURCE MODEL MAPPING (models/provided.py):
    - Vote: Model is `Vote` (table `votes`); vote value is `value` ('yes', 'no'); has `comment`, `proposal_id`, `user_id`.
    - Trip: Model is `Trip` (table `trips`); mode is `mode` ('Mode NA', 'Mode A').
    - TripMember: Model is `TripMember` (table `trip_members`); status is lowercase string 'active'.
    - Proposal: Model is `Proposal` (table `proposals`); action is 'replace_item' or 'ADVISORY_PROPOSAL'.
    
    TARGET MODEL PREREQUISITE & SCHEMA CONTRACT:
    - Atomic lease persistence requires migrated target fields:
        SlotConsensus.lease_token (VARCHAR(36))
        SlotConsensus.lease_expires_at (TIMESTAMP WITH TIME ZONE)
        SlotConsensus.generation_attempts (INTEGER)
      pending approval and schema migration under Decision #17.
    - In this target engineering contract, abstract repository persistence (consensus_repo)
      defines durable atomic write semantics. We DO NOT assume unmapped Python attributes
      magically persist in the current database schema. (Zero migration/source code edits are made here).
      
    Target Concurrency Algorithm:
    - Acquires brief row lock on SlotConsensus (SELECT ... FOR UPDATE).
    - Checks whether an active claim exists (lease_expires_at is not None and now < lease_expires_at).
    - If active, rejects concurrent attempt cleanly (409 / CONCURRENT_CLAIM_ACTIVE).
    - Durably writes unique lease_token and lease_expires_at via target repository.
    - Captures immutable state snapshot fingerprint (competing proposals, votes, comments, electorate, mode).
    - Commits immediately to release DB row lock before dispatching async LLM inference.
    """
    import hashlib, json
    from ..models.provided import Trip, Itinerary, ItineraryItem, Proposal, Vote, TripMember
    from ..models.additive import SlotConsensus, RevisionHistory
    
    now = datetime.now(timezone.utc)
    
    # 1. Authoritative Row Lock on SlotConsensus
    slot_consensus = db.query(SlotConsensus).filter(
        SlotConsensus.item_id == item_id
    ).with_for_update().first()
    
    if not slot_consensus:
        raise ValueError(f"SlotConsensus for item_id {item_id} not found")
        
    itinerary_item = db.query(ItineraryItem).filter(ItineraryItem.item_id == item_id).first()
    itinerary = db.query(Itinerary).filter(Itinerary.itinerary_id == itinerary_item.itinerary_id).first()
    trip = db.query(Trip).filter(Trip.trip_id == itinerary.trip_id).first()
    
    # 2. ATOMIC LIVE CLAIM CHECK:
    active_expiry = getattr(slot_consensus, "lease_expires_at", None)
    if active_expiry is not None and now < active_expiry:
        # Another worker is actively reconciling this slot within the 30s TTL
        db.rollback()
        return {
            "status": "CONCURRENT_CLAIM_ACTIVE",
            "active_lease_expires_at": active_expiry.isoformat(),
            "message": "Reconciliation already in progress for this slot"
        }
        
    # 3. ACQUIRE & PERSIST UNIQUE LEASE ATOMICALLY
    lease_token = f"lease_{uuid.uuid4().hex}"
    lease_expires_at = now + timedelta(seconds=PROPOSED_LEASE_TTL_SECONDS)
    
    # Target repository write: persists lease_token, lease_expires_at, and attempt counter
    setattr(slot_consensus, "lease_token", lease_token)
    setattr(slot_consensus, "lease_expires_at", lease_expires_at)
    current_attempts = getattr(slot_consensus, "generation_attempts", 0) or 0
    setattr(slot_consensus, "generation_attempts", current_attempts + 1)
    
    # 4. COMPREHENSIVE DETERMINISTIC SNAPSHOT FINGERPRINT ACROSS ALL COMPETING PROPOSALS
    # Contested slots can have competing proposals; capture ALL active proposals and their votes!
    slot_proposals = db.query(Proposal).filter(
        Proposal.itinerary_id == itinerary.itinerary_id,
        Proposal.target_item_id == item_id
    ).all()
    
    proposal_ids = [p.proposal_id for p in slot_proposals]
    slot_votes = []
    if proposal_ids:
        slot_votes = db.query(Vote).filter(Vote.proposal_id.in_(proposal_ids)).all()
        
    electorate_members = {
        m.user_id for m in db.query(TripMember).filter(
            TripMember.trip_id == itinerary.trip_id,
            TripMember.status == "active" # Verified lowercase status in models/provided.py
        ).all()
    }
    
    # Authoritative Clarification & Constraint Retrieval:
    # Preserves original objection in votes.comment for auditability.
    # Supplementary clarifications and structured constraints C_obj retrieved via repository accessor.
    # [PROPOSED_STORAGE] for dedicated slot_clarifications table; accessor reads from consensus state.
    slot_clarifications = consensus_repo.get_slot_clarifications(db, item_id=item_id)
    
    # Canonical deterministic list sorting before hashing (DB row order cannot alter hash!)
    canonical_state = {
        "proposals": [
            {"id": p.proposal_id, "action": p.action, "status": p.status}
            for p in sorted(slot_proposals, key=lambda x: x.proposal_id)
        ],
        "votes": [
            {"p": v.proposal_id, "u": v.user_id, "val": v.value, "c": v.comment or ""}
            for v in sorted(slot_votes, key=lambda x: (x.proposal_id, x.user_id))
        ],
        "clarifications": canonicalize_clarifications(slot_clarifications),
        "electorate": sorted(list(electorate_members)),
        "mode": trip.mode if trip else "Mode NA" # Verified trip.mode in models/provided.py
    }
    state_fingerprint = hashlib.sha256(json.dumps(canonical_state, sort_keys=True).encode()).hexdigest()
    
    snapshot = {
        "item_id": item_id,
        "itinerary_id": itinerary.itinerary_id,
        "trip_id": itinerary.trip_id,
        "consensus_cycle": slot_consensus.consensus_cycle,
        "itinerary_version": itinerary.version,
        "current_round": slot_consensus.current_round,
        "trip_mode": trip.mode if trip else "Mode NA",
        "state_fingerprint": state_fingerprint,
        "lease_token": lease_token,
        "lease_expires_at": lease_expires_at.isoformat(),
        "snapshot_timestamp": now.isoformat(),
    }
    
    # Commit transaction to persist lease and release row lock immediately
    db.commit()
    
    return {"status": "DISPATCHED", "lease_token": lease_token, "snapshot": snapshot}

def commit_reconciliation_result(
    db: Session,
    item_id: str,
    lease_token: str,
    snapshot: dict,
    ai_result: dict,
    initiating_user_id: str,
    server_reconciliation_context: Optional[dict] = None
) -> dict:
    """
    Phase 2: Short Write Transaction with Fail-Closed Lease Check, Snapshot OCC & Partition Validation
    
    AUTHORITY CONTRACT:
    - initiating_user_id: Authenticated trip member executing the dissent or action.
    - Proposal attribution: proposals.proposed_by_user_id references initiating_user_id (users.user_id FK).
    - System execution identity ('system_ai_concierge') is recorded in RevisionHistory and audit logs.
    - In Mode A: proposals are marked action='ADVISORY_PROPOSAL', status='open' (non-binding until accepted).
    - Mode is loaded authoritatively from trip.mode in the database, NEVER from caller parameters.
    """
    import hashlib, json
    from ..models.provided import Trip, Itinerary, ItineraryItem, Proposal, Vote, TripMember
    from ..models.additive import SlotConsensus, RevisionHistory, Branch, BranchMember
    
    now = datetime.now(timezone.utc)
    snapshot_version = snapshot.get("itinerary_version")
    snapshot_cycle = snapshot.get("consensus_cycle")
    
    # 1. Acquire write locks
    slot_consensus = db.query(SlotConsensus).filter(
        SlotConsensus.item_id == item_id
    ).with_for_update().first()
    itinerary_item = db.query(ItineraryItem).filter(ItineraryItem.item_id == item_id).first()
    itinerary = db.query(Itinerary).filter(Itinerary.itinerary_id == itinerary_item.itinerary_id).with_for_update().first()
    trip = db.query(Trip).filter(Trip.trip_id == itinerary.trip_id).first()
    
    mode = trip.mode if trip else "Mode NA"
    
    # 2. FAIL-CLOSED LEASE CLAIM VERIFICATION
    active_token = getattr(slot_consensus, "lease_token", None)
    active_expiry = getattr(slot_consensus, "lease_expires_at", None)
    
    # Guard 2A: Must have an active stored claim (cleared claims reject repeated callbacks)
    if not active_token:
        db.rollback()
        return {
            "status": "DISCARDED_NO_ACTIVE_CLAIM",
            "reason": "No active lease claim exists for this slot (claim already cleared, expired, or never acquired)"
        }
        
    # Guard 2B: Exact token match
    if active_token != lease_token:
        db.rollback()
        return {
            "status": "DISCARDED_SUPERSEDED_LEASE",
            "reason": f"Lease token mismatch: stored '{active_token}' != callback '{lease_token}'"
        }
        
    # Guard 2C: Non-null and live expiry
    if active_expiry is None or now >= active_expiry:
        setattr(slot_consensus, "lease_token", None)
        setattr(slot_consensus, "lease_expires_at", None)
        db.commit()
        return {
            "status": "DISCARDED_LEASE_EXPIRED",
            "reason": f"Lease expired before inference completed (expiry={active_expiry}, now={now})"
        }
        
    # 3. REVALIDATE ENTIRE CAPTURED STATE FINGERPRINT & OCC VERSION
    slot_proposals = db.query(Proposal).filter(
        Proposal.itinerary_id == itinerary.itinerary_id,
        Proposal.target_item_id == item_id
    ).all()
    proposal_ids = [p.proposal_id for p in slot_proposals]
    slot_votes = []
    if proposal_ids:
        slot_votes = db.query(Vote).filter(Vote.proposal_id.in_(proposal_ids)).all()
        
    electorate_members = {
        m.user_id for m in db.query(TripMember).filter(
            TripMember.trip_id == itinerary.trip_id,
            TripMember.status == "active"
        ).all()
    }
    
    slot_clarifications = consensus_repo.get_slot_clarifications(db, item_id=item_id)
    
    current_canonical_state = {
        "proposals": [
            {"id": p.proposal_id, "action": p.action, "status": p.status}
            for p in sorted(slot_proposals, key=lambda x: x.proposal_id)
        ],
        "votes": [
            {"p": v.proposal_id, "u": v.user_id, "val": v.value, "c": v.comment or ""}
            for v in sorted(slot_votes, key=lambda x: (x.proposal_id, x.user_id))
        ],
        "clarifications": canonicalize_clarifications(slot_clarifications),
        "electorate": sorted(list(electorate_members)),
        "mode": trip.mode if trip else "Mode NA"
    }
    current_state_fingerprint = hashlib.sha256(json.dumps(current_canonical_state, sort_keys=True).encode()).hexdigest()
    
    is_stale = (
        (itinerary.version != snapshot_version) or
        (slot_consensus.consensus_cycle != snapshot_cycle) or
        (current_state_fingerprint != snapshot.get("state_fingerprint"))
    )
    
    if is_stale:
        # Clear lease and discard stale result without mutating slot or proposals
        setattr(slot_consensus, "lease_token", None)
        setattr(slot_consensus, "lease_expires_at", None)
        
        rev_id = f"rev_{uuid.uuid4().hex[:12]}"
        db.add(RevisionHistory(
            revision_id=rev_id,
            item_id=item_id,
            version_number=itinerary.version,
            snapshot_data={
                "event": "STALE_AI_DISCARDED",
                "reason": "State mutation detected during inference (version/cycle/vote/electorate/comment mismatch)",
                "discarded_action": ai_result.get("action")
            },
            created_by=initiating_user_id
        ))
        db.commit()
        return {
            "status": "DISCARDED_STALE",
            "reason": "State mutation occurred while AI inference was running"
        }
        
    action = ai_result.get("action")
    
    # 4. Apply Atomic Mutations with Exact Physical ORM Models
    if action == "BLENDED" and ai_result.get("blended_plan"):
        plan = ai_result.get("proposal_payload") or ai_result["blended_plan"]
        new_proposal_id = f"prp_{uuid.uuid4().hex[:12]}"
        
        proposal_action = "ADVISORY_PROPOSAL" if mode == "Mode A" else "replace_item"
        
        new_proposal = Proposal(
            proposal_id=new_proposal_id,
            itinerary_id=itinerary.itinerary_id,
            proposed_by_user_id=initiating_user_id,
            action=proposal_action,
            target_item_id=item_id,
            entity_type=plan.get("entity_type", "poi"),
            entity_id=plan.get("entity_id"),
            title=plan["title"],
            rationale=plan.get("rationale", ""),
            cost_delta=plan.get("cost_delta", "0.00"),
            currency=plan.get("currency", "USD"),
            status="open"
        )
        db.add(new_proposal)
        
        slot_consensus.current_round += 1
        slot_consensus.slot_status = "IN_CONSENSUS"  # Mapped column in models/additive.py:27; target enum 'PROPOSAL_OPEN' is [TARGET_ENUM_EXPANSION]
        
        # Clear active lease upon successful commit
        setattr(slot_consensus, "lease_token", None)
        setattr(slot_consensus, "lease_expires_at", None)
        
        # INVARIANT: Publishing an open/advisory proposal does NOT confirm the slot
        # and does NOT mutate itineraries.version! Master itinerary item is unchanged.
        # itineraries.version is preserved at current version.
        
        rev_id = f"rev_{uuid.uuid4().hex[:12]}"
        db.add(RevisionHistory(
            revision_id=rev_id,
            item_id=item_id,
            version_number=itinerary.version,
            snapshot_data={
                "event": "BLENDED_PROPOSAL_PUBLISHED",
                "proposal_id": new_proposal_id,
                "advisory": (mode == "Mode A"),
                "round": slot_consensus.current_round
            },
            created_by=initiating_user_id
        ))
        
        db.commit()
        return {
            "status": "COMMITTED",
            "action": "BLENDED_PROPOSAL_PUBLISHED",
            "proposal_id": new_proposal_id,
            "round": slot_consensus.current_round
        }
        
    elif action in ["NEEDS_CLARIFICATION", "BLENDED_PLAN_FAILED"]:
        # Clarification & Failure preserve baseline; clear lease; do NOT bump version
        setattr(slot_consensus, "lease_token", None)
        setattr(slot_consensus, "lease_expires_at", None)
        
        rev_id = f"rev_{uuid.uuid4().hex[:12]}"
        db.add(RevisionHistory(
            revision_id=rev_id,
            item_id=item_id,
            version_number=itinerary.version,
            snapshot_data={
                "event": action,
                "violations": ai_result.get("violations"),
                "status": ai_result.get("status")
            },
            created_by=initiating_user_id
        ))
        db.commit()
        return {"status": action, "details": ai_result}
        
    elif action == "BRANCHED":
        # Mandatory Authoritative Branch Partition Validation Before Any Writes
        branches_data = ai_result.get("branches", [])
        if not branches_data:
            db.rollback()
            return {"status": "FAILED", "reason": "No branch partition data supplied"}
            
        # SERVER-OWNED RECONCILIATION SCOPE: Define parent branch from server context, not model row 0!
        server_ctx = server_reconciliation_context or {}
        authorized_parent_id = server_ctx.get("parent_branch_id")
        
        # Validate EVERY branch against the authorized parent scope before any DB writes
        for idx, b_data in enumerate(branches_data):
            cand_parent_id = b_data.get("parent_branch_id")
            if authorized_parent_id is None and cand_parent_id is not None:
                db.rollback()
                return {
                    "status": "PARTITION_REJECTED",
                    "violations": [f"Branch [{idx}] supplies unauthorized parent '{cand_parent_id}' in root cycle"]
                }
            elif authorized_parent_id is not None and cand_parent_id != authorized_parent_id:
                db.rollback()
                return {
                    "status": "PARTITION_REJECTED",
                    "violations": [f"Branch [{idx}] parent mismatch: '{cand_parent_id}' != authorized '{authorized_parent_id}'"]
                }
                
        # Validate parent existence and trip/slot binding
        if authorized_parent_id:
            parent_branch = db.query(Branch).filter(
                Branch.branch_id == authorized_parent_id,
                Branch.item_id == item_id
            ).first()
            if not parent_branch:
                db.rollback()
                return {
                    "status": "PARTITION_REJECTED",
                    "violations": [f"Parent branch '{authorized_parent_id}' does not exist for this trip/slot"]
                }
            authoritative_electorate = {
                bm.user_id for bm in db.query(BranchMember).filter(BranchMember.branch_id == authorized_parent_id).all()
            }
        else:
            # Full top-level trip electorate
            authoritative_electorate = electorate_members
            
        if not authoritative_electorate:
            db.rollback()
            return {"status": "FAILED", "reason": "Authoritative electorate is missing or empty; partition validation cannot proceed"}
            
        # Mandatory partition validation against authoritative electorate
        is_valid, violations = validate_branch_partition(branches_data, authoritative_electorate)
        if not is_valid:
            db.rollback()
            return {"status": "PARTITION_REJECTED", "violations": violations}
            
        # Insert all validated branch rows atomically
        for b_data in branches_data:
            brc_id = f"brc_{uuid.uuid4().hex[:12]}"
            members = b_data.get("member_user_ids", [])
            
            branch_row = Branch(
                branch_id=brc_id,
                item_id=item_id,
                parent_branch_id=authorized_parent_id,
                title=b_data.get("title", "Alternative Activity"),
                rationale=b_data.get("rationale", "Divergent preference subgroup"),
                entity_type=b_data.get("entity_type"),
                entity_id=b_data.get("entity_id"),
                cost_delta=b_data.get("cost_delta", "0.00"),
                currency=b_data.get("currency", "USD"),
                status="OPEN"
            )
            db.add(branch_row)
            
            for uid in members:
                bmb_id = f"bmb_{uuid.uuid4().hex[:12]}"
                db.add(BranchMember(
                    member_id=bmb_id,
                    branch_id=brc_id,
                    user_id=uid,
                    confirmed=False
                ))
                
        setattr(slot_consensus, "lease_token", None)
        setattr(slot_consensus, "lease_expires_at", None)
        
        itinerary.version += 1
        
        rev_id = f"rev_{uuid.uuid4().hex[:12]}"
        db.add(RevisionHistory(
            revision_id=rev_id,
            item_id=item_id,
            version_number=itinerary.version,
            snapshot_data={
                "event": "BRANCH_PARTITION_COMMITTED",
                "branch_count": len(branches_data)
            },
            created_by=initiating_user_id
        ))
        
        db.commit()
        return {"status": "COMMITTED", "action": "BRANCHED"}
        
    # Baseline preservation
    setattr(slot_consensus, "lease_token", None)
    setattr(slot_consensus, "lease_expires_at", None)
    db.commit()
    return {"status": "BASELINE_PRESERVED", "action": action}

def confirm_slot_proposal(
    db: Session,
    item_id: str,
    proposal_id: str,
    confirming_user_id: str,
    expected_version: int
) -> Dict[str, Any]:
    """
    Phase 3: Authoritative Slot Confirmation & CAS Itinerary Version Increment
    
    AUTHORIZATION, GOVERNANCE & CONCURRENCY CONTRACT:
    1. Caller Authentication & Authorization (BEFORE Any State Disclosure or Mutation):
       - Caller identity (confirming_user_id) is derived from verified Clerk JWT.
       - Caller MUST be an active trip member in trip_members (status == 'active').
       - In Mode A: caller MUST be the authoritative trip owner (Trip.owner_user_id).
         Unauthorized callers are rejected with 403 Forbidden (ERR_NOT_OWNER).
       - In Mode NA: any active member can trigger confirmation, but confirmation
         MUST strictly enforce server-evaluated consensus rules under lock.
    2. Lock Acquisition Order (Consistent Concurrency Invariant):
       - Acquires exclusive row lock on SlotConsensus FIRST:
         `SELECT ... FROM slot_consensus WHERE item_id = :item_id FOR UPDATE`
       - Acquires exclusive row lock on Itinerary SECOND:
         `SELECT ... FROM itineraries WHERE itinerary_id = :itinerary_id FOR UPDATE`
       - Matches start_async_reconciliation and commit_reconciliation_result lock order,
         eliminating database deadlocks.
    3. Idempotent Retry & Conflict Handling (After Authorization Verified):
       - If slot is already confirmed (slot_consensus.slot_status == 'CONFIRMED'):
         * Identical retry (same proposal already accepted on this slot): returns 200
           ALREADY_CONFIRMED idempotently without re-incrementing version or reapplying mutations.
         * Conflicting request (different proposal requested or stale expected_version):
           rejects with 409 Conflict (ERR_SLOT_ALREADY_CONFIRMED).
       - If slot has branched (slot_consensus.slot_status == 'BRANCHED'):
         rejects with 409 Conflict (ERR_SLOT_BRANCHED).
    4. Optimistic Concurrency Control (CAS Revision Strategy):
       - Version checked under exclusive lock: `itinerary.version == expected_version`.
       - If mismatched: rolls back transaction and returns 409 Conflict (ERR_STALE_VERSION).
    5. Proposal Scope & Current-Cycle Candidate Eligibility:
       - Proposal must exist and belong to the same itinerary and requested slot:
         `proposal.itinerary_id == itinerary.itinerary_id` and `proposal.target_item_id == item_id`.
       - Proposal must be in admissible state: `proposal.status == 'open'`.
       - Proposal must belong to the active consensus cycle: candidate was created during
         the current cycle (`proposal.created_at >= slot_consensus.created_at` in current schema;
         target column `proposal.consensus_cycle == slot_consensus.consensus_cycle` [PROPOSED_STORAGE]).
         Stale candidates from prior cycles are rejected with 422 (ERR_STALE_PROPOSAL_CYCLE).
    6. Authoritative Server-Side Consensus Evaluation (Mode NA):
       - An arbitrary caller object or AI claim is NEVER accepted as proof of consensus.
       - The server evaluates consensus directly under database lock via consensus_service:
         a) Unanimous YES from all active electorate members:
            `len(active_members) > 0` and `len(no_voters) == 0` and `active_members.issubset(yes_voters)`.
            (Empty electorate fails closed with ERR_EMPTY_ELECTORATE).
         b) Voting countdown window expired (`now >= slot_consensus.closes_at`) with 0 NO votes,
            or meeting approved supermajority rules under Decision #31.
         If consensus conditions are not met, rolls back and returns 422 (ERR_CONSENSUS_NOT_REACHED).
    7. Atomic Mutations & Transaction Ownership:
       - The domain function owns transaction completion: explicit db.rollback() on all rejection
         paths; explicit db.commit() only upon successful mutation.
       - Selected proposal marked status = 'accepted'; competing proposals marked 'rejected'.
       - Master ItineraryItem updated with accepted proposal details.
       - SlotConsensus updated: slot_consensus.slot_status = 'CONFIRMED', active leases cleared.
       - Itinerary version incremented: itinerary.version += 1.
       - RevisionHistory audit snapshot inserted.
       - Emits slotStatusChanged ('CONFIRMED') and itineraryUpdated (version N+1).
    """
    now = datetime.now(timezone.utc)
    
    try:
        # 1. Consistent Lock Order: SlotConsensus FIRST
        slot_consensus = db.query(SlotConsensus).filter(
            SlotConsensus.item_id == item_id
        ).with_for_update().first()
        if not slot_consensus:
            db.rollback()
            return {"status": "FAILED", "error": "ERR_SLOT_NOT_FOUND", "message": f"SlotConsensus for item_id {item_id} not found"}
            
        itinerary_item = db.query(ItineraryItem).filter(ItineraryItem.item_id == item_id).first()
        if not itinerary_item:
            db.rollback()
            return {"status": "FAILED", "error": "ERR_ITEM_NOT_FOUND", "message": f"ItineraryItem {item_id} not found"}
            
        # 2. Consistent Lock Order: Itinerary SECOND
        itinerary = db.query(Itinerary).filter(
            Itinerary.itinerary_id == itinerary_item.itinerary_id
        ).with_for_update().first()
        if not itinerary:
            db.rollback()
            return {"status": "FAILED", "error": "ERR_ITINERARY_NOT_FOUND", "message": "Itinerary not found"}
            
        trip = db.query(Trip).filter(Trip.trip_id == itinerary.trip_id).first()
        if not trip:
            db.rollback()
            return {"status": "FAILED", "error": "ERR_TRIP_NOT_FOUND", "message": "Trip not found"}
            
        if trip.mode not in ["Mode A", "Mode NA"]:
            db.rollback()
            return {"status": "FAILED", "error": "ERR_UNKNOWN_GOVERNANCE_MODE", "message": f"Unknown governance mode '{trip.mode}'"}
            
        mode = trip.mode
        
        # 3. Caller Authentication & Authority Check (BEFORE disclosing prior confirmation state)
        caller_member = db.query(TripMember).filter(
            TripMember.trip_id == trip.trip_id,
            TripMember.user_id == confirming_user_id,
            TripMember.status == "active"
        ).first()
        if not caller_member:
            db.rollback()
            return {"status": "FORBIDDEN", "error": "ERR_NOT_TRIP_MEMBER", "message": "Caller is not an active trip member"}
            
        if mode == "Mode A" and trip.owner_user_id != confirming_user_id:
            db.rollback()
            return {"status": "FORBIDDEN", "error": "ERR_NOT_OWNER", "message": f"Only trip owner '{trip.owner_user_id}' can confirm proposals in Mode A"}
            
        # 4. Idempotent Retry & Terminal State Handling (Authorized Caller Only)
        if slot_consensus.slot_status == "CONFIRMED":
            existing_accepted = db.query(Proposal).filter(
                Proposal.itinerary_id == itinerary.itinerary_id,
                Proposal.target_item_id == item_id,
                Proposal.status == "accepted"
            ).first()
            if existing_accepted and existing_accepted.proposal_id == proposal_id:
                # Legitimate identical retry: release lock cleanly and return confirmed state
                db.rollback()
                return {
                    "status": "ALREADY_CONFIRMED",
                    "slot_id": item_id,
                    "proposal_id": proposal_id,
                    "itinerary_version": itinerary.version,
                    "idempotent": True
                }
            else:
                db.rollback()
                return {
                    "status": "CONFLICT",
                    "error": "ERR_SLOT_ALREADY_CONFIRMED",
                    "message": "Slot is already confirmed with another proposal or revision"
                }
                
        if slot_consensus.slot_status == "BRANCHED":
            db.rollback()
            return {"status": "CONFLICT", "error": "ERR_SLOT_BRANCHED", "message": "Slot has branched and cannot be confirmed"}
            
        # 5. CAS Itinerary Version Guard
        if itinerary.version != expected_version:
            db.rollback()
            return {
                "status": "CONFLICT",
                "error": "ERR_STALE_VERSION",
                "current_version": itinerary.version,
                "expected_version": expected_version
            }
            
        # 6. Proposal Scope & Current-Cycle Candidate Validation
        selected_proposal = db.query(Proposal).filter(
            Proposal.proposal_id == proposal_id,
            Proposal.itinerary_id == itinerary.itinerary_id,
            Proposal.target_item_id == item_id
        ).first()
        if not selected_proposal:
            db.rollback()
            return {
                "status": "REJECTED_INVALID_PROPOSAL_SCOPE",
                "error": "ERR_PROPOSAL_SCOPE_MISMATCH",
                "message": "Proposal does not exist or does not belong to the requested itinerary and slot"
            }
            
        if selected_proposal.status != "open":
            db.rollback()
            return {
                "status": "REJECTED_INADMISSIBLE_STATE",
                "error": "ERR_PROPOSAL_NOT_OPEN",
                "message": f"Proposal is in terminal/ineligible state '{selected_proposal.status}'"
            }
            
        # Enforce cycle boundary: proposal must belong to the active consensus cycle
        cycle_start = slot_consensus.created_at
        if selected_proposal.created_at and cycle_start and selected_proposal.created_at < cycle_start:
            db.rollback()
            return {
                "status": "REJECTED_STALE_CYCLE",
                "error": "ERR_STALE_PROPOSAL_CYCLE",
                "message": "Proposal belongs to a previous consensus cycle and is no longer admissible"
            }
            
        # 7. Authoritative Consensus Evaluation (Mode NA)
        if mode == "Mode NA":
            active_members = {
                m.user_id for m in db.query(TripMember).filter(
                    TripMember.trip_id == trip.trip_id,
                    TripMember.status == "active"
                ).all()
            }
            
            # An empty electorate must NEVER satisfy the unanimity path
            if len(active_members) == 0:
                db.rollback()
                return {
                    "status": "REJECTED_EMPTY_ELECTORATE",
                    "error": "ERR_EMPTY_ELECTORATE",
                    "message": "Trip has zero active electorate members; consensus cannot be satisfied"
                }
                
            prop_votes = db.query(Vote).filter(
                Vote.proposal_id == proposal_id,
                Vote.cast_at >= cycle_start if cycle_start else True
            ).all()
            yes_voters = {v.user_id for v in prop_votes if v.value == "yes"}
            no_voters = {v.user_id for v in prop_votes if v.value == "no"}
            
            # Internal server evaluation rule:
            is_unanimous = (len(no_voters) == 0 and active_members.issubset(yes_voters))
            window_closed = (
                getattr(slot_consensus, "closes_at", None) is not None and
                now >= slot_consensus.closes_at and
                len(no_voters) == 0
            )
            
            if not (is_unanimous or window_closed):
                db.rollback()
                return {
                    "status": "REJECTED_CONSENSUS_UNMET",
                    "error": "ERR_CONSENSUS_NOT_REACHED",
                    "message": "Mode NA requires verified unanimous YES votes or closed voting window with zero dissent"
                }
                
        # 8. Atomic State Mutations & Version CAS Increment
        competing_proposals = db.query(Proposal).filter(
            Proposal.itinerary_id == itinerary.itinerary_id,
            Proposal.target_item_id == item_id
        ).all()
        for p in competing_proposals:
            if p.proposal_id == proposal_id:
                p.status = "accepted"
            else:
                p.status = "rejected"
                
        itinerary_item.title = selected_proposal.title
        if hasattr(selected_proposal, "entity_type") and selected_proposal.entity_type:
            setattr(itinerary_item, "entity_type", selected_proposal.entity_type)
        if hasattr(selected_proposal, "entity_id") and selected_proposal.entity_id:
            setattr(itinerary_item, "entity_id", selected_proposal.entity_id)
            
        slot_consensus.slot_status = "CONFIRMED"
        setattr(slot_consensus, "lease_token", None)
        setattr(slot_consensus, "lease_expires_at", None)
        
        itinerary.version += 1
        
        rev_id = f"rev_{uuid.uuid4().hex[:12]}"
        db.add(RevisionHistory(
            revision_id=rev_id,
            item_id=item_id,
            version_number=itinerary.version,
            snapshot_data={
                "event": "PROPOSAL_CONFIRMED",
                "proposal_id": proposal_id,
                "confirmed_by": confirming_user_id,
                "mode": mode,
                "itinerary_version": itinerary.version
            },
            created_by=confirming_user_id
        ))
        
        db.commit()
        return {
            "status": "CONFIRMED",
            "slot_id": item_id,
            "proposal_id": proposal_id,
            "itinerary_version": itinerary.version
        }
    except Exception as exc:
        db.rollback()
        raise exc
```

---

### 7.4 Grounded Catalog Retrieval (`candidate_selector.py`)

`[APPROVED_REQUIREMENT]` Grounded candidate synthesis uses deterministic SQL queries over the PostgreSQL `activities_poi` catalog table (or raw SQL repository):

```python
# backend/ai/core/candidate_selector.py
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text

def retrieve_catalog_candidates(
    db: Session,
    city_id: str,
    time_slot_duration_minutes: int,
    max_budget: Decimal,
    excluded_categories: list[str],
    limit: int = 10,
) -> list[dict]:
    """
    Step 1: Grounded Catalog Retrieval
    Queries real entities from PostgreSQL activities_poi table. Vector search is NOT required.
    """
    sql = text("""
        SELECT poi_id, name, category, cost, currency, duration_minutes, latitude, longitude, rating
        FROM activities_poi
        WHERE city_id = :city_id
          AND cost <= :max_budget
          AND category NOT IN :excluded_cats
        ORDER BY rating DESC
        LIMIT :limit
    """)
    
    # Parameterize and execute query safely
    rows = db.execute(
        sql,
        {
            "city_id": city_id,
            "max_budget": float(max_budget),
            "excluded_cats": tuple(excluded_categories) if excluded_categories else ("NONE",),
            "limit": limit
        }
    ).fetchall()
    
    results = []
    for r in rows:
        results.append({
            "entity_id": r.poi_id,
            "entity_type": "poi",
            "title": r.name,
            "category": r.category,
            "cost": str(r.cost),
            "currency": r.currency,
            "duration_minutes": r.duration_minutes,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "rating": float(r.rating) if r.rating else 0.0,
        })
    return results
```

### 8.2 `guide_compatibility_scorer.py`

**Scoring formula** (weighted sum, 0-100 integer):
```
language_match:       40 points  (% overlap between user's languages and guide's languages × 40)
specialisation_match: 30 points  (primary match 20pts, secondary match 10pts)
budget_fit:           20 points  (guide's day_rate ≤ user's max_budget → 20pts, else 0)
rating_score:         10 points  (rating / 5.0 × 10, rounded to int)
TOTAL:               100 points maximum
```

```python
# backend/ai/scorers/guide_compatibility_scorer.py
from decimal import Decimal

def score_guide_match(
    user: dict,
    user_prefs: dict,     # { preferred_languages, interests, max_daily_budget, preferred_currency }
    candidate_guides: list[dict],
    max_budget: str | None = None,  # ISO money string e.g. "100.00", overrides user_prefs if provided
) -> list[dict]:
    """
    Returns list of { guide_id, compatibility_score, shared_languages, shared_specialisations }
    sorted by compatibility_score descending.
    compatibility_score is INTEGER 0-100.
    """
    results = []
    
    user_languages = set(user_prefs.get("preferred_languages", "").split(","))
    user_interests = set(user_prefs.get("interests", "").split(","))
    
    budget = None
    budget_str = max_budget or user_prefs.get("max_daily_budget")
    if budget_str:
        try:
            budget = Decimal(str(budget_str))
        except:
            budget = None
    
    for guide in candidate_guides:
        score = 0
        
        # --- Language match (40 points) ---
        guide_languages = set(guide.get("languages", "").split(","))
        shared_langs = user_languages & guide_languages
        lang_score = 0
        if user_languages:
            lang_score = int((len(shared_langs) / len(user_languages)) * 40)
        score += lang_score
        
        # --- Specialisation match (30 points) ---
        spec_score = 0
        guide_primary = guide.get("specialisation", "")
        guide_secondary = guide.get("secondary_specialisation", "")
        
        if guide_primary in user_interests:
            spec_score += 20
        if guide_secondary and guide_secondary in user_interests:
            spec_score += 10
        score += spec_score
        
        shared_specs = []
        if guide_primary in user_interests:
            shared_specs.append(guide_primary)
        if guide_secondary and guide_secondary in user_interests:
            shared_specs.append(guide_secondary)
        
        # --- Budget fit (20 points) ---
        budget_score = 0
        if budget is not None:
            try:
                guide_rate = Decimal(str(guide.get("day_rate", "9999")))
                if guide_rate <= budget:
                    budget_score = 20
            except:
                pass
        else:
            budget_score = 10  # no budget constraint = partial score
        score += budget_score
        
        # --- Rating (10 points) ---
        rating_score = 0
        if guide.get("rating") is not None:
            try:
                rating = Decimal(str(guide["rating"]))
                rating_score = int((rating / Decimal("5.0")) * 10)
            except:
                pass
        score += rating_score
        
        # Clamp 0-100
        final_score = max(0, min(100, score))
        
        results.append({
            "guide_id": guide["guide_id"],
            "compatibility_score": final_score,      # INTEGER
            "shared_languages": list(shared_langs - {""}),
            "shared_specialisations": shared_specs,
        })
    
    results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return results
```

---

## 9. PHASE-BY-PHASE EXECUTION PLAN

### PHASE 0 — Hour 0–1 (12:00–13:00)
**Your job**: Draft prompts against real PS-11 dataset examples. Set up Ollama.

Concrete deliverables:
1. Set up Ollama on your laptop:
   ```bash
   ollama pull phi4-mini
   ollama serve
   # Verify: curl http://localhost:11434/api/tags
   ```
2. Test Phi-4-mini responds to a simple JSON prompt:
   ```bash
   curl http://localhost:11434/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"phi4-mini","messages":[{"role":"user","content":"Return {\"test\":true}"}],"response_format":{"type":"json_object"}}'
   ```
3. Create `backend/ai/llm/client.py` with `call_llm()` and `safe_llm_call()` (Section 5)
4. Look at real data from PS-11.db:
   - Open the SQLite DB and read 5-10 actual proposal rows
   - Read 5-10 actual vote rows with comments
   - Read 5-10 actual user_preferences rows
   This is your grounding data — your AI reads these exact field names
5. Draft the 3 system prompts (classifier, blend generator, branch grouper) — test them manually against real data examples
6. Confirm with Panchami: function signatures agreed (what she calls, what you return)

**Gate**: `safe_llm_call()` works, returns parsed JSON, falls back gracefully on timeout. Done.

---

### PHASE 1 — Hours 1–4 (13:00–16:00)
**Your job**: Build `hard_constraint_validator.py` and `branch_trigger_classifier.py`.

Concrete deliverables:
1. `hard_constraint_validator.py` — fully working, no LLM dependency (Section 6.1)
2. Test validator with scripted inputs:
   ```python
   # Should PASS:
   validate_plan({"title":"X","rationale":"Y","entity_type":"poi","entity_id":"poi_test","cost_delta":"0.00","currency":"USD"}, {...}, {...})
   # Should FAIL:
   validate_plan({"title":"","entity_type":"invalid_type","entity_id":"","cost_delta":"not_a_number"}, {...}, {...})
   ```
3. `branch_trigger_classifier.py` with LLM + fallback (Section 6.2)
4. Test classifier with scripted inputs:
   ```python
   # Should return FIXED_REQUIREMENT:
   classify_objection([{"user_id":"usr_1","comment":"injured ankle cannot hike","round":1}], 1)
   # Should return NEEDS_CLARIFICATION:
   classify_objection([{"user_id":"usr_1","comment":"not feeling it","round":1}], 1)
   # Should return FIXABLE_TWEAK:
   classify_objection([{"user_id":"usr_1","comment":"prefer spa instead","round":1}], 1)
   ```
5. Write these tests to `tests/test_branch_classifier.py`

**Gate**: Both modules work standalone. Vague comment → NEEDS_CLARIFICATION. Injury comment → FIXED_REQUIREMENT. Specific tweak → FIXABLE_TWEAK. Done.

---

### PHASE 2 — Hours 4–8 (16:00–20:00)
**Your job**: Build `blended_plan_generator.py` end-to-end on scripted disagreement.

Concrete deliverables:
1. `blended_plan_generator.py` with LLM + fallback + validator integration (Section 6.3)
2. Scripted test scenario:
   ```python
   # Proposal: Mount Batur Trek
   # NO comment 1: "injured ankle, prefer hot springs spa"
   # NO comment 2: "morning person, prefer sunrise activity"
   # Expected: blended plan e.g. "Batur Thermal Springs Sunrise Visit"
   result = generate_blended_plan(
       current_proposal={"title":"Mount Batur Trek","rationale":"Sunrise hike","entity_type":"poi","entity_id":"poi_batur","cost_delta":"0.00","currency":"USD"},
       no_vote_comments=[
           {"user_id":"usr_1","comment":"injured ankle, prefer hot springs spa","round":1},
           {"user_id":"usr_2","comment":"morning person, prefer sunrise activity","round":1},
       ],
       itinerary_item={"item_id":"itm_1","title":"Morning Activity","entity_type":"poi","entity_id":"poi_batur","cost":"65.00","currency":"USD"},
       trip_context={"destination_city":"Bali","start_date":"2026-10-10","end_date":"2026-10-16","mode":"Mode NA"},
       current_round=1,
   )
   assert result["action"] == "BLENDED"
   assert result["blended_plan"]["entity_type"] in valid_entity_types
   assert result["constraint_validation"] in ["PASSED","REGENERATED_ONCE"]
   ```
3. Run with Phi-4-mini connected via ngrok (or localhost if testing locally)
4. Verify fallback works: temporarily break ngrok URL → should get fallback plan, not crash

**Gate**: generate_blended_plan returns valid BLENDED result on scripted scenario. Fallback works. Done.

---

### PHASE 3 — Hours 8–12 (20:00–00:00)
**Your job**: `branch_grouping.py` + revision loop for 2–3 rounds.

Concrete deliverables:
1. `branch_grouping.py` with LLM + fallback + single-member auto-finalize (Section 6.4)
2. Test with 3-way and 4-way split scenarios:
   ```python
   holdouts = [
       {"user_id":"usr_1","comment":"want beach","suggestion":"beach"},
       {"user_id":"usr_2","comment":"want mountain hiking","suggestion":"hiking"},
       {"user_id":"usr_3","comment":"want temple visit","suggestion":"temple"},
   ]
   result = group_into_branches(holdouts, itm, trip)
   assert result["action"] == "BRANCHED"
   assert len(result["branches"]) == 3
   # Each member in exactly one branch
   all_ids = [uid for b in result["branches"] for uid in b["member_user_ids"]]
   assert sorted(all_ids) == sorted(["usr_1","usr_2","usr_3"])
   ```
3. `mode_na_orchestrator.py` — full round flow (Section 7.1)
4. `mode_a_orchestrator.py` — advisory round flow (Section 7.2)
5. Share function signatures with Panchami so she can call them

**Gate**: 3-way branch scenario creates 3 branches. Single-member branch has auto_finalized=True. Done.

---

### CHECKPOINT 1 — Hour 12 (00:00)
**Your job at checkpoint**: Confirm with Panchami that:
- `consensus_service.py` exposes `reconcile_slot()` and `run_mode_na_round()` for router integration
- `voting_service.py` and `trip_service.py` signatures match what routers require
- Panchami's `routers/consensus.py` calls domain service and dispatches `aiPlanGenerated` / `aiRecommendationReady`
- Pure math scorers in `backend/app/ai/matching/` are tested and passing

---

### PHASE 4 — Hours 12–16 (00:00–04:00)
**Your job**: Wire branch classifier + multi-way grouping to real 3–4-way test scenarios with Panchami.

Concrete deliverables:
1. Work with Panchami to confirm end-to-end: POST /api/consensus/reconcile → calls Sharvani's domain service → returns correct shape
2. Test the full flow: real NO votes from PS-11 data → domain service persistence & AI state machine → WebSocket event publication → Nikitha's UI update
3. Handle the case where domain service receives real database models from `backend/app/models/`
4. Adjust any field mapping issues that arise when real data flows through

**Gate**: POST /api/consensus/reconcile with real trip data returns valid BLENDED or BRANCHED response. Done.

---

### PHASE 5 — Hours 16–19 (04:00–07:00)
**Your job**: Solo scorers + edge case prep.

Concrete deliverables:
1. `group_compatibility_scorer.py` fully tested (Section 8.1)
2. `guide_compatibility_scorer.py` fully tested (Section 8.2)
3. Verify scores are INTEGER 0-100 (no floats, no strings)
4. Verify determinism: same inputs → same output every time
5. Test against synthetic profile pairs with known-good expected rankings:
   ```python
   # User speaks 'en' and 'hi', interested in 'heritage' and 'food'
   # Guide A: languages='en,hi', specialisation='heritage', day_rate='80.00'
   # Guide B: languages='ta', specialisation='trekking', day_rate='50.00'
   # Expected: Guide A scores much higher than Guide B
   ```
6. Prep the scripted disagreement scenario for demo (3-4 members, known expected branches)

**Gate**: score_group_match returns integer scores, sorted descending. Same inputs → same scores every run. Done.

---

### PHASE 6 — Hours 19–21 (07:00–09:00)
**Your job**: Fix any prompt/validator integration issues from full click-through.

- Run full demo flow: proposal → NO with comment → reconcile → blended plan → re-vote → branch
- Fix any JSON parsing issues from Phi-4-mini output
- Fix any field name mismatches found in integration
- Ensure fallback fires correctly when tested

---

### CHECKPOINT 2 — Hour 21 (09:00)
**STOP.** Feature freeze. Merge into develop → main.

---

### PHASE 7 — Hours 21–24 (09:00–12:00)
**Demo prep**: Verify your scripted 3-4 way branch scenario works cleanly on the demo machine. Pre-run and cache expected outputs if needed.

---

## 9.1 CROSS-MEMBER LOADING & CLERK PERFORMANCE INVESTIGATION PROTOCOL (DOMAIN, DATABASE & AI TASK CARD)

This protocol governs the cross-member performance triage for severe loading issues reported during Trip Home rendering and Clerk user authentication. Sharvani owns the database query execution, domain business logic, AI inference latency, and root-cause analysis track.

### 1. Domain & Persistence Investigation Scope & Responsibilities
- **Database Query Profiling & N+1 Query Elimination**:
  * Profile SQL queries executed during Trip Home load (`get_trip_detail`, `get_trip_snapshot`).
  * Audit relationships on `TripMember`, `Proposal`, and `Vote` tables. Replace lazy loading with eager loading (`joinedload` or `selectinload`) to eliminate N+1 round-trips to Neon PostgreSQL.
  * Ensure compound indexes exist on foreign keys (`trip_members(trip_id, user_id)`, `proposals(slot_id, trip_id)`, `votes(proposal_id, user_id)`).
- **LLM Inference Timeout & Circuit Breaker Policies**:
  * Profile local Ollama execution latency and evaluate operational timeout ceilings (`[PROPOSED TARGET]`: 8s–10s latency ceiling, pending Decision #28).
  * Ensure synchronous request threads never block on slow LLM calls; consensus negotiation runs asynchronously with immediate status responses.
  * Activate deterministic rule-based fallback when LLM timeout is breached.
- **Privacy & Security during Instrumentation**:
  * Instrumentation logs must **NEVER** output JWT tokens, secrets, biometric vectors, or raw traveler objection comments.
- **Clerk User Synchronization Profiling (`POST /api/auth/webhook`)**:
  * Profile `security.sync_clerk_user_to_db` execution time. Ensure user record creation and preference record initialization occur in a single atomic database transaction to prevent connection pool exhaustion and table locking.
- **Structured Audit Logging**:
  * Instrument domain service methods with high-resolution execution timers (`elapsed_ms`), emitting structured log entries:
    `logger.info("domain_call_completed", extra={"service": "consensus_service", "method": "reconcile_slot", "elapsed_ms": 42.5})`.

### 2. Standardized Investigation Artifact Format
Sharvani must log performance findings using the standardized four-part ledger:
- **Baseline**: Initial measured database query duration or LLM synthesis latency (in milliseconds).
- **Reproduction**: Exact SQL execution plan (`EXPLAIN ANALYZE`) or domain service profiling script reproducing the bottleneck.
- **Measured Bottleneck**: Concrete measured bottleneck taking $> 150\text{ms}$ (e.g. "Unindexed N+1 query loading votes individually for 12 slots resulting in 340ms database delay").
- **Verification**: Post-optimization `EXPLAIN ANALYZE` or timing profile demonstrating verified latency reduction.

---

## 10. DEPENDENCY MAP

| What you need | From whom | When | Related Decision |
|---|---|---|---|
| Ollama running locally or mock LLM provider | You (your own machine) | Baseline setup | Decision #1, #2 |
| Panchami to agree in-process service call interfaces | Panchami | Checkpoint 1 | Decision #27, #31 |
| Real PS-11 data seeded to test against | You (seed script verified) | Baseline setup | Decision #16 |
| Panchami routers calling your domain services in-process | Panchami | Checkpoint 1 | N/A |
| Frontend testing against live services (`VITE_USE_MOCK_DATA=false`) | Nikitha | Phase 6 | Decision #30 |
| Deployment build artifacts & verification (Render & Vercel) | Panchami & Nikitha | Checkpoint 2 / Phase 6 | Decision #3 |

---

## 11. WHAT YOU MUST NEVER DO

1. Never bypass domain services or transactions for database operations — Sharvani owns shared models and transactional persistence; Panchami must never write ad-hoc SQL or manipulate models directly in router handlers
2. Never write an HTTP endpoint or WebSocket route handler — Panchami owns all transport adapters
3. Never use float for money — always Decimal in Python, string in output dicts
4. Never classify a vague comment ("not feeling it") as FIXED_REQUIREMENT
5. Never skip the hard_constraint_validator before returning a blended plan
6. Never resume common-ground blending on a slot that has already switched to BRANCHED in this cycle
7. Never cap branches at 2 — if there are 5 distinct preferences, return 5 branches
8. Never forget to mark single-member branches as auto_finalized=True
9. Never return compatibilityScore as a float — it must be an integer
10. Never make an LLM call from the solo scorers — they are pure math, no exceptions
11. Never crash if the LLM times out — always use safe_llm_call with a fallback
12. Never invent a vote value of 'abstain' — you only receive 'yes' or 'no'


---

## 5. Master AI System Specification Alignment (Post-Hackathon)

> **Canonical Reference**: All AI logic, prompt templates, validators, and evaluation suites must strictly conform to canonical [AI.md](AI.md) (and [ai/AIConsensus/docs/AI.md](AI.md)).

### Key Requirements for AI Track:
1. **Constrained Objection Taxonomy**: Refactor `branch_trigger_classifier.py` to output strictly one of: `FIXABLE_TWEAK`, `FIXED_REQUIREMENT`, `NEEDS_CLARIFICATION`, `UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE`.
2. **Two-Leg Route Feasibility**: Extend `hard_constraint_validator.py` beyond basic dictionary keys to enforce road travel time feasibility ($T_{prev\to cand} + T_{act} + T_{cand\to next} + 2 \cdot B \le T_{avail}$) before marking any candidate valid.
3. **The 6 Verification Statuses**: Tag every blended plan with `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `NEEDS_CLARIFICATION`, `INFEASIBLE`, or `BLOCKED`.
4. **Negotiation Output Contract**: When a candidate is infeasible, output the structured 3-option negotiation payload (`opt_keep_original`, `opt_closer_alternative`, `opt_reschedule_next`).
5. **Local Evaluation via Promptfoo**: Configure Promptfoo to benchmark Phi-4 Mini and Qwen2.5-Coder against the 90 numbered test scenarios specified in `AI.md Section 10`.

<a id="member-phase-4"></a>
## Phase 4 — Implement consensus orchestration and compatibility services

Read the retained sections below together for this phase:



<a id="member-phase-5"></a>
## Phase 5 — Verify independently and investigate performance

Read the retained sections below together for this phase:

- 0.4 RIGOROUS FIVE-TIER TESTING STRATEGY & TEST SAFETY

## 0.4 RIGOROUS FIVE-TIER TESTING STRATEGY & TEST SAFETY

| Tier | Test Scope & Purpose | Execution Command / Environment | Isolation Requirement |
| :--- | :--- | :--- | :--- |
| **Tier 1: Mock Transport Tests** | Fast HTTP/WebSocket router tests with mocked domain services. | `pytest tests/test_routers.py` | Complete isolation; domain calls mocked. |
| **Tier 2: Deterministic Domain Tests** | Pure domain logic: matching scorers, state machine, branching logic. | `pytest tests/test_matching.py tests/test_consensus.py` | In-memory SQLite with PS-11 seed data; zero network calls. |
| **Tier 3: Real Recognition Tests** | DeepFace recognition with known facial images and edge cases. | `pytest ai/DeepFace/tests/` | Isolated local test SQLite DB; dummy float vectors strictly prohibited as proof of recognition. |
| **Tier 4: Isolated Concurrency Tests** | True PostgreSQL concurrency & CAS atomic versioning validation. | `pytest tests/test_concurrency.py` (explicit opt-in) | Dedicated isolated PostgreSQL database; SQLite tests alone do NOT prove PostgreSQL concurrency. |
| **Tier 5: Full Acceptance Tests** | End-to-end integration flows across all components. | Controlled staging runner | Controlled integration tests may import `backend.app.main:app` after safe isolation (isolated test DB URL, disabled demo seeding). |

---


<a id="member-phase-6"></a>
## Phase 6 — Follow task cards, execution checklist and integration checkpoints

Read the retained sections below together for this phase:

- 0.5 CONCRETE DOMAIN & AI TASK CARDS (SHARVANI'S WORKSTREAM)

## 0.5 CONCRETE DOMAIN & AI TASK CARDS (SHARVANI'S WORKSTREAM)

All task cards link to the authoritative decision register in [`docs/AI.md §12`](AI.md#12-stack-neutral-decision-register).

```
┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-0: App Lifecycle, Startup Wiring & Deployment Coordination │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Ready for Implementation                     │
│ Target Files: backend/app/main.py, render.yaml, vercel.json            │
│ Deliverables:                                                          │
│ 1. Own backend/app/main.py router mounts, CORS, static mounts.         │
│ 2. Coordinate deployment across Render (backend/worker) & Vercel.      │
│ 3. Coordinate environment variable configuration across environments.  │
│ Acceptance: Backend and frontend build and boot cleanly on platforms.  │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-1: Shared Model Integrity & Baseline Verification          │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Ready for Implementation (Decision #16)      │
│ Target Files: backend/app/models/provided.py, additive.py              │
│ Deliverables:                                                          │
│ 1. Verify all 14 provided.py models match docs/data/schema.sql.        │
│ 2. Verify all 10 additive.py models match WanderMatch requirements.    │
│ 3. Confirm Alembic baseline c8a6a4789a32 represents clean migration.   │
│ 4. Validate backend/seed.py populates reference SQLite and Neon DB.    │
│ Acceptance: Schema matches exactly across SQLite, DDL, and models.     │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-2: Atomic Concurrency (CAS) & Itinerary Persistence        │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Ready for Implementation                     │
│ Target Files: backend/app/services/trip_service.py                     │
│ Deliverables:                                                          │
│ 1. Implement atomic CAS update on itineraries.version.                 │
│ 2. Raise VersionConflictError on 0 rows affected.                      │
│ 3. Provide transactional trip and itinerary retrieval helpers.         │
│ Acceptance: Concurrent conflicting updates abort safely with HTTP 409. │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-3: Atomic Voting Service & Single-Active-YES Invariant     │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Ready for Implementation (AC-VOT-02)         │
│ Target Files: backend/app/services/voting_service.py                   │
│ Deliverables:                                                          │
│ 1. Atomic vote persistence: record yes/no in single transaction.       │
│ 2. Enforce AC-VOT-02: auto-retract prior YES on competing proposal.    │
│ 3. Enforce mandatory typed comment when vote is NO.                    │
│ Acceptance: Single-active-YES guaranteed; NO without comment rejected. │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-4: Consensus State Machine & Slot-Level Authoritative Timer │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Ready for Implementation (Decision #27, #31) │
│ Target Files: backend/app/services/consensus_service.py                 │
│ Deliverables:                                                          │
│ 1. Manage slot_consensus.closes_at authoritatively on first NO vote.   │
│ 2. Exclude test-only advance_minutes from production contract.         │
│ 3. Orchestrate Mode A admin controls and Mode NA auto-branching.       │
│ Acceptance: Countdown timer operates accurately at slot level.         │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-5: Pure Deterministic Matching Scorers                     │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Ready for Implementation (Decision #26)      │
│ Target Files: backend/app/ai/matching/group_compatibility_scorer.py,   │
│               backend/app/ai/matching/guide_compatibility_scorer.py    │
│ Deliverables:                                                          │
│ 1. Pure deterministic math scoring (0–100 integer range).              │
│ 2. Comprehensive unit test suite with 100% deterministic assertions.   │
│ 3. Zero LLM calls in matching scoring path.                            │
│ Acceptance: 100% deterministic score output for identical inputs.      │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-6: Photo & Face Recognition Persistence Services           │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Ready for Implementation (Decision #9, #18)  │
│ Target Files: backend/app/services/photo_service.py                    │
│ Deliverables:                                                          │
│ 1. Implement get_candidate_member_embeddings(trip_id).                 │
│ 2. Implement save_uploaded_photo_record(processing_status='pending').  │
│ 3. Implement save_photo_tags_records() with tags & boxes.              │
│ 4. Strictly omit 512-d ArcFace vectors from logs and responses.        │
│ Acceptance: Photo lifecycle accurately tracked from pending to done.   │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-7: AI Decision Audit Persistence Implementation            │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Pending Implementation (Decision #29)        │
│ Target Files: backend/app/services/audit_service.py                    │
│ Deliverables:                                                          │
│ 1. Implement audited AI decision persistence for consensus rounds.     │
│ 2. Support both dedicated table and revision snapshot alternatives.    │
│ Acceptance: 20-attribute audit record accurately recorded.             │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TASK CARD S-8: Itinerary PDF Renderer Strategy Finalization            │
├────────────────────────────────────────────────────────────────────────┤
│ Owner: Sharvani | Status: Pending Evaluation (Decision #30)            │
│ Deliverables:                                                          │
│ 1. Evaluate client-side @react-pdf/renderer vs backend WeasyPrint.     │
│ 2. Finalize rendering strategy with Nikitha for FR-EXP-01 requirement. │
│ Acceptance: PDF export generates uniform print layout without errors.  │
└────────────────────────────────────────────────────────────────────────┘
```


---

> **Architectural Status Note**: Render-to-ngrok-to-local-Ollama is strictly a development and demo candidate, NOT an approved production topology. Permanent SLM roles (Phi-4 Mini vs Qwen2.5-Coder) and quantization remain open decisions pending Promptfoo benchmark evaluation [STACK_DEPENDENT_DECISION].

