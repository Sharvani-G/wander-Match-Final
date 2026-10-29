# Product Requirements Document (PRD): WanderMatch

**Product**: WanderMatch — Social & Group Travel Planning with an AI Consensus Planner  
**Hackathon**: KogniVera Hackathon 2026 (Problem Statement PS-11, Travel & Tourism Theme)  
**Team**: Chaosminds — Nikitha (Frontend); Panchami (HTTP/WebSocket Transport and DeepFace); Sharvani (Business Logic, AI/Consensus, Authentication, Database, Integration and Deployment)
**Specification Status**: Updated Draft — Pending User Review  
**Canonical AI Specification Reference**: For exhaustive mathematical formulas, Pydantic schemas, edge-case test matrices, and the complete field validation matrix, consult the canonical [AI System Specification](AI.md).

---

## 1. Problem Statement

Group travel planning breaks down when participants disagree, nobody wants to block the group, and differing opinions are either steamrolled (forced through to avoid confrontation) or lost in chat back-and-forth (unstructured discussion leading to indecision).

WanderMatch combines a live shared itinerary, a structured proposal-and-vote flow, and an AI layer that reads the **reasons** behind objections (mandatory typed comments on `no` votes, rather than just a numerical tally) to synthesize common ground or, when preferences are genuinely incompatible, parallel branches.

**Core Governance Principle**: The AI never holds final authority over a trip. In Mode A (Admin-Led), the trip owner retains final decision authority, and AI outputs are strictly advisory recommendations. In Mode NA (Collaborative), consensus is governed by an automated workflow, but unanimous agreement or direct chat proposals can always short-circuit AI processing.

---

## 2. Target Users

1. **Group Trip Organizers (Trip Owners / Admins)**: Users initiating group travel who set destination and dates, keep decision-making moving forward, and retain final schedule authority in Mode A.
2. **Group Trip Members**: Participants in a group trip who want an equal voice, clear visibility into itinerary changes, and a structured mechanism to object and propose alternatives without interpersonal friction.
3. **Solo Travelers**: Individuals traveling alone seeking compatible group trips or local tour guides based on shared age groups, languages, interests, dates, and specializations.
4. **Local Tour Guides**: Professional or local guides listing their language capabilities, specializations, and daily rates to connect with solo travelers or groups.

---

## 3. Core User Stories

- **US-01 (Proposing an Activity)**: As a group trip member, I want to propose a new activity for a specific itinerary time slot with a rationale, cost_delta, and entity resolution (entity_type/entity_id), so that the group can evaluate my suggestion against our schedule.
- **US-02 (Voting with a Mandatory Reason)**: As a group trip member, I want to cast a binary `yes` or `no` vote on an active proposal, and be required to provide a typed comment when voting `no`, so that my specific objection or suggestion is captured for AI reconciliation.
- **US-03 (Seeing an AI Blended Compromise Plan)**: As a group trip member, I want the AI to generate a single blended activity plan that incorporates fixable typed `no` suggestions into the existing activity before any split occurs, so that the group can re-vote on a unified compromise.
- **US-04 (Early Branching for Hard Incompatibilities)**: As a group member with a genuine non-negotiable physical or medical constraint (e.g., severe injury, mobility limitation, or flight departure), I want the system to recognize my objection as a fixed requirement and initiate branching without forcing an implausible compromise plan or waiting out the standard voting timer.
- **US-05 (Preference-Driven Branch Assignment)**: As a dissenting group member whose preference is incompatible, I want to be grouped into a slot-specific parallel branch with others sharing similar preferences, where single-member branches auto-finalize and silent members default safely to the primary base plan (Track A).
- **US-06 (Short-Circuiting AI via Trip Chat Proposal)**: As a group trip member, I want to click the "Propose this as the plan" button on a message in the mandatory Trip Chat, so that if every applicable member votes `yes` in chat, the proposal is accepted immediately, terminating active AI consensus processing for that slot.
- **US-07 (Restoring an Earlier Milestone via Append-Only Reversion)**: As a trip organizer (Mode A) or group member (Mode NA), I want to restore an earlier confirmed milestone without erasing intermediate audit history, so that past plans can be restored safely as a new revision.
- **US-08 (Solo-to-Group Matchmaking & Privacy Discovery)**: As a solo traveler, I want to find eligible public group trips ranked by an explainable, deterministic compatibility score over age group, languages known, and travel interests, while keeping private trips strictly hidden from discovery.
- **US-09 (Solo-to-Guide Matchmaking)**: As a solo traveler, I want to find local tour guides ranked by an explainable compatibility evaluation over destination city, spoken languages, specialization, price, and rating, so that I can hire a compatible guide for my trip.
- **US-10 (Photo Memories & Face Segregation)**: As a trip member, I want the application's photo segregation system to automatically organize trip photos into All Photos, Member Albums, Group Photos, and Scenery & Landmarks; and as an individual traveler, I want the option to enroll reference photos of my face, with full graceful degradation if I opt out.
- **US-11 (Geospatial Feasibility & Evidence-Grounded Negotiation)**: As a group trip member proposing an excursion, I want the system to calculate real road-travel times, verify operating hours, check transit buffers before the next confirmed activity, and present structured negotiation alternatives if my proposal is unfeasible, so that our schedule remains realistic without silently erasing existing plans.
- **US-12 (Permission-Based Location & Transparent Accuracy)**: As a traveler looking for nearby activities, I want the app to explicitly request my location permission, provide a manual entry fallback if denied, and maintain my device location strictly separate from the group's shared itinerary origin.

---

## 4. Functional Requirements

### 4.1 Trip Privacy, Discovery, Capacity & Access Matrix

- **FR-PRV-01 (Four-Case Access Matrix)**: Trip discovery, joining, and membership authorization shall strictly adhere to the four combinations of governance mode and visibility:

| Trip Governance & Visibility | Discovery Visibility | Entry Mechanism | Approval & Capacity Rule |
| :--- | :--- | :--- | :--- |
| **Mode A + Private** | Hidden from public search and Solo Match discovery | Valid secret 8-character invite code | **Instant join**: Possession of valid invite code acts as pre-authorization. Capacity capped at `party_size`. |
| **Mode A + Public** | Eligible for public search and Solo Match discovery | "Request to Join" button | **Admin approval required**: Creates pending join request; Admin must explicitly approve; Reject if active members reach `party_size`. |
| **Mode NA + Private** | Hidden from public search and Solo Match discovery | Valid secret 8-character invite code | **Instant join as editor**: Possession of valid invite code acts as pre-authorization. Capacity capped at `party_size`. |
| **Mode NA + Public** | Eligible for public search and Solo Match discovery | "Join Trip" button | **Instant join as editor**: Allowed immediately if user meets compatibility and active members are below `party_size`; displays "Trip Full" when capacity reached. |

- **FR-PRV-02 (Default Privacy)**: Every newly created trip shall default to **Private** (`visibility = 'private'`) unless the creator explicitly publishes it as Public.
- **FR-PRV-03 (Invite Code Pre-Authorization & Open Policies)**:
  - For all private trips (Mode A and Mode NA), possession and submission of a valid, active 8-character invite code constitutes pre-authorization to join. No subsequent administrator approval step shall be required for private invite-code holders.
  - *Open Product Decision*: The lifecycle policies for invite codes (automatic expiration after $N$ days, owner-initiated code revocation, or regenerating a new code) are not yet formalized in the MVP schema and remain an open product decision.
- **FR-PRV-04 (Server-Side Privacy Enforcement)**: Private trips shall never be returned in public discovery queries, solo matchmaking feeds, or unauthenticated API endpoints. Direct URL navigation to private trip itineraries shall be blocked for non-members with an authorization error.
- **FR-PRV-05 (Strict Capacity Enforcement Across All Paths)**: Every trip defines a maximum group capacity (`party_size`). The system shall enforce this limit server-side across all entry paths (including private invite codes). Under concurrent join attempts, requests shall be rejected when active members equal or exceed `party_size`.
- **FR-PRV-07 (Permission-Based Personal Location vs. Shared Group Itinerary Origin)**:
  - Personal nearby discovery requires explicit user click on "Use my current location" and user browser/device permission grant. Background location tracking is strictly prohibited. If denied, a manual text input is provided.
  - The shared group itinerary origin is strictly defined as the immediately preceding itinerary activity (or confirmed hotel base for the day's first slot). An individual member's device GPS must never alter or move the group itinerary origin.
- **FR-PRV-06 (Membership Lifecycle States)**: The system shall distinguish between:
  1. *Discovering a trip* (viewing a public trip card in Solo Match),
  2. *Requesting to join* (submitting a join request for a public Mode A trip; row created in `join_requests` with status `pending`),
  3. *Being approved / rejected* (administrator decision on a pending request),
  4. *Joining via invitation* (submitting a valid 8-character invite code for instant entry), and
  5. *Active member* (persisted in `trip_members` with assigned canonical role `owner`, `editor`, or `viewer`).

### 4.2 Governance Modes & Base Itinerary Permissions

- **FR-GOV-01 (Mode A — Admin-Led Authority Boundary)**:
  - In Mode A, the Trip Owner (`owner` role) has exclusive authority to directly create, edit, reorder, or delete base itinerary schedule items.
  - Non-admin members (`editor` or `viewer` role) cannot directly mutate base itinerary items; they must submit proposals (`prp_`) or discuss in Trip Chat.
  - **AI is Strictly Advisory**: In Mode A, the AI consensus engine produces recommendations only (`advisory: true`). Even when the AI detects a fixed incompatibility or the round limit is reached, it **must not** silently or automatically execute a binding branch. The admin retains sole authority to accept the recommendation, reject it, extend the round, or manually force-branch the slot.
- **FR-GOV-02 (Mode NA — Collaborative Automatic Authority)**:
  - In Mode NA, all members with `owner` or `editor` role have equal governance rights to create baseline items, submit proposals, and vote.
  - Consensus is automated: the system automatically triggers AI blending or branching based on defined voting thresholds, fixed-incompatibility rules, or round caps, without requiring administrator sign-off.
- **FR-GOV-03 (Itinerary Optimistic Concurrency Control)**: The system maintains a shared itinerary per trip backed by the authoritative database, using monotonic versioning on the itinerary header (`itineraries.version` incrementing on edit, never overwriting) to detect concurrent write conflicts.
- **FR-GOV-04 (Proposal Data Contract)**: Proposals (`prp_` prefix) attached to an itinerary item (`itm_`) shall store `rationale` (not description) and `cost_delta` (not estimated_cost). Location resolution shall pass through `entity_type` (e.g. `'city'` or `'poi'`) and `entity_id` (e.g. `'cty_123'`), never a free-text location column.
- **FR-GOV-05 (Canonical Slot Statuses)**: Itinerary slot status shall strictly use the canonical 4-value list:
  1. `EMPTY`: Unassigned or placeholder slot (Slate `#6B7280`),
  2. `IN_CONSENSUS`: Active proposal undergoing voting, AI blending, or objection reconciliation (Route `#2F6F6B`),
  3. `BRANCHED`: Parallel tracks generated due to incompatible preferences (Clay `#C1502E`),
  4. `CONFIRMED`: Plan locked by unanimous agreement, non-dissent, or admin approval (Amber `#E1A93A`).

### 4.3 Voting Engine & Silence Semantics

- **FR-VOT-01 (Binary Voting Only)**: A vote's `value` field shall accept strictly `'yes'` or `'no'`. Abstentions are invalid application votes. The database column `votes.weight` remains UNUSED for the MVP.
- **FR-VOT-02 (Mandatory Reason on NO Votes)**: A `no` vote submission shall be rejected by API validation if the `comment` field is empty or contains only whitespace. The AI reads the typed comment string exactly as submitted without conversational follow-up questions.
- **FR-VOT-03 (Server-Side Single Active YES Guarantee)**: A member shall hold at most ONE active `yes` vote per itinerary slot at any time. Casting a `yes` on an alternative proposal for the same slot atomically retracts any previous active `yes` vote held by that user in that slot. Retracting a `yes` vote simply removes or deactivates that `yes`; it must **never** synthesize a `no` vote or add a dissent comment.
- **FR-VOT-04 (Three Stages of Silence)**: Silence (non-voting) carries distinct, unambiguous meanings depending on the planning stage:
  - **Stage 1 (Undisputed Baseline Itinerary)**: Silence implies agreement and passive consent. An initial, uncontested baseline activity remains `CONFIRMED` without forcing members to vote. No countdown timer or artificial dissent cycle is triggered on peaceful slots.
  - **Stage 2 (Active Contested Voting Window)**: During an active consensus round, non-voters are treated as non-voters (not automatically counted as YES). Silence does NOT block or delay the Mode NA timer (`[IMPLEMENTATION BEHAVIOR — DECISION PENDING: Product Sign-Off Required]`, currently 10 minutes in code) from expiring. At timer expiration, reconciliation proceeds based on active votes cast.
  - **Stage 3 (Branch Assignment)**: When a slot branches, silent members who expressed no preference default to the primary base-plan branch (Track A). They are never stranded without an itinerary and never labeled as objectors. They receive an on-screen option to switch to an alternative branch later.

### 4.4 AI Consensus Lifecycle & Objection Reconciliation

- **FR-CON-01 (Authoritative Slot-Level Timer Lifecycle in Mode NA)**:
  - In Mode NA, exactly one authoritative voting deadline (`[IMPLEMENTATION BEHAVIOR — DECISION PENDING: Product Sign-Off Required]`, currently 10 minutes in code) governs a contested itinerary slot during a given consensus cycle.
  - The timer does NOT start upon proposal creation.
  - The timer does NOT run on uncontested baseline items.
  - The timer starts immediately when the **first `no` vote** lands on any proposal belonging to that slot and cycle.
  - All competing proposals for that slot and cycle share this single authoritative deadline.
  - In Mode A, there is no automatic 10-minute countdown; the administrator controls decision timing.
- **FR-CON-02 (Reconciling Early Branching with the Ten-Minute Timer)**:
  - In Mode NA, when the first NO vote lands, the 10-minute countdown begins.
  - The objection classifier evaluates the objection comment.
  - **Fixed-Incompatibility Exception**: If the classifier reliably identifies a fixed, non-negotiable physical or medical constraint (e.g., severe injury, wheelchair requirement, or absolute geographical conflict), the system may initiate early branching immediately under this approved exception without waiting for the 10-minute timer to elapse or forcing an implausible compromise plan.
  - **Fixable Tweaks**: If the objection represents negotiable preferences (e.g., timing, budget, activity style), the voting window remains open for its full 10-minute duration. At expiry, the engine reconciles all proposals and votes, synthesizing exactly ONE blended compromise plan.
  - Mode A never inherits automatic timer expiration or automatic branching authority from the shared classifier.
- **FR-CON-03 (Constraint Pre-Validation)**: Every generated blended plan must be validated against hard constraints (timing bounds, slot duration, geographical distance, transit feasibility, and return feasibility for evening regrouping) before presentation to users. If validation fails, it is regenerated once; if it fails a second time, the system escalates directly to branching (Mode NA) or flags the failure for admin review (Mode A).
- **FR-CON-04 (Three-Round Consensus Soft Cap)**: Re-voting on blended compromises is limited to a maximum of 3 rounds per consensus cycle:
  - *Round 1*: Initial proposal receives objections; first blended plan is generated.
  - *Round 2*: Group votes on the first blended plan; persistent objections generate second blended plan.
  - *Round 3*: Group votes on the second blended plan. If unresolved after the Round 3 window closes, further blending stops and branching occurs (Mode NA) or branching is recommended to the admin (Mode A).
- **FR-CON-05 (Slot-Specific Branching Scope)**: Branching is strictly scoped to the specific contested activity slot. Parallel branches reunite at the subsequent itinerary slot or next morning without splitting the overall trip.
  - **FR-CON-06 (Multi-Leg Temporal & Geospatial Route Feasibility)**:
    - Every proposed activity must be validated across both route legs: (1) previous activity to candidate, and (2) candidate to next confirmed commitment.
    - Road distances and travel times must be derived from topological road network data (e.g., OSRM), never straight-line distance.
    - Each leg must satisfy mandatory transition and assembly buffers ($B_{	ext{arr}} \ge 15	ext{ min}$, $B_{	ext{dep}} \ge 15	ext{ min}$).
    - The system must never silently shorten, shift, or discard a subsequent confirmed commitment to accommodate a proposal.
  - **FR-CON-07 (Evidence-Grounded Negotiation Contract)**:
    - If a candidate violates scheduling or distance bounds, the AI must not emit a generic rejection.
    - It must generate an evidence-grounded negotiation payload explaining exact road distances and missing time windows, accompanied by structured options (e.g., keep baseline, choose a verified closer alternative, or request an explicit admin/group vote to reschedule the next activity).
  - **FR-CON-08 (Six-Tier Verification Statuses & Uncertainty Disclosure)**:
    - AI proposals and route calculations must report one of six standard verification statuses: `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `NEEDS_CLARIFICATION`, `INFEASIBLE`, or `BLOCKED`.
    - If real-time road closure or traffic data is unavailable, the UI must display an honest uncertainty disclaimer (`PARTIALLY_VERIFIED`), preventing ungrounded claims of verified access.

### 4.5 Multi-Way Recursive Branching & Group Assignment

- **FR-BRN-01 (Preference-Driven Multi-Way Grouping)**: Branching shall group members strictly by shared stated preferences and compatibility, never as a punitive measure or "troll tag".
- **FR-BRN-02 (Uncapped Branches & Duplicate Merging)**: The system supports two, three, or more parallel branches per slot if supported by distinct preferences. Near-duplicate preferences are automatically clustered into a single branch.
- **FR-BRN-03 (Single-Member Auto-Finalization)**: A branch containing exactly one member is marked `auto_finalized = true` (`status = 'FINALIZED'`) without requiring a vote, adopting the member's proposed suggestion directly.
- **FR-BRN-04 (Recursive Sub-Branching)**: If a multi-member branch experiences internal disagreement in subsequent rounds, it can recursively fork via a `parent_branch_id` self-reference.
- **FR-BRN-05 (Mode A Manual Force-Branch)**: In Mode A, the administrator retains final authority to trigger a manual force-branch at any time, overriding advisory AI flows.

### 4.6 Revision History & Mode-Specific Restoration

- **FR-REV-01 (Append-Only History Rule)**: Reverting an itinerary slot to an earlier version shall NEVER delete, overwrite, or truncate historical revision records. Restoring an earlier milestone creates a brand new revision snapshot in `revision_history` with the next monotonic `version_number` (e.g., restoring Version 1 while Version 3 is active creates Version 4 containing Version 1's plan data).
- **FR-REV-02 (Mode A Admin Reversion)**: In Mode A, ONLY the Trip Owner/Admin has permission to execute a direct 1-click restore of an earlier itinerary version. Non-admin members may suggest restoration in Trip Chat or via proposal.
- **FR-REV-03 (Mode NA Collaborative Reversion & Majority Threshold)**:
  - In Mode NA, any member may submit a restoration proposal referencing an earlier milestone.
  - *Open Product Decision on Majority Denominator*: Whether a proposal's rejection or approval is calculated against total votes cast by active voters during the window or against all eligible trip members is currently an open product decision. Provisionally, the system evaluates consensus based on active votes cast within the 10-minute window.
  - If a restoration proposal is approved, the slot reverts to the milestone as a new revision. If a replacement proposal fails, the slot safely snaps back to the prior confirmed milestone.

### 4.7 Mandatory Trip Chat & Unanimous Override

- **FR-CHT-01 (Real-Time Communication)**: Every trip features an always-on, real-time Trip Chat backed by `trip_chat_messages` (`msg_` prefix) independent of the AI consensus engine.
- **FR-CHT-02 (Unanimous Chat Proposal Override)**: Clicking "Propose this as the plan" on a chat message triggers an in-chat vote. If all applicable members vote `yes`, the slot status immediately transitions to `CONFIRMED`, and all active AI consensus and branching processes for that slot are terminated immediately. If majority but non-unanimous, it enters the standard proposal queue for the next cycle.

### 4.8 Solo Matchmaking & Tour Guide Discovery

- **FR-MCH-01 (Deterministic Solo-to-Group Compatibility)**: Solo-to-group matchmaking calculates an explainable 0–100% compatibility score based strictly on:
  $$\text{Group Score} = 0.45 \times \text{Jaccard Interest Similarity} + 0.35 \times \text{Language Match} + 0.20 \times \text{Age Bracket Compatibility}$$
  Date overlap acts as a pre-filtering eligibility constraint. The calculation is deterministic and does not invoke a generative LLM call.
- **FR-MCH-02 (Tour Guide Discovery)**: Solo travelers can search local guides (`tour_guides` table) filtered by destination city (`tour_guides.city_id`), spoken languages (`user_preferences.preferred_languages` vs. `tour_guides.languages`), primary and secondary specializations, maximum daily budget rate with currency compatibility (`user_preferences.max_daily_budget` vs. `tour_guides.day_rate`, requiring `user_preferences.max_daily_budget_currency == tour_guides.currency`), and review ratings (`tour_guides.rating`). The group matching formula must **never** be applied to tour guides, and guide-scoring mathematical weights remain an open product decision awaiting approval.

### 4.9 Photo Memories & Face Segregation (Required Application Capability; Individual Enrollment Optional)

- **FR-MEM-01 (Four Gallery Categories)**: The shared trip photo gallery organizes uploaded media into four distinct views:
  1. `All Photos`: Chronological master gallery of all media uploaded to the trip.
  2. `Member Albums`: Photos containing a recognized registered trip member.
  3. `Group Photos`: Photos containing at least two recognized registered trip members.
  4. `Scenery & Landmarks`: Photos where zero faces are detected.
- **FR-MEM-02 (Unrecognized Detected Faces Rule)**: If a photo contains detected faces but none match registered trip members above the confidence threshold, it shall NOT be classified as "Scenery & Landmarks" (since faces are present). It remains in `All Photos` and is flagged as "Unknown Guest / Unregistered".
- **FR-MEM-03 (Optional Traveler Enrollment & Required Application Capability)**: The photo-segregation capability is a required WanderMatch application feature. For individual travelers, reference photo enrollment is optional (travelers may opt out of biometric tagging). Users who choose to enroll provide 3 reference photos (straight, left tilt, right tilt). Facial embedding data is logically represented as a 512-dimensional vector. In the current prototype schema, storage as `JSONB` in `face_profiles.embedding_data` is an illustrative and provisional physical representation only; the final storage format and indexing approach remain open for stack verification and database review. The core trip planning, voting, and chat experiences function completely without face registration.

---

### 4.10 Master Field Validation & Accessible Error Contract

- **FR-VAL-01 (Authoritative Master Field Validation)**: Every form field across trip setup, itinerary slot editing, proposal submission, voting comments, and onboarding profiles must adhere to explicit validation bounds defined in the Master Field Validation Matrix (see canonical `docs/AI.md` Section 6). Empty strings, invalid enums, out-of-bound party sizes (party size >= 2 [APPROVED_CONTRACT]; proposed upper bound <= 50 pending review [PROPOSED_PENDING_REVIEW]), negative costs, and end-dates before start-dates are rejected.
- **FR-VAL-02 (Monetary Data Integrity)**: All prices, budgets, and cost deltas must be stored as `DECIMAL(12,2)` paired with an ISO-4217 currency code. Floating-point arithmetic and cross-currency comparisons without approved rates are prohibited.
- **FR-VAL-03 (Accessible Visible Form Error States)**: Invalid fields must display a visible red/clay outline (`border-clay`), inline descriptive error text, `aria-invalid="true"`, and automatic focus on submission failure. Backend validation independently repeats all checks.

---

## 5. Explicit Non-Goals

1. **Multilingual UI**: English-only interface for MVP (language preferences used for matchmaking only).
2. **Admin-Inactivity Auto-Fallback**: In Mode A, no automatic mode transition if the admin is idle.
3. **Custom-Managed Production GPU Cluster**: Standardized OpenAI-compatible inference endpoints (with local Ollama as development/evaluation candidate; production cloud/hosted provider undecided [PENDING]) used for consensus generation rather than building and managing an in-house GPU cluster.
4. **Live Bulk Face Recognition During Demo**: Bulk matching pre-processed; live single-user enrollment capture demoed.
5. **AI Conversational Follow-Up**: The AI never prompts users with clarifying questions; typed comments are processed as submitted.
6. **Harmful Troll Labeling**: Grouping algorithms cluster by stated preferences, never labeling users as blockers or trolls.
7. **Weighted Voting / Harmony Score**: Harmony Score is deprecated. `votes.weight` exists in DB schema but is strictly unused.

---

## 6. Observable Acceptance Criteria Matrix

| Requirement Area | Acceptance Criteria ID | Observable Behavioral Verification |
| :--- | :--- | :--- |
| **Privacy Isolation** | `AC-PRD-01` | Private trips never appear in `/api/trips/discover` or Solo Match search. Direct unauthenticated GET request to private trip returns `404 Not Found` or `403 Forbidden`. |
| **Invite Pre-Auth** | `AC-PRD-02` | Submitting a valid 8-character invite code for a private Mode A or Mode NA trip immediately adds the user to `trip_members` without requiring admin approval, provided capacity remains. |
| **Capacity Cap** | `AC-PRD-03` | Attempting to join a trip where active `trip_members` count equals `party_size` fails with HTTP 400 `"Trip has reached maximum capacity"`, across both invite-code and join-request paths. |
| **Mode A Authority** | `AC-PRD-04` | In Mode A, AI generates branching recommendations with `advisory: true`. No automatic branching occurs upon fixed incompatibility or round cap until admin invokes accept or force-branch. Non-admin direct edit returns HTTP 403 Forbidden. |
| **Single Active YES**| `AC-PRD-05` | User voting `yes` on Proposal B for slot `itm_1` while holding active `yes` on Proposal A results in Proposal A vote retracted and Proposal B vote recorded in same transaction. No synthetic `no` vote is generated. |
| **Mandatory NO Reason**| `AC-PRD-06` | Casting `no` vote with empty comment returns HTTP 400 `"A 'no' vote REQUIRES a typed reason or suggestion in the comment field."` |
| **Slot Timer Start** | `AC-PRD-07` | In Mode NA, slot countdown timer remains inactive on creation; starts 10-minute countdown only upon arrival of first `no` vote on that slot. |
| **Early Branching Exception** | `AC-PRD-08` | In Mode NA, a `no` comment containing a fixed physical constraint (e.g. `"broken leg, cannot hike"`) initiates early branching without waiting 10 minutes or generating a forced compromise. |
| **Silent Member Track**| `AC-PRD-09` | When a slot branches, members who did not vote are assigned to Track A (Base Plan) with an on-screen switch option. |
| **Single Member Auto**| `AC-PRD-10` | A branch containing exactly one member is set to `status = 'FINALIZED'` with `auto_finalized = true` without triggering a vote. |
| **Append-Only Revert**| `AC-PRD-11` | Restoring Version 1 creates Version 4 with identical content; Versions 1, 2, and 3 remain intact in `revision_history`. `itineraries.version` increments monotonically. |
| **Photo Segregation**| `AC-PRD-12` | Uploaded photo with 0 faces lands in `Scenery & Landmarks`. Photo with 2 registered members lands in `Group Photos`. Photo with unknown faces stays in `All Photos` only and is never misclassified as Scenery. |
| **Multi-Leg Route Feasibility** | `AC-PRD-13` | Candidate activity requiring 1h 20m road drive when available window before next confirmed activity is 1h 00m is flagged `INFEASIBLE`. Subsequent confirmed activity is never silently removed. |
| **Grounded Negotiation** | `AC-PRD-14` | Infeasible excursion proposal returns structured negotiation response presenting exact road duration, available window, and 3 explicit options (keep baseline, closer alternative, or admin reschedule). |
| **Location Permission & Origin** | `AC-PRD-15` | Personal nearby search prompts explicit device permission with manual address fallback. Shared group planning uses preceding slot location as origin regardless of individual member GPS. |
| **Accessible Form Errors** | `AC-PRD-16` | Submitting proposal with empty rationale or invalid cost format highlights field in clay red with inline error text, sets `aria-invalid="true"`, focuses the field, and blocks API submission. |
