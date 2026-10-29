# WanderMatch — Shared Integration Contract & Master Ownership Ledger

**Document Authority**: Sharvani G Bhaskar (Final Integration, Architecture & Deployment Owner)  
**Status**: Authoritative Shared Contract (`[SYSTEM OF RECORD]`)  
**Authoritative Decision Register**: [`docs/AI.md §12`](AI.md#12-stack-neutral-decision-register)  
**Applicability**: Nikitha (Frontend), Panchami (Transport & DeepFace), Sharvani (Domain, AI & Integration)

---

## 1. Master System Ownership & Operating Principles

1. **Three-Person Active Team**:
   - **Nikitha M N**: Sole owner of frontend implementation (`frontend/`), all 24 UI components, 19 screens, 4 custom hooks, UI state, accessibility (WCAG 2.1 AA), client data-access adapters, and client-side form validation.
   - **Panchami P**: Sole owner of the transport layer (FastAPI HTTP route definitions, Pydantic wire validation schemas, WebSocket connection lifecycle/broadcast), backend photo adapter, and the complete DeepFace face recognition microservice (`ai/DeepFace/`). Calls Sharvani's domain persistence services in-process.
   - **Sharvani G Bhaskar**: Sole authority for system architecture, `backend/app/main.py`, shared startup wiring, all deployment coordination (including frontend deployment to Vercel and backend/worker deployment to Render), core domain services, shared database models, Alembic migrations, database transactions, cryptographic security verification, authorization rules, consensus state machines, AI modules, and final integrated acceptance.

2. **Main Document Governance**:
   - Following this consistency pass, **each member edits only her own main document**:
     - Nikitha solely edits `docs/NIKITHA.md`.
     - Panchami solely edits `docs/PANCHAMI.md`.
     - Sharvani solely edits `docs/SHARVANI.md`.
   - Sharvani solely edits and maintains this shared contract (`docs/INTEGRATION_CONTRACT.md`).
   - Any cross-boundary contract modification must be requested through a structured handoff proposal.

3. **Separation of Structural Preparation from Feature Implementation**:
   - Structural preparation establishes clean interfaces, documentation, and decoupled module boundaries.
   - Feature changes (such as live LLM calls, WebSocket client token query parameters, atomic database CAS, server-side timer recovery, and PDF export rendering engine) are strictly assigned to later implementation phases.
   - **Pending Decision Principle**: Unresolved decisions in `docs/AI.md §12` block only dependent choices (e.g. renderer selection for PDF), not all implementation (e.g. PDF export requirement is locked; data preparation and UI triggers proceed).

---

## 2. Complete File & Path Ownership Ledger

Every file and directory path across the workspace is accounted for below and explicitly classified:
- `[CURRENT]`: Verified to exist on disk at the verified location.
- `[PROPOSED]`: Target file or directory planned for future extraction or feature implementation. Does not exist on disk today; must not be created during documentation phases.
- `[HISTORICAL]`: Referenced in legacy specifications or prototypes; does not exist in the active service tree or has been superseded.

Untracked personal secret files (`.env`, `backend/.env`, `frontend/.env`) are strictly excluded from shared editing.

| File / Directory Path | Classification | Owner | Purpose & Contents | Boundary Rules |
| :--- | :---: | :---: | :--- | :--- |
| **Frontend Configuration & Assets** | | | | |
| `frontend/package.json` | `[CURRENT]` | **Nikitha** | Node package manifest, scripts | Nikitha manages client dependencies. |
| `frontend/package-lock.json` | `[CURRENT]` | **Nikitha** | Dependency lockfile | Committed with `package.json`. |
| `frontend/vite.config.ts` | `[CURRENT]` | **Nikitha** | Vite dev & build configuration | Port 5173, dev proxy rules. |
| `frontend/tailwind.config.ts` | `[CURRENT]` | **Nikitha** | Tailwind v4 palette & theme | HSL palette and design tokens. |
| `frontend/tsconfig*.json` (3 files)| `[CURRENT]` | **Nikitha** | TypeScript compiler configs | Strict type checking rules. |
| `frontend/.oxlintrc.json` | `[CURRENT]` | **Nikitha** | Oxlint configuration | Static linting rules. |
| `frontend/index.html` | `[CURRENT]` | **Nikitha** | HTML entry point | Mounts root DOM element & Google Fonts. |
| `frontend/public/*` (2 files) | `[CURRENT]` | **Nikitha** | Public assets (`favicon.svg`, `icons.svg`)| Browser static assets. |
| `frontend/src/assets/*` (3 files) | `[CURRENT]` | **Nikitha** | Bundled assets (`hero.png`, `react.svg`, `vite.svg`)| Static images and illustrations. Note: `logo.svg` does NOT exist. |
| `frontend/.env.example` | `[CURRENT]` | **Nikitha** | Frontend env template | Documents `VITE_*` variable names. |
| **Frontend Source (`frontend/src/`)** | | | | |
| `frontend/src/main.tsx` | `[CURRENT]` | **Nikitha** | React DOM initialization | Mounts `<App />` root. |
| `frontend/src/App.tsx` | `[CURRENT]` | **Nikitha** | Route definitions & auth gates | Connects routes to screens. |
| `frontend/src/App.css`, `index.css` | `[CURRENT]` | **Nikitha** | Global CSS & Tailwind directives | Base styling. |
| `frontend/src/hooks/*` (4 files) | `[CURRENT]` | **Nikitha** | Reusable UI state hooks | `useTrip`, `useProposals`, `useVotes`, `useSoloMatch`. |
| `frontend/src/components/*` (24 files)| `[CURRENT]`| **Nikitha**| 24 component source files verified on disk | Verified: chat (3), face (2), itinerary (5: `BranchTabs`, `ConflictResolutionPanel`, `ProposalCard`, `RouteLine`, `SlotCard`), layout (4: `GlobalTopHeader`, `PageWrapper`, `SidebarNav`, `TopNav`), solo (2: `CompatibilityCard`, `GuideCard`), ui (8: `Button`, `EmptyState`, `Input`, `Modal`, `StatusPill`, `SuggestionChip`, `Toast`, `VotePill`). Note: `Footer`, `Navbar`, `Badge`, `Card` do NOT exist. |
| `frontend/src/screens/*` (19 files) | `[CURRENT]` | **Nikitha** | 19 application screen views verified on disk | Verified: `AccountScreen`, `AuditHistoryScreen`, `BranchViewScreen`, `ConflictResolutionPanel`, `CreateTripScreen`, `LoginScreen`, `MemoriesScreen`, `MyTripsScreen`, `OnboardingScreen`, `PhotosScreen`, `ProposeActivityModal`, `ResolvedItineraryScreen`, `SignUpScreen`, `SoloMatchScreen`, `SoloOrGroupDecisionScreen`, `TripChatScreen`, `TripHomeScreen`, `TripPreviewScreen`, `VoteModal`. |
| `frontend/src/types/*` (6 files) | `[CURRENT]` | **Nikitha** | TypeScript wire models | Aligned with backend Pydantic schemas. |
| `frontend/src/context/AuthContext.tsx`| `[CURRENT]`| **Nikitha** | Client auth state & Clerk wrapper | Obtains token for API requests. |
| `frontend/src/context/TripContext.tsx`| `[CURRENT]`| **Nikitha** | Trip state, WS listener, toasts | Receives serialized WebSocket events. |
| `frontend/src/lib/api.ts` | `[CURRENT]` | **Nikitha** | Client HTTP fetch wrapper | Calls backend REST endpoints. |
| `frontend/src/lib/websocket.ts` | `[CURRENT]` | **Nikitha** | Client WebSocket initiator | Connects to `/ws/trips/{id}/{user}`. |
| `frontend/src/lib/data-access/client.ts` | `[PROPOSED]`| **Nikitha**| Data-access interface contract | Decouples components from network. |
| `frontend/src/lib/data-access/mock_adapter.ts` | `[PROPOSED]`| **Nikitha**| In-memory scenario fixtures | Offline scenario testing. |
| `frontend/src/lib/data-access/real_adapter.ts` | `[PROPOSED]`| **Nikitha**| Live FastAPI HTTP/WS adapter | Production transport client. |
| **Backend Configuration & Setup** | | | | |
| `backend/requirements.txt` | `[CURRENT]` | **Sharvani** | Python dependencies manifest | Sharvani solely updates dependencies. |
| `backend/alembic.ini` | `[CURRENT]` | **Sharvani** | Alembic CLI config | Manages database migrations. |
| `backend/alembic/*` (4 files) | `[CURRENT]` | **Sharvani** | Migration env & baseline revision| Authoritative baseline revision `c8a6a4789a32_initial_schema_baseline.py`. |
| `backend/seed.py` | `[CURRENT]` | **Sharvani** | PS-11 database seed script | Populates PostgreSQL/SQLite from PS-11.db. |
| `backend/migrate_mode.py` | `[CURRENT]` | **Sharvani** | Ad-hoc SQLite migration script | Retained as historical tool. |
| `backend/wandermatch.db` | `[CURRENT]` | **Sharvani** | Local SQLite runtime database | Local dev database file. |
| `backend/.env.example` | `[CURRENT]` | **Sharvani** | Backend env template | Authoritative backend env keys. |
| **Backend Application (`backend/app/`)** | | | | |
| `backend/app/__init__.py` | `[CURRENT]` | **Sharvani** | Package marker | Standard package init. |
| `backend/app/main.py` | `[CURRENT]` | **Sharvani** | App init, startup wiring, router mounts | Sharvani owns app lifecycle & mounting. |
| `backend/app/database.py` | `[CURRENT]` | **Sharvani** | SQLAlchemy engine & SessionLocal | Database connection and connection pool. |
| `backend/app/websocket_manager.py` | `[CURRENT]` | **Panchami** | WebSocket connection lifecycle | Manages active rooms, connections, broadcasts. |
| `backend/app/models/__init__.py` | `[CURRENT]` | **Sharvani** | Model registry | Exposes ORM models to Alembic. |
| `backend/app/models/provided.py` | `[CURRENT]` | **Sharvani** | Canonical PS-11 tables D1–D9 | Immutable shared schema contract. |
| `backend/app/models/additive.py` | `[CURRENT]` | **Sharvani** | 10 additive tables verified on disk | Verified models: `JoinRequest`, `SlotConsensus`, `Branch`, `BranchMember`, `RevisionHistory`, `TripChatMessage`, `FaceProfile`, `Photo`, `PhotoPerson` (table `photo_person`), `TripInviteCode`. (Note: `photo_tags` does NOT exist). Prerequisite: `slot_consensus.closes_at` missing in current schema. |
| `backend/app/schemas/*` (3 files: `user.py`, `trip.py`, `matching.py`) | `[CURRENT]` | **Panchami** | Pydantic wire models | Validates HTTP request/response payloads. |
| `backend/app/routers/auth.py` | `[CURRENT]` | **Panchami** | Auth & webhook route handlers | Mounts `POST /api/auth/webhook`, calls Sharvani. |
| `backend/app/routers/trips.py` | `[CURRENT]` | **Panchami** | Trip & chat route definitions | HTTP transport; delegates to Sharvani service. |
| `backend/app/routers/consensus.py` | `[CURRENT]` | **Panchami** | Consensus & voting route handlers| Mounts `/proposals`, `/votes`, `/proposals/check-timer`. |
| `backend/app/routers/matching.py` | `[CURRENT]` | **Panchami** | Matchmaking route definitions | HTTP transport; calls Sharvani scorers. |
| `backend/app/routers/photos.py` | `[CURRENT]` | **Panchami** | Photo upload & Memories routes | Mounts `POST /api/photos`, calls Sharvani & worker.|
| `backend/app/routers/face.py` | `[CURRENT]` | **Panchami** | Face registration transport | Forwards registration payload. |
| `backend/app/services/` | `[CURRENT]` | **Sharvani** | Domain service package directory | Contains `__init__.py` and `clerk_auth.py`. |
| `backend/app/services/clerk_auth.py` | `[CURRENT]` | **Sharvani** | Token verification & provisioning | Auth dependency applied by Panchami's routes. |
| `backend/app/ai/matching/*` (2 files) | `[CURRENT]`| **Sharvani** | Jaccard & cosine scoring math | Canonical deterministic scoring algorithms. |
| `backend/app/utils/*` (3 files) | `[CURRENT]` | **Sharvani** | ID generation, time, money | Shared utility helpers. |
| `backend/static/uploads/` | `[CURRENT]` | **Panchami** | Local photo storage directory | Verified disk path: `backend/static/uploads/` (NOT `backend/app/static/uploads/`). |
| `backend/app/services/trip_service.py` | `[PROPOSED]`| **Sharvani**| Trip lifecycle & CAS concurrency | Domain service extraction. |
| `backend/app/services/voting_service.py` | `[PROPOSED]`| **Sharvani**| Atomic votes & YES retraction | Domain service extraction. |
| `backend/app/services/consensus_service.py`| `[PROPOSED]`| **Sharvani**| Slot timer & Mode A/NA engine | Domain service extraction. |
| `backend/app/services/matching_service.py`| `[PROPOSED]`| **Sharvani**| Solo/guide matching orchestrator | Domain service extraction. |
| `backend/app/services/photo_service.py` | `[PROPOSED]`| **Sharvani**| Photo & face-tag persistence | Domain service extraction. |
| `backend/app/services/audit_service.py` | `[PROPOSED]`| **Sharvani**| Audited AI decision persistence | Domain service extraction (Decision #29). |
| `backend/app/core/security.py` | `[PROPOSED]`| **Sharvani**| Clerk JWT & Svix verification | Domain security extraction. |
| `backend/ai/` | `[HISTORICAL]`| N/A | Nonexistent legacy directory | Relocated to `backend/app/ai/matching/`. |
| **DeepFace Microservice (`ai/DeepFace/`)** | | | | |
| `ai/DeepFace/requirements.txt` | `[CURRENT]` | **Panchami** | Microservice dependencies | DeepFace, TensorFlow, OpenCV packages. |
| `ai/DeepFace/README.md` | `[CURRENT]` | **Panchami** | Microservice documentation | Operating runbook. |
| `ai/DeepFace/demo_verify_deepface.py` | `[CURRENT]` | **Panchami** | Terminal demonstration script | Standalone verification script. |
| `ai/DeepFace/wandermatch.db` | `[CURRENT]` | **Panchami** | Local demo SQLite database | Local demo database. |
| `ai/DeepFace/backend/database.py` | `[CURRENT]` | **Panchami** | Microservice SQLite engine | Local persistence for standalone mode. |
| `ai/DeepFace/backend/main.py` | `[CURRENT]` | **Panchami** | Microservice FastAPI entry point | Microservice server on Port 8001. |
| `ai/DeepFace/backend/routers/*` (3 files)| `[CURRENT]`| **Panchami**| Microservice route handlers | Face, photo, and trip endpoints. |
| `ai/DeepFace/backend/services/face/*` (3 files)| `[CURRENT]`| **Panchami**| ArcFace embedding & matching logic | Core recognition algorithms. |
| `ai/DeepFace/tests/*` (2 files) | `[CURRENT]` | **Panchami** | Recognition tests & sample faces| Microservice test suite. |
| `ai/DeepFace/Dockerfile` | `[PROPOSED]`| **Panchami**| Container definition | Container deployment image. |
| `ai/DeepFace/models/` | `[PROPOSED]`| **Panchami**| Pre-trained weights cache | Local weights storage. |
| **AIConsensus Prototype (`ai/AIConsensus/`)** | | | | |
| `ai/AIConsensus/pyproject.toml`, `uv.lock`| `[CURRENT]` | **Sharvani** | Prototype metadata & lockfile | Preserved prototype setup. |
| `ai/AIConsensus/README.md` | `[CURRENT]` | **Sharvani** | Prototype documentation | Preserved prototype notes. |
| `ai/AIConsensus/.env.example` | `[CURRENT]` | **Sharvani** | Prototype LLM keys template | Preserved prototype template. |
| `ai/AIConsensus/backend/demo_*.py` (3 files)| `[CURRENT]`| **Sharvani**| CLI simulation scripts | Preserved simulation tools. |
| `ai/AIConsensus/backend/test_live_ai.py` | `[CURRENT]` | **Sharvani** | Live LLM connectivity tester | Diagnostic script. |
| `ai/AIConsensus/backend/app/main.py` | `[CURRENT]` | **Sharvani** | Standalone Swagger server | Development playground (Port 8002). |
| `ai/AIConsensus/backend/services/*` (2 files)| `[CURRENT]`| **Sharvani**| In-memory consensus state | Prototype state machines. |
| `ai/AIConsensus/backend/ai/core/*` (5 files) | `[CURRENT]` | **Sharvani**| Blended plan generator, classifiers| Consensus algorithms (kept in place). |
| `ai/AIConsensus/backend/ai/llm/*` (3 files) | `[CURRENT]` | **Sharvani**| Multi-provider LLM client | Model interface layer (kept in place). |
| `ai/AIConsensus/backend/ai/modes/*` (3 files)| `[CURRENT]` | **Sharvani**| Mode A and Mode NA orchestrators | Prototype orchestrators (kept in place). |
| `ai/AIConsensus/backend/ai/tests/*` (3 files)| `[CURRENT]` | **Sharvani**| Automated tests for Mode A/NA | Prototype test suites. |
| `ai/AIConsensus/docs/README.md` | `[CURRENT]` | **Sharvani** | Canonical documentation index | Maps mirror docs to canonical root docs. |
| `ai/AIConsensus/docs/IMPLEMENTATION_LOG.md`| `[CURRENT]`| **Sharvani**| Chronological implementation log | Unique historical record preserved in place. |
| `ai/AIConsensus/docs/*` (14 other files)| `[HISTORICAL]`| **Sharvani**| Mirror copies of specifications | Historical prototype snapshots. |
| **Reference Assets & Documentation Suite** | | | | |
| `data-model/*` (7 files) | `[CURRENT]` | **Sharvani** | Canonical DDL, enums, reference DB | Canonical data model assets. |
| `deepface/*` (empty skeleton + db) | `[HISTORICAL]`| **Panchami** | Stale root directory | Stale legacy skeleton. |
| `scratch/*` (2 files) | `[CURRENT]` | **Sharvani** | Database diagnostic scripts | Non-production scratch tools. |
| `neon.ts` | `[CURRENT]` | **Sharvani** | Neon config stub | Root configuration file. |
| `.env.example` (Root) | `[CURRENT]` | **Sharvani** | Master environment template | Single authoritative template. |
| `HACKATHON.md`, `README.md` | `[CURRENT]` | **Sharvani** | Master documentation & operating guides | Root project documentation. |
| `docs/NIKITHA.md` | `[CURRENT]` | **Nikitha** | Frontend track specification | Nikitha solely updates this document. |
| `docs/PANCHAMI.md` | `[CURRENT]` | **Panchami** | Backend & DeepFace track spec | Panchami solely updates this document. |
| `docs/SHARVANI.md` | `[CURRENT]` | **Sharvani** | Domain, AI & Integration spec | Sharvani solely updates this document. |
| `docs/archive/former-team/` | `[HISTORICAL]` | **Sharvani** | Preserved former-team documents | Reference only; no active fourth member or assignments. |
| `docs/INTEGRATION_CONTRACT.md` | `[CURRENT]` | **Sharvani** | Master shared contract | Single source of truth for contracts. |
| `docs/AI.md` | `[CURRENT]` | **Sharvani** | Master AI spec & 31-decision register | Authoritative architecture suite. |
| `docs/ARCHITECTURE.md`, `DATABASE.md`, etc.| `[CURRENT]`| **Sharvani**| System architecture documentation | Authoritative system documentation. |
| `docs/data/PS-11.db` | `[CURRENT]` | **Sharvani** | Reference seed database copy | Mirrored reference dataset. |
| `docs/data/csv/*` (14 files) | `[CURRENT]` | **Sharvani** | Canonical PS-11 CSV datasets | Reference CSV data assets. |
| `docs/data/queries/starter_queries.sql`| `[CURRENT]`| **Sharvani**| Canonical SQL queries | Reference analytical queries. |
| `docs/data/schema*.sql`, `enums.json` | `[CURRENT]` | **Sharvani** | Canonical schema definitions | Reference DDLs and enums. |

---

## 2.1 Explicit Wire Field Mapping & Alias Table

Pydantic's automatic `to_camel` converts snake_case words by capitalizing subsequent words (`user_id` -> `userId`, `proposal_id` -> `proposalId`). To support legacy shortened wire abbreviations (`usrId`, `prpId`, `trpId`, `itmId`, `votId`, `phoId`), the following explicit mapping is maintained in Pydantic schemas:

| Canonical Entity | Internal Model Column | Canonical Wire Name | Approved Short Alias | Wire Type / Constraint | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **User** | `user_id` | `userId` | `usrId` | `str` (`usr_...`) | Caller identity derived strictly from JWT |
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

## 2.3 Authoritative WebSocket Event Catalog & Wire Delivery Contract

`[AUTHORITATIVE_SHARED_CONTRACT]`
The backend WebSocket manager broadcasts structured JSON envelopes to connected trip members (`/ws/trips/{trip_id}?token={jwt}`). The table below specifies all 16 canonical event types, emission timing, and payload envelopes:

| Event Type Name | Direction | Trigger & Emission Boundary | Authoritative Payload Fields | Recipient Scope & Privacy Filter |
| :--- | :--- | :--- | :--- | :--- |
| **`resyncSnapshot`** | Server -> Client | Initial connection & reconnection | `type: "resyncSnapshot", tripId: str, version: int, snapshot: {trip, itinerary, activeProposals, branches}` | Connecting client only. Full state synchronization. Dual-access adapter supported (`payload.tripId` and `payload.snapshot.trip.trip_id`). |
| **`voteCast`** | Server -> All | Committed vote insert/update | `type: "voteCast", trpId: "...", itmId: "...", prpId: "...", usrId: "...", value: "yes"\|"no", comment: str\|null` | All active trip members. Sensitive medical comments sanitized. |
| **`voteRetracted`** | Server -> All | Committed vote deletion | `type: "voteRetracted", trpId: "...", itmId: "...", prpId: "...", usrId: "..."` | All active trip members. Clears vote tally. |
| **`proposalCreated`** | Server -> All | Committed proposal insert | `type: "proposalCreated", trpId: "...", itmId: "...", proposal: {...}` | All active trip members. |
| **`slotTimerStarted`** | Server -> All | First NO vote committed | `type: "slotTimerStarted", trpId: "...", itmId: "...", closesAt: ISO8601, durationSeconds: 600` | All active trip members. Starts countdown window (Decision #31). |
| **`slotTimerUpdated`** | Server -> All | Mode A owner timer extension | `type: "slotTimerUpdated", trpId: "...", itmId: "...", closesAt: ISO8601, deltaMinutes: int` | All active trip members. Updates countdown UI. |
| **`slotStatusChanged`**| Server -> All | Committed slot status change | `type: "slotStatusChanged", trpId: "...", itmId: "...", slotStatus: "EMPTY"\|"IN_CONSENSUS"\|"BRANCHED"\|"CONFIRMED"` | All active trip members. Updates Route Line pill. |
| **`consensusReconciling`** | Server -> All | Short read lock released; AI task started | `type: "consensusReconciling", trpId: "...", itmId: "...", round: int` | All active trip members. Renders non-blocking subtle spinner. |
| **`aiPlanGenerated`** | Server -> All | Committed blended plan insert | `type: "aiPlanGenerated", trpId: "...", itmId: "...", blendedPlan: {...}, round: int` | All active trip members. Aliased with `aiRecommendationReady`. |
| **`aiRecommendationReady`**| Server -> All | Native backend alias | `type: "aiRecommendationReady", trpId: "...", itmId: "...", ...` | Backend alias for `aiPlanGenerated`. |
| **`consensus.clarification_requested`** | Server -> All | Classifier returned NEEDS_CLARIFICATION | `type: "consensus.clarification_requested", trpId: "...", itmId: "...", extractedConstraints: [...], prompt: str` | All active trip members. Renders clarification chips to author. |
| **`clarificationSubmitted`** | Server -> All | Dissenting author clarified objection | `type: "clarificationSubmitted", trpId: "...", itmId: "...", slotId: "...", usrId: "...", commentId: "...", cycle: int, round: int` | All active trip members. Updates objection status with dual-access slot identifier (`itmId` / `slotId`). |
| **`negotiationCardRendered`** | Server -> All | Reconcile attempts exhausted | `type: "negotiationCardRendered", trpId: "...", itmId: "...", options: [KEEP_ORIGINAL, CLOSER_ALT, RESCHEDULE]` | All active trip members. Renders 3-option negotiation card. |
| **`branchConfirmed`** | Server -> All | Committed branch confirmation | `type: "branchConfirmed", trpId: "...", brcId: "...", usrId: "..."` | All active trip members. Updates subgroup assignments. |
| **`newChatMessage`** | Server -> All | Committed chat message | `type: "newChatMessage", trpId: "...", message: {msgId, usrId, text, timestamp}` | All active trip members. Appends to chat drawer. |
| **`itineraryUpdated`** | Server -> All | Itinerary version incremented | `type: "itineraryUpdated", trpId: "...", version: int` | All active trip members. Triggers OCC cache re-sync. |

> [!CRITICAL]
> **Delivery Protocol Invariants**:
> 1. **Emission After Database Commit**: Events are emitted **strictly after** the underlying PostgreSQL database transaction commits. A service dictionary return is NOT event emission.
> 2. **Client Commands vs Server Events**: Clients communicate mutations via authenticated HTTP endpoints (`POST /api/votes`, `POST /api/proposals`, etc.). Clients NEVER emit broadcast events like `resyncSnapshot` or `aiPlanGenerated` directly over WebSockets.
> 3. **Reconnect Recovery**: If a client reconnects or detects a version mismatch (`version_client < version_server`), it issues an HTTP `GET /api/trips/{trpId}` request to refresh authoritative state.

---

## 2.4 Dissent Clarification Endpoint Contract (`POST /api/slots/{slot_id}/clarify`)

`[PROPOSED_TARGET_ENDPOINT]`
- **Route**: `POST /api/slots/{slot_id}/clarify`
- **Ownership**: Panchami exposes route and serialization; Sharvani executes domain service; Nikitha provides form/chips UI.
- **Request Envelope**:
  ```json
  {
    "tripId": "trp_a91f3c2b",
    "slotId": "itm_7a2b9c",
    "commentId": "com_12345",
    "clarificationText": "Prefer cultural museum with wheelchair ramp, max $25 budget",
    "expectedVersion": 4,
    "evidenceToken": "ev_tok_8f9a2b"
  }
  ```
- **Authority & Security Guards**:
  1. Authenticated caller (`current_user.user_id`) verified in `trip_members`.
  2. Caller must match the author of the original dissenting comment (`403 Forbidden` if caller != author).
  3. Path parameter `slot_id` must match envelope `slotId` (`400 Bad Request` with `ERR_SLOT_ID_MISMATCH` if mismatched).
  4. English-Only Scope: `clarificationText` is received and processed in English; non-English input triggers clarification in English.
  5. `expectedVersion` validated against `itineraries.version` (OCC guard; `409 Conflict` on mismatch).
  6. `evidenceToken` validated (1h TTL `[PROPOSED_CONFIGURATION_TTL]`, Decision #12).
- **Domain Invariants**: Clarification preserves the objection constraint set, does NOT advance round number, does NOT count as a vote, does NOT reset voting deadline.
- **Canonical Server Response DTO**: `200 OK` with:
  ```json
  {
    "status": "CLARIFICATION_ACCEPTED",
    "slotId": "itm_7a2b9c",
    "commentId": "com_12345",
    "cycle": 1,
    "round": 1
  }
  ```
  *(Note: Clarification is a discussion input; it records the objection clarification into the slot constraint set but does NOT mutate `itineraries.version`. In WanderMatch, `itineraries.version` tracks authoritative itinerary item modifications (such as proposal confirmations, schedule changes, branch partition confirmations, and revision restores; see Section 2.6 Authoritative Mutation, Version & Freshness Matrix). Submitting a clarification updates the deterministic clarification state captured in both snapshot creation and commit-time revalidation, causing in-flight AI synthesis leases to be rejected as stale (`DISCARDED_STALE`) without fabricating an itinerary version bump or mutating traveler votes. Thus `version` is omitted from the clarification response).*

- **Authoritative Logical Representation of Objections & Clarifications**:
  To guarantee full auditability, objection traceability, and unambiguous freshness invalidation, the system distinguishes five distinct representations:
  1. **Original Objection**: The traveler's primary dissent reason recorded during the NO vote in `votes.comment` (e.g. *"Too expensive and lacks wheelchair accessibility"*). This field is immutable and permanently preserved for audit traceability; submitting a clarification never overwrites or mutates `votes.comment`.
  2. **Additional Clarification**: The supplementary nuance provided by the dissenting traveler via `POST /api/slots/{slot_id}/clarify` (`clarificationText`, e.g. *"Prefer cultural museum with ramp, max $25 budget"*). In the current schema without table migrations, this is maintained in-process and recorded in `RevisionHistory` snapshots (`[PROPOSED_STORAGE]` for future `vote_clarifications` / `slot_clarifications` dedicated table).
  3. **Extracted Structured Constraints ($C_{\text{obj}}$)**: Deterministically parsed constraint predicates extracted from the clarification text (e.g. `[{"type": "budget_max", "value": 25.0, "currency": "USD"}, {"type": "accessibility", "value": "wheelchair"}]`).
  4. **Logical Revision Used for Freshness & Canonical Serialization**:
     The deterministic canonical clarification state derived by `canonicalize_clarifications(slot_clarifications)` using `canonicalize_extracted_constraints(constraints)`.
     - **Type Validation & Unstructured Coercion**: Dictionaries are recursively normalized; unstructured string constraints are normalized to `{"type": "unstructured_constraint", "value": s.strip()}`. Unsupported types raise `TypeError('ERR_MALFORMED_CONSTRAINT')`.
     - **Boolean vs Numeric Discrimination**: Evaluates `isinstance(v, bool)` before `isinstance(v, (int, float))` (preventing Python `issubclass(bool, int)` coercion of `True`/`False` into `1`/`0` or `1.0`). Native booleans are strictly preserved.
     - **Exact Numeric & Float Precision**: Integers and floating-point/decimal coordinates/weights are preserved with full numeric precision (no lossy two-decimal rounding, ensuring distinct coordinates like 48.8584 != 48.8589 remain distinguishable).
     - **String & Currency Normalization**: `type` stripped lowercase, `currency` stripped uppercase ISO (e.g. `'USD'`), `unit` stripped lowercase.
     - **Schema Extension & Unknown Fields**: All dictionary keys are retained and recursively canonicalized without silent field dropping.
     - **Safe Deterministic Sorting**: Avoids Python dictionary comparison `TypeError` by serializing each normalized constraint dictionary via `json.dumps(c, sort_keys=True)` for key sorting.
     - **Unambiguous Tie-Breaking**: Deterministically orders multiple clarification records by composite tuple `(vote_id, user_id, clarification_id)`, where `clarification_id` is a stable primary key (`[PROPOSED_STORAGE]` table) or fallback content SHA-256 hash.
     ```python
     def canonicalize_extracted_constraints(constraints: List[Any]) -> List[Dict[str, Any]]:
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
     ```
     This deterministic state is directly serialized into `canonical_state["clarifications"]` during both snapshot capture and commit-time revalidation.
  5. **Data Supplied to AI**: Synthesized prompt context concatenating the original objection, the author's clarifying text, and extracted constraints to guide LLM candidate generation.
- **WebSocket Broadcast Envelope**: Emits `clarificationSubmitted` to all connected trip members:
  ```json
  {
    "type": "clarificationSubmitted",
    "trpId": "trp_a91f3c2b",
    "itmId": "itm_7a2b9c",
    "slotId": "itm_7a2b9c",
    "usrId": "usr_test_nikitha",
    "commentId": "com_12345",
    "cycle": 1,
    "round": 1
  }
  ```
- **Authoritative Unified Error Mapping Table**:
  | Condition | HTTP Status | Domain Error Code | Wire Response / UI Behavior | Status |
  | :--- | :--- | :--- | :--- | :--- |
  | **Malformed JSON request** | `400 Bad Request` | `ERR_MALFORMED_REQUEST` | Syntax parse failure. UI displays: *"Request payload could not be parsed."* | `[PROPOSED]` |
  | **Path/body slot mismatch** | `400 Bad Request` | `ERR_SLOT_ID_MISMATCH` | URL `slot_id` != body `slotId`. UI displays: *"Slot route mismatch error."* | `[PROPOSED]` |
  | **Missing required field** | `422 Unprocessable Entity` | `ERR_MISSING_FIELD` | Pydantic validation failure. UI highlights missing field in `#C1502E`. | `[PROPOSED]` |
  | **Missing or invalid authentication** | `401 Unauthorized` | `ERR_UNAUTHORIZED` | Missing/invalid Bearer JWT. Frontend redirects to Clerk `<SignIn />`. | `[CURRENT]` |
  | **Nonmember caller** | `403 Forbidden` | `ERR_NOT_TRIP_MEMBER` | Caller not active in `trip_members`. UI displays: *"You are not an active member of this trip."* | `[CURRENT]` |
  | **Caller not original objection author** | `403 Forbidden` | `ERR_NOT_COMMENT_AUTHOR` | Caller does not own dissenting `comment_id`. UI displays: *"Only the author of the objection may clarify it."* | `[PROPOSED]` |
  | **Unknown trip/slot/objection** | `404 Not Found` | `ERR_NOT_FOUND` | Referenced entity not found. UI displays: *"The specified slot or objection was not found."* | `[PROPOSED]` |
  | **Stale version or cycle** | `409 Conflict` | `ERR_STALE_VERSION` | `expectedVersion` != `itineraries.version` (OCC guard). UI displays: *"Itinerary updated. Refreshing..."* | `[PROPOSED]` |
  | **Expired evidence token** | `422 Unprocessable Entity` | `ERR_TOKEN_EXPIRED` | Token timestamp > 1h TTL (Decision #12). UI displays: *"Clarification window expired. Please re-open session."* | `[PROPOSED]` |
  | **Tampered or mismatched token** | `422 Unprocessable Entity` | `ERR_EVIDENCE_INVALID` | HMAC signature invalid or binds to wrong slot. UI displays: *"Evidence token invalid. Session re-initialized."* | `[PROPOSED]` |
  | **Identical retry** | `200 OK` | N/A (Idempotent) | Identical text & token re-submitted. Returns existing acceptance record idempotently. | `[PROPOSED]` |
  | **Conflicting replay** | `409 Conflict` | `ERR_CONFLICTING_REPLAY` | Different text submitted for already resolved objection. UI: *"This objection has already been processed."* | `[PROPOSED]` |
  | **Unavailable dependent service** | `503 Service Unavailable` | `ERR_SERVICE_UNAVAILABLE` | Database or consensus service unreachable. UI displays: *"Service temporarily unavailable. Please retry shortly."* | `[PROPOSED]` |

---

## 2.5 Deterministic Status Precedence & UI Badge Mapping

The table below defines the strict precedence mapping from backend verification and feasibility fields to Nikitha's 6 displayed status badges:

| Precedence | Backend Condition & Trigger | Canonical Status Badge | Visual Token & Color | User Tooltip Guidance |
| :---: | :--- | :--- | :--- | :--- |
| **1 (Highest)** | Venue confirmed closed or road access closed | **`BLOCKED`** | Terracotta (`#C1502E`) | "Road confirmed closed or venue closed on scheduled date." |
| **2** | Transit duration + buffers + activity exceeds slot window | **`INFEASIBLE`** | Red (`#D9381E`) | "Schedule conflict: transit plus activity exceeds available slot window." |
| **3** | Classifier returned ambiguous objection / multiple matches | **`NEEDS_CLARIFICATION`** | Clay (`#D97706`) | "Clarification required from traveler to proceed." |
| **4** | Road routing unavailable (503) or missing travel duration | **`UNVERIFIED`** | Slate (`#64748B`) | "Road routing or catalog evidence unavailable. Travel time unverified." |
| **5** | Route found, schedule fits, but operating hours unconfirmed | **`PARTIALLY_VERIFIED`** | Amber (`#F59E0B`) | "Schedule verified; operating hours or closure feed unconfirmed." |
| **6 (Lowest)** | Coords verified, road route found, schedule fits, open verified | **`VERIFIED`** | Green (`#2E7D32`) | "All details verified against catalog and live road network." |

---

## 2.6 Authoritative Mutation, Version & Freshness Matrix

`[AUTHORITATIVE_SHARED_CONTRACT]`
The table below specifies the precise authoritative concurrency, invalidation, and freshness rules across all system mutations. It strictly separates:
1. **Physical Itinerary Mutations**: Operations that mutate the master itinerary items and increment the physical optimistic concurrency control (OCC) column (`itineraries.version`).
2. **Consensus State & Round Transitions**: Operations that advance rounds, open proposal reviews, or transition slot consensus states (`slot_consensus.current_round`, `slot_consensus.status`).
3. **AI Input State Fingerprints**: Operations that change the deterministic state fingerprint $\text{Hash}(S_{\text{snap}})$ (proposals, votes, comments, clarifications, electorate, mode), invalidating in-flight AI synthesis leases.

| Operation / System Event | Mutates `itineraries.version`? | Updates Consensus State / Cycle / Round? | Updates AI Input Fingerprint $\text{Hash}(S_{\text{snap}})$? | In-Flight AI Lease Invalidation Rule | Client Wire Context & Event Emitted |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Trip / Slot Creation & Timeline Edits** | **Yes** ($Ver + 1$) | Initializes / resets slot consensus state | **Yes** (modifies itinerary layout) | In-flight lease invalidated by $Ver_{\text{db}} \ne Ver_{\text{snap}}$ mismatch; commit discards stale result | `itineraryUpdated` ($Ver$), `slotStatusChanged` |
| **New Competing Proposal Created** | **No** (proposal added with status `open`) | **No** (voting deadline NOT extended) | **Yes** (modifies candidate pool in `proposals`) | In-flight synthesis rejected on commit due to `state_fingerprint` mismatch; new proposal queued for next cycle | `proposalCreated` (`prpId`, `itmId`) |
| **Vote Cast, Switched, or Retracted** | **No** (updates `votes` table) | May trigger `slotStatusChanged` or start countdown | **Yes** (modifies vote values, comments, or voter tally) | Commit-time fingerprint revalidation detects vote change; discards stale in-flight candidate; unanimous YES terminates lease | `voteCast`, `voteRetracted`, `slotTimerStarted` (on first NO) |
| **Dissent Clarification Submitted** | **No** (discussion input; no itinerary mutation) | **No** (does NOT advance round, count as vote, or reset timer) | **Yes** (updates deterministic `clarifications` state in fingerprint) | In-flight AI synthesis lease invalidated: constraint change causes commit-time fingerprint mismatch (`DISCARDED_STALE`); re-generation triggered | `clarificationSubmitted` (`cycle`, `round`), no version change |
| **Slot Countdown Expiration (Mode NA)** | **No** (state machine timer tick) | **Yes** (transitions to `RECONCILING` or `BRANCHED`) | **Yes** (locks voting snapshot and electorate) | Acquires exclusive AI reconciliation lease $Req_{\text{ai}}$ with TTL (Decision #17) | `slotStatusChanged` (`IN_CONSENSUS`), `consensusReconciling` |
| **Mode A Owner Action (Extend / Force Branch)** | **Yes** on branch ($Ver + 1$); **No** on extend | **Yes** (timer extended or slot branched) | **Yes** (overrides candidate pool or terminates cycle) | Explicitly cancels pending AI generation lease; clears `lease_token` | `slotTimerUpdated` (extend) or `branchConfirmed`, `itineraryUpdated` (branch) |
| **AI Blended Proposal Publication** | **No** (master item unchanged; proposal inserted with `status="open"`) | **Yes** (advances round: `current_round + 1`; slot transitions to `PROPOSAL_OPEN`) | **Yes** (establishes new proposal candidate in slot pool) | Commits synthesis proposal; releases and clears active lease (`lease_token = None`, `lease_expires_at = None`) | `aiPlanGenerated` (aliased with `aiRecommendationReady`), `proposalCreated` |
| **Proposal Confirmation & Slot Lock (Mode A / NA)** | **Yes** ($Ver + 1$ via CAS update) | **Yes** (slot transitions to `CONFIRMED`; proposal `status="accepted"`; voting closed) | **Yes** (terminates slot consensus cycle) | Clears any active lease; in-flight worker jobs aborted on $Ver$ mismatch | `slotStatusChanged` (`CONFIRMED`), `itineraryUpdated` ($Ver$) |
| **Branch Partition Confirmed** | **Yes** ($Ver + 1$) | **Yes** (slot state transitions to `BRANCHED`) | **Yes** (terminates consensus cycle for slot) | Releases lease; partitions travelers into tracks; in-flight jobs aborted on $Ver$ mismatch | `branchConfirmed`, `itineraryUpdated` ($Ver$) |
| **Unanimous Chat Override** | **Yes** ($Ver + 1$) | **Yes** (immediate confirmation; cycle closed) | **Yes** (cancels AI requirement) | Aborts any active AI worker lease immediately | `slotStatusChanged`, `itineraryUpdated` ($Ver$) |
| **Slot Rescheduling (`RESCHEDULE_WINDOW`)** | **Yes** ($Ver + 1$ in Mode A / upon confirmation) | **Yes** (re-evaluates time-window constraints) | **Yes** (changes transit and operating feasibility) | Lease invalidated by $Ver$ and schedule mismatch | `itineraryUpdated` ($Ver$), `slotStatusChanged` |
| **Itinerary Revision Restored** | **Yes** ($Ver + 1$) | **Yes** (replaces active slots with snapshot tip) | **Yes** (invalidates all pending state) | Aborts all in-flight AI worker leases across trip | `itineraryUpdated` ($Ver$), `resyncSnapshot` (on reconnect) |

---

### 2.6.1 Detailed Lifecycle Specification: Proposal Publication vs Confirmation

To prevent conflation between generating advisory candidates and authoritative itinerary modifications, the system strictly separates **Publication** from **Confirmation**:

```
[Phase 1: Generation & Lease Acquisition]
  -> In-flight worker acquires lease (TTL 30s)
  -> Captures immutable snapshot: {proposals, votes, clarifications, electorate, mode, version, cycle}
  -> Computes deterministic state_fingerprint = SHA256(canonical_state)

[Phase 2: Validated Proposal Publication]
  -> Authority: AI Worker / System via Sharvani Domain Service (`commit_reconciliation_result`)
  -> Guard: Live lease token match + unexpired lease + (itinerary.version == snapshot.version) + (state_fingerprint match)
  -> State Mutation: Inserts Proposal(status="open", action="ADVISORY_PROPOSAL" in Mode A | "replace_item" in Mode NA)
  -> Round & Slot Effect: slot_consensus.current_round += 1; slot_consensus.slot_status = "IN_CONSENSUS" (target enum: "PROPOSAL_OPEN" [TARGET_ENUM_EXPANSION])
  -> Itinerary Version Effect: NO CHANGE (itineraries.version remains at current Ver; master item unmodified)
  -> Lease Effect: Clears lease_token and lease_expires_at
  -> Events Emitted: aiPlanGenerated (aliased with aiRecommendationReady), proposalCreated
  -> Frontend State: Nikitha renders proposal card in slot with voting/acceptance actions; Route Line remains unlocked

[Phase 3: Proposal Confirmation & Slot Lock]
  -> Authority: Mode A Trip Owner (POST /api/trips/{id}/slots/{item_id}/accept-proposal or POST /api/consensus/mode-a/accept; verified against trip.owner_user_id) OR Mode NA Authoritative Consensus Resolution (evaluated strictly by internal server logic under row lock)
  -> Authentication & Authorization Guard: Caller authentication & trip membership authorization verified BEFORE disclosing any prior confirmation status; unauthorized callers receive 401/403 without status disclosure
  -> Governance Mode Guard: Missing trip or unrecognized mode fails closed (404/400); no silent fallback to Mode NA
  -> Consensus Guard: CAS check (itineraries.version == expected_version); Mode A requires trip.owner_user_id == confirming_user_id; Mode NA requires server-verified unanimous YES with active electorate (len(active_members) > 0) or closed timer window without caller-supplied dictionary override; proposal scope validated (same trip itinerary, target item ID, active cycle, status == 'open'); slot not in terminal state ('CONFIRMED', 'BRANCHED')
  -> State Mutation: Selected proposal marked status="accepted", competing proposals marked "rejected"; master ItineraryItem fields updated
  -> Round & Slot Effect: slot_consensus.slot_status = "CONFIRMED"; consensus cycle concluded
  -> Lock Order Invariant: Row lock on SlotConsensus FIRST, then Itinerary SECOND (matching reconciliation lock ordering) with explicit transaction management (db.rollback() on all exception paths)
  -> Idempotency Invariant: Identical retry returns 200 ALREADY_CONFIRMED without re-incrementing version; conflicting retry rejected with 409 Conflict
  -> Itinerary Version Effect: INCREMENT (itineraries.version = version + 1 via atomic CAS)
  -> Lease Effect: Terminates any pending lease
  -> Events Emitted: slotStatusChanged (slotStatus: "CONFIRMED"), itineraryUpdated (version: Ver + 1)
  -> Frontend State: Locks Route Line slot, turns pill green CONFIRMED, hides proposal review cards, triggers OCC version sync
```

### 2.6.2 State Revalidation, Freshness & Invalidation Rules

Every asynchronous synthesis or clarification callback is governed by the same strict, deterministic freshness contract before ANY authoritative state mutation:
1. **Accepted into Active Input**: An operation that occurs prior to lease acquisition is included in `snapshot.state_fingerprint` and directly influences active generation.
2. **Queued Outside Active Input**: A new proposal submitted while inference is running is persisted with `status="open"`. Because `proposals` set in the database now differs from `snapshot.proposals`, the commit-time fingerprint check fails (`DISCARDED_STALE`). The proposal is safely preserved and processed in the subsequent round.
3. **Existing Input Modified**: If a traveler casts a vote, changes a vote value, alters dissent comments (`votes.comment`), or submits a clarification (`clarificationText`), the recomputed `current_state_fingerprint` immediately diverges from `snapshot.state_fingerprint`. Commit-time revalidation discards the stale AI candidate (`DISCARDED_STALE`) and initiates a fresh generation cycle.
4. **Current Cycle Cancelled or Superseded**: If an owner action, unanimous chat override, revision restoration, or unanimous YES resolution occurs, `itineraries.version` is incremented or `lease_token` is cleared. Any in-flight worker callback fails closed (either `DISCARDED_SUPERSEDED_LEASE` or `itinerary.version != snapshot_version`).
5. **Deterministic Ordering Invariant**: All collections (`proposals`, `votes`, `clarifications`, `electorate`) are deterministically sorted by primary keys / composite keys before serialization and hashing. Database row arrival order can never alter the fingerprint.

---

## 2.2 Trusted Identity & Request Boundary Rules
1. **Verified Actor Identity**:
   - The actor performing ANY operation is derived strictly from verified credentials (`current_user.user_id`), NOT from request bodies (`payload.userId`, `payload.usrId`, `proposedByUserId`).
   - If a legacy body contains an identity field for backwards compatibility, it MUST be either validated to match `current_user.user_id` or ignored in favor of `current_user.user_id`. It must NEVER override the authenticated actor.
2. **Actor vs Target Member vs Resource Identifiers**:
   - `current_user.user_id`: Authenticated caller executing the request.
   - `target_user_id`: Target of an administrative action (e.g., approving a join request or adding a member).
   - `trp_id`, `itm_id`, `prp_id`, `brc_id`, `msg_id`: Resource identifiers identifying domain entities.

---

## 3. Authoritative Contract Consistency Table

This reference table establishes the single source of truth across all three tracks, reconciling discrepancies between existing source code, target designs, and unapproved proposals.

| Surface / Interface | Current Implementation `[CURRENT]` | Agreed Target Contract `[AGREED TARGET]` | Unapproved Proposal / Prohibited `[PROHIBITED / UNAPPROVED]` | Ownership & Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **Photo Upload Endpoint** | `POST /api/photos` (`routers/photos.py`). Form: `file`/`photo`, `trp_id`/`trpId`, `uploader_id`. Saves to `static/uploads/`, sends relative URL to worker, sets `completed` prematurely. | `POST /api/photos`. Form: `file: UploadFile` (binary), `trpId: str`. Panchami reads file, calls Sharvani persistence with initial `pending`, streams multipart bytes + candidate vectors to worker, updates DB with face matches. | `POST /api/photos/upload` (historical proposal; unapproved alias; clients MUST call `POST /api/photos`). Sending relative paths to worker. | **Panchami** owns route & worker forwarding; **Sharvani** owns photo and tag database persistence in-process. |
| **Clerk Webhook Endpoint** | `POST /api/auth/webhook` (`routers/auth.py`). Extracts svix headers, verifies signature, creates `User` and `UserPreference`. | `POST /api/auth/webhook`. Panchami extracts headers & body, invokes Sharvani's `security.verify_svix_signature()`. Sharvani executes `security.sync_clerk_user_to_db()` in single atomic transaction. | `POST /api/webhooks/clerk` (historical proposal; unapproved alias; Clerk must be configured to `POST /api/auth/webhook`). | **Panchami** owns HTTP endpoint; **Sharvani** owns cryptographic verification & DB user sync in-process. |
| **Timer Check Endpoint** | `POST /api/proposals/check-timer` (`routers/consensus.py:L693`). Accepts `prp_id`, `advance_minutes`. If window expired with 0 NO votes, auto-confirms slot. | `POST /api/proposals/check-timer`. Production contract evaluates `now >= slot_consensus.closes_at` without test parameters. `advance_minutes` restricted strictly to automated test fixtures. | Calling `POST /api/consensus/check-timer` (unmounted alias; route is `/api/proposals/check-timer`). Exposing test clock controls in production payloads. | **Panchami** exposes HTTP route; **Sharvani** owns authoritative countdown state machine in-process. |
| **Trip Chat Messages** | `GET /api/trips/{trip_id}/chat` & `POST /api/trips/{trip_id}/chat` (`routers/trips.py:L960, L991`). Returns chat history with sender details. | `GET /api/trips/{trip_id}/chat` & `POST /api/trips/{trip_id}/chat`. Canonical unified endpoints. Frontend `api.ts` aligned. | Calling `/api/trips/{trip_id}/messages` or `/api/messages` (stale frontend aliases; must align to `/api/trips/{trip_id}/chat`). | **Panchami** owns HTTP transport; **Sharvani** owns message persistence in-process. |
| **WebSocket Connection & Resync** | `ws://host/ws/trips/{trip_id}/{user_id}` (`websocket_manager.py`). Verifies token & membership; immediately sends `{"type": "resyncSnapshot", "snapshot": {...}}`. | `ws://host/ws/trips/{trip_id}?token=...`. Panchami verifies token query, checks membership, and delivers `{"type": "resyncSnapshot", ...}` on connection and reconnect. | Silently renaming `resyncSnapshot` to `tripStateSnapshot` without coordinating with backend. | **Panchami** manages connection lifecycle & broadcast; **Nikitha** handles `resyncSnapshot` in `TripContext`. |
| **WebSocket Event: AI Plan Broadcast** | Backend emits `{"type": "aiRecommendationReady", ...}` (`consensus.py` lines 452, 684). | Backend emits both `aiPlanGenerated` and `aiRecommendationReady` as aliases to maintain complete frontend and backend compatibility. | Breaking frontend by dropping either event without unified client adapter update. | **Panchami** broadcasts event; **Nikitha** handles event in `TripContext.tsx`. |
| **Vote Values & Invariants** | Writes `yes` or `no` to `votes.value`. Retracts prior vote on same proposal only. | Mandatory typed reason when `value === 'no'`. Retracts prior YES on competing proposal in same slot (`AC-VOT-02`). Idempotent re-voting. | Writing `value: 'abstain'` (strictly prohibited; only binary `yes` or `no` permitted). Claiming competing YES retraction is already working. | **Sharvani** enforces invariants in `voting_service.py` in-process; **Panchami** returns HTTP 400 if comment missing. |
| **Optimistic Concurrency Control** | Verifies `itineraries.version`. Bumps `version = version + 1`. Returns HTTP 409 on mismatch. | Atomic CAS update: `UPDATE itineraries SET version = version + 1 WHERE itinerary_id = :id AND version = :expected`. | Application-level read-then-write without atomic CAS in database transaction. | **Sharvani** implements atomic CAS query; **Panchami** maps conflict to HTTP 409. |
| **DeepFace Microservice Transport** | `backend/routers/photos.py` defectively sends relative URL `{"photo_url": "/static/uploads/pho_xxx.jpg"}` to `http://localhost:8001`. | Panchami fetches candidate embeddings from Sharvani in-process and streams real multipart form-data image bytes + candidate vectors payload to worker on port 8001. | Treating relative local filesystem paths as image binary across microservice network boundaries. Calling persistence on port 8000. | **Panchami** owns transport to worker; **Sharvani** owns database persistence in-process. |
| **Face Recognition Failure State** | On worker timeout/failure, code catches exception and leaves photo marked `processing_status = 'completed'` with 0 tags. | If worker times out or fails: photo is marked `processing_status = 'failed'`. Worker failure logged. | Documenting worker network failure or timeout as successful completed recognition. | **Panchami** handles worker response; **Sharvani** persists failed/completed status in-process. |
| **Privacy / Embedding Vector Exposure** | Serializer omits `embedding_data`. | 512-d ArcFace floating-point vectors are server-internal only. Never printed in logs or sent to browser. | Returning raw facial vectors in client API responses or frontend inspection panels. | **Panchami** filters responses; **Sharvani** encapsulates vector storage. |
| **Itinerary PDF Export** | Client-side export button stubbed in UI (`FR-EXP-01`). | Itinerary PDF export is **REQUIRED** (`FR-EXP-01`). Generation rendering engine choice (`@react-pdf/renderer` vs backend `weasyprint`) is **PENDING** under Decision #30. | Omitting PDF export or treating entire requirement as optional. | **Nikitha** owns UI trigger; **Sharvani & Nikitha** coordinate renderer selection under Decision #30. |
| **Mode A Admin Routes** | Mounted under `/api/consensus/mode-a/*` (`consensus.py:L414, L465, L508, L572, L607`). | `POST /api/consensus/mode-a/invoke`, `/accept`, `/force-branch`, `/extend`, `/direct-confirm`. | Mislabeled `/api/mode-a/*` (unmounted route; must use full prefix `/api/consensus/mode-a/*`). | **Panchami** exposes HTTP routes; **Sharvani** enforces owner permissions and executes transitions. |
| **Direct Membership Addition** | Join requests (`/join-request`), approvals (`/approve`), invite codes (`/invite-code`), join by code (`/join-by-code`) are implemented in `trips.py`. Direct `POST /api/trips/{trp_id}/members` does NOT exist in code. | `POST /api/trips/{trp_id}/members` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`. Direct addition route by trip owner. | Describing `POST /api/trips/{trp_id}/members` as current implementation before it is written. | **Panchami** implements router endpoint; **Sharvani** enforces capacity & authorization. |
| **Negotiation Option Selection** | Explanation card renders options; submitting chosen option is missing. | `POST /api/negotiation/select-option` `[PROPOSED TARGET / MISSING IMPLEMENTATION]`. Submits option (`KEEP_ORIGINAL`, `CLOSER_ALTERNATIVE`, `RESCHEDULE_WINDOW`) with `selectedOptionId`, `expectedVersion`, and `evidenceToken`. | Silently mutating confirmed activity or skipping group vote on reschedule. | **Nikitha** renders choices; **Panchami** exposes route; **Sharvani** applies transaction. |
| **Objection Taxonomy & Vague Comments** | Old prototype used 2 classes and classified vague comments as fixable tweak. | Canonical 4-class taxonomy (`AI.md § 3`): `FIXABLE_TWEAK`, `FIXED_REQUIREMENT`, `NEEDS_CLARIFICATION`, `UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE`. Vague comments map to `NEEDS_CLARIFICATION`. | Classifying vague input as `FIXABLE_TWEAK`; treating soft preferences as hard constraints. | **Sharvani** owns classifier prompt & schema; **Nikitha** displays clarification chips. |
| **Round-Cap Branching Guard** | Code previously branched whenever `round >= 3` without evaluating deadline. | Round-cap branching requires BOTH completion of round 3 AND window closure (`now >= slot_consensus.closes_at`) with unresolved dissent. | Branching on `round >= 3` while voting window remains open; bypassing open window via reconcile. | **Sharvani** enforces window closure guard in orchestrator; **Panchami** maps trigger. |
| **Silent Member Governance** | Inactive members in open voting window. | Non-voters are NEVER counted as YES votes. When parallel branching occurs, silent members default to Track A per canonical rule (`AI.md:196`). | Treating non-voters as YES; claiming silent members can never be assigned without taking action. | **Sharvani** enforces Track A branch default; **Nikitha** renders branch cards. |
| **Road Routing & Feasibility Equation** | Geodesic approximations or synthetic fallbacks. | Real road distance/duration (OSRM/GraphHopper). Feasibility equation: Outbound + activity + onward + buffers (2 x 15m) + return commitments. Batur: 75m + 120m + 90m + 30m + 30m = 345m. | Using Haversine as feasibility proof; omitting transit buffers from schedule arithmetic. | **Sharvani** validates road network & arithmetic; **Panchami** serializes badges. |
| **In-Process Service Handoff** | Describing domain service calls as "on port 8000" or HTTP. | Router handlers run in the SAME process as domain services; calls are direct Python function calls passing `Session = Depends(get_db)`. | Making HTTP requests from FastAPI backend to `http://localhost:8000` to save data. | **Panchami** calls domain functions; **Sharvani** executes database transactions. |

---

## 3.1 Consensus Algorithm Stages & Cross-Document Responsibility Matrix

`[APPROVED_REQUIREMENT]` The table below defines the exact architectural division across all 8 consensus algorithm stages, mapping each canonical specification in [`docs/AI.md`](AI.md) to the concrete responsibilities of Sharvani, Panchami, and Nikitha:

| Stage # | Algorithm Stage | Canonical Definition (`docs/AI.md`) | Sharvani (Domain & Persistence) | Panchami (Transport & Serialization) | Nikitha (Frontend UI & Interaction) | Shared Wire & Service Anchor |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Consensus State Machine (FSM)** | Section 3.2: Formal 11-tuple state vector $\mathbf{X}_{	ext{slot}}$, transition matrix T-01..T-14, safety vs liveness | `consensus_service.py`: Enforces guards, evaluates state, executes CAS version checks, commits atomic DB writes | `routers/consensus.py`: Dispatches clean HTTP commands; maps domain exceptions to RFC 7807; no consensus logic in routers | Renders authoritative slot status (`CONFIRMED`, `BRANCHED`, `OPEN`); no client-side consensus inference | `INTEGRATION_CONTRACT.md § 1 & § 3` |
| **2** | **Objection Interpretation** | Section 3.3: 4-class taxonomy, structured schema (`ObjectionInterpretationResult`), negation/sarcasm handling | `branch_trigger_classifier.py`: Runs structured Pydantic extraction; binds stated limitations to traveler | `POST /api/votes`: Validates non-empty comment on NO vote; serializes classification in response | Renders non-blocking clarification prompt chips when `NEEDS_CLARIFICATION` is emitted | `INTEGRATION_CONTRACT.md § 2.1 & § 6` |
| **3** | **Grounded Catalog Retrieval** | Section 3.4: Relational SQL retrieval over catalog; no vector DB required; verified candidate set | `candidate_selector.py`: Queries `activities_poi` with relational filters (city, budget, category exclusions) | Serializes candidate items into proposal responses; enforces Pydantic field schemas | Displays verified catalog activities with photos, duration badges, and cost deltas | `INTEGRATION_CONTRACT.md § 2.2` |
| **4** | **Deterministic Feasibility Engine** | Section 3.5: Schedule inequality, OSRM road distance, transit buffers ($B_{arr}, B_{dep}$), tri-state outcome | `hard_constraint_validator.py`: Evaluates complete inequality; flags `INFEASIBLE` or `FEASIBILITY_CANNOT_BE_DETERMINED` | Exposes routing adapter endpoints; handles geocoding/routing provider timeouts | Renders 6 verification badges (`VERIFIED`, `INFEASIBLE`, etc.); displays transit duration diffs | `INTEGRATION_CONTRACT.md § 3 (Road Routing)` |
| **5** | **Preference Aggregation & Ranking** | Section 3.6: Jaccard soft preference matching, cost delta penalty, Pareto dominance, unaddressed dissenters | Computes candidate ranking score; identifies compromised minority travelers; passes rationale | Transports candidate score breakdown in proposal metadata | Renders compromise rationale banner: explains why plan was chosen and who remains compromised | `INTEGRATION_CONTRACT.md § 6` |
| **6** | **Conflict Analysis & Branch Grouping** | Section 3.7: Incompatibility graph, validated partition (`validate_branch_partition`), singleton auto-finalize | `branch_grouping.py`: Enforces disjointness & completeness; assigns silent members to Track A; no synthetic `poi_other` | `POST /api/branches/{id}/confirm`: Manages subgroup confirmation handoff | Renders parallel branch track cards; defaults non-voters to Track A; allows track switching | `INTEGRATION_CONTRACT.md § 3 (Silent Members)` |
| **7** | **Bounded Feedback & Negotiation** | Section 3.8: 2-attempt loop, cycle counters, 3-option negotiation payload derivation | Generates 3-option negotiation payload; `apply_negotiation_selection` executes atomic state transition | `POST /api/negotiation/select-option`: Validates `expectedVersion` and `evidenceToken` (1h TTL `[PROPOSED_CONFIGURATION_TTL]`, Decision #12) | Renders 3-option negotiation card (`KEEP_ORIGINAL`, `CLOSER_ALTERNATIVE`, `RESCHEDULE_WINDOW`) | `INTEGRATION_CONTRACT.md § 2.1 & § 6` |
| **8** | **Async Snapshot-and-Commit** | Section 3.9: Non-blocking inference, lease token, version revalidation, stale rejection | Starts short read transaction; releases DB lock during inference; revalidates version before commit; discards stale | Dispatches WebSocket events (`aiPlanGenerated`, `consensus.clarification_requested`) **only after** DB commit | Subscribes to WebSocket; issues authenticated HTTP `GET /api/trips/{trpId}` snapshot refresh if client version lags server version (clients never emit server broadcast events) | `INTEGRATION_CONTRACT.md § 1 & § 5` |

---

## 4. Detailed Photo Recognition Protocol & Semantics

### 4.1 Image-Transfer Mechanism
1. **Frontend to Backend**:
   - Frontend sends a standard HTTP `multipart/form-data` request to `POST /api/photos`.
   - Form fields: `file: UploadFile` (binary image data), `trpId: string` (target trip ID).
2. **Backend to DeepFace Worker**:
   - Panchami's photo handler calls Sharvani's in-process `photo_service.get_candidate_member_embeddings(db, trip_id)` to load active trip members and their 512-d ArcFace vectors from Neon PostgreSQL.
   - Panchami forwards the image bytes and candidate vectors as a real `multipart/form-data` stream to the DeepFace worker:
     ```python
     async with httpx.AsyncClient(timeout=10.0) as client:
         files = {"file": (filename, image_bytes, content_type)}
         data = {"trip_id": trip_id, "candidate_embeddings": json.dumps(candidate_embeddings_payload)}
         resp = await client.post(f"{DEEPFACE_SERVICE_URL}/api/face/match-photo", files=files, data=data)
     ```
   - **Relative Path Prohibition**: Panchami must **never** send a relative path (such as `/static/uploads/pho_123.jpg`) across network boundaries to a separate service.

### 4.2 Face-Instance Identifiers & Instance-Counting Completeness
To prevent confusion between distinct registered users and detected face instances (e.g. a group photo with 4 people, 2 of whom are registered and 2 unknown):
1. **Face Instances**: The DeepFace worker returns an explicit list of detected face instances, each tagged with an integer index and bounding box:
   ```json
   {
     "detected_faces_count": 3,
     "face_instances": [
       { "face_index": 0, "box": {"x": 120, "y": 80, "w": 65, "h": 70}, "matched_user_id": "usr_alice", "confidence": 0.94 },
       { "face_index": 1, "box": {"x": 240, "y": 95, "w": 60, "h": 68}, "matched_user_id": "usr_bob", "confidence": 0.89 },
       { "face_index": 2, "box": {"x": 410, "y": 110, "w": 58, "h": 65}, "matched_user_id": null, "confidence": null }
     ]
   }
   ```
2. **Completeness Semantics**:
   - `detected_faces_count == 0`: **Scenery Candidate**. Categorized as `folder:Scenery`.
   - `detected_faces_count > 0 and matched_count == 0`: **Unknown Faces**. Group photo with faces, but zero enrolled matches. **Must NEVER be categorized as Scenery**. Stored in `folder:GroupPhotos` with `unidentified_faces: true`.
   - `0 < matched_count < detected_faces_count`: **Partial Match**. Some travelers recognized; others unidentified.
   - `matched_count == detected_faces_count`: **Complete Match**. All detected faces identified.
   - **Worker Failure**: If DeepFace worker times out, crashes, or returns 5xx: photo status is set to `processing_status = 'failed'`. **A worker failure must never be recorded as successful completed recognition.**
   - **Photo Recognition Architecture & Storage Layers**:
     1. **Actual Current Persisted Schema (`backend/app/models/additive.py:80–94`)**:
        - `photos` table: `photo_id`, `trip_id`, `uploader_id`, `photo_url`, `processing_status` (`'pending' | 'processed' | 'failed'`), `created_at`. It contains **NO** `detected_faces_count`, **NO** `matched_count`, and **NO** raw vectors.
        - `photo_person` table: `pp_id` (PK), `photo_id` (FK), `user_id` (FK, `nullable=False`), `confidence`. Because `user_id` is NOT NULL, only recognized trip members can be inserted. Unknown face instances cannot be stored in `photo_person` as `user_id = None`.
     2. **Worker Runtime Recognition Result**:
        - DeepFace worker (`POST /api/face/match-photo` on port 8001) processes image bytes and returns transient runtime metrics in memory: `detected_faces_count`, `matched_count`, and bounding box coordinates `[x, y, w, h]`. These exist strictly in worker runtime memory and HTTP transit payloads.
     3. **Wire Response & Frontend Metadata**:
        - In the immediate upload response (`POST /api/photos`), Panchami's router forwards `facesDetected` (from runtime worker result) and normalized tags to Nikitha's frontend.
     4. **Proposed Durable Aggregate & Face-Instance Representation**:
        - Durable persistence of aggregate face counts (`photos.detected_faces_count`, `matched_count`) and individual face instances with coordinates (`photo_face_tags` with `tag_id`, `photo_id`, nullable `user_id`, `face_index`, `bounding_box`) is an explicit **pending target schema migration** owned by Sharvani.
     5. **Honest Reload Behavior Prior to Target Migration**:
        - During initial upload, the live worker result enables full recognition categorization.
        - On subsequent gallery reload (`GET /api/photos/{trp_id}`), the server queries the database, which currently holds only `photo_person` rows and photo `processing_status`.
        - **Critical Invariant**: Absence of recognized `photo_person` tags does **NOT** mean zero detected faces. If a photo has `processing_status = 'processed'` and 0 rows in `photo_person`, the server cannot determine from database rows alone whether the image had zero faces (scenery) or un-enrolled travelers. Unknown or unavailable recognition evidence must **NEVER** be misclassified as "Scenery"!
        - Worker failure (`processing_status = 'failed'`) remains strictly distinct from successful processing with unknown travelers (`processing_status = 'processed'`). Full reload segregation of unknown faces depends on Sharvani's target schema migration.

### 4.3 Privacy & Vector Protection
- The 512-dimensional floating-point ArcFace vectors are strictly server-internal biometric data.
- Vectors must **never** be logged to stdout/stderr, written to debug logs, or included in any Pydantic response models returned to browsers.

---

## 5. Security & Authentication Handoff

| Security Dimension | Sharvani (Authority & Business Rules) | Panchami (Transport Receiver & Enforcer) |
| :--- | :--- | :--- |
| **Clerk JWT Authentication** | Implements token decoding, JWKS key fetching/caching, and claims verification in `services/clerk_auth.py`. | Extracts `Authorization: Bearer <token>` from HTTP headers. Injects verified user into route dependencies. Enforces HTTP 401 on missing/invalid token. |
| **Clerk Webhook Signature Verification** | Implements cryptographic signature verification using `svix.webhooks.Webhook(secret).verify(payload, headers)`. Executes idempotent user sync transaction. | Mounts `POST /api/auth/webhook`. Reads raw request body and headers (`svix-id`, `svix-timestamp`, `svix-signature`). Invokes Sharvani's verification in-process. Enforces HTTP 400 on signature failure. |
| **WebSocket Authentication** | Implements `verify_trip_membership(trip_id, user_id, db) -> bool`. Checks Neon DB membership. | Receives WebSocket handshake. Extracts `?token=...`. If token missing/invalid: closes with **code 4401**. If user not accepted trip member: closes with **code 4403**. |
| **Itinerary Concurrency (CAS)** | Defines atomic CAS query: `UPDATE itineraries SET version = version + 1 WHERE itinerary_id = :id AND version = :expected`. | Receives `expected_version` in request body. Calls Sharvani service in-process. If rows affected == 0, translates `VersionConflictError` to **HTTP 409 Conflict**. |

---

## 6. Service Signatures: In-Process Domain Service Contracts

Panchami's routers call Sharvani's domain services **in-process as Python function calls**, never over HTTP port 8000:

```python
# backend/app/services/trip_service.py (Sharvani)
def create_trip(db: Session, creator_user_id: str, trip_data: dict) -> Trip:
    """Creates trip shell, joins owner, creates v1 itinerary in single atomic transaction."""

def atomic_itinerary_cas_update(db: Session, trip_id: str, expected_version: int, items_delta: list[dict]) -> tuple[Itinerary, int]:
    """Applies CAS update. Raises VersionConflictError if expected_version does not match."""

# backend/app/services/voting_service.py (Sharvani)
def cast_vote(db: Session, proposal_id: str, user_id: str, value: str, comment: str | None) -> Vote:
    """Verifies membership, atomically retracts prior YES on competing proposal in same slot (AC-VOT-02), updates slot_consensus.closes_at on first NO."""

# backend/app/services/consensus_service.py (Sharvani)
def check_and_expire_timer(db: Session, proposal_id: str) -> dict:
    """Evaluates voting window against slot_consensus.closes_at. In production, evaluates `now >= slot_consensus.closes_at`. Test harness invokes isolated test fixture `test_check_and_expire_timer(..., advance_minutes)`."""

def run_consensus_round(db: Session, itm_id: str) -> dict:
    """Evaluates consensus round, runs Mode A or Mode NA orchestrator, persists revision_history / branches."""

def apply_negotiation_selection(db: Session, user_id: str, selection: dict) -> dict:
    """Validates expectedVersion (OCC) and evidenceToken (freshness/HMAC binding [TARGET_PROPOSAL]), verifies caller trip membership, and applies KEEP_ORIGINAL (caller dismiss), CLOSER_ALTERNATIVE (creates proposal for voting), or RESCHEDULE_WINDOW (Mode A owner update / Mode NA schedule proposal) in an atomic database transaction."""

# backend/app/services/photo_service.py (Sharvani)
def get_candidate_member_embeddings(db: Session, trip_id: str) -> list[dict]:
    """Queries active trip members and returns candidate user IDs with enrolled 512-d ArcFace vectors."""

def save_uploaded_photo_record(db: Session, photo_id: str, trip_id: str, uploader_id: str, photo_url: str, initial_status: str = "pending") -> Photo:
    """Inserts initial photo record with pending status."""

def save_photo_tags_records(db: Session, photo_id: str, face_matches: list[dict], final_status: str = "processed") -> list[PhotoPerson]:
    """Persists matched faces in photo_person and updates photo.processing_status to processed or failed (storage 'processed' maps to wire 'completed'; worker failure must NEVER map to 'processed' or 'completed')."""
```

---

## 7. Testing Standards: Five Rigorous Verification Tiers

1. **Tier 1: Mock Transport Tests (Owner: Panchami)**:
   - Tests FastAPI router deserialization, Pydantic validation, status codes, and error formatting using `TestClient`.
   - Uses mock domain services. Zero database, network, or DeepFace dependencies.
2. **Tier 2: Deterministic Domain Tests (Owner: Sharvani)**:
   - Tests pure math compatibility scoring (Jaccard similarity on travel styles, BCP-47 language set intersection, age-group matrix weights) and consensus state transitions.
   - Tested with static fixtures and fixed clocks.
3. **Tier 3: Real Recognition Tests with Known Images (Owner: Panchami)**:
   - Tests face detection and ArcFace matching using actual reference test images (`ai/DeepFace/tests/fixtures/`) containing real human faces at straight/left/right angles, and non-face scenery images.
   - **Verification Requirement**: Random float dummy vectors alone do **NOT** prove correct face recognition. Tests must verify true positive identification and true negative scenery rejection with real images.
4. **Tier 4: Isolated PostgreSQL Concurrency Tests (Owner: Sharvani)**:
   - Tests atomic compare-and-swap (CAS) updates and concurrent voting transactions against a real PostgreSQL database instance (Neon test branch or container).
   - **Verification Requirement**: SQLite in-memory tests alone do **NOT** prove PostgreSQL concurrency because SQLite uses database-level locks, whereas PostgreSQL uses row-level MVCC.
5. **Tier 5: Full Application Acceptance Tests (Team Chaos Minds)**:
   - End-to-end integration across frontend, backend, database, and DeepFace.
   - **Safe Isolation Rule**: Controlled integration tests may import the application (`backend.app.main:app`) after safe environment isolation (setting `DATABASE_URL` to an isolated test DB and isolating external provider APIs). We do not impose an absolute prohibition that blocks legitimate integration testing.

---

## 8. Concrete Member Task Cards & Shared Feature-Handoff Matrix

### 8.1 Nikitha M N (Frontend Track)
- [ ] **Task N-1: Mock Data-Access Layer**: Create `frontend/src/lib/data-access/client.ts`, `mock_adapter.ts`, and `fixtures/` with a fixed mock clock.
- [ ] **Task N-2: 19-Screen Offline Click-Through**: Verify all 19 screens render without error using mock data (`VITE_USE_MOCK_DATA=true`).
- [ ] **Task N-3: Accessible Form Validation Matrix**: Implement client-side validation across the 17 interactive frontend form controls (supporting the 48 backend context-specific validation rules) with `border-clay` (`#C1502E`), inline alerts, and `aria-invalid="true"`.
- [ ] **Task N-4: WCAG 2.1 AA Compliance**: Enforce 44px touch targets, visible focus rings (`focus-visible:ring-2 focus-visible:ring-route`), and `aria-live="polite"` for consensus countdown timer (Decision #31).
- [ ] **Task N-5: WebSocket Reconnect & Resync**: Update `TripContext.tsx` to handle `resyncSnapshot` and alias `aiPlanGenerated` / `aiRecommendationReady`.
- [ ] **Task N-6: Photo Gallery UI**: Wire `POST /api/photos` multipart upload and display face bounding boxes and smart folders (Decision #9).
- [ ] **Task N-7: Chat Route Alignment**: Reconcile `frontend/src/lib/api.ts` to call `GET/POST /api/trips/{trip_id}/chat` instead of `/api/trips/{trip_id}/messages`.
- [ ] **Task N-8: PDF Export Preview & Online Download UI**: Implement Itinerary PDF export preview modal (`ExportPreviewModal.tsx`), responsive printable DOM layout with `@media print` styling, and online export download lifecycle against backend endpoint (`FR-EXP-01`; Decision #30 pending renderer selection). Fixture-backed preview serves as development support; offline PDF export is deferred and NOT a completion gate.
- [ ] **Task N-9: Cross-Member Loading & Clerk Profiling (Frontend)**: Profile DOM render times, eliminate sequential request waterfalls on Trip Home, verify loading skeletons, and measure Clerk SDK session hydration.

### 8.2 Panchami P (Transport & DeepFace Track)
- [ ] **Task P-1: Router Validation Tightening**: Reconcile all Pydantic schemas in `backend/app/schemas/` to enforce camelCase wire aliases and strict field types.
- [ ] **Task P-2: Multipart Binary Photo Forwarding**: Refactor `POST /api/photos` to fetch candidate embeddings from Sharvani in-process and stream real multipart image bytes + candidate vectors payload to DeepFace worker on port 8001 (Decision #9).
- [ ] **Task P-3: Face Recognition Completeness & Failure Handling**: Implement instance-counting face logic (`face_index`, `detected_faces_count` vs `matched_count`); record `processing_status = 'failed'` on worker error.
- [ ] **Task P-4: Exact Three-Person Real Image Regression Test Suite**: Execute `ai/DeepFace/tests/` using real reference images of 3 distinct enrolled individuals, individual/group photos, 1 unknown person, and 1 scenery photo. Verify ArcFace 512-d embeddings, prototype score threshold ($\ge 0.90$), multi-face instance separation, and zero false cross-person tags.
- [ ] **Task P-5: WebSocket Connection Lifecycle**: Enforce close codes 4401 (invalid token) and 4403 (unauthorized member); send `resyncSnapshot` upon connection.
- [ ] **Task P-6: Photo Persistence Handoff**: Wire `POST /api/photos` to call Sharvani's `save_uploaded_photo_record` and `save_photo_tags_records` in-process with unified signatures.
- [ ] **Task P-7: Timer & Chat Route Exposure**: Mount `POST /api/proposals/check-timer` and `GET/POST /api/trips/{trip_id}/chat` with clean schemas. Active vote route is `POST /api/votes`.
- [ ] **Task P-8: Zero-Dependency Mock Router Test Suite**: Build isolated transport test suite using `FakeConsensusService`, `FakeTripService`, dependency injection seams, and mock auth dependency overrides with ZERO database, ZERO LLM, and ZERO worker dependencies. Verify Ollama is NOT a teammate prerequisite.
- [ ] **Task P-9: Cross-Member Loading & Clerk Profiling (Transport)**: Profile router endpoint round-trip latencies, WebSocket connection handshake latency, and Clerk webhook Svix signature verification latency (`[PROPOSED TARGET]`: $< 15\text{ms}$).

### 8.3 Sharvani G Bhaskar (Architecture, Domain, AI & Deployment Authority)
- [ ] **Task S-1: App Lifecycle & Deployment Coordination**: Own `backend/app/main.py`, router mounts, and all deployment coordination across Render (backend & DeepFace) and Vercel (frontend).
- [ ] **Task S-2: Domain Service Extraction**: Prepare domain service modules in `backend/app/services/` (`trip_service`, `voting_service`, `consensus_service`, `matching_service`, `photo_service`, `audit_service`) matching unified signatures.
- [ ] **Task S-3: Security Core Extraction**: Extract Clerk JWT claims verification and Svix webhook signature validation into `backend/app/core/security.py` (proposed modular extraction).
- [ ] **Task S-4: Atomic CAS Concurrency Implementation**: Implement atomic `WHERE version = :expected` update query and single-active-YES auto-retraction (`AC-VOT-02`).
- [ ] **Task S-5: Slot-Level Consensus Timer**: Implement slot-level countdown state machine (`slot_consensus.closes_at`) without test `advance_minutes` parameters in production contract (Decision #31).
- [ ] **Task S-6: Isolated PostgreSQL Concurrency Tests**: Build multi-threaded integration test verifying CAS conflict rejection (HTTP 409) on real PostgreSQL (Decision #16).
- [ ] **Task S-7: Deterministic Scorers Unit Tests**: Verify pure math Jaccard and cosine scoring algorithms with 100% deterministic test assertions (Decision #26).
- [ ] **Task S-8: PDF Rendering Architecture & Server-Side Compiler**: Finalize Decision #30. If server-side rendering is selected, implement Jinja2 + WeasyPrint HTML-to-PDF compilation service consuming authoritative JSON export payload.
- [ ] **Task S-9: Neon Database Environment Preparation & Small Bounded Fixture Delivery**: Provision isolated integration database on Neon PostgreSQL, run Alembic migrations up to head (`c8a6a4789a32`), seed agreed small bounded fixture (`usr_alice`, `usr_bob`, `usr_carol`, `trp_paris_2026`), and deliver connection instructions for `.env.local`.
- [ ] **Task S-10: Cross-Member Loading & Clerk Profiling (Domain & DB)**: Profile database queries to eliminate N+1 round-trips via eager loading, evaluate LLM operational timeouts (`[PROPOSED TARGET]`: 8s–10s ceiling, Decision #28), profile Clerk user sync atomic transactions, and add structured `elapsed_ms` logging.

---

### 8.4 Comprehensive Shared Feature-Handoff Matrix (All 17 Features)

| # | Feature Scope | Nikitha UI Request & Interaction | Endpoint (Current vs Proposed) | Panchami Transport DTO & Wire Checks | Trusted Actor Context | Sharvani Domain Service & Authority | Authoritative Data Source | Business Validation & Transaction Owner | Success Result & Wire Response | Typed Errors & HTTP Status Mapping | Event / Refresh Behavior | Frontend Rendering & UI Display | Mock Scenario (Level 1) | Real Integration Prerequisite (Level 4) | Owned Files & Exclusions |
|:--|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **1** | **Authentication & User Sync** | Clerk `<SignIn />` / `<SignUp />` components. Obtains session JWT. | `POST /api/auth/webhook` (`[CURRENT]`) | Validates Svix headers (`svix-id`, `svix-timestamp`, `svix-signature`). | Svix signature verified against webhook secret. | `security.sync_clerk_user_to_db(db, event_data)` | Clerk webhook payload | Atomic transaction creates `User` & default `UserPreference`. Sharvani owns txn. | `{"status": "success", "userId": "usr_..."}` | Invalid Svix signature -> `400 Bad Request`. Duplicate event -> `200 OK` (idempotent). | Server webhook synchronizes profile into PostgreSQL; browser session JWT and cookie are managed directly between browser and Clerk SDK (`<ClerkProvider>`). | User avatar & name in top navbar. Sign-out button. | Mock user in `AuthContext.tsx` with fixed ID `usr_test_nikitha`. | Clerk webhook secret configured; Neon DB seeded. | Panchami: `routers/auth.py`. Sharvani: `services/clerk_auth.py`, `models/`. Nikitha: `AuthContext.tsx`. |
| **2** | **Trip Discovery & Listing** | My Trips page (`/trips`). Discover page (`/discover`). | `GET /api/trips` & `GET /api/trips/discover` (`[CURRENT]`) | Deserializes query filters. Validates `Authorization: Bearer <token>`. | `current_user.user_id` from JWT. | `trip_service.list_user_trips(db, user_id)` & `discover_public_trips(db)` | `trips`, `trip_members` tables | Filters by active membership or `visibility = 'public'`. Read-only. | `{"trips": [TripResponseDTO]}` (camelCase wire fields). | Expired token -> `401 Unauthorized`. Backend timeout -> `504`. | Pull-to-refresh or route navigation trigger. | Grid of Trip Cards (destination hero image, mode pill, member avatars). | `mock_adapter.ts` returns array of 3 sample trips. | Neon DB running with seeded trips for `usr_alice`. | Panchami: `routers/trips.py`. Sharvani: `services/trip_service.py`. Nikitha: `screens/MyTripsScreen.tsx`. |
| **3** | **Trip Creation & Publishing** | Create Trip modal (`/trips/new`). Form validation on destination, dates, mode. | `POST /api/trips` & `PATCH /api/trips/{id}/publish` (`[CURRENT]`) | `CreateTripRequest` schema. Enforces required title, valid date range. | Authenticated caller becomes `owner_user_id`. | `trip_service.create_trip(db, user_id, data)` & `publish_trip(db, id, user_id)` | Neon DB `trips` table | Validates start_date <= end_date, valid governance mode (`'Mode NA'` or `'Mode A'`). Sharvani owns txn. | `TripResponseDTO` (`tripId`, `ownerUserId`, `status: "draft" / "published"`). | Invalid dates -> `422 Unprocessable`. Non-owner publish -> `403 Forbidden`. | Emits `tripCreated` event or client navigates to `/trips/:id`. | Redirects to Trip Home (`/trips/:trpId`) with Route Line initialized. | `mock_adapter.ts` appends new trip to local array. | Neon migration `c8a6a4789a32` applied. | Panchami: `routers/trips.py`. Sharvani: `services/trip_service.py`. Nikitha: `screens/CreateTripModal.tsx`. |
| **4** | **Membership, Joins & Invites** | Share Invite Code dialog. Join Request button on public trip. | `POST /api/trips/{id}/join` & `POST /api/trips/{id}/members` (`[CURRENT]`) | `JoinRequestDTO` & `AddMemberDTO`. Validates code format or target user ID. | `current_user.user_id`. | `trip_service.add_trip_member(db, trip_id, inviter_id, target_id)` | `trip_members`, `trip_invite_codes` | Checks group capacity (Decision #21), active invite code validity, duplicate member checks. | `{"status": "joined", "role": "member", "tripId": "trp_..."}` | Max capacity reached -> `409 Conflict`. Invalid code -> `404 Not Found`. | Broadcasts `memberJoined` to WebSocket room. | Member avatar stack in hero header updates in real-time. | `mock_adapter.ts` returns success state. | Database unique constraint on `(trip_id, user_id)`. | Panchami: `routers/trips.py`. Sharvani: `services/trip_service.py`. Nikitha: `screens/TripHomeScreen.tsx`. |
| **5** | **Itinerary Reads & Writes** | Add Itinerary Item form. Renders timeline slots on Trip Home. | `GET /api/trips/{id}` & `POST /api/trips/{id}/itinerary` (`[CURRENT]`) | `ItineraryItemCreateDTO`. Validates day number, time window, cost >= 0. | Verified trip member. | `trip_service.add_itinerary_item(db, trip_id, user_id, data)` | `itinerary_items`, `slot_consensus` | Validates time slot availability. Initializes slot consensus record with `status='draft'`. Sharvani owns txn. | `ItineraryItemDTO` (`slotId`, `title`, `timeWindow`, `status`). | Overlapping slot -> `400 Bad Request`. Non-member write -> `403 Forbidden`. | Broadcasts `itineraryUpdated` event. | Renders new slot card on Route Line timeline with Amber/Green status. | Mock timeline returns 4 predefined day slots. | Neon DB foreign keys on `trip_id`. | Panchami: `routers/trips.py`. Sharvani: `services/trip_service.py`. Nikitha: `components/SlotCard.tsx`. |
| **6** | **Proposal Creation & History** | Propose Activity modal. Alternate proposal button on slot card. | `POST /api/proposals` & `GET /api/slots/{id}/proposals` (`[CURRENT]`) | `CreateProposalRequest`. Enforces title, entity_type, cost_delta. | `current_user.user_id` as `proposer_id`. | `trip_service.submit_proposal(db, slot_id, user_id, data)` | `proposals` table | Validates target slot exists, proposal state is `open`. Sets initial version = 1. Sharvani owns txn. | `ProposalResponseDTO` (`proposalId`, `slotId`, `status: "open"`, `version: 1`). | Slot already confirmed -> `409 Conflict`. Invalid entity -> `422 Unprocessable`. | Broadcasts `proposalCreated` via WebSocket. | Alternate proposal card appears nested under target timeline slot. | Mock proposals loaded from fixture. | Proposals table indexed on `(slot_id, trip_id)`. | Panchami: `routers/trips.py`. Sharvani: `services/trip_service.py`. Nikitha: `screens/ProposeActivityModal.tsx`. |
| **7** | **Votes, Switching & Retraction** | Vote Pill interaction (YES / NO / RETRACT). Single active YES. | `POST /api/votes` (`[CURRENT]`) | Legacy current: `CastVoteRequest(proposal_id, user_id, value, comment, weight)`. Target trusted contract: `CastVoteRequest(proposal_id, value, comment)` with caller identity derived from verified JWT `current_user.user_id` and weight defaulting to 1.0 (or domain-calculated based on role; never arbitrary client input). | `current_user.user_id` from verified JWT. | `voting_service.cast_vote(db, proposal_id, user_id, value, comment, weight)` | `votes` table | Atomic CAS update: retracts prior active YES on same slot (`AC-VOT-02`). Checks electorate eligibility. Sharvani owns txn. | `{"status": "recorded", "voteId": "vot_...", "proposalId": "prp_..."}` | Slot closed -> `409 Conflict`. Invalid vote value -> `422 Unprocessable`. | Broadcasts `voteCast` (`trpId`, `itmId`, `prpId`, `usrId`, `value`, `comment`). | Vote pill updates color (Green YES / Clay NO). Electorate vote count increments. | `FakeConsensusService` updates in-memory vote dictionary. | PostgreSQL unique constraint on `(proposal_id, user_id)`. | Panchami: `routers/consensus.py`. Sharvani: `services/voting_service.py`. Nikitha: `components/VotePill.tsx`. |
| **8** | **Consensus Timers & Mode NA Auto-Reconcile** | 10-minute slot countdown timer. Auto-confirms when timer expires with 0 NO votes. | `POST /api/proposals/check-timer` & `POST /api/consensus/reconcile` (`[CURRENT]`) | `CheckTimerRequest(prp_id)`. `advance_minutes` restricted strictly to tests. | System timer or triggered by trip member. | `consensus_service.check_and_expire_timer(db, proposal_id)` | `proposals`, `votes`, `slot_consensus` | Evaluates `now >= closes_at`. If `no_votes == 0`, marks proposal `accepted` and slot `confirmed`. | `{"proposalId": "prp_...", "status": "confirmed", "expired": true}` | Proposal not found -> `404`. Timer not expired -> `200` with `status: "active"`. | Broadcasts `slotStatusChanged` (`slot_status: "confirmed"`). | Slot card background turns soft Green; status badge displays "Confirmed". | `FakeConsensusService` simulates timer expiration deterministically. | Neon DB `slot_consensus.closes_at` timestamp check. | Panchami: `routers/consensus.py`. Sharvani: `services/consensus_service.py`. Nikitha: `components/CountdownTimer.tsx`. |
| **9** | **Mode A Owner Admin Actions** | Admin action bar: "Accept Blended Plan", "Force Branch Now", "Extend Round". | `POST /api/consensus/mode-a/{action}` (`[CURRENT]`) | `ModeAActionDTO(itm_id, action)`. Validates action enum. | `current_user.user_id == trip.owner_user_id`. | `consensus_service.execute_mode_a_admin_action(db, item_id, action, owner_id)` | `trips`, `slot_consensus`, `branches` | Enforces Mode A governance rules. Rejects actions by non-owner members (`403 Forbidden`). | `{"status": "executed", "action": "force_branch", "branchId": "brn_..."}` | Non-owner caller -> `403 Forbidden`. Invalid slot state -> `409 Conflict`. | Broadcasts `slotStatusChanged` or `branchCreated`. | Renders admin badge and reveals Branch View link. | Mock admin controls toggled via mock role. | Mode A check against `trips.mode == 'Mode A'`. | Panchami: `routers/consensus.py`. Sharvani: `services/consensus_service.py`. Nikitha: `screens/TripHomeScreen.tsx`. |
| **10** | **AI Clarifications & Candidate Negotiation** | Dissent clarification input drawer. Suggestion chips on slot card. | `POST /api/slots/{slot_id}/clarify` (`[PROPOSED TARGET / MISSING IMPLEMENTATION]`) | 6-field envelope: `tripId`, `slotId`, `commentId`, `clarificationText`, `expectedVersion`, `evidenceToken`. Validates `url.slot_id == body.slotId`. | Dissenting voter identity (`current_user.user_id`). | `consensus_service.submit_clarification(db, slot_id, comment_id, user_id, text, version, token)` | `votes.comment`, evidence cache | OCC concurrency check on `itineraries.version`. Enforces evidence token freshness (Decision #12). Sharvani owns txn. | `{"status": "CLARIFICATION_ACCEPTED", "slotId": "itm_...", "commentId": "com_...", "cycle": 1, "round": 1}` | Structural mismatch -> `400` (`ERR_SLOT_ID_MISMATCH`). Non-author -> `403` (`ERR_NOT_COMMENT_AUTHOR`). Stale version -> `409` (`ERR_STALE_VERSION`). Token expired/tampered -> `422` (`ERR_TOKEN_EXPIRED` / `ERR_EVIDENCE_INVALID`). Missing field -> `422` (`ERR_MISSING_FIELD`). | Broadcasts `clarificationSubmitted` (`type: "clarificationSubmitted", trpId: "...", itmId: "...", slotId: "...", usrId: "...", commentId: "...", cycle: 1, round: 1`). Initiates async compromise generation. | Renders clarification chip on voter's objection card. | `FakeConsensusService` returns canonical `CLARIFICATION_ACCEPTED` status (omits fabricated version bump). | Concurrency check on `itineraries.version` (OCC guard). | Panchami: `routers/consensus.py`. Sharvani: `services/consensus_service.py`. Nikitha: `screens/ConflictResolutionPanel.tsx`. |
| **11** | **Recursive Branching & Partitions** | Branch View screen (`/branches/:itmId`). Join Branch button. | `GET /api/branches/{itm_id}` & `POST /api/branches/{id}/join` (`[CURRENT]`) | `BranchQueryDTO` & `JoinBranchRequest`. | Trip member choosing branch option. | `consensus_service.confirm_branch_member(db, branch_id, user_id)` | `branches`, `branch_members` tables | Enforces parent branch hierarchy. Validates branch membership bounds. Sharvani owns txn. | `{"branchId": "brn_...", "memberCount": 3, "status": "active"}` | Branch closed -> `409 Conflict`. Unauthorized parent -> `400 Bad Request`. | Broadcasts `branchMemberJoined`. | UI splits timeline into parallel sub-routes with amber branch markers. | Mock branch fixture loads two alternate paths. | Parent branch foreign key validation in Neon DB. | Panchami: `routers/consensus.py`. Sharvani: `services/consensus_service.py`. Nikitha: `screens/BranchViewScreen.tsx`. |
| **12** | **Trip Chat & Chat-to-Proposal** | Collapsible Trip Chat drawer. "Propose this" action on chat messages. | `GET /api/trips/{id}/chat` & `POST /api/trips/{id}/chat` (`[CURRENT]`) | `ChatMessageDTO(message_text)`. Canonical `/chat` endpoints. | Trip member. | `trip_service.post_chat_message(db, trip_id, user_id, text)` | `chat_messages` table | Sanitizes input text (max length bounds, Decision #20). Sharvani owns txn. | `ChatMessageResponseDTO` (`msgId`, `senderName`, `text`, `createdAt`). | Empty text -> `422 Unprocessable`. Non-member -> `403 Forbidden`. | Broadcasts `newChatMessage` to trip WebSocket room. | Chat bubble appears in real-time in chat rail with sender avatar. | In-memory message store in `TripContext.tsx`. | Neon `chat_messages` table indexed on `trip_id`. | Panchami: `routers/trips.py`. Sharvani: `services/trip_service.py`. Nikitha: `components/TripChatDrawer.tsx`. |
| **13** | **Solo & Guide Matchmaking** | Solo Match screen (`/solo`). View guide compatibility scores. | `POST /api/solo-matching/groups` & `POST /api/solo-matching/guides` (`[CURRENT]`) | `SoloMatchRequestDTO`. Validates budget range, travel style preferences. | Authenticated solo traveler. | `matching_service.match_groups(...)` & `match_guides(...)` | `user_preferences`, `tour_guides` | Pure math deterministic Jaccard & cosine scoring algorithms. Read-only. | `{"matches": [GroupMatchDTO], "bestGuide": GuideMatchDTO}` | No preferences configured -> `400 Bad Request`. | On-demand calculation; no WebSocket broadcast. | Compatibility score badges (e.g. "94% Match") on group and guide cards. | Mock scores returned from static fixture. | Guide profiles seeded in `tour_guides` table. | Panchami: `routers/trips.py`. Sharvani: `services/matching_service.py`. Nikitha: `screens/SoloMatchScreen.tsx`. |
| **14** | **Face Profile Enrollment** | Optional 3-angle face capture modal on signup/profile. | `POST /api/face/register` & `GET /api/face/status/{id}` (`[CURRENT]`) | `RegisterFaceRequest(images: [3])`. Validates exactly 3 photos provided. | `current_user.user_id`. | `photo_service.enroll_face_profile(db, user_id, vectors)` | `face_profiles` table | Quality check: exactly 1 face per image. Generates 512-d ArcFace vector. Atomic failure. | `{"status": "registered", "userId": "usr_...", "registeredAt": "..."}` | 0 or >1 face in image -> `400 Bad Request`. Worker timeout -> `504`. | Updates user's face enrollment status flag. | "Face Profile Enrolled" checkmark badge shown in user profile. | Mock enrollment succeeds with stubbed status. | ArcFace model weights available to DeepFace worker. | Panchami: `routers/face.py`. Sharvani: `services/photo_service.py`. Nikitha: `screens/SignUpScreen.tsx`. |
| **15** | **Photo Upload, Streaming & Face Tags** | Photo upload button on Trip Photos tab. Smart folder navigation. | `POST /api/photos` (`[CURRENT]`) | Multipart form: `file: UploadFile`, `trpId: str`. | Trip member (`current_user.user_id`). | `photo_service.get_candidate_member_embeddings`, `save_uploaded_photo_record`, `save_photo_tags_records` | `photos`, `photo_person` (current) / `photo_face_tags` (target) | Scopes candidates strictly to trip members. DeepFace worker extracts 512-d vector and computes matches. Database storage status `'processed'` maps to wire `"completed"`. (Worker failure must NEVER map to `'processed'` or `"completed"`). Consumes `normalize_photo_tag_record`. | `{"photoId": "pho_...", "processingStatus": "completed", "facesDetected": 2}` | Non-member uploader -> `403 Forbidden`. Invalid file -> `422`. DeepFace timeout -> `504 Gateway Timeout`. | No WebSocket broadcast (absent from §2.3 catalog); frontend updates gallery from HTTP response payload or refreshes via `GET /api/photos/{trp_id}` (supported mounted route; `GET /api/photos?trpId=...` is an unmounted `[PROPOSED ALIAS]`). | Uploaded photo rendered in gallery with face bounding boxes and member pills. | Mock upload returns preset photo record with 2 tags. | DeepFace worker running on port 8001; Neon candidate embeddings. | Panchami: `routers/photos.py`. Sharvani: `services/photo_service.py`. Nikitha: `screens/MemoriesScreen.tsx`. |
| **16** | **Itinerary Audit Trail & Restore** | Version History drawer. "Restore This Revision" action. | `GET /api/trips/{id}/history` & `POST /api/trips/{id}/revisions/{rev}/restore` (`[CURRENT]`) | `RestoreRevisionDTO`. Validates revision ID. | Trip owner or authorized editor. | `audit_service.restore_itinerary_revision(db, trip_id, rev_id, user_id)` | `revision_history` table | Verifies snapshot integrity. Overwrites active slot items with archived snapshot. Sharvani owns txn. | `{"status": "restored", "revisionId": "rev_...", "restoredAt": "..."}` | Revision not found -> `404`. Non-owner restore -> `403 Forbidden`. | Broadcasts `itineraryUpdated` and `resyncSnapshot` (on reconnect). | Entire timeline updates reactively to match restored revision state. | Mock audit log displays 3 historical revisions. | `revision_history.snapshot_data` populated in Neon DB. | Panchami: `routers/trips.py`. Sharvani: `services/audit_service.py`. Nikitha: `screens/AuditHistoryScreen.tsx`. |
| **17** | **Online Itinerary PDF Export** | "Export Itinerary PDF" button on Resolved screen. Export preview modal. | `GET /api/trips/{id}/itinerary/export` (`[PROPOSED TARGET / MISSING IMPLEMENTATION]`) / `.pdf` (`[PROPOSED]`) | `ExportQueryDTO`. Validates trip ID and confirmed itinerary status. | Trip member (`current_user.user_id`). | `trip_service.get_itinerary_export_data` (data) + WeasyPrint (server-side, proposed) | Neon DB confirmed slots | Access check: user is member. Verifies all slots confirmed. Generates authoritative export JSON or PDF binary. | Authoritative JSON payload (client-side) OR binary PDF stream with `Content-Disposition: attachment`. | Slots unconfirmed -> `409 Conflict`. Trip not found -> `404`. Timeout -> `504`. | No broadcast; direct user download stream. | Browser triggers download of `wander-match-itinerary.pdf` via blob URL. | Fixture-backed preview loads `export_itinerary_pdf_preview.json`. | Resolved trip with all slots confirmed in Neon DB. | Panchami: `routers/trips.py`. Sharvani: `services/trip_service.py`. Nikitha: `screens/ResolvedItineraryScreen.tsx`. |

---

## 9. Five Focused Handoff Workflows & Shared Protocols

### 9.1 PDF Export Architecture & Online Export Protocol
1. **Agreed Online Scope & Deferred Offline Generation**:
   - PDF export is **REQUIRED and ONLINE** (`FR-EXP-01`). Offline PDF generation/export is **DEFERRED** and is NOT an acceptance gate. (Earlier audit instructions requesting mandatory offline PDF acceptance are superseded by this human clarification).
   - Ordinary independent frontend mock development remains required. Nikitha uses `mock_adapter.ts` with fixture `export_itinerary_pdf_preview.json` to iterate on the preview modal and print styling without live backend dependencies. This serves as development support, but working offline export is NOT a completion gate.
2. **Nikitha's Concrete Deliverables**:
   - Owns the export preview modal (`ExportPreviewModal.tsx`), responsive printable DOM layout, print stylesheet (`@media print`), download loading and error states, and client download lifecycle against the agreed online endpoint.
   - Deliverable is NOT reduced to a button alone; Nikitha owns the complete preview, layout, and client download orchestration.
3. **Pending Renderer Strategy (Decision #30)**:
   - Decision #30 (PDF Rendering Strategy) remains **PENDING** between client-side generation (`@react-pdf/renderer` / `jspdf`) and server-side compilation (FastAPI WeasyPrint / ReportLab).
   - Neither engine is approved yet; all named libraries and routes (`/api/v1/...`) are **PROPOSED**.
4. **Conditional Roles Under Pending Decision #30**:
   - **If Client-Side**: Sharvani provides authoritative JSON export payload; Nikitha bundles the browser renderer and generates the PDF blob in-memory.
   - **If Server-Side**: Sharvani owns data authorization and executes server-side HTML-to-PDF compilation; Panchami mounts the binary streaming transport endpoint (`GET /api/trips/{trip_id}/itinerary/export.pdf` [proposed]) with `Content-Type: application/pdf` and `Content-Disposition: attachment; filename="wander-match-itinerary.pdf"`; Nikitha triggers browser download via `window.URL.createObjectURL(blob)`.
5. **Business & Edge Cases Handled**:
   - **Access Check**: Caller must be an authorized trip member (`403 Forbidden` if unauthorized).
   - **Itinerary Completeness**: Rejects export if any slot is in draft or active voting (`409 Conflict: "Cannot export itinerary with unconfirmed slots"`).
   - **Content Length & Layout**: Print stylesheet cleanly handles multi-day itineraries with page-break controls (`break-inside-avoid`).
   - **Failure Resilience**: Explicit UI error banners for network timeouts (`HTTP 504 Gateway Timeout`) with an accessible retry button.

### 9.2 Independent Transport Testing with Zero-Dependency Fakes & LLM Isolation
1. **Unified Authoritative Signatures Across Tracks**:
   - `submit_clarification(db: Session, slot_id: str, comment_id: str, user_id: str, text: str, version: int, token: str) -> Dict[str, Any]` (callers passing dict payloads use an adapter to unpack arguments).
   - `save_uploaded_photo_record(db: Session, photo_id: str, trip_id: str, uploader_id: str, photo_url: str, initial_status: str = "pending") -> Photo`.
   - `save_photo_tags_records(db: Session, photo_id: str, face_matches: List[Dict[str, Any]], final_status: str = "processed") -> List[PhotoPerson]` (production ORM) / `List[Dict[str, Any]]` (protocols/fakes).
     * Service-Facing DTO Normalizer (`normalize_photo_tag_record`):
       Both production ORM records (`PhotoPerson`) and fake test records (`Dict[str, Any]`) are normalized by the transport layer before wire serialization to guarantee identical field access (`tagId`, `photoId`, `userId`, `confidence`, `box`):
       ```python
       def normalize_photo_tag_record(record: Union[PhotoPerson, Dict[str, Any]]) -> Dict[str, Any]:
           """Authoritative adapter normalizing both production SQLAlchemy PhotoPerson ORM records
           and FakePhotoService dictionary records into an identical service-facing DTO shape before wire serialization."""
           if isinstance(record, dict):
               # Fake dictionary record: must provide explicit identifier (pp_id or tagId/tag_id) and photo_id
               tag_id = record.get("pp_id") or record.get("tagId") or record.get("tag_id")
               photo_id = record.get("photo_id") or record.get("photoId")
               if not tag_id or not photo_id:
                   raise ValueError(f"ERR_INVALID_TAG_RECORD: Missing required identity (pp_id/tagId or photo_id) in {record}")
               return {
                   "tagId": str(tag_id),
                   "photoId": str(photo_id),
                   "userId": record.get("user_id") or record.get("userId"),  # str for recognized traveler; None only in proposed unknown instance
                   "confidence": float(record.get("confidence", 0.0)),
                   "box": record.get("box") or record.get("bounding_box")  # Optional[Dict[str, int]]; None if absent
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
                   "userId": str(record.user_id),  # Current PhotoPerson.user_id is NOT NULL (recognized trip member)
                   "confidence": float(record.confidence) if record.confidence is not None else 0.0,
                   "box": None  # Current photo_person schema lacks bounding_box column; represented honestly as None (not fabricated)
               }
       ```
     * Concrete Router Invocation Step:
       ```python
       persisted_tags = sharvani_photo_service.save_photo_tags_records(db=db, photo_id=photo_id, face_matches=matches.tags, final_status=storage_status)
       normalized_tag_dtos = [normalize_photo_tag_record(t) for t in persisted_tags]
       wire_status = "completed" if storage_status == "processed" else "failed"
       ```
     * Storage-to-Wire Status Mapping: Database storage status `'processed'` maps to wire `"completed"`; database storage `'failed'` maps to wire `"failed"`; worker timeout/failure must NEVER map to `'processed'` or `"completed"`. Unmatched faces with `detected_faces_count > 0` are marked `'processed'` in storage and `"completed"` on wire with `unidentified_faces = True`.
2. **FastAPI Domain-Service Dependency Injection Seam (`[TARGET ARCHITECTURE]`)**:
   - Routes obtain domain services via FastAPI dependencies: `Depends(get_consensus_service)`, `Depends(get_trip_service)`, `Depends(get_photo_service)`.
   - In production, these return Sharvani's domain modules. In test suites, tests override them with `FakeConsensusService` or `FakeTripService`.
3. **Standalone Test Composition & Mock-Auth Attribute Compatibility**:
   - Router routes access caller identity via `current_user.user_id` (attribute access). The mock-auth override must return an object with attribute access (e.g. `SimpleNamespace(user_id="usr_test_panchami", clerk_user_id="user_clerk_panchami", email="panchami@example.com", display_name="Panchami", status="active")`), NOT a raw dictionary.
   - Current import location: `from backend.app.services.clerk_auth import get_current_user` and `from backend.app.database import get_db`. Note that `core/security.py` and `dependencies.py` are PROPOSED future extractions.
   - Test composition mounts the router directly in a fresh `FastAPI` instance with mocked dependencies, preventing application startup hooks that create database tables or seed data. (Note: `consensus.router` already declares `prefix="/api"` internally in `consensus.py:16`; do NOT pass redundant `prefix="/api"` on `test_app.include_router(consensus.router)`). Router refactoring to consume `Depends(get_consensus_service)` is an explicit target architecture prerequisite.
4. **Deterministic Fake Scenarios**:
   - Success (200/201), Validation Error (422), Unauthorized Non-Member (403), Stale Version (409), Duplicate Identical Request (200 idempotent), Conflicting Replay (409), In-Progress Synthesis (202 `in_consensus`), Worker Timeout (504), and Baseline Proposal Preservation.
5. **Teammate LLM Isolation Prerequisite**:
   - **Consensus SLM/LLM installation (Ollama / Phi-4-mini) is strictly owned by Sharvani**. Teammates require ZERO local Ollama installations.
6. **The Four Verification Levels**:
   - Level 1: Panchami transport & schema testing with in-memory fakes (zero DB, zero LLM, zero worker).
   - Level 2: Panchami DeepFace worker real-image recognition tests with isolated local storage.
   - Level 3: Sharvani domain business logic, CAS concurrency, and deterministic math scorers.
   - Level 4: Feature-by-feature integration connecting real route → domain service → isolated Neon PostgreSQL.

### 9.3 Small Bounded Neon Database Environment Handoff Protocol
1. **Sharvani's Provisioning Responsibility**:
   - Sharvani provisions the isolated nonproduction Neon PostgreSQL database target, runs Alembic migrations up to agreed baseline revision `c8a6a4789a32` (or current `head`), and seeds the agreed small, bounded test fixture.
2. **Small Bounded Test Fixture Details**:
   - **Synthetic Users**: `usr_alice` (`role='owner'`), `usr_bob` (`role='editor'`), `usr_carol` (`role='viewer'`) (mapped to canonical `TripMember.role` values `owner / editor / viewer`).
   - **Synthetic Trips**: `trp_paris_2026` ("Paris Weekend", Mode NA, published), `trp_tokyo_admin` ("Tokyo Explorer", Mode A, draft).
   - **Representative Slots**: `slt_day1_morning` ("Louvre Guided Tour", 09:00–12:00, 30.00 USD), `slt_day1_lunch` ("Le Marais Bistro", 12:30–14:00, 25.00 USD).
   - **Representative Proposals & Votes**: `prp_louvre_guided` with initial YES votes from `usr_alice` and `usr_bob`.
   - **Minimal Photo Metadata**: `pho_sample_1` (`trip_id: trp_paris_2026`, `uploader_id: usr_alice`, `photo_url: /static/uploads/pho_sample_1.jpg`).
3. **Explicit Environment Loading**:
   - Python / FastAPI does **NOT** automatically load `.env.local` by default unless configured via `python-dotenv` (`load_dotenv(".env.local")`) or shell environment variables. Nonproduction credentials must be shared privately; no secrets in version control.
4. **Console Collaboration vs Database-Role Access**:
   - Panchami receives direct database connection credentials (`DATABASE_URL=postgresql://panchami_dev:...@...neon.tech/wandermatch_test?sslmode=require` or `postgresql+psycopg2://...`); no shared personal Neon account login is required. (Note: `backend/app/database.py` initializes a synchronous SQLAlchemy `create_engine` using `psycopg2-binary`. The asynchronous prefix `postgresql+asyncpg://` is an unapproved future proposal that is incompatible with the present synchronous backend engine; Panchami uses the synchronous driver string matching `psycopg2-binary`).
5. **Feature-by-Feature Integration**:
   - Real integration proceeds feature-by-feature; mock transport development and router unit testing must **NEVER wait** for live Neon database access.

### 9.4 Cross-Member Loading & Clerk Performance Investigation Protocol
A cross-cutting engineering task to diagnose reported loading bottlenecks on Trip Home and Clerk user authentication:
1. **Frontend Track (Nikitha)**:
   - Measures DOM render and hydration timing, eliminates sequential request waterfalls, verifies loading skeletons (`[PROPOSED TARGET]`: maintain CLS < 0.05), and profiles Clerk React SDK session hydration (`useAuth().getToken()`).
2. **Transport Track (Panchami)**:
   - Profiles router endpoint round-trip durations, WebSocket handshake latency, and Clerk webhook Svix signature verification latency (`[PROPOSED TARGET]`: Svix verification executes in $< 15\text{ms}$).
3. **Domain, Database & AI Track (Sharvani)**:
   - Profiles database queries to eliminate N+1 round-trips via eager loading (`joinedload`/`selectinload`), evaluates LLM operational timeouts (`[PROPOSED TARGET]`: 8s–10s ceiling, Decision #28), profiles atomic Clerk user sync transactions, and adds structured `elapsed_ms` logging.
4. **Standardized Triage Lifecycle**:
   - Every performance finding must record: **Baseline (ms)** → **Reproduction Steps** → **Measured Bottleneck (ms)** → **Evidence** → **Chosen Fix** → **Verification**. Speculative diagnoses are prohibited prior to profiling.
5. **Privacy & Security during Instrumentation**:
   - Instrumentation code must **NEVER** log JWT tokens, user passwords, biometric facial embeddings, or raw traveler objection comments.

### 9.5 Exact Three-Person Face Recognition Regression Test Case
Translates the reported face grouping failure into a concrete, reproducible test suite:
1. **Test Dataset**:
   - 3 enrolled individuals: Person A (Nikitha), Person B (Panchami), Person C (Sharvani), each providing 3-angle enrollment vectors (Straight, Left Tilt, Right Tilt).
   - Individual photos of A, B, C; multi-person group photos (A+B, B+C, A+B+C); 1 unknown person (Person D, un-enrolled); 1 scenery photo (0 faces).
2. **Recognition Metric Calibration Reality**:
   - DeepFace matching evaluates three distinct mathematical quantities:
     1. **Raw Cosine Similarity**: $S_{\text{cos}} \in [-1, 1]$.
     2. **Cosine Distance**: $D_{\text{cos}} = 1 - S_{\text{cos}}$ (DeepFace default ArcFace distance threshold is 0.68, equivalent to raw similarity 0.32).
     3. **Prototype Transformed Heuristic Score**: The prototype in `matching.py` maps raw similarity 0.45 to heuristic score 0.90, comparing against `CONFIDENCE_THRESHOLD = 0.90`.
   - **Evidentiary Honesty**: A heuristic score is NOT a probability or a mathematical guarantee of zero false merges across all future images. Target calibration policies remain **PROPOSED**.
3. **Physical Schema Reality (`photo_person` vs Proposed `photo_face_tags`)**:
   - Current table in `backend/app/models/additive.py` is `photo_person` (`photo_id`, `user_id`, `confidence`). It lacks `face_index`, `bounding_box`, and unknown face instances (`user_id = NULL`).
   - `photo_face_tags` is an explicit **proposed logical target representation** and pending schema migration owned by Sharvani, NOT an existing database table.
4. **Cross-Member Verification**:
   - **Panchami**: ArcFace 512-d feature vector extraction, prototype score threshold ($\ge 0.90$), multi-face instance separation in group photos, honest reporting of unknown faces (`unidentified_faces = true`).
   - **Sharvani**: Trip-scoped candidate retrieval (`get_candidate_member_embeddings` strictly limited to active trip members), persistence of distinct face instances and member tags in `photo_person` (current) or `photo_face_tags` (proposed).
   - **Nikitha**: Photo gallery UI, strict per-person isolation in "My Photos", member filter chips in "All Photos", unidentified faces drawer, scenery folder segregation, review needed badges for borderline matches.

---

## 10. Authoritative Unresolved Decision Register

All decisions correspond strictly to the official 32-decision project register in [`docs/AI.md §12`](AI.md#12-stack-neutral-decision-register) and `docs/PROJECT_MEMORY.md`. Exactly **1 decision is RESOLVED** (#16) and **31 decisions remain open/pending**:

- **Decision #1: Primary vs Secondary Model Assignment** `[PENDING]`: Phi-4 Mini vs Qwen2.5-Coder.
- **Decision #2: Exact Model Identifiers & Quantization** `[PENDING]`: `q4_K_M` vs `q5_K_M` vs `q8_0`.
- **Decision #3: Inference Deployment Topology** `[PENDING]`: Local per-developer vs shared GPU vs ngrok tunnel.
- **Decision #4: Developer Tunnel Security** `[PENDING]`: IP whitelisting vs Tailscale vs Cloudflare Tunnel.
- **Decision #5: Promptfoo Acceptance Thresholds** `[PENDING]`: 95% vs 99% pass rate.
- **Decision #6: Arize Phoenix Telemetry Deployment** `[PENDING]`: Ephemeral container vs hosted Arize.
- **Decision #7: Groundedness Evaluator Adoption** `[PENDING]`: Ragas vs Promptfoo assertion suite.
- **Decision #8: Geocoding & POI Provider** `[PENDING]`: Self-hosted Nominatim vs Photon vs Mapbox/Google API.
- **Decision #9: Cloudinary Folder Hierarchy & Upload Presets** `[PENDING]`: Dedicated folder per trip vs flat folder. Local storage (`backend/static/uploads/`) preserved currently.
- **Decision #10: Live Traffic & Road Closure Provider** `[PENDING]`: Commercial feed vs static OSM with warning.
- **Decision #11: Geospatial & Road-Routing Engine Provider** `[PENDING]`: Self-hosted OSRM vs Mapbox Directions API.
- **Decision #12: Evidence Freshness TTL Thresholds** `[PENDING]`: Closure TTL (1h vs 4h); Route TTL (7d vs 30d).
- **Decision #13: Buffer Durations & Return Policies** `[PENDING]`: $B_{arr}=15	ext{m}, B_{dep}=15	ext{m}$ vs 30m.
- **Decision #14: Regional Geographic Scope for POI Search** `[PENDING]`: City boundary vs 25km vs 50km radius.
- **Decision #15: Paid API Fallback Policy** `[PENDING]`: Prohibit all paid APIs vs emergency Claude/Gemini fallback.
- **Decision #16: Production Managed Database Provider** `[RESOLVED — 2026-10-27]`: **Neon Managed PostgreSQL (`neondb`)** stamped at Alembic revision `c8a6a4789a32`.
- **Decision #17: Physical Schema for Consensus Audit** `[PENDING]`: Normalized table vs append-only JSONB log.
- **Decision #18: Physical Facial Embedding Storage** `[PENDING]`: PostgreSQL `pgvector` vs encrypted binary blob vs JSONB array.
- **Decision #19: Audit Data Retention & Access Rules** `[PENDING]`: 30-day retention vs indefinite; admin-only vs member access.
- **Decision #20: Unresolved Form Field Bounds** `[PENDING]`: Party size max (20 vs 50); Bio max (500 vs 1000).
- **Decision #21: Maximum Group Size Cap** `[PENDING]`: Cap at 10 vs 20 vs 50 travelers.
- **Decision #22: Objection Comment Length Bounds** `[PENDING]`: Min 5, max 500 chars vs Min 1, max 2000 chars.
- **Decision #23: Cross-Currency Conversion Policy** `[PENDING]`: Prohibit mixing currencies vs live ECB exchange rate.
- **Decision #24: Invite Code Expiry & Revocation** `[PENDING]`: 7-day expiration vs permanent until trip ends.
- **Decision #25: Governance Rejoining Policy** `[PENDING]`: Auto-reconverge at next slot vs mutual admin consent.
- **Decision #26: Tour-Guide Matchmaking Weights** `[PENDING]`: 30/25/25/20 proposed vs equal 25/25/25/25.
- **Decision #27: Subsequent Round Window Start Policy** `[PENDING]`: First NO starts timer vs immediate countdown on round advance.
- **Decision #28: Operational LLM Inference Timeout** `[PENDING]`: 8s vs 10s vs 15s latency ceiling.
- **Decision #29: AI Decision Audit Entity Persistence Strategy** `[PENDING]`: Dedicated `ai_decision_audit` table vs leveraging `revision_history.snapshot_data`.
- **Decision #30: Itinerary PDF Rendering Engine Strategy** `[PENDING]`: Client-side (`@react-pdf/renderer` / `jspdf`) vs Server-side (FastAPI `weasyprint` / `reportlab`). PDF export is REQUIRED (`FR-EXP-01`); renderer selection remains open.
- **Decision #31: Consensus Voting Window Duration Sign-Off** `[PENDING]`: 10 minutes (current implementation behavior) vs 5 minutes vs 15 minutes.
- **Decision #32: Active Voting Electorate Modification Policy** `[PENDING]`: Mid-voting electorate lock vs dynamic threshold recalculation.
