# NIKITHA.md — Frontend Track Owner

**Track Owner**: Nikitha M N  
**Specification Status**: Authoritative Specification (`[SYSTEM OF RECORD]`)  
**Shared Integration Contract**: [`docs/INTEGRATION_CONTRACT.md`](INTEGRATION_CONTRACT.md)  
**Authoritative Decision Register**: [`docs/AI.md §12`](AI.md#12-stack-neutral-decision-register)  
**Governance Rule**: Following initial preparation, **Nikitha solely edits this document**. Cross-boundary contract updates are managed by Sharvani in `docs/INTEGRATION_CONTRACT.md`.

## WanderMatch · KogniVera Hackathon 2026 · PS-11

---

## HOW TO USE THIS DOC (Read this first, give it to your agent verbatim)

> "I am Nikitha M N, Frontend developer for WanderMatch at KogniVera Hackathon 2026. Read this entire document carefully. It contains my full project context, my exact responsibilities, the complete naming contract, every screen I must build, every API I must call, every component I must create, and my phase-by-phase execution plan. After reading, give me a detailed prompt to execute Phase [X] of my work. Do not assume anything not written here. Do not invent field names, endpoint paths, or component behavior. Everything is specified."

---

## Phase-based reading guide

This is a structure-only reorganization. All original specifications, examples, ownership rules, pending decisions and execution checklists are retained below.

Use the phases as a reading and working sequence. Existing numbered section titles remain intact for cross-document references. The original hour-based plan is retained in Phase 6; it is not a new delivery estimate. Work can proceed in parallel using the documented mocks and agreed interfaces. Pending decisions and implementation prerequisites remain pending.

- [Phase 1 — Understand the project, ownership and working boundaries](#member-phase-1)
- [Phase 2 — Prepare the frontend foundation and shared contracts](#member-phase-2)
- [Phase 3 — Connect APIs and real-time events](#member-phase-3)
- [Phase 4 — Build components and feature screens](#member-phase-4)
- [Phase 5 — Verify usability, accessibility and performance](#member-phase-5)
- [Phase 6 — Follow the execution checklist and integration checkpoints](#member-phase-6)


<a id="member-phase-1"></a>
## Phase 1 — Understand the project, ownership and working boundaries

Read the retained sections below together for this phase:

- 0. OWNERSHIP LEDGER & LIFECYCLE DISTINCTION
- 1. WHAT WANDERMATCH IS — FULL CONTEXT
- 2. TECH STACK — EXACTLY WHAT YOU USE
- 5. DIRECTORY STRUCTURE — WHAT YOU OWN
- 15. DEPENDENCY MAP — WHAT YOU NEED FROM OTHERS AND WHEN
- 16. WHAT YOU MUST NEVER DO

## 0. OWNERSHIP LEDGER & LIFECYCLE DISTINCTION

This section establishes Nikitha's unambiguous ownership boundary, future structural plans, and lifecycle progression in accordance with `docs/INTEGRATION_CONTRACT.md`.

### A. Current Owned Files
Nikitha solely owns all files within `frontend/`:
- **Configuration & Setup** (8 files):
  - `frontend/package.json`, `frontend/package-lock.json`
  - `frontend/vite.config.ts`, `frontend/tailwind.config.ts`
  - `frontend/tsconfig.json`, `frontend/tsconfig.app.json`, `frontend/tsconfig.node.json`
  - `frontend/.oxlintrc.json`
- **Application Shell & Assets** (8 files verified on disk):
  - `frontend/index.html`
  - `frontend/public/favicon.svg`, `frontend/public/icons.svg`
  - `frontend/src/assets/hero.png`, `frontend/src/assets/react.svg`, `frontend/src/assets/vite.svg` (Note: `logo.svg` does not exist; active asset is `vite.svg`)
  - `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/App.css`, `frontend/src/index.css`
  - `frontend/.env.example`
- **Component Primitives & Composites** (24 source files verified on disk):
  - `frontend/src/components/chat/` (3 files): `ChatDrawer.tsx`, `ChatMessage.tsx`, `ChatProposeButton.tsx`
  - `frontend/src/components/face/` (2 files): `FaceCapture.tsx`, `FaceRegistration.tsx`
  - `frontend/src/components/itinerary/` (5 files): `BranchTabs.tsx`, `ConflictResolutionPanel.tsx`, `ProposalCard.tsx`, `RouteLine.tsx`, `SlotCard.tsx`
  - `frontend/src/components/layout/` (4 files): `GlobalTopHeader.tsx`, `PageWrapper.tsx`, `SidebarNav.tsx`, `TopNav.tsx`
  - `frontend/src/components/solo/` (2 files): `CompatibilityCard.tsx`, `GuideCard.tsx`
  - `frontend/src/components/ui/` (8 files): `Button.tsx`, `EmptyState.tsx`, `Input.tsx`, `Modal.tsx`, `StatusPill.tsx`, `SuggestionChip.tsx`, `Toast.tsx`, `VotePill.tsx`
- **Screens & Modals** (19 source files verified on disk):
  - `frontend/src/screens/` (19 files): `AccountScreen.tsx`, `AuditHistoryScreen.tsx`, `BranchViewScreen.tsx`, `ConflictResolutionPanel.tsx`, `CreateTripScreen.tsx`, `LoginScreen.tsx`, `MemoriesScreen.tsx`, `MyTripsScreen.tsx`, `OnboardingScreen.tsx`, `PhotosScreen.tsx`, `ProposeActivityModal.tsx`, `ResolvedItineraryScreen.tsx`, `SignUpScreen.tsx`, `SoloMatchScreen.tsx`, `SoloOrGroupDecisionScreen.tsx`, `TripChatScreen.tsx`, `TripHomeScreen.tsx`, `TripPreviewScreen.tsx`, `VoteModal.tsx`
- **Custom Hooks** (4 files verified on disk):
  - `frontend/src/hooks/useProposals.ts`, `frontend/src/hooks/useSoloMatch.ts`, `frontend/src/hooks/useTrip.ts`, `frontend/src/hooks/useVotes.ts`
- **Context & State** (2 files verified on disk):
  - `frontend/src/context/AuthContext.tsx`, `frontend/src/context/TripContext.tsx`
- **Shared Type Definitions** (6 files verified on disk):
  - `frontend/src/types/branch.ts`, `frontend/src/types/proposal.ts`, `frontend/src/types/solo.ts`, `frontend/src/types/trip.ts`, `frontend/src/types/user.ts`, `frontend/src/types/vote.ts`
- **Utilities & HTTP/WS Lib** (2 files verified on disk):
  - `frontend/src/lib/api.ts`, `frontend/src/lib/websocket.ts`

### B. Proposed Future Files (Pending Implementation Approval)
When frontend data-access decoupling is approved, Nikitha will introduce a clean abstraction layer:
- `frontend/src/lib/data-access/client.ts` — Interface contract defining all data operations (`getTrip`, `castVote`, `submitProposal`, `fetchPhotos`, `subscribeToTripEvents`, etc.).
- `frontend/src/lib/data-access/real_adapter.ts` — Concrete production adapter executing native `fetch()` calls to Panchami's FastAPI backend (`http://localhost:8000/api`) and native `WebSocket` connections.
- `frontend/src/lib/data-access/mock_adapter.ts` — Deterministic in-memory adapter serving scenario fixtures with simulated async delay (50–150ms).
- `frontend/src/lib/data-access/fixtures/*.ts` — Static scenario datasets (Solo matches, Kyoto Mode NA trip with active dissent timer, branched slots, chat history, auto-tagged photo metadata).

### C. Necessary Extraction Tasks (Preparation Phase)
1. **Decouple Component Data Fetching**: Replace ad-hoc `fetch()` calls inside screens and hooks with calls to the unified `dataAccessClient` interface.
2. **Enforce Non-Circular Import Direction**:
   - `Screens / Components / Hooks` ➔ `data-access/client.ts` ➔ `real_adapter.ts` or `mock_adapter.ts` ➔ `types/*.ts`.
   - Adapters and fixtures import strictly from `types/*.ts`. Adapters **NEVER** import components, hooks, or context.
   - This eliminates circular dependency hazards and guarantees that the UI can be run and tested in complete isolation.

### D. Later Feature Implementation (Feature Phase — Not Yet Approved)
- **WebSocket Auth Query Parameter**: Append JWT token to the connection URL: `ws://.../ws/trips/{trip_id}?token=${jwtToken}`.
- **WebSocket Reconnection & Backoff**: Exponential backoff reconnect logic with state recovery on reconnect.
- **Itinerary PDF Export (Required Online Export & Preview UI)**: PDF export is **REQUIRED and ONLINE** (`FR-EXP-01`). Offline PDF generation/export is **DEFERRED** and is NOT an acceptance gate (older audit text requesting offline PDF export is superseded by this human clarification). Nikitha owns the Export Preview Modal (`ExportPreviewModal.tsx`), responsive printable DOM layout, print stylesheet (`@media print`), loading/error states, and client download lifecycle against the agreed online endpoint. Optional fixture-backed preview using `mock_adapter.ts` with fixture `export_itinerary_pdf_preview.json` remains available as development support for offline UI iteration, but working offline export is NOT a completion gate. Rendering engine strategy selection (`@react-pdf/renderer` client-side vs backend `weasyprint`) remains **PENDING** under Decision #30.
- **Trip Chat Alignment**: Align `frontend/src/lib/api.ts` to call backend canonical routes `GET /api/trips/{trip_id}/chat` and `POST /api/trips/{trip_id}/chat` (replacing `/api/trips/{trpId}/messages` and `/api/messages`).
- **Full WCAG 2.1 AA Compliance**: Keyboard navigation rings (`focus-visible:ring-2 focus-visible:ring-route`), `aria-invalid="true"` binding on all form fields, and screen reader announcements (`aria-live="polite"`) for consensus timer countdowns (Decision #31) and toast notifications.
- **Responsive Layout Hardening**: Polish viewports across mobile (375px), tablet (768px), and desktop (1280px).

### E. Mock-Only Completion Criteria
Nikitha can declare complete frontend mock readiness when:
1. `npm run dev` boots cleanly with `VITE_USE_MOCK_DATA=true`.
2. All 19 screens and all 24 components render without runtime JavaScript exceptions.
3. User can click through the entire user journey offline:
   - Browse trips, view live itinerary Route Line with colored slot statuses.
   - Cast a NO vote with mandatory reason, triggering the 10-minute countdown simulation.
   - View AI compromise panel and branch views with member splits.
   - Open Trip Chat drawer, send message, and click "Propose this as the plan".
   - View Solo Match compatibility scores (0–100% formatted in monospace font).
   - View photo gallery with face bounding boxes and "My Photos" face-registration gate.
4. No network requests are made to `localhost:8000` or external servers in mock mode.

### F. Real Integrated Completion Criteria
Full integrated completion is achieved when:
1. `VITE_USE_MOCK_DATA=false` connects to Panchami's running FastAPI service (`http://localhost:8000/api`) and WebSocket (`ws://localhost:8000/ws/trips/{trip_id}?token=...`).
2. Real Clerk JWT authentication tokens are attached to HTTP `Authorization: Bearer <token>` and WebSocket connection queries.
3. Live WebSocket broadcast messages (`resyncSnapshot`, `voteCast`, `slotStatusChanged`, `branchConfirmed`, `aiRecommendationReady` [current] / `aiPlanGenerated` [proposed], `newChatMessage`) update the UI reactively without page reloads.
4. Photo upload (`POST /api/photos`) displays uploaded images and rendered face tags returned by Panchami's orchestration of Sharvani's persistence and the DeepFace worker.

---

## 1. WHAT WANDERMATCH IS — FULL CONTEXT

WanderMatch is a social group travel planning web app. It solves a real problem: when a group of friends plan a trip together, disagreements get either steamrolled or lost in chat. WanderMatch gives every group member a structured way to propose activities, vote on them, and have their objections heard — while an AI layer reads the typed reasons behind objections and generates compromise plans or, when preferences are truly incompatible, parallel branches.

### The core user flow:
1. A trip owner creates a group trip with destination, dates, mode (Mode A or Mode NA)
2. Members join the trip and see a shared live itinerary (the "Route Line")
3. Members propose activities for time slots (Morning/Afternoon/Evening/Night)
4. Members vote YES or NO on proposals — NO votes REQUIRE a typed reason/suggestion
5. The AI reads typed NO reasons and generates ONE blended compromise plan
6. If compromise fails after ~3 rounds, the group splits into parallel branches (one per distinct preference)
7. Single-member branches auto-resolve; multi-member branches re-run the full consensus flow recursively
8. Trip Chat (always-on) allows unanimous override of the AI at any point
9. Solo travelers can find compatible group trips or tour guides via deterministic scoring

### Two trip modes:
- **Mode A (Admin-Led)**: Trip owner has final authority. AI recommends, admin decides. Round cap is advisory. Admin can extend rounds, force branches, or accept proposals directly at any time.
- **Mode NA (Collaborative)**: Fully automatic. First NO vote starts a response timer (`[IMPLEMENTATION BEHAVIOR — DECISION PENDING: Product Sign-Off Required]`, currently 10 minutes in code per Decision #31). After ~3 rounds unresolved, AI auto-branches. No admin override — purely democratic.

### Actor rules (CRITICAL for UI gating — implement exactly this):

| Actor | Sees | Can Do | Cannot Do |
|---|---|---|---|
| All trip members (any mode) | Full itinerary + every slot's status; every proposal ever submitted with live vote tallies; every NO-reason attributed to the voter; complete revision history per slot; all branches and their assigned members/plans (even branches they're not part of); Trip Chat | Vote YES on one proposal per slot; vote NO with typed reason on any proposal; submit new proposals; respond to a branch preview if they're a branch member | See another member's private face-registration data; edit or retract someone else's vote; force a slot to confirm without going through vote/window rules |
| Admin (Mode A only) | Everything above PLUS the AI recommendation panel with explicit controls once AI is invoked | Build/edit the base itinerary; invoke AI consensus; approve, reject, or override any AI recommendation; force branching early; extend rounds past the soft cap; accept a proposal directly at any time | N/A — there is one admin per trip in this mode |
| AI system | Current round's active proposals, full vote distribution, every stated reason (current and prior rounds within the current consensus cycle), and hard-constraint data (location, timing, transport feasibility) | Generate exactly one common-ground candidate per round; classify a NO-reason as fixable vs. genuinely incompatible; group holdouts into branches by stored preference; validate its own generated plan against hard constraints before it is shown to anyone | Invent a plan that violates a hard constraint; make a binding decision in Mode A (it only recommends there); resume common-ground attempts on a slot after it has already switched that slot to branching, within the same cycle |
| Non-voter / silent member (either mode) | Identical visibility to any other member — nothing is hidden from members just because they haven't voted | Vote or object at any later point, in any future round, on any slot | Be treated as a blocker to the group's progress; be counted as a YES vote (silence is never YES). Note: When parallel branching occurs, silent members default to Track A per canonical rule (docs/AI.md:196) |

---

## 2. TECH STACK — EXACTLY WHAT YOU USE

- **Framework**: React 19 (React 19.2.8 in package.json)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS (utility classes only — no custom CSS files unless absolutely necessary)
- **Build tool**: Vite
- **Auth SDK**: Clerk React SDK (`@clerk/clerk-react`) — for `<ClerkProvider>`, `useUser()`, `useAuth()`, sign-in/sign-up components
- **State**: React Context + `useState`/`useReducer` — no Redux, no Zustand unless you add it yourself
- **WebSocket**: Native browser `WebSocket` API, managed inside a `TripContext`
- **HTTP**: Native `fetch` API with `async/await` — no axios
- **Deployment Coordination**: Owned by Sharvani (Vercel static build from Vite for frontend, Render for backend and worker). Nikitha provides build artifacts and client environment variables.

You DO NOT touch:
- PostgreSQL directly (ever)
- FastAPI code (ever)
- `/backend/` directory (ever)
- `/infra/` directory (ever)
- `/backend/ai/` directory (ever)

---

## 5. DIRECTORY STRUCTURE — WHAT YOU OWN

```
frontend/
  package.json
  package-lock.json
  vite.config.ts
  tailwind.config.ts
  tsconfig.json
  tsconfig.app.json
  tsconfig.node.json
  .oxlintrc.json
  index.html
  .env.example
  public/
    favicon.svg
    icons.svg
  src/
    assets/
      hero.png
      react.svg
      vite.svg
    components/               ← YOU OWN ALL 24 COMPONENT FILES VERIFIED ON DISK
      chat/
        ChatDrawer.tsx
        ChatMessage.tsx
        ChatProposeButton.tsx
      face/
        FaceCapture.tsx
        FaceRegistration.tsx
      itinerary/
        BranchTabs.tsx
        ConflictResolutionPanel.tsx
        ProposalCard.tsx
        RouteLine.tsx
        SlotCard.tsx
      layout/
        GlobalTopHeader.tsx
        PageWrapper.tsx
        SidebarNav.tsx
        TopNav.tsx
      solo/
        CompatibilityCard.tsx
        GuideCard.tsx
      ui/
        Button.tsx
        EmptyState.tsx
        Input.tsx
        Modal.tsx
        StatusPill.tsx
        SuggestionChip.tsx
        Toast.tsx
        VotePill.tsx
    screens/                  ← YOU OWN ALL 19 SCREEN COMPONENTS VERIFIED ON DISK
      AccountScreen.tsx
      AuditHistoryScreen.tsx
      BranchViewScreen.tsx
      ConflictResolutionPanel.tsx
      CreateTripScreen.tsx
      LoginScreen.tsx
      MemoriesScreen.tsx
      MyTripsScreen.tsx
      OnboardingScreen.tsx
      PhotosScreen.tsx
      ProposeActivityModal.tsx
      ResolvedItineraryScreen.tsx
      SignUpScreen.tsx
      SoloMatchScreen.tsx
      SoloOrGroupDecisionScreen.tsx
      TripChatScreen.tsx
      TripHomeScreen.tsx
      TripPreviewScreen.tsx
      VoteModal.tsx
    context/                  ← YOU OWN BOTH CONTEXTS VERIFIED ON DISK
      AuthContext.tsx
      TripContext.tsx
    hooks/                    ← YOU OWN ALL 4 HOOKS VERIFIED ON DISK
      useProposals.ts
      useSoloMatch.ts
      useTrip.ts
      useVotes.ts
    types/                    ← YOU OWN ALL 6 TYPE FILES VERIFIED ON DISK
      branch.ts
      proposal.ts
      solo.ts
      trip.ts
      user.ts
      vote.ts
    lib/                      ← YOU OWN ALL 2 LIB FILES VERIFIED ON DISK
      api.ts                  ← All fetch calls to FastAPI (align to canonical routes)
      websocket.ts            ← WebSocket connection manager
      data-access/            ← PROPOSED FUTURE EXTRACTION
        client.ts             ← Abstract data access interface & factory
        real_adapter.ts       ← Live FastAPI HTTP/WS implementation
        mock_adapter.ts       ← Deterministic client-side mock implementation
        fixtures/             ← Static scenario fixtures with fixed clock
    App.tsx
    main.tsx
    App.css
    index.css
```

You NEVER touch anything outside `frontend/`. Sharvani manages backend models, migrations, and services. Panchami manages FastAPI endpoints and DeepFace.

---

## 15. DEPENDENCY MAP — WHAT YOU NEED FROM OTHERS AND WHEN

| What you need | From whom | When you need it |
|---|---|---|
| `VITE_API_BASE_URL` value | Sharvani / Panchami | Baseline setup |
| `VITE_WS_BASE_URL` value | Sharvani / Panchami | Baseline setup |
| `VITE_CLERK_PUBLISHABLE_KEY` value | Sharvani | Baseline setup |
| `GET /api/trips` working | Panchami | Checkpoint 1 |
| `POST /api/votes` working | Panchami | Checkpoint 1 |
| WebSocket broadcasting `voteCast` | Panchami | Checkpoint 1 |
| `POST /api/consensus/reconcile` working | Panchami + Sharvani | Phase 4 |
| `GET /api/branches/:itmId` working | Panchami | Phase 4 |
| `POST /api/solo-matching/groups` working | Panchami + Sharvani | Phase 5 |
| `GET /api/trips/:tripId/chat` working | Panchami | Phase 4 |
| Photo upload endpoint (`POST /api/photos`) | Panchami (calls Sharvani persistence) | Phase 5 |

---

## 16. WHAT YOU MUST NEVER DO

1. Never call PostgreSQL directly from the frontend
2. Never call the LLM API directly from the frontend
3. Never use `float` or `Number()` for money — keep money as string
4. Never parse or split an ID string (e.g. never do `id.split('_')[1]`)
5. Never use `abstain` as a vote value — WanderMatch only writes `yes` or `no`
6. Never use field name `description` for proposal text — it is `rationale`
7. Never use field name `estimatedCost` — it is `costDelta`
8. Never show admin controls to non-owner users
9. Never gate "All Photos" behind face registration — only "My Photos" is gated
10. Never block a non-voter from voting in future rounds
11. Never use color as the sole status signal — always pair with icon + text label
12. Never emit server broadcast events over WebSocket. The frontend is strictly a listener/receiver subscribing to the central 16-event catalog (`resyncSnapshot`, `voteCast`, `voteRetracted`, `proposalCreated`, `slotTimerStarted`, `slotTimerUpdated`, `slotStatusChanged`, `consensusReconciling`, `aiPlanGenerated`, `aiRecommendationReady`, `consensus.clarification_requested`, `clarificationSubmitted`, `negotiationCardRendered`, `branchConfirmed`, `newChatMessage`, `itineraryUpdated`). State re-synchronization is initiated via authenticated HTTP `GET /api/trips/{trpId}`, never by dispatching `resyncSnapshot`.


---


<a id="member-phase-2"></a>
## Phase 2 — Prepare the frontend foundation and shared contracts

Read the retained sections below together for this phase:

- 3. LOCKED VISUAL SYSTEM — IMPLEMENT EXACTLY, NO DEVIATIONS
- 4. NAMING CONTRACT — READ BEFORE WRITING ANY CODE
- 6. TAILWIND CONFIG — SET THIS UP FIRST
- 7. TYPESCRIPT TYPES — DEFINE THESE BEFORE ANY COMPONENT

## 3. LOCKED VISUAL SYSTEM — IMPLEMENT EXACTLY, NO DEVIATIONS

### 3.1 Color Palette (use these exact hex values everywhere)
```
Paper     #F7F5F0   → Canvas & main background (warm tactile paper tone)
Ink       #14213D   → Primary headings & high-contrast text
Route     #2F6F6B   → Brand color, primary buttons, active states, In-Consensus
Route Dark #204B48  → Button hover & pressed states
Amber     #E1A93A   → CONFIRMED state ONLY (warm gold transit line)
Clay      #C1502E   → BRANCHED/conflict state ONLY (terracotta, never decorative)
Slate     #6B7280   → Secondary text, labels, subtitles, EMPTY state
Slate Light #E4E1DA → Borders, dividers, card outlines
Card      #FFFFFF   → Surface backgrounds (clean white paper cards)
```

### 3.2 Typography
```
Headings & Trip Titles  → font: 'Fraunces' (editorial serif)
UI Labels & Body Text   → font: 'Inter' (clean sans-serif)
Data/Times/Counts/%     → font: 'IBM Plex Mono' (structured transit font)
```
Load all three from Google Fonts in `index.html`.

### 3.3 Geometry
```
Cards & Buttons    → border-radius: 10px  (Tailwind: rounded-[10px])
Input Fields       → border-radius: 8px   (Tailwind: rounded-[8px])
Shadows            → box-shadow: 0 1px 3px rgba(20, 33, 61, 0.04) — NO heavy shadows, NO glass blur
```

### 3.4 The Signature Route Line (CRITICAL VISUAL ELEMENT)
The Route Line is a vertical dashed sequence line connecting itinerary time slots. It is the visual centerpiece of Trip Home, Trip Preview, and Resolved Itinerary screens.

```
Default/Pending slot    → dashed, Slate Light #E4E1DA
CONFIRMED slot          → solid, Amber #E1A93A
BRANCHED slot           → forks into parallel lines, Clay #C1502E
IN_CONSENSUS slot       → dashed, Route #2F6F6B
```

### 3.5 Slot Status → Color mapping (1:1, never deviate)
```
EMPTY        → Slate  #6B7280
IN_CONSENSUS → Route  #2F6F6B
BRANCHED     → Clay   #C1502E
CONFIRMED    → Amber  #E1A93A
```

These four statuses come from the backend `itinerary_items` + WanderMatch's slot_status extension. Display the status pill, the Route Line segment color, and status icons all using this exact mapping.

---

## 4. NAMING CONTRACT — READ BEFORE WRITING ANY CODE

This is the most important section for preventing integration bugs.

### 4.1 What comes FROM the backend (API responses)
All FastAPI responses are `camelCase`. Your TypeScript types must match exactly:

```typescript
// From PS-11 provided tables (these field names come from the DB but are camelCased in API)
trpId          // trips.trip_id
itmId          // itinerary_items.item_id
prpId          // proposals.proposal_id
votId          // votes.vote_id
usrId          // users.user_id
itnId          // itineraries.itinerary_id
tmbId          // trip_members.member_id
gidId          // tour_guides.guide_id

// Field names (camelCase versions of snake_case DB fields)
ownerId        // trips.owner_user_id
destinationCityId  // trips.destination_city_id
startDate      // trips.start_date
endDate        // trips.end_date
isGroupTrip    // trips.is_group_trip
costDelta      // proposals.cost_delta
closesAt       // proposals.closes_at
proposedByUserId // proposals.proposed_by_user_id
entityType     // proposals.entity_type / itinerary_items.entity_type
entityId       // proposals.entity_id / itinerary_items.entity_id
dayIndex       // itinerary_items.day_index
sortOrder      // itinerary_items.sort_order
startsAt       // itinerary_items.starts_at
endsAt         // itinerary_items.ends_at
preferredLanguages // user_preferences.preferred_languages
```

### 4.2 WanderMatch additive fields (also camelCase in API)
```typescript
slotStatus     // WanderMatch's 4-value slot status (EMPTY/IN_CONSENSUS/BRANCHED/CONFIRMED)
currentRound   // which round of consensus we're in
brcId          // branches.brc_id
bmcId          // branch_members.bmb_id
msgId          // trip_chat_messages.msg_id
fcpId          // face_profiles.fcp_id
phoId          // photos.pho_id
compatibilityScore  // solo matchmaker output (0-100 integer)
```

### 4.3 Money — NEVER use a JavaScript number for money
```typescript
// Money comes from the API as a STRING. Keep it as string for display.
// Use a decimal library (decimal.js) only if you need arithmetic for display purposes.
// Example: cost_delta comes as "15.00" not 15.00
cost: string        // e.g. "65.00"
costDelta: string   // e.g. "15.00" or "-5.00"
currency: string    // ISO-4217 e.g. "USD" "INR" "EUR"
```

### 4.4 Authoritative WebSocket Event Catalog & Server-to-Client Contract
```
// Complete Authoritative Event Catalog (Server Broadcast -> Client Listener):
resyncSnapshot                  // Sent by backend to connecting client upon initial WS connection & reconnect with full trip snapshot
voteCast                        // Broadcast when a member casts a vote (YES or NO with reason)
proposalCreated                 // Broadcast when a new proposal is created for a slot
branchConfirmed                 // Broadcast when a member confirms their branch assignment
slotStatusChanged               // Broadcast when a slot transitions (EMPTY, IN_CONSENSUS, BRANCHED, CONFIRMED, MANUAL_RESOLUTION_REQUIRED)
aiPlanGenerated                 // AI compromise plan published (aliased with aiRecommendationReady)
aiRecommendationReady           // Backend native event name for AI compromise plan
newChatMessage                  // New message posted to trip chat
consensus.clarification_requested // AI requests clarification on ambiguous objection; frontend renders clarification chips
itineraryUpdated                // Slot updated or itinerary version incremented
slotTimerStarted                // 10-minute countdown timer started by first NO vote
slotTimerUpdated                // Mode A admin extended timer
voteRetracted                   // Traveler retracted vote
negotiationCardRendered         // 3-option schedule negotiation card rendered on persistent constraint failure
```

> [!IMPORTANT]
> **Client vs Server Protocol Boundaries**:
> 1. **Client Never Emits Server Events**: The frontend is strictly a **receiver/listener** of WebSocket broadcast events. The frontend NEVER emits server events (such as `resyncSnapshot`, `slotStatusChanged`, or `aiPlanGenerated`) over the WebSocket connection.
> 2. **Client Snapshot Refresh**: To recover from network disconnection or missing packets, the client does NOT emit a WebSocket resync event; instead, `TripContext` issues an authenticated HTTP `GET /api/trips/{trpId}` request to fetch the authoritative database state.
> 3. **At-Most-Once Network Recovery**: Network deliveries over WebSockets are at-most-once. In the event of dropped packets, the authoritative state is reconciled via optimistic concurrency (`itinerary.version`) checks and HTTP state re-fetching.

### 4.4.1 Deterministic UI Verification Badge Mapping
Nikitha renders 6 distinct verification badges across proposal and slot cards based on deterministic feasibility attributes:

| Badge Label | Color / Token | Condition & Provenance | User Guidance / Tooltip |
| :--- | :--- | :--- | :--- |
| **`VERIFIED`** | Green (`text-forest bg-forest/10`) | All 4 dimensions verified: POI coords verified, road route found, schedule feasible, venue/road confirmed OPEN_REPORTED. | "All details verified against catalog and live road network." |
| **`PARTIALLY_VERIFIED`** | Amber (`text-amber bg-amber/10`) | Coords verified, road route found, schedule feasible, but closure or operating hours unverified. | "Schedule verified; operating hours or road closure unconfirmed." |
| **`UNVERIFIED`** | Slate (`text-slate bg-slate/10`) | Routing service unavailable (HTTP 503) or missing road network data. (NO Haversine!). | "External road routing unavailable. Travel time unverified." |
| **`NEEDS_CLARIFICATION`** | Clay (`text-clay bg-clay/10`) | Classifier returned ambiguous objection or multiple candidate matches. | "Clarification required from traveler to proceed." |
| **`INFEASIBLE`** | Red (`text-terracotta bg-terracotta/10`) | Provably exceeds slot duration window or onward commitments. | "Schedule conflict: transit plus activity exceeds available time window." |
| **`BLOCKED`** | Terracotta (`text-terracotta bg-terracotta/20`) | Road confirmed closed or venue operating hours shut. | "Road confirmed closed or venue closed on scheduled date." |

### 4.5 Enums you display (exact values from enums.json)
```typescript
// Slot status (WanderMatch additive — these are NOT in enums.json but are canonical)
type SlotStatus = 'EMPTY' | 'IN_CONSENSUS' | 'BRANCHED' | 'CONFIRMED'

// Vote value (from enums.json — WanderMatch only writes yes/no, never abstain)
type VoteValue = 'yes' | 'no'

// Member role (from enums.json)
type MemberRole = 'owner' | 'editor' | 'viewer'

// Trip mode (WanderMatch additive)
type TripMode = 'Mode A' | 'Mode NA'

// Proposal status (from enums.json)
type ProposalStatus = 'open' | 'accepted' | 'rejected' | 'expired'

// Branch status (WanderMatch additive)
type BranchStatus = 'OPEN' | 'FINALIZED'
```

---

## 6. TAILWIND CONFIG — SET THIS UP FIRST

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#F7F5F0',
        ink: '#14213D',
        route: '#2F6F6B',
        'route-dark': '#204B48',
        amber: '#E1A93A',
        clay: '#C1502E',
        slate: '#6B7280',
        'slate-light': '#E4E1DA',
        card: '#FFFFFF',
      },
      fontFamily: {
        serif: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
} satisfies Config
```

---

## 7. TYPESCRIPT TYPES — DEFINE THESE BEFORE ANY COMPONENT

```typescript
// types/user.ts
export interface User {
  usrId: string
  displayName: string
  email: string
  homeCityId: string
  locale: string
  budgetBand: string
  travelStyle: string
  travellerType: string
}

export interface UserPreferences {
  preferenceId: string
  usrId: string
  preferredLanguages: string[]  // BCP-47 tags e.g. ['en', 'hi']
  interests: string[]           // e.g. ['heritage', 'food']
  pace: string
  maxDailyBudget: string | null // money as string
  preferredCurrency: string
}

// types/trip.ts
export interface Trip {
  trpId: string
  ownerId: string
  title: string
  destinationCityId: string
  startDate: string    // YYYY-MM-DD (no timezone)
  endDate: string      // YYYY-MM-DD (no timezone)
  partySize: number
  mode: 'Mode A' | 'Mode NA'
  status: string
  homeCurrency: string
  members: TripMember[]
  itinerary?: Itinerary
}

export interface TripMember {
  tmbId: string
  trpId: string
  usrId: string
  displayName: string
  role: 'owner' | 'editor' | 'viewer'
  joinedAt: string
}

// types/itinerary.ts
export interface Itinerary {
  itnId: string
  trpId: string
  version: number     // CRITICAL: always send this back on mutations
  isActive: boolean
  totalCost: string   // money as string
  currency: string
  items: ItineraryItem[]
}

export interface ItineraryItem {
  itmId: string
  itnId: string
  dayIndex: number
  sortOrder: number
  startsAt: string | null
  endsAt: string | null
  itemType: string
  entityType: string | null
  entityId: string | null
  title: string
  cost: string        // money as string e.g. "65.00"
  currency: string
  slotStatus: 'EMPTY' | 'IN_CONSENSUS' | 'BRANCHED' | 'CONFIRMED'
  locked: boolean
  status: string
  activeProposal?: Proposal
}

// types/proposal.ts
export interface Proposal {
  prpId: string
  itnId: string
  proposedByUserId: string
  proposedByDisplayName: string
  action: string
  entityType: string | null
  entityId: string | null
  title: string
  rationale: string   // NOT description — this field is called rationale
  costDelta: string   // money as string, NOT estimated_cost
  currency: string
  closesAt: string | null  // null until first NO vote in Mode NA
  status: 'open' | 'accepted' | 'rejected' | 'expired'
  currentRound: number
  votes: Vote[]
}

// types/vote.ts
export interface Vote {
  votId: string
  prpId: string
  usrId: string
  displayName: string
  value: 'yes' | 'no'   // WanderMatch never writes 'abstain'
  comment: string | null // REQUIRED when value === 'no', null when value === 'yes'
  castAt: string
}

// types/branch.ts
export interface Branch {
  brcId: string
  itmId: string
  parentBranchId: string | null  // null for top-level branches
  title: string
  rationale: string
  entityType: string | null
  entityId: string | null
  costDelta: string   // money as string
  status: 'OPEN' | 'FINALIZED'
  members: BranchMember[]
}

export interface BranchMember {
  bmcId: string
  brcId: string
  usrId: string
  displayName: string
}

// types/solo.ts
export interface GroupMatch {
  trip: Trip
  compatibilityScore: number   // integer 0-100
  ageGroupMatch: boolean
  sharedLanguages: string[]    // BCP-47 tags
  sharedInterests: string[]
  dateOverlapDays: number
}

export interface GuideMatch {
  guide: TourGuide
  compatibilityScore: number   // integer 0-100
  sharedLanguages: string[]
  sharedSpecialisations: string[]
}

export interface TourGuide {
  gidId: string
  cityId: string
  displayName: string
  languages: string[]
  specialisation: string
  dayRate: string      // money as string
  halfDayRate: string  // money as string
  currency: string
  rating: number | null
  reviewCount: number
  certified: boolean
  bio: string
}
```

---


<a id="member-phase-3"></a>
## Phase 3 — Connect APIs and real-time events

Read the retained sections below together for this phase:

- 8. API CALLS — COMPLETE LIST OF ENDPOINTS YOU CALL
- 9. WEBSOCKET — HOW TO CONNECT AND HANDLE EVENTS

## 8. API CALLS — COMPLETE LIST OF ENDPOINTS YOU CALL

All calls go to `import.meta.env.VITE_API_BASE_URL`. Never hardcode the URL.

```typescript
// lib/api.ts

const BASE = import.meta.env.VITE_API_BASE_URL

// Auth header helper — get JWT from Clerk
async function authHeaders(getToken: () => Promise<string | null>) {
  const token = await getToken()
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  }
}

// TRIPS
// GET /api/trips — get all trips for current user
// GET /api/trips/{trpId} — get single trip with itinerary + members + proposals
// POST /api/trips — create new trip
// POST /api/trips/{trpId}/members — invite a member

// PROPOSALS
// POST /api/proposals — create proposal
//   Body: { itmId, trpId, rationale, costDelta, currency, entityType, entityId, title }
//   Note: field is 'rationale' NOT 'description', 'costDelta' NOT 'estimatedCost'

// VOTES
// POST /api/votes — cast a vote
//   Body: { prpId, usrId, value: 'yes'|'no', comment: string|null }
//   Rule: comment is REQUIRED (non-empty string) when value === 'no'
//   Rule: comment must be null or omitted when value === 'yes'
//   Rule: casting yes on a new proposal auto-retracts your yes on another proposal for same itmId

// CONSENSUS
// POST /api/consensus/reconcile — trigger AI blended plan or branching
//   Body: { prpId }
//   Response either: { action: 'BLENDED', blendedPlan: {...}, currentRound: number }
//   Or:              { action: 'BRANCHED', branches: Branch[] }

// BRANCHES
// GET /api/branches/{itmId} — get all branches for a slot
// POST /api/branches/{brcId}/confirm — confirm branch as member
// POST /api/branches/{brcId}/modify — request modification on branch

// TRIP CHAT
// GET /api/trips/{trip_id}/chat — get chat messages for trip
// POST /api/trips/{trip_id}/chat — send a chat message
//   Body: { content, isProposal?: boolean } (Caller identity from JWT token)
// POST /api/chat/{msgId}/propose — click "Propose this as the plan" button
//   Logic: if unanimous yes ➔ slot becomes CONFIRMED, AI loop terminates

// SOLO MATCHING
// POST /api/solo-matching/groups — match solo user to group trips
//   Caller identity from JWT token (no caller ID in body)
//   Response: GroupMatch[]
// POST /api/solo-matching/guides — match solo user to guides
//   Body: { city: string, maxBudget?: string } (Caller identity from JWT)
//   Response: GuideMatch[]

// PHOTOS & MEMORIES
// POST /api/photos — upload trip photo (multipart form-data: file: UploadFile, trpId: string)
//   Note: POST /api/photos/upload is an unapproved historical proposal; production route is POST /api/photos.
// GET /api/photos/{trpId} — get trip photo gallery
//   Query: ?usrId=usr_xxx for "My Photos" filtered view
// POST /api/face/register — register face (multipart form-data: straight, left, right photos + usrId)
// GET /api/face/status/{usrId} — get face registration status for onboarding banner
```

---

## 9. WEBSOCKET — HOW TO CONNECT AND HANDLE EVENTS

```typescript
// context/TripContext.tsx

// Connect to: ws://{WS_BASE_URL}/ws/trips/{trpId}?token={jwtToken}
// (Target authenticated route; historical development URL was /ws/trips/{trpId}/{usrId})
// where WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL

// Events you receive (all camelCase, verb-first):
// resyncSnapshot                  → { type: 'resyncSnapshot', snapshot: { trip, itinerary, members, activeProposals, branches } }
// voteCast                        → { type: 'voteCast', trpId, prpId, usrId, value, comment }
// proposalCreated                 → { type: 'proposalCreated', trpId, proposal: Proposal }
// branchConfirmed                 → { type: 'branchConfirmed', trpId, brcId, usrId }
// slotStatusChanged               → { type: 'slotStatusChanged', trpId, itmId, slotStatus: SlotStatus }
// aiPlanGenerated                 → { type: 'aiPlanGenerated', trpId, itmId, blendedPlan | branches }
// aiRecommendationReady          → { type: 'aiRecommendationReady', trpId, itmId, ... } (alias of aiPlanGenerated)
// newChatMessage                  → { type: 'newChatMessage', trpId, message: ChatMessage }
// consensus.clarification_requested → { type: 'consensus.clarification_requested', trpId, itmId, extractedConstraints: [] }
// itineraryUpdated                → { type: 'itineraryUpdated', trpId, version: number }
// slotTimerStarted                → { type: 'slotTimerStarted', trpId, itmId, closesAt: string }
// slotTimerUpdated                → { type: 'slotTimerUpdated', trpId, itmId, closesAt: string }
// voteRetracted                   → { type: 'voteRetracted', trpId, prpId, usrId }
// negotiationCardRendered         → { type: 'negotiationCardRendered', trpId, itmId, options: [] }

// ON RECONNECT: TripContext receives resyncSnapshot automatically; or re-fetches GET /api/trips/{trpId} to sync state
// because WebSocket may have dropped events while disconnected
```

---


<a id="member-phase-4"></a>
## Phase 4 — Build components and feature screens

Read the retained sections below together for this phase:

- 10. GLOBAL COMPONENT LIBRARY — BUILD THESE FIRST
- 11. SCREENS — COMPLETE SPECIFICATION
- 7. Master AI System Specification Alignment (Post-Hackathon)

## 10. GLOBAL COMPONENT LIBRARY — BUILD THESE FIRST

Before any screen, build these reusable components:

### 10.1 Primary Button
```tsx
// bg-route text-paper rounded-[10px] font-sans font-medium px-4 py-2
// hover: bg-route-dark
// focus-visible: ring-2 ring-route
// min height/width: 44px (mobile touch target)
```

### 10.2 Secondary Button
```tsx
// bg-paper text-ink border border-slate-light rounded-[10px] font-sans font-medium px-4 py-2
// hover: bg-slate-light/30
// focus-visible: ring-2 ring-route
```

### 10.3 Input Field
```tsx
// bg-paper border border-slate-light rounded-[8px] px-3 py-2 text-sm text-ink
// focus: border-route outline-none
// placeholder: text-slate
```

### 10.4 Status Pill
```tsx
// Props: status: SlotStatus
// EMPTY        → bg-slate/10 text-slate
// IN_CONSENSUS → bg-route/10 text-route
// BRANCHED     → bg-clay/10 text-clay
// CONFIRMED    → bg-amber/10 text-amber
// Always pairs color with text label AND icon (never color alone)
// Icons: EMPTY→Circle, IN_CONSENSUS→Vote, BRANCHED→GitFork, CONFIRMED→CheckCircle
```

### 10.5 Vote Pill (interactive)
```tsx
// YES button: bg-route text-paper rounded-[10px]
// NO button:  bg-clay text-paper rounded-[10px]
// When NO is selected: show mandatory comment textarea below
// Submit is BLOCKED if NO and comment is empty/whitespace
// Show error: "A 'no' vote requires a typed reason or suggestion"
```

### 10.6 Suggestion Chip
```tsx
// Compact tag showing typed NO comment / suggestion
// bg-paper border border-slate-light rounded-full px-3 py-1 text-xs text-ink font-mono
```

### 10.7 Toast Notification
```tsx
// Slide-in from top-right
// Triggered by WebSocket events: voteCast, slotStatusChanged, proposalCreated
// Shows for 4 seconds then auto-dismisses
// bg-card border border-slate-light rounded-[10px] shadow-sm
```

### 10.8 Modal Window
```tsx
// Centered overlay, backdrop: bg-ink/40
// Card: bg-card rounded-[10px] p-6 max-w-lg w-full
// Always has explicit close button (X) top-right
```

### 10.9 Empty State Block
```tsx
// Centered, bg-paper, font-mono subtitle, calm message, single primary CTA button
```

### 10.10 Top Nav Bar
```tsx
// Persistent header across all authenticated screens
// Contains: WanderMatch logo (font-serif), section tabs, Mode pill, 
//           live presence avatars, Trip Chat toggle button, profile dropdown
// Mode pill: "Mode A (Admin)" in route color | "Mode NA (Collab)" in slate color
```

---

## 11. SCREENS — COMPLETE SPECIFICATION

### Screen 1: Sign Up Screen
**Route**: `/sign-up`
**Purpose**: Clerk auth + collect travel preferences + optional face registration

**Layout**: Centered paper card, 3 steps:
- Step 1: Clerk `<SignUp />` component
- Step 2: Preference chips — age group selector, BCP-47 language multi-select, interests multi-select (use enums: heritage, food, trekking, wildlife, photography, religious, shopping, accessibility from guide_specialisation + poi_category)
- Step 3: Optional face capture (3 photos: Straight, Left Tilt, Right Tilt) with prominent "Skip for now" button

**States**: Default | Loading | Error ("Face quality check failed: exactly one face required per photo")

**Dummy data for Phase 1** (use this until backend is ready):
```typescript
const dummyNewUser = {
  usrId: 'usr_new_01',
  email: 'user@example.com',
  displayName: 'Jordan Lee',
  preferredLanguages: ['en', 'es'],
  interests: ['heritage', 'food', 'trekking'],
  faceRegistered: false,
}
```

---

### Screen 2: Log In Screen
**Route**: `/sign-in`
**Purpose**: Authenticate existing user

**Layout**: Clean paper card, WanderMatch logo (font-serif), Clerk `<SignIn />` component (in production) or Mock Auth Provider (in offline dev mode).

**Offline Mock Authentication Contract**:
When developing offline without live Clerk credentials or network connectivity, `AuthContext.tsx` operates in mock mode:
- Simulates authenticated traveler: `user = { id: "usr_001", email: "nikitha@example.com", displayName: "Nikitha", role: "owner" }`
- Provides toggle for unauthenticated state (`user = null`) and expired token simulation.
- Supplies mock JWT bearer tokens for HTTP and WebSocket client headers.
- Never requires live network access to Clerk servers for frontend development.

---

### Screen 3: My Trips Screen
**Route**: `/trips`
**Purpose**: Show all trips the user belongs to

**Layout**: Grid of trip cards (2-col desktop, 1-col mobile)

**Each trip card shows**:
- Destination city name + country
- Date range (font-mono)
- Mode pill: "Mode A" | "Mode NA"
- Role badge: "Owner" | "Editor" | "Viewer"
- Trip status
- Route Line thumbnail (small visual preview)

**Data source**: `GET /api/trips` (after Checkpoint 1) or dummy data (Phase 1)

**Dummy data for Phase 1**:
```typescript
const dummyTrips = [
  {
    trpId: 'trp_bali_2026',
    title: 'Bali Tropical Escape & Cultural Journey',
    destinationCityId: 'cty_bali',
    destinationCityName: 'Bali',
    startDate: '2026-10-10',
    endDate: '2026-10-16',
    mode: 'Mode A',
    ownerId: 'usr_nikitha',
    role: 'owner',
    status: 'planning',
  },
  {
    trpId: 'trp_kerala_2026',
    title: 'Kerala Backwaters & Spice Trail',
    destinationCityId: 'cty_kochi',
    destinationCityName: 'Kochi',
    startDate: '2026-11-01',
    endDate: '2026-11-07',
    mode: 'Mode NA',
    ownerId: 'usr_panchami',
    role: 'editor',
    status: 'planning',
  },
]
```

---

### Screen 4: Create Trip Screen
**Route**: `/trips/new`
**Purpose**: Create a new group trip

**Layout**: Centered form card
**Fields**:
- Trip title (text input)
- Destination city (text input — will resolve to city_id via backend)
- Start date (date picker)
- End date (date picker)
- Party size (number input)
- Trip mode selector: "Mode A (Admin-Led)" | "Mode NA (Collaborative)"
- Notes (optional textarea)

**On submit**: `POST /api/trips` → redirect to `TripHomeScreen`

**Validation**: End date must be after start date. All fields except notes are required.

---

### Screen 5: Trip Preview Screen
**Route**: `/trips/:trpId/preview`
**Purpose**: Read-only landing for invited members before joining

**Layout**:
- Hero banner: destination city, dates, mode pill, member count
- Read-only Route Line timeline (all slots shown as EMPTY, dashed Slate Light)
- "Join Trip" primary button → calls `POST /api/trips/:trpId/members`
- "View Full Itinerary" (disabled until joined)

---

### Screen 6: Trip Home Screen (MOST COMPLEX SCREEN)
**Route**: `/trips/:trpId`
**Purpose**: Main workspace for group itinerary collaboration

**Layout (Desktop ≥ 768px)**:
- Left/Center: Itinerary Timeline with Route Line (max-w-4xl)
- Right: Collapsible Trip Chat rail (w-80 or w-96)

**Layout (Mobile < 768px)**:
- Single column, full-width slot cards
- Trip Chat as full-screen drawer overlay
- Primary action buttons anchored at bottom (sticky bottom-0)

**Top section**:
- Hero banner: trip title (font-serif), destination, date range (font-mono), mode pill
- Live presence bar: avatar stack of currently online members (pulled from WebSocket connections)
- "Add Activity" button (only for owner/editor role)

**The Route Line timeline**:
- Vertical dashed line connecting Morning → Afternoon → Evening → Night slots for each day
- Each slot is an `ItinerarySlotCard` component
- Line color changes based on slot status (see section 3.4)
- BRANCHED slots fork into parallel Clay lines

**ItinerarySlotCard shows**:
- Time badge (Morning/Afternoon/Evening/Night) in font-mono
- Activity title
- Entity type (city/POI) + cost (font-mono, money as string)
- Status pill (EMPTY/IN_CONSENSUS/BRANCHED/CONFIRMED with color + icon + text)
- Live vote tally: "3 YES / 1 NO" (font-mono)
- "Vote / Review" button → opens VoteModal
- If CONFIRMED: Amber background highlight
- If BRANCHED: Clay left border, "View Branches" button

**Real-time updates**:
- Subscribe to WebSocket on mount
- On `voteCast`: update vote tally on affected proposal
- On `proposalCreated`: add new proposal to relevant slot
- On `slotStatusChanged`: update slot status + Route Line color
- On `aiPlanGenerated`: show AI Concierge Panel + toast notification
- On reconnect: always re-fetch `GET /api/trips/:trpId` first

**Mode A admin controls** (only show if current user is trip owner AND mode is 'Mode A'):
- "Invoke AI" button per slot
- "Accept Blended Plan" button
- "Force Branch Now" button
- "Extend Round" button
These appear in the AI Concierge Panel only after AI has been invoked.

**Dummy data for Phase 1**:
```typescript
const dummyTripHome = {
  trpId: 'trp_bali_2026',
  title: 'Bali Tropical Escape',
  mode: 'Mode A',
  version: 3,
  items: [
    {
      itmId: 'itm_b1',
      dayIndex: 1,
      sortOrder: 1,
      title: 'Sacred Monkey Forest',
      slotStatus: 'CONFIRMED',
      cost: '25.00',
      currency: 'USD',
      entityType: 'poi',
      entityId: 'poi_monkey_forest',
    },
    {
      itmId: 'itm_b2',
      dayIndex: 1,
      sortOrder: 2,
      title: 'Mount Batur Trek',
      slotStatus: 'IN_CONSENSUS',
      cost: '65.00',
      currency: 'USD',
      entityType: 'poi',
      entityId: 'poi_batur',
    },
    {
      itmId: 'itm_b3',
      dayIndex: 1,
      sortOrder: 3,
      title: 'Evening Activity',
      slotStatus: 'EMPTY',
      cost: '0.00',
      currency: 'USD',
      entityType: null,
      entityId: null,
    },
  ],
}
```

---

### Screen 7: Propose Activity Modal
**Route**: Modal on top of `/trips/:trpId`
**Purpose**: Submit a new activity proposal for a slot

**Layout**: Modal with form:
- Title (text input, required)
- Rationale (textarea, required) — label it "Rationale" NOT "Description"
- Entity type selector: hotel | flight | poi | package | guide | transfer | meal | free
- Entity ID (text input) — label "Entity ID (e.g. verified catalog ID like poi_campuhan_ridge)"
- Cost delta (number input, labeled "Cost Change ($)") + currency selector
- Submit button

**On submit**: `POST /api/proposals`
```typescript
// Request body shape:
{
  itmId: string,
  trpId: string,
  title: string,
  rationale: string,      // NOT description
  entityType: string,
  entityId: string,
  costDelta: string,      // Send as string e.g. "15.00", NOT a number
  currency: string,
}
```

**Important**: If backend returns `{ status: 'QUEUED' }`, show message: "Your proposal has been queued for the next round — the current voting window is still open." Do NOT treat this as an error.

---

### Screen 8: Vote Modal (Slot Detail Modal)
**Route**: Modal on top of `/trips/:trpId`
**Purpose**: Review active proposal and cast vote

**Layout** (top to bottom):
1. Proposal details: title, rationale, creator name, cost delta (font-mono), entity info
2. Group vote tally: "X YES / Y NO / Z haven't voted" with avatar breakdown
3. All NO vote comments shown as Suggestion Chips (visible to everyone per actor rules)
4. If in Mode A + current user is admin: AI recommendation panel with admin control buttons
5. Vote form at bottom:
   - Vote Pill: YES (Route green) | NO (Clay red)
   - If NO selected: mandatory comment textarea appears
   - Submit button (disabled if NO and no comment)
   - Error message if NO submitted without comment: "A 'no' vote requires a typed reason or suggestion"

**Timer display** (Mode NA only):
- If `closesAt` is not null: show countdown timer in font-mono
- Format: "Voting closes in MM:SS"
- When timer reaches 0: show "Voting window closed — awaiting AI reconciliation"

**Non-voter rule**: If current user hasn't voted, show "You haven't voted yet" — they can always vote even if others have.

---

### Screen 9: Conflict Resolution / AI Concierge Panel
**Route**: Panel inside `/trips/:trpId` (not a modal, an inline panel)
**Purpose**: Show AI blended plan, dissent clarifications, and admin controls

#### Plan & Resolve Usability & Clutter Resolution Contract
To resolve clutter, cognitive overload, and visual inconsistency in the Plan & Resolve workflow, Nikitha must enforce the following strict visual hierarchy and interaction rules:
1. **Spatial Separation & 8pt Grid**:
   - The panel uses `space-y-6 p-6 bg-surface border border-sand-dark rounded-xl shadow-sm`.
   - Distinct card boundaries prevent AI recommendation chips, objection clarification inputs, and voting bars from visually bleeding into one another.
2. **Visual Hierarchy & State Differentiation**:
   - **Header**: High-contrast badge with Round indicator (`"Round 2 of 3"`, font-mono), status pill matching 1:1 enum mapping, and time countdown.
   - **Side-by-Side Proposal Diff**: Original proposal (muted border) vs Blended proposal (`border-route ring-1 ring-route bg-route/5`). Distinct Route Green badges call out specific blended concessions (e.g. `"+30m buffer added"`, `"Cost: -$15/person"`).
   - **Dissent Clarification Drawer**: Collapsible and cleanly nested below the slot card rather than expanding into the timeline. Displays structured objection chips (`"Budget Concern"`, `"Schedule Conflict"`, `"Alternative POI Preferred"`) that voters can click to populate the clarification input without typing friction.
3. **Interactive Control Layout**:
   - **Mode A Admin Controls** (trip owner only): Clear action grouping in a dedicated footer bar (`"Accept Blended Plan"` as Primary Button; `"Force Branch Now"` with Clay border; `"Extend Round"` as Secondary Button).
   - **Mode NA (Collaborative)**: Informational banner: `"The group is re-voting on this synthesized compromise"`.
4. **Resilience & Loading Skeletons**:
   - Dedicated loading skeleton while AI is synthesizing (`animate-pulse` placeholder cards with route line shimmer), preventing Cumulative Layout Shift (CLS).
   - Error banner with retry trigger if negotiation synthesis fails (`"Failed to generate compromise. Retaining original proposal."`).

---

### Screen 10: Branch View
**Route**: `/trips/:trpId/branches/:itmId`
**Purpose**: View forked parallel branches + Trip Chat

**Layout**:
- Clay Route Line forks into N parallel branch lines at top
- Branch cards side-by-side (or stacked on mobile)
- Each branch card shows:
  - Branch title + rationale
  - Member avatars assigned to this branch
  - "FINALIZED" tag if single-member auto-resolved
  - "Confirm" button (only if current user is member of this branch)
  - "Request Modification" button (only if current user is member of this branch)
  - Entity info + cost delta
- Right side: Trip Chat drawer (same as on Trip Home)

**Branch confirmation UI**:
- "Confirm" → calls `POST /api/branches/:brcId/confirm`
- "Request Modification" → calls `POST /api/branches/:brcId/modify` with comment textarea
- No action = accepted after response window (show "Will auto-accept when window closes")

**Single-member auto-resolved branch**:
- Show "Auto-Resolved" badge in Amber
- Show "This branch had one member — their preference was automatically finalized"

---

### Screen 11: Resolved Itinerary Screen
**Route**: `/trips/:trpId/resolved`
**Purpose**: Finalized trip schedule & export hub

**Layout**:
- Clean Route Line with all stops highlighted in Amber (`#EAA93B`)
- Each confirmed slot shows: title, entity info, time, cost (font-mono), confirmed vote margin, and location address
- Branch reconvergence markers where branches rejoined into the master schedule
- Budget summary breakdown card (total estimated cost vs per-member spend)
- Final trip consensus audit badge (indicating 100% confirmed slots)

#### PDF Export Architecture, Preview & Online Export Contract
Itinerary PDF export is **REQUIRED and ONLINE** (`FR-EXP-01`). Offline PDF file generation/export is **DEFERRED** and is not an acceptance gate. Nikitha's responsibility is **NOT** reduced to a simple button; she owns the complete visual and interactive export experience:
1. **Export Preview Modal (`ExportPreviewModal.tsx`)**:
   - Triggered by the primary button `"Export Itinerary PDF"`.
   - Displays a pixel-accurate preview of the compiled itinerary document before triggering the download.
   - Allows users to toggle preview sections: "Include Budget Breakdown", "Include Member Roster", "Include Route Map".
   - Primary action: `"Download PDF"`; Secondary action: `"Print via Browser"` (`window.print()`).
2. **Printable DOM Layout & Print Stylesheet (`@media print`)**:
   - Comprehensive print stylesheet rules:
     * Navigation bar, sidebars, modal controls, and floating action buttons are strictly hidden (`print:hidden`).
     * Itinerary slots formatted into clean paginated day cards with page-break controls (`break-inside-avoid`).
     * Route line rendered in high-contrast monochrome with amber destination markers.
     * Font sizes adjusted for standard A4 / US-Letter paper with 0.5-inch margins.
3. **Authoritative JSON Export Data Contract**:
   - The export layout consumes a structured JSON contract matching `export_itinerary_pdf_preview.json`:
     ```typescript
     export interface ItineraryExportPayload {
       tripId: string;
       title: string;
       destination: string;
       dateRange: { startDate: string; endDate: string };
       mode: "Mode NA" | "Mode A";
       currency: string;
       totalCost: string;
       perPersonCost: string;
       members: Array<{ userId: string; displayName: string; role: string }>;
       days: Array<{
         dayNumber: number;
         date: string;
         slots: Array<{
           slotId: string;
           title: string;
           timeWindow: { startTime: string; endTime: string };
           entityName: string;
           cost: string;
           location: string;
           notes?: string;
         }>;
       }>;
       reconciliationSummary: {
         totalSlots: number;
         confirmedSlots: number;
         branchesReconverged: number;
       };
     }
     ```
4. **Online Export Workflow & Fixture-Backed UI Development Support**:
   - PDF export is an **online capability** requiring backend coordination. Nikitha verifies the frontend preview and download interaction against the agreed online export endpoint (`GET /api/trips/{trip_id}/itinerary/export` or proposed `/api/trips/{trip_id}/itinerary/export.pdf`).
   - **Optional Fixture-Backed Preview**: During early frontend development without a live backend, Nikitha may load the static preview modal using `mock_adapter.ts` with fixture `export_itinerary_pdf_preview.json`. This provides development support so UI work is not blocked, but offline PDF file generation is strictly deferred and is NOT a completion gate.
   - **Error & Failure Handling**: The export UI must display explicit error states for network disconnects, upstream timeouts (HTTP 504), or draft trips with unconfirmed slots (`"Cannot export itinerary while slots are unconfirmed"`), with an accessible retry button.
5. **Collaborative Division Under Pending Decision #30**:
   - **Decision #30 (PDF Rendering Strategy)** remains **PENDING** between client-side generation (`@react-pdf/renderer` / `jspdf`) and server-side compilation (FastAPI WeasyPrint / ReportLab). Neither engine is approved yet; all named libraries and routes (`/api/v1/...`) are **PROPOSED**.
   - If **Client-Side** rendering is approved: Sharvani supplies the authoritative export payload; Nikitha bundles the renderer and generates the PDF blob in the browser.
   - If **Server-Side** rendering is approved:
     * **Sharvani** owns data authorization and executes server-side HTML-to-PDF template compilation.
     * **Panchami** mounts the binary streaming transport endpoint (`GET /api/trips/{trip_id}/itinerary/export.pdf` [proposed]) with `Content-Type: application/pdf` and `Content-Disposition: attachment; filename="wander-match-itinerary.pdf"`.
     * **Nikitha** connects the preview modal's `"Download PDF"` button to fetch the binary blob and trigger browser download via `window.URL.createObjectURL(blob)`.
   - Pending Decision #30 blocks only the specific rendering library choice; it does NOT block the preview modal, print stylesheet, or mock UI development.

---

### Screen 12: Audit / Members / Photos Screen
**Route**: `/trips/:trpId/history` (tabbed)
**Purpose**: Audit trail, members, trip photos

**Three tabs**:

**Tab 1: Audit Log**
- Chronological list of version history entries
- Each entry: timestamp (font-mono), action description, who did it
- Pulled from revision_history

**Tab 2: Members**
- List of all trip members
- Each row: avatar, display name, role badge (owner/editor/viewer), join date
- Owner badge highlighted in Route green

**Tab 3: Trip Photos**
- Subtabs: "All Photos" | "My Photos"
- "All Photos": grid of all uploaded trip photos (served via Panchami's `/static/uploads/` or target CDN URL) — visible to ALL members
- "My Photos": if face registered → grid of auto-tagged personal photos
  - If NOT face registered: show message "Register your face profile to view your auto-sorted personal trip photos." + "Register Now" button
- Upload button: opens file picker → calls `POST /api/photos` (Panchami's endpoint, persisting to Sharvani's schema in-process)
- Face registration gating: only the "My Photos" tab is gated, never "All Photos"

#### Exact Three-Person Face Regression Acceptance Scenario (Gallery UI)
This concrete acceptance scenario verifies that the photo gallery cleanly resolves the original reported face grouping regression (where photos of distinct members were collapsed into a single folder or tagged inaccurately):
1. **Reference Test Dataset**:
   - **Enrolled Individuals (3 Distinct Members)**: Person A (Nikitha), Person B (Panchami), Person C (Sharvani), each with registered 3-angle enrollment profiles (Straight, Left Tilt, Right Tilt).
   - **Individual Photos**: 3 distinct photos containing exactly one of Person A, Person B, or Person C.
   - **Group Photos**: Multi-person photos containing combinations (Person A + B, Person B + C, Person A + B + C).
   - **Unknown / Un-Enrolled Person**: 1 photo containing Person D (who has never registered a face profile).
   - **Scenery / Landscape**: 1 photo containing mountains/beach with zero human faces.
2. **Recognition Metric Calibration Reality**:
   - DeepFace matching involves three distinct mathematical quantities:
     1. **Raw Cosine Similarity**: $S_{\text{cos}} \in [-1, 1]$.
     2. **Cosine Distance**: $D_{\text{cos}} = 1 - S_{\text{cos}}$ (DeepFace default ArcFace distance threshold is 0.68, equivalent to raw similarity 0.32).
     3. **Prototype Transformed Heuristic Score**: The prototype in `matching.py` maps raw similarity 0.45 to heuristic score 0.90, comparing against `CONFIDENCE_THRESHOLD = 0.90`.
   - **Evidentiary Honesty**: A heuristic score is NOT a probability or a mathematical guarantee of zero false merges across all future images. The gallery displays face tags based on trip-isolated candidate matching, rendering bounding boxes from API responses without accessing raw biometric vectors.
3. **Schema Model Boundary (`photo_person` vs Proposed `photo_face_tags`)**:
   - The current schema table in `backend/app/models/additive.py` is `photo_person` (`photo_id`, `user_id`, `confidence`). It links recognized users but lacks `face_index`, `bounding_box`, and unknown face instances (`user_id = NULL`).
   - `photo_face_tags` is an explicit **proposed logical target representation** and pending schema migration owned by Sharvani. The frontend consumes the unified API JSON shape returned by Panchami (`facesDetected`, `tags: [{ faceIndex, userId, displayName, confidence, facialArea }]`), decoupling UI rendering from physical database schema evolution.
4. **Gallery UI Acceptance Criteria**:
   - **Strict Per-Person Isolation ("My Photos")**: When logged in as Person A, only photos containing Person A are rendered. Photos containing only Person B or Person C are strictly excluded.
   - **Group Photo Instance Multi-Tagging**: In group photos with multiple people, each detected face receives a separate bounding box and name tag. Distinct people are mapped to their respective member profiles, never collapsed into a single identity or cross-tagged.
   - **Zero False Cross-Person Tags**: Person A is never labeled as Person B or C, and vice versa within the fixed reference corpus.
   - **Unidentified Faces Drawer**: Person D (un-enrolled) produces an `unidentified` match status and is displayed in an accessible "Unidentified Faces" review badge/drawer. Person D is NEVER misattributed to Person A, B, or C.
   - **Scenery Folder Segregation**: The scenery photo returns `facesDetected: 0` and is automatically categorized under the "Scenery / Landscapes" folder view with zero face bounding boxes rendered.
   - **Honest Review Badging**: If match confidence falls below threshold (e.g. prototype heuristic score < 0.90), the face tag renders a `"Review Needed"` amber pill rather than displaying a false positive name.

---

### Screen 13: Solo Match Screen
**Route**: `/solo`
**Purpose**: Find compatible group trips or tour guides

**Layout**: Two tabs:

**Tab 1: Find a Group**
- "Find My Groups" button → calls `POST /api/solo-matching/groups`
- Results list: each GroupMatch card shows:
  - Trip title, destination, dates
  - Compatibility score: large number in font-mono (e.g. "85%") in Route green
  - Breakdown: "Age Group ✓" | "Languages: en, es" | "Interests: heritage, food" | "Overlap: 5 days"
  - "Request to Join" button

**Tab 2: Find a Guide**
- City input + max budget input
- "Find Guides" button → calls `POST /api/solo-matching/guides`
- Results list: each GuideMatch card shows:
  - Guide display name, city, specialisation
  - Compatibility score: font-mono percentage
  - Day rate (font-mono, money as string + currency)
  - Rating (e.g. "4.8 ★")
  - Languages spoken (BCP-47 tags rendered as readable names: "en" → "English")
  - Certified badge if certified === true

---

### Screen 14: Trip Chat (Drawer component, always available on Trip Home + Branch View)
**Purpose**: Always-on real-time chat per trip
**Canonical Endpoints**: `GET /api/trips/{trip_id}/chat` & `POST /api/trips/{trip_id}/chat` (Frontend `api.ts` must align to these canonical routes, retiring `/api/trips/{trpId}/messages` and `/api/messages`).

**Layout**: Right rail on desktop (w-80), full-screen drawer on mobile
- Message list (newest at bottom, auto-scroll)
- Each message: sender avatar, display name, content, timestamp (font-mono)
- "Propose this as the plan" action button on each message
  - Clicking it calls `POST /api/chat/:msgId/propose`
  - If unanimous YES → slot becomes CONFIRMED immediately
  - If majority but not unanimous → message: "Not unanimous — this has been queued as a standard proposal for the next round"
  - Show vote status on the message after propose is clicked
- Chat input field + Send button at bottom

---

## 7. Master AI System Specification Alignment (Post-Hackathon)

> **Canonical Reference**: All UI components, form validation rules, error displays, and negotiation screens must strictly conform to canonical [AI.md](AI.md) (and [ai/AIConsensus/docs/AI.md](AI.md)).

### Key Requirements for Frontend Track:
1. **Master Field Validation Matrix**: Implement client-side validation across the 17 interactive form controls defined in `FRONTEND_SPEC.md Section 4`, which map to the 48 canonical backend/API field validation rules defined in `AI.md Section 6.1`. (The historical reference to "42 fields" is superseded by the 48 context-specific backend contracts and 17 frontend controls).
2. **Accessible Visual Error Contract**: Style invalid fields with `border-clay` (`#C1502E`), inline alert text, `aria-invalid="true"`, and autofocus on the first invalid field.
3. **The 6 Verification Badges**: Render distinct visual badges and icons for `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `NEEDS_CLARIFICATION`, `INFEASIBLE`, and `BLOCKED`.
4. **Schedule Negotiation Card Specification**:
   - When an activity or candidate is infeasible (e.g. transit time exceeds slot window), render the evidence-grounded 3-option card:
     - **Option 1: `KEEP_ORIGINAL`**:
       - *UI Behavior*: Dismisses the negotiation card locally for the caller.
       - *State Contract*: Preserves the baseline activity view with a non-blocking warning badge. Does **NOT** mutate the slot or force a binding group decision.
       - *API*: Dispatches `POST /api/negotiation/select-option` with `optionType: "KEEP_ORIGINAL"`, `expectedVersion`, `evidenceToken`.
     - **Option 2: `CLOSER_ALTERNATIVE`**:
       - *UI Behavior*: Shows closer POI card with travel duration comparison. Clicking "Propose Closer Option" submits proposal for group consideration.
       - *State Contract*: Does **NOT** directly mutate accepted itinerary. In Mode A shows "Submitted to Admin for Review"; in Mode NA shows "Proposal Created for Group Vote".
       - *API*: Dispatches `POST /api/negotiation/select-option` with `optionType: "CLOSER_ALTERNATIVE"`, `selectedOptionId: "opt_closer_02"`.
     - **Option 3: `RESCHEDULE_WINDOW`**:
       - *UI Behavior*: Shows suggested time window adjustment. In Mode A (if caller is admin), presents "Confirm New Times"; in Mode NA, presents "Propose Schedule Adjustment".
       - *State Contract*: Mode A updates slot times and bumps version; Mode NA opens schedule-modification proposal / voting round (unanimous chat override is separate).
       - *API*: Dispatches `POST /api/negotiation/select-option` with `optionType: "RESCHEDULE_WINDOW"`.
   - **Concurrency & Stale State Handling**:
     - Always include `expectedVersion: itinerary.version` in selection payload.
     - If API returns `409 Conflict` (`ERR_STALE_VERSION`), display alert: *"Itinerary was updated by another traveler. Refreshing latest state..."* and issue an authenticated HTTP `GET /api/trips/{trpId}` request to refresh authoritative state (clients never emit server events).
     - If API returns `422 Unprocessable Entity` (`ERR_TOKEN_EXPIRED`), display: *"Clarification window expired. Please request a new clarification session."* If `422` (`ERR_EVIDENCE_INVALID`), display: *"Clarification token invalid. Session re-initialized."*
5. **Dissent Clarification Flow (`NEEDS_CLARIFICATION`)**:
   - When AI classifier returns `NEEDS_CLARIFICATION` or `UNCLASSIFIED_OR_INSUFFICIENT_EVIDENCE` (or WebSocket emits `consensus.clarification_requested`):
   - Render a prominent Clarification Prompt Card to dissenting travelers: *"Your objection needs more detail (e.g., specific budget limits, mobility requirements, or alternative times) before a blended option can be generated."*
   - Display suggested clarification chips based on `extracted_constraints`.
   - Invariant: Clarification does **NOT** increment round number, does **NOT** count as a vote, and does **NOT** reset voting deadline.
6. **Permission-Based Geolocation**: Provide user-triggered location button with browser permission dialog and fallback manual address input. Never use device GPS as group itinerary origin.

### 7.2 UI State Machine & Interaction Rules for AI-Assisted Consensus

`[APPROVED_REQUIREMENT]` Nikitha's frontend components must strictly adhere to the authoritative consensus state machine without performing local business logic:

1. **Strict Prohibition on Frontend Consensus Inference**:
   - The UI must **never** infer consensus, decide that travelers consented, or predict round advances based on free-form LLM text or client-side heuristics.
   - Slot status is driven **strictly** by backend state properties (`slot.status = 'CONFIRMED' | 'BRANCHED' | 'OPEN'`) received via REST API or WebSocket event (`slotStatusChanged`, `branchConfirmed`).
2. **Authoritative Countdown & Timer Display**:
   - The countdown pill in the slot header is driven strictly by server-provided `slot_consensus.closes_at`.
   - The client computes remaining time as:
     ```typescript
     const remainingSeconds = Math.max(0, Math.floor((new Date(closesAt).getTime() - (Date.now() + serverTimeOffset)) / 1000));
     ```
   - When the countdown reaches `00:00`, the UI renders `Reconciling...` with a subtle spinner. The client **never** unilaterally transitions to confirmed or branched; it waits for backend `slotStatusChanged` or `aiPlanGenerated`.
3. **Advisory vs. Binding Action Gating**:
   - *Mode A (Admin-Led)*: AI candidates and branching proposals are rendered with an **`Advisory AI Proposal`** badge. The UI renders explicit action buttons (`Accept Proposal`, `Extend Round`, `Force Branch`) **strictly to the trip owner**. Non-owners see *"Awaiting admin decision"*.
   - *Mode NA (Collaborative)*: AI-blended plans are published as open proposals in the slot with binary voting pills (`Vote YES` / `Vote NO`).
4. **Dissent Clarification Interaction (`NEEDS_CLARIFICATION`)**:
   - When WebSocket emits `consensus.clarification_requested` matching `current_user.user_id`:
     - Render the Clarification Card directly beneath the contested proposal:
       - *"Your objection needs more detail (e.g., specific budget limits, mobility requirements, or alternative times) before AI can suggest a blend."*
       - Renders clickable suggestion chips (e.g., `Prefer Cultural/Museum`, `Shorter Walking (<15m)`, `Lower Cost (<$20)`).
     - Submitting clarification dispatches `POST /api/slots/{slot_id}/clarify` with canonical envelope, expecting response `{"status": "CLARIFICATION_ACCEPTED", "slotId": string, "commentId": string, "cycle": number, "round": number}`:
       ```typescript
       interface SubmitClarificationPayload {
         tripId: string;
         slotId: string;
         commentId: string;
         clarificationText: string;
         expectedVersion: number;
         evidenceToken?: string; // [PROPOSED_CONFIGURATION_TTL = 1h subject to Decision #12]
       }
       ```
     - Enforces `payload.slotId === slot_id` (rejects mismatches client-side before dispatch).
     - English-Only UI Scope: The user interface, form inputs, validation messages, objection fields, clarification chips, and negotiation cards are presented and collected strictly in English.
     - Invariant: Clarification does **NOT** increment round number, does **NOT** count as a vote, and does **NOT** reset voting deadline.
5. **Stale Response Handling & Optimistic Concurrency Control (OCC)**:
   - All mutation dispatches (`POST /api/votes`, `POST /api/negotiation/select-option`) must include `expectedVersion: itinerary.version`.
   - If the API returns `409 Conflict (ERR_STALE_VERSION)`:
     - Render an inline alert toast: *"Itinerary was updated by another traveler. Refreshing latest state..."*
     - Re-fetch authoritative trip state via HTTP `GET /api/trips/{trpId}` (the client never dispatches server broadcast events).
     - Never silently overwrite or discard traveler changes.

### 7.1 Offline Mock Fixtures for UI Development
Nikitha can develop and test all screens offline without live backend or AI services using the proposed mock adapter in `frontend/src/lib/data-access/mock_adapter.ts` (source creation is pending; Nikitha implements against this contract):

```typescript
// Mock Negotiation Card Fixture (Grounding: 75m out + 15m arr buffer + 150m hike + 15m dep buffer + 90m ret = 345m vs 180m window -> 165m deficit)
export const mockNegotiationCard = {
  slotId: "itm_7a2b9c",
  infeasibleActivity: "Mount Batur Sunrise Hike",
  conflictReason: "Schedule infeasible: transit (75m outbound + 90m return = 165m) plus arrival buffer (15m) + activity duration (150m) + departure buffer (15m) totals 345m, exceeding morning slot window (180m) by a 165m deficit",
  expectedVersion: 4,
  evidenceToken: "ev_tok_mock_8f9a2b",
  options: [
    {
      id: "opt_orig_01",
      type: "KEEP_ORIGINAL",
      title: "Keep Mount Batur",
      description: "Acknowledge schedule tightness and keep original activity."
    },
    {
      id: "opt_closer_02",
      type: "CLOSER_ALTERNATIVE",
      title: "Campuhan Ridge Walk",
      description: "Closer scenic walk (15m travel time, fits easily within window).",
      poiId: "poi_campuhan_01",
      travelTimeMinutes: 15
    },
    {
      id: "opt_resched_03",
      type: "RESCHEDULE_WINDOW",
      title: "Reschedule to Early Morning",
      description: "Shift slot to 05:00 - 11:00 to accommodate hike and transit buffers.",
      suggestedStartsAt: "05:00",
      suggestedEndsAt: "11:00"
    }
  ]
};

// Mock Clarification State Fixture
export const mockClarificationState = {
  slotId: "itm_7a2b9c",
  status: "CLARIFICATION_REQUIRED",
  message: "Your objection was marked as needing clarification.",
  prompt: "Could you specify what kind of activity you would prefer instead of Mount Batur?",
  suggestedChips: ["Prefer Cultural/Museum", "Shorter Travel (<30m)", "Lower Cost (<$20)"],
  currentRound: 1,
  deadlineRemainingSeconds: 3600
};
```

<a id="member-phase-5"></a>
## Phase 5 — Verify usability, accessibility and performance

Read the retained sections below together for this phase:

- 12. RESPONSIVE RULES
- 13. ACCESSIBILITY RULES
- 13.1 CROSS-MEMBER LOADING & CLERK PERFORMANCE INVESTIGATION PROTOCOL (FRONTEND TASK CARD)

## 12. RESPONSIVE RULES

### Mobile (< 768px):
- Single column layout everywhere
- Full-width slot cards
- Primary action buttons anchored at bottom: `sticky bottom-0 bg-paper border-t border-slate-light`
- Trip Chat: full-screen drawer overlay (not side rail)
- No intermediate breakpoints between mobile and desktop

### Desktop (≥ 768px):
- Two-column Trip Home: itinerary timeline left (`max-w-4xl`), Trip Chat rail right (`w-80`)
- Branch cards side-by-side
- Modal dialogs centered in viewport

---

## 13. ACCESSIBILITY RULES

1. **Focus rings**: All interactive elements must have `focus-visible:ring-2 focus-visible:ring-route`
2. **Color not sole signal**: Every status state pairs color WITH icon AND text label
3. **Touch targets**: All touchable elements minimum `min-h-[44px] min-w-[44px]`
4. **Motion**: Route Line animation MUST respect `prefers-reduced-motion: reduce`
   ```css
   @media (prefers-reduced-motion: reduce) {
     .route-line-draw { animation: none; }
   }
   ```

---

## 13.1 CROSS-MEMBER LOADING & CLERK PERFORMANCE INVESTIGATION PROTOCOL (FRONTEND TASK CARD)

This protocol governs the cross-member performance triage for severe loading issues reported during Trip Home rendering and Clerk user authentication. Nikitha owns the frontend reproduction and client-side profiling track.

### 1. Frontend Investigation Scope & Responsibilities
- **Reproduction**: Create reproducible test scenarios in Chrome DevTools using throttled network profiles (Fast 3G, Slow 3G) and 4x CPU throttling.
- **Client Render Timing**: Profile React component mount and re-render cycles on Trip Home (`/trips/:trpId`). Measure time-to-first-render (TTFR) and total DOM rendering latency.
- **Network Request Waterfall Analysis**:
  * Inspect DevTools Network waterfall to detect sequential request chaining (e.g., verifying whether slot data, trip membership, and chat history are fetched in parallel or blocked in serial waterfalls).
  * Enforce parallel data fetching via `Promise.all` or independent SWR/React Query caching.
- **Loading Skeletons & Layout Shift (CLS)**:
  * Verify that loading skeletons match the exact dimensions of loaded cards (`[PROPOSED TARGET]`: maintain CLS < 0.05).
  * Audit transitions from loading states to error boundaries to prevent silent blank screens during API degradation.
- **Privacy & Security during Instrumentation**:
  * Instrumentation code must **NEVER** log JWT tokens, user passwords, biometric facial embeddings, or raw objection comments to console or external monitoring services.
- **Clerk React SDK Session Hydration**:
  * Profile latency of Clerk SDK `<ClerkProvider>` initialization and session token retrieval (`useAuth().getToken()`).
  * Verify that frontend does not stall initial page rendering while waiting for Clerk session hydration; render public/skeleton layout immediately and populate authenticated state reactively.

### 2. Standardized Investigation Artifact Format
Nikitha must log performance findings using the standardized four-part ledger:
- **Baseline**: Initial measured render timing and network waterfall duration (in milliseconds).
- **Reproduction**: Step-by-step reproduction path with device and network throttling parameters.
- **Measured Bottleneck**: Concrete measured component or request taking $> 200\text{ms}$ (e.g. "Sequential waterfall: `GET /api/trips/:id` blocks for 450ms before `GET /api/trips/:id/chat` is initiated").
- **Verification**: Post-optimization DevTools profile proving latency reduction and zero regression.

---


<a id="member-phase-6"></a>
## Phase 6 — Follow the execution checklist and integration checkpoints

Read the retained sections below together for this phase:

- 14. PHASE-BY-PHASE EXECUTION PLAN

## 14. PHASE-BY-PHASE EXECUTION PLAN

### PHASE 0 — Baseline Verification, Mock Adapter Setup & Refinement Scope (Hours 0–2)
**Your job**: Verify existing application files, set up mock scenario adapter, and align demo flow.

> [!NOTE]
> **Historical Prototype Note**: The original hackathon instructions instructed scaffolding a new Vite project from scratch. The active repository already contains the complete Vite React TypeScript application (24 components, 19 screens, 4 hooks, 2 contexts). **Do NOT re-scaffold or overwrite existing source files.**
> 
> **UI Refinement Authorization**: Nikitha is explicitly authorized to improve layouts, spacing, visual hierarchy, and micro-interactions—especially streamlining the cluttered Plan & Resolve experience. Functional API contracts and voting rules remain locked.

Concrete deliverables:
1. Verify existing Vite dev server boots cleanly (`npm run dev`) with zero TypeScript errors.
2. Confirm Tailwind palette tokens in `tailwind.config.ts` and typography in `index.html`.
3. Set up data-access mock adapter (`frontend/src/lib/data-access/`) for offline fixture testing.
4. Verify `AuthContext.tsx` and Clerk provider configuration with fallback test credentials.

**Gate**: Does the Vite dev server start? Does Tailwind render a colored div? Done.

---

### PHASE 1 — Hours 1–4 (13:00–16:00)
**Your job**: Static Trip Home + Slot Detail UI against dummy data. NO real API calls yet.

Concrete deliverables:
1. Build all global components (Section 10): Button, Input, StatusPill, VotePill, Toast, Modal, TopNav, EmptyState
2. Build `TripHomeScreen` with dummy data (Section 11, Screen 6):
   - Route Line rendered with 3 dummy slots (CONFIRMED, IN_CONSENSUS, EMPTY)
   - Each slot renders an `ItinerarySlotCard`
   - Correct colors per slot status
   - Desktop two-column layout working
3. Build `ItinerarySlotCard` component with all visual states
4. Set up Clerk `<ClerkProvider>` in `main.tsx` with `VITE_CLERK_PUBLISHABLE_KEY`
5. Build `LoginScreen` and `SignUpScreen` with Clerk components
6. Set up React Router: routes for `/sign-in`, `/sign-up`, `/trips`, `/trips/:trpId`
7. Route Line draws correctly with dummy data — the visual centerpiece must look right

**Gate**: Can you see Trip Home screen with 3 slots, correct colors, Route Line connecting them? Done.

---

### PHASE 2 — Hours 4–8 (16:00–20:00)
**Your job**: Wire proposal/vote UI. Add live tally updates (still dummy WebSocket data).

Concrete deliverables:
1. Build `ProposeActivityModal` (Screen 7) with full form validation
   - `rationale` field labeled "Rationale" — NOT "description"
   - `costDelta` sent as string, NOT number
   - `entityType` dropdown with legal enum values
2. Build `VoteModal` (Screen 8):
   - Show proposal details + current vote tally
   - Vote Pill (YES green / NO red)
   - NO vote: mandatory comment textarea appears, submit blocked if empty
   - Error message on empty NO comment
3. Build `ConflictResolutionPanel` (Screen 9) with dummy AI data
4. Create `TripContext.tsx`:
   - State: `trip`, `setTrip`, `wsStatus`
   - Connects to WebSocket URL from env
   - Handlers for all 5 event types (update state accordingly)
   - Re-fetch trip on reconnect
5. Wire `MyTripsScreen` against dummy trips array
6. Build `CreateTripScreen` form (validation only, no API call yet)

**Gate**: Can you click "Vote NO", see the comment box appear, and be blocked from submitting without a comment? Done.

---

### PHASE 3 — Hours 8–12 (20:00–00:00)
**Your job**: Admin recommendation panel. AI Concierge Panel. Mode display.

Concrete deliverables:
1. Build `AIConciergePanel` component (Screen 9):
   - Shows blended plan vs. original
   - Round indicator in font-mono
   - Mode A admin controls (Accept/Force Branch/Extend) — gated to owner role only
   - Mode NA view (no controls, just info)
2. Mode A vs Mode NA gating throughout Trip Home:
   - Mode A: show admin controls to owner, show "Admin-Led" mode pill
   - Mode NA: show countdown timer (`[IMPLEMENTATION BEHAVIOR — DECISION PENDING: Product Sign-Off Required]`, 10-minute default) when `closesAt` is not null
3. Build `MyTripsScreen` properly with trip card grid
4. Build face registration 3-step flow (Screen 1, Step 3):
   - Photo capture UI (can use `<input type="file" accept="image/*" capture="user">`)
   - 3 slots: Straight, Left Tilt, Right Tilt
   - Skip button prominent
5. Build `AuditHistoryScreen` (Screen 12) with 3 tabs (dummy data)

**Gate**: Does Mode A trip show admin controls? Does Mode NA trip show countdown timer? Done.

---

### CHECKPOINT 1 — Hour 12 (00:00)
**STOP all development.** Merge `feature/frontend` into `develop`. Everyone does integration testing together.

**What must work**:
- Sign up → create trip → Trip Home loads with dummy data → click "Vote NO" → comment required → WebSocket toast fires on vote (can use dummy WS event)
- This is tested against real backend (Panchami's API should be live at this point)
- If backend isn't ready: keep dummy data, that's fine for Checkpoint 1

---

### PHASE 4 — Hours 12–16 (00:00–04:00)
**Your job**: Replace all dummy data with real API calls. Branch View.

Concrete deliverables:
1. Wire `lib/api.ts` with real fetch calls to all endpoints (Section 8)
2. Wire `MyTripsScreen` → `GET /api/trips`
3. Wire `TripHomeScreen` → `GET /api/trips/:trpId` on mount
4. Wire `ProposeActivityModal` → `POST /api/proposals`
5. Wire `VoteModal` → `POST /api/votes`
6. Wire real WebSocket in `TripContext` → `wss://{WS_BASE_URL}/ws/trips/{trpId}?token=${jwtToken}` (with fallback to `{trpId}/{usrId}` for current local dev)
7. Build `BranchViewScreen` (Screen 10):
   - Clay fork visual on Route Line
   - Branch cards with member avatars
   - Confirm / Request Modification buttons
   - Auto-resolved single-member branch badge
8. Wire `POST /api/branches/:brcId/confirm` and `POST /api/branches/:brcId/modify`
9. Handle `slotStatusChanged` → BRANCHED transition: show "View Branches" button on slot card

**Gate**: Two browser tabs, vote NO in one, see toast + tally update in other tab? Done.

---

### PHASE 5 — Hours 16–19 (04:00–07:00)
**Your job**: Solo Match screens. Trip Chat. Photos.

Concrete deliverables:
1. Build `SoloMatchScreen` (Screen 13):
   - Wire `POST /api/solo-matching/groups` → show GroupMatch cards with compatibility score
   - Wire `POST /api/solo-matching/guides` → show GuideMatch cards
   - Compatibility score displayed prominently in font-mono
2. Build `ChatDrawer` component (Screen 14):
   - Wire canonical `GET /api/trips/:tripId/chat` for message history
   - Wire canonical `POST /api/trips/:tripId/chat` for sending messages
   - Wire WebSocket for real-time new messages (handled via TripContext)
   - "Propose this as the plan" button ➔ `POST /api/chat/:msgId/propose`
   - Handle both unanimous (CONFIRMED toast) and non-unanimous (queued message) responses
3. Build `AuditHistoryScreen` Tab 3 (Trip Photos):
   - Wire `GET /api/photos/:trpId` for all photos
   - Add ?usrId= filter for "My Photos"
   - Show face registration gate message for unregistered users
4. Build `ResolvedItineraryScreen` (Screen 11)

**Gate**: Can you run solo match and see percentage scores? Does Trip Chat show messages in real time? Done.

---

### PHASE 6 — Hours 19–21 (07:00–09:00)
**Your job**: Full click-through. Flag bugs. Do NOT fix in isolation — coordinate with team.

Concrete deliverables:
1. Run the full demo script end to end in two browser windows
2. Fix any UI issues visible in the demo flow (layout, colors, wrong field names)
3. Verify all WebSocket events show correct UI updates (including `resyncSnapshot` on connect and `aiPlanGenerated` / `aiRecommendationReady`)
4. Verify compatibility scores display correctly (integer 0-100, font-mono)
5. Verify NO vote blocks on empty comment
6. Verify CONFIRMED slot shows Amber Route Line
7. Verify BRANCHED slot shows Clay fork
8. Verify Mode A admin controls only visible to owner

**Do NOT add new features after Hour 21.**

---

### CHECKPOINT 2 — Hour 21 (09:00)
**STOP.** Merge `feature/frontend` into `develop` → `main`. Feature freeze.

---

### PHASE 7 — Hours 21–24 (09:00–12:00)
**Your job**: Demo prep only.

1. Clean up any visible UI rough edges on the demo path ONLY
2. Seed demo trip is loaded and looking correct
3. Two browser windows positioned for dual-presenter demo
4. Rehearse the click-through twice
5. Record offline fallback video

---

