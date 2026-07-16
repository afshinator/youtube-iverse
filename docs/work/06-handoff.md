# HANDOFF — YouTube 3D Universe Explorer POC (continuation in a fresh chat)

## 0. Read first, then acknowledge
Three project files are attached to this project: the original concept/handoff, the final harvested
dataset, and the harvest result log. **Read them and acknowledge before doing anything.** Do not
re-derive their contents. This document carries what those files do **not**: the POC design decisions
locked in the prior chat, the current state, the next step, and — most importantly — the **verification
protocol (§5)** that must govern all further planner/worker/human work. Treat §5 as binding, not advisory.

---

## 1. Where we are
- **Concept:** a navigable 3D "universe" of YouTube content — same data shown as different universes
  (see the concept file). **POC job:** let a human judge whether the 3D navigation is easy/enjoyable and
  whether the way videos are disclosed is valuable. It is a risk-removal exercise, not a feature build.
- **Data workstream: DONE and independently verified.** A real, keyless, static-JSON dataset (564 real
  videos, 18 channels, 3 topics) is finished. Its integrity was confirmed by recomputing the critical
  numbers directly from the raw JSON — not by trusting the worker's audit summary. See the dataset and
  harvest-log files. **Do not re-harvest.**
- **Next:** turn the locked decisions (§2) + this real data into a tight **PRD for native.builder's
  Product Architect** (step 1 of their pipeline), then oversee the native.builder build.

---

## 2. Locked POC decisions (these live in NO file — carry them forward exactly)
- **Modes (two):** channels-as-solar-systems (channel = star, videos = planets — 2-level) and
  topics-as-solar-systems (topic = star, channels = planets, videos = moons — 3-level). One shared video
  pool. Each mode is visually unmistakable: distinct palette, a persistent HUD mode-badge, and an in-world
  backdrop/landmark. Modes must be structurally different, not just recolored.
- **Channel is always explorable.** From topic mode, clicking a channel **switches modes** and lands at
  that channel's system. A **warp transition (camera pull-out → swap → fly-in + one cheap effect)** is a
  **must-have** for game-feel; heavy VFX deferred.
- **Navigation/orientation:** bounded world via **camera-distance clamp** (no literal wraparound);
  **reset-to-overview** button; **focus-on-click** camera flights. **Breadcrumbs are OUT.**
- **Minimap:** a **2D schematic** (NOT a second live 3D render), warping to a **solar system** on click;
  fixed-map default with a cheap toggle to trial center-on-me; "you are here" = highlight current system.
- **Layout:** mostly-3D with a **small floating info panel** + minimap. **Not** split-screen. Info panel
  on select shows channel + thumbnail + a launch action.
- **Visual identity:** **stars are individually distinctive** (few, they're the landmarks); **planets/moons
  vary by data→visual mapping** (size/color/glow from real metrics), **not** bespoke art. **Planet size =
  channel's `video_count_total`; moon count = harvested count.**
- **Channel-as-world:** mapping is **planet = channel, moon = video**. **LOD drill-in** (fly into a channel
  → its videos bloom as moons) is a **core density mechanism**, not optional. Grouping is demonstrated on
  the two showcase channels (Veritasium's 6 subject clusters, Two Minute Papers' 3 AI clusters) via real
  playlist membership. **Literal terrain/cities is a banked north-star — NOT built in the POC.**
- **Density handling:** LOD bloom-on-approach is primary; optional cap + "show more"; physics tuning for
  spacing. The dataset deliberately contains dense + clustered cases to stress-test this.
- **Library:** **`react-force-graph-3d`** (drop-in) for the POC. `r3f-forcegraph` is the proven upgrade
  path if the hackathon later needs bespoke spectacle. Same core, so upgrading is not a rewrite.
- **Playback:** open the **real YouTube watch page in a new tab** (keyless; preserves the user's real
  history + Premium ad-free experience). Inline/embed playback is deferred.

## 3. Explicitly OUT of POC scope
Auth/OAuth; any live API call at runtime; live programmatic search; navigable terrain/cities; inline or
embedded playback UX; breadcrumb history. The app ships the static JSON and makes no network calls except
opening YouTube in a new tab.

---

## 4. Immediate next step
Draft the **PRD as a product brief for the step-1 Product Architect** (not code instructions for the
builder): state the §2 decisions as *already decided* constraints so the Architect plans around them
rather than reopening them; include the §3 out-of-scope fence; and point at the real dataset (its shape,
not its contents). Confirm PRD-shaping choices with the human before drafting, then write it as a
hand-off file.

---

## 5. VERIFICATION PROTOCOL (binding — governs all planner/worker/human work from here)

**Premise: mistakes are guaranteed — by the worker, by the planner, and in the human's stated intent.**
The goal is not to prevent errors but to **catch them early and cheaply.** The data phase was a rehearsal
that revealed the specific failure patterns below; the same patterns will recur during the native.builder
build. This protocol must be honored there too.

### 5.1 The three roles and their boundaries
- **Human** — owns intent and final judgment on anything not reducible to a check.
- **Planner (you, Claude)** — translates intent into *checkable requirements*, writes work orders,
  reviews worker output adversarially, and surfaces judgment calls to the human in plain language.
- **Worker (an agent: the harvest LLM before, native.builder's agents next)** — executes and reports.
Every boundary is a place errors cross. Verify at each one; do not assume any party is reliable.

### 5.2 Standing rules for every work order the planner issues
1. **No value without a real, cited source.** Every factual claim (a count, an ID, a "playlist X exists",
   a "feature Y works") must trace to an actual fetch/run/test performed this session. Unsourced claims
   are void, not provisionally accepted.
2. **No fabrication.** Unobtainable → explicit null/empty + a logged reason. Never invent to fill a gap.
3. **Audits are computed in code and pasted raw.** Any hand-typed total or summary is itself a violation,
   because hand-typed numbers are where reconciliation errors hide.
4. **Mandatory STOP gates.** Split every task into checkpoints; the worker halts at each and waits, even
   when everything looks fine. Plan-and-execute in one uninterrupted pass is prohibited.
5. **Every requirement carries an acceptance test.** When the planner writes a requirement, it also writes
   the concrete pass/fail check for it — a number, a boolean, or, if it's a judgment call, an explicit
   "HUMAN MUST EYEBALL THIS" tag. A requirement with no check is not a requirement; it's a wish.

### 5.3 The planner's adversarial review duty (do NOT rubber-stamp "all PASS")
When a worker reports success, the planner **independently re-derives the critical facts from the raw
artifact** (the JSON, the built app, the logs) before accepting anything. A green audit from the worker is
an input to review, never the conclusion of it. Approval is given only on facts the planner reconstructed.

### 5.4 Known failure catalog — watch for each recurring (all of these actually happened this project)
1. **Guess dressed as observation.** ("5 playlists confirmed" when only 1 was ever seen.) → Demand the
   cited fetch; treat any specific presented without a source as fiction until proven.
2. **Impossibility claim that contradicts prior success.** ("Can't get X keyless" after X was gotten
   keyless earlier.) → Before accepting any "can't", cross-check against what has already been done.
3. **Hand-typed totals that don't reconcile.** (296 vs 265; "none at 15" while six were at 15; 19 vs 13.)
   → Recompute every subtotal from the raw data yourself.
4. **Criteria met, outcome wrong.** (A selection rule "passed" but chose the worst option because the
   metric rewarded contaminated data — playlist sums exceeding the whole catalog.) → Sanity-check rule
   *outputs* against physical reality: impossible sums, suspiciously round/identical numbers, results that
   contradict the stated goal. A passing check on a wrong metric is still a failure.
5. **Silent scope drop.** (A required feature/field quietly missing.) → The audit must enumerate every
   requirement and mark it present/absent; absence is a FAIL, not an omission.
6. **The planner's own rule was flawed.** (An 80% catch-all threshold let a 64% soft-catch-all through; a
   "largest volume" metric optimized for the wrong thing.) → When a rule's output looks surprising, suspect
   the rule, not just the worker. Re-examine your own criteria; route genuine judgment calls to the human.
7. **Rubber-stamped "done".** → §5.3. Never approve on a summary; approve on re-derived facts.

### 5.5 Human backstop
Some things cannot be reduced to a check — *is this the right showcase channel? do these clusters make
sense? does this navigation actually feel good?* The planner routes these to the human in **plain,
jargon-free language with a clear recommendation and the tradeoff** (the human has a high-level view and
does not want to track internals). The planner never silently resolves a judgment call the human should own.

### 5.6 Applying this to the native.builder build specifically
The worker becomes native.builder's agents; "the artifact" becomes the running app. The same duties hold:
requirements go in with acceptance tests; the build proceeds in checkpointed stages with STOPs; and each
stage's output is verified against the requirement list by inspection of the actual app, not the agent's
claim that it's done. Expect the §5.4 patterns (features silently dropped, "it works" that doesn't,
plausible-but-untrue status reports) and catch them the same way.

---

## 6. Opening move for this chat
Acknowledge the three files and this handoff. Confirm you will operate under §5. Then propose the
PRD-shaping questions (format, dataset-reference approach, scope fence, stretch-item labeling) for the
human to confirm before you draft the PRD. Do not start generating the PRD until those are settled.