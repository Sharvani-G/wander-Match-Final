> **HISTORICAL SNAPSHOT — NOT ACTIVE INSTRUCTIONS.** Active team: Nikitha, Panchami and Sharvani only. Current ownership and requirements: [root document](../../../docs/DEPLOYMENT.md) and [shared contract](../../../docs/INTEGRATION_CONTRACT.md). Earlier member assignments in this snapshot are superseded.

# Deployment & Operations Documentation: WanderMatch

**Product**: WanderMatch — Social & Group Travel Planning with an AI Consensus Planner  
**Hackathon**: KogniVera Hackathon 2026 (Problem Statement PS-11, Travel & Tourism Theme)  
**Team**: Chaosminds — Nikitha (Frontend); Panchami (HTTP/WebSocket Transport and DeepFace); Sharvani (Business Logic, AI/Consensus, Authentication, Database, Integration and Deployment)
**Specification Status**: Updated Draft — Pending User Review  
**Canonical AI Specification Reference**: For model evaluation suites, runtime failure policies, and telemetry storage rules, consult the canonical [AI System Specification](AI.md).

---

## 1. Deployment Targets & Infrastructure Stack

| Service Component | Target Infrastructure Host | Description & Tech Stack |
| :--- | :--- | :--- |
| **Frontend UI** | **Vercel** | React 19.2.8, TypeScript ~6.0.2, Tailwind CSS 4.3.3, Vite 8.3.0 build output. Serves static bundle and connects via REST/WebSockets to backend. |
| **Backend Orchestrator** | **Render** | FastAPI web service running Python 3.11+, Uvicorn server, SQLAlchemy ORM, and WebSocket connection hub. |
| **Real-Time WebSocket Hub** | **FastAPI In-Process Hub [CURRENT — VERIFIED] / Redis Pub/Sub [TARGET — UNCONFIGURED]** | WebSocket rooms managed in-process via ConnectionManager with Clerk JWT validation and membership checks. Operates correctly on a single Render web service instance. Redis pub/sub broker is currently UNCONFIGURED and is required for multi-instance horizontal scaling. |
| **Database System of Record** | **Neon Managed PostgreSQL [CONFIRMED SYSTEM OF RECORD]** | AWS ap-southeast-1 (PostgreSQL 18.6), unpooled connection for Alembic DDL, connection pooler for runtime. Houses 24 application tables, 34 foreign keys, stamped at Alembic baseline revision `c8a6a4789a32`. |
| **DeepFace Face Recognition Service** | **Render (Candidate)** | Isolated Python worker service running DeepFace / ArcFace embedding extraction logic. Required application processing service; traveler facial enrollment is optional; failures are non-blocking. |
| **Authentication Service** | **Clerk (Hosted)** | User identity management, social logins, and webhook event emitter syncing users to PostgreSQL. |
| **Photo Storage & CDN** | **Cloudinary [TARGET — CURRENTLY UNCONFIGURED]** | Cloudinary SDK declared in backend requirements. Currently UNCONFIGURED in runtime environment (no API keys in .env). Backend currently stores uploads on local disk under `backend/static/uploads/`, which is EPHEMERAL on Render container restarts. Configuring Cloudinary or an external persistent media store is a required production deployment prerequisite. |
| **AI LLM Engine (Candidate)** | **Local Ollama Runtime** | Local serving of Phi-4 Mini (3.8B) and Qwen2.5-Coder. Supports offline inference and zero API cost. |
| **Model Evaluation Suite** | **Promptfoo CLI** | Local regression testing and evaluation matrix runner. Interfaces via Ollama provider. |
| **Observability Service (Dev)** | **Arize Phoenix** | Development tracing and validation span capture; deployed with isolated ephemeral local storage. |
| **Geospatial Routing Service** | **OSRM (Candidate)** | Open Source Routing Machine computing topological road distances and durations over OSM data. |

---

## 2. Environment Variables Matrix (`.env.example`)

Below are the required environment configuration keys for production deployment:

```bash
# --- CLERK AUTHENTICATION ---
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...    # Clerk publishable API key for React frontend auth SDK
CLERK_SECRET_KEY=sk_test_...             # Clerk secret key for FastAPI JWT validation middleware
CLERK_WEBHOOK_SECRET=whsec_...           # Secret for verifying Clerk user creation webhooks

# --- DATABASE CONNECTION ---
DATABASE_URL=postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_NEON_HOST/YOUR_DATABASE?sslmode=require # Confirmed Neon PostgreSQL connection string (pooler for runtime; unpooled for Alembic migrations)




# --- CLOUDINARY MEDIA STORAGE ---
CLOUDINARY_CLOUD_NAME=wandermatch         # Cloudinary cloud identifier for trip photo uploads
CLOUDINARY_API_KEY=123456789             # Cloudinary API authentication key
CLOUDINARY_API_SECRET=abc123xyz...       # Cloudinary secret key for signed upload signatures

# --- BACKEND CORS & WEBSOCKET URLS ---
VITE_API_BASE_URL=https://wandermatch-api.onrender.com # Production FastAPI REST endpoint base URL
VITE_WS_BASE_URL=wss://wandermatch-api.onrender.com/ws # Production WebSocket endpoint base URL
```

---

## 3. Sequential Deployment Pipeline

To prevent race conditions, deployment MUST proceed in the following strict order:

```
┌────────────────────────┐     ┌────────────────────────┐     ┌────────────────────────┐     ┌────────────────────────┐
│   Step 1: Database     │ ──► │   Step 2: Backend      │ ──► │   Step 3: Frontend     │ ──► │   Step 4: Smoke Test   │
│   Provision & Seed     │     │   Render Deployment    │     │   Vercel Deployment    │     │   End-to-End Live Check│
└────────────────────────┘     └────────────────────────┘     └────────────────────────┘     └────────────────────────┘
```

1. **Step 1: Database Provisioning & Schema Migration**:
   - Provision Managed PostgreSQL instance: Neon Managed PostgreSQL (`neondb` on AWS ap-southeast-1) is the confirmed system of record.
   - Execute `alembic upgrade head` using direct (unpooled) PostgreSQL connection credentials to create all 24 unified tables stamped at baseline revision `c8a6a4789a32`.
   - Database cleanup policy: Primary database `neondb` houses 27,544 rows (27,283 historical transactional records under `[CLEANUP_ON_HOLD]` + 261 reference rows). Ad-hoc SQL DDL and raw `seed_data.sql` scripts are obsolete and strictly prohibited.
2. **Step 2: Backend Deployment on Render**:
   - Deploy FastAPI application repository branch to Render.
   - Configure environment variables (`DATABASE_URL`, `CLERK_SECRET_KEY`, `CLERK_WEBHOOK_SECRET`, etc.).
   - Verify health check endpoint returns `HTTP 200 OK` at `https://wandermatch-api.onrender.com/api/health`.
3. **Step 3: Frontend Deployment on Vercel**:
   - Deploy React Vite repository to Vercel.
   - Set environment variables (`VITE_API_BASE_URL`, `VITE_WS_BASE_URL`, `VITE_CLERK_PUBLISHABLE_KEY`) pointing directly to the live Render backend URL.
4. **Step 4: Production End-to-End Smoke Test**:
   - Perform live smoke test on the production Vercel URL (not localhost).
   - Verify dual-browser live WebSocket syncing (`voteCast`), proposal creation, AI blended plan generation, and deterministic solo matching.

---

## 4. Rollback & Emergency Strategy

> [!WARNING]
> **Production Branch Protection Rule**: The `main` git branch MUST remain in a 100% demo-safe, deployable state at all times.

- If a deployment failure or unexpected bug occurs during the hackathon judging window:
  - **DO NOT debug live** or push unverified hotfixes directly during the judging session.
  - Immediately perform a 1-click redeploy of the **last known-good commit from `main`** on Vercel and Render dashboards.
  - Verify that the previous stable production build is serving successfully.

---

## 5. Offline Fallback Deliverable (Phase 3 Requirement)

> [!IMPORTANT]
> **Mandatory Fallback Deliverable**: A pre-recorded video recording of the entire live product demo is a **REQUIRED Phase 3 deliverable**, not an optional extra.

- **Purpose**: Protects against unexpected venue Wi-Fi failure, network latency spikes, or cloud service outages during live judging.
- **Specification**: High-resolution screen capture stored locally on the presentation laptop demonstrating:
  1. Live itinerary editing and presence across two simulated user profiles.
  2. Mode NA 10-minute timer start on 1st `no` vote with typed reason.
  3. AI blended plan output and multi-way branch fork on the Route Line (Clay `#C1502E`).
  4. Unanimous Trip Chat proposal override.
  5. Deterministic Solo Matchmaker results for groups and tour guides.

---

## 7. Local Model Serving, Tunnel Security & Availability Risks

`[STACK_DEPENDENT_DECISION]`
- **Local Ollama Inference**: Runs locally on `http://localhost:11434` serving Phi-4 Mini (3.8B) and Qwen2.5-Coder.
- **Developer Tunnel Security**: If ngrok is utilized to expose Ollama across development laptops:
  - Must configure ngrok Basic Auth or HTTP header verification.
  - Must implement client-side timeout handling (15s ceiling) to detect laptop sleep or network interruption.
  - Tunnel usage is strictly restricted to development testing and is prohibited in production.

---

## 6. Unapproved Candidate Cloud Fallback (Pending Approval)

> [!NOTE]
> **Status: PENDING REVIEW (Not Approved for Production)**  
> The baseline architecture relies on candidate local SLM evaluation. Any cloud fallback provider (e.g. cloud-hosted inference API) and its corresponding credentials remain an unapproved open decision (Decision Register #15). It is strictly excluded from production deployment checklists and required environment configuration until explicitly evaluated and approved by the user.



---

## 3.1 Safe Alembic Schema Migration Procedure

To maintain schema integrity and protect live production data in Neon PostgreSQL, database migrations must adhere to this structured six-stage lifecycle:

1. **Creating a Migration**:
   - Run `alembic revision --autogenerate -m "descriptive_title"` from the `backend/` directory using an isolated development/test database.
   - Inspect the generated migration file in `backend/alembic/versions/` to verify every `op.create_table`, `op.add_column`, or index modification.
2. **Reviewing the Migration Script**:
   - Check that foreign key constraint actions match approved product rules (`ON DELETE NO ACTION` or explicit `CASCADE` where intended).
   - Verify that autogenerated scripts do not drop existing tables, rename columns unexpectedly, or violate existing non-null constraints.
3. **Testing Migration Upgrade & Downgrade**:
   - Test `alembic upgrade head` against an isolated staging/test database (e.g., `wandermatch_test_restore`).
   - Test `alembic downgrade -1` (or to baseline `c8a6a4789a32`) to confirm reverse operations function without error.
4. **Applying to Production Environment**:
   - Verify a restorable snapshot/backup exists prior to running production migrations.
   - Execute `alembic upgrade head` using direct (unpooled) Neon PostgreSQL connection credentials to prevent DDL startup parameter rejection.
5. **Recording Current Migration Revision**:
   - Execute `alembic current` and inspect `alembic_version` in the primary database to confirm the migration hash matches expected HEAD.
6. **Disaster Recovery & Failed Migration Policy**:
   - If a migration fails mid-execution, do NOT run `alembic stamp` casually.
   - Inspect `alembic_version` to identify the recorded revision, diagnose the failed DDL statement, rollback transactionally if possible, or restore from the pre-migration snapshot.

---

## 3.2 Production Media Storage Prerequisite & Ephemeral Disk Warning

> [!WARNING]
> **Ephemeral Filesystem on Render**:  
> In the current implementation, photos uploaded via `POST /api/photos/upload` are saved to local disk at `backend/static/uploads/`. Render web services operate on ephemeral container filesystems: all files written to local disk are permanently discarded upon container sleep, redeploy, or restart.  
> **Production Prerequisite**: Cloudinary credentials (`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`) or an S3-compatible object store must be provisioned and wired into `backend/app/routers/photos.py` before production launch.

---

## 3.3 WebSocket Horizontal Scaling & Redis Pub/Sub Prerequisite

> [!NOTE]
> **In-Process Connection Management**:  
> Real-time collaborative events (`voteCast`, `proposalCreated`, `branchConfirmed`, `slotStatusChanged`, `aiPlanGenerated`) are broadcast in-process via `ConnectionManager` (`backend/app/websocket_manager.py`).  
> This architecture operates reliably on a **single** Render web service instance.  
> If the backend is horizontally scaled across multiple Render instances, a Redis Pub/Sub message broker must be introduced to fan out WebSocket broadcasts across instances. Single-instance operation remains the baseline deployment topology.

---

## 3.4 Database Cleanup Policy — Prohibited During Audit

> [!CAUTION]
> **Database Cleanup Is On Hold (`[CLEANUP_ON_HOLD]`)**:  
> The 27,283 historical transactional records residing in 19 tables in Neon PostgreSQL are strictly preserved. Deletion, truncation, or cleanup scripts are prohibited during documentation audit and planning stages. Cleanup dry-run has been verified on a test database with 100% row preservation of the 261 reference rows; live execution requires explicit stakeholder authorization.

---

## 3.5 Deferred Navbar Navigation Performance Investigation

> [!NOTE]
> **User-Observed Navigation Latency (`[DEFERRED_FOLLOW_UP]`)**:  
> User-observed slow navigation between tabs/pages in the navbar is recorded as a deferred performance investigation item. No speculative optimizations, caching layers, or code changes are permitted during this phase. An empirical profiling investigation measuring route transitions, React rendering cycles, Clerk auth checks, and backend latency will be executed at the designated performance optimization phase.
