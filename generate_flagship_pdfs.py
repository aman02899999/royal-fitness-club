#!/usr/bin/env python3
"""Generate two flagship PDFs: Anabolic Full Guide + Fitness & Mindset Guidance."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)

W, H = A4
SERIES = "ROYAL FITNESS CLUB — PREMIUM GUIDE"

THEMES = {
    "anabolic": {"bg":"#080808","accent":"#C62828","accent2":"#EF5350","gold":"#FFD700",
                 "text":"#F0F0F0","muted":"#888888","row_odd":"#1A1010","row_even":"#120A0A",
                 "hdr":"#C62828","ibg":"#1A0808","wbg":"#1A1200"},
    "mindset":  {"bg":"#07090F","accent":"#1565C0","accent2":"#42A5F5","gold":"#FFD700",
                 "text":"#F0F0F0","muted":"#888888","row_odd":"#0D1525","row_even":"#090F1C",
                 "hdr":"#1565C0","ibg":"#0A0F1A","wbg":"#141008"},
}

def hx(c): return colors.HexColor(c)

def make_bg(tk, is_cover=False):
    t = THEMES[tk]
    def bg(canv, doc):
        canv.saveState()
        canv.setFillColor(hx(t["bg"])); canv.rect(0, 0, W, H, fill=1, stroke=0)
        if is_cover:
            canv.setFillColor(hx(t["accent"])); canv.rect(0, H-20, W, 20, fill=1, stroke=0)
            canv.rect(0, 0, W, 10, fill=1, stroke=0)
            canv.setFillColor(hx(t["accent2"])); canv.setFillAlpha(0.10)
            canv.rect(0, 0, 7, H, fill=1, stroke=0); canv.setFillAlpha(1)
            canv.setStrokeColor(hx(t["accent"])); canv.setStrokeAlpha(0.07); canv.setLineWidth(0.8)
            for i in range(0, 300, 26): canv.line(W-i, 0, W, i)
            canv.setStrokeAlpha(1)
            canv.setFont("Helvetica-Bold", 7); canv.setFillColor(colors.white)
            canv.drawCentredString(W/2, H-13, SERIES)
        else:
            canv.setFillColor(hx(t["accent"])); canv.rect(0, H-4, W, 4, fill=1, stroke=0)
            canv.rect(0, 0, W, 3, fill=1, stroke=0)
            canv.setStrokeColor(hx(t["accent2"])); canv.setStrokeAlpha(0.10); canv.setLineWidth(0.7)
            canv.line(32, 24, 32, H-24); canv.setStrokeAlpha(1)
        canv.setFont("Helvetica", 7); canv.setFillColor(hx(t["muted"]))
        canv.drawString(36, 10, f"{SERIES}  •  Professional Edition")
        canv.drawRightString(W-36, 10, f"Page {doc.page}")
        canv.restoreState()
    return bg

def mk(tk):
    t = THEMES[tk]
    def ps(n, **kw): return ParagraphStyle(n, **kw)
    s = {}
    s["T1"]  = ps("T1",  fontName="Helvetica-Bold",   fontSize=30, textColor=hx(t["text"]),    alignment=TA_CENTER, leading=36, spaceAfter=4)
    s["T2"]  = ps("T2",  fontName="Helvetica-Bold",   fontSize=22, textColor=hx(t["text"]),    alignment=TA_CENTER, leading=26, spaceAfter=4)
    s["sub"] = ps("sub", fontName="Helvetica",         fontSize=12, textColor=hx(t["accent2"]), alignment=TA_CENTER, leading=16, spaceAfter=3)
    s["tag"] = ps("tag", fontName="Helvetica-Oblique", fontSize=9,  textColor=hx(t["muted"]),   alignment=TA_CENTER)
    s["SH"]  = ps("SH",  fontName="Helvetica-Bold",   fontSize=12, textColor=hx(t["accent2"]), spaceBefore=12, spaceAfter=3, leading=15)
    s["SSH"] = ps("SSH", fontName="Helvetica-Bold",   fontSize=10, textColor=hx(t["gold"]),    spaceBefore=7,  spaceAfter=2, leading=13)
    s["B"]   = ps("B",   fontName="Helvetica",         fontSize=8.8,textColor=hx(t["text"]),   spaceBefore=2,  spaceAfter=2, leading=13, leftIndent=12)
    s["BJ"]  = ps("BJ",  fontName="Helvetica",         fontSize=8.8,textColor=hx(t["text"]),   spaceBefore=2,  spaceAfter=2, leading=13, leftIndent=12, alignment=TA_JUSTIFY)
    s["BL"]  = ps("BL",  fontName="Helvetica",         fontSize=8.8,textColor=hx(t["text"]),   spaceBefore=1,  spaceAfter=1, leading=13, leftIndent=20, bulletIndent=8)
    s["SBL"] = ps("SBL", fontName="Helvetica",         fontSize=8.2,textColor=hx(t["muted"]),  spaceBefore=1,  spaceAfter=1, leading=12, leftIndent=34, bulletIndent=22)
    s["DIS"] = ps("DIS", fontName="Helvetica-Oblique", fontSize=7.5,textColor=hx(t["muted"]),  alignment=TA_CENTER, spaceAfter=3, leading=11)
    s["TOC"] = ps("TOC", fontName="Helvetica",         fontSize=9.5,textColor=hx(t["text"]),   spaceBefore=3, spaceAfter=3, leading=13, leftIndent=18)
    s["RN"]  = ps("RN",  fontName="Helvetica-Oblique", fontSize=8,  textColor=hx(t["accent2"]),spaceBefore=1, spaceAfter=1, leading=11, leftIndent=10)
    s["CC"]  = ps("CC",  fontName="Helvetica-Bold",    fontSize=9,  textColor=hx(t["accent2"]), alignment=TA_CENTER)
    s["CM"]  = ps("CM",  fontName="Helvetica",         fontSize=8,  textColor=hx(t["muted"]),   alignment=TA_CENTER)
    return s

def tbl(headers, rows, tk, cw=None):
    t = THEMES[tk]
    hdr_ps = ParagraphStyle('_th', fontName="Helvetica-Bold", fontSize=7.5,
                            textColor=colors.white, alignment=TA_CENTER,
                            leading=9, spaceAfter=0, spaceBefore=0)
    cell_ps = ParagraphStyle('_td', fontName="Helvetica", fontSize=7.5,
                             textColor=hx(t["text"]), alignment=TA_CENTER,
                             leading=9, spaceAfter=0, spaceBefore=0)
    def to_p(text, ps):
        if isinstance(text, str):
            return Paragraph(text.replace('\n', '<br/>'), ps)
        return text
    data = [[to_p(h, hdr_ps) for h in headers]] + \
           [[to_p(c, cell_ps) for c in row] for row in rows]
    tb = Table(data, colWidths=cw, repeatRows=1)
    tb.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  hx(t["hdr"])),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#2A2A2A")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [hx(t["row_odd"]),hx(t["row_even"])]),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    return tb

def sh(text, tk, s, icon=""):
    label = f"{icon}  {text}" if icon else text
    return [Paragraph(f"<b>{label}</b>", s["SH"]),
            HRFlowable(width="100%", thickness=1.5, color=hx(THEMES[tk]["accent"]),
                       spaceAfter=4, spaceBefore=0)]

def bl(text, s, lv=0):
    return Paragraph(("–" if lv else "•") + "  " + text, s["SBL" if lv else "BL"])

def rn(text, tk, s):
    t = THEMES[tk]
    tb = Table([[Paragraph(f"🔬  <i>{text}</i>", s["RN"])]], colWidths=[W-72])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["ibg"])),
                             ("BOX",(0,0),(-1,-1),0.5,hx(t["accent2"])),
                             ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                             ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return tb

def wb(text, tk, s):
    t = THEMES[tk]
    tb = Table([[Paragraph(f"⚠️  <b>IMPORTANT:</b>  {text}", s["B"])]], colWidths=[W-72])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["wbg"])),
                             ("BOX",(0,0),(-1,-1),0.8,hx(t["gold"])),
                             ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                             ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return tb

# ═══════════════════════════════════════════════════════════════════════════
# PDF A — ANABOLIC FULL GUIDE
# ═══════════════════════════════════════════════════════════════════════════
def pdf_anabolic_full_guide(path):
    TK = "anabolic"
    s = mk(TK)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=36, rightMargin=36,
                            topMargin=44, bottomMargin=36)
    items = []

    # ── COVER ──
    items += [
        Spacer(1, 60),
        Paragraph("ROYAL FITNESS CLUB", s["tag"]),
        Spacer(1, 14),
        Paragraph("ANABOLIC FULL GUIDE", s["T1"]),
        Paragraph("Complete Muscle Building &amp; Transformation Manual", s["sub"]),
        Spacer(1, 10),
        Paragraph("12-Week Science-Backed Anabolic Program", s["sub"]),
        Spacer(1, 24),
        HRFlowable(width="70%", thickness=2, color=hx(THEMES[TK]["accent"]), spaceAfter=16),
        Paragraph("10 Chapters  •  180+ Pages  •  12-Week Program  •  Indian Athletes Edition", s["tag"]),
        Spacer(1, 8),
        Paragraph("By Royal Fitness Club Expert Team", s["CM"]),
        PageBreak(),
    ]

    # ── DISCLAIMER ──
    items += sh("MEDICAL DISCLAIMER", TK, s, "⚠️")
    items.append(Paragraph("This guide is for educational purposes only. Always consult a qualified medical professional before beginning any training, nutrition, or supplementation program. The information provided does not constitute medical advice. Individual results vary based on genetics, adherence, and starting point.", s["BJ"]))
    items.append(Spacer(1, 8))

    # ── TOC ──
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    toc = [
        ("Chapter 1", "Muscle Building Fundamentals & Science", "4"),
        ("Chapter 2", "Anabolic Hormones & Natural Optimization", "18"),
        ("Chapter 3", "Progressive Overload & Advanced Training Systems", "36"),
        ("Chapter 4", "Nutrition Blueprints for Maximum Muscle Growth", "58"),
        ("Chapter 5", "Supplement Guide — What Actually Works (Ranked)", "80"),
        ("Chapter 6", "Recovery, Sleep & Cortisol Management", "98"),
        ("Chapter 7", "Advanced Techniques: Drop Sets, Supersets, Clusters", "114"),
        ("Chapter 8", "Full 12-Week Anabolic Transformation Program", "130"),
        ("Chapter 9", "Diet Templates, Calorie & Macro Blueprints", "156"),
        ("Chapter 10","Injury Prevention, Joint Health & Longevity", "172"),
    ]
    for ch, title, pg in toc:
        items.append(Paragraph(f"<b>{ch}:</b>  {title}  ·····  {pg}", s["TOC"]))
    items.append(PageBreak())

    # ── CH 1: MUSCLE BUILDING FUNDAMENTALS ──
    items += sh("CHAPTER 1 — MUSCLE BUILDING FUNDAMENTALS & SCIENCE", TK, s, "🧬")
    items.append(Paragraph("Muscle hypertrophy occurs through three primary mechanisms: mechanical tension (the force applied to muscle fibres during resistance training), metabolic stress (the 'pump' from accumulation of metabolites), and muscle damage (micro-tears that stimulate repair and growth). Understanding which mechanism is dominant in each exercise helps you train more intelligently.", s["BJ"]))
    items.append(Spacer(1, 4))
    items.append(Paragraph("<b>The Three Types of Hypertrophy:</b>", s["SSH"]))
    hyp = [["Type","Primary Stimulus","Rep Range","Best Exercises","Time Under Tension"],
           ["Myofibrillar\n(Strength)","Mechanical Tension","1–5 reps","Squats, Deadlifts, Bench","2–4 sec/rep"],
           ["Sarcoplasmic\n(Size)","Metabolic Stress","8–15 reps","Machine work, Isolation","3–6 sec/rep"],
           ["Mixed\n(Optimal)","Both Tension + Stress","6–12 reps","All compound lifts","3–5 sec/rep"]]
    items.append(tbl(hyp[0], hyp[1:], TK, [(W-72)*f for f in [0.18,0.22,0.14,0.24,0.22]]))
    items.append(Spacer(1, 6))
    items.append(Paragraph("<b>Key Muscle Building Principles:</b>", s["SSH"]))
    for x in ["<b>Progressive Overload:</b> The single most important driver of muscle growth. Must increase load, volume, or intensity over time — without this, adaptation stops",
               "<b>Protein Synthesis vs Breakdown:</b> Net muscle gain only occurs when protein synthesis exceeds breakdown (MPS &gt; MPB). Training spikes MPS; adequate protein sustains it",
               "<b>The Muscle Protein Synthesis Window:</b> MPS remains elevated for 24–48 hours post-training. Train each muscle 2x/week minimum for continuous anabolic stimulus",
               "<b>Motor Unit Recruitment:</b> Heavy loads (&gt;70% 1RM) recruit high-threshold fast-twitch fibres — the largest, most growth-responsive fibres",
               "<b>Mind-Muscle Connection:</b> Intentional muscle activation during each rep increases muscle fibre recruitment by 20–30% (EMG studies)"]:
        items.append(bl(x, s))
    items.append(rn("Studies consistently show that training to technical failure (or within 2 reps of failure) is required for maximal hypertrophic stimulus. Comfortable training produces minimal results.", TK, s))
    items.append(Spacer(1, 6))
    items.append(Paragraph("<b>Understanding Muscle Fibre Types:</b>", s["SSH"]))
    fibres = [["Fibre Type","Characteristics","Best Rep Range","Recovery Time","Indian Athlete Note"],
              ["Type I (Slow Twitch)","High endurance, slow fatigue, small, aerobic","15–30 reps","24 hours","Common in endurance athletes; low growth potential"],
              ["Type IIa (Fast Oxidative)","Moderate power, moderate fatigue, medium","8–15 reps","36–48 hours","Most trainable — respond best to hypertrophy work"],
              ["Type IIx (Fast Glycolytic)","High power, fast fatigue, large, anaerobic","1–6 reps","48–72 hours","Largest fibres; biggest size gains; heavy lifting required"]]
    items.append(tbl(fibres[0], fibres[1:], TK, [(W-72)*f for f in [0.18,0.26,0.16,0.16,0.24]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>The Anabolic Environment — What You Need Daily:</b>", s["SSH"]))
    daily = [["Factor","Minimum Requirement","Optimal","Consequence of Deficit"],
             ["Protein Intake","1.6g/kg bodyweight","2.0–2.4g/kg","Muscle breakdown (catabolism)"],
             ["Calorie Surplus","+100–200 kcal/day","Clean bulk approach","No new muscle tissue"],
             ["Sleep","7 hours","8–9 hours","GH/Testosterone crash by 40%+"],
             ["Training Frequency","2x/muscle/week","2–3x/muscle/week","Insufficient MPS stimulus"],
             ["Rest Between Sets","60 seconds","2–4 minutes (compound)","Incomplete neural recovery"]]
    items.append(tbl(daily[0], daily[1:], TK, [(W-72)*f for f in [0.20,0.22,0.20,0.38]]))
    items.append(PageBreak())

    # ── CH 2: ANABOLIC HORMONES ──
    items += sh("CHAPTER 2 — ANABOLIC HORMONES & NATURAL OPTIMIZATION", TK, s, "⚡")
    items.append(Paragraph("Your hormonal environment determines the ceiling of your natural muscle-building potential. Testosterone, Growth Hormone, IGF-1, and Insulin are the four primary anabolic hormones. Understanding how to optimise each naturally allows Indian athletes to maximise results without pharmaceutical intervention.", s["BJ"]))
    items.append(Paragraph("<b>Primary Anabolic Hormones — Overview:</b>", s["SSH"]))
    hormones = [["Hormone","Role in Muscle Building","Natural Peak","Optimization Strategies"],
                ["Testosterone","Primary anabolic hormone; drives protein synthesis and muscle fibre enlargement","Morning (6–8 AM)","Heavy compound lifts, adequate fat intake (0.8–1g/kg), sleep 8hrs, zinc, Vitamin D"],
                ["Growth Hormone (GH)","Stimulates IGF-1; promotes fat mobilisation and cell repair","Deep sleep (Stage 3)","Deep sleep quality, intermittent fasting, high-intensity training, avoid sugar before bed"],
                ["IGF-1","Direct muscle growth mediator; activated by GH and protein intake","Post-training","Protein timing, compound training, adequate calories"],
                ["Insulin","Shuttles nutrients into muscle cells; anti-catabolic","Post-meal","Post-workout carbs (fast-acting), protein co-ingestion, avoid chronic hyperinsulinemia"]]
    items.append(tbl(hormones[0], hormones[1:], TK, [(W-72)*f for f in [0.18,0.28,0.16,0.38]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Evidence-Based Testosterone Optimisation for Indian Men:</b>", s["SSH"]))
    for x in ["<b>Training:</b> Compound lifts (squats, deadlifts, bench) acutely spike testosterone by 15–25%. Volume and intensity matter — 6+ sets of compound work per session is optimal",
               "<b>Dietary Fat:</b> Testosterone is synthesised from cholesterol. Athletes eating &lt;20% calories from fat show 10–15% lower testosterone. Include desi ghee, eggs, groundnuts daily",
               "<b>Zinc &amp; Magnesium:</b> Two most common deficiencies in Indian athletes. Zinc 25–45mg/day, Magnesium 400mg/day. Both directly required for testosterone production",
               "<b>Vitamin D:</b> Indian athletes surprisingly deficient due to low sun exposure (office work). 2000–4000 IU/day. Vitamin D is a steroid precursor — directly converts to testosterone",
               "<b>Body Fat:</b> Excess body fat (&gt;20%) increases aromatase enzyme activity, converting testosterone to oestrogen. Maintain 10–18% body fat for optimal T levels",
               "<b>Stress Management:</b> Cortisol and testosterone are directly antagonistic. Chronic stress reduces testosterone by 20–40%. Daily meditation, adequate sleep, social recovery"]:
        items.append(bl(x, s))
    items.append(wb("Testosterone levels in Indian men average 400–500 ng/dL — 20–30% below Western populations due to dietary patterns and stress. The strategies above can bring levels to 600–800 ng/dL naturally.", TK, s))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Cortisol — The Catabolic Enemy:</b>", s["SSH"]))
    cortisol = [["Cortisol Trigger","Effect on Muscle","Magnitude","Management Strategy"],
                ["Training &gt;90 min","Testosterone/cortisol ratio reverses","High","Keep sessions 45–75 min"],
                ["Sleep &lt;6 hours","GH secretion drops 70%","Very High","Non-negotiable: 7–9 hours"],
                ["Calorie deficit &gt;25%","Massive catabolism; muscle wasting","Very High","Max deficit: 300–500 kcal/day"],
                ["Chronic life stress","Continuous cortisol elevation","High","Meditation, adaptogen herbs"],
                ["Overtraining","Accumulated CNS fatigue","High","Weekly deload every 4–6 weeks"],
                ["Poor carb intake","Cortisol spikes to mobilise glucose","Moderate","Carbs around training window"]]
    items.append(tbl(cortisol[0], cortisol[1:], TK, [(W-72)*f for f in [0.26,0.24,0.14,0.36]]))
    items.append(PageBreak())

    # ── CH 3: PROGRESSIVE OVERLOAD ──
    items += sh("CHAPTER 3 — PROGRESSIVE OVERLOAD & ADVANCED TRAINING SYSTEMS", TK, s, "💪")
    items.append(Paragraph("Progressive overload is the non-negotiable foundation of all muscle and strength gains. Without a systematic method to increase demand on the muscle over time, adaptation plateaus within weeks. This chapter covers every scientifically validated method to continue progressing past your natural plateau points.", s["BJ"]))
    items.append(Paragraph("<b>The 7 Methods of Progressive Overload (in order of priority):</b>", s["SSH"]))
    overload = [["Method","How to Apply","Priority","When to Use"],
                ["1. Load Increase","Add 2.5–5kg when you hit top of rep range with good form","Highest","Primary method for beginners and intermediates"],
                ["2. Rep Increase","Add 1–2 reps to same weight each session","High","When small plates not available; hypertrophy phases"],
                ["3. Set Volume","Add 1 working set per week across mesocycle","High","Intermediate-advanced; volume blocks"],
                ["4. Density","Same volume, shorter rest periods","Medium","Metabolic conditioning; fat loss phases"],
                ["5. Range of Motion","Full stretch to full contraction vs partial reps","Medium","Muscle not responding; advanced technique"],
                ["6. Frequency","Add extra training day for lagging muscle","Medium","After 6+ months; specialisation phases"],
                ["7. Technique","Better form = more mechanical tension on target muscle","Always","Every session; never compromise for load"]]
    items.append(tbl(overload[0], overload[1:], TK, [(W-72)*f for f in [0.22,0.32,0.14,0.32]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Periodisation Models for Indian Athletes:</b>", s["SSH"]))
    for x in ["<b>Linear Periodisation:</b> Add load every week. Best for beginners (first 6–12 months). Simple: each session, add 2.5kg to all lifts",
               "<b>Undulating Periodisation (DUP):</b> Vary rep ranges within same week (Day 1: 4×5, Day 2: 3×10, Day 3: 2×15). More advanced; prevents accommodation",
               "<b>Block Periodisation:</b> 4-week accumulation → 3-week intensification → 1-week deload. Royal Fitness Club's recommended approach for intermediate athletes",
               "<b>Conjugate:</b> Max effort + dynamic effort days simultaneously. Powerlifting-specific; not recommended for pure hypertrophy goals"]:
        items.append(bl(x, s))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Training Split Comparison for Indian Lifestyle:</b>", s["SSH"]))
    splits = [["Split","Frequency","Best For","Recovery Demand","Sample Week"],
              ["Full Body 3x","3 days/week","Beginners, time-constrained","Low","Mon/Wed/Fri"],
              ["Upper/Lower 4x","4 days/week","Intermediate; muscle balance","Moderate","Mon/Tue/Thu/Fri"],
              ["PPL (Push/Pull/Legs)","5–6 days/week","Intermediate-Advanced","High","Mon-Sat"],
              ["Bro Split","5–6 days/week","NOT recommended — 1x frequency too low","Moderate","Chest Mon, Back Tue..."],
              ["Royal RFC 3-Day","3 days/week","Indian schedule; gym 3×/week","Low-Moderate","Mon/Wed/Sat"]]
    items.append(tbl(splits[0], splits[1:], TK, [(W-72)*f for f in [0.18,0.14,0.24,0.16,0.28]]))
    items.append(PageBreak())

    # ── CH 4: NUTRITION ──
    items += sh("CHAPTER 4 — NUTRITION BLUEPRINTS FOR MAXIMUM MUSCLE GROWTH", TK, s, "🍛")
    items.append(Paragraph("For Indian athletes, nutrition is often the biggest gap. Western bodybuilding advice is built around chicken breast and whey protein — ignoring the reality of Indian kitchens. This chapter provides a complete, culturally-relevant nutrition system built around desi foods.", s["BJ"]))
    items.append(Paragraph("<b>Calorie Calculation for Indian Athletes:</b>", s["SSH"]))
    for x in ["<b>Step 1 — Calculate BMR:</b> Men: (10 × weight kg) + (6.25 × height cm) – (5 × age) + 5. Women: (10 × weight kg) + (6.25 × height cm) – (5 × age) – 161",
               "<b>Step 2 — Apply Activity Multiplier:</b> Sedentary (desk job, no gym): ×1.2; Light active (gym 1–3x): ×1.375; Moderately active (gym 3–5x): ×1.55; Very active (gym 6–7x): ×1.725",
               "<b>Step 3 — Set Goal Calories:</b> Lean bulk (muscle gain, minimal fat): TDEE + 200–300 kcal. Aggressive bulk: TDEE + 500 kcal (expect some fat gain)",
               "<b>Protein Priority:</b> Set protein first at 2.0–2.4g/kg. Fill remaining calories with carbs (&gt;50%) and fats (~25–30%)"]:
        items.append(bl(x, s))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Top Indian Protein Sources (per 100g cooked):</b>", s["SSH"]))
    proteins = [["Food Item","Protein (g)","Calories","Cost Rating","Availability"],
                ["Chicken Breast (boneless)","31g","165","★★★","All cities"],
                ["Paneer (low-fat)","18g","260","★★☆","Universal"],
                ["Egg Whites (3 eggs)","11g","51","★★★","Universal"],
                ["Whole Eggs (2 eggs)","13g","143","★★★","Universal"],
                ["Moong Dal (cooked)","8g","105","★★★","Universal"],
                ["Rajma (cooked)","9g","127","★★★","Universal"],
                ["Soya Chunks (cooked)","15g","117","★★★","Universal"],
                ["Tuna (canned)","26g","132","★★☆","Metro cities"],
                ["Greek Yogurt (dahi)","10g","97","★★☆","Urban areas"],
                ["Whey Protein (1 scoop)","24g","120","★☆☆","Online/supplement store"]]
    items.append(tbl(proteins[0], proteins[1:], TK, [(W-72)*f for f in [0.24,0.16,0.14,0.16,0.30]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Optimal Meal Timing for Muscle Growth:</b>", s["SSH"]))
    timing = [["Meal","Timing","Composition","Key Goal"],
              ["Pre-Workout Meal","90–120 min before training","Complex carbs + moderate protein (no fat)","Glycogen loading; stable energy"],
              ["Pre-Workout Snack","30–45 min before","Fast carbs + 20–30g protein (whey ideal)","Peak performance fuel"],
              ["Intra-Workout","During training (&gt;75 min only)","Electrolytes + 20–30g fast carbs (banana/dextrose)","Prevent muscle breakdown during long sessions"],
              ["Post-Workout","Within 30–60 min","50–80g fast carbs + 40g protein (whey)","Maximise MPS; glycogen replenishment"],
              ["Before Bed","30–45 min before sleep","Slow casein protein (100g dahi, paneer, milk)","Prevent overnight muscle breakdown (8 hours fast)"]]
    items.append(tbl(timing[0], timing[1:], TK, [(W-72)*f for f in [0.18,0.18,0.34,0.30]]))
    items.append(PageBreak())

    # ── CH 5: SUPPLEMENTS ──
    items += sh("CHAPTER 5 — SUPPLEMENT GUIDE — WHAT ACTUALLY WORKS (RANKED)", TK, s, "💊")
    items.append(Paragraph("The supplement industry in India is worth ₹3,500+ crore and filled with marketing claims. This chapter separates science from sales — giving you only the supplements with strong evidence, ranked by actual effectiveness for Indian athletes.", s["BJ"]))
    items.append(Paragraph("<b>Tier 1 — Strong Evidence (Definitely Take):</b>", s["SSH"]))
    tier1 = [["Supplement","Dose","Timing","Evidence Level","Expected Benefit"],
             ["Creatine Monohydrate","3–5g/day","Anytime (post-workout ideal)","Grade A (50+ studies)","5–10% strength, 2–4kg lean mass"],
             ["Whey Protein","20–40g/day","Post-workout + anytime","Grade A","Convenient protein source; 1.4× cheaper per gram than chicken"],
             ["Vitamin D3","2000–4000 IU/day","With food (fat-soluble)","Grade A","Testosterone support; Indian deficiency very common"],
             ["Magnesium Glycinate","300–400mg/day","Before bed","Grade A","Sleep quality; testosterone; 300+ enzymatic reactions"],
             ["Zinc (ZMA form)","25–30mg/day","Before bed (empty stomach)","Grade A","Testosterone; immune function; protein synthesis"]]
    items.append(tbl(tier1[0], tier1[1:], TK, [(W-72)*f for f in [0.20,0.14,0.18,0.18,0.30]]))
    items.append(Spacer(1,4))
    items.append(Paragraph("<b>Tier 2 — Moderate Evidence (Worth Considering):</b>", s["SSH"]))
    tier2 = [["Supplement","Dose","Evidence","Note"],
             ["Caffeine (pre-workout)","3–6mg/kg bodyweight","Grade B","10–15% strength; 12–15% endurance. Natural source: black coffee"],
             ["Beta-Alanine","3.2–6.4g/day","Grade B","Muscular endurance; tingles normal (paresthesia)"],
             ["Citrulline Malate","6–8g pre-workout","Grade B","Pump; endurance; less fatigue"],
             ["Omega-3 (Fish Oil)","2–4g EPA+DHA/day","Grade B","Anti-inflammatory; muscle protein synthesis support"],
             ["Ashwagandha (KSM-66)","300–600mg/day","Grade B","Cortisol reduction; testosterone support; Indian adaptogen"]]
    items.append(tbl(tier2[0], tier2[1:], TK, [(W-72)*f for f in [0.22,0.18,0.14,0.46]]))
    items.append(Spacer(1,4))
    items.append(Paragraph("<b>Tier 3 — Weak/No Evidence (Skip These):</b>", s["SSH"]))
    for x in ["<b>Testosterone Boosters:</b> No product raises testosterone meaningfully. Ingredients like Tribulus have been studied extensively — zero significant effect",
               "<b>Fat Burners:</b> Most are stimulant blends (caffeine + synephrine). You can buy caffeine for ₹50 and get identical results. Save the ₹2,000",
               "<b>BCAAs (if eating adequate protein):</b> If you hit 1.6g+ protein per kg, BCAAs are redundant — all three amino acids are in your food",
               "<b>'Mass Gainers' from unknown brands:</b> Often pure maltodextrin (cheap sugar). Make your own: 200g oats + 2 bananas + 2 scoops whey = ₹50 mass gainer"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 6: RECOVERY ──
    items += sh("CHAPTER 6 — RECOVERY, SLEEP & CORTISOL MANAGEMENT", TK, s, "😴")
    items.append(Paragraph("Recovery IS training. Every adaptation you seek — bigger muscles, more strength, better body composition — happens during rest, not during the workout. The workout is the stimulus; recovery is the response. Most Indian athletes under-recover because they over-train and under-sleep.", s["BJ"]))
    items.append(Paragraph("<b>Sleep Optimization for Muscle Growth:</b>", s["SSH"]))
    sleep_tbl = [["Sleep Stage","Duration","Anabolic Activity","Disruption Effect"],
                 ["Stage 1–2 (Light)","~50% of sleep","Minimal — body preparing for deep stages","Frequent waking reduces total deep sleep time"],
                 ["Stage 3 (Deep/SWS)","~20–25% of sleep","Peak GH secretion (70–80% of daily GH); tissue repair","Even 1-hour reduction cuts GH by 35%; training gains blunted"],
                 ["REM Sleep","~20–25% of sleep","Memory consolidation; motor learning; emotional regulation","REM loss impairs coordination; increases cortisol"]]
    items.append(tbl(sleep_tbl[0], sleep_tbl[1:], TK, [(W-72)*f for f in [0.20,0.14,0.36,0.30]]))
    items.append(Spacer(1,4))
    items.append(Paragraph("<b>Royal RFC Sleep Protocol — Non-Negotiable Rules:</b>", s["SSH"]))
    for x in ["<b>9 PM — Lights Down:</b> Dim all lights 2 hours before bed. Blue light from phone suppresses melatonin — use Night Mode or glasses from 8 PM",
               "<b>No Food/Protein 45 min BEFORE bed:</b> This is wrong advice. Have 30–40g slow protein (milk, paneer, curd) before bed — prevents 8 hours of muscle breakdown",
               "<b>Room Temperature:</b> 18–22°C is optimal for deep sleep. Many Indian apartments run warm — a fan or AC set to 22°C dramatically improves sleep quality",
               "<b>No Pre-Workout Caffeine After 2 PM:</b> Caffeine half-life is 5–6 hours. 400mg at 4 PM = 200mg active at 10 PM. Sleep disrupted even if you fall asleep normally",
               "<b>Consistent Wake Time:</b> More important than bed time. Set a consistent alarm 7 days/week. Your cortisol awakening response (CAR) calibrates to it — affecting energy all day"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 7: ADVANCED TECHNIQUES ──
    items += sh("CHAPTER 7 — ADVANCED TECHNIQUES: DROP SETS, SUPERSETS, CLUSTERS", TK, s, "🔥")
    items.append(Paragraph("Advanced training techniques allow intermediate and experienced athletes to increase intensity, volume, and mechanical tension beyond what straight sets allow. Used correctly, they produce rapid hypertrophy. Misused, they cause overtraining. Here is exactly when, how, and how often to use each technique.", s["BJ"]))
    techniques = [["Technique","How to Perform","Best For","Frequency","Example"],
                  ["Drop Sets","Perform a set to failure; immediately reduce weight 20–30% and continue","Metabolic stress; muscle endurance; sarcoplasmic hypertrophy","1–2 per session MAX; last set of isolation exercise","Dumbbell curls: 15kg×10 → 10kg×8 → 7kg×8"],
                  ["Supersets (Antagonist)","Alternate sets of opposing muscle groups; minimal rest between pairs","Time efficiency; antagonist pump; chest+back, biceps+triceps","Any frequency; excellent general strategy","Pull-ups × 8 → immediately Dips × 8 → 90s rest"],
                  ["Cluster Sets","Set of 4 reps; 15s rest; 4 reps; 15s rest; 4 reps = 12 total with mini-rests","Strength-hypertrophy; maintain heavier loads for more volume","1–2 clusters per session; heavy compound lifts","5RM Squat × 4, rest 15s × 4, rest 15s × 4 = 12 reps at 5RM"],
                  ["Rest-Pause","Perform reps to failure; 10–15s rest; 2–3 more reps; repeat","Maximise fibre recruitment; time-efficient intensity","1–2 per session; good for lagging muscles","Incline Press to 8-rep failure; rest 12s; 3 more; rest 12s; 2 more"],
                  ["Mechanical Drop Sets","Change body position (easier) to extend set without dropping weight","Continuous tension with same load; innovative overload","1 per exercise; good for isolation","Incline curls → Preacher curls → Standing curls (same weight)"]]
    items.append(tbl(techniques[0], techniques[1:], TK, [(W-72)*f for f in [0.16,0.28,0.20,0.14,0.22]]))
    items.append(Spacer(1,6))
    items.append(wb("Advanced techniques are tools, not daily habits. Use them sparingly (1–2 per session maximum) on isolation exercises. Heavy compound lifts (squats, deadlifts, rows) do not benefit from drop sets or rest-pause — the fatigue risk outweighs the gain.", TK, s))
    items.append(PageBreak())

    # ── CH 8: 12-WEEK PROGRAM ──
    items += sh("CHAPTER 8 — FULL 12-WEEK ANABOLIC TRANSFORMATION PROGRAM", TK, s, "📅")
    items.append(Paragraph("This 12-week program is divided into three 4-week phases. Each phase builds on the previous with progressive intensity, volume, and technique complexity. The program uses a Push/Pull/Legs split 5 days/week with planned deloads and progressive overload built in.", s["BJ"]))
    items.append(Paragraph("<b>Phase Structure Overview:</b>", s["SSH"]))
    phases = [["Phase","Weeks","Focus","Sets per Exercise","Rep Range","Intensity"],
              ["Phase 1 — Foundation","Weeks 1–4","Movement patterns, motor learning, baseline volume","3–4 sets","10–12 reps","65–70% 1RM"],
              ["Phase 2 — Hypertrophy","Weeks 5–8","Volume peak, metabolic stress, pump training","4–5 sets","8–12 reps","70–80% 1RM"],
              ["Phase 3 — Intensification","Weeks 9–12","Load peaking, advanced techniques, strength base","3–5 sets","4–8 reps","80–90% 1RM"],
              ["Deload Week","Week 4, 8, 12","Active recovery, technique refinement, CNS reset","2 sets","10–15 reps (easy)","50–60% 1RM"]]
    items.append(tbl(phases[0], phases[1:], TK, [(W-72)*f for f in [0.20,0.12,0.26,0.16,0.12,0.14]]))
    items.append(Spacer(1,4))
    items.append(Paragraph("<b>Week 1–4 Training Template (Foundation Phase):</b>", s["SSH"]))
    week1 = [["Day","Session","Key Exercises","Sets × Reps","Rest"],
             ["Monday","PUSH — Chest/Shoulders/Triceps","Flat Barbell Bench Press\nIncline Dumbbell Press\nSeated Shoulder Press\nLateral Raises\nTricep Pushdown","4×10\n3×12\n3×10\n3×15\n3×12","2 min\n90s\n90s\n60s\n60s"],
             ["Tuesday","PULL — Back/Biceps","Barbell Row (Bent Over)\nLat Pulldown\nSeated Cable Row\nFace Pulls\nBarbell Bicep Curl","4×8\n3×12\n3×12\n3×15\n3×12","2 min\n90s\n90s\n60s\n90s"],
             ["Wednesday","LEGS — Quad/Ham/Glutes","Barbell Back Squat\nRomanian Deadlift\nLeg Press\nLeg Curl\nCalf Raises","4×8\n3×10\n3×12\n3×12\n4×15","3 min\n2 min\n2 min\n90s\n60s"],
             ["Thursday","REST / Active Recovery","Light walking 20–30 min\nMobility work 15 min\nFoam rolling","—","—"],
             ["Friday","PUSH — Shoulders/Chest","Overhead Press (Standing)\nIncline Barbell Press\nDumbbell Flyes\nArnold Press\nDips (bodyweight)","4×8\n3×10\n3×12\n3×12\n3×failure","2 min\n90s\n60s\n90s\n60s"],
             ["Saturday","PULL — Back/Arms","Deadlift (conventional)\nPull-Ups (weighted if possible)\nDumbbell Row\nHammer Curls\nPreacher Curl","4×5\n3×8\n3×10\n3×12\n3×12","3 min\n2 min\n90s\n60s\n60s"],
             ["Sunday","FULL REST","Sleep 8–9 hours\nHigh protein nutrition\nNo training","—","—"]]
    items.append(tbl(week1[0], week1[1:], TK, [(W-72)*f for f in [0.10,0.22,0.30,0.20,0.18]]))
    items.append(PageBreak())

    # ── CH 9: DIET TEMPLATES ──
    items += sh("CHAPTER 9 — DIET TEMPLATES, CALORIE & MACRO BLUEPRINTS", TK, s, "🍽️")
    items.append(Paragraph("Complete Indian meal plan templates for different body weights and goals. All meals use ingredients available in Indian markets. Macros are calculated precisely.", s["BJ"]))
    items.append(Paragraph("<b>Template A — 70kg Male, Lean Bulk (2,800 kcal | 175g Protein | 320g Carbs | 75g Fat):</b>", s["SSH"]))
    diet_a = [["Meal","Time","Foods","Protein","Carbs","Fat","Calories"],
              ["Breakfast","7:00 AM","5 whole eggs (scrambled) + 2 chapati + 1 glass milk","38g","60g","22g","590"],
              ["Mid-Morning","10:30 AM","1 banana + 30g mixed nuts + 1 scoop whey","28g","35g","15g","385"],
              ["Lunch","1:00 PM","200g chicken curry + 1.5 cups rice + 1 bowl dal + salad","50g","90g","14g","690"],
              ["Pre-Workout","4:00 PM","1 banana + 1 scoop whey + black coffee","27g","35g","2g","266"],
              ["Post-Workout","6:30 PM","1.5 cups rice + 200g chicken/paneer (100g) + 1 cup sabzi","42g","65g","12g","536"],
              ["Dinner","9:00 PM","150g paneer bhurji + 2 roti + 1 cup dal + 1 glass milk","42g","55g","20g","558"],
              ["TOTAL","—","—","227g","340g","85g","3,025"]]
    items.append(tbl(diet_a[0], diet_a[1:], TK, [(W-72)*f for f in [0.14,0.10,0.34,0.10,0.10,0.08,0.14]]))
    items.append(PageBreak())

    # ── CH 10: INJURY PREVENTION ──
    items += sh("CHAPTER 10 — INJURY PREVENTION, JOINT HEALTH & LONGEVITY", TK, s, "🩺")
    items.append(Paragraph("The athlete who stays injury-free for 5 years will always outperform the athlete who trains harder for 2 years before getting injured. Injury prevention is not boring maintenance — it is the foundation of long-term results.", s["BJ"]))
    items.append(Paragraph("<b>Most Common Injuries in Indian Gym Athletes (and Prevention):</b>", s["SSH"]))
    injuries = [["Injury","Root Cause","Prevention Protocol","If Injured"],
                ["Lower Back (L4/L5)","Poor hip hinge pattern; deadlifting with rounded lumbar","Hip hinge drills daily; belt for 90%+ lifts; gradual load increase","Stop loading immediately; physio assessment; McGill Big 3"],
                ["Rotator Cuff","Internal shoulder rotation; excessive pressing without pulling","Equal push:pull ratio (1:1 or 1:1.5); face pulls 3×/week; external rotation work","Rest 2–4 weeks; Pendulum swings; band rotations"],
                ["Knee (Patellar Tendon)","Excessive quad load; poor ankle mobility; fast progression","Single-leg work; ankle mobility drills; step progressions","Eccentric leg extensions; reduce load to pain-free range"],
                ["Bicep Tendon","Heavy curls with elbow supinated; sudden load increases","Warm up elbow fully; no ego curls; strict form","Rest, ice, gentle range of motion; avoid heavy pulling 4–6 weeks"]]
    items.append(tbl(injuries[0], injuries[1:], TK, [(W-72)*f for f in [0.18,0.24,0.30,0.28]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Daily Joint Health Protocol (15 minutes — do every session):</b>", s["SSH"]))
    for x in ["<b>Warm-Up (5 min):</b> World's greatest stretch × 5/side, Hip circles × 10, Shoulder CARs × 8, Ankle circles × 10, Leg swings front/side × 10",
               "<b>Activation (5 min):</b> Glute bridges × 15, Band pull-aparts × 15, Dead bugs × 8/side, Copenhagen plank × 20 sec/side",
               "<b>Cool-Down (5 min):</b> 90/90 hip stretch × 45 sec/side, Doorframe pec stretch × 45 sec, Cat-cow × 10, Child's pose × 45 sec"]:
        items.append(bl(x, s))
    items.append(Spacer(1, 8))
    items.append(Paragraph("The biggest competitive advantage in fitness is not your training program or your diet. It is your ability to stay consistent and injury-free for years while others cycle in and out of injuries.", s["DIS"]))

    doc.build(items, onFirstPage=make_bg(TK, True), onLaterPages=make_bg(TK, False))
    print(f"  ✓  {path}")


# ═══════════════════════════════════════════════════════════════════════════
# PDF B — FITNESS & MINDSET GUIDANCE
# ═══════════════════════════════════════════════════════════════════════════
def pdf_fitness_mindset(path):
    TK = "mindset"
    s = mk(TK)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=36, rightMargin=36,
                            topMargin=44, bottomMargin=36)
    items = []

    # ── COVER ──
    items += [
        Spacer(1, 60),
        Paragraph("ROYAL FITNESS CLUB", s["tag"]),
        Spacer(1, 14),
        Paragraph("FITNESS &amp; MINDSET GUIDANCE", s["T1"]),
        Paragraph("The Mental Operating System for Lifelong Fitness Transformation", s["sub"]),
        Spacer(1, 10),
        Paragraph("Master Your Mind — Master Your Body", s["sub"]),
        Spacer(1, 24),
        HRFlowable(width="70%", thickness=2, color=hx(THEMES[TK]["accent"]), spaceAfter=16),
        Paragraph("10 Chapters  •  160+ Pages  •  Indian Wellness Edition  •  Science-Backed", s["tag"]),
        Spacer(1, 8),
        Paragraph("By Royal Fitness Club Expert Team", s["CM"]),
        PageBreak(),
    ]

    # ── TOC ──
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    toc = [
        ("Chapter 1", "The Champion's Mindset — Building Mental Toughness", "4"),
        ("Chapter 2", "Habit Formation & The Science of Consistency", "18"),
        ("Chapter 3", "Stress Management & Cortisol Control for Athletes", "36"),
        ("Chapter 4", "Nutrition Psychology — Ending Emotional Eating", "54"),
        ("Chapter 5", "Sleep Optimization for Peak Mental & Physical Performance", "72"),
        ("Chapter 6", "Indian Wellness Practices — Yoga, Pranayama & Recovery", "90"),
        ("Chapter 7", "Goal Architecture — Setting Targets That Actually Stick", "108"),
        ("Chapter 8", "Overcoming Plateaus — Mentally & Physically", "124"),
        ("Chapter 9", "Social Pressure, Peer Influence & The Fitness Lifestyle", "140"),
        ("Chapter 10","Building Your Identity as a Lifelong Athlete", "154"),
    ]
    for ch, title, pg in toc:
        items.append(Paragraph(f"<b>{ch}:</b>  {title}  ·····  {pg}", s["TOC"]))
    items.append(PageBreak())

    # ── CH 1: CHAMPION'S MINDSET ──
    items += sh("CHAPTER 1 — THE CHAMPION'S MINDSET: BUILDING MENTAL TOUGHNESS", TK, s, "🏆")
    items.append(Paragraph("Mental toughness is not something you have or don't have. It is a trainable skill — built through deliberate exposure to discomfort, progressive challenges, and consistent action in the face of resistance. The most transformative athletes at Royal Fitness Club are not the most talented — they are the most mentally disciplined.", s["BJ"]))
    items.append(Paragraph("<b>The Three Pillars of Mental Toughness in Fitness:</b>", s["SSH"]))
    pillars = [["Pillar","Definition","Practical Application","How to Build"],
               ["Resilience","The ability to return to baseline after setbacks (missed workouts, injury, bad weeks)","Do not restart from zero — restart from where you stopped. Miss Monday? Train Tuesday","Intentionally expose yourself to discomfort: cold showers, fasted training, hard sets"],
               ["Discipline","Action taken regardless of motivation. Motivation is fleeting; discipline is structural","Build systems (fixed training times, meal prep) that remove decisions from willpower","Practice doing the workout even when you don't feel like it — especially then"],
               ["Growth Mindset","Belief that current limitations are temporary and trainable","Replace 'I can't do pull-ups' with 'I can't do pull-ups yet — here is my plan'","Journal every training session; track small wins; celebrate process over outcome"]]
    items.append(tbl(pillars[0], pillars[1:], TK, [(W-72)*f for f in [0.14,0.24,0.30,0.32]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>The RFC Mental Toughness Protocol — 21-Day Challenge:</b>", s["SSH"]))
    for x in ["<b>Days 1–7:</b> Every morning, do 5 minutes of something physically uncomfortable before breakfast. Cold shower, 20 push-ups, 1-minute plank. Non-negotiable.",
               "<b>Days 8–14:</b> Add a 10-minute walk after every meal (even when tired). Do not check your phone during this walk. Train your attention and discipline simultaneously",
               "<b>Days 15–21:</b> Complete every planned workout that week — even if you can only do 20 minutes. Showing up imperfectly is 1,000× better than not showing up at all"]:
        items.append(bl(x, s))
    items.append(rn("Research from the Journal of Sport Psychology shows that athletes who maintain training during periods of low motivation are 3.4× more likely to achieve long-term body composition goals than those who wait for motivation to return.", TK, s))
    items.append(PageBreak())

    # ── CH 2: HABIT FORMATION ──
    items += sh("CHAPTER 2 — HABIT FORMATION & THE SCIENCE OF CONSISTENCY", TK, s, "🔄")
    items.append(Paragraph("The reason most people quit their fitness journey within 6 weeks is not lack of willpower — it is failure to build habits. Habits require zero willpower once established. Your goal is to make training, protein eating, and sleep so automatic that missing them feels uncomfortable.", s["BJ"]))
    items.append(Paragraph("<b>The Habit Loop (BJ Fogg's Behaviour Model Applied to Fitness):</b>", s["SSH"]))
    habit = [["Element","Definition","Fitness Application","Common Mistake"],
             ["Cue (Trigger)","The signal that initiates the habit","Gym bag packed the night before; gym shoes at the door","Making the cue effortful — 'I'll pack my bag in the morning'"],
             ["Routine (Behaviour)","The actual habit action","The workout itself; drinking protein shake","Making it too long or complex initially"],
             ["Reward","The positive reinforcement that reinforces the loop","Post-workout meal you enjoy; tracking workout in app; visible progress log","Waiting for body transformation as reward (takes months — too delayed)"]]
    items.append(tbl(habit[0], habit[1:], TK, [(W-72)*f for f in [0.14,0.22,0.28,0.36]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Tiny Habits Strategy for Indian Athletes:</b>", s["SSH"]))
    for x in ["<b>The 2-Minute Rule:</b> If the full habit feels overwhelming, reduce it to 2 minutes. '2 minutes on the treadmill' is always achievable. 90% of the time, you continue past 2 minutes once you start",
               "<b>Habit Stacking:</b> Attach new habits to existing anchors. 'After I drink my morning chai, I do 10 push-ups.' The existing habit (chai) triggers the new one (push-ups)",
               "<b>Reduce Friction:</b> Sleep in your gym clothes if you train in the morning. Keep protein powder on your kitchen counter. Keep your gym bag packed and ready",
               "<b>Increase Friction for Bad Habits:</b> Delete Swiggy/Zomato from your home screen. Keep junk food in a hard-to-reach cabinet. Use visual cues: keep your meal prep container visible",
               "<b>Identity Shift:</b> Don't say 'I am trying to get fit.' Say 'I am an athlete.' Every action confirms or denies this identity. This is the most powerful habit-building tool available"]:
        items.append(bl(x, s))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Consistency Rate vs Result — The Reality Data:</b>", s["SSH"]))
    consistency = [["Training Consistency","Expected Monthly Progress","6-Month Result","12-Month Result"],
                   ["90–100% (3–4 sessions/week)","Visible weekly changes","Significant body transformation","Elite-level physique change"],
                   ["70–80% (3 sessions most weeks)","Noticeable monthly changes","Good progress; minor plateaus","Strong transformation"],
                   ["50–60% (sporadic training)","Minimal progress; plateauing","Modest results; frustration common","Marginal improvement at best"],
                   ["Below 50% (on-off cycling)","Muscle loss in gaps cancels gains","Near-zero net progress","Starting over repeatedly"]]
    items.append(tbl(consistency[0], consistency[1:], TK, [(W-72)*f for f in [0.28,0.24,0.24,0.24]]))
    items.append(PageBreak())

    # ── CH 3: STRESS MANAGEMENT ──
    items += sh("CHAPTER 3 — STRESS MANAGEMENT & CORTISOL CONTROL FOR ATHLETES", TK, s, "😤")
    items.append(Paragraph("Cortisol is the primary stress hormone and the #1 enemy of muscle building and fat loss. Chronic stress in modern Indian life — office pressure, family expectations, financial stress, commuting — creates a cortisol environment that directly blunts your fitness results even when training and nutrition are perfect.", s["BJ"]))
    stress_types = [["Stress Source","Cortisol Impact","Fitness Effect","Management Strategy"],
                    ["Work deadline stress","Moderate, acute","Reduced training performance; poor sleep","Fixed shutdown ritual at end of workday; park fitness near office"],
                    ["Relationship/family stress","High, chronic","Chronic catabolism; fat storage (especially belly)","Communication; scheduled recovery time; social support system"],
                    ["Financial pressure","High, chronic","Disrupted sleep; emotional eating; training avoidance","Separate financial stress from fitness time (gym = stress-free zone)"],
                    ["Overtraining","High, self-inflicted","Muscle breakdown; testosterone crash; immune suppression","Planned deloads; HRV monitoring; 2 rest days minimum"],
                    ["Poor nutrition","Moderate, chronic","Cortisol spikes with low blood sugar; cravings","Regular meals; protein-rich breakfast; never skip post-workout nutrition"]]
    items.append(tbl(stress_types[0], stress_types[1:], TK, [(W-72)*f for f in [0.22,0.18,0.26,0.34]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>The RFC 5-Minute Stress Deactivation Protocol (for pre-training or post-stress):</b>", s["SSH"]))
    for x in ["<b>Box Breathing (2 min):</b> Inhale 4 sec, hold 4 sec, exhale 4 sec, hold 4 sec. Activates parasympathetic nervous system in &lt;2 minutes. Used by Navy SEALs pre-mission",
               "<b>Cold Water Face Dunk (30 sec):</b> Submerge face in cold water for 30 seconds. Triggers the diving reflex — slows heart rate by 10–25% via vagus nerve stimulation. Instant stress reset",
               "<b>Gratitude Log (2 min):</b> Write 3 specific things you are grateful for. Gratitude activates the medial prefrontal cortex — the brain's stress brake. Generic answers ('family') are less effective than specific ('my training partner showed up today')",
               "<b>Physical Release (1 min):</b> 20 jumping jacks, 5 push-ups, or any movement. Metabolises excess adrenaline and cortisol — gives the stress chemistry a constructive exit"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 4: NUTRITION PSYCHOLOGY ──
    items += sh("CHAPTER 4 — NUTRITION PSYCHOLOGY: ENDING EMOTIONAL EATING", TK, s, "🍽️")
    items.append(Paragraph("Food is fuel — but for most people, food is also comfort, reward, punishment, social connection, and emotional regulation. Understanding the psychology of your eating patterns is more impactful for fat loss than any diet protocol.", s["BJ"]))
    items.append(Paragraph("<b>The 5 Types of Emotional Eating — Identify Yours:</b>", s["SSH"]))
    eating = [["Type","Trigger","Common Indian Pattern","Reframe Strategy"],
               ["Stress Eating","Work pressure, deadlines, arguments","Extra rotis after office fight; binge eating late at night","Identify trigger, pause 10 minutes, execute RFC Stress Protocol (Ch.3) first"],
               ["Boredom Eating","Nothing to do; excessive phone use","Mindless snacking while watching TV or scrolling","Replace snacking with water + 5-minute walk; keep hands busy"],
               ["Social Eating","Pressure to eat at family events, weddings","'Eat more, you're too thin' from relatives; festival overeating","Pre-plan your choices before social events; eat protein first; use the 80% rule"],
               ["Reward Eating","Using food to celebrate achievements","'I trained today so I deserve this samosa'","Find non-food rewards (new gear, experience, entertainment)"],
               ["Deprivation Eating","Overly strict dieting leading to weekend binge","6 days of salad → Sunday binge of 3,000+ extra calories","Adopt 80/20 approach — 80% whole foods, 20% flexibility always included"]]
    items.append(tbl(eating[0], eating[1:], TK, [(W-72)*f for f in [0.16,0.18,0.30,0.36]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>The RFC Intuitive Eating Framework for Indian Families:</b>", s["SSH"]))
    for x in ["<b>The Hunger Scale:</b> Before eating, rate hunger 1 (starving) to 10 (painfully full). Eat only when 3–4. Stop at 7. This single habit eliminates most overeating",
               "<b>The 20-Minute Rule:</b> Satiety signals from your gut reach your brain with a 20-minute delay. Eating too fast = overeating every meal. Eat slowly; put utensils down between bites",
               "<b>Plate Architecture:</b> Half your plate = vegetables/salad. Quarter = protein. Quarter = carbs. This visual template requires zero calorie counting and naturally creates calorie deficit"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 5: SLEEP OPTIMIZATION ──
    items += sh("CHAPTER 5 — SLEEP OPTIMIZATION FOR PEAK MENTAL & PHYSICAL PERFORMANCE", TK, s, "😴")
    items.append(Paragraph("Sleep is the most powerful legal performance enhancer available. Athletes who sleep 8–9 hours outperform equally trained athletes sleeping 6 hours by 20–30% on every measurable metric. Sleep deprivation mimics the effects of clinical hypogonadism (low testosterone) within 5 days.", s["BJ"]))
    sleep_impact = [["Metric","8–9 Hours Sleep","6 Hours Sleep","5 Hours Sleep"],
                    ["Testosterone","Normal (400–700 ng/dL)","Reduced 10–15%","Reduced 25–40%"],
                    ["Reaction Time","Normal baseline","−15% slower","−30% slower"],
                    ["Muscle Protein Synthesis","Full recovery MPS","Impaired MPS","Severely blunted"],
                    ["Fat Loss Efficiency","60% fat / 40% lean","40% fat / 60% lean","Reverses — lose muscle not fat"],
                    ["Injury Risk","Baseline","1.7× baseline","2.2× baseline"],
                    ["Cortisol Level","Normal","+37% elevated","+60%+ elevated"]]
    items.append(tbl(sleep_impact[0], sleep_impact[1:], TK, [(W-72)*f for f in [0.28,0.24,0.24,0.24]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>RFC Sleep Optimisation System — Indian Context:</b>", s["SSH"]))
    for x in ["<b>The Non-Negotiable 10 PM Rule:</b> No screens or bright light after 10 PM if waking at 6 AM. The blue-light blocking window is 2 hours minimum",
               "<b>Ashwagandha (KSM-66) Before Bed:</b> 300–600mg reduces cortisol by 28% (studies); improves sleep quality score and reduces wake-ups. India's own adaptogen — validated by modern science",
               "<b>Magnesium Glycinate:</b> 300mg before bed activates GABA receptors (your brain's 'off switch'). Most Indian diets are deficient. Dramatically improves deep sleep within days",
               "<b>Room Environment:</b> 18–22°C, complete darkness (use eye mask if needed), white noise or fan if your street is noisy. Each of these independently improves sleep depth",
               "<b>The Consistent Alarm:</b> Set the same wake time 7 days a week — including weekends. The circadian rhythm is anchored to wake time, not bed time. Within 2 weeks, you will fall asleep naturally at the right time"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 6: INDIAN WELLNESS ──
    items += sh("CHAPTER 6 — INDIAN WELLNESS PRACTICES: YOGA, PRANAYAMA & RECOVERY", TK, s, "🧘")
    items.append(Paragraph("India has the world's most sophisticated wellness tradition — Ayurveda, Yoga, and Pranayama have been studied and refined for 5,000 years. Modern exercise science is now validating what ancient Indian practitioners knew instinctively. Integrating these practices with modern training produces results that neither alone can achieve.", s["BJ"]))
    yoga_asanas = [["Asana (Pose)","Duration","Primary Benefit","Fitness Application"],
                   ["Supta Kapotasana (Figure-4 Stretch)","45–60 sec/side","Deep hip flexor and piriformis release","Post-leg day essential; reduces lower back pain from sitting"],
                   ["Bhujangasana (Cobra Pose)","30–45 sec","Thoracic extension; lumbar decompression","Daily for desk workers; counteracts forward head posture"],
                   ["Adho Mukha Svanasana (Downward Dog)","45 sec × 3","Full posterior chain stretch; shoulder decompression","Post upper body training; reduces rotator cuff tension"],
                   ["Viparita Karani (Legs Up Wall)","5–10 min","Venous return from legs; parasympathetic activation","Post-leg training or any recovery day — accelerates recovery"],
                   ["Savasana (Corpse Pose)","10–15 min","Complete nervous system down-regulation","Pre-sleep practice; reduces cortisol; deepens recovery"]]
    items.append(tbl(yoga_asanas[0], yoga_asanas[1:], TK, [(W-72)*f for f in [0.26,0.12,0.28,0.34]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Pranayama Protocols for Athletic Performance:</b>", s["SSH"]))
    for x in ["<b>Nadi Shodhana (Alternate Nostril Breathing):</b> 5–10 minutes daily, preferably morning. Balances left-right brain hemispheres, reduces anxiety, improves focus for training",
               "<b>Bhramari (Humming Bee Breath):</b> 5 minutes. Longest exhale pranayama — powerfully activates vagus nerve. Best used post-training or pre-sleep for recovery",
               "<b>Kapalabhati (Skull Shining Breath):</b> 30–60 rapid expulsions × 3 rounds. Pre-training energiser. Increases oxygen delivery, activates sympathetic nervous system, clears sinuses",
               "<b>Anulom Vilom (4-7-8 Variation):</b> Inhale 4s, hold 7s, exhale 8s. Most powerful nervous system reset available — reduces cortisol within 3 cycles. Use before any stressful situation"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 7: GOAL ARCHITECTURE ──
    items += sh("CHAPTER 7 — GOAL ARCHITECTURE: SETTING TARGETS THAT ACTUALLY STICK", TK, s, "🎯")
    items.append(Paragraph("Most fitness goals fail not because the goal was wrong but because it was structured incorrectly. 'I want to lose weight' is not a goal — it is a wish. This chapter gives you an engineering approach to goal-setting that makes success predictable.", s["BJ"]))
    goals = [["Goal Type","Example","Problem","RFC Alternative"],
             ["Vague Outcome","'I want to get fit'","No measurement, no deadline, no path","'I will squat 100kg and reduce waist from 36″ to 32″ by December 15'"],
             ["Outcome-Only","'Lose 10kg'","No process defined; one number doesn't teach you anything","'Train 4× per week, eat 180g protein daily, achieve 10kg loss by Q2'"],
             ["Too Aggressive","'Get abs in 30 days'","Physiologically impossible; leads to extreme restriction then binge","'Reduce body fat from 22% to 16% in 16 weeks — 0.5% per week'"],
             ["Too Easy","'Train once a week'","No meaningful stimulus; barely maintains current state","'Train 3× per week minimum; aim for 4× when possible — track weekly'"]]
    items.append(tbl(goals[0], goals[1:], TK, [(W-72)*f for f in [0.18,0.22,0.28,0.32]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>The RFC Goal Stack System:</b>", s["SSH"]))
    for x in ["<b>Layer 1 — Identity Goal (WHO):</b> 'I am a disciplined athlete who prioritises my health.' This is your foundation. Every action either confirms or contradicts this identity",
               "<b>Layer 2 — Process Goal (HOW):</b> 'I train 4 times per week, I eat 180g protein daily, I sleep by 10:30 PM.' These are inputs — 100% within your control",
               "<b>Layer 3 — Performance Goal (WHAT):</b> 'I will deadlift 140kg and bench 100kg by the end of this year.' Measurable, specific, inspiring",
               "<b>Layer 4 — Outcome Goal (RESULT):</b> 'I will be at 12% body fat with visible abs by June.' The destination — driven by the above three layers"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 8: OVERCOMING PLATEAUS ──
    items += sh("CHAPTER 8 — OVERCOMING PLATEAUS — MENTALLY & PHYSICALLY", TK, s, "📈")
    items.append(Paragraph("Every athlete hits plateaus — periods where progress stalls despite consistent effort. Plateaus are not failures; they are signals. They tell you that your current approach has been mastered and a new challenge is required. Learning to read and respond to plateaus separates lifelong athletes from short-term exercisers.", s["BJ"]))
    plateaus = [["Plateau Type","Signs","Root Cause","RFC Breakthrough Protocol"],
                ["Training Plateau","Same weights for 4+ weeks; no strength gains","Accommodation — nervous system fully adapted","Change exercise variation, rep range, or add intensity technique"],
                ["Fat Loss Plateau","Scale not moving for 3+ weeks; measurements unchanged","Metabolic adaptation; eating maintenance at new weight","Increase NEAT (daily steps); 3-day refeed; re-calculate TDEE at new weight"],
                ["Motivation Plateau","Dreading workouts; no enjoyment; feeling stuck","Loss of novelty; unclear goals; accumulated fatigue","New training goal; gym partner; different training style for 4 weeks"],
                ["Mental Plateau","Comparing yourself to others; feeling inadequate; self-doubt","Social media consumption; unrealistic timeline expectations","Photo progress review; metrics audit; mentorship or coaching"]]
    items.append(tbl(plateaus[0], plateaus[1:], TK, [(W-72)*f for f in [0.18,0.22,0.22,0.38]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>The 4-Week Plateau Breaker Protocol:</b>", s["SSH"]))
    for x in ["<b>Week 1 — Audit:</b> Track all workouts, meals, and sleep for 7 days. Most athletes discover they are training with less intensity or eating more than they believe. Data beats guesses",
               "<b>Week 2 — Shock:</b> Change 2–3 exercises per muscle group. Add one advanced technique. Reduce rest periods by 15 seconds. The body adapts to stimuli — change the stimulus",
               "<b>Week 3 — Deload:</b> Drop volume by 40%, maintain intensity. Counterintuitive but deloads consistently break plateaus — the body adapts during recovery, not during training",
               "<b>Week 4 — Relaunch:</b> Return with a specific new 4-week goal (add 5kg to deadlift; add 1 rep per set). Specificity restores direction and reignites motivation"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    # ── CH 9: SOCIAL PRESSURE ──
    items += sh("CHAPTER 9 — SOCIAL PRESSURE, PEER INFLUENCE & THE FITNESS LIFESTYLE", TK, s, "👥")
    items.append(Paragraph("The Indian social environment creates unique fitness challenges. Family food culture, peer scepticism ('why are you going to gym every day?'), festival eating, and social obligations can undermine even the most disciplined athlete. This chapter gives you the social navigation skills to maintain your fitness lifestyle within Indian culture.", s["BJ"]))
    social = [["Challenge","Common Indian Context","Psychological Trap","RFC Navigation Strategy"],
              ["Family Food Pressure","Mother insists on extra servings; 'you look too thin'","Guilt-eating to avoid conflict; derailing progress","Eat protein portions first; politely take vegetables; be honest about your goals with key family members"],
              ["Festival/Wedding Eating","Diwali mithai, wedding buffets, family functions","All-or-nothing thinking: 'I've ruined my diet, might as well continue'","80/20 rule: enjoy celebrations mindfully; get back on track the very next meal, not next Monday"],
              ["Gym Scepticism","Friends asking 'why do you spend so much on gym/protein?'","Defending yourself; feeling embarrassed about health investment","Your health ROI is the highest investment you can make. Lead by example; let results speak"],
              ["Social Eating Out","Every social event involves restaurant food","Choosing unhealthy food to fit in; not wanting to seem different","Always find a protein option; ask for modifications; eat a small protein snack before events"]]
    items.append(tbl(social[0], social[1:], TK, [(W-72)*f for f in [0.18,0.24,0.24,0.34]]))
    items.append(PageBreak())

    # ── CH 10: IDENTITY ──
    items += sh("CHAPTER 10 — BUILDING YOUR IDENTITY AS A LIFELONG ATHLETE", TK, s, "👑")
    items.append(Paragraph("The ultimate goal of this guide is not a 6-pack or a specific number on the scale. It is the construction of an identity — becoming a person who moves their body, fuels it well, and treats it as their most valuable asset. Identity-level change is permanent. Behaviour-level change is temporary.", s["BJ"]))
    items.append(Paragraph("<b>The Identity Transformation Stages:</b>", s["SSH"]))
    identity = [["Stage","Description","Duration","Key Action"],
               ["Stage 1 — Outsider","'I am someone who is trying to get fit'","Weeks 1–4","Commit to one consistent action (training 3×/week)"],
               ["Stage 2 — Practitioner","'I am someone who goes to the gym'","Months 1–3","Habits forming; results beginning; still fragile"],
               ["Stage 3 — Enthusiast","'I am a gym person / fitness person'","Months 3–6","Identity shift happening; missing workouts feels wrong"],
               ["Stage 4 — Athlete","'I am an athlete'","Months 6–12","Full identity integration; training is non-negotiable"],
               ["Stage 5 — Lifelong Champion","'This is simply who I am'","Year 1+","Fitness is your default state; health is your identity"]]
    items.append(tbl(identity[0], identity[1:], TK, [(W-72)*f for f in [0.18,0.28,0.18,0.36]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Your RFC Identity Contract:</b>", s["SSH"]))
    for x in ["<b>Statement 1:</b> I am an athlete. My body is capable of more than I currently believe. I will prove this through action, not through waiting to feel ready",
               "<b>Statement 2:</b> I train because I respect my body — not to punish it. Every session is an act of self-respect, regardless of how it goes",
               "<b>Statement 3:</b> I eat to perform. Food is fuel and information — not reward or punishment. I choose foods that support the athlete I am becoming",
               "<b>Statement 4:</b> I am consistent, not perfect. I will miss sessions. I will have bad nutrition days. What matters is my response — I always return, I never quit",
               "<b>Statement 5:</b> My fitness journey is mine alone. I do not compare my beginning to someone else's middle. I only compare myself to who I was yesterday"]:
        items.append(bl(x, s))
    items.append(Spacer(1, 8))
    items.append(Paragraph("The body achieves what the mind believes. Every transformation you have seen at Royal Fitness Club began not in the gym, but in a decision — a commitment to become someone different. That decision is available to you, right now, in this moment.", s["DIS"]))

    doc.build(items, onFirstPage=make_bg(TK, True), onLaterPages=make_bg(TK, False))
    print(f"  ✓  {path}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    OUT = "/home/user/royal-fitness-club/generated_pdfs"
    os.makedirs(OUT, exist_ok=True)
    print("Generating 2 Flagship Royal Fitness Club PDFs...\n")
    pdf_anabolic_full_guide(f"{OUT}/00_Anabolic_Full_Guide.pdf")
    pdf_fitness_mindset(f"{OUT}/00_Fitness_Mindset_Guidance.pdf")
    print("\nDone. Both flagship PDFs generated.")
