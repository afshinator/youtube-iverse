# CP2-REDO DIRECTIVE — Keyless. No API key.

This supersedes CP2's "need an API key" conclusion. The blockers you cited are not real: you
already obtained real playlist sizes **keyless** in v1. Redo CP2 properly, keyless, then STOP.

---

## 0. Rejected: the API-key path

Do **not** request or use an API key. Your §3 claim that real playlist `itemCount` and
`video_count_total` are "API only" is contradicted by your own prior work:

- **In v1 you reported the "AI and Deep Learning" playlist's total size as 692 videos.** That is a
  real playlist item-count, obtained keyless. You already did the thing you now call impossible.
- **Your CP2 §4 table states:** "Full playlist enumeration ✅ Works — yt-dlp on individual playlist
  URLs." Enumerating a playlist returns its real `playlist_count` **and** its video IDs.
- **The v1 reliability report documented** that yt-dlp on `youtube.com/playlist?list=PL...` returns
  `playlist_title`, `playlist_index`, and `playlist_count` per entry.

The "13/page artifact" you hit came from `--flat-playlist` on the channel's `/playlists` **tab**,
which is the wrong call for sizing. Query each **individual playlist URL** instead.

---

## 1. Keyless methods for the two "impossible" values

- **Real playlist `itemCount`:** for each discovered playlist ID, run yt-dlp on its individual URL
  and read `playlist_count`. Illustrative:
  `yt-dlp --flat-playlist -I 1:1 -O "%(playlist_count)s" "https://www.youtube.com/playlist?list=PLxxxx"`
  (flat + one item = fast; you only need the count here, video IDs come at harvest time).
- **Real `video_count_total`:** flat-enumerate the channel's long-form uploads and read
  `playlist_count`. Illustrative:
  `yt-dlp --flat-playlist -I 1:1 -O "%(playlist_count)s" "https://www.youtube.com/channel/UC...id.../videos"`
  This is the **long-form upload count** (Shorts are a separate tab and are excluded) — which is
  exactly what we want for planet sizing. Record it as `video_count_total` and note "long-form" in
  the manifest. Only if this genuinely returns nothing after retry may you set it `null`, with the
  failure logged (R4).

Adjust flags to whatever your yt-dlp version needs; the requirement is the **value**, obtained
keyless. If a specific channel resists, retry with slower pacing before declaring it unavailable.

---

## 2. Fix the real CP2 failures (keyless)

- **sentdex — resolve by handle, do not replace first.** Run yt-dlp on
  `https://www.youtube.com/@sentdex/videos` and use whatever real `UC...` ID it returns. Do **not**
  hardcode a guessed ID. Only if the handle truly fails to resolve after retry may you substitute a
  different active AI/ML channel — and if so, state which and why.
- **Topic floor:** after sentdex resolves, confirm AI = 8 channels (floor is 5). Report the count.

---

## 3. Apply the ORIGINAL §4 rule — unchanged — with the now-real data

Do **not** use a "modified keyless rule." The data is obtainable, so the real rule stands. For the
three fat candidates (Two Minute Papers, 3Blue1Brown, Veritasium):

1. Get real `video_count_total` (§1) for each.
2. Get real `playlist_count` (§1) for **every** discovered playlist.
3. Exclude a playlist if **any** of:
   - `itemCount ≥ 80% of video_count_total` (catch-all), or
   - it is a translation / language-duplicate playlist (by title, e.g., "Russian translations",
     "Hindi translations"), or
   - `itemCount < 8`.
4. **Qualifying** = survives all exclusions. A candidate **qualifies as fat-with-grouping** if it has
   **≥3 qualifying playlists** whose combined items total **≥40**.
5. **Select** the qualifying candidate with the largest combined harvest across its top distinct
   playlists (tie → density). A genuine "none qualify" is only acceptable if it follows from **real
   counts failing the thresholds** — not from data being unavailable.

Given what you already discovered (TMP: Fluid/Cloth/Hair Simulations, Light Transport & Ray Tracing,
DeepMind explained, ChatGPT/GPT4…, NVIDIA RTX, VR/Metaverse, 3D Printing; 3B1B: Neural Networks,
Essence of Calculus, Essence of Linear Algebra, Differential Equations, Physics), at least one
candidate is very likely to qualify once real counts are attached. Let the numbers decide.

---

## 4. Cost / pacing

All of the above is flat metadata (no video downloads): ~50 playlist-count calls + 3 channel-total
calls + 1 handle resolve. Pace ~1s/call. This is well inside v1's proven keyless footprint. No key,
no quota.

---

## 5. Output, then STOP

Re-emit the CP2 report containing:
- sentdex resolution result (real ID or justified replacement);
- real `video_count_total` for all 18 channels;
- for each fat candidate, a table of **every** playlist with its **real `playlist_count`** and its
  exclusion flags (catch-all / translation / <8);
- the §4 selection: exactly one fat channel, or a genuine "none qualify" backed by real counts;
- confirmation that AI topic ≥ 5.

Then **STOP** and await approval. Do not proceed to CP3.