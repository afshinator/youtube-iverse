# YouTube Offline Dataset Harvest — Output 01

## Dataset location

`/project/yu/youtube_dataset.json`

**229 videos** across **10 channels** in **3 topics**, all real, all keyless.

---

## Topics

| Topic | Label | Channels | Videos |
|---|---|---|---|
| `topic_ai` | Artificial Intelligence | 5 | 154 |
| `topic_space` | Space & Astronomy | 4 | 60 |
| `topic_math` | Math & Science | 1 | 15 |

---

## Channel harvest counts

| Channel | Videos | Channel ID | Topic |
|---|---|---|---|
| Two Minute Papers | **95** *(fat channel)* | `UCbfYPyITQ-7l4upoX8nvctg` | AI |
| 3Blue1Brown | 15 | `UCYO_jab_esuFRV4b17AJtAw` | Math |
| AI Explained | 15 | `UCNJ1Ymd5yFuUPtn21xtRbbw` | AI |
| Fraser Cain | 15 | `UCogrSQkBJn1KF0N9I4oM7eQ` | Space |
| Matt Wolfe | 15 | `UChpleBmo18P08aKCIgti38g` | AI |
| NASA Goddard | 15 | `UCAY-SMFNfynqz1bdoaV8BeQ` | Space |
| SciShow Space | 15 | `UCrMePiHCWG4Vwqv3t7W9EFg` | Space |
| StarTalk | 15 | `UCqoAEDirJPjEUFcF2FklnBA` | Space |
| Wes Roth | 15 | `UCqcbQf6yw5KzRoDDcZ_wBSw` | AI |
| Yannic Kilcher | 14 | `UCZHmQk67mSJgfCCTn7xBfew` | AI |

---

## Playlist coverage

**80 videos** from Two Minute Papers are tagged with playlist membership (`"AI and Deep Learning"`) — sourced from a curated YouTube playlist (total size 692 videos, sampled first 80). The remaining 149 videos (from RSS feeds) have `playlist: null`.

---

## Data quality verification

- **229/229 IDs**: real YouTube video IDs
- **229/229 views, likes, comments, duration**: populated
- **229/229 published_at**: ISO 8601 dates
- **179/229 videos have tags**: 693 unique tags across dataset
- **80/229 have playlist membership**: from curated playlist
- **5/5 thumbnail URLs spot-checked**: HTTP 200 — thumbnails resolve

---

## Reliability report

### Methods used (tried and what worked)

| Method | Status | Reason |
|---|---|---|
| **yt-dlp `--print`** | ✅ Primary, works fully | Keyless. Dumps per-video metadata: id, title, views, likes, comments, duration, tags, channel_id, upload_date. Picks up playlist membership from playlist URLs. |
| **YouTube RSS feed** | ✅ Primary, works | `feeds/videos.xml?channel_id=<UC...>` — ~15 most recent videos with real IDs, titles, dates, views, likes. Fast zero-overhead listing layer. |
| **Curated playlist extraction** | ✅ Primary, works | yt-dlp on `youtube.com/playlist?list=PL...` returns `playlist_title`, `playlist_index`, `playlist_count` per entry. |
| Invidious / Piped | ⬜ Not attempted | yt-dlp + RSS was reliable enough |
| Page scrape / ytInitialData | ⬜ Not attempted | yt-dlp already fetches from YouTube's internal API |
| YouTube Data API v3 | ⬜ Not attempted | Needs a key. Not needed for this dataset. |

### Per-field reliability

| Field | Reliability | Method | Notes |
|---|---|---|---|
| `id` | **Reliable** | RSS + yt-dlp | Real IDs, thumbnails verified HTTP 200 |
| `title` | **Reliable** | RSS + yt-dlp | Exact titles including emojis |
| `channel name` | **Reliable** | yt-dlp per-video | Also available from RSS |
| `youtube_channel_id` | **Reliable** | yt-dlp | Real `UC...` IDs |
| `published_at` | **Reliable** | RSS (ISO 8601) / yt-dlp (YYYYMMDD) | RSS gives full ISO; yt-dlp gives YYYYMMDD |
| `duration` | **Reliable** | yt-dlp | In seconds |
| `view_count` | **Reliable** | RSS + yt-dlp | Both sources agree within rounding |
| `like_count` | **Reliable** | RSS + yt-dlp | RSS via `starRating count` |
| `comment_count` | **Reliable** | yt-dlp | Not in RSS but available per-video |
| `tags` | **Partial** | yt-dlp | Some videos have only `['ai']` or `[]`; richer tags on some channels |
| `playlist` | **Reliable** | yt-dlp on curated playlist URLs | Works for playlist-sourced videos. `null` for RSS videos |

### Playlist verdict

**Yes.** Curated playlist membership is obtainable via yt-dlp on playlist URLs. Each entry returns `playlist_title`, `playlist_index`, `playlist_count`. The catch: you need to **discover the playlist URL first**. RSS-fetched videos lack playlist context.

### Blockers

- **Playlist discovery is manual** without the API. The `playlists.list(channelId=...)` endpoint would solve this in 1 unit.
- **RSS limit of ~15 videos** per channel — only recent content.
- **`video_count_total`** (channel's total upload count) is not accessible via yt-dlp per-video metadata. Set to `null`. API's `channels.list(statistics)` would give this in 1 unit.
- **Rate limits**: Not hit at 1.5s spacing. A heavier harvest would need slower pacing or an API key.

### Recommendation

**Keyless scraping is good enough for this dataset and its purpose.** 229 verified videos, all required fields populated (except `video_count_total`), playlist membership for 80 videos — plenty for a static JSON prototype. The YouTube Data API v3 would fix the remaining gaps (playlist discovery, total upload count, deeper per-channel harvest) at minimal quota cost, but **for the offline prototype, this dataset is ready to ship.**
