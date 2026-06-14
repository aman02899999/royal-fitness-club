#!/usr/bin/env python3
"""Generate realistic RFC Academy course thumbnails (600x340, ~16:9 — no mobile crop)."""
import os

OUT = '/home/user/royal-fitness-club/thumbnails'

def w(fname, svg):
    with open(os.path.join(OUT, fname), 'w') as f: f.write(svg)

# ── shared helpers ─────────────────────────────────────────────────────────────
def top_bar(label, lcolor, badge_text, badge_color):
    return f'''  <!-- Top bar -->
  <rect width="600" height="48" fill="rgba(0,0,0,0.55)"/>
  <rect x="0" y="0" width="4" height="48" fill="#FF9933"/>
  <rect x="4" y="0" width="4" height="48" fill="#ffffff" opacity="0.9"/>
  <rect x="8" y="0" width="4" height="48" fill="#138808"/>
  <text x="22" y="20" font-family="Arial Black,Impact,sans-serif" font-size="11" font-weight="900" fill="{lcolor}" letter-spacing="2.5">RFC ACADEMY</text>
  <text x="22" y="36" font-family="Arial,sans-serif" font-size="8" fill="rgba(255,255,255,0.5)" letter-spacing="1.5">ROYAL FITNESS CLUB · CERTIFIED PROGRAMS</text>
  <rect x="488" y="11" width="104" height="26" rx="5" fill="{badge_color}"/>
  <text x="540" y="29" font-family="Arial,sans-serif" font-size="10" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">{badge_text}</text>'''

def bottom_bar(price, orig, off_pct, modules, weeks, rating, enrolled):
    return f'''  <!-- Bottom bar -->
  <rect x="0" y="290" width="600" height="50" fill="rgba(0,0,0,0.6)"/>
  <rect x="0" y="290" width="600" height="1.5" fill="rgba(255,255,255,0.12)"/>
  <rect x="22" y="303" width="88" height="27" rx="14" fill="#E8001D"/>
  <text x="66" y="321" font-family="Arial Black,sans-serif" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">₹{price}</text>
  <text x="120" y="316" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.38)" text-decoration="line-through">₹{orig}</text>
  <rect x="148" y="303" width="54" height="27" rx="5" fill="rgba(220,38,38,0.28)"/>
  <text x="175" y="321" font-family="Arial,sans-serif" font-size="10" font-weight="700" fill="#f87171" text-anchor="middle">{off_pct}% OFF</text>
  <text x="240" y="316" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.5)">📚 {modules} modules</text>
  <text x="340" y="316" font-family="Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.5)">⏱ {weeks}</text>
  <text x="430" y="316" font-family="Arial,sans-serif" font-size="11" fill="#fbbf24">★ {rating}</text>
  <text x="460" y="316" font-family="Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.4)">· {enrolled}</text>'''

def info_block(category, line1, line2, tagline, ac, stats1, stats2):
    return f'''  <!-- Left content block -->
  <rect x="22" y="62" width="3" height="190" fill="{ac}" opacity="0.8"/>
  <text x="36" y="82" font-family="Arial,sans-serif" font-size="9" fill="{ac}" letter-spacing="2.5" font-weight="700">{category}</text>
  <text x="36" y="135" font-family="Arial Black,Impact,sans-serif" font-size="46" font-weight="900" fill="#ffffff" opacity="0.97">{line1}</text>
  <text x="36" y="192" font-family="Arial Black,Impact,sans-serif" font-size="46" font-weight="900" fill="#ffffff" opacity="0.97">{line2}</text>
  <text x="36" y="218" font-family="Arial,sans-serif" font-size="12" fill="rgba(255,255,255,0.6)">{tagline}</text>
  <rect x="36" y="232" width="86" height="24" rx="12" fill="rgba(255,255,255,0.08)" stroke="{ac}" stroke-width="1" stroke-opacity="0.5"/>
  <text x="79" y="248" font-family="Arial,sans-serif" font-size="9" font-weight="700" fill="{ac}" text-anchor="middle">{stats1}</text>
  <rect x="132" y="232" width="86" height="24" rx="12" fill="rgba(255,255,255,0.08)" stroke="{ac}" stroke-width="1" stroke-opacity="0.5"/>
  <text x="175" y="248" font-family="Arial,sans-serif" font-size="9" font-weight="700" fill="{ac}" text-anchor="middle">{stats2}</text>'''

# ── Dumbbell shape (cx, cy, w=bar width, fill) ──
def dumbbell(cx, cy, bw=120, bh=10, pw=18, ph=36, fill="rgba(255,255,255,0.18)"):
    bx = cx - bw//2; by = cy - bh//2
    return f'''  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5" fill="{fill}"/>
  <rect x="{bx-pw}" y="{cy-ph//2}" width="{pw}" height="{ph}" rx="5" fill="{fill}"/>
  <rect x="{bx+bw}" y="{cy-ph//2}" width="{pw}" height="{ph}" rx="5" fill="{fill}"/>'''

# ── Barbell ──
def barbell(cx, cy, fill="rgba(255,255,255,0.18)"):
    return f'''  <rect x="{cx-90}" y="{cy-5}" width="180" height="10" rx="4" fill="{fill}"/>
  <rect x="{cx-110}" y="{cy-22}" width="22" height="44" rx="4" fill="{fill}"/>
  <rect x="{cx-90}" y="{cy-18}" width="16" height="36" rx="3" fill="{fill}" opacity="0.7"/>
  <rect x="{cx+68}" y="{cy-18}" width="16" height="36" rx="3" fill="{fill}" opacity="0.7"/>
  <rect x="{cx+88}" y="{cy-22}" width="22" height="44" rx="4" fill="{fill}"/>'''

# ── Person silhouette doing squat ──
def person_squat(cx, cy, s=1.0, fill="rgba(255,255,255,0.14)"):
    # head, torso, legs in squat
    return f'''  <circle cx="{cx}" cy="{int(cy-80*s)}" r="{int(16*s)}" fill="{fill}"/>
  <ellipse cx="{cx}" cy="{int(cy-44*s)}" rx="{int(14*s)}" ry="{int(24*s)}" fill="{fill}"/>
  <path d="M{int(cx-14*s)} {int(cy-25*s)} Q{int(cx-30*s)} {int(cy-5*s)} {int(cx-22*s)} {int(cy+10*s)} L{int(cx-10*s)} {int(cy+10*s)} Q{int(cx-4*s)} {int(cy-5*s)} {cx} {int(cy-25*s)} Z" fill="{fill}"/>
  <path d="M{cx} {int(cy-25*s)} Q{int(cx+4*s)} {int(cy-5*s)} {int(cx+10*s)} {int(cy+10*s)} L{int(cx+22*s)} {int(cy+10*s)} Q{int(cx+30*s)} {int(cy-5*s)} {int(cx+14*s)} {int(cy-25*s)} Z" fill="{fill}"/>'''

# ── Running person silhouette ──
def person_run(cx, cy, s=1.0, fill="rgba(255,255,255,0.14)"):
    return f'''  <circle cx="{int(cx+5*s)}" cy="{int(cy-95*s)}" r="{int(14*s)}" fill="{fill}"/>
  <path d="M{cx} {int(cy-80*s)} L{int(cx-8*s)} {int(cy-40*s)} L{int(cx-25*s)} {int(cy)}" stroke="{fill}" stroke-width="{int(14*s)}" fill="none" stroke-linecap="round"/>
  <path d="M{cx} {int(cy-80*s)} L{int(cx+12*s)} {int(cy-42*s)} L{int(cx+30*s)} {int(cy-8*s)}" stroke="{fill}" stroke-width="{int(12*s)}" fill="none" stroke-linecap="round"/>
  <path d="M{int(cx-8*s)} {int(cy-45*s)} L{int(cx-28*s)} {int(cy-60*s)}" stroke="{fill}" stroke-width="{int(10*s)}" fill="none" stroke-linecap="round"/>
  <path d="M{int(cx+12*s)} {int(cy-46*s)} L{int(cx+32*s)} {int(cy-36*s)}" stroke="{fill}" stroke-width="{int(10*s)}" fill="none" stroke-linecap="round"/>'''

# ── Person lifting overhead ──
def person_lift(cx, cy, s=1.0, fill="rgba(255,255,255,0.14)"):
    return f'''  <circle cx="{cx}" cy="{int(cy-95*s)}" r="{int(15*s)}" fill="{fill}"/>
  <rect x="{int(cx-12*s)}" y="{int(cy-80*s)}" width="{int(24*s)}" height="{int(40*s)}" rx="{int(8*s)}" fill="{fill}"/>
  <line x1="{int(cx-12*s)}" y1="{int(cy-58*s)}" x2="{int(cx-38*s)}" y2="{int(cy-80*s)}" stroke="{fill}" stroke-width="{int(10*s)}" stroke-linecap="round"/>
  <line x1="{int(cx+12*s)}" y1="{int(cy-58*s)}" x2="{int(cx+38*s)}" y2="{int(cy-80*s)}" stroke="{fill}" stroke-width="{int(10*s)}" stroke-linecap="round"/>
  <line x1="{int(cx-6*s)}" y1="{int(cy-40*s)}" x2="{int(cx-18*s)}" y2="{int(cy)}" stroke="{fill}" stroke-width="{int(12*s)}" stroke-linecap="round"/>
  <line x1="{int(cx+6*s)}" y1="{int(cy-40*s)}" x2="{int(cx+18*s)}" y2="{int(cy)}" stroke="{fill}" stroke-width="{int(12*s)}" stroke-linecap="round"/>'''

# ── Molecule / DNA helix ──
def molecule(cx, cy, r, fill, n=6):
    import math
    circles = ''
    for i in range(n):
        a = i * 2 * math.pi / n
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        circles += f'  <circle cx="{int(x)}" cy="{int(y)}" r="12" fill="{fill}" opacity="0.6"/>\n'
        circles += f'  <line x1="{cx}" y1="{cy}" x2="{int(x)}" y2="{int(y)}" stroke="{fill}" stroke-width="3" opacity="0.35"/>\n'
    circles += f'  <circle cx="{cx}" cy="{cy}" r="18" fill="{fill}" opacity="0.7"/>\n'
    return circles

# ── Body outline circle ring ──
def body_rings(cx, cy, ac):
    return f'''  <circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{ac}" stroke-width="1" stroke-opacity="0.12" stroke-dasharray="6,5"/>
  <circle cx="{cx}" cy="{cy}" r="55" fill="none" stroke="{ac}" stroke-width="1" stroke-opacity="0.18" stroke-dasharray="4,4"/>
  <circle cx="{cx}" cy="{cy}" r="30" fill="{ac}" opacity="0.08"/>'''

# ══════════════════════════════════════════════════════════════════════════════
# CS_B1 — Fitness Foundations Certificate  (Beginner · Green)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#22c55e"
cs_b1 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#021d0e"/><stop offset="55%" stop-color="#052e16"/><stop offset="100%" stop-color="#064e3b"/>
    </linearGradient>
    <radialGradient id="glow" cx="75%" cy="50%"><stop offset="0%" stop-color="#22c55e" stop-opacity="0.14"/><stop offset="100%" stop-color="#22c55e" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <!-- bokeh -->
  <circle cx="480" cy="140" r="130" fill="#22c55e" opacity="0.05"/>
  <circle cx="530" cy="240" r="70" fill="#4ade80" opacity="0.04"/>
{top_bar("RFC ACADEMY", ac, "BEGINNER", "#16a34a")}
{info_block("CERTIFICATE PROGRAM", "FITNESS", "FOUNDATIONS", "Build strength from the ground up", ac, "8 MODULES", "4 WEEKS")}
  <!-- dumbbell illustration right -->
{dumbbell(455, 165, 130, 12, 22, 44, ac.replace("22c55e", "22c55e") + "55")}
{dumbbell(455, 220, 110, 10, 18, 36, "rgba(34,197,94,0.25)")}
{person_squat(455, 250, 1.1, "rgba(255,255,255,0.11)")}
{body_rings(460, 180, ac)}
  <text x="410" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">STRENGTH TRAINING</text>
{bottom_bar("2,999", "5,999", 50, 8, "4 Weeks", "4.9", "2.3K+")}
</svg>'''
w('cs_b1.svg', cs_b1)

# ══════════════════════════════════════════════════════════════════════════════
# CS_B2 — Nutrition & Healthy Eating Certificate  (Beginner · Teal)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#2dd4bf"
cs_b2 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#021a17"/><stop offset="50%" stop-color="#0d2b27"/><stop offset="100%" stop-color="#134e4a"/>
    </linearGradient>
    <radialGradient id="glow" cx="70%" cy="45%"><stop offset="0%" stop-color="#2dd4bf" stop-opacity="0.13"/><stop offset="100%" stop-color="#2dd4bf" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="470" cy="150" r="120" fill="#2dd4bf" opacity="0.05"/>
  <circle cx="520" cy="260" r="60" fill="#5eead4" opacity="0.04"/>
{top_bar("RFC ACADEMY", ac, "BEGINNER", "#0d9488")}
{info_block("CERTIFICATE PROGRAM", "NUTRITION", "ESSENTIALS", "Eat smart · Live strong · Feel amazing", ac, "8 MODULES", "4 WEEKS")}
  <!-- Plate / bowl illustration -->
  <ellipse cx="458" cy="200" rx="88" ry="68" fill="none" stroke="{ac}" stroke-width="2" stroke-opacity="0.35"/>
  <ellipse cx="458" cy="200" rx="65" ry="50" fill="rgba(45,212,191,0.08)"/>
  <!-- food items on plate -->
  <ellipse cx="440" cy="192" rx="20" ry="14" fill="rgba(74,222,128,0.35)"/>
  <ellipse cx="472" cy="195" rx="16" ry="12" fill="rgba(251,191,36,0.35)"/>
  <ellipse cx="455" cy="215" rx="18" ry="12" fill="rgba(248,113,113,0.35)"/>
  <ellipse cx="435" cy="215" rx="12" ry="10" fill="rgba(167,243,208,0.35)"/>
  <!-- fork -->
  <line x1="555" y1="145" x2="545" y2="250" stroke="{ac}" stroke-width="3" stroke-opacity="0.5" stroke-linecap="round"/>
  <line x1="545" y1="145" x2="542" y2="175" stroke="{ac}" stroke-width="2" stroke-opacity="0.4"/>
  <line x1="548" y1="145" x2="546" y2="175" stroke="{ac}" stroke-width="2" stroke-opacity="0.4"/>
  <line x1="551" y1="145" x2="549" y2="175" stroke="{ac}" stroke-width="2" stroke-opacity="0.4"/>
  <!-- macros ring -->
{body_rings(458, 200, ac)}
  <text x="412" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">NUTRITION SCIENCE</text>
{bottom_bar("3,499", "6,999", 50, 8, "4 Weeks", "4.8", "1.9K+")}
</svg>'''
w('cs_b2.svg', cs_b2)

# ══════════════════════════════════════════════════════════════════════════════
# CS_B3 — Body Transformation Blueprint  (Beginner · Orange/Fire)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#f97316"
cs_b3 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1c0a04"/><stop offset="50%" stop-color="#431407"/><stop offset="100%" stop-color="#7c2d12"/>
    </linearGradient>
    <linearGradient id="fire" x1="0.5" y1="1" x2="0.5" y2="0">
      <stop offset="0%" stop-color="#dc2626" stop-opacity="0.6"/>
      <stop offset="60%" stop-color="#f97316" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0.2"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="50%"><stop offset="0%" stop-color="#f97316" stop-opacity="0.18"/><stop offset="100%" stop-color="#f97316" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="480" cy="155" r="115" fill="#f97316" opacity="0.06"/>
  <circle cx="540" cy="245" r="60" fill="#fbbf24" opacity="0.04"/>
{top_bar("RFC ACADEMY", ac, "BEGINNER", "#c2410c")}
{info_block("TRANSFORMATION PROGRAM", "BODY", "TRANSFORM", "Burn fat · Build muscle · Change your life", ac, "8 MODULES", "6 WEEKS")}
  <!-- Before/After silhouettes -->
  <!-- BEFORE (heavier) -->
  <circle cx="405" cy="135" r="14" fill="rgba(255,255,255,0.1)"/>
  <ellipse cx="405" cy="180" rx="20" ry="30" fill="rgba(255,255,255,0.08)"/>
  <rect x="388" y="205" width="14" height="48" rx="7" fill="rgba(255,255,255,0.08)"/>
  <rect x="405" y="205" width="14" height="48" rx="7" fill="rgba(255,255,255,0.08)"/>
  <!-- AFTER (leaner) -->
  <circle cx="468" cy="132" r="13" fill="rgba(255,255,255,0.18)"/>
  <ellipse cx="468" cy="172" rx="13" ry="26" fill="rgba(255,255,255,0.15)"/>
  <rect x="458" y="196" width="10" height="52" rx="5" fill="rgba(255,255,255,0.15)" transform="rotate(-4 463 222)"/>
  <rect x="470" y="196" width="10" height="52" rx="5" fill="rgba(255,255,255,0.15)" transform="rotate(4 475 222)"/>
  <!-- Arrow between them -->
  <line x1="425" y1="180" x2="452" y2="180" stroke="{ac}" stroke-width="2.5" stroke-opacity="0.8"/>
  <polygon points="452,175 460,180 452,185" fill="{ac}" opacity="0.8"/>
  <!-- flame shapes -->
  <path d="M500 280 Q494 250 504 235 Q508 248 516 240 Q512 260 520 280 Z" fill="url(#fire)"/>
  <path d="M520 280 Q514 245 526 228 Q532 244 540 235 Q534 260 542 280 Z" fill="url(#fire)"/>
  <path d="M540 280 Q532 252 546 238 Q548 255 556 248 Q550 265 558 280 Z" fill="url(#fire)" opacity="0.7"/>
{body_rings(480, 190, ac)}
  <text x="480" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">FAT LOSS · MUSCLE GAIN</text>
{bottom_bar("3,999", "7,999", 50, 8, "6 Weeks", "4.9", "1.6K+")}
</svg>'''
w('cs_b3.svg', cs_b3)

# ══════════════════════════════════════════════════════════════════════════════
# CS_A1 — Certified Personal Trainer (CPT)  (Advanced · Blue/Amber)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#3b82f6"
cs_a1 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#030712"/><stop offset="50%" stop-color="#0c1a3a"/><stop offset="100%" stop-color="#1e3a6e"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="45%"><stop offset="0%" stop-color="#3b82f6" stop-opacity="0.15"/><stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="488" cy="155" r="125" fill="#3b82f6" opacity="0.06"/>
  <circle cx="540" cy="250" r="65" fill="#60a5fa" opacity="0.04"/>
{top_bar("RFC ACADEMY", ac, "ADVANCED", "#1d4ed8")}
{info_block("PROFESSIONAL CERTIFICATION", "PERSONAL", "TRAINER (CPT)", "Certify · Coach · Transform clients", ac, "12 MODULES", "10 WEEKS")}
  <!-- Trainer with client illustration -->
{person_lift(452, 260, 1.15, "rgba(255,255,255,0.15)")}
{barbell(452, 148, "rgba(59,130,246,0.5)")}
  <!-- Clipboard / certification -->
  <rect x="528" y="110" width="48" height="60" rx="4" fill="rgba(255,255,255,0.08)" stroke="{ac}" stroke-width="1" stroke-opacity="0.5"/>
  <rect x="540" y="106" width="24" height="8" rx="4" fill="rgba(255,255,255,0.15)"/>
  <line x1="537" y1="126" x2="568" y2="126" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.5"/>
  <line x1="537" y1="135" x2="568" y2="135" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.5"/>
  <line x1="537" y1="144" x2="560" y2="144" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.5"/>
  <text x="552" y="160" font-family="Arial,sans-serif" font-size="8" fill="{ac}" text-anchor="middle" font-weight="700">CPT</text>
{body_rings(462, 195, ac)}
  <text x="412" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">PERSONAL TRAINING</text>
{bottom_bar("5,999", "11,999", 50, 12, "10 Weeks", "4.9", "1.1K+")}
</svg>'''
w('cs_a1.svg', cs_a1)

# ══════════════════════════════════════════════════════════════════════════════
# CS_A2 — Sports Nutrition & Dietetics Diploma  (Advanced · Purple)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#a855f7"
cs_a2 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d0219"/><stop offset="50%" stop-color="#1e0a3d"/><stop offset="100%" stop-color="#2e1065"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="48%"><stop offset="0%" stop-color="#a855f7" stop-opacity="0.16"/><stop offset="100%" stop-color="#a855f7" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="478" cy="158" r="120" fill="#a855f7" opacity="0.06"/>
{top_bar("RFC ACADEMY", ac, "ADVANCED", "#7e22ce")}
{info_block("DIPLOMA PROGRAM", "SPORTS", "NUTRITION", "Clinical dietetics for athletic excellence", ac, "10 MODULES", "10 WEEKS")}
  <!-- Molecule / DNA illustration -->
{molecule(468, 185, 70, ac, 6)}
  <!-- Helix lines -->
  <path d="M415 130 Q440 160 415 190 Q440 220 415 250" stroke="{ac}" stroke-width="2" fill="none" stroke-opacity="0.4" stroke-dasharray="5,3"/>
  <path d="M425 130 Q450 160 425 190 Q450 220 425 250" stroke="#c084fc" stroke-width="2" fill="none" stroke-opacity="0.3" stroke-dasharray="5,3"/>
  <!-- connecting rungs -->
  <line x1="415" y1="148" x2="425" y2="148" stroke="{ac}" stroke-width="2" stroke-opacity="0.45"/>
  <line x1="415" y1="170" x2="425" y2="170" stroke="{ac}" stroke-width="2" stroke-opacity="0.45"/>
  <line x1="415" y1="192" x2="425" y2="192" stroke="{ac}" stroke-width="2" stroke-opacity="0.45"/>
  <line x1="415" y1="214" x2="425" y2="214" stroke="{ac}" stroke-width="2" stroke-opacity="0.45"/>
{body_rings(468, 185, ac)}
  <text x="420" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">SPORTS DIETETICS</text>
{bottom_bar("6,999", "13,999", 50, 10, "10 Weeks", "4.8", "890+")}
</svg>'''
w('cs_a2.svg', cs_a2)

# ══════════════════════════════════════════════════════════════════════════════
# CS_A3 — Physio & Sports Rehabilitation Diploma  (Advanced · Cyan/Blue)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#06b6d4"
cs_a3 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#021b1f"/><stop offset="50%" stop-color="#0a2f38"/><stop offset="100%" stop-color="#134e4a"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="47%"><stop offset="0%" stop-color="#06b6d4" stop-opacity="0.14"/><stop offset="100%" stop-color="#06b6d4" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="478" cy="160" r="118" fill="#06b6d4" opacity="0.06"/>
{top_bar("RFC ACADEMY", ac, "ADVANCED", "#0e7490")}
{info_block("DIPLOMA PROGRAM", "SPORTS", "PHYSIO", "Rehabilitate · Recover · Return to sport", ac, "10 MODULES", "8 WEEKS")}
  <!-- Anatomy body outline -->
  <!-- Head -->
  <circle cx="468" cy="110" r="22" fill="none" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.5"/>
  <!-- Spine -->
  <line x1="468" y1="132" x2="468" y2="230" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.4" stroke-dasharray="4,3"/>
  <!-- Ribcage -->
  <ellipse cx="468" cy="175" rx="38" ry="28" fill="none" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.4"/>
  <ellipse cx="468" cy="175" rx="28" ry="20" fill="none" stroke="{ac}" stroke-width="1" stroke-opacity="0.25"/>
  <!-- Shoulder lines -->
  <line x1="430" y1="145" x2="506" y2="145" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.45"/>
  <!-- Arms -->
  <path d="M430 145 Q410 175 415 210" stroke="{ac}" stroke-width="8" fill="none" stroke-linecap="round" stroke-opacity="0.2"/>
  <path d="M506 145 Q526 175 521 210" stroke="{ac}" stroke-width="8" fill="none" stroke-linecap="round" stroke-opacity="0.2"/>
  <!-- Hip/pelvis -->
  <ellipse cx="468" cy="230" rx="30" ry="16" fill="none" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.4"/>
  <!-- Legs -->
  <path d="M455 244 Q448 265 450 285" stroke="{ac}" stroke-width="10" fill="none" stroke-linecap="round" stroke-opacity="0.18"/>
  <path d="M481 244 Q488 265 486 285" stroke="{ac}" stroke-width="10" fill="none" stroke-linecap="round" stroke-opacity="0.18"/>
  <!-- Joint highlight circles -->
  <circle cx="430" cy="145" r="6" fill="{ac}" opacity="0.4"/>
  <circle cx="506" cy="145" r="6" fill="{ac}" opacity="0.4"/>
  <circle cx="415" cy="210" r="5" fill="{ac}" opacity="0.35"/>
  <circle cx="521" cy="210" r="5" fill="{ac}" opacity="0.35"/>
  <circle cx="450" cy="285" r="5" fill="{ac}" opacity="0.3"/>
  <circle cx="486" cy="285" r="5" fill="{ac}" opacity="0.3"/>
  <!-- Medical cross -->
  <rect x="543" y="135" width="8" height="28" rx="3" fill="{ac}" opacity="0.5"/>
  <rect x="535" y="143" width="24" height="8" rx="3" fill="{ac}" opacity="0.5"/>
  <text x="428" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">REHABILITATION</text>
{bottom_bar("5,499", "10,999", 50, 10, "8 Weeks", "4.8", "650+")}
</svg>'''
w('cs_a3.svg', cs_a3)

# ══════════════════════════════════════════════════════════════════════════════
# CS_A4 — Fat Loss Specialist (FLS) Certification  (Advanced · Orange/Amber)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#f59e0b"
cs_a4 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1c1004"/><stop offset="50%" stop-color="#3b1f06"/><stop offset="100%" stop-color="#6b3a0a"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="46%"><stop offset="0%" stop-color="#f59e0b" stop-opacity="0.16"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="478" cy="158" r="120" fill="#f59e0b" opacity="0.06"/>
{top_bar("RFC ACADEMY", ac, "ADVANCED", "#b45309")}
{info_block("SPECIALIST CERTIFICATION", "FAT LOSS", "SPECIALIST", "Science-backed protocols for rapid fat loss", ac, "8 MODULES", "6 WEEKS")}
  <!-- Target / bullseye -->
  <circle cx="468" cy="183" r="90" fill="none" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.15"/>
  <circle cx="468" cy="183" r="65" fill="none" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.22"/>
  <circle cx="468" cy="183" r="42" fill="none" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.32"/>
  <circle cx="468" cy="183" r="22" fill="none" stroke="{ac}" stroke-width="2" stroke-opacity="0.5"/>
  <circle cx="468" cy="183" r="8" fill="{ac}" opacity="0.7"/>
  <!-- Arrow hitting target -->
  <line x1="410" y1="125" x2="462" y2="179" stroke="{ac}" stroke-width="3" stroke-opacity="0.8"/>
  <polygon points="462,179 452,169 458,162" fill="{ac}" opacity="0.9"/>
  <!-- Feathers of arrow -->
  <path d="M410 125 L402 118 L414 120 Z" fill="{ac}" opacity="0.7"/>
  <path d="M410 125 L404 132 L416 128 Z" fill="{ac}" opacity="0.7"/>
{person_run(540, 260, 0.9, "rgba(255,255,255,0.13)")}
  <text x="420" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">FAT LOSS SCIENCE</text>
{bottom_bar("4,999", "9,999", 50, 8, "6 Weeks", "4.9", "1.4K+")}
</svg>'''
w('cs_a4.svg', cs_a4)

# ══════════════════════════════════════════════════════════════════════════════
# CS_M1 — Elite Performance & Fitness Master  (Master · Gold/Dark)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#eab308"
cs_m1 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a0700"/><stop offset="45%" stop-color="#1a1200"/><stop offset="100%" stop-color="#2d2000"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fbbf24"/><stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="46%"><stop offset="0%" stop-color="#eab308" stop-opacity="0.2"/><stop offset="100%" stop-color="#eab308" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="480" cy="155" r="130" fill="#eab308" opacity="0.07"/>
  <circle cx="540" cy="250" r="65" fill="#fbbf24" opacity="0.04"/>
{top_bar("RFC ACADEMY", "#fbbf24", "MASTER", "#92400e")}
{info_block("MASTER CERTIFICATION", "ELITE", "PERFORMANCE", "Peak performance · Elite coaching mastery", "#fbbf24", "15 MODULES", "16 WEEKS")}
  <!-- Crown illustration -->
  <path d="M395 200 L395 240 L545 240 L545 200 L530 170 L510 200 L470 160 L430 200 L410 170 Z" fill="url(#gold)" opacity="0.7"/>
  <circle cx="470" cy="157" r="10" fill="#fbbf24" opacity="0.9"/>
  <circle cx="530" cy="168" r="8" fill="#fbbf24" opacity="0.8"/>
  <circle cx="410" cy="168" r="8" fill="#fbbf24" opacity="0.8"/>
  <!-- Gems on crown -->
  <polygon points="428,198 436,186 444,198 436,210" fill="#ef4444" opacity="0.8"/>
  <polygon points="461,196 469,184 477,196 469,208" fill="#3b82f6" opacity="0.8"/>
  <polygon points="496,198 504,186 512,198 504,210" fill="#22c55e" opacity="0.8"/>
  <!-- Shine on crown -->
  <path d="M400 205 L395 200 L410 170 L430 200" fill="rgba(255,255,255,0.12)"/>
  <!-- Stars -->
  <text x="430" y="275" font-family="Arial,sans-serif" font-size="14" fill="#fbbf24" opacity="0.7">✦ ✦ ✦ ✦ ✦</text>
{bottom_bar("9,999", "19,999", 50, 15, "16 Weeks", "4.9", "380+")}
</svg>'''
w('cs_m1.svg', cs_m1)

# ══════════════════════════════════════════════════════════════════════════════
# CS_M2 — Pharmaceutical Performance Science 18+  (Master · Dark Red)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#ef4444"
cs_m2 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f0000"/><stop offset="50%" stop-color="#1f0505"/><stop offset="100%" stop-color="#3b0b0b"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="46%"><stop offset="0%" stop-color="#ef4444" stop-opacity="0.16"/><stop offset="100%" stop-color="#ef4444" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="480" cy="155" r="120" fill="#ef4444" opacity="0.06"/>
{top_bar("RFC ACADEMY", ac, "MASTER  18+", "#991b1b")}
{info_block("MASTER PROGRAM  ⚠️ 18+", "PHARMA", "SCIENCE", "Evidence-based performance pharmacology", ac, "12 MODULES", "14 WEEKS")}
  <!-- Flask / Erlenmeyer flask illustration -->
  <!-- Flask body -->
  <path d="M440 130 L440 185 L408 240 L535 240 L502 185 L502 130 Z" fill="rgba(239,68,68,0.12)" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.5"/>
  <!-- Flask neck -->
  <rect x="455" y="108" width="32" height="26" rx="3" fill="rgba(239,68,68,0.15)" stroke="{ac}" stroke-width="1.5" stroke-opacity="0.5"/>
  <!-- Flask stopper -->
  <rect x="451" y="104" width="40" height="8" rx="2" fill="{ac}" opacity="0.5"/>
  <!-- Liquid in flask -->
  <path d="M440 210 L420 240 L525 240 L505 210 Z" fill="rgba(239,68,68,0.3)"/>
  <!-- Bubbles in liquid -->
  <circle cx="455" cy="225" r="5" fill="{ac}" opacity="0.35"/>
  <circle cx="475" cy="218" r="4" fill="{ac}" opacity="0.3"/>
  <circle cx="495" cy="228" r="3" fill="{ac}" opacity="0.25"/>
  <!-- Rising bubbles -->
  <circle cx="462" cy="195" r="3" fill="{ac}" opacity="0.2"/>
  <circle cx="482" cy="188" r="2.5" fill="{ac}" opacity="0.18"/>
  <circle cx="471" cy="175" r="2" fill="{ac}" opacity="0.15"/>
  <!-- Molecule dots around -->
{molecule(540, 165, 30, ac, 5)}
  <text x="430" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">EDUCATIONAL · 18+ ONLY</text>
{bottom_bar("9,999", "19,999", 50, 12, "14 Weeks", "4.9", "290+")}
</svg>'''
w('cs_m2.svg', cs_m2)

# ══════════════════════════════════════════════════════════════════════════════
# CS_M3 — Sports Medicine & Physio Expert  (Master · Teal/Dark)
# ══════════════════════════════════════════════════════════════════════════════
ac = "#14b8a6"
cs_m3 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020e0d"/><stop offset="50%" stop-color="#0a1f1e"/><stop offset="100%" stop-color="#0f3635"/>
    </linearGradient>
    <radialGradient id="glow" cx="72%" cy="46%"><stop offset="0%" stop-color="#14b8a6" stop-opacity="0.16"/><stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="600" height="340" fill="url(#bg)"/>
  <rect width="600" height="340" fill="url(#glow)"/>
  <circle cx="480" cy="155" r="120" fill="#14b8a6" opacity="0.06"/>
{top_bar("RFC ACADEMY", ac, "MASTER", "#0f766e")}
{info_block("EXPERT CERTIFICATION", "SPORTS", "MEDICINE", "Advanced clinical sports medicine expertise", ac, "14 MODULES", "12 WEEKS")}
  <!-- Stethoscope illustration -->
  <!-- Earpiece left -->
  <circle cx="422" cy="118" r="8" fill="{ac}" opacity="0.45"/>
  <!-- Earpiece right -->
  <circle cx="514" cy="118" r="8" fill="{ac}" opacity="0.45"/>
  <!-- Tubing from earpieces down to Y junction -->
  <path d="M422 126 Q422 155 468 170" stroke="{ac}" stroke-width="5" fill="none" stroke-linecap="round" stroke-opacity="0.55"/>
  <path d="M514 126 Q514 155 468 170" stroke="{ac}" stroke-width="5" fill="none" stroke-linecap="round" stroke-opacity="0.55"/>
  <!-- Tube down to chestpiece -->
  <path d="M468 170 Q468 210 480 235" stroke="{ac}" stroke-width="5" fill="none" stroke-linecap="round" stroke-opacity="0.55"/>
  <!-- Chestpiece -->
  <circle cx="482" cy="242" r="18" fill="{ac}" opacity="0.35"/>
  <circle cx="482" cy="242" r="12" fill="{ac}" opacity="0.5"/>
  <circle cx="482" cy="242" r="5" fill="{ac}" opacity="0.8"/>
  <!-- Medical cross in background -->
  <rect x="538" y="120" width="10" height="36" rx="4" fill="{ac}" opacity="0.3"/>
  <rect x="524" y="134" width="38" height="10" rx="4" fill="{ac}" opacity="0.3"/>
{body_rings(468, 185, ac)}
  <text x="420" y="278" font-family="Arial,sans-serif" font-size="9" fill="{ac}" text-anchor="middle" letter-spacing="1" opacity="0.7">SPORTS MEDICINE</text>
{bottom_bar("8,999", "17,999", 50, 14, "12 Weeks", "4.8", "220+")}
</svg>'''
w('cs_m3.svg', cs_m3)

print("✅ All 10 thumbnails generated in", OUT)
