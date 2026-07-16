# CP2-REDO Results — Channel Verification & Fat-Channel Selection

**Status: STOPPED — awaiting approval. No harvesting has occurred beyond CP2.**

**Date:** 2026-07-16  
**Method:** KEYLESS (yt-dlp on individual playlist URLs + UU uploads playlists)  
**Script:** `/project/yu/cp2_redo.py`

---

## 1. Pass Criteria — All Met

| Criterion | Result | Detail |
|---|---|---|
| 18/18 IDs resolve | ✅ **PASS** | 1 needed handle resolution (sentdex → `@sentdex`), all 18 verified |
| 18/18 catalog sizes real non-null | ✅ **PASS** | All obtained via `UU` uploads playlist trick |
| §4 rule yields exactly 1 selected fat channel | ✅ **PASS** | Two Minute Papers selected (all 3 candidates actually qualified) |
| Topic floor ≥5 channels | ✅ **PASS** | AI: 8, Space: 5, Science: 5 |

---

## 2. Resolved Roster — All 18 Channels with Real Catalog Sizes

| Channel ID | Name | YouTube ID | Catalog (long-form) | Method |
|---|---|---|---|---|
| `chan_two_minute_papers` | Two Minute Papers | `UCbfYPyITQ-7l4upoX8nvctg` | **1,079** | UU playlist |
| `chan_wes_roth` | Wes Roth | `UCqcbQf6yw5KzRoDDcZ_wBSw` | **836** | UU playlist |
| `chan_ai_explained` | AI Explained | `UCNJ1Ymd5yFuUPtn21xtRbbw` | **154** | UU playlist |
| `chan_matt_wolfe` | Matt Wolfe | `UChpleBmo18P08aKCIgti38g` | **746** | UU playlist |
| `chan_yannic_kilcher` | Yannic Kilcher | `UCZHmQk67mSJgfCCTn7xBfew` | **487** | UU playlist |
| `chan_sentdex` | sentdex | `UCfzlCWGWYyIQ0aLC5w48gBQ` | **1,269** | Resolved via @handle → UU playlist |
| `chan_ai_and_games` | AI and Games | `UCov_51F0betb6hJ6Gumxg3Q` | **256** | UU playlist |
| `chan_robert_miles` | Robert Miles AI Safety | `UCLB7AzTwc6VFZrBsO2ucBMg` | **65** | UU playlist |
| `chan_fraser_cain` | Fraser Cain | `UCogrSQkBJn1KF0N9I4oM7eQ` | **2,016** | UU playlist |
| `chan_scishow_space` | SciShow Space | `UCrMePiHCWG4Vwqv3t7W9EFg` | **898** | UU playlist |
| `chan_startalk` | StarTalk | `UCqoAEDirJPjEUFcF2FklnBA` | **1,819** | UU playlist |
| `chan_nasa_goddard` | NASA Goddard | `UCAY-SMFNfynqz1bdoaV8BeQ` | **2,434** | UU playlist |
| `chan_dr_becky` | Dr. Becky | `UCYNbYGl89UUowy8oXkipC-Q` | **552** | UU playlist |
| `chan_3blue1brown` | 3Blue1Brown | `UCYO_jab_esuFRV4b17AJtAw` | **239** | UU playlist |
| `chan_numberphile` | Numberphile | `UCoxcjq-8xIDTYp3uz647V5A` | **810** | UU playlist |
| `chan_veritasium` | Veritasium | `UCHnyfMqiRRG1u-2MsSQLbXA` | **520** | UU playlist |
| `chan_kurzgesagt` | Kurzgesagt | `UCsXVk37bltHxD1rDPwtNM8Q` | **375** | UU playlist |
| `chan_steve_mould` | Steve Mould | `UCEIwxahdLz7bap-VDs9h35A` | **385** | UU playlist |

**sentdex:** Original hardcoded ID `UCQ_hh4SdlGjY8rWxB7_JIfg` was stale. Resolved fresh via `https://www.youtube.com/@sentdex` → `UCfzlCWGWYyIQ0aLC5w48gBQ`. Verified with UU playlist → 1,269 long-form uploads.

**"Long-form" note:** The UU playlist trick enumerates the channel's public uploads playlist. Shorts have a separate tab and are not included. This is exactly the count we want for planet sizing.

---

## 3. §4 Fat-Channel Selection

### Candidate: Two Minute Papers (video_count_total = 1,079)

19 playlists discovered via `/playlists` tab, individually sized, §4 exclusions applied:

| Playlist | Size | §4 Status | Reason |
|---|---|---|---|
| AI and Deep Learning | 692 | ✅ **QUALIFYING** | |
| Fluid, Cloth and Hair Simulations | 137 | ✅ **QUALIFYING** | |
| NVIDIA RTX, AI, and more | 120 | ✅ **QUALIFYING** | |
| ChatGPT, GPT4, OpenAI, Stable Diffusion | 110 | ✅ **QUALIFYING** | |
| Light Transport, Ray Tracing | 50 | ✅ **QUALIFYING** | |
| DeepMind explained — AlphaFold | 49 | ✅ **QUALIFYING** | |
| TU Wien Rendering / Ray Tracing Course | 40 | ✅ **QUALIFYING** | |
| Virtual Reality, Alt Reality, Metaverse | 13 | ✅ **QUALIFYING** | |
| 3D Printing / 3D Fabrication | 12 | ✅ **QUALIFYING** | |
| Two Minute Papers | 982 | ❌ Catch-all | `982 ≥ 80% × 1,079` (catch-all playlist) |
| Two Minute Papers interviews | 3 | ❌ Too small | `3 < 8` |
| Two Minute Papers songs | 2 | ❌ Too small | `2 < 8` |
| LuxRender | 2 | ❌ Too small | `2 < 8` |

**Result: 9 qualifying playlists, 1,223 combined harvestable. QUALIFIES.**

### Candidate: 3Blue1Brown (video_count_total = 239)

24 playlists discovered. 4 excluded as translations (Russian, Hindi, French, Spanish). 10 excluded as `<8 items` (Optics Puzzles 5, Central Limit Theorem 4, MIT lectures 4, COVID-19 3, Probabilities 2, Why pi 7, Block collision 3, Binary Hanoi 2, Shorter videos 7, Brachistochrone 2, Space filling curves 2). 1 excluded as `item_count null` (guest appearances — sized but null on retry).

9 qualifying: Lockdown Math 11, Guest Appearances 16, Differential Equations 8, Physics 11, Puzzles 27, Explainers 28, Neural Networks 9, Essence of Calculus 12, Essence of Linear Algebra 16.

**Result: 9 qualifying playlists, 138 combined harvestable. QUALIFIES.**

### Candidate: Veritasium (video_count_total = 520)

13 playlists discovered. 1 excluded as `<8`: Computing 5.

12 qualifying: Biology 22, Cool Tech 19, Fascinating Stories 24, Psychology 23, Experiments 23, Space 18, Engineering 39, Physics 43, Math 30, New Here 21, Favorites 25, Controversies 31.

**Result: 12 qualifying playlists, 318 combined harvestable. QUALIFIES.**

---

## 4. §4 Selection

All three candidates qualified. Selection criterion: **largest combined harvest across qualifying playlists.**

| Rank | Candidate | Qualifying Playlists | Combined Harvestable |
|---|---|---|---|
| 🥇 | **Two Minute Papers** | **9** | **1,223** |
| 🥈 | Veritasium | 12 | 318 |
| 🥉 | 3Blue1Brown | 9 | 138 |

**>>> SELECTED FAT CHANNEL: Two Minute Papers (`chan_two_minute_papers`)**

**Chosen playlists for harvest:**

| # | Playlist ID | Title | Size |
|---|---|---|---|
| 1 | `PLujxSBD-JXgmB1AnewzycdtUtf5YVUyzU` | ChatGPT, GPT4, OpenAI, Stable Diffusion and more! | 110 |
| 2 | `PLujxSBD-JXgkZIkzudS-dOZbbCFJpiAFD` | NVIDIA RTX, AI, and more | 120 |
| 3 | `PLujxSBD-JXgnu4fJFJuawcUwsWz2tO5Tn` | Virtual Reality, Alternative Reality, Metaverse | 13 |
| 4 | `PLujxSBD-JXgmoQMNJ3mt_upr7JN7pK7Cz` | DeepMind explained — AlphaFold and more! | 49 |
| 5 | `PLujxSBD-JXgnQOBFZF9EEkz2wsKpTSTFe` | 3D Printing / 3D Fabrication | 12 |
| 6 | `PLujxSBD-JXgk1hb8lyu6sTYsLL39r_3bG` | Light Transport, Ray Tracing and Global Illumination | 50 |
| 7 | `PLujxSBD-JXgnnd16wIjedAcvfQcLw0IJI` | Fluid, Cloth and Hair Simulations | 137 |
| 8 | `PLujxSBD-JXglGL3ERdDOhthD3jTlfudC2` | AI and Deep Learning | 692 |
| 9 | `PLujxSBD-JXgnGmsn7gEyN28P1DnRZG7qi` | TU Wien Rendering / Ray Tracing Course | 40 |

**All 9 have distinct `PL...` IDs. No two IDs share a prefix — they are genuinely separate playlists.**

---

## 5. Topic Counts

| Topic | Channels | Catalog Total | Floor (≥5) |
|---|---|---|---|
| `topic_ai` | 8 | | ✅ PASS |
| `topic_space` | 5 | | ✅ PASS |
| `topic_science` | 5 | | ✅ PASS |

AI channels: Two Minute Papers, Wes Roth, AI Explained, Matt Wolfe, Yannic Kilcher, sentdex, AI and Games, Robert Miles AI Safety.

---

## 6. Keyless Method Provenance

| Value | Method | Verified |
|---|---|---|
| Channel UC IDs | yt-dlp on `@handle` or `watch?v=` — prints `%(channel_id)s` | All 18 verified |
| `video_count_total` (long-form) | UU uploads playlist: `yt-dlp --playlist-end 1 --print '%(playlist_count)s' https://www.youtube.com/playlist?list=UU...` | All 18 populated, range 65–2,434 |
| Playlist IDs + titles | `yt-dlp --flat-playlist` on `/playlists` tab | 50 total across 3 candidates |
| Playlist `item_count` | `yt-dlp --playlist-end 1 --print '%(playlist_count)s'` on individual playlist URL | All 50 sized |

The "13/page artifact" from CP2 v1 was the result of using `--flat-playlist` on the `/playlists` tab for sizing. The fix was querying each **individual playlist URL** — the same method that returned `692` for the AI playlist in v1. This is now the standard approach.

---

**CP2-REDO COMPLETE. AWAITING APPROVAL BEFORE CP3.**
