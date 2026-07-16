# WORK ORDER: CP3 + CP4 Harvest — Veritasium Showcase + AI Cluster (ENFORCED)

Fat/showcase channel is now **Veritasium** (`chan_veritasium`, verified `UCHnyfMqiRRG1u-2MsSQLbXA`,
520 long-form uploads). This supersedes the earlier "Two Minute Papers" selection. CP2-REDO's verified
roster and real catalog sizes are accepted. Proceed keyless (no API key). Follow every rule; STOP where
told.

---

## 0. Informational — CP2-REDO oversight (NOT a rewrite request)

For the record, so it isn't repeated at CP4: CP2-REDO's playlist subtotals didn't reconcile — Two Minute
Papers was described as "19 playlists discovered" but only 13 were listed, and 3Blue1Brown's exclusion
breakdown summed to 25 against 24 discovered. These did **not** affect the fat-channel decision, so no
redo is needed. They are cited only to underline **§8's rule: CP4's self-audit must be computed in code,
not hand-typed.** No action required on CP2.

---

## 1. What we're building — three kinds of channel

1. **Showcase-cluster channel — Veritasium.** Harvested as clean, distinct subject clusters. This is the
   grouping-legibility + density proof (drill in → videos bloom into subject-neighborhoods).
2. **AI-cluster channel — Two Minute Papers** (`chan_two_minute_papers`, `UCbfYPyITQ-7l4upoX8nvctg`,
   1,079 uploads). Harvested as 2–3 distinct AI playlists so the dataset has a genuine AI cluster inside
   the busy AI topic.
3. **Flat channels — the other 16.** Shallow flat harvest, no playlist grouping (`playlist: null`), just
   to populate both universes with planets/moons.

---

## 2. Immutable rules (carry forward + new cleanup rules)

- **R1 no value without a real fetched source; R4 no fabrication** (null scalar / `[]` list for missing);
  **R5 provenance per field** (`api`|`ytdlp` — all `ytdlp` here); **R6 sizing:** planet size =
  `video_count_total` (already have real values), moon count = `harvested_video_count`; **R7 STOP = halt
  the run.**
- **NEW — Single cluster label per video.** Each video gets exactly one `playlist` value. If a harvested
  video appears in more than one chosen playlist, assign it to the **smallest** of those playlists (most
  specific), and log the collision.
- **NEW — External-video filter.** A playlist may contain videos from other channels. **Drop any video
  whose real `channel_id` ≠ the host channel's `UC…` id.** Every moon around a channel must actually be
  that channel's video. (This is what caused Veritasium/TMP playlist sums to exceed catalog size — it
  must be filtered out, not shipped.)
- **NEW — Soft-catch-all exclusion.** Beyond the §4 catch-all rule, **exclude any playlist ≥ 50% of the
  channel's catalog** from cluster use — it's too broad to be a sub-topic (this is why TMP's 692-video
  "AI and Deep Learning" list is not used).
- **NEW — Overlap gate.** After the external-video filter and single-assignment, any two clusters on the
  same channel must share **< 30%** of their videos. If a pair exceeds this, drop the larger of the two.
- **No Shorts.** Exclude any video with `duration_seconds ≤ 60`. Over-fetch and trim to target *after*
  excluding Shorts and non-channel videos, so counts don't silently fall short.

---

## 3. Veritasium harvest (showcase clusters)

- **Cluster playlists (clean, distinct subjects):** Physics, Engineering, Math, Biology, Space,
  Psychology. Use the real `PL…` IDs discovered at CP2. **Do NOT use** the "Favorites," "New Here? Try
  These!," or "Controversies/Fascinating Stories" playlists — they are curated cross-subject samplers
  and will overlap. (If, after filtering, a chosen subject drops below 8 real Veritasium videos, note it
  and drop that cluster rather than padding.)
- **Cap:** up to **~20 videos per cluster** (most-viewed or most-recent — pick one and state which),
  after the external-video and Shorts filters. Target ~100–120 Veritasium videos across ~6 clusters.
- Apply single-assignment + overlap gate (§2). Result: 5–6 clean, low-overlap subject clusters.

---

## 4. Two Minute Papers harvest (AI cluster)

- **Choose 2–3 distinct AI playlists** with the least mutual overlap. Candidates (real, from CP2):
  "ChatGPT, GPT4, OpenAI, Stable Diffusion and more!" (110), "DeepMind explained — AlphaFold and more!"
  (49), "NVIDIA RTX, AI, and more" (120). Prefer the pair/trio that overlaps least after filtering.
- **Exclude** "AI and Deep Learning" (692 — soft catch-all, >50% of catalog) and the "Two Minute Papers"
  catch-all (982).
- **Cap ~15–20 per playlist** after external-video + Shorts filters. Target ~40–60 TMP videos forming a
  clear AI cluster. Apply single-assignment + overlap gate.

---

## 5. Flat channels (the other 16)

- Harvest each channel's **~15–25 most-recent long-form videos** (exclude Shorts), full per-video
  metadata, `playlist: null`. Exact depth may vary; sizing is driven by `video_count_total` (already
  real from CP2), so flat harvested counts need not be varied.
- All 16 = every roster channel except Veritasium and Two Minute Papers.

---

## 6. Schema (unchanged — no new or renamed fields)

`topics[]`: `{id, label, channel_ids[]}`
`channels[]`: `{id, youtube_channel_id, name, topic_id, video_count_total, harvested_video_count, video_ids[]}`
`videos[]`: `{id, title, channel_id, published_at, duration_seconds, view_count, like_count, comment_count, tags[], playlist, thumbnail_url}`

- `video_count_total` = the real CP2-REDO long-form counts. `thumbnail_url` = `https://img.youtube.com/vi/<id>/hqdefault.jpg`.
- `playlist` carries the cluster label for Veritasium + TMP-AI videos; `null` for everything else.

---

## 7. CP3 — Data-quality probe (small, then STOP)

Do: harvest **5 videos from each of 2 Veritasium clusters + 1 TMP AI playlist + 1 flat channel**, fully
enriched. Apply all filters.
Pass criteria: every `id` resolves (thumbnail HTTP 200); 0 Shorts; every harvested video's `channel_id`
matches its host channel (external-video filter working); single-assignment produces exactly one label
per video; the two Veritasium clusters show < 30% overlap.
Output the probe rows + a per-field null/source summary. **Then STOP.** Ask: "Data quality good? Approve
full harvest?"

## 8. CP4 — Full harvest + self-audit (code-run, then STOP)

Do the full harvest per §3–§5, build the JSON (§6), then run this audit **in code** and paste its output
with a PASS/FAIL per line. Any FAIL → do not deliver; fix or report.

- **Counts reconcile:** `sum(harvested_video_count) == len(videos)`; per-topic sums printed and
  self-consistent — **no hand-typed subtotals** (this is the CP2 oversight guard).
- **Topic floor:** every topic ≥ 5 channels.
- **ID reality:** ≥10 random `thumbnail_url`s → HTTP 200.
- **No Shorts:** count of `duration_seconds ≤ 60` == 0.
- **External-video filter:** count of videos whose `channel_id` ≠ their host channel == 0.
- **Single label:** no video has more than one `playlist` value.
- **Cluster health:** for Veritasium and TMP, list each cluster with its final video count (each ≥ 8) and
  confirm all pairwise overlaps < 30%.
- **Playlist provenance:** every distinct non-null `playlist` value matches a real title fetched at CP2.
- **Sizing populated:** channels with null `video_count_total` == 0 (all are known real from CP2).
- **Grouping honesty line:** exact count and % of videos whose only signal is channel membership
  (`playlist` null AND `tags` empty).

**Then STOP.** Ask: "Approve dataset as final?"

---

**Begin at CP3. Probe, verify the filters work, then STOP.**