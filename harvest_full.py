#!/usr/bin/env python3
"""
Phase C: Full YouTube Dataset Harvest
Keyless methods: YouTube RSS feed + yt-dlp per-video enrichment + curated playlist extraction
"""

import subprocess, json, xml.etree.ElementTree as ET, sys, time, re, os
from datetime import datetime, timezone
from urllib.request import urlopen

YTDLP = '/tmp/yt-env/bin/yt-dlp'
SCRIPT_DIR = '/project/yu'
OUTPUT_PATH = os.path.join(SCRIPT_DIR, 'youtube_dataset.json')

# ============ CHANNEL DEFINITIONS ============

CHANNELS = {
    # === TOPIC: AI / Machine Learning (8 channels, busy) ===
    'chan_two_minute_papers': {
        'name': 'Two Minute Papers',
        'youtube_channel_id': 'UCbfYPyITQ-7l4upoX8nvctg',
        'topic_id': 'topic_ai',
        'description': 'AI research summaries and breakthrough videos',
        'playlist_url': 'https://www.youtube.com/playlist?list=PLujxSBD-JXglGL3ERdDOhthD3jTlfudC2',
        'playlist_videos_to_take': 80,  # FAT CHANNEL
    },
    'chan_wes_roth': {
        'name': 'Wes Roth',
        'youtube_channel_id': 'UCqcbQf6yw5KzRoDDcZ_wBSw',
        'topic_id': 'topic_ai',
        'description': 'AI news and emerging tech breakthroughs',
    },
    'chan_ai_explained': {
        'name': 'AI Explained',
        'youtube_channel_id': 'UCNJ1Ymd5yFuUPtn21xtRbbw',
        'topic_id': 'topic_ai',
        'description': 'Deep analysis of AI news and research',
    },
    'chan_matt_wofe': {
        'name': 'Matt Wolfe',
        'youtube_channel_id': 'UChpleBmo18P08aKCIgti38g',
        'topic_id': 'topic_ai',
        'description': 'AI, no-code, tech tutorials and news',
    },
    'chan_yannic_kilcher': {
        'name': 'Yannic Kilcher',
        'youtube_channel_id': 'UCZHmQk67mSJgfCCTn7xBfew',
        'topic_id': 'topic_ai',
        'description': 'Machine learning research papers and programming',
    },
    # === TOPIC: Space / Astronomy (5 channels) ===
    'chan_fraser_cain': {
        'name': 'Fraser Cain',
        'youtube_channel_id': 'UCogrSQkBJn1KF0N9I4oM7eQ',
        'topic_id': 'topic_space',
        'description': 'Space and astronomy news from Universe Today',
    },
    'chan_scishow_space': {
        'name': 'SciShow Space',
        'youtube_channel_id': 'UCrMePiHCWG4Vwqv3t7W9EFg',
        'topic_id': 'topic_space',
        'description': 'Weekly space exploration and news',
    },
    'chan_startalk': {
        'name': 'StarTalk',
        'youtube_channel_id': 'UCqoAEDirJPjEUFcF2FklnBA',
        'topic_id': 'topic_space',
        'description': 'Astrophysics and pop culture with Neil deGrasse Tyson',
    },
    'chan_nasa_goddard': {
        'name': 'NASA Goddard',
        'youtube_channel_id': 'UCAY-SMFNfynqz1bdoaV8BeQ',
        'topic_id': 'topic_space',
        'description': 'NASA Goddard Space Flight Center',
    },
    # === TOPIC: Math / Science (3 channels) ===
    'chan_3blue1brown': {
        'name': '3Blue1Brown',
        'youtube_channel_id': 'UCYO_jab_esuFRV4b17AJtAw',
        'topic_id': 'topic_math',
        'description': 'Animated math visualizations',
    },
}

TOPICS = [
    {'id': 'topic_ai', 'label': 'Artificial Intelligence', 'channel_ids': [
        'chan_two_minute_papers', 'chan_wes_roth', 'chan_ai_explained',
        'chan_matt_wofe', 'chan_yannic_kilcher',
    ]},
    {'id': 'topic_space', 'label': 'Space & Astronomy', 'channel_ids': [
        'chan_fraser_cain', 'chan_scishow_space', 'chan_startalk', 'chan_nasa_goddard',
    ]},
    {'id': 'topic_math', 'label': 'Math & Science', 'channel_ids': [
        'chan_3blue1brown',
    ]},
]

# ============ HELPERS ============

def run_ytdlp(args, timeout=30):
    try:
        r = subprocess.run([YTDLP] + args, capture_output=True, text=True, timeout=timeout)
        lines = [l for l in r.stdout.split('\n') if l and not l.startswith('WARNING')]
        return lines
    except subprocess.TIMEOUTEXPIRED:
        print(f'  [TIMEOUT] yt-dlp {args[0][:40]}...')
        return []
    except Exception as e:
        print(f'  [ERROR] {e}')
        return []

def fetch_rss(channel_id):
    url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    try:
        with urlopen(url, timeout=15) as r:
            xml_data = r.read().decode('utf-8')
    except Exception as e:
        print(f'  [RSS ERROR] {e}')
        return []

    videos = []
    try:
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom',
              'yt': 'http://www.youtube.com/xml/schemas/2015',
              'media': 'http://search.yahoo.com/mrss/'}
        for entry in root.findall('atom:entry', ns):
            v = {}
            vid_elem = entry.find('yt:videoId', ns)
            v['id'] = vid_elem.text if vid_elem is not None else None
            title_elem = entry.find('atom:title', ns)
            v['title'] = title_elem.text if title_elem is not None else None
            published_elem = entry.find('atom:published', ns)
            v['published_at'] = published_elem.text if published_elem is not None else None
            stats = entry.find('.//media:statistics', ns)
            v['view_count'] = int(stats.get('views', 0)) if stats is not None else None
            rating = entry.find('.//media:starRating', ns)
            v['like_count'] = int(float(rating.get('count', 0))) if rating is not None else None
            desc = entry.find('.//media:description', ns)
            v['description'] = (desc.text[:250] + '...') if desc is not None and desc.text and len(desc.text) > 250 else (desc.text if desc is not None else None)
            if v['id']:
                videos.append(v)
    except Exception as e:
        print(f'  [RSS PARSE ERROR] {e}')
    return videos

def enrich_video(video_id):
    lines = run_ytdlp([
        '--print',
        'id=%(id)s\nduration=%(duration)s\ncomment_count=%(comment_count)s\ntags=%(tags)s\nupload_date=%(upload_date)s\nview_count=%(view_count)s\nlike_count=%(like_count)s\nchannel=%(channel)s\nchannel_id=%(channel_id)s',
        f'https://www.youtube.com/watch?v={video_id}'
    ], timeout=20)
    data = {}
    for line in lines:
        if '=' in line:
            k, v2 = line.split('=', 1)
            data[k] = v2
    return data

def get_playlist_videos(playlist_url, limit=50):
    lines = run_ytdlp([
        '--print', '%(id)s;%(playlist_title)s;%(playlist_index)s;%(playlist_count)s;%(title)s',
        '--playlist-items', f'1-{limit}',
        playlist_url
    ], timeout=180)
    videos = []
    for line in lines:
        parts = line.split(';')
        if len(parts) >= 3 and parts[0]:
            playlist_name = parts[1] if len(parts) > 1 else ''
            # Clean playlist name - remove channel suffix
            for ch_name in ['Two Minute Papers', ' - Two Minute Papers']:
                if ch_name in playlist_name:
                    playlist_name = playlist_name.replace(ch_name, '').strip(' -')
            v = {
                'id': parts[0],
                'playlist': playlist_name if playlist_name else None,
                'playlist_index': int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None,
                'playlist_count': int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None,
                'title': parts[4] if len(parts) > 4 else None,
            }
            videos.append(v)
    return videos

# ============ MAIN HARVEST ============

def harvest():
    print('=' * 60)
    print('PHASE C: FULL YOUTUBE DATASET HARVEST')
    print('=' * 60)

    all_videos = {}  # id -> video dict
    channel_data = {}  # chan_id -> {video_ids: [], harvest_count: N}

    # Initialize channel tracking
    for ch_id, ch_info in CHANNELS.items():
        channel_data[ch_id] = {
            'video_ids': [],
            'harvested_count': 0,
            'errors': [],
        }

    # === STEP 1: Fat channel - curated playlist ===
    print('\n--- STEP 1: Curated playlist harvest (Two Minute Papers) ---')
    fat_ch = 'chan_two_minute_papers'
    ch_info = CHANNELS[fat_ch]
    pl_url = ch_info['playlist_url']
    pl_limit = ch_info['playlist_videos_to_take']

    print(f'  Fetching {pl_limit} videos from "AI and Deep Learning" playlist...')
    playlist_vids = get_playlist_videos(pl_url, limit=pl_limit)
    print(f'  Got {len(playlist_vids)} playlist entries')

    # Enrich each playlist video
    for i, pl_vid in enumerate(playlist_vids):
        vid_id = pl_vid['id']
        if vid_id in all_videos:
            continue
        time.sleep(1.5)
        extra = enrich_video(vid_id)
        if not extra.get('id'):
            print(f'  [{i+1}/{len(playlist_vids)}] SKIP {vid_id[:12]} (no enrichment)')
            continue

        v = {
            'id': vid_id,
            'title': pl_vid.get('title') or extra.get('title', ''),
            'channel_id': fat_ch,
            'published_at': None,
            'duration_seconds': int(extra.get('duration', 0)) if extra.get('duration', 'NA').isdigit() else None,
            'view_count': int(extra.get('view_count', 0)) if extra.get('view_count', 'NA').isdigit() else None,
            'like_count': int(extra.get('like_count', 0)) if extra.get('like_count', 'NA').isdigit() else None,
            'comment_count': int(extra.get('comment_count', 0)) if extra.get('comment_count', 'NA').isdigit() else None,
            'tags': eval(extra.get('tags', '[]')) if extra.get('tags', '[]') != 'NA' else [],
            'playlist': pl_vid.get('playlist'),
            'thumbnail_url': f'https://img.youtube.com/vi/{vid_id}/hqdefault.jpg',
        }
        # Parse date
        upload_date = extra.get('upload_date', '')
        if upload_date and upload_date != 'NA' and len(upload_date) == 8:
            try:
                d = datetime.strptime(upload_date, '%Y%m%d')
                v['published_at'] = d.strftime('%Y-%m-%dT00:00:00Z')
            except:
                pass

        all_videos[vid_id] = v
        channel_data[fat_ch]['video_ids'].append(vid_id)
        channel_data[fat_ch]['harvested_count'] += 1
        print(f'  [{i+1}/{len(playlist_vids)}] {vid_id[:12]} -- {v["title"][:50] if v.get("title") else "?"}')

    print(f'  Total playlist videos harvested: {channel_data[fat_ch]["harvested_count"]}')

    # === STEP 2: RSS feed for all other channels ===
    print('\n--- STEP 2: RSS feed harvest (all channels) ---')

    for ch_id, ch_info in CHANNELS.items():
        print(f'\n  Processing: {ch_info["name"]}')
        yt_ch_id = ch_info['youtube_channel_id']

        rss_vids = fetch_rss(yt_ch_id)
        print(f'  RSS returned {len(rss_vids)} videos')

        for i, rss_vid in enumerate(rss_vids):
            vid_id = rss_vid['id']
            if vid_id in all_videos:
                continue  # Already got it (e.g, fat channel overlap)

            time.sleep(1.5)
            extra = enrich_video(vid_id)
            if not extra.get('id'):
                continue

            # Use RSS published_at if available
            published_at = rss_vid.get('published_at')
            if not published_at:
                upload_date = extra.get('upload_date', '')
                if upload_date and upload_date != 'NA' and len(upload_date) == 8:
                    try:
                        d = datetime.strptime(upload_date, '%Y%m%d')
                        published_at = d.strftime('%Y-%m-%dT00:00:00Z')
                    except:
                        published_at = None

            v = {
                'id': vid_id,
                'title': rss_vid.get('title') or extra.get('title', ''),
                'channel_id': ch_id,
                'published_at': published_at,
                'duration_seconds': int(extra.get('duration', 0)) if extra.get('duration', 'NA').isdigit() else None,
                'view_count': rss_vid.get('view_count') or (int(extra.get('view_count', 0)) if extra.get('view_count', 'NA').isdigit() else None),
                'like_count': rss_vid.get('like_count') or (int(extra.get('like_count', 0)) if extra.get('like_count', 'NA').isdigit() else None),
                'comment_count': int(extra.get('comment_count', 0)) if extra.get('comment_count', 'NA').isdigit() else None,
                'tags': eval(extra.get('tags', '[]')) if extra.get('tags', '[]') != 'NA' else [],
                'playlist': None,
                'thumbnail_url': f'https://img.youtube.com/vi/{vid_id}/hqdefault.jpg',
            }
            all_videos[vid_id] = v
            channel_data[ch_id]['video_ids'].append(vid_id)
            channel_data[ch_id]['harvested_count'] += 1
            print(f'  [{i+1}/{len(rss_vids)}] {vid_id[:12]} -- {v["title"][:50] if v.get("title") else "?"}')

        print(f'  Total for {ch_info["name"]}: {channel_data[ch_id]["harvested_count"]}')

    # === STEP 3: Build output ===
    print('\n--- Building output JSON ---')

    output_channels = []
    for ch_id, ch_info in CHANNELS.items():
        cd = channel_data[ch_id]
        output_channels.append({
            'id': ch_id,
            'youtube_channel_id': ch_info['youtube_channel_id'],
            'name': ch_info['name'],
            'topic_id': ch_info['topic_id'],
            'video_count_total': None,
            'harvested_video_count': cd['harvested_count'],
            'video_ids': cd['video_ids'],
        })

    output_videos = []
    for v in all_videos.values():
        output_videos.append(v)

    # Sort videos by channel_id then title
    output_videos.sort(key=lambda v: (v['channel_id'], v.get('title', '')))

    total_videos = len(output_videos)
    print(f'  Total videos: {total_videos}')
    print(f'  Total channels: {len(output_channels)}')

    output = {
        'meta': {
            'harvested_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'method_used': 'YouTube RSS feed + yt-dlp (keyless) + curated playlist extraction',
            'notes': f'Full Phase C harvest. {total_videos} videos across {len(output_channels)} channels. Fat channel: Two Minute Papers (playlist: 692 videos, harvested {channel_data[fat_ch]["harvested_count"]}). Playlist data available for playlist-sourced videos.',
            'total_videos': total_videos,
        },
        'topics': TOPICS,
        'channels': output_channels,
        'videos': output_videos,
    }

    # Write output
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f'\n=== OUTPUT WRITTEN TO {OUTPUT_PATH} ===')
    print(f'  Total videos: {total_videos}')
    print(f'  Total channels: {len(output_channels)}')

    # Per-channel summary
    print('\n--- Per-channel harvest count ---')
    for ch_id, cd in sorted(channel_data.items()):
        print(f'  {CHANNELS[ch_id]["name"]:30s}: {cd["harvested_count"]:4d} videos')

    return output

if __name__ == '__main__':
    output = harvest()
