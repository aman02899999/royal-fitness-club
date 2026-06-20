#!/usr/bin/env python3
"""
Fetch animated GIFs for the 13 new workout tab exercises.
Uses free-exercise-db (MIT License): https://github.com/yuhonas/free-exercise-db
Follows the same pattern as fetch-exercise-gifs.py
"""

import json, os, re, io, time
import urllib.request
from PIL import Image

DB_URL   = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
IMG_BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises"
OUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'icons', 'exercises')

GIF_W, GIF_H    = 400, 267
GIF_DURATION_MS = 1400

# key -> exact DB exercise name to look up
EXERCISE_MAP = {
    'mountain_climbers': 'Mountain Climbers',
    'burpees':           'Burpees',
    'bicycle_crunches':  'Bicycle Crunch',
    'crunches':          'Crunches',
    'jump_squats':       'Freehand Jump Squat',
    'high_knees':        'Knee Tuck Jump',
    'jumping_jacks':     'Star Jump',
    'jump_lunges':       'Jump Lunge',
    'side_plank':        'Side Bridge',
    'box_jumps':         'Front Box Jump',
    'wall_sit':          'Wall Squat',
    'superman':          'Superman',
    'step_ups':          'Dumbbell Step Ups',
}

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
                print(f"    [fetch error: {e}]")
    return None

def download_img(url):
    data = fetch_bytes(url)
    if not data:
        return None
    try:
        return Image.open(io.BytesIO(data)).convert('RGB')
    except Exception as e:
        print(f"    [image decode error: {e}]")
        return None

def create_gif(img0, img1, out_path):
    def prep(img):
        w, h = img.size
        tr = GIF_W / GIF_H
        if w / h > tr:
            nw = int(h * tr); off = (w - nw) // 2
            img = img.crop((off, 0, off + nw, h))
        else:
            nh = int(w / tr); off = (h - nh) // 2
            img = img.crop((0, off, w, off + nh))
        return img.resize((GIF_W, GIF_H), Image.LANCZOS).convert(
            'P', palette=Image.ADAPTIVE, dither=Image.FLOYDSTEINBERG, colors=192)
    f0, f1 = prep(img0), prep(img1)
    f0.save(out_path, save_all=True, append_images=[f1],
            loop=0, duration=GIF_DURATION_MS, optimize=True)

def normalize(name):
    return re.sub(r'[^a-z0-9 ]+', ' ', name.lower()).strip()

def find_exercise(db, preferred_name):
    """Look up by exact name first, then case-insensitive, then word overlap."""
    by_name = {ex['name']: ex for ex in db}
    # Exact
    if preferred_name in by_name:
        return by_name[preferred_name]
    # Case-insensitive
    lower = preferred_name.lower()
    for ex in db:
        if ex['name'].lower() == lower:
            return ex
    # Word-overlap fallback
    search_words = set(normalize(preferred_name).split())
    best_score, best_ex = 0.0, None
    for ex in db:
        ex_words = set(normalize(ex['name']).split())
        if not search_words or not ex_words:
            continue
        overlap = len(search_words & ex_words)
        union   = len(search_words | ex_words)
        score   = overlap / union
        if score > best_score:
            best_score, best_ex = score, ex
    if best_score > 0.25:
        return best_ex
    return None

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Fetching exercise database (free-exercise-db, MIT license)...")
    raw = fetch_bytes(DB_URL)
    if not raw:
        print("ERROR: could not fetch DB"); return
    db = json.loads(raw)
    print(f"Loaded {len(db)} exercises\n")

    results = {'ok': [], 'fail': []}

    for key, db_name in EXERCISE_MAP.items():
        gif_path = os.path.join(OUT_DIR, f'{key}.gif')

        ex = find_exercise(db, db_name)
        if not ex or len(ex.get('images', [])) < 2:
            alt_tried = db_name
            print(f"  FAIL  {key:25s}  no DB match for '{alt_tried}'")
            results['fail'].append(key)
            continue

        url0 = f"{IMG_BASE}/{ex['images'][0]}"
        url1 = f"{IMG_BASE}/{ex['images'][1]}"
        img0 = download_img(url0)
        img1 = download_img(url1)

        if not img0 or not img1:
            print(f"  FAIL  {key:25s}  download failed ({ex['name']})")
            results['fail'].append(key)
            continue

        # Save JPG originals (consistent with existing convention)
        img0.save(os.path.join(OUT_DIR, f'{key}_0.jpg'), 'JPEG', quality=88, optimize=True)
        img1.save(os.path.join(OUT_DIR, f'{key}_1.jpg'), 'JPEG', quality=88, optimize=True)

        create_gif(img0, img1, gif_path)
        kb = os.path.getsize(gif_path) // 1024
        print(f"  OK    {key:25s}  -> {ex['name'][:45]}  [{kb} KB]")
        results['ok'].append(key)

    print(f"\n{'='*65}")
    print(f"  Created : {len(results['ok'])}/{len(EXERCISE_MAP)}")
    if results['ok']:
        print(f"  Success : {', '.join(results['ok'])}")
    if results['fail']:
        print(f"  Failed  : {', '.join(results['fail'])}")
    print(f"\n  Source: free-exercise-db (MIT License)")
    print(f"  https://github.com/yuhonas/free-exercise-db")

if __name__ == '__main__':
    main()
