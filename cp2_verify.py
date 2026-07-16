#!/usr/bin/env python3
"""
CP2: Channel verification + fat-candidate playlist discovery (keyless, yt-dlp only)
Per work order §4: discovers playlists for 3 fat candidates, applies the DECISION RULE.
"""
import subprocess, re, json, time, sys
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import URLError

YTDLP = '/tmp/yt-env/bin/yt-dlp'

# ===== ALL 18 CHANNELS (with corrected typo chan_matt_wolfe) =====
ROSTER = [
    # --- AI (8) ---
    ('chan_two_minute_papers', 'Two Minute Papers', 'UCbfYPyITQ-7l4upoX8nvctg'),
    ('chan_wes_roth', 'Wes Roth', 'UCqcbQf6yw5KzRoDDcZ_wBSw'),
    ('chan_ai_explained', 'AI Explained', 'UCNJ1Ymd5yFuUPtn21xtRbbw'),
    ('chan_matt_wolfe', 'Matt Wolfe', 'UChpleBmo18P08aKCIgti38g'),
    ('chan_yannic_kilcher', 'Yannic Kilcher', 'UCZHmQk67mSJgfCCTn7xBfew'),
    ('chan_sentdex', 'sentdex', 'UCQ_hh4SdlGjY8rWxB7_JIfg'),
    ('chan_ai_and_games', 'AI and Games', 'UCov_51F0betb6hJ6Gumxg3Q'),
    ('chan_robert_miles', 'Robert Miles AI Safety', 'UCLB7AzTwc6VFZrBsO2ucBMg'),
    # --- Space (5) ---
    ('chan_fraser_cain', 'Fraser Cain', 'UCogrSQkBJn1KF0N9I4oM7eQ'),
    ('chan_scishow_space', 'SciShow Space', 'UCrMePiHCWG4Vwqv3t7W9EFg'),
    ('chan_startalk', 'StarTalk', 'UCqoAEDirJPjEUFcF2FklnBA'),
    ('chan_nasa_goddard', 'NASA Goddard', 'UCAY-SMFNfynqz1bdoaV8BeQ'),
    ('chan_dr_becky', 'Dr. Becky', 'UCYNbYGl89UUowy8oXkipC-Q'),
    # --- Math & General Science (5) ---
    ('chan_3blue1brown', '3Blue1Brown', 'UCYO_jab_esuFRV4b17AJtAw'),
    ('chan_numberphile', 'Numberphile', 'UCoxcjq-8xIDTYp3uz647V5A'),
    ('chan_veritasium', 'Veritasium', 'UCHnyfMqiRRG1u-2MsSQLbXA'),
    ('chan_kurzgesagt', 'Kurzgesagt', 'UCsXVk37bltHxD1rDPwtNM8Q'),
    ('chan_steve_mould', 'Steve Mould', 'UCEIwxahdLz7bap-VDs9h35A'),
]

# Fat channel candidates per §4
FAT_CANDIDATES = [
    'chan_two_minute_papers',
    'chan_3blue1brown',
    'chan_veritasium',
]

def run(cmd_args, timeout=60):
    try:
        r = subprocess.run(cmd_args, capture_output=True, text=True, timeout=timeout)
        lines = [l for l in r.stdout.split('\n') if l and not l.startswith('WARNING:')]
        errs = [l for l in r.stderr.split('\n') if l and 'WARNING' not in l]
        return lines, errs
    except subprocess.TimeoutExpired:
        return [], ['TIMEOUT']
    except Exception as e:
        return [], [str(e)]

def verify_channel(uc_id):
    """Verify a UC ID resolves by fetching the RSS feed (keyless, fast)."""
    url = f'https://www.youtube.com/feeds/videos.xml?channel_id={uc_id}'
    try:
        with urlopen(url, timeout=15) as r:
            data = r.read().decode('utf-8')
            # RSS feed is XML. Check for expected XML elements.
            if '<entry>' in data and '<yt:videoId>' in data:
                return True, 'RSS OK'
            elif 'error' in data.lower() or 'bad request' in data.lower():
                return False, 'RSS returned error'
            else:
                return False, f'RSS unexpected content ({len(data)} bytes)'
    except URLError as e:
        return False, f'RSS fetch failed: {e}'
    except Exception as e:
        return False, f'RSS error: {e}'

def check_channel_via_ytdlp(uc_id):
    """Verify via yt-dlp on the channel page (deeper but slower)."""
    lines, errs = run([YTDLP, '--print', '%(title)s;%(channel_id)s', '--playlist-items', '1-1',
                        f'https://www.youtube.com/channel/{uc_id}'], timeout=30)
    for line in lines:
        if uc_id in line:
            return True, f'yt-dlp OK: {line[:80]}'
    return False, 'yt-dlp could not resolve channel'

def discover_playlists_via_ytdlp(uc_id):
    """Discover playlists on a channel's playlists tab using yt-dlp.
    Returns list of {title, id, approx_count} dicts."""
    playlists = []
    url = f'https://www.youtube.com/channel/{uc_id}/playlists'
    lines, errs = run([YTDLP, '--print', '%(title)s;%(id)s;%(playlist_count)s',
                        '--flat-playlist', url], timeout=120)
    for line in lines:
        parts = line.split(';')
        if len(parts) >= 2:
            title = parts[0].strip()
            pl_id = parts[1].strip()
            count = parts[2].strip() if len(parts) > 2 and parts[2].isdigit() else None
            # Skip channel's "Created playlists" header entries
            if title.lower() in ('created playlists', 'uploads', 'liked videos'):
                continue
            if pl_id and not pl_id.startswith('UC'):  # Real playlist IDs start with PL
                playlists.append({
                    'title': title,
                    'pl_id': pl_id,
                    'item_count': int(count) if count else None,
                })
    return playlists

def apply_fat_rule(candidate_name, uc_id, video_count_total, playlists):
    """Apply §4 DECISION RULE.
    Returns (qualifies, qualifying_playlists, total_harvestable, reason)."""
    if video_count_total is None:
        return False, [], 0, 'video_count_total is null (keyless, API unavailable)'

    # Exclude catch-all: itemCount >= 80% of video_count_total
    qualifying = []
    excluded = []
    for pl in playlists:
        ic = pl.get('item_count')
        if ic is None:
            continue  # can't evaluate
        if ic >= 0.8 * video_count_total:
            excluded.append(pl)
        elif ic >= 8:
            qualifying.append(pl)

    if len(qualifying) < 3:
        return False, qualifying, sum(p['item_count'] or 0 for p in qualifying), \
               f'Only {len(qualifying)} qualifying playlists (need ≥3). {len(excluded)} excluded as catch-all.'

    total = sum(p['item_count'] or 0 for p in qualifying)
    if total < 40:
        return False, qualifying, total, f'Combined harvestable {total} < 40 threshold.'

    return True, qualifying, total, 'Meets all criteria'

def discover_channel_handle(uc_id):
    """Try to discover channel handle from yt-dlp."""
    lines, errs = run([YTDLP, '--print', '%(channel)s;%(uploader_url)s;%(channel_url)s',
                        '--playlist-items', '1-1',
                        f'https://www.youtube.com/channel/{uc_id}'], timeout=30)
    handle = None
    for line in lines:
        parts = line.split(';')
        for p in parts:
            if '@' in p:
                handle = p.strip()
                break
    return handle

# ========== MAIN ==========
print('=' * 70)
print('CP2: CHANNEL VERIFICATION & FAT-CANDIDATE PLAYLIST DISCOVERY')
print(f'Time: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
print('Method: KEYLESS (RSS + yt-dlp only. No API key.)')
print('=' * 70)

# Phase 1: Verify all channel IDs
print('\n--- PHASE 1: Channel ID verification ---')
verified = []
for ch_id, name, uc_id in ROSTER:
    print(f'\n  {ch_id} ({name}) — UC ID: {uc_id}')
    ok, msg = verify_channel(uc_id)
    print(f'    RSS: {"PASS" if ok else "FAIL"} — {msg}')
    if not ok:
        # Try yt-dlp fallback
        ok2, msg2 = check_channel_via_ytdlp(uc_id)
        print(f'    yt-dlp fallback: {"PASS" if ok2 else "FAIL"} — {msg2}')
        ok = ok2
    verified.append((ch_id, name, uc_id, ok, msg if ok else (msg2 if ok else msg)))

# Phase 2: Discover playlists for fat candidates
print('\n--- PHASE 2: Playlist discovery for fat candidates ---')
fat_data = {}
for ch_id in FAT_CANDIDATES:
    ch_info = next((c for c in ROSTER if c[0] == ch_id), None)
    if not ch_info:
        continue
    _, name, uc_id = ch_info
    print(f'\n  Fat candidate: {name} (UC: {uc_id})')
    print('  Discovering playlists via yt-dlp (channel playlists tab)...')
    playlists = discover_playlists_via_ytdlp(uc_id)
    print(f'  Found {len(playlists)} playlists:')
    for pl in playlists:
        print(f'    [{pl["pl_id"][:30]}...] "{pl["title"]}" — {pl["item_count"]} videos')

    # Check for total video count via yt-dlp channel page
    print('  Attempting to get total video count (keyless)...')
    lines, errs = run([YTDLP, '--print', '%(playlist_count)s',
                        '--playlist-items', '1-1',
                        f'https://www.youtube.com/channel/{uc_id}/videos'], timeout=45)
    video_count_total = None
    for line in lines:
        if line.isdigit():
            video_count_total = int(line)
            print(f'  video_count_total (from uploads playlist count): {video_count_total}')
            break
    if video_count_total is None:
        print('  video_count_total: UNAVAILABLE (yt-dlp could not retrieve uploads count)')

    fat_data[ch_id] = {
        'name': name,
        'uc_id': uc_id,
        'video_count_total': video_count_total,
        'playlists': playlists,
    }

# Phase 3: Apply §4 DECISION RULE
print('\n--- PHASE 3: Fat channel DECISION RULE (§4) ---')
print('Excluding catch-all playlists (itemCount >= 80% of video_count_total)')
print('Requiring ≥3 qualifying playlists, combined ≥40 harvestable videos\n')

results = []
for ch_id, data in fat_data.items():
    qualifies, q_playlists, total_harvestable, reason = apply_fat_rule(
        data['name'], data['uc_id'], data['video_count_total'], data['playlists']
    )
    results.append((ch_id, data['name'], qualifies, len(q_playlists), total_harvestable, reason))
    print(f'  {data["name"]:25s} qualifies={str(qualifies):5s}  q_playlists={len(q_playlists)}  harvestable={total_harvestable}  → {reason}')

# Select winner
qualifying = [(ch, name, qp, th) for ch, name, q, qp, th, r in results if q]
if qualifying:
    qualifying.sort(key=lambda x: x[3], reverse=True)
    winner_ch, winner_name, winner_qp, winner_th = qualifying[0]
    print(f'\n  >>> SELECTED FAT CHANNEL: {winner_name} ({winner_ch})')
    print(f'  >>> Qualifying playlists: {winner_qp}, harvestable total: {winner_th}')

    # Print chosen playlists
    print(f'\n  Chosen playlists:')
    data = fat_data[winner_ch]
    vct = data['video_count_total']
    for pl in data['playlists']:
        ic = pl.get('item_count')
        is_catchall = ic and vct and ic >= 0.8 * vct
        is_qualifying = ic and vct and ic < 0.8 * vct and ic >= 8
        flag = 'CATCH-ALL' if is_catchall else ('QUALIFYING' if is_qualifying else 'too-small/unknown')
        print(f'    [{flag:14s}] {pl["pl_id"]} "{pl["title"]}" ({pl["item_count"]} videos)')
else:
    print('\n  >>> NO CANDIDATE QUALIFIES as fat-with-grouping.')
    print('  >>> STOP — human decision required.')

# Phase 4: Summary table
print('\n\n--- CP2 SUMMARY TABLE ---')
print(f'{"Channel ID":<28s} {"Name":<25s} {"UC Verified":<12s} {"Catalog Size":<15s} {"Playlists Found":<18s}')
print('-' * 100)
for ch_id, name, uc_id, ok, msg in verified:
    vct = 'unknown'
    pl_count = 0
    if ch_id in fat_data:
        vct = str(fat_data[ch_id].get('video_count_total', 'unknown'))
        pl_count = len(fat_data[ch_id]['playlists'])
    print(f'{ch_id:<28s} {name:<25s} {"PASS" if ok else "FAIL":<12s} {vct:<15s} {pl_count:<18d}')

# Check pass criteria
all_verified = all(v[3] for v in verified)
print(f'\nPass criteria:')
print(f'  18/18 IDs resolve: {"PASS" if all_verified else "FAIL"} ({sum(1 for v in verified if v[3])}/18 verified)')
print(f'  Catalog sizes: all null (keyless, API unavailable per work order — expected)')
print(f'  Fat channel selected: {"PASS — " + winner_name if qualifying else "FAIL — no candidate qualifies"}')

print('\n=== CP2 COMPLETE. AWAITING APPROVAL. ===')
