#!/usr/bin/env python3
"""
CP2-REDO: Keyless channel verification + fat-candidate selection.
Queries individual playlist URLs for real item counts (not tab-page flat-playlist artifacts).
Queries channel /videos tab for real long-form upload counts.
"""
import subprocess, time, sys
from datetime import datetime, timezone

YTDLP = '/tmp/yt-env/bin/yt-dlp'

# ===== ALL 18 CHANNELS =====
ROSTER = [
    # --- AI (8) ---
    ('chan_two_minute_papers', 'Two Minute Papers', 'UCbfYPyITQ-7l4upoX8nvctg'),
    ('chan_wes_roth', 'Wes Roth', 'UCqcbQf6yw5KzRoDDcZ_wBSw'),
    ('chan_ai_explained', 'AI Explained', 'UCNJ1Ymd5yFuUPtn21xtRbbw'),
    ('chan_matt_wolfe', 'Matt Wolfe', 'UChpleBmo18P08aKCIgti38g'),
    ('chan_yannic_kilcher', 'Yannic Kilcher', 'UCZHmQk67mSJgfCCTn7xBfew'),
    ('chan_sentdex', 'sentdex', None),  # resolve via handle
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

FAT_CANDIDATES = ['chan_two_minute_papers', 'chan_3blue1brown', 'chan_veritasium']

def run(cmd_args, timeout=60):
    try:
        r = subprocess.run(cmd_args, capture_output=True, text=True, timeout=timeout)
        lines = [l for l in r.stdout.split('\n') if l and not l.startswith('WARNING:')]
        return lines
    except subprocess.TimeoutExpired:
        return ['__TIMEOUT__']
    except Exception as e:
        return [f'__ERROR__:{e}']

def resolve_handle(handle):
    """Resolve a YouTube @handle to a UC channel ID."""
    url = f'https://www.youtube.com/@{handle}/videos'
    lines = run([YTDLP, '--print', '%(channel_id)s', '--playlist-items', '1-1', url], timeout=30)
    for line in lines:
        if line.startswith('UC') and len(line) == 24:
            return line
    return None

def get_channel_video_count(uc_id):
    """Get long-form upload count via the UU uploads playlist (UC → UU).
    This is the channel's auto-generated uploads playlist, reliably sized."""
    uu_id = 'UU' + uc_id[2:]  # UCbfYPyITQ-7l4upoX8nvctg → UUbfYPyITQ-7l4upoX8nvctg
    url = f'https://www.youtube.com/playlist?list={uu_id}'
    lines = run([YTDLP, '--playlist-end', '1', '--print', '%(playlist_count)s', url], timeout=30)
    for line in lines:
        line = line.strip()
        if line.isdigit():
            return int(line)
    return None

def discover_playlists(uc_id):
    """Discover playlist IDs and titles from channel's playlists tab.
    Returns list of (pl_id, title) tuples."""
    url = f'https://www.youtube.com/channel/{uc_id}/playlists'
    lines = run([YTDLP, '--flat-playlist', '--print', '%(title)s|%(id)s', url], timeout=120)
    playlists = []
    skip_titles = {'created playlists', 'uploads', 'liked videos'}
    for line in lines:
        if '|' not in line:
            continue
        parts = line.split('|', 1)
        title = parts[0].strip()
        pl_id = parts[1].strip()
        if title.lower() in skip_titles:
            continue
        if pl_id and not pl_id.startswith('UC'):
            playlists.append((pl_id, title))
    return playlists

def get_playlist_size(pl_id):
    """Get real playlist item count by querying the individual playlist URL."""
    url = f'https://www.youtube.com/playlist?list={pl_id}'
    lines = run([YTDLP, '--flat-playlist', '-I', '1:1', '-O', '%(playlist_count)s', url], timeout=60)
    for line in lines:
        line = line.strip()
        if line.isdigit():
            return int(line)
    return None

def is_translation_playlist(title):
    """Detect translation/language-duplicate playlists by title heuristics."""
    title_lower = title.lower()
    translations = [
        'russian', 'русск', 'hindi', 'हिन्दी', 'french', 'français', 'francais',
        'spanish', 'español', 'espanol', 'german', 'deutsch', 'japanese', '日本語',
        'korean', '한국어', 'chinese', '中文', 'portuguese', 'português',
        'traductions', 'traducciones', 'übersetzungen', 'traduções',
        'переводы', 'translations',
        'subtitles', 'subtitulos',
    ]
    for t in translations:
        if t in title_lower:
            return True
    return False

# ========== MAIN ==========
print('=' * 70)
print('CP2-REDO: KEYLESS CHANNEL VERIFICATION & FAT-CHANNEL SELECTION')
print(f'Time: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
print('Method: KEYLESS (yt-dlp on individual playlist URLs for real counts)')
print('=' * 70)

# === Step 1: Resolve sentdex handle ===
print('\n--- Step 1: Resolve sentdex handle ---')
if ROSTER[5][0] == 'chan_sentdex' and ROSTER[5][2] is None:
    # Replace the entry with resolved ID
    uc_id = resolve_handle('sentdex')
    if uc_id:
        ROSTER[5] = ('chan_sentdex', 'sentdex', uc_id)
        print(f'  sentdex resolved to UC ID: {uc_id}')
    else:
        # Try alternate: yt-dlp on the old UC ID
        old_uc = 'UCQ_hh4SdlGjY8rWxB7_JIfg'
        lines = run([YTDLP, '--print', '%(channel_id)s', '--playlist-items', '1-1',
                      f'https://www.youtube.com/channel/{old_uc}/videos'], timeout=30)
        for line in lines:
            if line.startswith('UC') and len(line) == 24:
                ROSTER[5] = ('chan_sentdex', 'sentdex', line)
                print(f'  sentdex resolved (old ID fallback): {line}')
                break
        else:
            # Try @sentdex again with /videos
            lines2 = run([YTDLP, '--print', '%(channel_id)s|%(title)s', '--playlist-items', '1-1',
                          'https://www.youtube.com/@sentdex'], timeout=30)
            for line in lines2:
                parts = line.split('|')
                if len(parts) >= 1 and parts[0].startswith('UC') and len(parts[0]) == 24:
                    ROSTER[5] = ('chan_sentdex', 'sentdex', parts[0])
                    print(f'  sentdex resolved via @handle: {parts[0]}')
                    break

    if ROSTER[5][2] is None:
        print('  FAILED: sentdex unresolvable. Need replacement.')
else:
    print(f'  sentdex already has UC ID: {ROSTER[5][2]}')

# === Step 2: Get video_count_total for ALL channels ===
print('\n--- Step 2: Get video_count_total (long-form uploads) for all channels ---')
channel_data = {}
for ch_id, name, uc_id in ROSTER:
    if uc_id is None:
        print(f'  {name:25s}: SKIP (no UC ID)')
        continue
    vct = get_channel_video_count(uc_id)
    verified = vct is not None
    channel_data[ch_id] = {
        'name': name,
        'uc_id': uc_id,
        'video_count_total': vct,
        'verified': verified,
    }
    status = f'{vct:,}' if vct else 'NULL'
    print(f'  {name:25s}: video_count_total = {status:>8s}  verified={"PASS" if verified else "FAIL"}')
    time.sleep(0.5)

# === Step 3: Discover + size all playlists for fat candidates ===
print('\n--- Step 3: Playlist discovery + real sizing for fat candidates ---')
fat_playlist_data = {}

for ch_id, name, uc_id in [(c[0], c[1], c[2]) for c in ROSTER if c[0] in FAT_CANDIDATES]:
    if uc_id is None:
        continue
    print(f'\n  >>> {name} (UC: {uc_id})')
    print('  Discovering playlists...')
    playlists = discover_playlists(uc_id)
    print(f'  Found {len(playlists)} playlists. Getting real sizes...')

    sized = []
    for pl_id, title in playlists:
        time.sleep(1)
        size = get_playlist_size(pl_id)
        sized.append({'pl_id': pl_id, 'title': title, 'item_count': size})
        print(f'    [{str(size) if size else "NULL":>6s}] {pl_id[:40]}... "{title[:60]}"')

    fat_playlist_data[ch_id] = sized

# === Step 4: Apply §4 DECISION RULE ===
print('\n--- Step 4: Apply §4 FAT-CHANNEL DECISION RULE ---')

TRANSLATION_KEYWORDS = {
    'russian', 'русск', 'hindi', 'french', 'français', 'francais',
    'spanish', 'español', 'espanol', 'german', 'deutsch', 'japanese',
    'korean', 'chinese', 'portuguese', 'português',
    'traductions', 'traducciones', 'übersetzungen', 'traduções',
    'переводы', 'translations', 'subtitles', 'subtitulos',
}

def is_translation(title):
    t = title.lower()
    return any(kw in t for kw in TRANSLATION_KEYWORDS)

results = []
for ch_id in FAT_CANDIDATES:
    cd = channel_data.get(ch_id, {})
    vct = cd.get('video_count_total')
    name = cd.get('name', ch_id)
    playlists = fat_playlist_data.get(ch_id, [])

    if vct is None:
        results.append((ch_id, name, False, [], 0, f'video_count_total is null'))
        print(f'\n  {name}: video_count_total=null → CANNOT QUALIFY')
        continue

    qualifying = []
    excluded_reasons = []
    for pl in playlists:
        ic = pl['item_count']
        title = pl['title']

        if ic is None:
            excluded_reasons.append((pl, 'item_count null'))
            continue
        if ic >= 0.8 * vct:
            excluded_reasons.append((pl, f'catch-all ({ic} >= 80% of {vct})'))
            continue
        if is_translation(title):
            excluded_reasons.append((pl, 'translation playlist'))
            continue
        if ic < 8:
            excluded_reasons.append((pl, f'too small ({ic} < 8)'))
            continue

        qualifying.append(pl)

    total = sum(p['item_count'] for p in qualifying)

    print(f'\n  {name} (video_count_total={vct}):')
    print(f'    Qualifying playlists: {len(qualifying)}, combined harvestable: {total}')

    if len(qualifying) < 3:
        reason = f'Only {len(qualifying)} qualifying (need ≥3)'
        results.append((ch_id, name, False, qualifying, total, reason))
        print(f'    {reason}')
    elif total < 40:
        reason = f'Combined {total} < 40 threshold'
        results.append((ch_id, name, False, qualifying, total, reason))
        print(f'    {reason}')
    else:
        reason = f'Meets all criteria: {len(qualifying)} playlists, {total} total'
        results.append((ch_id, name, True, qualifying, total, reason))
        print(f'    ✓ {reason}')

    # Show excluded
    print(f'    Excluded:')
    for pl, reason in excluded_reasons:
        ic_str = str(pl['item_count'] or '?')
        print(f'      [{reason:<35s}] {pl["pl_id"][:40]}... "{pl["title"][:50]}" ({ic_str})')

    # Show qualifying
    print(f'    Qualifying:')
    for pl in qualifying:
        print(f'      [{pl["item_count"]:>5d}] {pl["pl_id"][:40]}... "{pl["title"][:50]}"')

# === Step 5: Select winner ===
print('\n' + '=' * 70)
print('--- §4 SELECTION ---')
qualifying = [(ch, name, qp, th, r) for ch, name, q, qp, th, r in results if q]

if qualifying:
    # Select the one with largest combined harvest
    qualifying.sort(key=lambda x: x[3], reverse=True)
    winner_ch, winner_name, winner_qp, winner_th, winner_reason = qualifying[0]
    print(f'\n  >>> SELECTED FAT CHANNEL: {winner_name} ({winner_ch})')
    print(f'  >>> {len(winner_qp)} qualifying playlists, {winner_th} total harvestable videos')
    print(f'  >>> {winner_reason}')

    # Print chosen playlists
    print(f'\n  Chosen playlists for harvest:')
    for pl in winner_qp:
        print(f'    PL={pl["pl_id"]}  title="{pl["title"]}"  count={pl["item_count"]}')
else:
    print('\n  >>> NO CANDIDATE QUALIFIES. Genuine "none qualify" per §4.')
    print('  >>> Requires human decision before proceeding.')

# === Final CP2 summary ===
print('\n\n' + '=' * 70)
print('CP2 SUMMARY TABLE')
print('=' * 70)
print(f'{"Channel":<30s} {"UC Verified":<12s} {"Video Count (long-form)":<28s} {"Playlists":<12s}')
print('-' * 90)
for ch_id, name, uc_id in ROSTER:
    cd = channel_data.get(ch_id, {})
    vct = cd.get('video_count_total')
    vct_str = f'{vct:,}' if vct is not None else 'NULL'
    verified = 'PASS' if cd.get('verified') else 'FAIL'
    pl_count = len(fat_playlist_data.get(ch_id, []))
    print(f'{name:<30s} {verified:<12s} {vct_str:<28s} {pl_count:<12d}')

# Topic counts
ai_count = sum(1 for c in ROSTER if c[0] in [r[0] for r in ROSTER if r[1] in [
    'Two Minute Papers','Wes Roth','AI Explained','Matt Wolfe','Yannic Kilcher',
    'sentdex','AI and Games','Robert Miles AI Safety'
]])
print(f'\nTopic AI: {ai_count} channels (floor: 5) → {"PASS" if ai_count >= 5 else "FAIL"}')

verified_count = sum(1 for cd in channel_data.values() if cd['verified'])
null_vct = sum(1 for cd in channel_data.values() if cd['video_count_total'] is None)
print(f'IDs verified: {verified_count}/{len([c for c in ROSTER if c[2] is not None])} (excl. unresolved)')
print(f'video_count_total null: {null_vct} channels')
print(f'Sentdex UC ID: {next((c[2] for c in ROSTER if c[0]=="chan_sentdex"), "UNRESOLVED")}')

print('\n=== CP2-REDO COMPLETE. AWAITING APPROVAL. ===')
