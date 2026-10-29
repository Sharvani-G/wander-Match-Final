# Database Documentation: WanderMatch Architecture, Schema & Data Persistence

**Product**: WanderMatch — Social & Group Travel Planning with an AI Consensus Planner  
**Hackathon / Problem Statement**: PS-11, KogniVera Hackathon 2026 (Travel & Tourism Track)  
**Team**: Chaosminds — Nikitha (Frontend); Panchami (HTTP/WebSocket Transport and DeepFace); Sharvani (Business Logic, AI/Consensus, Authentication, Database, Integration and Deployment)
**Document Status**: Canonical Reference — Verified Against Live PostgreSQL & Repository Code  
**Inspection Date**: October 27, 2026  
**Canonical Path**: `docs/DATABASE.md`  
**Active Mirror Path**: `ai/AIConsensus/docs/DATABASE.md`  

---

## 1. Document Purpose, Scope & Confidence Legend

This document is the definitive source of truth for all database architecture, physical schema tables, entity relationships, data ownership boundaries, persistence guarantees, migration management, and security constraints for **WanderMatch**.

To avoid mistaking proposed ideas or historical audit logs for active runtime behavior, every architectural statement and component in this document is tagged with an explicit confidence status:

| Status Tag | Definition & Evidence Standard |
| :--- | :--- |
| `[CURRENT_VERIFIED]` | Directly inspected in the active codebase or verified live against the primary PostgreSQL database. |
| `[IMPLEMENTED_VERIFIED]` | Implemented in backend code and proven through reproducible automated integration tests. |
| `[UNCONFIGURED_INACTIVE]` | Library or integration code exists in repository, but credentials/infrastructure are absent; operates in degraded or fallback mode. |
| `[DECISION_PENDING]` | Open architectural or product question requiring user/team sign-off before adoption. |
| `[CLEANUP_ON_HOLD]` | Action or data cleanup explicitly placed on hold; no destructive SQL may be executed. |
| `[DEFERRED_FOLLOW_UP]` | Non-blocking follow-up issue tracked for execution in a later implementation phase. |

---

## 2. Technology Stack & Persistence Tier Overview

| Component | Technology / Platform | Status | Architectural Role |
| :--- | :--- | :--- | :--- |
| **Primary Relational DB** | **Neon PostgreSQL 18.6** | `[CURRENT_VERIFIED]` | Authoritative, persistent system of record for all relational data. AWS `ap-southeast-1` region. |
| **ORM & Data Access** | **SQLAlchemy 2.0+** | `[CURRENT_VERIFIED]` | Object-relational mapping, declarative models, connection pooling (`pool_pre_ping=True`). |
| **Migration Engine** | **Alembic** | `[CURRENT_VERIFIED]` | Schema version control. Active revision: `c8a6a4789a32_initial_schema_baseline.py`. |
| **Authentication Authority** | **Clerk** | `[CURRENT_VERIFIED]` | Manages user identity; backend validates RS256/HS256 JWT claims before authorizing database operations. |
| **Real-Time Pub/Sub** | **In-Process ConnectionManager** | `[INSPECTED_IN_SOURCE]` | Class `ConnectionManager` present in `backend/app/websocket_manager.py:L14`; manages trip rooms in memory. Runtime integration test suite unexecuted in this documentation pass. |
| **Redis Cache / PubSub** | *None (Unconfigured)* | `[UNCONFIGURED_INACTIVE]` | Port 6379 not running; multi-instance horizontal scaling currently unneeded on single-instance dev/test tiers. |
| **Photo / Media Storage** | **Local Disk (`backend/static/uploads/`)** | `[CURRENT_VERIFIED]` | Ephemeral local development storage; Cloudinary credentials unconfigured. Requires durable S3/Cloudinary for Render production. |
| **Face Recognition Compute** | **DeepFace Service (Port 8001)** | `[CURRENT_VERIFIED]` | Separate microservice boundary. Raw 512-d embeddings kept private; main backend receives only matched `user_id` tags. |
| **External AI LLMs** | *Deterministic Algorithmic Fallback* | `[CURRENT_VERIFIED]` | No cloud LLM keys in `.env`; compromise synthesis and clustering operate deterministically via `blended_plan_generator`. |

---

## 3. High-Level Storage Architecture

```
[ Frontend Client (Vercel SPA) ]
       │                      │
  HTTP REST (FastAPI)     WebSocket (/ws/trips/{trip_id})
       │                      │
       ▼                      ▼
[ Backend Orchestrator (FastAPI on Render) ]
   ├── Authentication Guard (Clerk JWT Signature & Claims Verification)
   ├── Room Connection Manager (In-Memory Pub/Sub + State Resync Snapshot)
   └── SQLAlchemy 2.0 ORM Engine (pool_pre_ping=True)
       │
       ▼ (Direct SSL Connection)
[ Primary Relational Database: Neon PostgreSQL 18.6 ]
   ├── public schema (24 Application Tables + alembic_version)
   ├── Master Reference Data (currencies, languages, countries, cities, tour_guides: 261 rows)
   └── Application Relational State (users, trips, itineraries, proposals, votes, consensus, branches)

[ Auxiliary & Non-Authoritative Boundaries ]
   ├── Local File Storage (backend/static/uploads/): Ephemeral photo storage for dev/test
   └── Standalone DeepFace Service (localhost:8001): Private biometric processing, isolated SQLite/memory
```

---

## 4. Authoritative Data Ownership Boundaries

WanderMatch enforces strict separation of concerns regarding which tier owns the authoritative source of truth:

1. **Relational Application State (Authoritative Owner: Neon PostgreSQL)**
   - All user profiles, trips, memberships, itineraries, slots, proposals, votes, consensus cycles, branches, and photo metadata are persistently stored in Neon PostgreSQL `neondb`.
   - In-memory dictionaries (`TRIPS_DB = {}`) have been **completely eliminated** as state authorities.
2. **Real-Time Ephemeral State (Owner: `ConnectionManager` in `backend/app/websocket_manager.py`)**
   - Active WebSocket connections (`active_rooms: Dict[str, Dict[str, WebSocket]]`) are strictly transient.
   - Upon client connect or reconnect, the server queries Neon PostgreSQL and delivers an authoritative `resyncSnapshot`. No durable application records exist solely in memory.
3. **Biometric Face Embeddings (Owner: DeepFace Service Boundary)**
   - High-dimensional vector embeddings (ArcFace 512-d) reside strictly within the DeepFace service domain.
   - Neon PostgreSQL `face_profiles` stores only profile metadata (`model_version`, registration timestamp, status).
   - Neon PostgreSQL `photo_person` stores only the resulting member associations (`photo_id`, `user_id`, `confidence`).
4. **Media Binaries (Owner: Storage Layer)**
   - Image binary files are written to storage; Neon PostgreSQL `photos` table stores only the URL reference (`photo_url`), uploader metadata, and processing timestamps.

---

## 5. Complete Schema Inventory (24 Tables + 1 Migration Table)

The primary database `neondb` (schema `public`) contains **25 total tables**, categorized into 6 logical functional domains:

### Domain 1: Master Reference Catalogs (PRESERVED Reference Data)
Master tables containing read-only or platform-curated reference datasets.

| Table Name | Primary Key | Key Columns | Row Count | Purpose & Usage |
| :--- | :--- | :--- | :---: | :--- |
| `currencies` | `code` (VARCHAR) | `code`, `name`, `symbol` | 25 | ISO-4217 currency catalog (USD, EUR, INR, etc.). |
| `languages` | `code` (VARCHAR) | `code`, `name`, `native_name` | 26 | BCP-47 language catalog used in traveler compatibility matching. |
| `countries` | `country_id` (TEXT) | `code`, `name`, `continent` | 30 | ISO country master catalog. |
| `cities` | `city_id` (TEXT) | `name`, `country_id`, `latitude`, `longitude`, `timezone`, `cost_index` | 60 | Global destination city catalog; foreign key to `countries`. |
| `tour_guides` | `guide_id` (TEXT) | `city_id`, `name`, `languages`, `rating`, `day_rate`, `currency` | 120 | Verified destination local tour guides; foreign key to `cities`. |

### Domain 2: Identity, User Profiles & Preferences
| Table Name | Primary Key | Key Columns | Row Count | Purpose & Usage |
| :--- | :--- | :--- | :---: | :--- |
| `users` | `user_id` (TEXT) | `clerk_user_id`, `email`, `full_name`, `display_name`, `age`, `age_group`, `status` | 1,216 | Registered traveler identities, authentication mappings, and demographics. |
| `user_preferences` | `preference_id` (TEXT) | `user_id`, `preferred_languages`, `interests`, `pace`, `budget_band` | 1,209 | Traveler travel styles, pacing, and interests used for 45/35/20 compatibility scoring. |
| `user_interactions` | `interaction_id` (TEXT) | `user_id`, `target_id`, `interaction_type`, `created_at` | 12,339 | Historical traveler activity logs and behavioral signals. |
| `face_profiles` | `profile_id` (TEXT) | `user_id`, `model_version`, `embedding_data`, `registered_at` | 0 | Facial recognition enrollment status and model metadata. |

### Domain 3: Trips, Membership & Social Collaboration
| Table Name | Primary Key | Key Columns | Row Count | Purpose & Usage |
| :--- | :--- | :--- | :---: | :--- |
| `trips` | `trip_id` (TEXT) | `owner_user_id`, `title`, `destination_city_id`, `start_date`, `end_date`, `mode`, `status` | 605 | Core trip entity. `mode` designates Mode A (Admin-Led) or Mode NA (Collaborative). |
| `trip_members` | `member_id` (TEXT) | `trip_id`, `user_id`, `role`, `status` (`accepted`, `pending`) | 1,414 | Trip membership roster and authorization lookup. |
| `trip_invite_codes` | `code_id` (TEXT) | `trip_id`, `code` (INDEXED), `created_by_user_id`, `expires_at` | 0 | Shareable alphanumeric invite codes for joining private trips. |
| `join_requests` | `request_id` (TEXT) | `trip_id`, `user_id`, `status` (`pending`, `accepted`, `rejected`) | 0 | Requests from travelers wishing to join group trips. |
| `trip_chat_messages`| `message_id` (TEXT) | `trip_id`, `user_id`, `message`, `proposal_ref_id`, `created_at` | 4 | In-trip group chat records with optional proposal references. |

### Domain 4: Itineraries & Scheduled Slots
| Table Name | Primary Key | Key Columns | Row Count | Purpose & Usage |
| :--- | :--- | :--- | :---: | :--- |
| `itineraries` | `itinerary_id` (TEXT) | `trip_id`, `name`, `version` (INTEGER), `status` | 807 | Master itinerary shell. `version` enforces monotonic optimistic concurrency locking. |
| `itinerary_items` | `item_id` (TEXT) | `itinerary_id`, `day_index`, `sort_order`, `title`, `cost`, `currency`, `status` | 8,590 | Individual scheduled activity slots in the day-by-day itinerary. |

### Domain 5: Proposals, Consensus & Voting
| Table Name | Primary Key | Key Columns | Row Count | Purpose & Usage |
| :--- | :--- | :--- | :---: | :--- |
| `proposals` | `proposal_id` (TEXT) | `itinerary_id`, `target_item_id`, `proposed_by_user_id`, `title`, `rationale`, `cost_delta`, `status`, `closes_at` | 291 | Competing activity suggestions submitted by trip members for contested slots. |
| `votes` | `vote_id` (TEXT) | `proposal_id`, `user_id`, `value` (`yes`/`no`), `weight`, `comment`, `cast_at` | 772 | Binary votes cast on proposals. Strict application constraint: `no` requires non-empty comment. |
| `slot_consensus` | `consensus_id` (TEXT) | `item_id`, `slot_status`, `current_round`, `consensus_cycle`, `first_no_at` | 7 | Authoritative state machine tracking consensus rounds and status (`EMPTY`, `IN_CONSENSUS`, `BRANCHED`, `CONFIRMED`). |
| `branches` | `branch_id` (TEXT) | `item_id`, `parent_branch_id` (SELF-REF), `title`, `status` | 5 | Parallel itinerary branches created when group members diverge. |
| `branch_members` | `member_id` (TEXT) | `branch_id`, `user_id`, `confirmed` | 5 | Sub-group traveler assignment to specific parallel branches. |
| `revision_history` | `revision_id` (TEXT) | `item_id`, `version_number`, `snapshot_data` (JSON), `created_by` | 13 | Audit snapshots of itinerary items prior to modifications. |

### Domain 6: Photos & Memories
| Table Name | Primary Key | Key Columns | Row Count | Purpose & Usage |
| :--- | :--- | :--- | :---: | :--- |
| `photos` | `photo_id` (TEXT) | `trip_id`, `uploader_id`, `photo_url`, `processing_status`, `created_at` | 6 | Trip photo metadata records pointing to uploaded media. |
| `photo_person` | `pp_id` (TEXT) | `photo_id`, `user_id`, `confidence` | 0 | Auto-tagged member associations detected by DeepFace face matching. |

### Migration Metadata
| Table Name | Primary Key | Key Columns | Row Count | Purpose & Usage |
| :--- | :--- | :--- | :---: | :--- |
| `alembic_version` | `version_num` (VARCHAR) | `version_num` | 1 | Tracks active database migration revision: `c8a6a4789a32`. |

---

## 6. Entity Relationships & Foreign Key Constraints

All 34 foreign keys in the primary database enforce relational integrity with `ON DELETE NO ACTION` (no silent cascading deletes):

```
                        countries (30)
                              │
                              ▼
currencies (25)           cities (60)
      ▲                       │
      │                       ├──────────────────────┐
      │                       ▼                      ▼
      │                 trips (605) ◄───────── tour_guides (120)
      │                       │
      │         ┌─────────────┼─────────────────────────────┐
      │         ▼             ▼                             ▼
      │   itineraries (807)  trip_members (1,414)      photos (6) ◄─── photo_person (0)
      │         │             │                             │               │
      │         ▼             │                             │               │
      │   itinerary_items     │                             │               │
      │     (8,590)           │                             │               │
      │         │             │                             │               │
      │    ┌────┴────┬────────┴──────┐                      │               │
      │    ▼         ▼               ▼                      │               │
      │ proposals  slot_consensus  branches (5)             │               │
      │   (291)        (7)           │ (parent_branch_id)   │               │
      │    │                         ▼                      │               │
      │    ▼                   branch_members (5)           │               │
      │  votes (772)                                        │               │
      │                                                     │               │
      └────────────────────────── users (1,216) ────────────┴───────────────┘
                                     │
                 ┌───────────────────┼────────────────────┐
                 ▼                   ▼                    ▼
        user_preferences    user_interactions       face_profiles
            (1,209)              (12,339)                (0)
```

### Self-Referencing Foreign Key Rule
- Table `branches` contains `branches.parent_branch_id -> branches.branch_id`.
- Child sub-branches must be deleted or nullified prior to deleting root branches to prevent self-referential constraint violations.

---

## 7. Data Flow & Transaction Lifecycle for Critical Operations

### 7.1 Activity Proposal Submission (`POST /api/proposals`)
1. **Auth Verification**: Token extracted; authenticated identity checked against `trip_members`.
2. **Item & Consensus Lookup**: Queries `itinerary_items` and `slot_consensus`.
3. **Transaction**:
   - Inserts `proposals` record (`status = 'open'`).
   - Updates `slot_consensus.slot_status = 'in_consensus'` and increments `current_round`.
   - `db.commit()` commits the transaction to Neon PostgreSQL.
4. **Broadcast**: `ws_manager.broadcast_to_trip()` emits `proposalCreated` to all connected trip members.

### 7.2 Voting & Unanimous Fast-Path (`POST /api/votes`)
1. **Single Active Vote**: Checks if `(proposal_id, user_id)` already exists in `votes`. If present, updates `value` and `comment` (vote retraction/change); if not, creates new `Vote`.
2. **Evaluation**: Queries all votes for the proposal.
   - **Unanimous YES Fast-Path**: If all accepted trip members voted `yes` and `no_votes == 0`:
     - Sets `proposals.status = 'accepted'`.
     - Sets `slot_consensus.slot_status = 'confirmed'`.
     - Updates `itinerary_items.title = proposal.title` and adjusts `cost`.
     - Commits transaction atomically.
     - Emits `voteCast` and `slotStatusChanged` (`CONFIRMED`).
   - **Contested Slot (Mode NA)**: If first `no` vote lands:
     - Sets `slot_consensus.first_no_at = NOW()`.
     - Emits `voteCast` and triggers consensus reconciliation.
   - **Contested Slot (Mode A)**:
     - No automatic countdown timer is set; advisory AI recommendations are generated for admin review.

### 7.3 Optimistic Concurrency on Itinerary Updates
- `itineraries.version` is monotonically incremented on write.
- Updates execute conditional matching: `WHERE itinerary_id = :id AND version = :expected_version`. If another client updated the itinerary concurrently, zero rows match and FastAPI raises `HTTP 409 Conflict`.

---

## 8. WebSocket Authentication & Security Boundaries

- **Token Inspection**: Query parameter `?token=<jwt>` is validated on connection:
  - Cryptographic signature check against `CLERK_SECRET_KEY` (HS256) or Clerk JWKS (RS256).
  - Expiration (`exp`) and issuer (`iss`) claim verification.
- **Identity Derivation**: Authenticated identity is derived strictly from token `sub`.
- **Anti-Forgery Enforcement**: If a URL path specifies `/ws/trips/{trip_id}/{user_id}`, the server validates `user_id == token_sub`. Any impersonation attempt immediately terminates the connection with WebSocket close code `4403`.
- **Pre-Snapshot Membership Gate**: Queries `trips` and `trip_members` in Neon PostgreSQL. If the authenticated traveler is not an accepted member, connection is rejected with code `4403`. No data snapshot is delivered to unauthorized clients.

---

## 9. Migration Engine & Baseline Verification

- **Tooling**: Alembic configured in `backend/alembic.ini` and `backend/alembic/env.py`.
- **Active Revision**: `c8a6a4789a32_initial_schema_baseline.py` in `backend/alembic/versions/`.
- **Target Metadata**: Reconstructs all 24 application models from `app.models.provided` and `app.models.additive`.
- **Verification Testing (Executed on `wandermatch_alembic_test`)**:
  1. `alembic upgrade head` executed on fresh, empty database: **Created all 25 tables successfully**.
  2. `alembic downgrade base` executed: **Dropped all 24 application tables cleanly** (0 tables remaining).
  3. `alembic upgrade head` re-executed: **Recreated all 25 tables with identical schemas**.
- **Primary Database Status**: Stamped at `c8a6a4789a32 (head)` without data loss or schema disruption.

---

## 10. Backup, Restore & Data Integrity Evidence

### 10.1 PostgreSQL Version Incompatibility Finding
- The primary Neon server runs PostgreSQL **18.6**.
- The standard local `pg_dump.exe` client on the developer workstation is version **15.4**.
- Standard `pg_dump` commands abort on major-version mismatch (`server version: 18.6; pg_dump version: 15.4`).

### 10.2 Implemented Version-Independent Archive
- Created streaming, column-explicit backup utility: `scratch/verify_backup_restore.py`.
- Dumps data using PostgreSQL native `COPY "{table}" ("col1", ...) TO STDOUT`.
- Generates compressed archive: `scratch/backups/neondb_verified_backup.tar.gz` (865,480 bytes), kept strictly outside version control.

### 10.3 Restoration Verification on `wandermatch_test_restore`
- **Measured Backup Time**: 5.69 seconds
- **Measured Restore Time**: 13.84 seconds
- **Verification Evidence**: Restored exactly **27,544 rows out of 27,544 rows** across all 24 tables (**100.0% exact parity**).

---

## 11. Database Cleanup Status: EXPLICITLY ON HOLD

> [!CAUTION]
> **NO DESTRUCTIVE ACTIONS HAVE BEEN EXECUTED ON THE PRIMARY DATABASE.**
> The primary database `neondb` remains completely intact with its 27,283 supplied-dataset transactional rows.

- **Current Inventory**:
  - **19 Transactional Tables**: 27,283 rows (pre-seeded hackathon test data).
  - **5 Reference Master Tables**: 261 rows (currencies, languages, countries, cities, tour guides).
- **Cleanup Policy**:
  - Cleanup is **ON HOLD** pending explicit user review and approval.
  - No `DELETE`, `TRUNCATE`, or `DROP` statements may be executed against `neondb`.
- **Dry-Run Validated Deletion Sequence (Child-to-Parent)**:
  1. `user_interactions` (12,339 rows)
  2. `trip_chat_messages` (4 rows)
  3. `votes` (772 rows)
  4. `branch_members` (5 rows)
  5. `branches` child rows (`parent_branch_id IS NOT NULL`) then root `branches` (5 rows total)
  6. `slot_consensus` (7 rows)
  7. `revision_history` (13 rows)
  8. `proposals` (291 rows)
  9. `photo_person` (0 rows)
  10. `photos` (6 rows)
  11. `trip_invite_codes` (0 rows)
  12. `join_requests` (0 rows)
  13. `itinerary_items` (8,590 rows)
  14. `itineraries` (807 rows)
  15. `trip_members` (1,414 rows)
  16. `trips` (605 rows)
  17. `user_preferences` (1,209 rows)
  18. `face_profiles` (0 rows)
  19. `users` (1,216 rows)

---

## 12. Approved Domain Rules & Behavioral Discrepancies

The following approved product requirements are tracked for database layer alignment. *(Note: Status labels reflect static source and schema inspection; no runtime tests or database mutations were executed during this documentation reconciliation)*:

| Domain Rule | Approved Requirement | Implementation Status | Source Evidence & Reconciled Target Behavior |
| :--- | :--- | :---: | :--- |
| **Consensus Authority** | Mode A: Admin final say; Mode NA: Collaborative | `[INSPECTED_IN_SOURCE]` | Enforced in `backend/app/routers/consensus.py` (Mode A owner confirmation endpoint vs Mode NA collaborative window). |
| **Binary Voting** | Votes are strictly `yes` or `no` | `[INSPECTED_IN_SOURCE]` | Schema accepts string, API strictly validates `yes`/`no`. `abstain` is strictly prohibited. |
| **NO Vote Comment** | Non-empty rationale required for `no` | `[INSPECTED_IN_SOURCE]` | Validated at API boundary (`len(comment.strip()) >= 1`) before insert into `votes`. |
| **Single Active YES** | At most 1 active YES vote per user **per slot** across all proposals | `[PARTIALLY_IMPLEMENTED]` | Physical schema enforces `uq_proposal_user_vote` (per-proposal uniqueness; `models/provided.py:L157`). Slot-level single active YES across competing proposals is an authoritative target invariant (`AC-VOT-02`) requiring transactional CAS enforcement in domain service. |
| **Round 3 Cap** | Enforced only after Round 3 window closes | `[PARTIALLY_IMPLEMENTED]` | Column `slot_consensus.current_round` exists in ORM (`additive.py:L23`). Window closure guard (`NOW >= closes_at`) and round cap branching are specified in domain orchestrator contracts; automated background cron scheduler is documented target. |
| **Compatibility Weights** | PRD Target: 45% interests, 35% languages, 20% age | `[DISCREPANCY_NOTED]` | Mounted scorer (`group_compatibility_scorer.py`) implements 40% Interests, 30% Language, 20% Dates, 10% Age. Reconciled as: PRD 45/35/20 remains target discovery policy; mounted 40/30/20/10 preserved as active prototype implementation. |
| **Mode NA Timer Window** | 10-minute voting window upon first NO vote | `[DECISION_PENDING]` | Present in consensus router (`first_no_at + 10m`). Product sign-off pending formal review under Decision #31. |

---

## 13. Deferred Performance Follow-Up Issue

### Issue Title
**Investigate and Optimize Slow Navbar Navigation and Page Transitions** `[DEFERRED_FOLLOW_UP]`

### Problem Description
Switching between navigation tabs and pages in the WanderMatch frontend introduces noticeable latency and loading delays. The root cause is currently unmeasured and unisolated.

### Execution Policy & Scheduling
- **Status**: Formally deferred. No profiling or speculative code modifications are permitted during this database documentation phase.
- **Investigation Sequence**:
  1. Complete database documentation.
  2. Verify all shared project documents (`PRD.md`, `TRD.md`, `ARCHITECTURE.md`, `AI.md`, `DEPLOYMENT.md`).
  3. Prepare member-specific implementation plans.
  4. Conduct focused performance profiling at the designated follow-up stage.

### Investigation Protocol (When Authorized)
- Capture browser network waterfalls and CPU profiles for route transitions.
- Measure API latency vs. client-side React rendering time vs. database query latency.
- Inspect bundle chunk sizes, lazy-loaded route boundaries, and re-render triggers.
- Check for duplicate or blocking authentication calls during route changes.
- Establish measured before-and-after benchmarks; do not introduce speculative caching or Redis without empirical justification.

---

## 14. Verification Sources & Audit Evidence Reference

- **Primary Database Connection**: Neon PostgreSQL 18.6 direct connection on AWS `ap-southeast-1`.
- **Baseline Migration Revision**: `backend/alembic/versions/c8a6a4789a32_initial_schema_baseline.py`.
- **Integration Test Suite**: `scratch/test_e2e_verified.py` (16/16 verified tests passing).
- **Verified Backup Artifact**: `scratch/backups/neondb_verified_backup.tar.gz` (865,480 bytes, 27,544 rows verified restorable).
- **Dry-Run Cleanup Script**: `scratch/dry_run_cleanup.py` (27,283 rows deleted on test restore DB, 261 reference rows preserved).
