#!/usr/bin/env python3
"""Revert to dark-red theme, compact nav/plans, ensure mobile compat."""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. CSS VARIABLES → dark-red ──────────────────────────────────────────
html = html.replace(
    ':root{--red:#7c3aed;--orange:#a855f7;--gold:#ffd000;--dark:#f8f6ff;--card:#ffffff;--card2:#f0ebff;--border:#e2d9f3;--border2:#d4c8ef;--text:#1e1b4b;--muted:#6b7280;--muted2:#9ca3af;--pro:linear-gradient(135deg,#7c3aed,#a855f7);--fire:linear-gradient(135deg,#6d28d9,#a855f7);--green:#16a34a;--blue:#2563eb;}',
    ':root{--red:#e8001d;--orange:#ff4500;--gold:#ffd000;--dark:#070707;--card:#101010;--card2:#141414;--border:#222;--border2:#2c2c2c;--text:#f0f0f0;--muted:#a0a0a0;--muted2:#707070;--pro:linear-gradient(135deg,#ffd000,#ff4500);--fire:linear-gradient(135deg,#e8001d,#ff4500);--green:#22c55e;--blue:#38bdf8;}'
)

# ── 2. SCROLLBAR TRACK ────────────────────────────────────────────────────
html = html.replace('::-webkit-scrollbar-track{background:#ede9fe;}',
                    '::-webkit-scrollbar-track{background:#0a0a0a;}')

# ── 3. NAV — compact, dark ───────────────────────────────────────────────
html = html.replace(
    'nav{position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;justify-content:space-between;padding:0 36px;height:62px;background:rgba(255,255,255,.97);border-bottom:1px solid var(--border);backdrop-filter:blur(20px);box-shadow:0 1px 20px rgba(124,58,237,.08);}',
    'nav{position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;justify-content:space-between;padding:0 28px;height:54px;background:rgba(7,7,7,.97);border-bottom:1px solid var(--border);backdrop-filter:blur(20px);box-shadow:0 1px 20px rgba(232,0,29,.08);}'
)

# ── 4. HERO BACKGROUND ────────────────────────────────────────────────────
html = html.replace(
    '.hbg{position:absolute;inset:0;background:radial-gradient(ellipse 90% 70% at 50% -5%,rgba(124,58,237,.12) 0%,transparent 65%),#f8f6ff;}',
    '.hbg{position:absolute;inset:0;background:radial-gradient(ellipse 90% 70% at 50% -5%,rgba(232,0,29,.22) 0%,transparent 65%),#070707;}'
)
html = html.replace(
    '.hgrid{position:absolute;inset:0;background-image:linear-gradient(rgba(124,58,237,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(124,58,237,.05) 1px,transparent 1px);background-size:48px 48px;mask-image:radial-gradient(ellipse 80% 80% at 50% 50%,black 20%,transparent 100%);}',
    '.hgrid{position:absolute;inset:0;background-image:linear-gradient(rgba(232,0,29,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(232,0,29,.04) 1px,transparent 1px);background-size:48px 48px;mask-image:radial-gradient(ellipse 80% 80% at 50% 50%,black 20%,transparent 100%);}'
)

# ── 5. HERO TAG border ────────────────────────────────────────────────────
html = html.replace('border:1px solid rgba(124,58,237,.3);padding:5px 18px;border-radius:2px;display:inline-block',
                    'border:1px solid rgba(232,0,29,.3);padding:5px 18px;border-radius:2px;display:inline-block')

# ── 6. .bfire:hover shadow ────────────────────────────────────────────────
html = html.replace('box-shadow:0 12px 38px rgba(109,40,217,.35);}',
                    'box-shadow:0 12px 38px rgba(232,0,29,.4);}')
html = html.replace('box-shadow:0 8px 28px rgba(109,40,217,.3);}',
                    'box-shadow:0 8px 28px rgba(232,0,29,.3);}')

# ── 7. PLANS SECTION — compact 2-col desktop layout ───────────────────────
# Change 1-col grid to 2-col, reduce padding/price
html = html.replace(
    '.plans2{display:grid;grid-template-columns:1fr;gap:20px;margin-top:40px;}',
    '.plans2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:32px;}'
)
html = html.replace(
    '@media(max-width:700px){.plans2{grid-template-columns:1fr;}}',
    '@media(max-width:700px){.plans2{grid-template-columns:1fr;}}'
)
# Compact pcard padding
html = html.replace(
    '.pcard{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:34px 26px;position:relative;overflow:hidden;transition:transform .3s;}',
    '.pcard{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:22px 20px;position:relative;overflow:hidden;transition:transform .3s;}'
)
# Compact price font — inline overrides
html = html.replace('.pprice{font-family:\'Bebas Neue\',sans-serif;font-size:60px;line-height:1;}',
                    '.pprice{font-family:\'Bebas Neue\',sans-serif;font-size:48px;line-height:1;}')
# Override !important size
html = html.replace('.pprice{font-size:68px!important;}',
                    '.pprice{font-size:50px!important;}')
# Compact feature list gap
html = html.replace('.pfeats{list-style:none;display:flex;flex-direction:column;gap:0;margin-bottom:26px;}',
                    '.pfeats{list-style:none;display:flex;flex-direction:column;gap:0;margin-bottom:18px;}')
html = html.replace('padding:8px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:13px;}',
                    'padding:6px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:13px;}')
# Compact per-line
html = html.replace('.pper{font-size:12px;color:var(--muted);margin-bottom:22px;}',
                    '.pper{font-size:12px;color:var(--muted);margin-bottom:14px;}')

# ── 8. MOBILE NAV — dark background ──────────────────────────────────────
html = html.replace(
    '.nlinks{display:none;position:fixed;top:62px;left:0;right:0;background:rgba(255,255,255,.98);border-bottom:1px solid var(--border);backdrop-filter:blur(20px);flex-direction:column;padding:16px 20px 20px;gap:0;z-index:999;}',
    '.nlinks{display:none;position:fixed;top:54px;left:0;right:0;background:rgba(7,7,7,.98);border-bottom:1px solid var(--border);backdrop-filter:blur(20px);flex-direction:column;padding:16px 20px 20px;gap:0;z-index:999;}'
)

# ── 9. NAV DROPDOWN — dark background ────────────────────────────────────
html = html.replace(
    '.ndrop-menu{display:none;position:absolute;top:calc(100% + 4px);left:50%;transform:translateX(-50%);background:rgba(255,255,255,.98);border:1px solid var(--border);border-radius:8px;min-width:220px;z-index:9999;padding:4px 0;backdrop-filter:blur(20px);box-shadow:0 8px 32px rgba(124,58,237,.15);}',
    '.ndrop-menu{display:none;position:absolute;top:calc(100% + 4px);left:50%;transform:translateX(-50%);background:rgba(10,10,10,.98);border:1px solid var(--border);border-radius:8px;min-width:220px;z-index:9999;padding:4px 0;backdrop-filter:blur(20px);box-shadow:0 8px 32px rgba(232,0,29,.15);}'
)

# ── 10. FOOTER ────────────────────────────────────────────────────────────
html = html.replace('#gym-gate{position:fixed;inset:0;background:#f8f6ff;',
                    '#gym-gate{position:fixed;inset:0;background:#070707;')

# ── 11. MACRO BAR BACKGROUNDS (light violet → dark) ──────────────────────
html = html.replace('.macbarbg{background:#ede9fe;', '.macbarbg{background:#1a1a1a;')
html = html.replace('.gbg{background:#ede9fe;', '.gbg{background:#1a1a1a;')
html = html.replace('.wcht{margin-top:9px;background:#f0ebff;', '.wcht{margin-top:9px;background:#111;')
html = html.replace('.wlinp{flex:1;background:#f8f6ff;', '.wlinp{flex:1;background:#111;')
html = html.replace('.gbtn{flex:1;padding:6px;background:#f0ebff;', '.gbtn{flex:1;padding:6px;background:#1a1a1a;')

# ── 12. PDF STORE — dark sections ─────────────────────────────────────────
html = html.replace(
    '.pdf-bonus-section{margin-top:48px;background:linear-gradient(135deg,#f0ebff,#e8e0f7);border:1px solid rgba(124,58,237,.25);border-radius:12px;padding:28px 24px;}',
    '.pdf-bonus-section{margin-top:48px;background:linear-gradient(135deg,#0a0a0a,#111);border:1px solid var(--border);border-radius:12px;padding:28px 24px;}'
)
html = html.replace(
    '.pdf-final-cta{margin-top:52px;text-align:center;background:linear-gradient(135deg,#f0ebff,#e8e0f7);border:1px solid var(--border);border-radius:16px;padding:44px 24px;}',
    '.pdf-final-cta{margin-top:52px;text-align:center;background:linear-gradient(135deg,#0a0a0a,#111);border:1px solid var(--border);border-radius:16px;padding:44px 24px;}'
)
html = html.replace(
    '.pdf-sticky-bar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:999;background:rgba(255,255,255,.97);border-top:2px solid var(--border);padding:10px 16px;align-items:center;gap:12px;box-shadow:0 -4px 20px rgba(124,58,237,.12);}',
    '.pdf-sticky-bar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:999;background:rgba(7,7,7,.97);border-top:2px solid var(--border);padding:10px 16px;align-items:center;gap:12px;box-shadow:0 -4px 20px rgba(232,0,29,.12);}'
)

# ── 13. STORE SECTION background ─────────────────────────────────────────
html = html.replace(
    '.shopbox{background:linear-gradient(135deg,rgba(124,58,237,.08),rgba(168,85,247,.05));border:1px solid rgba(124,58,237,.13);',
    '.shopbox{background:linear-gradient(135deg,rgba(232,0,29,.07),rgba(255,69,0,.04));border:1px solid rgba(232,0,29,.12);'
)

# ── 14. DIET HEADER BAR ────────────────────────────────────────────────────
html = html.replace(
    '.diet-header-bar{background:linear-gradient(135deg,rgba(124,58,237,.12),rgba(168,85,247,.08));border:1px solid rgba(124,58,237,.2);',
    '.diet-header-bar{background:linear-gradient(135deg,rgba(232,0,29,.10),rgba(255,69,0,.06));border:1px solid rgba(232,0,29,.2);'
)

# ── 15. PROFILE HEAD gradient ─────────────────────────────────────────────
html = html.replace(
    '.prof-head{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:linear-gradient(135deg,rgba(124,58,237,.08),rgba(168,85,247,.04));',
    '.prof-head{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:linear-gradient(135deg,rgba(232,0,29,.07),rgba(255,69,0,.03));'
)

# ── 16. PROGATE / MEAL LOCK gradient ─────────────────────────────────────
html = html.replace(
    '.progate{background:linear-gradient(135deg,rgba(255,208,0,.05),rgba(168,85,247,.05));',
    '.progate{background:linear-gradient(135deg,rgba(255,208,0,.05),rgba(255,69,0,.04));'
)

# ── 17. STORE PRODUCT TAB hover ──────────────────────────────────────────
html = html.replace(
    '.sptab:hover,.sptab.active{border-color:var(--red);background:rgba(124,58,237,.06);}',
    '.sptab:hover,.sptab.active{border-color:var(--red);background:rgba(232,0,29,.06);}'
)

# ── 18. FOOD CARD selected ────────────────────────────────────────────────
html = html.replace(
    '.food-card.selected{border-color:var(--red);background:rgba(124,58,237,0.08);}',
    '.food-card.selected{border-color:var(--red);background:rgba(232,0,29,0.08);}'
)

# ── 19. RADIO / CHECK buttons bg ─────────────────────────────────────────
html = html.replace(
    '.ro:has(input:checked){border-color:var(--red);color:var(--red);background:rgba(124,58,237,.07);}',
    '.ro:has(input:checked){border-color:var(--red);color:var(--red);background:rgba(232,0,29,.07);}'
)
html = html.replace(
    '.split-tab.active{border-color:var(--red);color:var(--red);background:rgba(124,58,237,.07);}',
    '.split-tab.active{border-color:var(--red);color:var(--red);background:rgba(232,0,29,.07);}'
)
html = html.replace(
    '.ptab.active{border-color:var(--red);color:var(--red);background:rgba(124,58,237,.07);}',
    '.ptab.active{border-color:var(--red);color:var(--red);background:rgba(232,0,29,.07);}'
)
html = html.replace(
    '.painbtn.sel{border-color:var(--red);background:rgba(124,58,237,.08);color:var(--red);}',
    '.painbtn.sel{border-color:var(--red);background:rgba(232,0,29,.08);color:var(--red);}'
)
html = html.replace(
    '.qopt.sel{border-color:var(--red);background:rgba(124,58,237,.1);color:var(--red);}',
    '.qopt.sel{border-color:var(--red);background:rgba(232,0,29,.1);color:var(--red);}'
)
html = html.replace(
    '.bfsi.active{border-color:var(--red);color:var(--red);background:rgba(124,58,237,.08);}',
    '.bfsi.active{border-color:var(--red);color:var(--red);background:rgba(232,0,29,.08);}'
)

# ── 20. MWARN background ─────────────────────────────────────────────────
html = html.replace(
    '.mwarn{background:rgba(124,58,237,.08);border:1px solid rgba(124,58,237,.2);',
    '.mwarn{background:rgba(232,0,29,.06);border:1px solid rgba(232,0,29,.15);'
)

# ── 21. PROF-PLAN-BADGE free ──────────────────────────────────────────────
html = html.replace(
    '.prof-plan-badge.free{background:rgba(124,58,237,.12);color:var(--red);}',
    '.prof-plan-badge.free{background:rgba(232,0,29,.12);color:var(--red);}'
)

# ── 22. PBFREE badge ──────────────────────────────────────────────────────
html = html.replace(
    '.pbfree{background:rgba(124,58,237,.1);color:var(--red);border:1px solid rgba(124,58,237,.2);}',
    '.pbfree{background:rgba(232,0,29,.1);color:var(--red);border:1px solid rgba(232,0,29,.2);}'
)

# ── 23. MEAL MAC badges ───────────────────────────────────────────────────
html = html.replace(
    '.mmac.p{background:rgba(124,58,237,.1);color:var(--red);}',
    '.mmac.p{background:rgba(232,0,29,.1);color:var(--red);}'
)

# ── 24. PDF READER PAGE (light bg) ────────────────────────────────────────
html = html.replace(
    '.pdf-reader-page{position:relative;border-radius:8px;overflow:hidden;background:#f0ebff;border:1px solid var(--border);}',
    '.pdf-reader-page{position:relative;border-radius:8px;overflow:hidden;background:#111;border:1px solid var(--border);}'
)

# ── 25. NAV HEIGHT reference in mobile CSS ────────────────────────────────
# Hero padding refs
html = html.replace('min-height:100svh;padding:80px 16px 60px!important;}',
                    'min-height:100svh;padding:72px 16px 60px!important;}')

# ── 26. COMPACT NAV — update hero padding top for shorter nav ─────────────
html = html.replace(
    '.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;overflow:hidden;padding:100px 20px 80px;text-align:center;}',
    '.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;overflow:hidden;padding:88px 20px 72px;text-align:center;}'
)

print("Done. Writing file...")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully.")
