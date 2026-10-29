**Specification Status**: Updated Draft — Pending User Review

# Technical Requirements Document (TRD): WanderMatch

**Product**: WanderMatch — Social & Group Travel Planning with an AI Consensus Planner  
**Hackathon**: KogniVera Hackathon 2026 (Problem Statement PS-11, Travel & Tourism Theme)  
**Team**: Chaosminds — Nikitha (Frontend); Panchami (HTTP/WebSocket Transport and DeepFace); Sharvani (Business Logic, AI/Consensus, Authentication, Database, Integration and Deployment)
**Specification Status**: Updated Draft — Pending User Review  
**Canonical AI Specification Reference**: For complete Pydantic schemas, geographic routing equations, Promptfoo/Phoenix evaluation setup, and the 20-attribute decision audit record, consult the canonical [AI System Specification](AI.md).

---

## 1. System Overview & Architecture Boundary

WanderMatch implements a **Single Orchestrator Backend Pattern** powered by **FastAPI**. The **React/TypeScript** frontend operates strictly as a presentation and interaction layer and **never** connects directly to PostgreSQL, external LLM providers, Cloudinary, or the DeepFace service. All client operations pass through authenticated FastAPI REST endpoints or WebSocket channels.

```
┌─────────────────────────────────────────────────────────────┐
│          React 19.2.8 + TypeScript Frontend (Vite 8.3.0)     │
│          (Tailwind CSS 4.3.3 / Clerk React 5.61.10)         │
└───────────────┬─────────────────────────────▲───────────────┘
                │ REST (camelCase)            │ WebSocket Events
                │                             │ (verb-first camelCase)
┌───────────────▼─────────────────────────────┴───────────────┐
│         FastAPI Consolidated Core Backend (Port 8000)       │
│          (Python 3.12+ / Uvicorn / Pydantic v2)             │
├─────────────────┬──────────────┬──────────────────┬─────────────┤
│  Authoritative  │ Clerk Auth   │ Candidate LLM    │ Candidate   │
│  PostgreSQL DB  │ Webhooks &   │ Endpoint (Hosted │ Cloudinary  │
│  (Neon Candidate│ Session JWT  │ API / Local      │ Media CDN   │
│   [PENDING])    │              │ Ollama [PENDING])│ [PENDING]   │
└─────────────────┴──────────────┴──────────────────┴─────────────┘
```

### 1.1 Universal Naming Contract Enforcement
- **Database & Python Internals**: `snake_case` (table names, column names, model fields, internal variables).
- **FastAPI REST Payloads & Responses**: `camelCase` at the API boundary (Pydantic schema aliasing).
- **TypeScript API-Facing Interfaces**: `camelCase`.
- **Approved Canonical WebSocket Event Names**: In strict accordance with the approved MVP contract, the real-time event list consists of five canonical verb-first `camelCase` events:
  1. `voteCast`: Emitted when a binary vote is cast or retracted.
  2. `proposalCreated`: Emitted when a new proposal is created.
  3. `branchConfirmed`: Emitted when a member confirms or locks a branch choice.
  4. `slotStatusChanged`: Emitted when a slot transitions status (`EMPTY`, `IN_CONSENSUS`, `BRANCHED`, `CONFIRMED`), advances a consensus round, starts a countdown window (`closesAt`), or restores a revision.
  5. `aiPlanGenerated`: Emitted when an AI compromise plan is synthesized.
  *(Note: Any additional real-time notifications, such as membership change events, are conveyed through REST refresh or documented as candidate additions for future implementation plan updates).*
- **Opaque Prefixed Identifiers**: `usr_` (user), `prf_` (preference), `trp_` (trip), `tmb_` (member), `itn_` (itinerary), `itm_` (item), `prp_` (proposal), `vot_` (vote), `slc_` (slot consensus), `brc_` (branch), `bmb_` (branch member), `rev_` (revision), `msg_` (chat message), `jrq_` (join request), `fcp_` (face profile), `pho_` (photo).

### 1.2 Target Technology Stack Baseline & Repository Findings

#### 1.2.1 Target Baseline Architecture
- **Frontend Layer**: React 19.2.8, TypeScript ~6.0.2, Vite 8.3.0, Tailwind CSS 4.3.3 (`@tailwindcss/vite`), React Router DOM 7.18.4, Clerk React 5.61.10, Lucide React 1.47.0, native `fetch` API client in `src/lib/api.ts`, React Context (`AuthContext`, `TripContext`). Proposed frontend test suite: Vitest + React Testing Library [DECISION PENDING].
- **Core Backend Orchestrator**: Consolidated FastAPI backend (Python 3.12+, Uvicorn, Pydantic v2, SQLAlchemy 2.x, Alembic migrations). Consolidation merges all routes into Port 8000.
- **15 Modular Core Responsibilities**:
  1. *Authentication & Authorization*: Clerk JWT validation, JWKS caching, Svix webhooks.
  2. *User Profiles & Onboarding*: Preferences, travel style, currency, locale.
  3. *Trip Creation & Management*: Trip lifecycle, public/private visibility, dates, capacity.
  4. *Invitations & Membership*: 8-character invite codes, join requests, approval flows.
  5. *Group & Guide Matchmaking*: Group compatibility ($0.45 \text{ Interest} + 0.35 \text{ Language} + 0.20 \text{ Age}$); guide matching.
  6. *Itinerary & Activity Management*: Day-wise activity slots, optimistic lock via monotonic `version`.
  7. *Proposals & Consensus Voting*: YES/NO binary voting, mandatory comments on NO.
  8. *Consensus Rounds & Branches*: Mode A (admin-led) and Mode NA (collaborative) engines, 10-minute timers, holdout branches.
  9. *AI Planning & Provider Integration*: Provider-independent LLM adapter (hosted Gemini/Groq/OpenAI vs. local Ollama).
  10. *Deterministic Constraint Validator*: Enforces road feasibility ($t_{arr} + t_{act} + t_{ret} + 2t_{buf} \le W_{avail}$), venue hours, and budgets.
  11. *Chat & Live Event Distribution*: Trip chat messages, authenticated WebSocket hub, canonical events (`voteCast`, `proposalCreated`, `branchConfirmed`, `slotStatusChanged`, `aiPlanGenerated`).
  12. *Notifications*: In-app toast alerts for vote deadlines, join requests, and admin actions.
  13. *Photo & DeepFace Orchestration*: Photo upload gateway, Cloudinary CDN dispatch, trip-scoped face recognition job coordination.
  14. *Routing, Geocoding & Place Evidence*: Road travel duration calculation (OSRM engine), coordinate resolution, venue hours.
  15. *Audit History & Persistence*: Immutable 20-attribute AI decision audit logs, slot revision snapshots, transactional reversions.
- **Authoritative Database**: PostgreSQL is the single target relational database for all persistent state. Neon is a candidate managed provider [DECISION PENDING].
- **DeepFace Biometrics**: DeepFace is a **REQUIRED separate processing service** (Port 8001), isolated due to heavy dependencies (TensorFlow/PyTorch, OpenCV) and computational load. Traveler facial enrollment is optional; application photo-segregation is required. Face processing failures are non-blocking.
- **Road Routing**: OSRM is the candidate road-network routing engine. Straight-line (Haversine) distance is strictly prohibited as a substitute for road travel duration.

#### 1.2.2 Verified Current Repository Findings
Static code inspection of the actual repository confirms the following 17 architectural facts:
1. `[CURRENT — VERIFIED]` Frontend declares React 19.2.8 (`react`, `react-dom`), Vite 8.3.0, Tailwind CSS 4.3.3, React Router 7.18.4, and Clerk React 5.61.10.
2. `[CURRENT — VERIFIED]` Core backend declares FastAPI >=0.111.0, Uvicorn, Pydantic v2, SQLAlchemy >=2.0.30, psycopg2-binary >=2.9.9, and Alembic >=1.13.1.
3. `[CURRENT — VERIFIED]` Three distinct FastAPI entry points exist (`backend/app/main.py`, `ai/AIConsensus/backend/app/main.py`, and `ai/DeepFace/backend/main.py`). Consolidation is a proposed architectural change.
4. `[CURRENT — VERIFIED]` Consensus router (`backend/app/routers/consensus.py`) is implemented and mounted in primary backend on Port 8000 (`/api/consensus/`). All consensus state persists authoritatively to Neon PostgreSQL (`proposals`, `votes`, `slot_consensus`, `branches`, `itinerary_items`), completely eliminating `TRIPS_DB = {}` as the authoritative store.
5. `[CURRENT — VERIFIED]` `POST /api/consensus/reconcile` is implemented and operational on Port 8000, connecting directly to Neon PostgreSQL.
6. `[CURRENT — VERIFIED]` Authenticated WebSocket room hub (`backend/app/websocket_manager.py`) is implemented on Port 8000 (`/ws/trips/{trip_id}`). It verifies Clerk JWT signatures, derives caller identity strictly from the `sub` claim (rejecting URL query mismatches with 4403), verifies trip membership before sending state snapshots, and broadcasts committed real-time events to all authorized connected room members.
7. `[CURRENT — VERIFIED]` Authentication helper implements production Clerk JWT verification with cached JWKS validation.
8. `[CURRENT — VERIFIED]` Photo uploads are implemented in `backend/app/routers/photos.py` saving to local disk (`backend/static/uploads/`) and persisting metadata to Neon `photos` table. Cloudinary SDK is installed but unconfigured in `.env`; local disk is ephemeral on Render web services.
9. `[CURRENT — VERIFIED]` Face profile management is implemented in `backend/app/routers/face.py` persisting registration status and embeddings to Neon `face_profiles` table and coordinating trip-scoped face matching.
10. `[CURRENT — VERIFIED]` DeepFace processing operates as an isolated service module; individual enrollment is optional and biometric failures are strictly non-blocking.
11. `[CURRENT — VERIFIED]` Neon Managed PostgreSQL (`neondb` on AWS ap-southeast-1, PostgreSQL 18.6) is the confirmed authoritative database of record, housing 24 application tables and 34 foreign keys.
12. `[CURRENT — VERIFIED]` Baseline Alembic migration revision `c8a6a4789a32` is created, tested against clean test databases, and stamped in `neondb`.
13. `[CURRENT — VERIFIED]` `AIConsensus` dependency declarations and runtime assumptions require reconciliation with the primary backend.
14. `[CURRENT — VERIFIED]` Test files exist in `AIConsensus` and `DeepFace`, but no test execution pass status has been established by static audit.
15. `[CURRENT — VERIFIED]` Frontend tests are proposed (Vitest + React Testing Library) but are not yet declared in `frontend/package.json`.
16. `[CURRENT — VERIFIED]` No Dockerfiles, Docker Compose files, or CI/CD workflow configurations exist in the current repository tree.
17. `[CURRENT — VERIFIED]` Current code, declared dependencies, documented architecture, and deployed infrastructure remain separate evidence categories.

---

### 1.2.3 Deferred Investigations & Operational Holds
- **`[DEFERRED_FOLLOW_UP]` Slow Navbar/Page Navigation**: User-observed latency when switching tabs/pages in the navbar is recorded as a deferred performance investigation item. No speculative code or architectural changes are permitted; empirical profiling of route transitions, React rendering, Clerk auth tokens, and API latency will occur in the designated performance phase.
- **`[CLEANUP_ON_HOLD]` Database Cleanup**: Cleanup of 27,283 historical transactional records in 19 tables in Neon PostgreSQL is strictly on hold. Verified backup and dry-run recovery have been confirmed, but primary database deletion is prohibited until all planning phases are approved.

## 2. API Contracts & Endpoint Specifications

### 2.1 Public Discovery, Privacy & Membership APIs

#### `GET /api/trips/discover`
- **Purpose**: Lists eligible public trips for Solo Match discovery.
- **Authorization**: Optional authentication.
- **Query Parameters**:
  - `destinationCityId` (string, optional; maps to `trips.destination_city_id`)
  - `startDate` (ISO 8601 date, optional)
  - `endDate` (ISO 8601 date, optional)
  - `mode` (string: `'Mode A'` | `'Mode NA'`, optional)
  - `hasCapacity` (boolean, default: `true`)
- **Backend Privacy Enforcement**:
  - The query strictly enforces `WHERE trips.visibility = 'public' AND trips.status != 'draft'`.
  - Trips marked `visibility = 'private'` are strictly excluded at the SQL level.
- **Response (`200 OK`)**:
  ```json
  [
    {
      "trpId": "trp_987",
      "title": "Kyoto Autumn Explorer",
      "destinationCity": "Kyoto",
      "destinationCountry": "Japan",
      "startDate": "2026-11-10",
      "endDate": "2026-11-17",
      "mode": "Mode NA",
      "visibility": "public",
      "partySize": 6,
      "currentMemberCount": 4,
      "hasCapacity": true,
      "owner": {
        "usrId": "usr_101",
        "displayName": "Alex Rivera"
      }
    }
  ]
  ```

#### `POST /api/trips/join-by-code` (also available as `/api/join-requests/by-code`)
- **Purpose**: Pre-authorized instant entry into a **Private trip** using a secret 8-character invite code. (In strict alignment with the PRD access matrix, invite-code admission applies to Private trips; Public Mode A trips require an admin-approved join request, and Public Mode NA trips use direct join).
- **Authorization**: Required (`Bearer <JWT>` session). Caller identity MUST be resolved from authenticated session credentials (`current_user.user_id`), never trusted from client payload.
- **Request Body**:
  ```json
  {
    "inviteCode": "A9K2M4X7"
  }
  ```
- **Illustrative Logical Transaction Example with Provisional Physical Mappings**:
  *(Note: PostgreSQL does not allow locking aggregate queries like `SELECT COUNT(*) ... FOR UPDATE`. To illustrate an atomic concurrency strategy where concurrent join attempts cannot exceed `party_size`, the backend executes the following serialized transaction. This represents an illustrative target transactional strategy, not a proof of current prototype concurrency safety. The entity `trip_invite_codes` represents a provisional logical mapping pending database schema finalization).*
  ```sql
  BEGIN;

  -- 1. Lock parent trip row to serialize concurrent joins for this trip
  SELECT trip_id, party_size, visibility, mode 
  FROM trips 
  WHERE trip_id = :trip_id 
  FOR UPDATE;

  -- 2. Validate trip privacy: invite-code admission is restricted to Private trips
  -- (If visibility == 'public', return HTTP 400 with guidance to use public join paths)

  -- 3. Validate invite code exists, is active, and belongs to this trip (provisional logical check)
  SELECT invite_code_id 
  FROM trip_invite_codes 
  WHERE code = :invite_code AND trip_id = :trip_id;

  -- 4. Check existing membership state for this user (unique constraint on (trip_id, user_id))
  SELECT member_id, status 
  FROM trip_members 
  WHERE trip_id = :trip_id AND user_id = :user_id;

  -- 5. Count ONLY records whose membership status is active
  SELECT COUNT(*) AS active_count 
  FROM trip_members 
  WHERE trip_id = :trip_id AND status = 'active';

  -- Evaluated Mutually Exclusive Business Logic Paths:
  -- Path 1: User already an active member (`status = 'active'`):
  --    -> ROLLBACK and return HTTP 400 ("ALREADY_MEMBER", "Already an active member of this trip.")
  --
  -- Capacity Check (Applies to both Path 2 and Path 3 before admission):
  --    If active_count >= party_size -> ROLLBACK and return HTTP 400 ("TRIP_FULL", "Trip has reached maximum capacity.")
  --
  -- Path 2: Record already exists for this (trip_id, user_id) with non-active status (inactive, archived, or draft):
  --    Because (trip_id, user_id) is unique, an existing record cannot be inserted again.
  --    -> If rejoining policy permits reactivation:
  --       UPDATE trip_members 
  --       SET status = 'active', role = 'editor', updated_at = NOW()
  --       WHERE trip_id = :trip_id AND user_id = :user_id;
  --    -> If rejoining policy is restrictive or does not permit re-entry:
  --       (Unresolved Policy: Rejoining rules for previously departed members remain an open product decision;
  --        if policy prohibits re-entry, ROLLBACK and return HTTP 403 Forbidden).
  --
  -- Path 3: No prior membership record exists for this (trip_id, user_id):
  --    -> Insert new member using verified logical fields (member_id, trip_id, user_id, role, joined_at, status, updated_at):
  --       INSERT INTO trip_members (member_id, trip_id, user_id, role, joined_at, status, updated_at)
  --       VALUES (:member_id, :trip_id, :user_id, 'editor', NOW(), 'active', NOW());

  COMMIT;
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "status": "joined",
    "trpId": "trp_987",
    "usrId": "usr_222",
    "role": "editor",
    "message": "Successfully joined private trip via invite code."
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: `{ "error": "INVALID_CODE", "message": "Invite code is invalid, expired, or revoked." }`
  - `400 Bad Request`: `{ "error": "TRIP_FULL", "message": "Trip has reached maximum capacity." }`
  - `400 Bad Request`: `{ "error": "ALREADY_MEMBER", "message": "Already an active member of this trip." }`
  - `400 Bad Request`: `{ "error": "PUBLIC_TRIP_CODE_UNSUPPORTED", "message": "Public trips use join requests (Mode A) or direct join (Mode NA)." }`
  - `401 Unauthorized`: Missing or invalid session token.

#### `POST /api/trips/{trpId}/join-request`
- **Purpose**: Submits a join request for a **Public Mode A** trip requiring administrator approval.
- **Authorization**: Required (`Bearer <JWT>`). Caller identity extracted from session token.
- **Request Body**:
  ```json
  {
    "message": "Hi, I am an experienced hiker and would love to join your Kyoto trip!"
  }
  ```
- **Execution & Validation Rules**:
  1. Check trip visibility: If `trip.visibility == 'private'`, reject with HTTP `403 Forbidden` (`"Private trips require an invite code"`).
  2. If trip mode is `Mode NA`, redirect to direct join flow or auto-accept if capacity permits.
  3. Verify active members are below `trip.party_size`. If full, return HTTP `400 Bad Request` (`"Trip is full"`).
  4. Verify user does not have an existing `pending` or `approved` request. If duplicate, return HTTP `409 Conflict`.
  5. Insert record into `join_requests` (`jrq_` prefix) with `status = 'pending'`.
- **Response (`201 Created`)**:
  ```json
  {
    "requestId": "jrq_301",
    "trpId": "trp_987",
    "usrId": "usr_222",
    "status": "pending",
    "message": "Join request submitted. Awaiting trip owner approval.",
    "createdAt": "2026-10-25T10:00:00Z"
  }
  ```

#### `POST /api/trips/{trpId}/join-requests/{requestId}/approve`
- **Purpose**: Administrator approval of a pending join request in Mode A.
- **Authorization**: Required; authenticated caller must be the trip `owner`.
- **Execution & Concurrency Strategy**:
  1. Locks the parent `trips` row (`FOR UPDATE`).
  2. Checks active member capacity: `SELECT COUNT(*) FROM trip_members WHERE trip_id = :trpId AND status = 'active' < trip.party_size`. If full, rejects with HTTP `400 Bad Request` (`"Trip capacity exceeded"`).
  3. Atomically updates `join_requests.status = 'approved'`, `reviewed_by = current_user.user_id`. (Entity `join_requests` is a provisional logical mapping).
  4. Atomically inserts or reactivates `trip_members` row (`role = 'editor'`, `status = 'active'`, `joined_at = NOW()`, `updated_at = NOW()`).
- **Response (`200 OK`)**:
  ```json
  {
    "requestId": "jrq_301",
    "status": "approved",
    "newMemberId": "usr_222",
    "currentMemberCount": 5,
    "partySize": 6
  }
  ```

#### `POST /api/trips/{trpId}/join-requests/{requestId}/reject`
- **Purpose**: Administrator rejection of a pending join request.
- **Authorization**: Required; authenticated caller must be the trip `owner`.
- **Response (`200 OK`)**:
  ```json
  {
    "requestId": "jrq_301",
    "status": "rejected"
  }
  ```

#### `POST /api/trips/{trpId}/join`
- **Purpose**: Direct instant join for a **Public Mode NA** trip where capacity remains.
- **Authorization**: Required (`Bearer <JWT>`). Caller identity extracted from session token.
- **Execution**: Serializes on parent `trips` row lock (`FOR UPDATE`), verifies `active_count < party_size` (`status = 'active'`), and inserts/reactivates member row (`role = 'editor'`, `status = 'active'`, `joined_at = NOW()`, `updated_at = NOW()`).
- **Response (`200 OK`)**:
  ```json
  {
    "status": "joined",
    "trpId": "trp_987",
    "usrId": "usr_222",
    "role": "editor"
  }
  ```

---

## 2.2 Voting Engine & Server-Side Single Active YES Contract

#### `POST /api/votes`
- **Purpose**: Cast a binary `yes` or `no` vote on an active proposal.
- **Authorization**: Required; caller must be an active member of the trip, verified via session token.
- **Request Body**:
  ```json
  {
    "prpId": "prp_111",
    "value": "no",
    "comment": "Injured ankle, cannot hike. Prefer visiting hot springs spa instead."
  }
  ```
- **Validation Rules**:
  1. `value` must be strictly `'yes'` or `'no'`. Abstentions are invalid application votes.
  2. If `value == 'no'`, `comment` is **mandatory**; empty strings, null, or whitespace-only strings fail with HTTP `400 Bad Request`.
  3. `votes.weight` exists in the database schema but is strictly unused for MVP.

#### Logical Voting Contract & Baseline Activity Participation
The PS-11 schema links `votes` directly to proposals (`votes.proposal_id` $\rightarrow$ `proposals.proposal_id`), while baseline activities reside in `itinerary_items`. To provide a consistent, coherent voting experience without inventing unapproved physical tables:
1. **Baseline as Confirmed Milestone**:
   - The scheduled activity in `itinerary_items` represents the currently confirmed baseline milestone.
   - Competing proposals (`prp_`) attach to that item via `proposals.target_item_id = itinerary_items.item_id`.
2. **Voting on Alternative Proposals**:
   - When a proposal `prp_` is created for a slot, it represents an alternative to the baseline.
   - Members casting `YES` on `prp_` vote to replace the baseline with that proposal.
   - Members who prefer to keep the original baseline activity cast `NO` on the competing proposal with a typed comment (e.g. `"Prefer original sunrise trek"`).
3. **Single Active YES Invariant**:
   - A member may back at most ONE alternative proposal per itinerary slot at any time.
   - If a member has an active `YES` on Proposal A and casts `YES` on Proposal B for the same slot:
     - FastAPI executes an atomic transaction that deactivates or removes the active `YES` on Proposal A and records the new `YES` on Proposal B.
     - **Non-Pollution Rule**: Retracting a previous `YES` vote simply deactivates/removes that `YES`. It must **never** synthesize a `no` vote or attach an artificial dissent comment.
     - YES votes on other itinerary slots remain completely unaffected.
4. **Resolution Outcome**:
   - If an alternative proposal achieves consensus, it replaces the baseline activity, and a new revision snapshot is appended to `revision_history`.
   - If competing proposals fail consensus or are rejected, the slot remains confirmed at its baseline milestone.
   - *(Physical Schema Note: If future design unifies baseline activities as explicit proposal records or re-keys votes to `target_item_id`, that physical schema decision is deferred to the database review phase).*
- **WebSocket Broadcast**: Emits `voteCast` event to `/ws/trips/{trpId}?token={jwt}` (authenticated route; historical dev connection was `/ws/trips/{trpId}/{usrId}`).
- **Response (`201 Created`)**:
  ```json
  {
    "votId": "vot_333",
    "prpId": "prp_111",
    "usrId": "usr_222",
    "value": "no",
    "comment": "Injured ankle, cannot hike. Prefer visiting hot springs spa instead.",
    "createdAt": "2026-10-25T10:05:00Z"
  }
  ```

---

## 2.3 Slot-Level Consensus Timer & Reconciliation Contract

> [!NOTE]
> **Nomenclature & State Mapping Invariant**:
> 1. **Physical Database Values**: Stored in PostgreSQL in lowercase `snake_case`: `'empty'`, `'in_consensus'`, `'confirmed'`, `'branched'` in `slot_consensus.slot_status` and `itinerary_items.slot_status`.
> 2. **Canonical UI Display Labels**: Displayed in frontend badges in uppercase: `EMPTY`, `IN_CONSENSUS`, `CONFIRMED`, `BRANCHED`.
> 3. **Proposal Lifecycle States**: Tracked separately in `proposals.status`: `'open'`, `'accepted'`, `'rejected'`.
> 4. **Branch Lifecycle States**: Tracked separately in `branches.status`: `'active'`, `'finalized'`.

#### Logical Requirements & Behavioral Rules:
1. **Single Authoritative Timer per Slot**: In Mode NA, exactly one countdown timer governs an itinerary slot during a given consensus cycle. There are NOT independent timers per proposal.
2. **Quiet Baseline**: The timer does NOT start upon proposal creation or on peaceful baseline slots.
3. **Trigger Condition**: The timer starts immediately when the **first `no` vote** lands on ANY proposal belonging to that slot in the current consensus cycle (`first_no_at = NOW()`).
4. **Deadline Definition (`[IMPLEMENTATION BEHAVIOR — DECISION PENDING: Product Sign-Off Required]`)**: Current code initiates a 10-minute voting window upon the first NO vote (`closes_at = first_no_at + INTERVAL '10 minutes'`). Product sign-off is pending whether this 10-minute duration is the immutable canonical product rule or configurable per trip.
5. **Shared Deadline**: All competing proposals for that slot share this authoritative deadline.
6. **Reconciling Early Branching with the Ten-Minute Timer**:
   - When the first NO vote arrives, the 10-minute timer starts (`[IMPLEMENTATION BEHAVIOR — DECISION PENDING: Product Sign-Off Required]`).
   - The objection classifier evaluates the objection comment.
   - **Early-Branch Path**: If the classifier identifies a fixed, non-negotiable physical or medical constraint (e.g., severe injury, wheelchair requirement, or absolute geographical conflict), the system initiates early branching immediately under this approved exception without waiting for the 10-minute timer to elapse or forcing an implausible compromise plan.
   - **Fixable Tweak Path**: If objections represent negotiable preferences (timing, budget, activity style), the voting window remains active for its full 10-minute duration. At expiry, all proposals and votes for that slot and cycle are reconciled together.
7. **Mode A Exclusion**: In Mode A, there is no automated 10-minute countdown. The administrator controls round duration, and AI recommendations are strictly advisory (`advisory: true`).
8. **Physical Schema Deferred Notice**: Logical requirements are documented here; physical schema persistence (e.g. extending `slot_consensus` vs proposal columns) will be formalized in the subsequent `DATABASE.md` review phase.

#### `POST /api/consensus/check-timer`
- **Purpose**: Evaluates slot consensus expiration and triggers automatic reconciliation if deadline has passed.
- **Request Body**:
  ```json
  {
    "itmId": "itm_456"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "itmId": "itm_456",
    "timerStatus": "ACTIVE",
    "firstNoAt": "2026-10-25T10:05:00Z",
    "closesAt": "2026-10-25T10:15:00Z",
    "secondsRemaining": 420
  }
  ```

---

## 2.4 AI Consensus & Multi-Way Branching APIs

#### `POST /api/consensus/reconcile`
- **Purpose**: Executes AI consensus reconciliation for a slot upon timer expiration or explicit invocation. (Note: An explicit invocation alone MUST NOT bypass the Round 3 closure requirement; round-cap branching in Mode NA is permitted only after the Round 3 voting window has actually closed, preserving the separate fixed-incompatibility exception).
- **Request Body**:
  ```json
  {
    "itmId": "itm_456"
  }
  ```
- **Execution Pipeline & Mode Authority Split**:
  1. Retrieve active proposals, votes, typed `no` comments, slot baseline item, and trip context.
  2. Invoke `classify_objection()`:
     - **Mode NA (Collaborative)**:
       - **Fixed-Incompatibility Exception**: If `FIXED_REQUIREMENT` is reliably identified, the engine executes early branching immediately into parallel tracks without waiting for timer expiry or round cap.
       - **Fixable Objections**: If objections are `FIXABLE_TWEAK`:
         - For Rounds 1 and 2: Generates exactly ONE blended compromise plan via `generate_blended_plan()`.
         - For Round 3: The round-cap condition is met ONLY when the Round 3 voting window has actually closed/expired. If the Round 3 window has closed with persistent dissent, blending terminates and the engine automatically branches via `group_into_branches()`. If invoked while the Round 3 window is still open, the voting window remains active until expiration.
     - **Mode A (Admin-Led)**:
       - AI output is strictly advisory (`advisory: true`). The AI generates a proposed compromise plan or recommended branching structure. It **never** commits automatic binding changes to the schedule. Even on fixed incompatibilities or at the round cap, branching is presented as an advisory recommendation for admin review and decision. The admin must explicitly execute an administrative action (`admin_accept`, `admin_force_branch`, `admin_extend`).
  3. Validate candidate against hard constraints (`hard_constraint_validator`).
  4. If validation passes, return blended plan and advance round counter (`current_round += 1`).
  5. If validation fails twice or round cap is reached:
     - **Mode NA**: Automatically invokes `group_into_branches()` to branch the slot into parallel tracks once eligibility conditions are satisfied.
     - **Mode A**: Returns a recommended branching plan with `advisory: true` for the administrator's review and decision; no automatic branch execution occurs.
- **Response — Blended Compromise**:
  ```json
  {
    "action": "BLENDED",
    "currentRound": 2,
    "blendedPlan": {
      "title": "Batur Thermal Springs & Sunrise Viewpoint",
      "rationale": "Reconciles summit hiking objection with thermal hot springs relaxation and panoramic views.",
      "entityType": "poi",
      "entityId": "poi_batur_springs",
      "costDelta": "5.00",
      "currency": "USD"
    }
  }
  ```
- **Response — Multi-Way Branching**:
  ```json
  {
    "action": "BRANCHED",
    "branches": [
      {
        "brcId": "brc_001",
        "title": "Mount Batur Sunrise Summit Trek (Track A - Base Plan)",
        "status": "OPEN",
        "memberUserIds": ["usr_101", "usr_102", "usr_silent_3"],
        "autoFinalized": false
      },
      {
        "brcId": "brc_002",
        "title": "Toya Devasya Hot Springs & Spa Relaxation (Track B)",
        "status": "FINALIZED",
        "memberUserIds": ["usr_222"],
        "autoFinalized": true
      }
    ]
  }
  ```
- **Behavioral Guarantees**:
  - Silent members who cast no vote automatically default to Track A (Base Plan) with an on-screen option to switch tracks.
  - Single-member branches have `autoFinalized = true` and `status = 'FINALIZED'`.
  - Recursive branches link to parent branch via `parent_branch_id`.

---

## 2.5 Revision History & Reversion API

#### `POST /api/trips/{trpId}/itinerary/items/{itmId}/revert`
- **Purpose**: Restores an earlier confirmed itinerary version using the append-only history rule.
- **Authorization**:
  - **Mode A**: Restricted to Trip Owner (`owner` role) only. Non-admins receive HTTP `403 Forbidden`.
  - **Mode NA**: Allowed for any trip member via collaborative restoration proposal.
- **Request Body**:
  ```json
  {
    "targetVersionNumber": 1,
    "expectedCurrentItineraryVersion": 3
  }
  ```
- **Transactional & Versioning Behavior**:
  *(Illustrative Logical Transaction with Provisional Physical Identifiers — Column identifiers such as `item_id` vs. `itm_id` and `itinerary_id` vs. `itn_id` represent provisional mappings pending formal database review)*:
  1. **Atomic Transaction Scope & Optimistic Concurrency**:
     All restoration operations occur within a single database transaction (`BEGIN ... COMMIT`). The operation must succeed completely or roll back completely. A version mismatch or zero-row update rolls back the entire transaction; it must never leave an orphaned revision record, an unincremented itinerary version, or a partially restored item.
  2. **Optimistic Concurrency Check**:
     Locks and verifies the parent itinerary optimistic version:
     ```sql
     SELECT version FROM itineraries WHERE itinerary_id = :itinerary_id FOR UPDATE;
     ```
     Ensure `itineraries.version == expectedCurrentItineraryVersion`. If mismatch, abort with HTTP `409 Conflict`.
  3. **Snapshot Retrieval**:
     Locate historical snapshot in `revision_history` where `itm_id = :itmId` and `version_number = :targetVersionNumber`. (In the verified PS-11 schema, the foreign key column is `itm_id`). If not found, return HTTP `404 Not Found`.
  4. **Extract Snapshot Fields**:
     Extract all mutable fields represented by the approved `snapshot_data` contract (`title`, `description`, `entity_type`, `entity_id`, `cost`, `starts_at`, `ends_at`).
  5. **Concurrency-Safe Version Allocation & Append-Only Write**:
     - Allocation of `MAX(version_number) + 1` for this `itm_id` requires a serialized/locked query or equivalent concurrency-safe logical mechanism within the transaction:
       ```sql
       SELECT COALESCE(MAX(version_number), 0) + 1 AS next_version_number 
       FROM revision_history 
       WHERE itm_id = :itm_id;
       ```
     - Inserts a **brand new revision** record into `revision_history` (maintaining the documented schema: `rev_id`, `itm_id`, `version_number`, `snapshot_data`, `created_at`):
       ```sql
       INSERT INTO revision_history (rev_id, itm_id, version_number, snapshot_data, created_at)
       VALUES (:new_rev_id, :itm_id, :next_version_number, :restored_snapshot_data, NOW());
       ```
     - Historical revisions (Versions 1, 2, and 3) remain completely untouched.
     - *(Note: Capturing extra audit attribution such as actor `created_by` or `restored_from_version` remains a logical requirement deferred to the physical database design stage).*
  6. **Restore Mutable Item Fields & Advance Itinerary Version**:
     ```sql
     -- Restore all mutable fields represented by snapshot_data
     UPDATE itinerary_items 
     SET title = :restored_title, 
         description = :restored_description, 
         entity_type = :restored_entity_type, 
         entity_id = :restored_entity_id, 
         cost = :restored_cost, 
         starts_at = :restored_starts_at, 
         ends_at = :restored_ends_at, 
         updated_at = NOW()
     WHERE item_id = :item_id;

     -- Atomically increment parent itinerary optimistic concurrency version
     UPDATE itineraries 
     SET version = version + 1, updated_at = NOW() 
     WHERE itinerary_id = :itinerary_id AND version = :expected_itinerary_version;
     ```
     *(If the UPDATE on itineraries affects 0 rows due to a concurrent write, FastAPI executes ROLLBACK immediately, reverting the revision_history insert and item field updates, returning HTTP 409 Conflict)*.
  7. Broadcast `slotStatusChanged` via WebSocket to notify all clients.
- **Response (`200 OK`)**:
  ```json
  {
    "itmId": "itm_456",
    "restoredFromVersion": 1,
    "newRevisionVersionNumber": 4,
    "itineraryVersion": 4,
    "title": "Original Mount Batur Trek",
    "status": "CONFIRMED",
    "updatedAt": "2026-10-25T10:20:00Z"
  }
  ```

---

## 2.6 Solo Matchmaking & Tour Guide APIs

#### `POST /api/solo-matching/groups`
- **Purpose**: Returns ranked compatible public group trips for a solo traveler.
- **Authorization**: Required (`Bearer <JWT>`). Caller identity obtained from authenticated session token, not client body.
- **Request Body**:
  ```json
  {}
  ```
- **Approved Deterministic Formula (0–100%)**:
  $$\text{Group Score} = 0.45 \times \text{Jaccard Interest Similarity} + 0.35 \times \text{Language Match} + 0.20 \times \text{Age Bracket Compatibility}$$
- **Response (`200 OK`)**:
  ```json
  [
    {
      "trip": {
        "trpId": "trp_987",
        "title": "Kyoto Autumn Explorer",
        "destinationCity": "Kyoto",
        "startDate": "2026-11-10",
        "endDate": "2026-11-17",
        "mode": "Mode NA",
        "partySize": 6,
        "currentMemberCount": 4
      },
      "compatibilityScore": 88,
      "breakdown": {
        "interestSimilarity": 0.80,
        "languageMatch": 1.00,
        "ageBracketCompatibility": 1.00
      },
      "sharedInterests": ["Photography", "Culinary", "Historical Walking Tours"],
      "sharedLanguages": ["en", "ja"]
    }
  ]
  ```

#### `POST /api/solo-matching/guides`
- **Purpose**: Returns ranked local tour guides for a solo traveler based on criteria.
- **Authorization**: Required (`Bearer <JWT>`).
- **Request Body**:
  ```json
  {
    "cityId": "cty_kyoto",
    "maxDailyBudget": "150.00",
    "currency": "USD"
  }
  ```
- **Tour Guide Scoring Criteria, Grounded Fields & Currency Handling**:
  - Factors evaluated against verified schema:
    - Destination city: `tour_guides.city_id == :cityId`
    - Spoken languages: `tour_guides.languages` vs. traveler `user_preferences.preferred_languages` (corrected from nonexistent `user_preferences.languages`).
    - Specializations: `tour_guides.specialisation`, `secondary_specialisation` vs. traveler `user_preferences.interests`
    - Budget compliance: `tour_guides.day_rate <= user_preferences.max_daily_budget`.
      *(Currency Rule: A guide's daily rate is compared meaningfully with a traveler's budget ONLY when the currency is known and compatible, i.e., `tour_guides.currency == user_preferences.max_daily_budget_currency`. All monetary values use `DECIMAL(12,2)` with an explicit ISO-4217 currency code; floating-point arithmetic for money is strictly prohibited. The system does not invent exchange rates or automated FX conversion; mismatched currencies are treated as an explicit non-match or an unresolved policy requiring a future product decision).*
    - Review ratings: `tour_guides.rating`
  - The group compatibility formula (45/35/20) must **never** be applied to tour guides.
  - *Unresolved Scoring Weights*: The mathematical scoring weights and tie-breaking formula incorporating guide review ratings remain an open product decision awaiting formal approval. No unapproved formula is finalized.
  - *Implementation Gap Note*: In the current prototype code (`backend/app/ai/matching/guide_compatibility_scorer.py`), scoring awards up to 50 points for language overlap, 30 points for specialization match, and 20 points for budget compliance, while review rating is currently omitted.
- **Response (`200 OK`)**:
  ```json
  [
    {
      "guideId": "gid_401",
      "name": "Kenji Sato",
      "city": "Kyoto",
      "languages": ["en", "ja"],
      "specialization": "Historical Temples & Culinary Markets",
      "dayRate": "120.00",
      "currency": "USD",
      "rating": 4.95,
      "compatibilityScore": 94,
      "withinBudget": true
    }
  ]
  ```

---

## 2.7 Mandatory Trip Chat & Real-Time APIs

#### `POST /api/trips/{trpId}/chat`
- **Request**: `{ "content": "Let's do the hot springs instead!" }`
- **Response (`201 Created`)**: Chat message object with `msg_` prefix.

#### `POST /api/trips/{trpId}/chat/{msgId}/propose`
- **Purpose**: "Propose this as the plan" action button on a chat message.
- **Logic**:
  - **Unanimous Yes**: If 100% of applicable members (defined as all active confirmed trip members participating in that slot's planning context, excluding pending invitees) vote `yes`, the slot status immediately transitions to `CONFIRMED` and ongoing AI consensus loops terminate.
  - **Majority (Non-Unanimous)**: Queued as a standard proposal for the next consensus cycle.
  - **No Votes / No Response**: Dropped; active AI consensus continues.

---

## 2.8 Face Recognition & Photo Memories APIs (REQUIRED SERVICE BOUNDARY — OPTIONAL TRAVELER ENROLLMENT)

#### `POST /api/face/register`
- **Request**: Multipart form data with 3 images (`straight`, `left`, `right`).
- **Validation**: Rejects with HTTP 400 if any image fails single-face quality check.
- **Storage Representation**: Facial embeddings are logically represented as ArcFace 512-dimensional vectors. In the current prototype schema, storage as `JSONB` in `face_profiles.embedding_data` is an illustrative and provisional physical representation only; the final physical storage format and vector indexing approach remain open for stack verification and database review. Embeddings are never returned in client API responses. Face recognition remains strictly optional.

#### `GET /api/photos/memories/{trpId}`
- **Response**: Four segregated boards:
  1. `all`: Chronological array of all photos.
  2. `memberAlbums`: Photos grouped by recognized member IDs.
  3. `groupPhotos`: Photos containing $\ge 2$ registered members.
  4. `scenery`: Photos with zero detected faces.
  - *Detected Unregistered Faces*: Flagged as Unknown Guest photos; strictly excluded from `scenery`.

---

### 2.9 Form Validation Error Contract & Negotiation API

#### Standard Field Validation Error Response (`400 Bad Request`)
When client input violates master validation constraints (see `AI.md` Section 6), FastAPI returns a standardized RFC 7807 compliant error payload:
```json
{
  "type": "https://wandermatch.app/errors/validation-error",
  "title": "Form Validation Failed",
  "status": 400,
  "detail": "One or more submitted fields violated validation constraints.",
  "errors": [
    {
      "field": "costDelta",
      "code": "ERR_PRP_COST_DELTA_INVALID",
      "message": "Cost delta must be a valid decimal amount (e.g., 5.00 or -10.00)."
    },
    {
      "field": "rationale",
      "code": "ERR_PRP_RATIONALE_REQUIRED",
      "message": "Please provide a rationale explaining why this activity fits the trip."
    }
  ]
}
```

#### `POST /api/consensus/negotiate`
- **Purpose**: Generates evidence-grounded alternative options when a proposed activity violates temporal or road-distance constraints.
- **Fixture Type**: `[SYNTHETIC TEST FIXTURE — BALI SCENARIO]`
- **Request Body**:
  ```json
  {
    "trpId": "trp_bali_2026",
    "itmId": "itm_456",
    "proposedEntityId": "poi_mount_batur",
    "expectedVersion": 3
  }
  ```
- **Canonical Response Contract (`200 OK`)**:
  The response contract defines three canonical options (`opt_keep_original`, `opt_closer_alternative`, `opt_reschedule_next`). The governance fields (`governanceAction`, `requiresAdminAction`, and `requiresGroupVote`) are mode-dependent and explicitly separated below:

  **1. Mode A Response (`mode == "MODE_A"` — Admin Governed)**:
  ```json
  {
    "feasibilityStatus": "INFEASIBLE",
    "verificationStatus": "PARTIALLY_VERIFIED",
    "reason": "SCHEDULE_DEFICIT",
    "calculation": {
      "availableWindowMinutes": 300,
      "totalRequiredMinutes": 345,
      "deficitMinutes": 45,
      "outboundDriveMinutes": 80,
      "arrivalBufferMinutes": 15,
      "activityMinutes": 150,
      "departureBufferMinutes": 15,
      "returnDriveMinutes": 85,
      "totalBufferMinutes": 30
    },
    "explanation": "Mount Batur requires an 80m outbound drive, 15m arrival buffer, 150m trek, 15m departure buffer, and 85m return drive (total 345m / 5h 45m). With your Ubud Traditional Dance starting at 18:00, visiting Mount Batur now causes a 45-minute schedule deficit.",
    "options": [
      {
        "optionId": "opt_keep_original",
        "label": "Keep Existing Plan",
        "description": "Preserve your 18:00 Ubud Palace booking without adding Mount Batur.",
        "governanceAction": "NO_CHANGE",
        "requiresAdminAction": false,
        "requiresGroupVote": false
      },
      {
        "optionId": "opt_closer_alternative",
        "label": "Consider Closer Alternative",
        "description": "Visit Campuhan Ridge Walk: 12m outbound drive + 15m arrival buffer + 90m visit + 15m departure buffer + 12m return drive = 144m total (2h 24m). Leaves 2h 36m (156m) surplus before 18:00 commitment.",
        "candidateEntityId": "poi_campuhan_ridge",
        "governanceAction": "SUBMIT_PROPOSAL",
        "requiresAdminAction": true,
        "requiresGroupVote": false
      },
      {
        "optionId": "opt_reschedule_next",
        "label": "Discuss Moving Next Activity",
        "description": "Request moving the Ubud Palace Dance from 18:00 to 20:00 to accommodate Mount Batur.",
        "governanceAction": "REQUEST_RESCHEDULE",
        "requiresAdminAction": true,
        "requiresGroupVote": false
      }
    ]
  }
  ```

  **2. Mode NA Response (`mode == "MODE_NA"` — Collaborative Consensus)**:
  ```json
  {
    "feasibilityStatus": "INFEASIBLE",
    "verificationStatus": "PARTIALLY_VERIFIED",
    "reason": "SCHEDULE_DEFICIT",
    "calculation": {
      "availableWindowMinutes": 300,
      "totalRequiredMinutes": 345,
      "deficitMinutes": 45,
      "outboundDriveMinutes": 80,
      "arrivalBufferMinutes": 15,
      "activityMinutes": 150,
      "departureBufferMinutes": 15,
      "returnDriveMinutes": 85,
      "totalBufferMinutes": 30
    },
    "explanation": "Mount Batur requires an 80m outbound drive, 15m arrival buffer, 150m trek, 15m departure buffer, and 85m return drive (total 345m / 5h 45m). With your Ubud Traditional Dance starting at 18:00, visiting Mount Batur now causes a 45-minute schedule deficit.",
    "options": [
      {
        "optionId": "opt_keep_original",
        "label": "Keep Existing Plan",
        "description": "Preserve your 18:00 Ubud Palace booking without adding Mount Batur.",
        "governanceAction": "NO_CHANGE",
        "requiresAdminAction": false,
        "requiresGroupVote": false
      },
      {
        "optionId": "opt_closer_alternative",
        "label": "Consider Closer Alternative",
        "description": "Visit Campuhan Ridge Walk: 12m outbound drive + 15m arrival buffer + 90m visit + 15m departure buffer + 12m return drive = 144m total (2h 24m). Leaves 2h 36m (156m) surplus before 18:00 commitment.",
        "candidateEntityId": "poi_campuhan_ridge",
        "governanceAction": "SUBMIT_PROPOSAL",
        "requiresAdminAction": false,
        "requiresGroupVote": true
      },
      {
        "optionId": "opt_reschedule_next",
        "label": "Discuss Moving Next Activity",
        "description": "Request moving the Ubud Palace Dance from 18:00 to 20:00 to accommodate Mount Batur.",
        "governanceAction": "REQUEST_RESCHEDULE",
        "requiresAdminAction": false,
        "requiresGroupVote": true
      }
    ]
  }
  ```

  > [!IMPORTANT]
  > **Non-Mutation Invariant**: Choosing any negotiation option NEVER automatically mutates the itinerary. It either dismisses the modal (`NO_CHANGE`), forwards a proposal to the admin queue (Mode A), or initiates a collaborative group vote cycle (Mode NA). Itinerary items are mutated ONLY upon explicit admin confirmation (Mode A) or voting cycle finalization (Mode NA).

---

### 2.12 Itinerary PDF Export Specification (Required Capability)
`[APPROVED_REQUIREMENT]`
1. **Architecture & Data Flow**:
   - The user triggers `Download Itinerary as PDF` on `ResolvedItineraryScreen` or `TripHomeScreen`.
   - The export request is validated against Clerk JWT authentication and trip membership in PostgreSQL.
   - Authoritative itinerary slots, activities, chronological times, and venue metadata are serialized from Neon DB.
   - The PDF document is structured with:
     - **Header**: Trip Title, Destination, Travel Dates, Timezone, Itinerary Status Badge, Export Timestamp, Version Number.
     - **Trip Summary**: Organizer, group size, trip notes (within authorized visibility).
     - **Day-by-Day Itinerary**: Chronological activity blocks with start/end times, activity title, rationale, venue name, verified address, and verified road transit duration.
     - **Timing Integrity**: Travel duration is explicitly distinguished from activity duration. Straight-line Haversine calculations must never substitute for road network travel. Missing travel times render as em-dash (`—`), never fabricated.
     - **Watermark & Status Distinction**: If any slot is `EMPTY`, `IN_CONSENSUS`, or `BRANCHED`, the document includes a prominent diagonal watermark: `PROVISIONAL DRAFT — NOT CONFIRMED`.
     - **Footer & Pagination**: Page X of Y, clean page breaks (`break-inside: avoid` on activity blocks), typography optimized for monochrome/contrast printing.
2. **Rendering Strategy**:
   - Evaluation of Client-Side (`@react-pdf/renderer` or `jspdf`) vs Server-Side (FastAPI WeasyPrint / ReportLab) remains open under Decision #30 `[DECISION PENDING]`.

### 2.13 AI Accountability, Traceability & Consequence Framework
`[APPROVED_REQUIREMENT]`
1. **The 10-Stage AI Decision Lifecycle**:
   - **Stage 1 (Request)**: Initiated by user action, consensus trigger, or Mode A admin invocation with explicit trip, slot, and user context.
   - **Stage 2 (Context)**: Assembles input itinerary version, active proposals, votes, objection comments, and trip constraints.
   - **Stage 3 (Evidence)**: Gathers verified POI, road network routing, and venue operating hours. Haversine distance is prohibited as driving duration.
   - **Stage 4 (Generation)**: Model generates structured blended plan JSON according to strict Pydantic schemas.
   - **Stage 5 (Validation)**: Deterministic backend checks hard constraints (`VALID_ENTITY_TYPES` (validates entity category strings only; Decision #8 covers geocoding and coordinates, while broader factual verification of operating hours or venue claims remains an unintegrated evidence gap), cost delta decimal format, non-empty title/rationale, temporal feasibility).
   - **Stage 6 (Decision)**: Backend marks result as valid compromise candidate, infeasible, or rejected.
   - **Stage 7 (Action)**: Backend advances consensus round or initiates branching; AI never commits state.
   - **Stage 8 (Persistence)**: Slot consensus state updated in Neon DB; itinerary version incremented only upon human confirmation.
   - **Stage 9 (Notification)**: Real-time event (`aiRecommendationReady` or `slotStatusChanged`) broadcasted via WebSocket to authorized trip members.
   - **Stage 10 (Review)**: Revision history snapshot persisted in `revision_history`; human override logged append-only.
2. **Persistence Audit Gap Disclosure**:
   - `[CURRENT_VERIFIED]` `revision_history` captures slot snapshot data and author (`'ai'` or user ID).
   - `[IMPLEMENTATION_GAP]` A dedicated structured `ai_decision_audit` table capturing raw prompt version, token usage, and rejected constraint logs does not currently exist in the physical schema and remains pending Decision #29.

## 3. Optimistic Concurrency Control Contract

1. Every GET response returning an itinerary includes the itinerary-level concurrency version `version` (integer starting at 1 on `itineraries`).
2. Every mutation request affecting an itinerary or its child items MUST provide `expectedVersion`.
3. FastAPI executes conditional update on `itineraries`:
   ```sql
   UPDATE itineraries
   SET version = version + 1, updated_at = NOW()
   WHERE itinerary_id = :itinerary_id AND version = :expected_version;
   ```
4. If zero rows are updated, FastAPI rolls back the transaction and returns HTTP `409 Conflict`:
   ```json
   {
     "error": "CONFLICT",
     "message": "Itinerary schedule was modified by another member. Please reload the latest schedule."
   }
   ```

---

## 4. Structured Error Dictionary

| Error Code | HTTP Status | Trigger Condition |
| :--- | :--- | :--- |
| `INVALID_INVITE_CODE` | 400 | Invite code does not exist, has expired, or is revoked. |
| `TRIP_FULL` | 400 | Trip membership has reached `party_size`. |
| `ALREADY_MEMBER` | 400 | User is already an active member of the trip. |
| `MANDATORY_COMMENT_MISSING` | 400 | A `no` vote was submitted with an empty or whitespace comment. |
| `UNAUTHORIZED_PRIVATE_TRIP` | 403 / 404 | Caller is not a member of a private trip and lacks a valid invite code. |
| `FORBIDDEN_BASE_EDIT` | 403 | Non-admin member attempted direct base itinerary edit in Mode A. |
| `FORBIDDEN_REVERT` | 403 | Non-admin member attempted direct revision revert in Mode A. |
| `STALE_VERSION_CONFLICT` | 409 | `expectedVersion` does not match current database `itineraries.version`. |
| `DUPLICATE_JOIN_REQUEST` | 409 | User already has a pending or approved join request for this trip. |
| `VOTING_WINDOW_CLOSED` | 400 | Vote submitted after the 10-minute consensus window expired. |
| `AI_VALIDATION_FAILURE` | 422 | Generated plan failed hard constraint checks after retry; escalated to branching. |

### 2.10 Single Authoritative Timer Invariant
`[APPROVED_REQUIREMENT]` In Mode NA, exactly one authoritative deadline per contested slot and consensus cycle (`slot_consensus.closes_at`) controls voting. Competing proposals share this single slot-level deadline. The physical column `proposals.closes_at` acts strictly as a read-only projection/mirror of the slot timer, never an independent authority.

### 2.11 Bounded Clarification vs. Conversational Chat Scope
`[APPROVED_REQUIREMENT]` The system explicitly distinguishes between:
1. **Bounded Clarification Chips (In-Scope)**: When an objection is classified as `NEEDS_CLARIFICATION`, the API returns structured choice chips (e.g. selection between distinct POI entities or budget categories).
2. **Conversational Chatbot Follow-up (Out-of-Scope Non-Goal)**: Open-ended conversational dialogues, chatbot follow-ups, or requiring a No-voter to enter a text chat loop are strictly out of scope. Comments are processed strictly as submitted.
