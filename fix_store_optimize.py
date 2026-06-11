#!/usr/bin/env python3
"""
1. Scope white-violet premium theme to #store (PDF) section
2. Full website performance optimizations
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ──────────────────────────────────────────────────────────────────────────────
# PART A — PERFORMANCE OPTIMIZATIONS
# ──────────────────────────────────────────────────────────────────────────────

# 1. Replace Google Fonts link with preconnect + preload pattern
html = html.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@300;400;600;700;900&family=Barlow:wght@300;400;500;600&display=swap" rel="stylesheet">',
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="preload" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@300;400;600;700;900&family=Barlow:wght@300;400;500;600&display=swap" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@300;400;600;700;900&family=Barlow:wght@300;400;500;600&display=swap" rel="stylesheet"></noscript>'
)

# 2. Add preconnect for Firebase + Razorpay CDNs right after charset meta
html = html.replace(
    '<meta charset="UTF-8">',
    '<meta charset="UTF-8">\n<meta name="theme-color" content="#070707">\n<meta name="description" content="Royal Fitness Club — India\'s most advanced gym ecosystem. AI-powered meal plans, body calculators, anabolic guides, and pro coaching.">\n<link rel="dns-prefetch" href="https://www.gstatic.com">\n<link rel="dns-prefetch" href="https://firestore.googleapis.com">\n<link rel="dns-prefetch" href="https://checkout.razorpay.com">'
)

# 3. Add defer to Firebase SDK scripts (non-critical for initial paint)
html = html.replace(
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>',
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js" defer></script>'
)
html = html.replace(
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>',
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js" defer></script>'
)
html = html.replace(
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js"></script>',
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js" defer></script>'
)
html = html.replace(
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-functions-compat.js"></script>',
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-functions-compat.js" defer></script>'
)
html = html.replace(
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-storage-compat.js"></script>',
    '<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-storage-compat.js" defer></script>'
)

# 4. Add defer to RFC service scripts
html = html.replace('<script src="src/auth.js"></script>', '<script src="src/auth.js" defer></script>')
html = html.replace('<script src="src/userService.js"></script>', '<script src="src/userService.js" defer></script>')
html = html.replace('<script src="src/subscriptionService.js"></script>', '<script src="src/subscriptionService.js" defer></script>')
html = html.replace('<script src="src/razorpayService.js"></script>', '<script src="src/razorpayService.js" defer></script>')
html = html.replace('<script src="src/analyticsService.js"></script>', '<script src="src/analyticsService.js" defer></script>')
html = html.replace('<script src="src/transformationService.js"></script>', '<script src="src/transformationService.js" defer></script>')
html = html.replace('<script src="src/communityService.js"></script>', '<script src="src/communityService.js" defer></script>')

# 5. Add content-visibility + will-change hints in CSS (add right before </style>)
perf_css = """
/* ── PERFORMANCE ── */
.hero{contain:layout style;}
section{content-visibility:auto;contain-intrinsic-size:0 500px;}
#home,nav{content-visibility:visible;}
.tcard,.pcard,.mcard,.toolcard,.pdf-review,.lb-row{will-change:transform;}
.hamburger span{will-change:transform,opacity;}
img{loading:lazy;}
"""
html = html.replace('</style>', perf_css + '</style>', 1)

# ──────────────────────────────────────────────────────────────────────────────
# PART B — WHITE/VIOLET THEME FOR #store SECTION
# ──────────────────────────────────────────────────────────────────────────────

# We inject scoped CSS variables + overrides for #store into the <style> block.
store_css = """
/* ══════════════════════════════════════════════════════
   STORE SECTION — WHITE / VIOLET PREMIUM PALETTE
   ══════════════════════════════════════════════════════ */
#store{
  background:linear-gradient(180deg,#f4f0ff 0%,#faf8ff 40%,#f0ebff 100%);
  --sv:#7c3aed;--sv2:#a855f7;--sv3:#6d28d9;
  --sc:#ffffff;--sc2:#f3eeff;--sb:#e2d4f8;--sb2:#d4c1f5;
  --st:#1e1b4b;--sm:#6b7280;
  color:var(--st);
}
#store .stag{color:var(--sv)!important;}
#store .sh{color:#1e1b4b!important;}
#store .ssub{color:var(--sm)!important;}
#store .divider{background:linear-gradient(90deg,transparent,var(--sb),transparent);}

/* Store product tabs */
#store .store-product-tabs{gap:16px;}
#store .sptab{background:#fff;border:2px solid var(--sb);color:var(--st);box-shadow:0 2px 12px rgba(124,58,237,.07);}
#store .sptab:hover,#store .sptab.active{border-color:var(--sv);background:rgba(124,58,237,.05);box-shadow:0 4px 20px rgba(124,58,237,.14);}
#store .sptab-name{color:var(--st);}
#store .sptab-price{color:var(--sv);}
#store .sptab-badge{background:linear-gradient(135deg,var(--sv),var(--sv2));}

/* Stats bar */
#store .pdf-stats-bar{background:#fff;border:1px solid var(--sb);box-shadow:0 2px 12px rgba(124,58,237,.06);}
#store .pdf-stat-num{color:var(--sv);}
#store .pdf-stat-lbl{color:var(--sm);}

/* Hero / book area */
#store .pdf-pages-tag{color:var(--sm);}
#store .pdf-rating-cnt{color:var(--sm);}

/* What's inside */
#store .pdf-what-inside h3{color:var(--sv);}
#store .pdf-chap-list li{color:#374151;}

/* Price box */
#store .pdf-price-box{background:#fff;border:1.5px solid var(--sb);box-shadow:0 4px 20px rgba(124,58,237,.08);}
#store .pdf-orig-price{color:#9ca3af;}
#store .pdf-price{color:var(--sv);}
#store .pdf-discount-tag{background:var(--sv);color:#fff;}
#store .pdf-price-note{color:var(--sm);}
#store .pdf-trust-badge{color:var(--sm);}

/* Buy button — violet gradient */
#store .pdf-buy-btn{
  background:linear-gradient(135deg,var(--sv),var(--sv2))!important;
  box-shadow:0 4px 20px rgba(124,58,237,.35)!important;
  color:#fff!important;
}
#store .pdf-buy-btn:hover{opacity:.9;transform:translateY(-1px);}
#store .pdf-download-btn{background:linear-gradient(135deg,#22c55e,#16a34a);}

/* Reviews section */
#store .pdf-reviews-section h3{color:var(--sv);}
#store .pdf-review{background:#fff;border:1px solid var(--sb);box-shadow:0 2px 8px rgba(124,58,237,.05);}
#store .pdf-rev-name2{color:var(--st);}
#store .pdf-rev-date{color:var(--sm);}
#store .pdf-rev-text{color:#4b5563;}
#store .pdf-review-avatar{background:linear-gradient(135deg,var(--sv),var(--sv2))!important;}

/* FAQ */
#store .pdf-faq-section h3{color:var(--sv);}
#store .faq-item{background:#fff;border:1px solid var(--sb);}
#store .faq-q{color:var(--st);}
#store .faq-a p{color:#6b7280;}
#store .faq-q::after{color:var(--sv);}

/* Bonus section */
#store .pdf-bonus-section{
  background:linear-gradient(135deg,rgba(124,58,237,.06),rgba(168,85,247,.04));
  border:1px solid rgba(124,58,237,.2);
}
#store .pdf-bonus-tag{background:linear-gradient(135deg,var(--sv),var(--sv2));}
#store .pdf-bonus-name{color:var(--sv)!important;}
#store .pdf-bonus-desc{color:#6b7280;}
#store .sh{color:#1e1b4b!important;}

/* For/not-for */
#store .pdf-for-box{background:#fff;border:1px solid var(--sb);box-shadow:0 2px 8px rgba(124,58,237,.05);}
#store .pdf-for-li{color:#4b5563;}

/* Guarantee */
#store .pdf-guarantee-box{background:#fff;border:2px solid rgba(34,197,94,.3);box-shadow:0 4px 16px rgba(34,197,94,.08);}
#store .pdf-guarantee-text h4{color:#16a34a;}
#store .pdf-guarantee-text p{color:#6b7280;}

/* Final CTA */
#store .pdf-final-cta{
  background:linear-gradient(135deg,#f0ebff,#e8e0f7)!important;
  border:1.5px solid rgba(124,58,237,.2)!important;
}
#store .pdf-final-cta .stag{color:var(--sv)!important;}
#store .pdf-final-cta .sh{color:#1e1b4b!important;}
#store .pdf-final-cta p{color:#6b7280!important;}
#store .pdf-final-cta .pdf-buy-btn{
  background:linear-gradient(135deg,var(--sv3),var(--sv))!important;
  box-shadow:0 6px 24px rgba(109,40,217,.35)!important;
}

/* Reader section */
#store .pdf-reader-section h3{color:var(--sv);}
#store .pdf-reader-desc{color:var(--sm);}
#store .pdf-reader-page{background:#f0ebff;border-color:var(--sb);}
#store .fm-reader-cta p{color:var(--sm);}

/* Store separator */
#store .store-section-sep{border-top-color:var(--sb);}

/* Sticky bar */
#pdf-sticky-bar{background:rgba(124,58,237,.97);border-top:2px solid rgba(124,58,237,.5);}
#pdf-sticky-bar .pdf-buy-btn{background:#fff!important;color:var(--sv)!important;box-shadow:none!important;}

/* Sub-section stags & sh inside store */
#store [class="stag"]{color:var(--sv)!important;}

/* Anabolic book keeps its red cover — no override */
/* FM book keeps blue cover — no override */

/* Mobile */
@media(max-width:768px){
  #store .store-product-tabs{flex-direction:column;align-items:center;}
  #store .sptab{width:100%;max-width:360px;}
  #store .pdf-hero{gap:20px;}
  #store .pdf-for-section{grid-template-columns:1fr;}
  #store .pdf-bonus-list{grid-template-columns:1fr;}
  #store .pdf-reviews-grid{grid-template-columns:1fr;}
}
"""

# Inject store CSS before </style>
html = html.replace('</style>', store_css + '\n</style>', 1)

# ──────────────────────────────────────────────────────────────────────────────
# PART C — Add loading="lazy" to any img tags that don't already have it
# ──────────────────────────────────────────────────────────────────────────────
import re

def add_lazy(m):
    tag = m.group(0)
    if 'loading=' in tag:
        return tag
    return tag.replace('<img ', '<img loading="lazy" ')

html = re.sub(r'<img\s', add_lazy, html)

# ──────────────────────────────────────────────────────────────────────────────
# PART D — Anabolic Final CTA price color: keep gold (not blue)
# Already fine — uses var(--gold) in HTML
# ──────────────────────────────────────────────────────────────────────────────

print("Writing file...")
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done.")
