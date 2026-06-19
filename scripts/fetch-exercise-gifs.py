#!/usr/bin/env python3
"""
Fetch exercise demonstration images from free-exercise-db (MIT License)
and create animated GIFs for the Royal Fitness Club workout section.

Source : https://github.com/yuhonas/free-exercise-db (MIT)
Images : https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/{id}/images/{n}.jpg
"""

import json, os, re, sys, io, time
import urllib.request, urllib.error
from PIL import Image

DB_URL  = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
IMG_BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises"
OUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'icons', 'exercises')

GIF_W, GIF_H    = 400, 267   # 3:2 ratio, matches existing JPG dimensions
GIF_DURATION_MS = 1400        # ms per frame

# Manual overrides: our key -> exact DB exercise name (or close enough for search)
MANUAL_MAP = {
    'bicep_curls':           'Bicep Curl',
    'db_press':              'Dumbbell Bench Press',
    'incline_db_press':      'Incline Dumbbell Press',
    'lateral_raises':        'Side Lateral Raise',
    'overhead_press':        'Standing Military Press',
    'skull_crushers':        'EZ-Bar Skullcrusher',
    'tricep_pushdown':       'Triceps Pushdown',
    'walking_lunges':        'Walking Lunge',
    'bulgarian_split_squat': 'Barbell Bulgarian Split Squat',
    'front_raises':          'Dumbbell Front Raise',
    'pull_ups':              'Pull-up',
    'push_ups':              'Push-up',
    'barbell_row':           'Bent Over Barbell Row',
    'bench_press':           'Barbell Bench Press',
    'seated_cable_row':      'Seated Cable Row',
    'deadlift':              'Barbell Deadlift',
    'squat':                 'Barbell Full Squat',
    'romanian_deadlift':     'Romanian Deadlift',
    'lat_pulldown':          'Wide-Grip Lat Pulldown',
    'dips':                  'Chest Dip',
    'decline_press':         'Decline Barbell Bench Press',
    'hip_thrust':            'Barbell Hip Thrust',
    'face_pulls':            'Face Pull',
    'calf_raises':           'Standing Calf Raise',
    'seated_calf':           'Seated Calf Raise',
    'cable_fly':             'Cable Crossover',
    'leg_curl':              'Lying Leg Curl',
    'hyperextensions':       'Hyperextensions',
}

# All unique image file keys (47 files needed)
OUR_KEYS = [
    'arnold_press','barbell_curl','barbell_row','bench_press','bicep_curls',
    'bulgarian_split_squat','cable_crunches','cable_fly','calf_raises',
    'close_grip_bench','db_press','deadlift','decline_press','dips',
    'face_pulls','front_raises','front_squat','hammer_curls','hanging_leg_raises',
    'hip_thrust','hyperextensions','incline_bench','incline_db_press',
    'lat_pulldown','lateral_raises','leg_curl','leg_extension','leg_press',
    'leg_raises','overhead_extension','overhead_press','plank','preacher_curl',
    'pull_ups','push_ups','reverse_fly','romanian_deadlift','russian_twists',
    'seated_cable_row','seated_calf','shrugs','skull_crushers','squat',
    't_bar_row','tricep_pushdown','walking_lunges','weighted_pull_ups'
]

def normalize(name):
    return re.sub(r'[^a-z0-9 ]+', ' ', name.lower()).strip()

def word_jaccard(a_words, b_name):
    b_words = set(normalize(b_name).split())
    if not a_words or not b_words:
        return 0.0
    overlap = len(a_words & b_words)
    union   = len(a_words | b_words)
    return overlap / union

def best_match(key, db_list):
    """Return best DB entry for a given key using manual map or word overlap."""
    search = MANUAL_MAP.get(key, key.replace('_', ' '))
    search_words = set(normalize(search).split())

    # First pass: exact name containment
    for ex in db_list:
        n = ex['name'].lower()
        if normalize(search) == normalize(ex['name']):
            return ex, 1.0

    # Second pass: scored word overlap
    scored = [(word_jaccard(search_words, ex['name']), ex) for ex in db_list]
    scored.sort(key=lambda x: -x[0])
    if scored and scored[0][0] > 0.2:
        return scored[0][1], scored[0][0]

    return None, 0.0

def fetch_bytes(url, retries=3):
    req = urllib.request.Request(url, headers={'User-Agent': 'RoyalFitnessClub/1.0'})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
            else:
                raise
    return None

def download_img(url):
    try:
        data = fetch_bytes(url)
        return Image.open(io.BytesIO(data)).convert('RGB')
    except Exception:
        return None

def create_gif(img0, img1, out_path):
    """2-frame looping GIF: start → end → (repeat)."""
    def prepare(img):
        # Crop to 3:2 from center, then resize
        w, h = img.size
        target_ratio = GIF_W / GIF_H
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            offset = (w - new_w) // 2
            img = img.crop((offset, 0, offset + new_w, h))
        else:
            new_h = int(w / target_ratio)
            offset = (h - new_h) // 2
            img = img.crop((0, offset, w, offset + new_h))
        return img.resize((GIF_W, GIF_H), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE, dither=Image.FLOYDSTEINBERG, colors=192)

    f0 = prepare(img0)
    f1 = prepare(img1)
    f0.save(out_path, save_all=True, append_images=[f1],
            loop=0, duration=GIF_DURATION_MS, optimize=True)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("⬇  Fetching exercise database (free-exercise-db, MIT license)...")
    db_data = json.loads(fetch_bytes(DB_URL))
    print(f"   Loaded {len(db_data)} exercises\n")

    results = {'ok': [], 'skip': [], 'fail': []}

    for key in OUR_KEYS:
        gif_path = os.path.join(OUT_DIR, f'{key}.gif')

        # Find best DB match
        ex, score = best_match(key, db_data)
        if not ex or not ex.get('images'):
            print(f"  ✗  {key:35s}  NO MATCH")
            results['fail'].append(key)
            continue

        if len(ex['images']) < 2:
            print(f"  ⚠  {key:35s}  only 1 image  ({ex['name']})")
            results['skip'].append(key)
            continue

        # Download both frames
        url0 = f"{IMG_BASE}/{ex['images'][0]}"
        url1 = f"{IMG_BASE}/{ex['images'][1]}"
        img0 = download_img(url0)
        img1 = download_img(url1)

        if not img0 or not img1:
            print(f"  ✗  {key:35s}  download failed  ({ex['name']})")
            results['fail'].append(key)
            continue

        # Save JPG originals (keep _0/_1 for any JPG fallback)
        img0.save(os.path.join(OUT_DIR, f'{key}_0.jpg'), 'JPEG', quality=88, optimize=True)
        img1.save(os.path.join(OUT_DIR, f'{key}_1.jpg'), 'JPEG', quality=88, optimize=True)

        # Create animated GIF
        create_gif(img0, img1, gif_path)
        kb = os.path.getsize(gif_path) // 1024
        print(f"  ✓  {key:35s}  → {ex['name'][:40]:40s}  [{kb} KB]")
        results['ok'].append(key)

    print(f"\n{'='*65}")
    print(f"  GIFs created : {len(results['ok'])}/{len(OUR_KEYS)}")
    if results['fail']:
        print(f"  Failed       : {', '.join(results['fail'])}")
    if results['skip']:
        print(f"  Skipped      : {', '.join(results['skip'])}")
    print(f"\n  Source: free-exercise-db (MIT License)")
    print(f"  https://github.com/yuhonas/free-exercise-db")

if __name__ == '__main__':
    main()
