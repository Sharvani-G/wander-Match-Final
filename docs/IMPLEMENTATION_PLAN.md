# WanderMatch — Implementation Plan

**Specification Status**: Updated Draft — Pending User Review


**PS-11 · KogniVera Hackathon 2026 · Team Chaosminds**  
**Sprint Window**: 24h Sprint (24 Sep 12:00 → 25 Sep 12:00)

Active ownership is governed by [INTEGRATION_CONTRACT.md](INTEGRATION_CONTRACT.md) and the three member documents. The original plan is preserved in [historical reference](archive/former-team/IMPLEMENTATION_PLAN-before-three-member-team.md); its old ownership and sprint assignments are superseded.

---

## 1. Active Three-Member Team

| Member | Responsibilities | Main document |
| :--- | :--- | :--- |
| Nikitha | Frontend, UI refinements, client adapters/mocks, browser HTTP/WS integration, PDF presentation and frontend tests | [NIKITHA.md](NIKITHA.md) |
| Panchami | HTTP/WS transport, wire schemas, recognition adapters and complete DeepFace processing implementation | [PANCHAMI.md](PANCHAMI.md) |
| Sharvani | Business logic, AI/consensus, authentication/authorization, shared database/schema/migrations, persistence, integration and all deployment coordination | [SHARVANI.md](SHARVANI.md) |

There is no fourth active member. Each member edits only her own main document after initial preparation. Shared contract changes are maintained by Sharvani; cross-owner code changes require coordination with the owner.

---

## 2. The Naming Contract (Read this before writing any code)

This is the single biggest conflict-preventer in the whole plan. Every track, every prompt, every session follows this without exception:

- **PostgreSQL and Python**: `snake_case` for every table, column, and internal variable — matches the provided PS-11 schema exactly, per Rule R1 (never rename or re-key provided fields).
- **FastAPI JSON responses**: `camelCase` at the API boundary. FastAPI/Pydantic models handle the `snake_case` → `camelCase` conversion; the frontend never sees a `snake_case` key.
- **TypeScript types**: match the `camelCase` API responses exactly, field for field. The frontend's dummy-data shapes (already locked in the UI/UX doc) already use this convention — do not invent new field names when wiring real data in, reuse the dummy names verbatim.
- **WebSocket event names**: `camelCase`, verb-first: `voteCast`, `proposalCreated`, `branchConfirmed`, `slotStatusChanged`, `aiPlanGenerated`. This exact list is the complete set for the MVP; do not add ad hoc events without updating this file.
- **IDs**: opaque, prefixed strings from the provided dataset conventions (`usr_`, `trp_`, `prp_`, `vot_`, etc. for provided tables; same pattern for new tables — `brc_` for branches, `bmb_` for branch_members, `rev_` for revision_history, `msg_` for trip_chat_messages, `fcp_` for face_profiles, `pho_` for photos). Never parsed, never assumed sequential.
- **Money**: always a `decimal(12,2)` + ISO-4217 currency code pair. Never a float, anywhere, on either side of the stack.
- **Enums**: lowercase `snake_case`, values only from `data/enums.json` for provided tables; new enums (slot status, branch status) follow the same style.
- **Votes are binary**: `value` is `yes` or `no` only. The dataset's `votes.value` enum technically allows abstain — do not use it. Treat it as a legacy value that exists in seed data but is never written by WanderMatch.
- **Votes.weight**: `votes.weight` exists in schema but is UNUSED for MVP.

> **Standing Instruction**: Paste this section into every phase's prompt, every time, regardless of track.

---

## 3. Directory Ownership

| Files / area | Owner | Boundary |
| :--- | :--- | :--- |
| `frontend/` and `docs/NIKITHA.md` | Nikitha | Frontend implementation; no direct database access |
| `backend/app/routers/`, `backend/app/schemas/`, `backend/app/websocket_manager.py`, recognition adapters, `ai/DeepFace/`, `docs/PANCHAMI.md` | Panchami | Transport and recognition; call Sharvani's services for authoritative rules and persistence |
| `backend/app/main.py`, `backend/app/services/`, `backend/app/models/`, `backend/app/database.py`, `backend/alembic/`, `backend/app/ai/matching/`, `ai/AIConsensus/`, shared data/configuration/deployment, `docs/SHARVANI.md`, `docs/INTEGRATION_CONTRACT.md` | Sharvani | Domain, security, database, AI, shared startup and integration authority |

Sharvani authors and manages shared schema and migrations. Panchami requests required changes. This ownership statement does not authorize running migrations or changing live data. Existing mixed-responsibility files require coordinated extraction before simultaneous edits.

---

## 4. Architecture — Properly Differentiated by Feature

### 4.1 Mode A vs Mode NA — Shared Core, Separate Orchestrators
```
/backend/ai/
  core/
    blended_plan_generator.py      <- mode-agnostic: reads proposals + votes + suggestions, returns ONE candidate
    branch_trigger_classifier.py   <- mode-agnostic: fixable tweak vs genuinely incompatible
    branch_grouping.py             <- mode-agnostic: clusters holdouts into N branches, recursive
    hard_constraint_validator.py   <- mode-agnostic: rejects a plan that breaks time/location/transport
  modes/
    mode_a_orchestrator.py         <- Admin-Led control flow ONLY: admin approval gates, advisory round cap
    mode_na_orchestrator.py        <- No-Admin control flow ONLY: fully automatic, hard round cap → auto-branch
```

### 4.2 Face Recognition — Fully Isolated, Optional Module
```
/backend/services/face/
  registration.py     <- capture quality-check, embedding generation (DeepFace.represent)
  matching.py          <- DeepFace.find against registered trip members, confidence threshold gate
  models.py            <- face_profiles, photos, photo_person table access
```

### 4.3 Solo-to-Group vs Solo-to-Guide — Two Scorers, One Pattern
- `group_compatibility_scorer.py`: age group, languages, interests, dates, against `trips`/`trip_members`/`user_preferences`.
- `guide_compatibility_scorer.py`: language, specialisation, price (and rating), against `tour_guides`.

---

## 5. Historical Sprint Timeline

The original timeline and former team assignments are preserved in [the historical plan](archive/former-team/IMPLEMENTATION_PLAN-before-three-member-team.md). They are not active work assignments. Use the three current member documents and shared integration contract for current work.

## 6. Git Mechanics & Branching Rules

- **`main`**: Protected, only receives merges at Checkpoint 1 (Hour 12) and Checkpoint 2 (Hour 21), always demo-safe. No one touches `main` directly.
- **`develop`**: Shared integration branch, everyone merges here first.
- **Track Feature Branches** (branched from `develop`):
  - `feature/frontend` (Nikitha)
  - `feature/backend` (Panchami)
  - `feature/ai` (Sharvani)
  - `feature/setup` (Sharvani)
- **Git Workflow Rules**:
  1. Pull `develop` before every work session.
  2. Commit small, commit often.
  3. One-line PR self-review before merging into `develop` (even solo, re-read your own diff once before it merges).
  4. No one touches `main` directly.

---

## 7. What's Explicitly Out of Scope

- Multilingual support (English only, final).
- Admin-inactivity auto-fallback.
- Self-hosting large cloud LLM clusters (Local Ollama SLM evaluation is in-scope).
- Live face recognition during judging (bulk photo matching is pre-processed; only single-user registration capture is demoed live).
- AI follow-up questioning of a No-voter (comments used strictly as submitted).
- Deep AI-training detail.
- Harmony Score & Weighted Voting (Harmony Score cut entirely; `votes.weight` present in schema but unused for MVP).

> **Note on Face Recognition**: Face recognition itself is optional, not cut — see Section 4.2 and Section 5 (Phase 2).

---

## 8. Stack-Neutral Future Work Items & Verification Gates

> **Canonical System Specification Reference**: All future implementation milestones must strictly adhere to the architecture, state machines, validators, and evaluation methodologies defined in [AI.md](AI.md) (and [ai/AIConsensus/docs/AI.md](AI.md)).

### 8.1 Future Work Packages (Post-Approval)
1. **WP-AI-01: Local Model Benchmarking & Promptfoo Evaluation**:
   - Set up Promptfoo test runner against local Ollama runtime (`phi4:mini` 3.8B and `qwen2.5-coder:latest`).
   - Execute regression test suite covering the 90 numbered test scenarios across all 5 categories (40 consensus, 20 geographic, 10 model reliability, 10 form validation, 10 security/biometric) in `AI.md Section 10`.
   - Validate structured JSON schema generation and Pydantic v2 parsing without temperature drift.
2. **WP-GEO-02: Geospatial Route Feasibility Engine**:
   - Integrate stack-neutral road-routing service (e.g., local OSRM instance over OpenStreetMap network).
   - Implement the two-leg route feasibility inequality ($B_{arr}, B_{dep} \ge 15\text{m}$) and return calculation.
   - Implement the 3-option schedule negotiation generator.
3. **WP-DB-03: Authoritative Database Persistence & OCC**:
   - Finalize PostgreSQL physical schema for logical persistence entities (`slc_`, `aud_`, `rfe_`).
   - Enforce `itineraries.version` optimistic concurrency checks on all consensus mutations.
   - Migrate in-memory `ConsensusManager` state to durable PostgreSQL transaction boundaries.
4. **WP-VAL-04: Master Field Validation & RFC 7807 Error Responses**:
   - Enforce master field validation across all FastAPI routes (`backend/app/`) and frontend forms (`frontend/src/`).
   - Implement strict ISO-4217 and `DECIMAL(12,2)` money types.

### 8.2 Architectural Invariants & Current Status
- **Current Status**: `Updated Draft — Pending User Review`.
- **Stack Verification**: Has NOT started. Dependencies, packages, and model tags are not locked.
- **Physical Schema**: Has NOT started. No database migrations or schema alterations have been executed.
- **Code Execution**: Has NOT started. Application source code and existing tests remain strictly untouched.
