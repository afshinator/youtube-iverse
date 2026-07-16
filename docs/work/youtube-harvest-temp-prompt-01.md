# TASK: Test-and-Harvest — Public YouTube Dataset for an Offline Prototype

You are assembling a **real, offline, static dataset** of public YouTube data. A separate
3D data-visualization prototype will ship this dataset as a **static JSON file** and make
**no live API calls at runtime** — so everything you collect happens **once, now, offline**.

This is a **feasibility test first, harvest second.** I want to learn whether you can obtain
this data using the tools and methods available to you *without an API key* (via your browser,
code execution, or any other tools you can find). If a keyless method works, harvest the full
scoped dataset. If it doesn't, stop and tell me exactly what's missing — a clean "this field
isn't reachable this way" is a valuable result, not a failure.

**Do not fabricate any data.** If a value cannot be obtained, set it to `null` and record that
in the reliability report. Real, verifiable data or `null` — never invented numbers, titles,
or IDs. This rule is absolute; the entire point of this exercise is real-shaped data.

---

## Why each field matters (so you can make good judgment calls)

- **`id` (real YouTube video ID)** — *essential, non-negotiable.* The prototype derives both the
  thumbnail (`https://img.youtube.com/vi/<id>/hqdefault.jpg`) and playback (`https://www.youtube.com/watch?v=<id>`)
  directly from this. A video with no real ID is useless. Every ID must be genuine and resolve.
- **`playlist` (which channel playlist a video belongs to)** — *highest-value grouping signal.*
  Channel owners curate playlists by hand, so they're the best "these videos are related" data
  we can get. Capture this wherever possible.
- **`tags` and `title`** — *fallback grouping signals* when playlists are absent.
- **`view_count` / `like_count` / `comment_count` / `duration`** — drive visual sizing in the
  prototype. Nice to have; `null` is acceptable if unreachable.
- **`published_at`** — enables a "fresh vs. evergreen" view; `null` acceptable.

---

## PHASE A — Capability discovery (do this first, report before harvesting)

1. **Inventory your own tools.** List every tool you actually have that could fetch web data:
   browser/fetch, code execution (Python/Node/shell), any file or HTTP tools, any connectors.
2. **Research candidate methods** for pulling public YouTube data *without an API key*. Investigate
   at least the avenues below — but treat them as **leads, not an exhaustive list**; look for
   others and prefer whatever proves most reliable:
   - **Channel RSS feed:** `https://www.youtube.com/feeds/videos.xml?channel_id=<UC...>` — keyless,
     returns roughly the ~15 most recent uploads with real IDs, titles, and dates. Reliable but shallow.
   - **`yt-dlp`** (if you can execute code): can list a channel's or playlist's full contents and
     dump per-video metadata as JSON, keyless. Powerful if available to you.
   - **Invidious / Piped public instances:** alternative YouTube front-ends that expose structured
     JSON for channels, playlists, and videos. Worth probing.
   - **Embedded page JSON:** the `ytInitialData` / `ytInitialPlayerResponse` blobs inside channel
     and watch-page HTML contain structured metadata if parsed.
   - **YouTube Data API v3** — *fallback only.* Needs a key. If keyless methods can't get the
     required fields, say so and ask me whether to supply a key; don't assume one.
3. **Report** which methods you found, which you can **actually execute** (some you may identify
   but not be able to run), and your recommended primary method — **before** collecting a full dataset.

---

## PHASE B — Feasibility probe (small sample, then show me)

Using your best keyless method, pull **one channel and ~5 of its videos** end to end. Then show me:

- The raw sample in the target schema below.
- **Per-field, which values you actually got vs. `null`**, and by what method.
- Whether you could obtain **playlist membership** for those videos (call this out specifically —
  it's the field most likely to be hard, and the most valuable).
- **Verify the IDs are real:** confirm a couple of the thumbnail URLs actually load.

**Decision gate:** proceed to Phase C **only if** the probe reliably yields, at minimum:
real `id`, `title`, `channel` name, and *some* grouping signal (playlist **or** tags **or**
usable titles). If it can't, **stop here** and report the gap — do not brute-force or fabricate.

---

## PHASE C — Full harvest (only if the probe passed)

Harvest a dataset shaped for a two-mode 3D visualization (channels-as-systems and
topics-as-systems), so it must be organized as **topics → channels → videos**:

- **2–3 topics** (e.g. broad areas like "AI", "Cooking", "Space"). Pick topics rich in active channels.
- **Per topic, 3–8 channels.** Make **at least one topic "busy"** (toward 8 channels) so dense
  layout gets tested.
- **At least one deliberately "fat" channel:** harvest **many** of its videos (aim for 50+, up to
  ~150) so the prototype's high-density handling gets a real workout. Other channels: ~5–20 videos each.
- **Prefer channels that use playlists**, and **capture playlist membership** — this is the payload
  that makes the grouping feature real rather than faked.
- Assign each channel to a **single primary topic** (a simplification — real channels span topics,
  but one-topic-per-channel keeps the dataset clean for the prototype).

Total size is flexible; roughly **150–300 videos** is plenty. Bigger isn't better — *real and
well-grouped* beats *large*.

---

## OUTPUT 1 — The dataset, in exactly this JSON schema

```json
{
  "meta": {
    "harvested_at": "<ISO 8601 timestamp>",
    "method_used": "<the method(s) that produced this data>",
    "notes": "<anything I should know: blockers, partial fields, caveats>"
  },
  "topics": [
    {
      "id": "topic_ai",
      "label": "Artificial Intelligence",
      "channel_ids": ["chan_two_minute_papers", "chan_..."]
    }
  ],
  "channels": [
    {
      "id": "chan_two_minute_papers",
      "youtube_channel_id": "UCbfYPyITQ-7l4upoX8nvctg",
      "name": "Two Minute Papers",
      "topic_id": "topic_ai",
      "video_count_total": 900,
      "harvested_video_count": 60,
      "video_ids": ["kK...", "..."]
    }
  ],
  "videos": [
    {
      "id": "kK9dTX1KX_s",
      "title": "<real title>",
      "channel_id": "chan_two_minute_papers",
      "published_at": "2024-05-01T00:00:00Z",
      "duration_seconds": 372,
      "view_count": 123456,
      "like_count": 6789,
      "comment_count": 234,
      "tags": ["neural rendering", "graphics"],
      "playlist": "Neural Rendering",
      "thumbnail_url": "https://img.youtube.com/vi/kK9dTX1KX_s/hqdefault.jpg"
    }
  ]
}
```

Rules for the JSON:
- **Every `videos[].id` must be a real, resolving YouTube video ID.** No placeholders.
- `youtube_channel_id` should be the real `UC...` ID **if you can get it**; otherwise `null`.
- `video_count_total` = the channel's real total upload count **if visible**; otherwise `null`.
  (Distinct from `harvested_video_count`, which is how many you actually collected.)
- Unobtainable scalar fields → `null`. Unobtainable lists (`tags`) → `[]`.
- `thumbnail_url` is just the ID slotted into the pattern above — always fill it once you have the ID.
- Emit valid, parseable JSON. If it's large, that's fine — completeness over brevity.

## OUTPUT 2 — Reliability report (this is as important as the data)

After the JSON, give me a short written report:

- **Method(s) that worked**, and which you tried and abandoned (and why).
- **Per-field reliability table:** for `id`, `title`, `channel name`, `youtube_channel_id`,
  `published_at`, `duration`, `view_count`, `like_count`, `comment_count`, `tags`, `playlist` —
  mark each as **Reliable / Partial / Unavailable** with a one-line note.
- **Playlist verdict specifically:** could you get real playlist membership, and how?
- **Blockers hit** (rate limits, blocks, missing fields) and whether an **API key would fix them**.
- **Your recommendation:** is keyless scraping good enough for this dataset, or should we switch the
  offline harvest to the YouTube Data API? Be blunt.

---

## Constraints & conduct

- **Public data only.** No login, no private data, no auth.
- **Be gentle:** space out requests, respect rate limits, don't hammer any endpoint or instance.
- **Prefer official/lightweight methods** (RSS, API) over heavy page-scraping where they suffice.
- **Honesty over completeness:** if a method feels like it violates a site's terms, say so and let
  me decide — don't silently push through, and don't fake data to fill a gap.
- If you get blocked or a field is simply unreachable, **that is a reportable result** — capture it
  and move on rather than forcing it.