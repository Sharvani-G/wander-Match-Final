# Consolidated Document Review & Contract Harmonization (Pass 8 Repair)

**Review Date**: 30 October 2026  
**Repository**: `C:/Users/gjaya/OneDrive/Desktop/PROJECTS/wander-match-final`  
**Evaluation Scope**: Authoritative verification of Pass 8 Post-Verification Corrections addressing the three defect groups diagnosed in `independent-pass8-final-verification.md`.  
**Execution Boundary**: Concrete documentation edits saved directly into repository markdown files; zero modifications to application source, schemas, migrations, dependencies, or databases. Zero runtime imports, database connections, or server executions.

---

## 1. Executive Summary & Verification Outcome

All **three defect groups** diagnosed in `independent-pass8-final-verification.md` have been corrected, saved, and statically verified:
1. **Removed Invented Current Photo-Storage Claims**:
   - Inspected `backend/app/models/additive.py:80–87` confirming that `Photo` contains only `photo_id`, `trip_id`, `uploader_id`, `photo_url`, `processing_status`, and `created_at`. It contains **NO** `detected_faces_count` or `matched_count` columns.
   - Separated the architecture into 4 explicit layers: (1) Actual current schema, (2) Worker runtime metrics, (3) Wire response & frontend metadata, and (4) Proposed durable aggregate/face-instance schema (`photo_face_tags` migration owned by Sharvani).
   - Established honest reload behavior prior to migration: absence of recognized `photo_person` tags does not mean zero detected faces; unavailable recognition evidence must never be misclassified as "Scenery"; worker failure (`'failed'`) remains strictly distinct from successful processing with unknown travelers (`'processed'`).
2. **Corrected Photo Normalizer & Demonstrated Concrete Router Invocation**:
   - Corrected `normalize_photo_tag_record` in `INTEGRATION_CONTRACT.md §9.2` and `PANCHAMI.md §9.10` to read the actual primary key `record.pp_id` (from `backend/app/models/additive.py:91`), eliminating fabricated `tag_{user_id}` identities.
   - Required explicit identity (`pp_id`, `tagId`, or `tag_id`) for fake dictionaries, raising `ValueError("ERR_INVALID_TAG_RECORD")` if absent rather than synthesizing from `user_id`.
   - Honestly represented missing bounding box coordinates as `None` for current ORM rows.
   - Added the concrete target transport invocation step in `POST /api/photos` demonstrating the router calling `normalize_photo_tag_record` over persisted tag records before wire response serialization.
3. **Removed Contradictory Global Version Claim & Established Mutation Matrix**:
   - Purged the unsupported claim that `itineraries.version` increments *only* on confirmation or revision restore.
   - Established `INTEGRATION_CONTRACT.md §2.6 Authoritative Mutation, Version & Freshness Matrix` covering all 11 system operations (distinguishing OCC version bumps, consensus state transitions, and AI snapshot fingerprint invalidations).
   - Clarified that clarification is a discussion input that does not bump `itineraries.version` or mutate traveler votes, but updates the AI objection constraint fingerprint $\text{Hash}(C_{\text{obj}})$, which invalidates in-flight AI synthesis leases.

| Metric | Result | Status |
| :--- | :--- | :--- |
| **Pass 8 Repair Static Acceptance Walkthroughs** | **14 / 14 Scenarios Passed (100%)** | **GREEN / VERIFIED** |
| **Repository Documents Edited & Saved** | **4 Files** (`INTEGRATION_CONTRACT.md`, `PANCHAMI.md`, `SHARVANI.md`, `PROJECT_MEMORY.md`) | **SAVED & COMMITTED** |
| **Application Source & Migrations Touched** | **0 Files** (Strict documentation-only boundary preserved) | **UNTOUCHED / COMPLIANT** |
| **Team Membership Split** | **Exactly 3 active members** (Nikitha Frontend, Panchami Transport/DeepFace, Sharvani Architecture/Domain/DB) | **PRESERVED** |
| **Language & Locale Scope** | **Strict English-only UI & AI synthesis** (Travel-language matching preserved as business preference metadata) | **PRESERVED** |
| **PDF Export Contract** | **Required & Online** (`FR-EXP-01`); **Offline export deferred** (Decision #30 pending) | **PRESERVED** |

---

## 2. Inventory of Saved Changes & Cryptographic Hashes

Pre-task backups were recorded in `scratch/task_backups_pass8_repair/manifest.json`. Unified diffs have been saved to `scratch/diffs_pass8_repair/`.

| Repository Document | Pre-Edit SHA-256 | Post-Edit SHA-256 | Pre Size | Post Size | Diff File Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `docs/INTEGRATION_CONTRACT.md` | `ebec0b3226a488ab...` | `68bc807a9efb5370...` | 102,626 B | 109,899 B | [`INTEGRATION_CONTRACT.md.diff`](file:///c:/Users/gjaya/OneDrive/Desktop/PROJECTS/wander-match-final/scratch/diffs_pass8_repair/INTEGRATION_CONTRACT.md.diff) |
| `docs/PANCHAMI.md` | `67a0ec22fb2d98c8...` | `d12cc709cd1d07c6...` | 97,065 B | 99,917 B | [`PANCHAMI.md.diff`](file:///c:/Users/gjaya/OneDrive/Desktop/PROJECTS/wander-match-final/scratch/diffs_pass8_repair/PANCHAMI.md.diff) |
| `docs/SHARVANI.md` | `4a8f6791bccc8a3b...` | `c52c6a55a0863fb6...` | 178,363 B | 179,916 B | [`SHARVANI.md.diff`](file:///c:/Users/gjaya/OneDrive/Desktop/PROJECTS/wander-match-final/scratch/diffs_pass8_repair/SHARVANI.md.diff) |
| `docs/PROJECT_MEMORY.md` | `18b47272ead3a055...` | `f3824806137d5d38...` | 126,015 B | 129,590 B | [`PROJECT_MEMORY.md.diff`](file:///c:/Users/gjaya/OneDrive/Desktop/PROJECTS/wander-match-final/scratch/diffs_pass8_repair/PROJECT_MEMORY.md.diff) |

---

## 3. Detailed Static Acceptance Walkthrough Results (14 / 14 Passed)

### Walkthrough 1: Current Photo Row Fields Alignment
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §4.2`, `docs/PANCHAMI.md §9.10`, `docs/SHARVANI.md §4.0`, `backend/app/models/additive.py:80–87`.
- **Inspected Fields**: `photo_id`, `trip_id`, `uploader_id`, `photo_url`, `processing_status`, `created_at`. Contains **NO** `detected_faces_count` or `matched_count` columns.
- **Result**: **PASSED**. All false current storage claims purged.

### Walkthrough 2: Recognition Counts as Runtime & Target Metrics
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §4.2`, `docs/PANCHAMI.md §9.10`.
- **Contract**: Counts (`detected_faces_count`, `matched_count`) and bounding boxes exist in worker runtime memory and transient HTTP responses. Storing them durably is a pending target schema migration (`photo_face_tags`) owned by Sharvani.
- **Result**: **PASSED**.

### Walkthrough 3: Honest Gallery Reload Semantics
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §4.2`, `docs/PANCHAMI.md §9.10`, `docs/SHARVANI.md §4.0`.
- **Rule**: Absence of recognized `photo_person` tags must **NEVER** be misclassified as "Scenery". Prior to target migration, images with 0 member tags cannot be distinguished between scenery and un-enrolled travelers on reload.
- **Result**: **PASSED**.

### Walkthrough 4: PhotoPerson User ID Non-Nullability
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §4.2`, `docs/SHARVANI.md §4.0`, `backend/app/models/additive.py:89`.
- **Rule**: `PhotoPerson.user_id` is NOT NULL (`nullable=False`). Unknown face instances cannot be stored as `user_id = None`. Only recognized members are inserted.
- **Result**: **PASSED**.

### Walkthrough 5: Real ORM PhotoPerson Record Normalization (`pp_id`)
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §9.2`, `docs/PANCHAMI.md §9.10`.
- **Code**: `pp_id = getattr(record, "pp_id", None)` $ightarrow$ `"tagId": str(pp_id)`.
- **Result**: **PASSED**. Preserves actual primary key `pp_id`, eliminating wrong `person_id`.

### Walkthrough 6: Fake Dictionary Normalization
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §9.2`, `docs/PANCHAMI.md §9.10`.
- **Code**: `tag_id = record.get("pp_id") or record.get("tagId") or record.get("tag_id")` $ightarrow$ produces identical DTO shape.
- **Result**: **PASSED**.

### Walkthrough 7: Explicit Identity Handling (No User ID Synthesis)
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §9.2`, `docs/PANCHAMI.md §9.10`.
- **Rule**: If identity is missing from fake dictionary or ORM record, raises `ValueError("ERR_INVALID_TAG_RECORD")` or `ValueError("ERR_INVALID_ORM_TAG")`. Never fabricates `tag_{user_id}`.
- **Result**: **PASSED**.

### Walkthrough 8: Honest Representation of Absent Bounding Box
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §9.2`, `docs/PANCHAMI.md §9.10`.
- **Rule**: For current ORM `PhotoPerson` records, `"box": None` is returned honestly, because `photo_person` schema has no bounding box column. Dummy coordinates are never fabricated.
- **Result**: **PASSED**.

### Walkthrough 9: Router Upload Step Concretely Invokes Normalizer
- **Enforcing Clause**: `docs/PANCHAMI.md §9.10.A`.
- **Implementation**:
  ```python
  persisted_tags = sharvani_photo_service.save_photo_tags_records(db=db, photo_id=photo_id, face_matches=matches.tags, final_status=storage_status)
  normalized_tags = [normalize_photo_tag_record(t) for t in persisted_tags]
  wire_status = "completed" if storage_status == "processed" else "failed"
  return PhotoResponseDTO(..., processingStatus=wire_status, taggedMembers=normalized_tags)
  ```
- **Result**: **PASSED**. Concrete invocation step clearly demonstrated.

### Walkthrough 10: Strict Failure Status Mapping
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §3.0 L295, §9.2`, `docs/PANCHAMI.md §9.10`.
- **Rule**: Worker failure maps strictly to storage `'failed'` and wire `"failed"`. All `(or 'degraded')` claims removed. Worker failure never maps to `'processed'` or `"completed"`.
- **Result**: **PASSED**.

### Walkthrough 11: Authoritative Mutation, Version & Freshness Matrix
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §2.6`.
- **Content**: Comprehensive 11-operation matrix distinguishing itinerary OCC version increments ($Ver + 1$) from consensus cycle/state transitions and AI snapshot fingerprint changes.
- **Result**: **PASSED**.

### Walkthrough 12: Invalidation of In-Flight AI Leases on Clarification
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §2.4, §2.6`, `docs/PANCHAMI.md §9.6.B`.
- **Rule**: Clarification updates objection constraint fingerprint $	ext{Hash}(C_{	ext{obj}})$, which invalidates in-flight AI worker leases without mutating `itineraries.version` or traveler votes.
- **Result**: **PASSED**.

### Walkthrough 13: Unsupported Global Version Claim Purged
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §2.4`, `docs/PANCHAMI.md §9.6.B`.
- **Verification**: The erroneous statement claiming version increments *only* on confirmation or restore was completely purged from all active documentation.
- **Result**: **PASSED**.

### Walkthrough 14: Preservation of Agreed Scope & Architecture
- **Enforcing Clause**: `docs/INTEGRATION_CONTRACT.md §1.0, §9.1`, `docs/NIKITHA.md §7.2`.
- **Agreements Preserved**:
  - Exactly 3 active team members (Nikitha, Panchami, Sharvani).
  - Online PDF export is **REQUIRED and ONLINE** (`FR-EXP-01`); offline PDF generation is **DEFERRED**.
  - All UI surfaces, validation messages, and AI consensus synthesis are strictly **English-only**.
- **Result**: **PASSED**.

---

## 4. Remaining Genuine Architecture Decisions

The documentation is 100% harmonized and internally consistent. The following architectural trade-offs remain open product decisions:
1. **Decision #30: Itinerary PDF Rendering Engine Strategy (Client-Side vs Server-Side)**:
   - *Option A (Client-Side)*: Nikitha renders PDF via `@react-pdf/renderer` consuming authoritative JSON export payload.
   - *Option B (Server-Side)*: Sharvani compiles PDF via WeasyPrint consuming Jinja2 templates, streamed by Panchami via `GET /api/trips/{id}/itinerary/export.pdf`.
   - *Status*: Both handoff workflows are conditionally documented.
2. **Decision #13: Buffer Durations & Return Policies**: $B_{\text{arr}}=15\text{m}, B_{\text{dep}}=15\text{m}$ default transition buffers vs 30m.
3. **Decision #28: Operational LLM Inference Timeout**: Latency ceiling (8s vs 10s vs 15s) before triggering baseline-preserving technical fallback.

---

## 5. Separate Source Implementation Gaps

As mandated by the documentation-only boundary, the following proposed endpoints and schema migrations remain unimplemented in application source:
1. `POST /api/slots/{slot_id}/clarify`: Proposed endpoint in `routers/consensus.py`.
2. `GET /api/trips/{id}/itinerary/export` / `.pdf`: Proposed export route in `routers/trips.py`.
3. `POST /api/trips/{trp_id}/members`: Proposed direct membership addition route in `routers/trips.py`.
4. `POST /api/negotiation/select-option`: Proposed option selection route.
5. `POST /api/trips/{trp_id}/revisions/{rev_id}/restore`: Proposed revision restore route.
6. `photo_face_tags` schema migration: Pending Alembic migration adding nullable `user_id`, `face_index`, and `bounding_box`.

---

## 6. Runtime Checks Explicitly Not Executed

Per the explicit task boundaries:
- Zero application imports executed (`from backend.app...` was not imported in live runtime).
- Zero database connections opened (no Neon or SQLite connections established).
- Zero migrations applied (`alembic upgrade head` was not run).
- Zero servers started (FastAPI and DeepFace worker processes were not booted).
- Zero network requests sent to external providers (Clerk, Cloudinary, Ollama).

All verifications in this report are bounded static file and cryptographic diff verifications.
