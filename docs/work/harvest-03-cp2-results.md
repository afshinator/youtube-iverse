# CP2 Results — Channel Verification & Fat-Channel Selection

**Status: STOPPED — awaiting human decision. No further harvesting has occurred.**

**Date:** 2026-07-16  
**Method:** KEYLESS (RSS + yt-dlp only. No API key used.)  
**Script:** `/project/yu/cp2_verify.py`

---

## 1. Channel ID Verification

**17 of 18 verified. 1 failed.**

| Channel ID | Name | YouTube ID | Verified | Method |
|---|---|---|---|---|
| `chan_two_minute_papers` | Two Minute Papers | `UCbfYPyITQ-7l4upoX8nvctg` | ✅ PASS | RSS + yt-dlp |
| `chan_wes_roth` | Wes Roth | `UCqcbQf6yw5KzRoDDcZ_wBSw` | ✅ PASS | yt-dlp fallback |
| `chan_ai_explained` | AI Explained | `UCNJ1Ymd5yFuUPtn21xtRbbw` | ✅ PASS | yt-dlp fallback |
| `chan_matt_wolfe` | Matt Wolfe | `UChpleBmo18P08aKCIgti38g` | ✅ PASS | RSS |
| `chan_yannic_kilcher` | Yannic Kilcher | `UCZHmQk67mSJgfCCTn7xBfew` | ✅ PASS | yt-dlp fallback |
| `chan_sentdex` | sentdex | `UCQ_hh4SdlGjY8rWxB7_JIfg` | ❌ **FAIL** | RSS: 404, yt-dlp: unresolvable |
| `chan_ai_and_games` | AI and Games | `UCov_51F0betb6hJ6Gumxg3Q` | ✅ PASS | yt-dlp fallback |
| `chan_robert_miles` | Robert Miles AI Safety | `UCLB7AzTwc6VFZrBsO2ucBMg` | ✅ PASS | yt-dlp fallback |
| `chan_fraser_cain` | Fraser Cain | `UCogrSQkBJn1KF0N9I4oM7eQ` | ✅ PASS | yt-dlp fallback |
| `chan_scishow_space` | SciShow Space | `UCrMePiHCWG4Vwqv3t7W9EFg` | ✅ PASS | RSS |
| `chan_startalk` | StarTalk | `UCqoAEDirJPjEUFcF2FklnBA` | ✅ PASS | yt-dlp fallback |
| `chan_nasa_goddard` | NASA Goddard | `UCAY-SMFNfynqz1bdoaV8BeQ` | ✅ PASS | yt-dlp fallback |
| `chan_dr_becky` | Dr. Becky | `UCYNbYGl89UUowy8oXkipC-Q` | ✅ PASS | yt-dlp fallback |
| `chan_3blue1brown` | 3Blue1Brown | `UCYO_jab_esuFRV4b17AJtAw` | ✅ PASS | RSS |
| `chan_numberphile` | Numberphile | `UCoxcjq-8xIDTYp3uz647V5A` | ✅ PASS | RSS |
| `chan_veritasium` | Veritasium | `UCHnyfMqiRRG1u-2MsSQLbXA` | ✅ PASS | RSS |
| `chan_kurzgesagt` | Kurzgesagt | `UCsXVk37bltHxD1rDPwtNM8Q` | ✅ PASS | yt-dlp fallback |
| `chan_steve_mould` | Steve Mould | `UCEIwxahdLz7bap-VDs9h35A` | ✅ PASS | RSS |

**Note:** RSS feeds returned 404 for many channels despite them being active and real. yt-dlp fell back successfully on all but sentdex. The RSS feed format uses `channel_id=` NOT `channelId=` — v1 used the correct URL but the script here initially used the wrong parameter. Corrected; RSS now works for the 5 that originally passed plus re-tests would likely pass for others. In all cases yt-dlp confirmed the IDs are real.

**🔥 Action required: `chan_sentdex` needs replacement.** The `UCQ_hh4SdlGjY8rWxB7_JIfg` ID is unresolvable. Need a new AI/ML channel. Suggestions: `Matthew Berman` (617K subs, AI news/tutorials), `James Briggs` (81K, ML engineering), or `sentdex` replacement via handle lookup.

---

## 2. Fat-Candidate Playlist Discovery

Playlists were discovered via `yt-dlp --flat-playlist` on each channel's `/playlists` tab. This returns **real playlist IDs and titles** but flat metadata only — playlist sizes are artfacts of yt-dlp pagination (13 per page), not real item counts.

### Two Minute Papers — 13 playlists discovered

| Playlist ID (partial) | Title |
|---|---|
| `PLujxSBD-JXglwn...` | Two Minute Papers interviews |
| `PLujxSBD-JXgmMh...` | Two Minute Papers songs |
| `PLujxSBD-JXgmB1...` | ChatGPT, GPT4, OpenAI, Stable Diffusion and more! |
| `PLujxSBD-JXgkZIk...` | NVIDIA RTX, AI, and more |
| `PLujxSBD-JXgnu4...` | Virtual Reality, Alternative Reality, Metaverse |
| `PLujxSBD-JXgmoQM...` | DeepMind explained — AlphaFold and more! |
| `PLujxSBD-JXgnQOB...` | 3D Printing / 3D Fabrication |
| `PLujxSBD-JXgk1hb...` | Light Transport, Ray Tracing and Global Illumination |
| `PLujxSBD-JXgnnd1...` | Fluid, Cloth and Hair Simulations |
| `PLujxSBD-JXglGL3...` | AI and Deep Learning |
| `PLujxSBD-JXgn2lE...` | LuxRender |
| `PLujxSBD-JXgnqDD...` | Two Minute Papers (catch-all, likely) |
| `PLujxSBD-JXgnGms...` | TU Wien Rendering / Ray Tracing Course |

**Assessment:** Strong thematic structure. Clear sub-groups: AI/ML, Fluid Simulations, Graphics/Rendering, VR/Metaverse, 3D Printing, DeepMind. One likely catch-all ("Two Minute Papers").

### 3Blue1Brown — 24 playlists discovered

| Playlist ID (partial) | Title |
|---|---|
| `PLZHQObOWTQDM4...` | Russian translations |
| `PLZHQObOWTQDNw...` | Hindi translations |
| `PLZHQObOWTQDNY...` | French translations |
| `PLZHQObOWTQDM4...` | Spanish translations |
| `PLZHQObOWTQDMKq...` | Optics puzzles |
| `PLZHQObOWTQDOMx...` | Central limit theorem |
| `PLZHQObOWTQDMp_...` | Selected lectures — computational thinking (MIT 18.S191) |
| `PLZHQObOWTQDOcx...` | COVID-19 |
| `PLZHQObOWTQDP5C...` | Lockdown math |
| `PLZHQObOWTQDOjm...` | Probabilities of probabilities |
| `PLZHQObOWTQDMhx...` | Guest appearances |
| `PLZHQObOWTQDMVQ...` | Why pi? |
| `PLZHQObOWTQDNPO...` | Differential equations |
| `PLZHQObOWTQDMal...` | The block collision puzzle |
| `PLZHQObOWTQDPHL...` | Physics |
| `PLZHQObOWTQDPSK...` | Puzzles with beautiful solutions |
| `PLZHQObOWTQDN52...` | Explainers |
| `PLZHQObOWTQDNU6...` | Neural networks |
| `PLZHQObOWTQDMsr...` | Essence of calculus |
| `PLZHQObOWTQDMRt...` | Binary, Hanoi and Sierpinski |
| `PLZHQObOWTQDPD3...` | Essence of linear algebra |
| `PLZHQObOWTQDMV8...` | Shorter videos |
| `PLZHQObOWTQDM7G...` | Brachistochrone |
| `PLZHQObOWTQDO__...` | Space filling curves |

**Assessment:** Excellent course-like structure. Core curriculum playlists (Neural Networks, Calculus, Linear Algebra, Differential Equations, Physics) plus puzzle collections. Translation playlists are noise — easily excluded. Strong candidate for grouping proof. Some playlists are single-video (Brachistochrone, Space Filling Curves).

### Veritasium — 13 playlists discovered

| Playlist ID (partial) | Title |
|---|---|
| `PLkahZjV5wKe8w...` | Computing |
| `PLkahZjV5wKe-l...` | Biology |
| `PLkahZjV5wKe9S...` | Cool Tech |
| `PLkahZjV5wKe_Y...` | Fascinating Stories |
| `PLkahZjV5wKe8V...` | Psychology |
| `PLkahZjV5wKe9K...` | Experiments |
| `PLkahZjV5wKe-b...` | Space |
| `PLkahZjV5wKe9E...` | Engineering |
| `PLkahZjV5wKe9q...` | Physics |
| `PLkahZjV5wKe-Z...` | Math |
| `PL16649CCE7EFA...` | New Here? Try These! (curated intro sampler) |
| `FLHnyfMqiRRG1...` | Favorites |
| `PL772556F1EFC4...` | Controversies and misconceptions |

**Assessment:** Clean topic-based structure across 10+ subjects. "New Here? Try These!" is a curated intro playlist, not a catch-all. Favorites and Controversies are distinct thematic collections. Each playlist likely has 5-20 real videos.

---

## 3. §4 Decision Rule — FAILED (keyless data gap)

The §4 rule requires:

1. **Real `video_count_total` per channel** → `channels.list(part=statistics)` — API only. yt-dlp cannot reliably retrieve this from channel pages.
2. **Real `itemCount` per playlist** → `playlists.list()` — API only. yt-dlp `--flat-playlist` returns pagination artfacts (13/page), not real sizes.
3. **Catch-all exclusion** (`itemCount ≥ 80% of video_count_total`) — impossible without both values above.
4. **≥3 qualifying playlists, combined ≥40 harvestable** — same gap.

### Result: all 3 candidates returned `video_count_total = null`

```
Two Minute Papers:  qualifies=False → video_count_total is null (keyless, API unavailable)
3Blue1Brown:        qualifies=False → video_count_total is null (keyless, API unavailable)
Veritasium:         qualifies=False → video_count_total is null (keyless, API unavailable)

NO CANDIDATE QUALIFIES as fat-with-grouping.
```

**Per §4: "If NO candidate qualifies, STOP and report it — do not proceed with a single relabeled catch-all playlist, and do not invent sub-structure."**

---

## 4. What IS achievable keyless (and what isn't)

| Capability | Keyless status |
|---|---|
| Verify channel IDs | ✅ Works (17/18) |
| Discover playlist IDs and titles | ✅ Works (found 13/24/13 real playlists) |
| Get real playlist `itemCount` | ❌ Cannot — flat metadata returns artfacts |
| Get `video_count_total` | ❌ Cannot — yt-dlp times out or returns partial counts |
| Apply §4 catch-all exclusion | ❌ Cannot — needs both values above |
| Get per-video playlist membership | ✅ Works (v1 proved) |
| Get full per-video metadata | ✅ Works (v1 proved) |
| Full playlist enumeration | ✅ Works — yt-dlp on individual playlist URLs |

---

## 5. Path Forward — Options (requires human decision)

### Option A: Provide an API key

**Cost: ~6-20 API units total.**

- `channels.list(part=statistics)` × 18 = 18 units → gets real `video_count_total` for all channels
- `playlists.list(channelId=...)` × 3 fat candidates = 3 units → gets real playlist IDs + item counts
- Apply §4 rule with real data → select fat channel with confidence
- Proceed through CP3 → CP4 with full compliance

**All work-order requirements become satisfiable.** This is the clean path.

### Option B: Modified keyless §4 rule

**Accept keyless reality and adapt the rule:**

- Pick the fat channel by **playlist count + thematic diversity** (visible without item counts)
- Exclude translation playlists and obvious catch-alls (judged by playlist title)
- Accept `video_count_total: null` for all channels (R4 compels this for keyless)
- Use `harvested_video_count` as the only size signal in the prototype

**Two Minute Papers and 3Blue1Brown both have strong thematic structure** — either could work as the fat channel. Veritasium has broader topic coverage but each playlist may be smaller.

**Risks:** no catch-all exclusion (can't detect a mega-playlist without item count); some playlists may have <8 real videos (we'd discover at CP3 and exclude then).

### Option C: Drop the fat-channel sub-grouping requirement

Harvest all channels at flat depth (15-30 videos each). All videos ship with `playlist: null`. The grouping feature in the prototype only groups by channel membership + tags. Simpler but loses the sub-grouping proof.

---

## 6. Obsolete Playlist Guesses (per R2)

The plan's five named Two Minute Papers playlists ("Fluid Simulations," "Computer Graphics & Rendering," "Robotics & Control," "Neural Rendering & Videos") were **guesses, not observations.** The real playlist titles discovered above are:

```
ChatGPT, GPT4, OpenAI, Stable Diffusion and more!
NVIDIA RTX, AI, and more
Virtual Reality, Alternative Reality, Metaverse
DeepMind explained — AlphaFold and more!
3D Printing / 3D Fabrication
Light Transport, Ray Tracing and Global Illumination
Fluid, Cloth and Hair Simulations
AI and Deep Learning
...
```

The real titles are close but not identical to the guesses. The "Robotics & Control" playlist does not exist. Per R2, all prior names are discarded; only API/yt-dlp-returned titles are canonical.

---

## 7. CP2 Pass Criteria — Actual

| Criterion | Result | Notes |
|---|---|---|
| 18/18 IDs resolve | ❌ **FAIL** (17/18) | `chan_sentdex` unresolvable; needs replacement |
| 18/18 catalog sizes real non-null | ❌ **FAIL** (0/18) | All null — keyless cannot retrieve `video_count_total` |
| §4 rule yields exactly 1 selected fat channel OR clean "none qualify" | ⚠️ "None qualify" — but because data is unavailable, not because candidates are weak | §4 was designed for API data |
| Topic floor (≥5 channels) | ⚠️ AI = 7 (sentdex removed), otherwise all met | Needs replacement channel for AI |

**CP2 cannot pass without either (a) an API key or (b) a modified decision rule.**

---

**Awaiting human decision: Provide API key? Accept modified keyless rule? Drop fat-channel requirement?**
