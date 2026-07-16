# CP4 Results — Full Harvest + Self-Audit

**Status: STOPPED — awaiting final approval.**

**Dataset:** `/project/yu/youtube_dataset.json` (564 videos)

---

## Harvest summary

| Channel | Videos | Type |
|---|---|---|
| Veritasium | 104 | Showcase — 6 clusters |
| Two Minute Papers | 60 | AI cluster — 3 playlists |
| Wes Roth | 25 | Flat |
| AI Explained | 25 | Flat |
| Matt Wolfe | 25 | Flat |
| Yannic Kilcher | 25 | Flat |
| sentdex | 25 | Flat |
| AI and Games | 25 | Flat |
| Robert Miles AI Safety | 25 | Flat |
| Fraser Cain | 25 | Flat |
| SciShow Space | 25 | Flat |
| StarTalk | 25 | Flat |
| NASA Goddard | 25 | Flat |
| Dr. Becky | 25 | Flat |
| 3Blue1Brown | 25 | Flat |
| Numberphile | 25 | Flat |
| Kurzgesagt | 25 | Flat |
| Steve Mould | 25 | Flat |
| **TOTAL** | **564** | |

---

## Veritasium showcase — 6 clusters, 0% pairwise overlap

| Cluster | Videos |
|---|---|
| Physics | 11 |
| Engineering | 14 |
| Math | 15 |
| Biology | 18 |
| Space | 15 |
| Psychology | 17 |

All 15 cluster pairs: 0.0% overlap. All ≥8 videos.

## Two Minute Papers AI cluster — 3 playlists, 0% pairwise overlap

| Cluster | Videos |
|---|---|
| ChatGPT, GPT4, OpenAI | 20 |
| DeepMind explained | 20 |
| NVIDIA RTX, AI | 20 |

All 3 pairs: 0.0% overlap. All ≥8 videos.

---

## §8 Self-audit — ALL PASS

| Check | Result |
|---|---|
| Counts reconcile | PASS — sum(harvested)=564 == len(videos)=564 |
| Topic floor (≥5) | PASS — AI:8, Space:5, Science:5 |
| ID reality (10 random thumbnails HTTP 200) | PASS — 10/10 |
| No Shorts (≤60s) | PASS — 0 found |
| External-video filter | PASS — 0 unknown channel_ids |
| Single label | PASS — 0 multi-playlist violations |
| Sizing populated (video_count_total) | PASS — 0 nulls |
| VS cluster ≥8 videos each | PASS — 6/6 |
| VS all pairwise overlap <30% | PASS — all 0.0% |
| TMP cluster ≥8 videos each | PASS — 3/3 |
| TMP all pairwise overlap <30% | PASS — all 0.0% |
| Playlist provenance (all match CP2 titles) | PASS — 0 unknown |
| Grouping honesty: no playlist AND no tags | **142/564 (25.2%)** |

---

## Per-field null/empty

| Field | Present | Null/Empty |
|---|---|---|
| id, title, channel_id, published_at, duration, views, likes | 564/564 | 0 |
| comment_count | 558/564 | 6 null |
| tags | 564/564 | 142 empty `[]` |
| playlist | 150/564 | 414 null (flat channels) |

All fields sourced via yt-dlp. `video_count_total` from CP2-REDO UU playlist.

---

**CP4 COMPLETE. Dataset ready for delivery. Awaiting approval.**
