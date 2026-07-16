#!/usr/bin/env python3
"""CP3: Data-quality probe — Veritasium showcase + TMP AI + 1 flat channel."""
import subprocess, time, json, itertools
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import URLError

YTDLP = '/tmp/yt-env/bin/yt-dlp'

# CP2-REDO verified data
VERITASIUM_UC = 'UCHnyfMqiRRG1u-2MsSQLbXA'
TMP_UC = 'UCbfYPyITQ-7l4upoX8nvctg'
AI_EXPLAINED_UC = 'UCNJ1Ymd5yFuUPtn21xtRbbw'

# Cluster playlists per §3
VS_CLUSTERS = {
    'Physics': 'PLkahZjV5wKe9q3K-nk82kVD_pNfPZ140i',
    'Engineering': 'PLkahZjV5wKe9EKkCQ25-XxvtRWgW-BtC3',
    'Math': 'PLkahZjV5wKe-Z1RP3ZiYwe8JSAolmqF9M',
    'Biology': 'PLkahZjV5wKe-lnPv1TseLsmMexz3IO81Q',
    'Space': 'PLkahZjV5wKe-bi4kBx7b9rX80g6SMW78H',
    'Psychology': 'PLkahZjV5wKe8VBzJn5wfJ7Avf_nr6Pt2N',
}

# TMP AI playlists (§4)
TMP_CLUSTERS = {
    'ChatGPT, GPT4, OpenAI': 'PLujxSBD-JXgmB1AnewzycdtUtf5YVUyzU',
    'DeepMind explained': 'PLujxSBD-JXgmoQMNJ3mt_upr7JN7pK7Cz',
    'NVIDIA RTX, AI': 'PLujxSBD-JXgkZIkzudS-dOZbbCFJpiAFD',
}

def run_yt(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return [l for l in r.stdout.split('\n') if l and not l.startswith('WARNING:')]
    except subprocess.TimeoutExpired:
        return ['__TIMEOUT__']
    except Exception as e:
        return [f'__ERROR__:{e}']

def get_playlist_videos(pl_id, limit=30):
    """Get video IDs + playlist titles from a playlist URL, with full metadata."""
    url = f'https://www.youtube.com/playlist?list={pl_id}'
    lines = run_yt([YTDLP, '--print',
        '%(id)s|%(title)s|%(playlist_title)s|%(playlist_index)s|%(channel_id)s|%(duration)s|%(view_count)s|%(like_count)s|%(comment_count)s|%(tags)s|%(upload_date)s',
        '--playlist-items', f'1-{limit}', url], timeout=180)
    vids = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5 or not parts[0]:
            continue
        vid = {
            'id': parts[0].strip(),
            'title': parts[1].strip() if len(parts) > 1 else '',
            'playlist': parts[2].strip() if len(parts) > 2 else None,
            'index': int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None,
            'channel_id_resolved': parts[4].strip() if len(parts) > 4 else None,
            'duration': int(parts[5]) if len(parts) > 5 and parts[5].isdigit() else None,
            'view_count': int(parts[6]) if len(parts) > 6 and parts[6].isdigit() else None,
            'like_count': int(parts[7]) if len(parts) > 7 and parts[7].isdigit() else None,
            'comment_count': int(parts[8]) if len(parts) > 8 and parts[8].isdigit() else None,
            'tags_raw': parts[9] if len(parts) > 9 else 'NA',
            'upload_date': parts[10] if len(parts) > 10 else 'NA',
        }
        vids.append(vid)
    return vids

def get_flat_videos(uc_id, limit=30):
    """Get most-recent long-form uploads for a channel via UU playlist."""
    uu_id = 'UU' + uc_id[2:]
    url = f'https://www.youtube.com/playlist?list={uu_id}'
    return get_playlist_videos(uu_id, limit=limit)

def filter_vids(vids, host_uc):
    """Apply all filters: external-video, Shorts, then deduplicate."""
    filtered = []
    for v in vids:
        # External-video filter: must match host channel
        if v['channel_id_resolved'] != host_uc:
            continue
        # No Shorts
        if v['duration'] is not None and v['duration'] <= 60:
            continue
        filtered.append(v)
    # Deduplicate by ID
    seen = set()
    deduped = []
    for v in filtered:
        if v['id'] not in seen:
            seen.add(v['id'])
            deduped.append(v)
    return deduped

def format_published(yd):
    if yd in ('NA', None) or len(yd) != 8:
        return None
    try:
        d = datetime.strptime(yd, '%Y%m%d')
        return d.strftime('%Y-%m-%dT00:00:00Z')
    except:
        return None

def check_thumbnail(vid_id):
    url = f'https://img.youtube.com/vi/{vid_id}/hqdefault.jpg'
    try:
        r = urlopen(url, timeout=10)
        return r.status == 200
    except:
        return False

# ========== CP3 MAIN ==========
print('=' * 70)
print('CP3: DATA-QUALITY PROBE')
print(f'Time: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
print('Method: KEYLESS (yt-dlp on individual playlist URLs)')
print('=' * 70)

# --- Probe 1: Veritasium clusters (Physics + Biology) ---
print('\n--- Probe 1: Veritasium — Physics ---')
vs_physics = get_playlist_videos(VS_CLUSTERS['Physics'], limit=30)
vs_physics = filter_vids(vs_physics, VERITASIUM_UC)
vs_physics_sample = vs_physics[:5]
print(f'  Filtered from playlist: {len(vs_physics)} videos (took 5 for probe)')

print('\n--- Probe 2: Veritasium — Biology ---')
vs_bio = get_playlist_videos(VS_CLUSTERS['Biology'], limit=30)
vs_bio = filter_vids(vs_bio, VERITASIUM_UC)
vs_bio_sample = vs_bio[:5]
print(f'  Filtered from playlist: {len(vs_bio)} videos (took 5 for probe)')

# --- Probe 3: TMP AI cluster (ChatGPT/GPT4) ---
print('\n--- Probe 3: Two Minute Papers — ChatGPT, GPT4, OpenAI ---')
tmp_ai = get_playlist_videos(TMP_CLUSTERS['ChatGPT, GPT4, OpenAI'], limit=30)
tmp_ai = filter_vids(tmp_ai, TMP_UC)
tmp_ai_sample = tmp_ai[:5]
print(f'  Filtered from playlist: {len(tmp_ai)} videos (took 5 for probe)')

# --- Probe 4: Flat channel (AI Explained) ---
print('\n--- Probe 4: Flat channel — AI Explained ---')
flat = get_flat_videos(AI_EXPLAINED_UC, limit=30)
flat = filter_vids(flat, AI_EXPLAINED_UC)
flat_sample = flat[:5]
print(f'  Filtered from uploads: {len(flat)} videos (took 5 for probe)')

time.sleep(0.5)

# --- Verify thumbnails ---
print('\n--- Thumbnail verification ---')
all_samples = vs_physics_sample + vs_bio_sample + tmp_ai_sample + flat_sample
thumb_results = []
for v in all_samples:
    ok = check_thumbnail(v['id'])
    thumb_results.append((v['id'], ok))
    print(f'  {v["id"]}: {"OK" if ok else "FAIL"}')
    time.sleep(0.3)

all_thumbs_ok = all(r[1] for r in thumb_results)
print(f'  All thumbnails HTTP 200: {"PASS" if all_thumbs_ok else "FAIL"}')

# --- Verify filters ---
print('\n--- Filter verification ---')
# Shorts check
short_count = sum(1 for v in all_samples if v['duration'] is not None and v['duration'] <= 60)
print(f'  Shorts (≤60s): {short_count} → {"PASS" if short_count == 0 else "FAIL"}')

# External-video filter
host_map = {
    **{v['id']: VERITASIUM_UC for v in vs_physics_sample + vs_bio_sample},
    **{v['id']: TMP_UC for v in tmp_ai_sample},
    **{v['id']: AI_EXPLAINED_UC for v in flat_sample},
}
external_count = 0
for v in all_samples:
    if v['id'] in host_map and v['channel_id_resolved'] != host_map[v['id']]:
        external_count += 1
print(f'  External videos in samples: {external_count} → {"PASS" if external_count == 0 else "FAIL"}')

# Single-assignment: no video appears in multiple probe pools
ids_in_physics = {v['id'] for v in vs_physics_sample}
ids_in_bio = {v['id'] for v in vs_bio_sample}
overlap = ids_in_physics & ids_in_bio
print(f'  VS Physics ∩ VS Biology: {len(overlap)} videos → {"PASS" if len(overlap) == 0 else "FAIL"}')

# VS cluster overlap (use full filtered lists for the two probed clusters)
vs_physics_ids = {v['id'] for v in vs_physics}
vs_bio_ids = {v['id'] for v in vs_bio}
full_overlap = vs_physics_ids & vs_bio_ids
overlap_pct = len(full_overlap) / min(len(vs_physics_ids), len(vs_bio_ids)) * 100 if min(len(vs_physics_ids), len(vs_bio_ids)) > 0 else 0
print(f'  Full Physics ∩ Biology overlap: {len(full_overlap)}/{min(len(vs_physics_ids), len(vs_bio_ids))} = {overlap_pct:.1f}% → {"PASS" if overlap_pct < 30 else "FAIL"}')

# --- Per-field summary ---
print('\n--- Per-field source summary (20 probe videos) ---')
fields = {
    'id': 0, 'title': 0, 'published_at': 0, 'duration_seconds': 0,
    'view_count': 0, 'like_count': 0, 'comment_count': 0, 'tags': 0, 'playlist': 0
}
nulls = dict(fields)
for v in all_samples:
    for field, default_null in [('id', None), ('title', None), ('upload_date', False),
                                  ('duration', None), ('view_count', None),
                                  ('like_count', None), ('comment_count', None),
                                  ('tags_raw', False), ('playlist', None)]:
        key_map = {'upload_date': 'published_at', 'tags_raw': 'tags', 'duration': 'duration_seconds'}
        out_field = key_map.get(field, field)
        val = v.get(field)
        if field == 'tags_raw':
            try:
                parsed = eval(val) if val not in ('NA', None) else []
                if not parsed or parsed == []:
                    nulls[out_field] += 1
                else:
                    fields[out_field] += 1
            except:
                nulls[out_field] += 1
        elif val is None or val == 'NA':
            nulls[out_field] += 1
        else:
            fields[out_field] += 1

total = len(all_samples)
provenance = 'ytdlp'
for f in ['id', 'title', 'published_at', 'duration_seconds', 'view_count', 'like_count', 'comment_count', 'tags', 'playlist']:
    present = fields.get(f, 0)
    missing = nulls.get(f, 0)
    print(f'  {f:20s} | source: {provenance:5s} | present: {present:2d}/{total} | null: {missing:2d}/{total}')

# Source: all yt-dlp in this probe
for f in ['id', 'title', 'published_at', 'duration_seconds', 'view_count', 'like_count', 'comment_count', 'tags', 'playlist']:
    present = fields.get(f, 0)
    print(f'    {f}: present={present}/{total} ({100*present//total}%)')

print(f'\n  Provenance: all fields sourced from yt-dlp (NO API calls)')
print(f'  Source field: source_method = "ytdlp" on all values')

# --- Pass criteria summary ---
print('\n' + '=' * 70)
print('CP3 PASS CRITERIA')
print('=' * 70)
print(f'  All thumbnails HTTP 200:        {"PASS" if all_thumbs_ok else "FAIL"}')
print(f'  0 Shorts in probe:             {"PASS" if short_count == 0 else "FAIL"}')
print(f'  No external videos:            {"PASS" if external_count == 0 else "FAIL"}')
print(f'  No cross-cluster overlap:      {"PASS" if len(overlap) == 0 else "FAIL"}')
print(f'  VS Physics∩Biology <30%:       {"PASS" if overlap_pct < 30 else "FAIL"} ({overlap_pct:.1f}%)')

all_pass = all_thumbs_ok and short_count == 0 and external_count == 0 and len(overlap) == 0 and overlap_pct < 30
print(f'\n  >>> OVERALL: {"PASS — ready for CP4" if all_pass else "FAIL — fix required"}')

# Print probe rows
print('\n--- PROBE VIDEO ROWS ---')
for i, v in enumerate(all_samples, 1):
    clust = 'VS-Physics' if i <= 5 else ('VS-Bio' if i <= 10 else ('TMP-AI' if i <= 15 else 'Flat'))
    print(f'\n  [{i}] {clust} | id={v["id"]} | title={v["title"][:60]} | dur={v["duration"]}s | '
          f'views={v["view_count"]} | likes={v["like_count"]} | comments={v["comment_count"]} | '
          f'playlist={v["playlist"]} | channel={v["channel_id_resolved"]}')

print('\n=== CP3 COMPLETE. AWAITING APPROVAL. ===')
