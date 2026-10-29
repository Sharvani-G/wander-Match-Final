# Deployment Architecture Documentation: Infrastructure & Physical Topology

**Product**: WanderMatch — Social & Group Travel Planning with an AI Consensus Planner  
**Hackathon**: KogniVera Hackathon 2026 (Problem Statement PS-11, Travel & Tourism Theme)  
**Team**: Chaosminds — Nikitha (Frontend); Panchami (HTTP/WebSocket Transport and DeepFace); Sharvani (Business Logic, AI/Consensus, Authentication, Database, Integration and Deployment)
**Specification Status**: Updated Draft — Complete Tech Stack Documentation Alignment  
**Deployment Model**: Decoupled Client-Server Cloud Topology (Candidate Hosting Infrastructure)  
**Canonical AI Specification Reference**: For model parameters, timeout configurations, and fallback degradation states, consult the canonical [AI System Specification](AI.md).

---

## 0. Infrastructure Verification Status & Boundary Rules

- **`[CURRENT — VERIFIED]`**: No Dockerfiles, Docker Compose files, GitHub Actions workflows, or cloud deployment configuration manifests currently exist in the repository tree.
- **`[CURRENT — VERIFIED]`**: Authoritative database is Neon Managed PostgreSQL (PostgreSQL 18.6 on AWS ap-southeast-1) stamped at Alembic revision `c8a6a4789a32`.
- **`[TARGET — PROPOSED]`**: Vercel (Frontend Edge CDN) and Render (Backend Orchestrator & DeepFace Worker) represent candidate hosting environments.
- **`[CURRENT — VERIFIED]`**: Real-time WebSockets run via in-process `ConnectionManager` on Render; Redis pub/sub broker is unconfigured and required for multi-instance horizontal scaling.
- **`[CURRENT — VERIFIED]`**: Photo uploads currently persist to local disk (`backend/static/uploads/`), which is ephemeral on Render. Cloudinary is declared in requirements but unconfigured in runtime environment.
- **`[APPROVED REQUIREMENT]`**: DeepFace is a **required separate processing service**, not an optional application component. However, individual traveler facial enrollment is optional, and biometric processing failures must never block normal trip planning, voting, or consensus operations.

---

## 1. Physical Deployment Topology & Network Segregation

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PUBLIC INTERNET / CLIENT BROWSERS                                                      │
└───────────────────────────┬───────────────────────────────────▲────────────────────────┘
                            │ HTTPS                             │ WSS / WebSockets
                            │                                   │ (camelCase events)
┌───────────────────────────▼───────────────────────────────────┴────────────────────────┐
│ CANDIDATE FRONTEND CDN (e.g., Vercel Edge Network) [PENDING]                           │
│ • Static Assets & React 19.2.8 HTML5/JS Application Bundle                             │
│ • Edge CDN Caching & Global DNS Routing                                                │
└───────────────────────────┬────────────────────────────────────────────────────────────┘
                            │ HTTPS REST & WSS WebSockets
                            │
┌───────────────────────────▼────────────────────────────────────────────────────────────┐
│ CANDIDATE CLOUD BACKEND HOSTING (e.g., Render Web Services) [PENDING]                  │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ Service 1: Consolidated FastAPI Core Orchestrator (Python 3.12+ / Uvicorn)        │ │
│ │ • Public HTTPS REST endpoints & WebSocket Hub (/ws/trips/{trp_id})                 │ │
│ └───────┬───────────────────────────────┬───────────────────────────────┬────────────┘ │
│         │                               │                               │              │
│         │ Internal Process / HTTP Call  │ HTTPS                         │ HTTPS        │
│ ┌───────▼─────────────────────────────┐ │                               │              │
│ │ Service 2: DeepFace Photo Service   │ │                               │              │
│ │ (REQUIRED PROCESSING SERVICE)       │ │                               │              │
│ │ • Isolated heavy ML dependencies    │ │                               │              │
│ │ • Async Trip-Scoped Face Tagging    │ │                               │              │
│ │ • Non-blocking failure mode         │ │                               │              │
│ └─────────────────────────────────────┘ │                               │              │
└─────────┬───────────────────────────────┼───────────────────────────────┼──────────────┘
          │                               │                               │
          │ Internal TLS Connection       │ Outbound HTTPS                │ Outbound HTTPS
┌─────────▼─────────────────────────────┐ │                               │
│ CANDIDATE MANAGED POSTGRESQL (Neon)   │ │                               │
│ • Single Authoritative System of      │ │                               │
│   Record Database [DECISION PENDING]  │ │                               │
│ • PS-11 Tables + Additive Tables      │ │                               │
└───────────────────────────────────────┘ │                               │
                                ┌─────────▼─────────────────────┐ ┌───────▼──────────────┐
                                │ CANDIDATE INFERENCE ENDPOINT  │ │ CLOUDINARY MEDIA CDN │
                                │ (Provider Undecided [PENDING])│ │ [DECISION PENDING]   │
                                │ • Blended Plan Generation     │ │ • Photo Storage      │
                                │ • Multi-Way Branch Classifier │ │ • Image Delivery CDN │
                                └───────────────────────────────┘ └──────────────────────┘
```

> **Strict Proxy Rule**: React client applications running in the browser connect **only** to the frontend CDN and the FastAPI orchestrator public endpoints. Clients **never** establish direct connections to PostgreSQL, Cloudinary, Clerk Webhooks, candidate routing engines, or candidate inference endpoints. Production LLM provider and inference hosting topology remain open decisions pending stack verification.

---

## 2. Network Boundaries & Security Isolation

- **Publicly Reachable Surface**:
  - **Candidate Static CDN**: Serves the built React 19 HTML/JS/CSS bundle over public HTTPS.
  - **FastAPI Public Endpoint**: Exposes public REST endpoints and WebSocket channels over TLS.
- **Internal / Protected Infrastructure Boundary**:
  - **Authoritative PostgreSQL Database**: Protected by strong authentication and SSL connection encryption (`sslmode=require`). The database instance accepts connections **exclusively** via backend connection string credentials; it is NEVER exposed directly to public client browsers. Neon is a candidate managed PostgreSQL provider [DECISION PENDING].
  - **DeepFace Service Isolation**: Runs on an internal port (Port 8001) or internal network without public route exposure. All image processing requests originate from the core FastAPI orchestrator.
  - **Candidate Inference Service & Cloudinary**: In development, Ollama runs locally serving Phi-4 Mini (3.8B) or Qwen2.5. Production inference hosting topology and cloud fallback remain an unapproved open decision [DECISION PENDING]. Cloudinary is accessed via server-side credentials (`CLOUDINARY_API_SECRET`).
  - **Candidate OSRM Routing Engine**: Self-hosted OSRM Docker container running on internal private network for sub-15ms road route calculation without external internet dependencies or rate limits.

---

## 3. Scaling Topology Notes (Documented Future Scope)

> [!NOTE]
> **Future Multi-Instance Scaling Architecture**: For post-hackathon production scaling across multiple backend application instances, the in-memory WebSocket connection manager is designed to be upgraded to a **Redis-backed Pub/Sub Connection Manager**.

This Redis message broker layer will handle cross-instance WebSocket event fan-out, ensuring `voteCast`, `slotStatusChanged`, and `proposalCreated` events propagate seamlessly regardless of which instance holds a specific client's WebSocket connection. Redis is strictly an event distribution broker, **never** an authoritative application database.

---

## 4. Checkpoint 2 Deployment Definition of Done

> [!IMPORTANT]
> **Checkpoint 2 Deployment Requirement**: Deployment is considered "DONE" **only** when the complete user flow—trip creation, real-time binary voting, Mode A / Mode NA AI consensus reconciliation, multi-way branch split rendering on the Route Line, unanimous chat overrides, and deterministic solo matching—is fully reachable and verified working end-to-end against the **live deployed production URLs**, not merely running on `localhost`.


---

## 2.3 Production Data Durability & Operational Policies

1. **Authoritative Relational State**: Stored exclusively in Neon PostgreSQL. SQLite files and process-local dictionaries are non-authoritative.
2. **Safe Migration Protocol**: All schema evolution follows the 6-stage Alembic lifecycle defined in `docs/DEPLOYMENT.md#3.1`. Direct production DDL or unverified `alembic stamp` operations are prohibited.
3. **Database Cleanup Policy (`[CLEANUP_ON_HOLD]`)**: The 27,283 historical transactional records across 19 tables are strictly preserved. Cleanup is deferred until all shared and member-specific planning is approved.
4. **Deferred Navbar Performance Investigation (`[DEFERRED_FOLLOW_UP]`)**: Navbar tab-switching latency is a known user-observed issue deferred for empirical profiling; no speculative caching or premature optimizations.
