#!/usr/bin/env python3
"""
YouTube dataset harvester - keyless approach using:
1. RSS feed (fast channel listing, ~15 most recent videos)
2. yt-dlp (per-video enrichment: duration, comment_count, tags)
3. yt-dlp on curated playlist URLs (playlist membership)
"""

import subprocess, json, xml.etree.ElementTree as ET, sys, time, re
from datetime import datetime, timezone
from urllib.request import urlopen

YTDLP = '/tmp/yt-env/bin/yt-dlp'

def run_ytdlp(args, timeout=30):
    """Run yt-dlp and return stdout lines, filtering warnings."""
    try:
        r = subprocess.run([YTDLP] + args, capture_output=True, text=True, timeout=timeout)
        lines = [l for l in r.stdout.split('\n') if l and not l.startswith('WARNING')]
        return lines
    except subprocess.TIMEOUTEXPIRED:
        return []
    except Exception as e:
        return [f'ERROR:{e}']

def fetch_rss(channel_id):
    """Fetch RSS feed for a channel. Returns list of video dicts."""
    url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    try:
        with urlopen(url, timeout=15) as r:
            xml_data = r.read().decode('utf-8')
    except Exception as e:
        return [], f'RSS fetch failed: {e}'

    videos = []
    try:
        root = ET.fromstring(xml_data)
        # Namespace handling
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'yt': 'http://www.youtube.com/xml/schemas/2015',
            'media': 'http://search.yahoo.com/mrss/',
        }
        for entry in root.findall('atom:entry', ns):
            v = {}
            vid_elem = entry.find('yt:videoId', ns)
            v['id'] = vid_elem.text if vid_elem is not None else None

            title_elem = entry.find('atom:title', ns)
            v['title'] = title_elem.text if title_elem is not None else None

            published_elem = entry.find('atom:published', ns)
            v['published_at'] = published_elem.text if published_elem is not None else None

            # View count from media:statistics
            stats = entry.find('.//media:statistics', ns)
            if stats is not None:
                v['view_count'] = int(stats.get('views', 0))
            else:
                v['view_count'] = None

            # Like count from media:starRating
            rating = entry.find('.//media:starRating', ns)
            if rating is not None:
                v['like_count'] = int(float(rating.get('count', 0)))
            else:
                v['like_count'] = None

            # Thumbnail URL
            thumb = entry.find('.//media:thumbnail', ns)
            if thumb is not None:
                v['thumbnail_url'] = thumb.get('url', '')
            else:
                v['thumbnail_url'] = None

            # Description
            desc = entry.find('.//media:description', ns)
            v['description'] = desc.text[:200] + '...' if desc is not None and desc.text and len(desc.text) > 200 else (desc.text if desc is not None else None)

            if v['id']:
                videos.append(v)
    except Exception as e:
        return videos, f'RSS parse error: {e}'

    return videos, None

def enrich_video_ytdlp(video_id):
    """Get full metadata for a single video using yt-dlp."""
    lines = run_ytdlp([
        '--print',
        'id=%(id)s\ntitle=%(title)s\nchannel=%(channel)s\nchannel_id=%(channel_id)s\nupload_date=%(upload_date)s\nview_count=%(view_count)s\nlike_count=%(like_count)s\ncomment_count=%(comment_count)s\nduration=%(duration)s\ntags=%(tags)s',
        f'https://www.youtube.com/watch?v={video_id}'
    ], timeout=20)

    data = {}
    for line in lines:
        if '=' in line:
            k, v = line.split('=', 1)
            data[k] = v

    return data

def parse_ytdlp_date(yyyymmdd):
    """Convert YYYYMMDD to ISO 8601"""
    if not yyyymmdd or yyyymmdd == 'NA':
        return None
    try:
        d = datetime.strptime(yyyymmdd, '%Y%m%d')
        return d.strftime('%Y-%m-%dT00:00:00Z')
    except:
        return None

def get_playlist_vids(playlist_url, limit=50):
    """Get videos from a curated playlist with playlist membership."""
    lines = run_ytdlp([
        '--print', '%(id)s;%(playlist_title)s;%(playlist_index)s;%(playlist_count)s;%(title)s',
        '--playlist-items', f'1-{limit}',
        playlist_url
    ], timeout=120)

    videos = []
    for line in lines:
        parts = line.split(';')
        if len(parts) >= 3:
            v = {
                'id': parts[0],
                'playlist_title': parts[1].replace(' - Two Minute Papers', ''),
                'playlist_index': int(parts[2]) if parts[2].isdigit() else None,
                'playlist_count': int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None,
            }
            videos.append(v)
    return videos


def probe_channel(channel_url, channel_id, name, playlist_url=None):
    """Full probe of a channel."""
    print(f'\n=== PROBING: {name} ===')
    print(f'Channel ID: {channel_id}')
    print(f'Channel URL: {channel_url}')

    # Step 1: RSS feed
    print('\n[1/3] Fetching RSS feed...')
    rss_videos, error = fetch_rss(channel_id)
    if error:
        print(f'  RSS error: {error}')
    else:
        print(f'  Got {len(rss_videos)} videos from RSS')

    # Step 2: Enrich each video
    print('\n[2/3] Enriching videos with yt-dlp...')
    enriched = []
    for i, v in enumerate(rss_videos):
        time.sleep(1.5)  # Be gentle
        extra = enrich_video_ytdlp(v['id'])
        v.update({
            'duration_seconds': int(extra.get('duration', 0)) if extra.get('duration', 'NA') != 'NA' and extra.get('duration', '0').isdigit() else None,
            'comment_count': int(extra.get('comment_count', 0)) if extra.get('comment_count', 'NA') != 'NA' and extra.get('comment_count', '0').isdigit() else None,
            'tags': eval(extra.get('tags', '[]')) if extra.get('tags', '[]') != 'NA' else [],
            'channel_name': extra.get('channel', name),
            'youtube_channel_id': extra.get('channel_id', channel_id),
            'upload_date_iso': parse_ytdlp_date(extra.get('upload_date', '')),
        })
        # Parse published_at from RSS if we have it
        if v.get('published_at'):
            try:
                dt = datetime.fromtimestemp(0, tz=timezone.utc)  # placeholder
                # Parse ISO 8601
                v['published_at_iso'] = v['published_at']
            except:
                v['published_at_iso'] = v['published_at']
        elif v.get('upload_date_iso'):
            v['published_at_iso'] = v['upload_date_iso']
        else:
            v['published_at_iso'] = None

        enriched.append(v)
        print(f'  [{i+1}/{len(rss_videos)}] {v["id"][:12]}... {v["title"][:50] if v.get("title") else "?"}')

    # Step 3: Playlist data
    print('\n[3/3] Fetching curated playlist...')
    playlist_vids = []
    if playlist_url:
        playlist_vids = get_playlist_vids(playlist_url, limit=30)
        print(f'  Got {len(playlist_vids)} playlist entries')
        # Mark playlist membership on enriched videos
        playlist_lookup = {v['id']: v for v in playlist_vids}
        for v in enriched:
            if v['id'] in playlist_lookup:
                v['playlist'] = playlist_lookup[v['id']]['playlist_title']
            else:
                v['playlist'] = None
    else:
        print('  No playlist URL provided')

    return enriched, playlist_vids


# ====== PHASE B: Probe Two Minute Papers ======
print('=' * 60)
print('PHASE B: FEASIBILITY PROBE')
print('=' * 60)

ch_id = 'UCbfYPyITQ-7l4upoX8nvctg'
pl_url = 'https://www.youtube.com/playlist?list=PLujxSBD-JXglGL3ERdDOhthD3jTlfudC2'

videos, playlist_vids = probe_channel(
    channel_url='https://www.youtube.com/@TwoMinutePapers',
    channel_id=ch_id,
    name='Two Minute Papers',
    playlist_url=pl_url
)

# Build Phase B output schema
output = {
    'meta': {
        'harvested_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'method_used': 'YouTube RSS feed + yt-dlp (keyless, no API key)',
        'notes': 'Phase B feasibility probe. One channel, ~15 RSS videos enriched with yt-dlp. Curated playlist data from "AI and Deep Learning" playlist.'
    },
    'topics': [{
        'id': 'topic_ai',
        'label': 'Artificial Intelligence',
        'channel_ids': ['chan_two_minute_papers']
    }],
    'channels': [{
        'id': 'chan_two_minute_papers',
        'youtube_channel_id': ch_id,
        'name': 'Two Minute Papers',
        'topic_id': 'topic_ai',
        'video_count_total': None,
        'harvested_video_count': len(videos),
        'video_ids': [v['id'] for v in videos]
    }],
    'videos': []
}

for v in videos:
    entry = {
        'id': v['id'],
        'title': v.get('title'),
        'channel_id': 'chan_two_minute_papers',
        'published_at': v.get('published_at_iso'),
        'duration_seconds': v.get('duration_seconds'),
        'view_count': v.get('view_count'),
        'like_count': v.get('like_count'),
        'comment_count': v.get('comment_count'),
        'tags': v.get('tags', []),
        'playlist': v.get('playlist'),
        'thumbnail_url': f'https://img.youtube.com/vi/{v["id"]}/hqdefault.jpg'
    }
    output['videos'].append(entry)

print('\n\n=== PHASE B OUTPUT ===')
print(json.dumps(output, indent=2, ensure_ascii=False))
