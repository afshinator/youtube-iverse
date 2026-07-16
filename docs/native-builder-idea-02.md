# HANDOFF: YouTube 3D Universe Explorer — Native.Builder Hackathon Project

## 0. Purpose of This Document
- Informative, not directive.
- Summarizes an idea, the brainstorming around it, and research findings so far.
- Very little has been decided beyond: (a) it is for the Native.Builder hackathon, (b) it will be built on native.builder, (c) the concept is a "YouTube universe explorer" in 3D.
- Everything else in this document is a possibility, an open question, or a research finding — not a commitment.
- Two-phase plan: a **proof of concept (POC)** first, then the **hackathon submission**, both built on native.builder.

---

## 1. User & Prior Context
- **User**: Afshin. GitHub: https://github.com/afshinator (notable repos: `mcp-server-pexels`, `mcp-server-go-quality`).
- **Workflow**: Engineered dev workflow. Docker containers bridging Linux Mint laptop/desktop. Toolchain includes `claude-code`, `opencode`, `pi`, `hermes`, `commandcode`.
- **Preference**: Prefers to handle data engineering, API orchestration, and backend logic locally; uses web platforms primarily for scaffolding, UI generation, and deployment.e.

---

## 2. Hackathon Facts (Verified from lablab.ai + NativelyAI docs)

### Event
- **Name**: AI Factory — Native.builder Hackathon
- **Host**: NativelyAI + lablab.ai
- **Dates**: August 3–10, 2026
- **Format**: Fully online, no travel
- **URL**: https://lablab.ai/ai-hackathons/nativebuilder-build-without-limits

### Prizes
- **Prize pool**: Listed as "To be announced" on the page. Do not assume any specific figure. Watch the event page and Discord for updates.
- Sponsor perks / extra API credits during the event are common at lablab.ai hackathons but **not confirmed** for this one.

### Perks on Signup
- 50 free native.builder credits ($10 value), one-time, non-renewing, Free plan only.

### Required Deliverables
- Publicly accessible deployed URL.
- Demo video, **≤3 minutes**, showing at least one complete end-to-end workflow.
- Written explanation of *how native.builder was used*.
- List of external APIs, datasets, and tools used.

### Judging Criteria (4 dimensions)
- **Application of Technology** — how well AI models / APIs / integrations are used.
- **Presentation** — clarity of demo and story.
- **Business Value** — practical impact for a defined user.
- **Originality** — uniqueness of approach.

### Hard Disqualifiers
- Inaccessible to judges (URL/credentials missing).
- Primarily built outside native.builder.
- Direct copy of an existing product without meaningful differentiation.
- No working demo.

---

## 3. Native.Builder — What It Actually Is (Verified from docs)

### The Platform
- An AI-native application development platform ("software factory") by NativelyAI.
- Output is **Vite + React web applications only**. No native mobile, no backend-only services.
- Generated code is **real, inspectable, ownable** — not a black box. Every file browsable in the platform.
- Live preview + one-click deploy to `*.nativelyai.app`. Custom domains on paid plans.
- Publishing does not consume credits.

### Agents (documented)
- **Product Architect** — plans, scopes, writes structure before code is generated. Cheaper than Builder.
- **Builder Agent** — writes and refines React code.
- **Feedback Agent** — captures post-deployment user feedback. Appears in tutorials but not core docs.
- Prior handoff mentioned a "Task Planner" and multi-node workflow builder — **not confirmed in docs**. Native.builder is a chat-driven code generator, not a node-graph workflow tool.

### Credits & Plans
| Plan | Price | Credits | Notes |
|---|---|---|---|
| Free | $0 | 50 one-time | Standard models only; 80 msg/hr, 400/day rate limit; 1 project; 2 workspace members |
| Builder | $20/mo | 100/mo | Solo builders |
| Pro | $50/mo | 400/mo | Premium models unlocked |
| Business | $200/mo | 2,000/mo | Teams |
| Scale | $700/mo | 10,000/mo | API access, webhooks |

- Credits consumed by: chat turns, code generation/refactoring, prompt enhancement.
- Credits NOT consumed by: browsing project, previewing, publishing, workspace admin.
- **Estimated hackathon cost**: Free 50 credits gets you through initial scoping + generation + a few iterations (~25–50 turns). $20 Builder plan for one month is likely enough to finish a well-scoped app. Cost driver is **rework**; a tight PRD before touching Builder is the biggest cost-control lever.

### BYOK (Bring Your Own Key)
- Supported: OpenRouter, AI/ML API, Fireworks AI.
- **Only for the building chat.** BYOK does not automatically apply to LLM calls made *by the deployed app at runtime*. The deployed app needs its own way to reach an LLM (usually a user-supplied key or a proxy).

### Platform Sweet Spot vs. Weak Spot
- **Sweet spot**: UI-heavy React apps where interesting logic lives in the frontend — dashboards, agentic orchestrators, structured-output generators, data-viz over public APIs, interactive tools.
- **Weak spot**: apps whose value lives in backend infra, custom data pipelines, or ML training.

---

## 4. The Idea — YouTube 3D Universe Explorer

### One-line Concept
A gamified, 3D exploratory interface for YouTube that replaces (or augments) the standard YouTube homepage, letting users discover topics, channels, and videos by navigating a spatial "universe" instead of scrolling a feed.

### Core Product Points (locked)
- **Works without auth** — public YouTube data alone provides a usable experience.
- **Better with auth** — optional Google login unlocks personal data (subscriptions, liked videos, playlists, etc.), turning personal data into explorable regions.
- **Gamified navigation** — controls should feel enjoyable, not clunky. Need to explore 3D game camera vocabulary  (orbit, focus, warp) vs first-person shooter controls.  Hopefully using poc will help clear this up. TBD.
- **Multi-metric popularity** — view count is one signal; other signals (engagement, recency, subscriber count, upload velocity) can encode into different visual dimensions (size, brightness, color, orbit distance, etc.). Specific mapping TBD.
- **Desktop first, must not crash on mobile.**

### Target User
- Any YouTube user, especially returning users with accounts who come back regularly looking for new interesting content.

### Judge Takeaway (the "aha" moment)
- Using easy 3D controls, the judge should see they have **more discovery options than the YouTube homepage surfaces**, without info-overload of video titles + thumbnails.

---

## 5. Brainstormed Possibilities (all still open)

### Onboarding / Starting Regions
- Front page lets the user pick "where in the YouTube universe to start their travels."
- Possible starting regions:
  - **Home-recs region** (mimics current YouTube homepage; requires auth to be personalized).
  - **History region** (recently watched — see quota/OAuth notes below; may be a proxy like "recent uploads from subscriptions").
  - **Topic query region** (user types a topic, universe is built around it — e.g. "AI").
  - **Channel deep-dive region** (a single channel's universe).
  - **Pre-baked canonical regions** (curated topics shipped as static JSON for instant demo).

- **Channel as first-class object ?** — just like youtube, videos will have 'links' to channels and channels will 'list' their videos, tbd how this is presented, and how many different ways this is presented in the app; idea: interacting with the channel can warp the user to that channel's region.

### Universe Modes (a key idea — worth exploring)
- The onboarding screen should let the user **choose how the data is projected** into the universe. Different modes → completely different universes over the same data:
  - **Topic-solar-systems mode**: major topics as solar systems; big planets = major sub-topics; moons = sub-sub-topics.
  - **Channel-solar-systems mode**: channels as solar systems; big planets = most-viewed videos; other planets = latest videos, most-commented, etc.
  - **Time mode**: newest videos as one region, evergreen classics as another.
  - Other modes TBD.
- The value here is that the same underlying data supports many discovery mental models.

### Interactions
- Click a planet → focus camera + reveal sub-info.
- Click a video → open on YouTube (or embed).
- Click a channel indicator on a video → warp to that channel's region.
- Zoom / orbit / tilt (Google 3D Maps vocabulary is a reasonable UX template).
- Minimap or overview mode for orientation.
- Breadcrumb / "back" trail — essential for not getting lost in 3D.

---

## 6. Research Findings

### 6.1 YouTube Data API v3 Quotas
- Default: **10,000 units/day per Google Cloud project**, resets midnight Pacific.
- Costs that matter:
  - `search.list` = **100 units** (expensive; ~100 searches/day max).
  - `videos.list`, `channels.list`, `playlistItems.list` = **1 unit each**, up to **50 IDs per call** (enrichment is essentially free).
  - `commentThreads.list` = 1 unit per page.
- **Strategic implication**: search sparingly, enrich aggressively. One `search.list` returns up to 50 video IDs; one 1-unit `videos.list` batch-hydrates all 50. Full hydration of 50 videos = 101 units.
- **Watch history via API is heavily restricted.** What OAuth still exposes: subscriptions, liked videos, playlists, video ratings. Recently-watched from the algorithmic homepage is not directly exposed. A "recent uploads from your subscriptions" proxy is the pragmatic substitute.
- No paid tier for the Data API; quota increases require an audit and are not guaranteed.
- "Google MCP" is not relevant to the deployed app's runtime — MCP is for agent contexts (Claude/dev tools), not for React apps at runtime. The deployed app uses standard Google OAuth 2.0 in the browser (PKCE flow).

### 6.2 3D Visualization — Major De-risk
- **`react-force-graph-3d`** (by vasturiano) is essentially a drop-in solution for "planets connected in 3D space":
  - Uses Three.js + WebGL + d3-force-3d physics.
  - Handles node sizing, custom Three.js objects per node (custom "planet" meshes), edges, camera orbit/pan/zoom, click/hover/drag, focus-on-node camera flights.
  - Sister libraries: `r3f-forcegraph` (react-three-fiber-native, more customizable), `three-forcegraph` (raw Three.js).
- Scale: performant into low thousands of nodes; hundreds is trivial. This project won't need more than ~200 visible nodes at a time.
- **Impact on hackathon feasibility**: native.builder agents wiring a well-known component library is much cheaper (in credits and time) than agents writing bespoke Three.js scene code from scratch.

### 6.3 3D Navigation UX
- Google's 3D Maps API has a decent control vocabulary: zoom, move, rotate (heading), tilt, compass-reset. Users recognize these.
- Game-derived patterns worth borrowing:
  - **Focus-on-click** — click a planet, camera flies to it. Built into `react-force-graph-3d`.
  - **Warp / hyperspace** — click channel → animated camera fly-through to that channel's region. Highly demo-friendly.
  - **Breadcrumb / "back" trail** — essential; getting lost in 3D is the #1 failure mode.
  - **Minimap or overview mode** — press a key, zoom way out.
  - **Hover for info, click for action** — reduces info-overload.
- Anti-patterns: true first-person controls (nauseating), forced camera paths (frustrating).

### 6.4 Persistence
- Native.builder deployed apps are **pure Vite + React frontend**. No native database.
- Options:
  - **IndexedDB** (browser-local) — sufficient for this project's cache needs. Decided.
  - Supabase, Firebase, Cloudflare Workers KV — available for cross-device state; not needed for MVP.

### 6.5 Topic Extraction
- YouTube provides per-video: title, description, tags (`snippet.tags`), category ID, channel, duration, view/like/comment counts.
- Approach chosen: **start with tags + category IDs** (deterministic, free, zero infra); upgrade to embedding-based clustering (local sentence-transformer or hosted embedding API + HDBSCAN/k-means/threshold) **if time allows**.
- LLM tagging is a fallback for edge cases or cluster labeling only, not per-video default.
- User's existing local toolchain (qmd, graphify, vector DBs) may be useful for **pre-baking canonical regions offline**, shipped as static JSON with the app.

---

## 7. Decisions Locked So Far
- **Concept**: YouTube 3D Universe Explorer (as described above).
- **Platform**: native.builder for the frontend build + deployment.
- **POC first**, then hackathon app — both on native.builder.
- **POC will run without auth** — public API only, to see how far that gets us.
- **Both pre-baked regions and live search** in the final app.
- **IndexedDB only** for persistence.
- **Topic extraction** starts with YouTube tags + category IDs; upgrade to embeddings if time.
- **Desktop first**, must not crash on mobile.
- **Popularity metrics** — deferred; will design after seeing what the API actually returns cleanly.

---

## 8. Open Decisions (Explicitly Not Yet Made)
- POC scope: which single universe mode + how much of one starting region is enough to prove the concept?  POC will be more about proving navigation is 'easy', enjoyable and presentation and disclosure of videos is valuable.  human needed to judge this.
- Which universe modes to ship in the hackathon app (topic-solar-systems is the most obvious first mode).
- Which popularity metrics to encode into which visual dimensions.
- Whether the app has a settings screen — presumed yes for future auth login + display options; details TBD.
- Whether to include a Google OAuth login flow at all in the hackathon submission (POC skips it).
- Whether to pre-bake regions locally using the user's toolchain, or generate them on the fly inside native.builder.
- How many pre-baked canonical regions to ship (3–4 was suggested; not committed).
- Whether to use `react-force-graph-3d` (drop-in, less customization) or `r3f-forcegraph` (more customization, more work). To be tested during POC.
- Demo-time scope: live query building vs. pre-baked demo tour.
- Naming, branding, aesthetic direction.

---

## 9. Two-Phase Plan

### Phase 1 — Proof of Concept (before hackathon week)
- Purpose: validate that native.builder agents can produce and iterate on a non-trivial 3D React app using a force-graph library.
- Purpose: sanity-check YouTube API quota behavior with real data flows.
- Purpose: expose UX questions early (navigation, click behavior, "getting lost" problem).
- Deliverables: **TBD**. Should be small enough to fit inside free credits + a small budget of paid credits if needed.
- comment: POC might have to be just showing 3D experience with bogus video data to prove discovery method is valid.

### Phase 2 — Hackathon Submission (Aug 3–10, 2026)
- Full app built during the official hackathon window.
- Must satisfy all hackathon deliverables (public URL, ≤3-min demo video, "how native.builder was used" writeup, external tools list).
- Must foreground native.builder's role in the demo video and writeup — this is what judges score on for "meaningful use."

---

## 10. Risks & Watchpoints
- **Credit exhaustion from rework** — mitigate with tight Product Architect scoping before Builder.
- **Google OAuth complexity** — only relevant if auth is included; PKCE flow from a SPA is straightforward but has moving parts.
- **YouTube API quota exhaustion during demo** — critical. Pre-bake or cache heavily. A demo that dies from quotaExceeded at judging time is a project killer.
- **3D-as-gimmick trap** — if navigation isn't genuinely easier/faster than YouTube's list UI, the project fails its own value proposition. Judge with real users during POC.
- **"Built outside native.builder" perception** — even if the app is legitimately built on native.builder, the demo video and writeup need to make that visible. Show the platform, not just the output.

---

## 11. Instructions for the Receiving AI
- Acknowledge receipt of this context.
- Focus on quality on project, not 'moving it forward'.
- Treat all items in Sections 4, 5, 8 as **possibilities and open questions**, not decisions.
- Treat items in Section 7 as decisions to preserve unless the user explicitly revisits them.
- Do not prescribe a path forward unprompted. Wait for the user's next prompt to begin scoping, PRD-drafting, POC design, or research.
- When research is asked for, verify against live sources rather than relying on prior knowledge (hackathon rules, native.builder features, and API quotas all change).
- Prefer bulleted lists over long paragraphs in responses, per user preference.
- Dont assume or guess, verify by checking docs when possible and asking user otherwise.
