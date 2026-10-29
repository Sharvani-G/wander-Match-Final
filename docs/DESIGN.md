# UI/UX Design Specification Document: WanderMatch

**Specification Status**: Updated Draft — Pending User Review


**Product**: WanderMatch — Social & Group Travel Planning with an AI Consensus Planner  
**Hackathon**: KogniVera Hackathon 2026 (Problem Statement PS-11, Travel & Tourism Theme)  
**Team**: Chaosminds — Nikitha (Frontend); Panchami (HTTP/WebSocket Transport and DeepFace); Sharvani (Business Logic, AI/Consensus, Authentication, Database, Integration and Deployment)

---

## 1. Locked Visual System Reference

### 1.1 Rationale
WanderMatch replaces cold, generic SaaS aesthetics with the tactile warmth of a **paper travel journal crossed with a transit map**. This evokes the excitement of journey planning, structured stop sequences, and clear route choices without resorting to travel clichés (e.g. palm trees, airplanes, neon gradients, or glassmorphism).

### 1.2 Color Palette
- `Paper` `#F7F5F0`: Canvas & Main Background (Warm, tactile paper tone).
- `Ink` `#14213D`: Primary Headings & High-contrast Text (Rich dark ink).
- `Route` `#2F6F6B`: Brand, Primary Buttons, Active States (Deep forest transit route teal).
- `Route Dark` `#204B48`: Button Hover & Pressed States.
- `Amber` `#E1A93A`: Confirmed & Unanimous Success States ONLY (Warm gold transit line).
- `Clay` `#C1502E`: Conflict & Branching States ONLY (Terracotta alert line, never decorative).
- `Slate` `#6B7280`: Secondary Text, Labels, & Subtitles.
- `Slate Light` `#E4E1DA`: Borders, Dividers, & Card Outlines.
- `Card` `#FFFFFF`: Surface Backgrounds (Clean white paper cards).

### 1.3 Typography
- **Headings & Trip Titles**: `Fraunces` (Editorial serif with character).
- **UI Labels & Body Text**: `Inter` (Clean, highly readable sans-serif).
- **Data, Times, Counts, & Percentages**: `IBM Plex Mono` (Structured transit schedule font).

### 1.4 Geometry & Radii
- **Cards & Buttons**: `10px` border-radius (`rounded-[10px]`).
- **Input Fields & Textareas**: `8px` border-radius (`rounded-[8px]`).
- **Shadows**: Subtle `0 1px 3px rgba(20, 33, 61, 0.04)` (No heavy drop shadows or glass blur).

### 1.5 The Signature Route Line
The **Route Line** is a vertical/horizontal dashed sequence line connecting itinerary stops. It is used **only** on Trip Preview, Trip Home, and Resolved Itinerary views:
- Default / Pending: Dashed `Slate Light` `#E4E1DA`.
- Confirmed / Reconverged: Rejoins in `Amber` `#E1A93A`.
- Branching / Conflict: Forks into parallel lines in `Clay` `#C1502E`.

---

## 2. Global Component Library

1. **Top Nav Bar**: Persistent header with WanderMatch logo, section tabs (Itinerary, Solo Matchmaker, Trip Photos), Mode indicator pill (`Mode A (Admin)` / `Mode NA (Collab)`), live presence avatars, Trip Chat toggle button, and multi-user switcher profile dropdown.
2. **Itinerary Slot Card**: Container card for an itinerary time slot showing time badge, title, entity resolution (city/POI), cost, status pill (`EMPTY`, `IN_CONSENSUS`, `BRANCHED`, `CONFIRMED`), active vote tally, and a "Vote / Review" button.
3. **Proposal Card**: Nested card inside slot details displaying proposal title, rationale, creator avatar, cost_delta, and vote breakdown.
4. **Vote Pill**: Interactive binary action button pair: `YES (Approve)` in `Route` `#2F6F6B` and `NO (Object)` in `Clay` `#C1502E`.
5. **Suggestion Chip**: Compact tag displaying typed objection comments or preferred alternatives (e.g. `"Hot springs spa instead"`).
6. **AI Concierge Panel**: Highlighted card displaying AI blended plan reconciliations, explanation notes, and hard constraint status.
7. **Branch Tabs / Fork View**: Side-by-side or stacked branch cards displaying forked activity options with member avatar badges and single-member auto-resolution tags.
8. **Primary Button**: `bg-route` (`#2F6F6B`), `text-paper` (`#F7F5F0`), `rounded-[10px]`, `font-sans font-medium`, hover state `bg-route-dark` (`#204B48`).
9. **Secondary Button**: `bg-paper` (`#F7F5F0`), `text-ink` (`#14213D`), `border border-slate-light` (`#E4E1DA`), `rounded-[10px]`.
10. **Input Field**: `bg-paper` (`#F7F5F0`), `border border-slate-light` (`#E4E1DA`), `rounded-[8px]`, `px-3 py-2 text-sm text-ink focus:border-route`.
11. **Status Dot / Pill**: Circular status indicator: `Amber` for Confirmed, `Route` for In Consensus, `Clay` for Branched, `Slate` for Empty.
12. **Toast Notification**: Lightweight slide-in card anchored at top-right for real-time WebSocket updates (`voteCast`, `slotStatusChanged`).
13. **Modal Window**: Centered overlay with backdrop blur, white `Card` container (`rounded-[10px]`), and explicit close button.
14. **Empty State Block**: Centered paper container with mono subtitle, calm editorial message, and single primary call-to-action button.

---

## 3. Screen-by-Screen Specifications

### 3.1 Sign Up Screen (with Preferences & Optional Face Registration)
- **Purpose**: Authenticate user via Clerk and collect initial travel preferences & optional face registration.
- **Layout**: Centered paper card layout. Step 1: Account credentials. Step 2: Interactive preference chips (Age group, BCP-47 languages, interests). Step 3: Optional 3-photo face capture (Straight, Left Tilt, Right Tilt) with skip button.
- **Components**: `Input Field`, `Primary Button`, `Secondary Button`, `Suggestion Chip`.
- **States**: Default, Loading, Error ("Quality check failed: exactly one face required per photo").
- **Dummy Data**:
  ```json
  {
    "usrId": "usr_new_01",
    "email": "user@example.com",
    "fullName": "Jordan Lee",
    "ageGroup": "25-34",
    "preferences": {
      "languages": ["en", "es"],
      "interests": ["Culture", "Foodie", "Hiking"]
    },
    "faceRegistered": false
  }
  ```

### 3.2 Log In Screen
- **Purpose**: Authenticate existing user.
- **Layout**: Clean paper card with WanderMatch logo, email/password fields, and Clerk social login.
- **Components**: `Input Field`, `Primary Button`, `Secondary Button`.

### 3.3 My Trips Screen
- **Purpose**: Display all trips the user belongs to as owner, editor, or viewer.
- **Layout**: Grid of trip cards with destination cover image, dates, mode pill (`Mode A` / `Mode NA`), and role badge.
- **Dummy Data**:
  ```json
  [
    {
      "trpId": "trp_bali_2026",
      "title": "Bali Tropical Escape & Cultural Journey",
      "destinationCity": "Bali",
      "destinationCountry": "Indonesia",
      "startDate": "2026-10-10",
      "endDate": "2026-10-16",
      "mode": "Mode A",
      "ownerId": "usr_nikitha",
      "role": "owner"
    }
  ]
  ```

### 3.4 Create Trip / Discover Screen
- **Purpose**: Initiate a new group trip or discover existing trips/guides.
- **Layout**: Tabbed view: "Create Group Trip" form on left, "Discover Solo Matches" on right.

### 3.5 Trip Preview Screen
- **Purpose**: Landing preview for invited members before joining.
- **Layout**: Read-only Route Line timeline preview with destination overview.

### 3.6 Trip Home Screen (with Signature Route Line)
- **Purpose**: Main workspace for group itinerary collaboration.
- **Layout**: Hero banner with destination/dates, active presence bar, and vertical **Route Line** timeline connecting morning, afternoon, evening, and night slots.
- **Dummy Data**:
  ```json
  {
    "trpId": "trp_bali_2026",
    "title": "Bali Tropical Escape",
    "mode": "Mode A",
    "version": 3,
    "items": [
      {
        "itmId": "itm_b1",
        "timeSlot": "Morning",
        "title": "Sacred Monkey Forest",
        "status": "CONFIRMED",
        "cost": 25.0
      },
      {
        "itmId": "itm_b2",
        "timeSlot": "Afternoon",
        "title": "Mount Batur Trek",
        "status": "IN_CONSENSUS",
        "cost": 65.0
      }
    ]
  }
  ```

### 3.7 Propose Activity Screen / Modal
- **Purpose**: Submit a new activity proposal for an itinerary slot.
- **Layout**: Modal form requesting title, rationale (not description), entity resolution (`entity_type`/`entity_id`), cost_delta ($), and currency code.

### 3.8 Vote States inside Slot Detail Modal
- **Purpose**: Review active proposal and cast binary `yes` or `no` vote.
- **Layout**: Top proposal details -> middle group vote tally -> bottom vote form with binary `YES`/`NO` pills and mandatory comment text box when `NO` is selected.

### 3.9 Conflict Resolution / AI Concierge Panel
- **Purpose**: Review AI blended plan recommendations or branch options.
- **Layout**: Highlighted panel displaying original vs blended activity and Mode A admin override buttons ("Accept Blended Plan", "Force Branch Now", "Extend Round").

### 3.10 Branch View + Mandatory Trip Chat
- **Purpose**: View forked activity branches and engage in trip chat.
- **Layout**: Split view: Left side displays parallel branch cards connected to Clay Route Line forks; Right side displays persistent Trip Chat drawer with "Propose this as the plan" message action button support.

### 3.11 Resolved Itinerary Screen
- **Purpose**: Finalized trip schedule view.
- **Layout**: Clean sequence timeline with all stops highlighted in `Amber` `#E1A93A` and branch reconvergence markers.

### 3.11.1 Itinerary PDF Print & Export Layout Design Specification
`[APPROVED_REQUIREMENT]`
To ensure printed itineraries maintain the tactile, editorial character of WanderMatch while functioning reliably in physical travel contexts:
1. **Canvas & Print Contrast**: Canvas defaults to pure white (`#FFFFFF`) to conserve physical ink. Text renders in Ink `#14213D` for maximum legibility. Card borders use subtle Slate Light `#E4E1DA`.
2. **Typography Hierarchy**:
   - Trip Title & Day Headings: `Fraunces` serif (Bold, elegant editorial styling).
   - Activity Names & Details: `Inter` UI sans-serif (Clean, readable at small print sizes).
   - Times, Durations & Coordinates: `IBM Plex Mono` (Tabular, precise alignment).
3. **Pagination & Page Break Safety**:
   - Activity cards and day tables enforce `page-break-inside: avoid` (`break-inside: avoid`) to prevent awkward splits across pages.
   - Running headers and footers display Trip Name, Date, Page X of Y, and Itinerary Version.
4. **Status Badges & Draft Watermark**:
   - Official confirmed plans render a restrained Route Dark `#204B48` confirmation seal.
   - Provisional or draft itineraries render a prominent 45-degree diagonal watermark across each page: `PROVISIONAL DRAFT — NOT CONFIRMED` (Slate `#6B7280` at 15% opacity).
5. **Transit & Non-Fabrication Rule**:
   - Verified road durations render with a car/bus icon.
   - Missing or unverified transit times render as em-dash (`—`), never a fabricated straight-line estimate.

### 3.12 Audit History / Members / Memories / Notifications Screen
- **Purpose**: Audit trail, member list, and trip photo gallery.
- **Layout**: Tabbed view: "Audit Log" (version history), "Members", and "Trip Photos" (All vs registration-gated "My Photos" view).
- **Registration Gating Message**: `"Register your face profile to view your auto-sorted personal trip photos."`

---

## 4. Responsive Rules

- **Mobile View (`< 768px`)**:
  - Single-column layout with full-width slot cards.
  - Primary action buttons anchored at the bottom of the viewport in a fixed bar (`sticky bottom-0`).
  - Trip Chat renders as a full-screen drawer overlay when opened.
  - No intermediate two-column layout between mobile and desktop.
- **Desktop View (`>= 768px`)**:
  - Two-column main workspace: Left/Center column contains Itinerary Timeline with Route Line (`max-w-4xl`); Right column contains persistent collapsible Trip Chat rail (`w-80` or `w-96`).

---

## 5. Accessibility & Animation Rules

1. **Visible Focus Rings**: All interactive elements (buttons, inputs, pills, tabs) must feature a visible `2px` focus outline in `Route` `#2F6F6B` when navigated via keyboard (`focus-visible:ring-2 focus-visible:ring-route`).
2. **Color Contrast & Signals**: Color is never used as the sole signal. Status states pair color (`Amber`, `Route`, `Clay`) with explicit icons (`CheckCircle`, `Vote`, `GitFork`) and text labels ("Confirmed", "In Consensus", "Branched").
3. **Minimum Touch Targets**: All touchable elements have a minimum height/width of `44px x 44px` on mobile devices.
4. **Motion Controls**: The Route Line draw-in sequence animation strictly respects `prefers-reduced-motion: reduce`, disabling smooth path transitions when reduced motion is requested.

---

## 6. AI Consensus, Verification Status & Feasibility Presentation

> **Canonical System Specification**: All visual statuses, negotiation flows, and form error states in this section directly implement the contracts defined in canonical [AI.md](AI.md) (and [ai/AIConsensus/docs/AI.md](AI.md)).

### 6.1 Verification Status Badges (The 6 AI Feasibility States)
To ensure transparency and eliminate AI hallucinations from misleading travelers, all AI-generated blended plans, POI suggestions, and schedule changes display one of six explicit status badges:

| Status Code | Visual Accent | Icon | Label Text | UI Meaning & User Guidance |
| :--- | :--- | :--- | :--- | :--- |
| `VERIFIED` | Green (`#15803D`, border `#86EFAC`, bg `#DCFCE7`) | `CheckCircle` | `Verified Route & Schedule` | Both legs verified against road-network coordinates; satisfies arrival/departure buffers ($B_{arr}, B_{dep} \ge 15\text{m}$). Safe to enter voting. |
| `PARTIALLY_VERIFIED` | Slate (`#6B7280`, border `#E4E1DA`, bg `#F7F5F0`) | `AlertTriangle` | `Estimated Route (Closure Unverified)` | Road distance and driving duration computed via road network, but real-time road closure / event data is unavailable or unverified. Neutral treatment preserves Amber `#E1A93A` exclusively for confirmed success. |
| `UNVERIFIED` | Slate (`#475569`, border `#CBD5E1`, bg `#F1F5F9`) | `HelpCircle` | `Factual Evidence Missing` | Coordinates or operating hours cannot be verified against authoritative place records. Flagged for traveler review. |
| `NEEDS_CLARIFICATION` | Blue (`#1D4ED8`, border `#BFDBFE`, bg `#DBEAFE`) | `Info` | `Ambiguous Destination / Needs Detail` | Vague destination (e.g., "mountain", "spa") mapped to multiple candidates; prompts group to select specific POI. |
| `INFEASIBLE` | Red (`#B91C1C`, border `#FECACA`, bg `#FEE2E2`) | `XCircle` | `Schedule / Route Conflict` | Driving duration plus activity exceeds slot window, or causes traveler to miss next mandatory itinerary event. Triggers negotiation panel. |
| `BLOCKED` | Deep Red (`#991B1B`, border `#FCA5A5`, bg `#FEE2E2`) | `ShieldAlert` | `Strict Safety / Access Block` | Destination is confirmed closed, road impassable, or violates a non-negotiable physical constraint. Blocked from consensus voting. |

### 6.2 Evidence-Grounded Schedule Negotiation Panel
When an activity proposal or objection results in an `INFEASIBLE` timing conflict (e.g., requested road trip exceeds time before the next scheduled commitment), the AI Concierge must not merely output "Invalid". It renders a dedicated **Schedule Feasibility Negotiation Card**:
- **Context Card**: Displays calculated road-network travel duration (e.g., "1 hour 20 minutes driving time via road network") compared against available slot window (e.g., "1 hour remaining before scheduled Monkey Forest visit").
- **3-Option Action Group**:
  1. **Option 1: Keep Existing Plan**: Preserve current itinerary commitment without adding the candidate.
  2. **Option 2: Consider Closer Alternative**: Automatically suggests a verified candidate within permissible travel radius (e.g., "Visit Campuhan Ridge Walk — 12 min drive, verified open").
  3. **Option 3: Discuss Moving Next Activity**: In Mode A, requests Admin approval to reschedule subsequent slot; in Mode NA, submits a group vote to shift subsequent activity to evening.

### 6.3 Master Form Field Error Contract (Accessible Validation UI)
To prevent silent submission failures and ensure accessibility:
- **Visual Alert**: Any field failing frontend or backend validation immediately receives a `2px` solid border in `Clay` (`#C1502E`, `border-clay`).
- **Inline Error Text**: Rendered directly below the field in `text-clay` (`#C1502E`, `text-xs font-sans`), preceded by an alert circle icon. Error messages are explicit and actionable (e.g., "Cost must be a valid amount with up to 2 decimal places (e.g., 25.50)").
- **Accessibility**: Inputs dynamically receive `aria-invalid="true"` and `aria-describedby="{field}-error"`. Screen readers announce errors on field blur.
- **Focus Shift**: On submit button click with invalid fields, keyboard focus and viewport scrolling smoothly snap to the first invalid field.
- **Submission Barrier**: Primary submission buttons remain disabled or intercept clicks with instant feedback until all required constraints pass.

### 6.4 Geolocation Permission & Origin Isolation Interface
- **Personal Location Trigger**: User profile and nearby discovery views provide a button: `"Use My Current Location"`.
- **Browser Permission**: Triggers standard browser Geolocation API (`navigator.geolocation.getCurrentPosition`).
- **Privacy Notice**: Renders helper text: `"Your device location is used strictly for nearby personal suggestions and is never broadcast as the group's itinerary origin."`
- **Manual Origin Fallback**: If location permission is denied or device GPS is unavailable, displays a prominent manual text input: `"Enter current city, landmark, or hotel address"`.
- **Shared Itinerary Isolation**: The shared group itinerary strictly anchors route calculations to the previous confirmed itinerary stop or trip origin, completely isolated from individual travelers' device GPS fixes.
