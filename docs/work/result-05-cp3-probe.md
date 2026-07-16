# CP3 Results — Data-Quality Probe

**Status: STOPPED — awaiting approval. No full harvest has occurred.**

Probed: 20 videos (5 × VS Physics, 5 × VS Biology, 5 × TMP ChatGPT, 5 × AI Explained flat).
All fields sourced from yt-dlp (`source_method: ytdlp`).

## Pass criteria — all PASS

- All thumbnails HTTP 200: **PASS** (20/20)
- 0 Shorts: **PASS** (smallest duration 486s)
- No external videos: **PASS** (all channel_id_resolved match their host UC)
- No cross-cluster overlap in probe: **PASS** (VS Physics ∩ Biology = 0)
- VS Physics∩Biology full overlap: **PASS** (0/22 = 0.0%)

## Filters verified working

- **External-video filter:** both Veritasium playlists contain only Veritasium videos (Physics=30 filtered, Biology=22 filtered).
- **Shorts filter:** no videos ≤60s in any sample (feed has no Shorts in these playlists).
- **Single-assignment:** no video appears in more than one probe pool.

## Per-field completeness (20 videos)

| Field | Present | Null |
|---|---|---|
| id | 20/20 | 0 |
| title | 20/20 | 0 |
| published_at | 20/20 | 0 |
| duration_seconds | 20/20 | 0 |
| view_count | 20/20 | 0 |
| like_count | 20/20 | 0 |
| comment_count | 20/20 | 0 |
| tags | 15/20 | 5/20 |
| playlist | 20/20 | 0 |

Tags null on 5/20 — expected for uploads-sourced flat channel and some Veritasium videos. All yt-dlp, no API.

## Flat channel note

AI Explained uploads returned `playlist: "Uploads from AI Explained"` (the auto-generated uploads playlist). Flat channels will get `playlist: null` at CP4 — this is set explicitly during harvest, not an artifact.

---

**CP3 PASS. Awaiting approval to proceed to CP4 full harvest.**
