#!/usr/bin/env python3
"""
Fetch warm-up exercise GIFs from free-exercise-db (MIT License).
Saves to icons/warmup/{key}.gif
"""

import json, os, re, io, time
import urllib.request
from PIL import Image

DB_URL   = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
IMG_BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises"
EX_DIR   = os.path.join(os.path.dirname(__file__), '..', 'icons', 'exercises')
WU_DIR   = os.path.join(os.path.dirname(__file__), '..', 'icons', 'warmup')

GIF_W, GIF_H     = 400, 267
GIF_DURATION_MS  = 1400

# key -> (DB exercise name, reuse_existing_gif_key_or_None)
# reuse key = path relative to icons/  e.g. 'exercises/squat.gif'
WARMUP_MAP = {
    # Upper
    'arm_circles':            ('Arm Circles',                         None),
    'band_pull_aparts':       ('Band Pull Apart',                     None),
    'shoulder_dislocates':    ('Shoulder Stretch',                    None),
    'wall_slides':            ('One Arm Against Wall',                None),
    'thoracic_rotations':     ('Torso Rotation',                      None),
    # Lower
    'leg_swings':             ('Front Leg Raises',                    None),
    'lateral_leg_swings':     ('Side Leg Raises',                     None),
    'hip_circles':            ('Standing Hip Circles',                None),
    'bodyweight_squat':       (None,                                  'exercises/squat.gif'),
    'walking_lunge_rotation': (None,                                  'exercises/walking_lunges.gif'),
    # Full body
    'jumping_jacks':          ('Star Jump',                           None),
    'worlds_greatest_stretch':("World's Greatest Stretch",            None),
    'inchworm':               ('Inchworm',                            None),
    'high_knees':             ('Knee Tuck Jump',                      None),
    # Cardio
    'march_on_spot':          ('Step-up with Knee Raise',             None),
    'ankle_rotations':        ('Ankle Circles',                       None),
    'calf_raises_wu':         (None,                                  'exercises/calf_raises.gif'),
}

def fetch_bytes(url, retries=3):
    req = urllib.request.Request(url, headers={'User-Agent': 'RoyalFitnessClub/1.0'})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except Exception:
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
    return None

def download_img(url):
    data = fetch_bytes(url)
    if not data:
        return None
    try:
        return Image.open(io.BytesIO(data)).convert('RGB')
    except Exception:
        return None

def create_gif(img0, img1, out_path):
    def prep(img):
        w, h = img.size
        tr = GIF_W / GIF_H
        if w/h > tr:
            nw = int(h * tr); off = (w-nw)//2; img = img.crop((off,0,off+nw,h))
        else:
            nh = int(w / tr); off = (h-nh)//2; img = img.crop((0,off,w,off+nh))
        return img.resize((GIF_W, GIF_H), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE, dither=Image.FLOYDSTEINBERG, colors=192)
    f0, f1 = prep(img0), prep(img1)
    f0.save(out_path, save_all=True, append_images=[f1], loop=0, duration=GIF_DURATION_MS, optimize=True)

def main():
    os.makedirs(WU_DIR, exist_ok=True)

    print("Fetching exercise database...")
    raw = fetch_bytes(DB_URL)
    if not raw:
        print("ERROR: Could not fetch DB"); return
    db = json.loads(raw)
    by_name = {ex['name']: ex for ex in db}
    print(f"Loaded {len(db)} exercises\n")

    icons_root = os.path.join(os.path.dirname(__file__), '..', 'icons')
    results = {'ok': [], 'reuse': [], 'fail': []}

    for key, (db_name, reuse) in WARMUP_MAP.items():
        out = os.path.join(WU_DIR, f'{key}.gif')

        # Reuse an existing GIF via symlink-like copy
        if reuse:
            src = os.path.join(icons_root, reuse)
            if os.path.exists(src):
                import shutil
                shutil.copy2(src, out)
                kb = os.path.getsize(out)//1024
                print(f"  ♻  {key:35s} <- {reuse}  [{kb} KB]")
                results['reuse'].append(key)
            else:
                print(f"  ✗  {key:35s}  reuse src not found: {reuse}")
                results['fail'].append(key)
            continue

        # Fetch from DB
        ex = by_name.get(db_name)
        if not ex or len(ex.get('images', [])) < 2:
            print(f"  ✗  {key:35s}  DB entry not found: {db_name}")
            results['fail'].append(key)
            continue

        img0 = download_img(f"{IMG_BASE}/{ex['images'][0]}")
        img1 = download_img(f"{IMG_BASE}/{ex['images'][1]}")
        if not img0 or not img1:
            print(f"  ✗  {key:35s}  download failed")
            results['fail'].append(key)
            continue

        create_gif(img0, img1, out)
        kb = os.path.getsize(out)//1024
        print(f"  ✓  {key:35s}  -> {db_name}  [{kb} KB]")
        results['ok'].append(key)

    print(f"\n{'='*60}")
    total = len(WARMUP_MAP)
    done  = len(results['ok']) + len(results['reuse'])
    print(f"  Done : {done}/{total}  ({len(results['ok'])} fetched, {len(results['reuse'])} reused)")
    if results['fail']:
        print(f"  Fail : {', '.join(results['fail'])}")

if __name__ == '__main__':
    main()
