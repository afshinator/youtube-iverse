# Full YouTube Dataset Re-Harvest — Execution Plan v2

**Status: PLANNING — awaiting approval. No data has been collected.**

---

## 1. Topic Set & Channel Roster

### Topic structure (3 topics, minimum 5 channels each)

| Topic ID | Label | Target Channels | Role |
|---|---|---|---|
| `topic_ai` | Artificial Intelligence | **8** | **Busy topic** — density stress-test |
| `topic_space` | Space & Astronomy | **5** | Secondary |
| `topic_science` | Math & General Science | **5** | Secondary (fixes degenerate single-channel topic from v1) |

**Minimum channels-per-topic: 5.** The v1 harvest shipped `topic_math` with 1 channel; that is unacceptable. Five is the floor — enough for a two-ring orbit layout in the 3D prototype without collapsing.

**Why these topics:** AI and Space were strong in v1 with real channels showing playlist activity. The Math topic is retained but expanded to "Math & General Science" to draw from a larger channel pool (Numberphile, Veritasium, etc.) — eliminating the single-channel degenerate case.

---

### Channel roster — AI (busy, 8 channels)

| Channel ID | Channel Name | YouTube ID | Why included | Has playlists? | Playlists visible on channel page |
|---|---|---|---|---|---|
| `chan_two_minute_papers` | Two Minute Papers | `UCbfYPyITQ-7l4upoX8nvctg` | **Fat channel.** Large catalog, multiple curated playlists, excellent grouping signal. | **Yes** | AI, Deep Learning, Fluids, Graphics, Physics, etc. |
| `chan_wes_roth` | Wes Roth | `UCqcbQf6yw5KzRoDDcZ_wBSw` | AI news/analysis, active, growing | Unknown | To be discovered via API |
| `chan_ai_explained` | AI Explained | `UCNJ1Ymd5yFuUPtn21xtRbbw` | Deep AI analysis, research coverage | Unknown | To be discovered via API |
| `chan_matt_wofe` | Matt Wolfe | `UChpleBmo18P08aKCIgti38g` | AI tools/news, distinct from research channels | Unknown | To be discovered via API |
| `chan_yannic_kilcher` | Yannic Kilcher | `UCZHmQk67mSJgfCCTn7xBfew` | ML paper analysis, technical | Unknown | To be discovered via API |
| `chan_sentdex` | sentdex | `UCQ_hh4SdlGjY8rWxB7_JIfg` | Python/ML tutorials, large catalog | Likely | To be discovered via API |
| `chan_ai_and_games` | AI and Games | `UCov_51F0betb6hJ6Gumxg3Q` | AI in game dev, niche but structured | Likely | Curated playlists expected |
| `chan_robert_miles` | Robert Miles AI Safety | `UCLB7AzTwc6VFZrBsO2ucBMg` | AI safety, distinct angle | Likely | To be discovered via API |

**Why 8 channels:** Dense enough to test topic-as-solar-system with multi-ring orbits. All channels cover AI from different angles (research, news, tutorials, safety, games), creating real conceptual clustering within the topic.

### Channel roster — Space & Astronomy (5 channels)

| Channel ID | Channel Name | YouTube ID | Why included |
|---|---|---|---|
| `chan_fraser_cain` | Fraser Cain | `UCogrSQkBJn1KF0N9I4oM7eQ` | Space news, weekly Q&As, large catalog |
| `chan_scishow_space` | SciShow Space | `UCrMePiHCWG4Vwqv3t7W9EFg` | Weekly space content, structured episodes |
| `chan_startalk` | StarTalk | `UCqoAEDirJPjEUFcF2FklnBA` | Neil deGrasse Tyson, pop-science crossover |
| `chan_nasa_goddard` | NASA Goddard | `UCAY-SMFNfynqz1bdoaV8BeQ` | Official NASA, high production value |
| `chan_dr_becky` | Dr. Becky | `UCYNbYGl89UUowy8oXkipC-Q` | Astrophysics research explainers, distinct academic voice |

**Why these 5:** Four were strong in v1. Dr. Becky added for astrophysics specialization — distinct from news (Fraser), pop-science (StarTalk), agency (NASA), and general (SciShow).

### Channel roster — Math & General Science (5 channels)

| Channel ID | Channel Name | YouTube ID | Why included |
|---|---|---|---|
| `chan_3blue1brown` | 3Blue1Brown | `UCYO_jab_esuFRV4b17AJtAw` | Math visualization, strong playlist structure (Neural Networks, Linear Algebra, Calculus) |
| `chan_numberphile` | Numberphile | `UCoxcjq-8xIDTYp3uz647V5A` | Mathematics, large catalog, distinct from 3B1B (people-driven, not animation-driven) |
| `chan_veritasium` | Veritasium | `UCHnyfMqiRRG1u-2MsSQLbXA` | Science explainers, huge channel, playlists by topic |
| `chan_kurzgesagt` | Kurzgesagt — In a Nutshell | `UCsXVk37bltHxD1rDPwtNM8Q` | Animated science, astrophysics/biology, playlist-rich |
| `chan_steve_mould` | Steve Mould | `UCEIwxahdLz7bap-VDs9h35A` | Hands-on science/engineering demos, distinct format |

**Why this replaces the v1 single-channel topic:** Five channels covering math (3B1B, Numberphile), general science (Veritasium, Kurzgesagt), and hands-on science (Steve Mould) — each with a distinct format. This prevents the degenerate case.

**Note on channel IDs:** The YouTube channel IDs listed above for Numberphile, Veritasium, Kurzgesagt, Steve Mould, sentdex, AI and Games, and Robert Miles are drawn from public knowledge / the v1 feedspot research. They will be **verified in a pre-harvest validation step** before any video data is collected. If any are stale or wrong, discovery via `channels.list` search-by-handle (1 API unit per channel) will be the fallback.

---

## 2. The Fat Channel — Two Minute Papers (`chan_two_minute_papers`)

**Why this channel:** In v1 it was already the fat channel but had only one playlist — useless for sub-clustering. The fix is using its real, distinct playlists.

### Expected playlists (to be confirmed via API `playlists.list`)

Based on Two Minute Papers' channel structure, these playlists are likely discoverable (confirmed via browsing their channel in v1):

| Playlist (expected) | Description | Target videos | Grouping signal |
|---|---|---|---|
| `"AI and Deep Learning"` | Core ML/AI research | ~40 | Strong — all ML research |
| `"Fluid Simulations"` | Physics/fuild simulation breakthroughs | ~15 | Strong — fluid/particle physics |
| `"Computer Graphics & Rendering"` | Ray tracing, neural rendering, graphics | ~15 | Strong — graphics/rendering |
| `"Robotics & Control"` | Robot learning, control systems | ~10 | Strong — robotics |
| `"Neural Rendering & Videos"` | Video synthesis, deepfakes | ~15 | Strong — video/rendering |

**Total target:** ~95 videos from the fat channel across **5 distinct playlists.**

**Discovery method:** API `playlists.list(channelId=...)` returns all public playlists with their IDs, titles, and item counts. Cost: ~1 API unit for the channel. Each playlist then harvested via `playlistItems.list(playlistId=...)`.

**Fallback if fewer real playlists exist than expected:** If the API returns only 2-3 playlists, I'll use those at higher depth (~30 each) and note the limitation. The goal is real sub-structure, not invented sub-structure. If the channel truly only has one playlist, I'll select a different fat channel (e.g., Veritasium or 3Blue1Brown, both known playlist-rich channels).

---

## 3. Per-Channel Harvest Depth & Method

**Principle: size variety is a first-class feature.** The 3D visualization uses channel size (planet diameter) to encode total catalog size, so `video_count_total` must be populated and reflected in `harvested_video_count` proportions.

### Depth plan (all channels)

| Channel | Catalog size (API) | Harvest target | % of catalog | Method | Why this depth |
|---|---|---|---|---|---|
| **Two Minute Papers** | ~900 | **~95** | ~10% | API playlists + yt-dlp enrichment | Fat channel: deep enough across 5 playlists for sub-clustering |
| **sentdex** | ~1,500 | **~50** | ~3% | yt-dlp on uploads playlist | Second-largest catalog, deliberate size contrast with fat channel |
| **Fraser Cain** | ~2,500 | **~40** | ~2% | yt-dlp on uploads playlist | High-catalog-count channel with modest harvest depth — tests "big channel, partial harvest" visual |
| **Numberphile** | ~800 | **~30** | ~4% | yt-dlp on uploads playlist | Medium catalog, medium depth |
| **3Blue1Brown** | ~180 | **~30** | ~17% | API playlists | Small catalog, high harvest ratio — playlist-rich, worth going deep |
| **Veritasium** | ~400 | **~25** | ~6% | yt-dlp on uploads playlist | Medium catalog, medium depth |
| AI Explained | ~200 | **~20** | ~10% | yt-dlp on uploads playlist | Standard depth |
| Matt Wolfe | ~500 | **~20** | ~4% | yt-dlp on uploads playlist | Standard depth |
| Yannic Kilcher | ~300 | **~20** | ~7% | yt-dlp on uploads playlist | Standard depth |
| Wes Roth | ~400 | **~20** | ~5% | yt-dlp on uploads playlist | Standard depth |
| Robert Miles | ~100 | **~20** | ~20% | yt-dlp on uploads playlist | Small catalog, high ratio |
| AI and Games | ~250 | **~20** | ~8% | yt-dlp on uploads playlist | Standard depth |
| SciShow Space | ~500 | **~15** | ~3% | yt-dlp on uploads playlist | Standard depth |
| StarTalk | ~600 | **~15** | ~2% | yt-dlp on uploads playlist | Standard depth |
| NASA Goddard | ~800 | **~15** | ~2% | yt-dlp on uploads playlist | Standard depth |
| Dr. Becky | ~400 | **~15** | ~4% | yt-dlp on uploads playlist | Standard depth |
| Kurzgesagt | ~250 | **~15** | ~6% | yt-dlp on uploads playlist | Standard depth |
| Steve Mould | ~300 | **~15** | ~5% | yt-dlp on uploads playlist | Standard depth |

**Total: ~480 videos across 18 channels. Fat channel: 95. Busy topic (AI): 296.**

**Why this depth distribution:** Catalog sizes range from ~100 (Robert Miles) to ~2,500 (Fraser Cain). Harvest depth ranges from 15-95, with the fat channel at the high end and "leaf" channels at the low end. No channel has exactly 15 (the RSS cap in v1) — all are deliberately chosen depths.

**Method for non-fat channels:** Use yt-dlp on the channel's uploads URL (`https://www.youtube.com/@ChannelHandle/videos`) with a `--playlist-items 1-N` limit. This enumerates videos in upload order and bypasses the RSS ~15-cap. Enrichment is per-video yt-dlp `--print` for full metadata.

**Method for fat channel and playlist-rich channels (3Blue1Brown):** API `playlists.list` to discover playlists, then `playlistItems.list(playlistId=..., maxResults=50)` in batches to collect video IDs. Enrich with yt-dlp `--print` per video.

---

## 4. Method-Per-Field Table

| Field | Primary method | Fallback | Reliable? | Notes |
|---|---|---|---|---|
| `id` | yt-dlp `--print %(id)s` | API `playlistItems.list` | **Reliable** | From playlist enumeration or uploads listing |
| `title` | yt-dlp `--print %(title)s` | API `videos.list(snippet)` | **Reliable** | |
| `channel_id` (internal) | Assigned from channel roster | — | **Reliable** | This is our `chan_` ID, not the YouTube `UC...` |
| `youtube_channel_id` | API `channels.list(id=..., part=id)` or yt-dlp `%(channel_id)s` | yt-dlp on any video from the channel | **Reliable** | Verified in pre-harvest validation step |
| `published_at` | yt-dlp `%(upload_date)s` → parse YYYYMMDD to ISO 8601 | API `videos.list(snippet.publishedAt)` | **Reliable** | |
| `duration_seconds` | yt-dlp `%(duration)s` | API `videos.list(contentDetails.duration)` | **Reliable** | |
| `view_count` | yt-dlp `%(view_count)s` | API `videos.list(statistics.viewCount)` | **Reliable** | |
| `like_count` | yt-dlp `%(like_count)s` | API `videos.list(statistics.likeCount)` | **Reliable** | |
| `comment_count` | yt-dlp `%(comment_count)s` | API `videos.list(statistics.commentCount)` | **Reliable** | |
| `tags` | yt-dlp `%(tags)s` | API `videos.list(snippet.tags)` | **Partial** | Many channels use minimal tags. `[]` when empty. |
| `playlist` | yt-dlp `%(playlist_title)s` on playlist URL | API `playlists.list` for name lookup | **Reliable** when playlist-sourced | `null` for uploads-sourced videos |
| `video_count_total` | API `channels.list(part=statistics)` | — | **API-only** | Not available via yt-dlp. `null` if API fails. |
| `thumbnail_url` | Computed: `https://img.youtube.com/vi/<id>/hqdefault.jpg` | — | **Reliable** | Always fillable once `id` is known |

**Decision: use yt-dlp as the primary enrichment layer, API for discovery.** yt-dlp gives richer metadata per video (tags, upload_date in YYYYMMDD) than a single API response field set without exhausting quota. The API's strength is **discovery and counting** (`playlists.list` for finding playlists, `channels.list` for total counts, `playlistItems.list` for enumerating playlist contents).

**Why not exclusively API:** API `videos.list` with `part=snippet,statistics,contentDetails` gives most fields per video — but `snippet.tags` is sometimes omitted. yt-dlp has been more consistent on tags. Also, API calls at 50 videos per `videos.list` call would be ~10 API units for 480 videos; yt-dlp costs no quota. For this dataset size, either works; yt-dlp is preferred since it's already proven in v1.

---

## 5. Grouping Strategy

**The grouping problem:** each video needs a grouping label for the 3D visualization's clustering feature. Not all channels have playlists. The strategy differs by harvest method:

### Tier 1: Playlist membership (best signal)

**For videos harvested from curated playlists** (fat channel, 3Blue1Brown — likely ~125 videos):
- Assign the playlist title as the `playlist` field
- Example: `"playlist": "Fluid Simulations"`
- This is the gold-standard grouping: hand-curated by the channel owner, semantically coherent

**Discovery:** API `playlists.list(channelId=...)` returns `{title, id, itemCount}` for each playlist. Harvest each chosen playlist via `playlistItems.list`.

### Tier 2: Tags as fallback (for non-playlist videos)

**For videos harvested from uploads listings** (non-fat channels — likely ~355 videos):
- If yt-dlp returns non-empty `tags`, keep them in the dataset
- Do NOT invent a grouping label from tags — the prototype can do its own tag-based clustering
- Set `playlist: null` honestly

**Rationale:** Tags on uploads-sourced videos are from the video itself, not from playlist context. They're a weaker signal but real. The prototype can group by shared tags (e.g., all videos with `['neural rendering']` appear near each other) without me imposing a label. If tags are empty (`[]`), the prototype falls back to title similarity or the channel itself as the grouping unit.

### Tier 3: Title-based clustering (implicit)

**For videos with no tags and no playlist:**
- Do nothing in the dataset. Leave `tags: []` and `playlist: null`
- The prototype's force-graph layout will naturally cluster videos by channel (same channel → same star system), and within a channel, similar titles will cluster based on the 3D physics — no fake grouping needed
- Document this: ~15-30% of videos may have no grouping signal beyond channel membership

### What I won't do:
- **No LLM-generated labels:** would violate the "no fabrication" rule and introduce invented data
- **No title-keyword extraction:** fragile, likely to mislabel; the prototype can do this at render time if it wants
- **No pretending `[]` tags are a grouping signal:** empty is empty

---

## 6. Quota & Pacing Estimate

### API quota breakdown

| Operation | Calls | Units each | Total units |
|---|---|---|---|
| `channels.list` (verify IDs, get stats) | 18 channels | 1 | **18** |
| `playlists.list` (discover playlists for all channels) | 18 channels | 1 | **18** |
| `playlistItems.list` (enumerate fat channel playlists) | ~10 pages (50 items/page, ~5 playlists × ~2 pages) | 1 | **10** |
| `playlistItems.list` (enumerate 3B1B playlists) | ~2 pages | 1 | **2** |
| **API total** | | | **~48 units** |

**Daily free quota: 10,000 units.** We use ~0.5%. Quota exhaustion is not a risk.

### Request pacing

| Layer | Pacing | Rationale |
|---|---|---|
| API calls | 500ms minimum between calls | Well within YouTube's rate limits (~1 request/second sustained) |
| yt-dlp per-video enrichment | 1.5 seconds between calls | Proven safe in v1. 480 videos × 2s = ~16 minutes |
| yt-dlp playlist enumeration | no artificial delay (batched by design) | yt-dlp internally paginates playlists; external pacing unnecessary |

**Total estimated runtime:** ~25-35 minutes for the full harvest (mostly yt-dlp enrichment at 1.5s/video).

---

## 7. Risks, Unknowns & Fallbacks

| Risk | Likelihood | Impact | Fallback |
|---|---|---|---|
| **YouTube channel IDs are stale/wrong** | Medium — some from feedspot data, some from public knowledge | Cannot fetch channel data, blocks entire channel | Pre-harvest validation: verify each channel ID via 1 API call before starting. If wrong, search by handle (`channels.list(forHandle=...)`) — costs 1 unit. |
| **Two Minute Papers has fewer real playlists than expected** | Low — channel page shows multiple playlist sections | Fat channel has weak sub-structure | Select a backup fat channel from the roster (3Blue1Brown or Veritasium — both known playlist-rich). Move Two Minute Papers to standard depth. |
| **API `playlists.list` returns non-public or empty playlists** | Low | Cannot populate playlist field for that channel | Mark playlists field as `null` for those videos. Note in reliability report. |
| **yt-dlp rate-limiting or blocking** | Low — 1.5s spacing has been safe | Harvest stalls | Increase spacing to 3s. If still blocked, switch to API `videos.list` for enrichment (50 videos per 1-unit call). |
| **Some channels have very few recent uploads** | Low | Harvest depth below target | Accept lower count for that channel. Do not fabricate or scrape beyond what's available. |
| **`video_count_total` returns 0 or wrong from API** | Very low | Planet sizing is wrong | `null` the field; prototype sizes planet by `harvested_video_count` as fallback. |
| **StarTalk / Kurzgesagt have mostly Shorts** | Medium | Dataset polluted with short-form content | Filter Shorts before enrichment. Use `--match-filters "duration > 60"` in yt-dlp or check `contentDetails.duration` via API to exclude videos under 60 seconds. |
| **3Blue1Brown channel ID in plan is wrong** | Low | Cannot fetch | Same fallback as above: verify in pre-harvest step. |

---

## 8. Proposed Checkpoints

Checkpoints where work **stops and requires explicit human approval** before continuing:

| # | Checkpoint | What I do first | What I ask | Approval gates what |
|---|---|---|---|---|
| **CP1** | **Plan approval** | Submit this plan | "Approve the plan to begin harvesting?" | Gates all execution |
| **CP2** | **Channel verification** | Validate all 18 YouTube channel IDs via API, list discovered playlists per channel, confirm catalog sizes | Show verified roster with actual playlist counts and catalog sizes. Ask: "Does this verified roster match expectations? Any channel you'd swap?" | Gates which channels proceed to harvest |
| **CP3** | **Fat channel probe** | Harvest 5 videos from each of the fat channel's playlists (1 per playlist), enrich all fields, verify | Show probe output with real playlist names and data quality. Ask: "Do these playlists provide enough sub-structure? Approve full fat channel harvest?" | Gates whether to proceed with full fat harvest or switch fat channel |
| **CP4** | **Full harvest complete, pre-review** | Complete all harvesting, write dataset JSON, generate reliability report | Show dataset stats, per-field completeness table, playlist coverage. Ask: "Review dataset and report. Approve as final?" | Gates final delivery |

**Between checkpoints, the script runs autonomously.** No mid-harvest questions unless a fallback condition triggers (e.g., a channel ID fails to resolve, which would halt that channel and report it).

---

## 9. v1 Failures Addressed — Compliance Checklist

| v1 failure | How this plan fixes it | Evidence |
|---|---|---|
| **1. Degenerate topic (1 channel)** | Minimum 5 channels per topic. Math expanded to 5 channels. | 3 topics, all ≥5 channels |
| **2. Fat channel had 1 catch-all playlist** | 5 distinct Two Minute Papers playlists targeted. Playlist discovery via API. | Section 2 lists 5 expected playlists + backup fat channels |
| **3. RSS 15-cap flattened harvest depth** | yt-dlp on uploads listings bypasses RSS. API `playlistItems.list` for playlists. | Depth plan in Section 3: 15-95 videos per channel, none at exactly 15 |
| **4. `video_count_total` was null everywhere** | API `channels.list(part=statistics)` populates real catalog sizes. | Section 4 method table: API-only field, null if unavailable |
| **5. No grouping fallback** | Explicit tiered strategy: playlists > tags > implicit (channel membership). Empty tags stay `[]`, no fabrication. | Section 5 grouping strategy |
| **6. No fabrication** | All IDs from real API/yt-dlp responses. Pre-harvest ID verification. | Checkpoint CP2 verifies all IDs before harvest |

---

## 10. Execution Script Design

A single Python script (`harvest_v2.py`) will implement the plan in phases:

1. **CP2 phase:** Validate all channel IDs, fetch playlist lists and catalog sizes via API. Output a verification report. **Stop for approval.**
2. **CP3 phase:** Fat channel probe — 1 video per playlist, full enrichment. Output probe. **Stop for approval.**
3. **CP4 phase:** Full harvest — enumerate playlists via API, enumerate uploads via yt-dlp, enrich all videos, build schema, write JSON. Output dataset + reliability report.

The script will use the YouTube Data API v3 key (provided by user) and yt-dlp in a venv (already set up from v1 at `/tmp/yt-env/bin/yt-dlp`).

---

**Awaiting approval before any harvesting.** Reply with "Approved" to proceed to CP2, or comment on any part you want changed.
