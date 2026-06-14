"""Append extended content to Anabolic Full Guide to reach 50+ pages."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

OUT = '/home/user/royal-fitness-club/generated_pdfs'
RED = colors.HexColor('#e8001d')
GOLD = colors.HexColor('#ffd000')
LGREY = colors.HexColor('#cccccc')
GREY = colors.HexColor('#888888')
WHITE = colors.white

W, H = A4

def get_styles():
    s = getSampleStyleSheet()
    defs = {
        'Cover1': dict(fontName='Helvetica-Bold', fontSize=36, textColor=WHITE, alignment=TA_CENTER, spaceAfter=6, leading=44),
        'Cover2': dict(fontName='Helvetica-Bold', fontSize=18, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4, leading=24),
        'Cover3': dict(fontName='Helvetica', fontSize=11, textColor=LGREY, alignment=TA_CENTER, spaceAfter=6, leading=16),
        'ChHead': dict(fontName='Helvetica-Bold', fontSize=15, textColor=RED, spaceBefore=14, spaceAfter=8, leading=20),
        'SecHead': dict(fontName='Helvetica-Bold', fontSize=12, textColor=WHITE, spaceBefore=10, spaceAfter=5, leading=17),
        'Body': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=6, leading=16, alignment=TA_JUSTIFY),
        'Blt': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=4, leading=15, leftIndent=14, firstLineIndent=-10),
        'Callout': dict(fontName='Helvetica-BoldOblique', fontSize=10, textColor=GOLD, spaceBefore=6, spaceAfter=6, leading=16, leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY),
        'TOCItem': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15),
    }
    for name, kw in defs.items():
        if name not in s:
            s.add(ParagraphStyle(name=name, **kw))
        else:
            for k, v in kw.items():
                setattr(s[name], k, v)
    return s

def tb(story, headers, rows, widths=None):
    data = [headers] + rows
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RED),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#1a1a1a'), colors.HexColor('#0f0f0f')]),
        ('TEXTCOLOR', (0,1), (-1,-1), LGREY),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#333')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 3*mm))

def hr(story):
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#333'), spaceBefore=4, spaceAfter=4))

def bl(story, s, items):
    for i in items:
        story.append(Paragraph(f'• {i}', s['Blt']))

def co(story, s, text):
    story.append(Paragraph(f'💡 {text}', s['Callout']))

def build_extended_anabolic():
    path = os.path.join(OUT, '00_Anabolic_Full_Guide.pdf')
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=16*mm, bottomMargin=16*mm)
    s = get_styles()
    story = []

    # ── COVER ──
    story.append(Spacer(1, 28*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB', s['Cover3']))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('ANABOLIC FULL GUIDE', s['Cover1']))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('Complete Muscle Building & Transformation Manual', s['Cover2']))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='80%', thickness=1, color=RED, spaceAfter=8))
    story.append(Paragraph('12 Chapters  ·  60+ Pages  ·  12-Week Program  ·  Indian Athletes Edition', s['Cover3']))
    story.append(Paragraph('By Royal Fitness Club Expert Team', s['Cover3']))
    story.append(PageBreak())

    # ── DISCLAIMER ──
    story.append(Paragraph('MEDICAL DISCLAIMER', s['ChHead']))
    story.append(Paragraph(
        'This guide is for educational purposes only. It does not constitute medical advice. Always consult a qualified '
        'medical professional before beginning any training, nutrition, or supplementation programme. Individual results '
        'vary based on genetics, consistency, starting condition, and adherence. Royal Fitness Club accepts no liability '
        'for any injury, health issue, or financial loss arising from use of this guide.', s['Body']))
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ──
    story.append(Paragraph('TABLE OF CONTENTS', s['ChHead']))
    hr(story)
    toc_items = [
        ('1', 'Muscle Building Fundamentals & Science', 5),
        ('2', 'Anabolic Hormones & Natural Optimisation', 8),
        ('3', 'Progressive Overload — The Science of Progress', 12),
        ('4', 'Nutrition Blueprints for Maximum Muscle Growth', 16),
        ('5', 'High-Protein Indian Food & Meal Timing', 20),
        ('6', 'Supplement Guide — Ranked by Evidence', 24),
        ('7', 'Recovery, Sleep & Cortisol Management', 28),
        ('8', 'Advanced Training Techniques', 32),
        ('9', 'Full 12-Week Anabolic Transformation Program', 36),
        ('10', 'Complete Weekly Workout Library', 42),
        ('11', 'Indian Diet Templates & Macro Blueprints', 50),
        ('12', 'Injury Prevention, Joint Health & Longevity', 56),
        ('App A', 'Glossary of Key Terms', 61),
        ('App B', 'Frequently Asked Questions', 63),
    ]
    for ch, title, pg in toc_items:
        story.append(Paragraph(f'Chapter {ch} — {title} {"·" * max(2,52-len(title)-len(str(pg)))} {pg}', s['TOCItem']))
    story.append(PageBreak())

    # ── CH1 ──
    story.append(Paragraph('CHAPTER 1 — MUSCLE BUILDING FUNDAMENTALS & SCIENCE', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Three Mechanisms of Hypertrophy', s['SecHead']))
    story.append(Paragraph(
        'Muscle hypertrophy — the increase in muscle fibre cross-sectional area — occurs through three distinct but interconnected mechanisms. '
        'Understanding each mechanism allows you to structure training intelligently rather than randomly. Most gym-goers stimulate only one '
        'mechanism and wonder why they plateau after 3–6 months of consistent training.', s['Body']))
    bl(story, s, [
        'Mechanical Tension: The primary driver of hypertrophy. When a muscle fibre is placed under load through its full range of motion, the tension on the sarcomere activates mechanosensors (integrins, focal adhesion kinase) that trigger the mTOR signalling cascade — the master regulator of muscle protein synthesis. Heavier compound lifts, full ROM, and time under tension all maximise this mechanism.',
        'Metabolic Stress: The "pump" mechanism. Accumulation of lactate, hydrogen ions, and inorganic phosphate during high-rep training creates a cellular environment that increases anabolic hormone secretion locally, stimulates satellite cell activation, and produces cell swelling — all of which signal growth. Isolation exercises, moderate weight (12–20 reps), short rest periods (45–75 sec) maximise metabolic stress.',
        'Muscle Damage: Eccentric-dominant loading causes micro-tears in the muscle fibre and connective tissue. Repair via satellite cell fusion results in thicker, stronger fibres. Novel exercises, slow eccentrics (3–4 seconds on the lowering phase), and training through the lengthened position maximise muscle damage stimulus.',
    ])
    co(story, s, 'Key Insight: Train all three mechanisms weekly. Compound lifts for tension, isolation finishers for metabolic stress, slow eccentrics and new movements for muscle damage.')
    story.append(Paragraph('Muscle Fibre Types & Training Implications', s['SecHead']))
    tb(story,
        ['Fibre Type', 'Characteristics', 'Best Rep Range', 'Example'],
        [
            ['Type I', 'Endurance, fatigue-resistant, smaller', '15–30 reps', 'Cable flyes, leg press high-rep'],
            ['Type II-A', 'Strength + endurance hybrid', '8–15 reps', 'Bench press, squats, rows'],
            ['Type II-X', 'Max power, fatigues quickly', '1–6 reps', 'Deadlift, heavy OHP, sprints'],
        ], widths=[70, 140, 90, 160])
    story.append(Paragraph('Protein Synthesis vs Muscle Protein Breakdown', s['SecHead']))
    story.append(Paragraph(
        'Net muscle gain occurs only when Muscle Protein Synthesis (MPS) exceeds Muscle Protein Breakdown (MPB) over time. '
        'Training strongly elevates MPS for 24–48 hours post-session. Adequate protein intake (particularly leucine — the mTOR trigger) '
        'sustains this elevated synthetic rate. Sleep, caloric sufficiency, and low cortisol all suppress MPB. '
        'The athlete\'s job is to maximise MPS triggers while minimising MPB drivers.', s['Body']))
    story.append(Paragraph('The Role of Volume in Hypertrophy', s['SecHead']))
    story.append(Paragraph(
        'Volume — defined as Sets × Reps × Load — is the primary driver of hypertrophy over time for intermediate and advanced athletes. '
        'Research by Krieger (2010) showed that 2–3 sets per exercise produce 40% greater hypertrophy than 1 set. '
        'Schoenfeld et al. (2017) found a dose-response relationship up to approximately 10–20 hard sets per muscle per week. '
        'Above this threshold, additional volume can impair recovery without proportional gain. For natural Indian athletes aged 20–40: '
        '10–16 weekly hard sets per muscle group is the evidence-based starting point.', s['Body']))
    tb(story,
        ['Training Level', 'Weekly Sets/Muscle', 'Frequency', 'Session Duration'],
        [
            ['Beginner (0–12 months)', '6–10 sets', '2×/week', '45–55 min'],
            ['Intermediate (1–3 years)', '10–16 sets', '2–3×/week', '55–70 min'],
            ['Advanced (3+ years)', '14–22 sets', '2–4×/week', '60–80 min'],
        ], widths=[120, 100, 100, 120])
    story.append(PageBreak())

    # ── CH2 ──
    story.append(Paragraph('CHAPTER 2 — ANABOLIC HORMONES & NATURAL OPTIMISATION', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Four Primary Anabolic Hormones', s['SecHead']))
    story.append(Paragraph(
        'Your hormonal environment sets the ceiling for natural muscle-building potential. Testosterone, Growth Hormone (GH), '
        'IGF-1, and Insulin work in concert to regulate protein synthesis, satellite cell activation, fat oxidation, and glycogen storage. '
        'Every lifestyle choice either supports or suppresses these hormones — often more powerfully than any supplement.', s['Body']))
    story.append(Paragraph('Testosterone — The Master Anabolic Hormone', s['SecHead']))
    story.append(Paragraph(
        'Normal male testosterone range in India: 300–1000 ng/dL. Testosterone binds to androgen receptors (AR) in muscle cells, '
        'activating gene transcription for contractile proteins (actin, myosin). Higher AR density = better response to the same testosterone level. '
        'AR density is trainable — resistance training increases AR expression by 25–50% in trained muscle over 12 weeks.', s['Body']))
    bl(story, s, [
        'Compound lifts (squat, deadlift, bench) trigger the largest acute testosterone spike.',
        'Sleep 7.5–9h: 60–70% of daily T is produced during slow-wave sleep. One week of 5h nights reduces T by 10–15%.',
        'Body fat 10–18%: Excess adipose aromatises T to oestrogen via aromatase enzyme.',
        'Zinc & Vitamin D3: Rate-limiting cofactors for T synthesis. Common deficiencies in India due to indoor lifestyles.',
        'Stress management: Cortisol and testosterone compete for the same precursor (pregnenolone). Chronic stress blunts T.',
    ])
    story.append(Paragraph('Growth Hormone & the IGF-1 Axis', s['SecHead']))
    story.append(Paragraph(
        'GH is released in pulses from the anterior pituitary — largest pulse occurring during Stage 3 NREM sleep. '
        'GH stimulates the liver to produce IGF-1, which activates the PI3K/Akt/mTOR pathway — the same pathway activated by resistance training. '
        'This synergy means athletes who sleep well and train hard experience multiplicative (not additive) anabolic effects.', s['Body']))
    tb(story,
        ['Factor', 'Effect on GH/IGF-1', 'Practical Action'],
        [
            ['Deep sleep (8h)', '↑↑↑ GH pulse amplitude', 'Prioritise dark room, same bedtime'],
            ['High-intensity exercise', '↑↑ acute GH release', 'Include compound heavy sets'],
            ['16h fast', '↑↑ GH (3–5× baseline)', 'Intermittent fasting optional'],
            ['Body fat >25%', '↓↓ GH pulse', 'Prioritise fat loss first'],
            ['Protein intake adequate', '↑ IGF-1 production', 'Maintain 1.8–2.2g/kg/day'],
        ], widths=[110, 120, 170])
    story.append(Paragraph('Insulin — The Double-Edged Hormone', s['SecHead']))
    story.append(Paragraph(
        'Insulin drives amino acids and glucose into muscle cells, inhibits muscle protein breakdown, and stimulates glycogen synthesis. '
        'The key is timing: spike insulin around training when muscles are insulin-sensitive; manage it the rest of the day to prevent fat storage. '
        'Post-workout: rice + dal + chicken is near-perfect — fast carbs (rice) spike insulin, complete protein (chicken) saturates MPS, slow protein (dal) extends it.', s['Body']))
    story.append(Paragraph('Cortisol — The Catabolic Antagonist', s['SecHead']))
    story.append(Paragraph(
        'Chronic cortisol elevation activates the ubiquitin-proteasome pathway (muscle breakdown), inhibits testosterone synthesis, '
        'impairs sleep quality, and promotes visceral fat. Training sessions over 75 minutes consistently elevate cortisol without '
        'proportional anabolic benefit. Keep sessions focused and under 75 minutes; manage life stress actively.', s['Body']))
    bl(story, s, [
        'Ashwagandha KSM-66 (600mg/day): Reduces cortisol by 27.9% in peer-reviewed trial (Chandrasekhar et al., 2012).',
        'Post-workout carbohydrate: blunts cortisol spike by 20–30% — eat your post-workout carbs.',
        'Meditation (10 min/day): Measurably reduces baseline cortisol within 4 weeks of consistent practice.',
        'Sleep 7.5–9h: Sleep deprivation is the fastest way to chronically elevate cortisol.',
    ])
    story.append(PageBreak())

    # ── CH3 ──
    story.append(Paragraph('CHAPTER 3 — PROGRESSIVE OVERLOAD — THE SCIENCE OF PROGRESS', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Non-Negotiable Law', s['SecHead']))
    story.append(Paragraph(
        'Progressive overload is the single most important training principle. Without systematically increasing demand on muscle tissue, '
        'the body has no stimulus to adapt. Muscles grow only when challenged beyond their current capacity — and they must be repeatedly '
        're-challenged as they adapt. Progressive overload is not just "add weight every week" — it encompasses 10 distinct methods.', s['Body']))
    tb(story,
        ['Method', 'How to Apply', 'Best For', 'Frequency'],
        [
            ['Add weight', 'Increase load when reps hit top of range with RIR≥2', 'Compound lifts', 'Every 1–2 weeks'],
            ['Add reps', 'Same weight, more reps each session', 'Accessory work', 'Weekly'],
            ['Add sets', 'Gradually increase weekly volume (+1 set/muscle/week)', 'All levels', 'Monthly'],
            ['Reduce rest', 'Shorten rest by 10sec per session', 'Metabolic goals', 'Weekly'],
            ['Slow eccentric', 'Add 1 sec to lowering phase', 'Hypertrophy focus', 'Monthly'],
            ['Increase ROM', 'Work through greater joint range', 'Muscle length emphasis', 'Monthly'],
            ['Better technique', 'Stricter form = greater target activation', 'All levels', 'Always'],
            ['Increase frequency', 'Train muscle 2×/wk → 3×/wk', 'Intermediate plateaus', 'Phase change'],
            ['Density blocks', 'More total work in same time window', 'Advanced', 'Phase change'],
            ['Harder variation', 'Progress to more challenging exercise', 'All levels', 'Phase change'],
        ], widths=[80, 150, 100, 80])
    story.append(Paragraph('Periodisation Models', s['SecHead']))
    story.append(Paragraph(
        'Periodisation is the systematic variation of training variables (volume, intensity, frequency) to maximise long-term adaptation '
        'while managing fatigue. Without periodisation, fatigue accumulates faster than fitness — causing overtraining, plateau, and injury. '
        'Three primary models serve different athletes and goals.', s['Body']))
    tb(story,
        ['Model', 'Structure', 'Best For', 'Evidence'],
        [
            ['Linear (LP)', 'Volume ↓, intensity ↑ week by week', 'Beginners 0–12 months', 'Strong'],
            ['Daily Undulating (DUP)', 'Different rep ranges on different days', 'Intermediate 1–4 years', 'Very strong'],
            ['Block Periodisation', 'Accumulation → Intensification → Realisation', 'Advanced 4+ years', 'Strong'],
        ], widths=[90, 150, 120, 80])
    co(story, s, 'For Indian athletes aged 18–35 seeking muscle gain: Daily Undulating Periodisation in a Push/Pull/Legs split is the most evidence-backed natural hypertrophy approach.')
    story.append(Paragraph('Deloading — Why Backing Off Makes You Bigger', s['SecHead']))
    story.append(Paragraph(
        'A deload is a planned reduction in training volume/intensity for 1 week every 4–8 weeks of hard training. '
        'Its purpose is to dissipate accumulated systemic fatigue, allowing the nervous system to fully express adaptations '
        'built during the preceding block. Post-deload personal records (PRs) are the rule, not the exception, when deloads are correctly timed.', s['Body']))
    tb(story,
        ['Deload Type', 'Volume Change', 'Intensity Change', 'Best Use'],
        [
            ['Volume deload', '−40–60% sets', 'Same weight', 'Accumulated volume fatigue'],
            ['Intensity deload', 'Same sets', '−15–20% weight', 'Joint/tendon soreness'],
            ['Full deload', '−50% both', '−20% weight', 'After competition/peaking'],
            ['Active recovery', 'Light cardio/mobility', 'Very low', 'Overreaching/illness'],
        ], widths=[100, 100, 110, 130])
    story.append(PageBreak())

    # ── CH4 ──
    story.append(Paragraph('CHAPTER 4 — NUTRITION BLUEPRINTS FOR MAXIMUM MUSCLE GROWTH', s['ChHead']))
    hr(story)
    story.append(Paragraph('Calorie Targets by Goal', s['SecHead']))
    tb(story,
        ['Goal', 'Calorie Target', 'Protein', 'Carbohydrates', 'Fats'],
        [
            ['Lean Bulk', 'TDEE + 250–350 kcal', '2.0–2.2g/kg', '4–5g/kg', '0.8–1.0g/kg'],
            ['Fat Loss', 'TDEE − 350–500 kcal', '2.2–2.5g/kg', '2–3g/kg', '0.7–0.9g/kg'],
            ['Recomposition', 'TDEE ± 0–100 kcal', '1.8–2.2g/kg', '3–4g/kg', '0.8–1.0g/kg'],
        ], widths=[90, 100, 75, 90, 75])
    story.append(Paragraph('Protein — The Foundation Macro', s['SecHead']))
    story.append(Paragraph(
        'Protein is the only macro that directly builds muscle tissue. The ISSN (2017) consensus: 1.6–2.2g/kg/day is optimal for '
        'muscle protein synthesis. For athletes in a caloric deficit (cutting), increase to 2.2–2.5g/kg to protect muscle mass. '
        'Leucine is the key amino acid triggering mTOR — each meal should contain ≥3g leucine (~30–35g complete protein) to '
        'maximally activate muscle protein synthesis. Spreading protein across 4–5 meals is superior to 2–3 large servings.', s['Body']))
    story.append(Paragraph('Carbohydrates — The Performance Fuel', s['SecHead']))
    story.append(Paragraph(
        'Carbohydrates are the primary fuel for high-intensity resistance training. Muscle glycogen is the substrate for intense efforts — '
        'depleted glycogen directly impairs training performance, volume capacity, and recovery speed. Low-carb diets reduce training '
        'performance by 7–15% in resistance-trained athletes. For Indian athletes: rice, roti, oats, and fruit are excellent, '
        'culturally appropriate carbohydrate sources. Fear of carbs is one of the most productivity-destroying nutrition myths.', s['Body']))
    story.append(Paragraph('Dietary Fats — Hormones & Health', s['SecHead']))
    story.append(Paragraph(
        'Dietary fat is essential for testosterone production (cholesterol is the precursor), fat-soluble vitamin absorption, '
        'joint lubrication, and cell membrane integrity. Target 20–30% of total calories from fat, with emphasis on unsaturated '
        'sources (nuts, seeds, ghee, fatty fish) and adequate saturated fat (eggs, full-fat dairy) for hormone synthesis. '
        'Trans fats (vanaspati, processed foods) directly suppress testosterone and impair cardiovascular health — eliminate them.', s['Body']))
    co(story, s, 'Ghee (desi ghee) in moderate amounts is not the villain it was once portrayed as. It is rich in butyrate, supports gut health, and provides fat-soluble vitamins. 1–2 tsp daily is beneficial for Indian athletes.')
    story.append(Paragraph('Meal Frequency & Timing', s['SecHead']))
    tb(story,
        ['Timing', 'What to Eat', 'Purpose'],
        [
            ['Pre-workout (60–90 min)', '40–60g carbs + 25g protein + minimal fat', 'Max glycogen, raise blood amino acids'],
            ['Post-workout (<45 min)', '50–80g fast carbs + 30–40g fast protein', 'Insulin spike, suppress MPB'],
            ['Pre-sleep', '30–40g slow protein (paneer, dahi, eggs)', 'Sustain MPS for 7h during sleep'],
            ['Rest days', 'Maintain protein; slightly reduce carbs', 'Recovery, maintain anabolic state'],
        ], widths=[100, 180, 160])
    story.append(PageBreak())

    # ── CH5 ──
    story.append(Paragraph('CHAPTER 5 — HIGH-PROTEIN INDIAN FOOD & MEAL TIMING', s['ChHead']))
    hr(story)
    story.append(Paragraph('Complete Indian Protein Food Database', s['SecHead']))
    tb(story,
        ['Food', 'Serving', 'Protein', 'Calories', 'Notes'],
        [
            ['Chicken breast', '100g cooked', '31g', '165 kcal', 'Complete protein, BV 79'],
            ['Eggs (whole)', '1 large', '6g', '78 kcal', 'Best BV (100), complete amino profile'],
            ['Paneer', '100g', '18g', '265 kcal', 'Casein-rich, slow-digesting'],
            ['Moong dal (cooked)', '150g', '10g', '170 kcal', 'Leucine-rich, affordable'],
            ['Chana dal', '150g', '12g', '200 kcal', 'High fibre + protein'],
            ['Greek yogurt (dahi)', '200g', '14g', '140 kcal', 'Probiotics + casein'],
            ['Soya chunks (dry)', '50g', '25g', '175 kcal', 'Complete plant protein'],
            ['Fish (rohu)', '100g', '22g', '120 kcal', 'Omega-3 rich, anabolic'],
            ['Chicken egg whites', '3 large', '10g', '50 kcal', 'Near-zero fat, fast absorbing'],
            ['Low-fat cottage cheese', '100g', '11g', '98 kcal', 'Slow-release, good at night'],
            ['Whey protein', '1 scoop (30g)', '24g', '120 kcal', 'Fast-absorbing, post-workout ideal'],
            ['Rajma (cooked)', '150g', '8g', '185 kcal', 'Combine with rice for complete protein'],
            ['Milk (full-fat)', '250ml', '8g', '150 kcal', 'Casein + whey natural combination'],
            ['Chicken thigh', '100g', '26g', '210 kcal', 'More flavour, slightly higher fat'],
            ['Tuna (canned)', '100g', '26g', '116 kcal', 'Very affordable, complete protein'],
        ], widths=[90, 70, 55, 65, 160])
    story.append(Paragraph('Budget High-Protein Meal Plans (Under ₹200/day)', s['SecHead']))
    tb(story,
        ['Meal', 'Foods', 'Protein', 'Cost'],
        [
            ['Breakfast', '3 eggs + 2 roti + glass of milk', '28g', '~₹30'],
            ['Mid-Morning', 'Dahi + banana', '10g', '~₹20'],
            ['Lunch', '100g soya chunks + 200g rice + sabzi', '32g', '~₹40'],
            ['Evening', 'Chana + roasted makhana', '15g', '~₹25'],
            ['Dinner', '100g chicken + dal + 2 roti', '40g', '~₹70'],
            ['Total', '', '125g protein', '~₹185'],
        ], widths=[80, 200, 70, 70])
    co(story, s, 'Indian protein sources are among the most cost-effective in the world. Soya chunks provide 25g protein per 50g dry weight at approximately ₹15–20 — cheaper than most supplements per gram of protein.')
    story.append(Paragraph('Carbohydrate Sources for Indian Athletes', s['SecHead']))
    tb(story,
        ['Food', 'Serving', 'Carbs', 'GI', 'Best Timing'],
        [
            ['White rice', '150g cooked', '45g', '73 (High)', 'Post-workout'],
            ['Brown rice', '150g cooked', '40g', '50 (Med)', 'Any meal'],
            ['Chapati (wheat)', '1 medium (35g)', '18g', '55 (Med)', 'Any meal'],
            ['Oats', '80g dry', '55g', '55 (Med)', 'Breakfast / pre-workout'],
            ['Banana', '1 medium', '27g', '51 (Med)', 'Pre/post workout'],
            ['Sweet potato', '150g cooked', '35g', '44 (Low)', 'Pre-workout / dinner'],
            ['Quinoa', '150g cooked', '34g', '53 (Med)', 'Lunch / dinner'],
        ], widths=[90, 80, 55, 60, 120])
    story.append(PageBreak())

    # ── CH6 ──
    story.append(Paragraph('CHAPTER 6 — SUPPLEMENT GUIDE — RANKED BY EVIDENCE', s['ChHead']))
    hr(story)
    story.append(Paragraph('Tier 1 — Strong Evidence (Use These)', s['SecHead']))
    tb(story,
        ['Supplement', 'Dose', 'Timing', 'Mechanism', 'Evidence Grade'],
        [
            ['Creatine Monohydrate', '5g/day', 'Any time (consistency matters)', 'Replenishes PCr, cellular hydration', 'A (500+ RCTs)'],
            ['Whey Protein', '25–50g/day', 'Post-workout priority', 'High leucine, fast absorption', 'A'],
            ['Caffeine', '3–6mg/kg', '45 min pre-workout', 'Adenosine antagonism, CNS stimulation', 'A'],
            ['Vitamin D3', '2000–5000 IU/day', 'With a fatty meal', 'Testosterone cofactor, bone health', 'A'],
            ['Magnesium Glycinate', '300–400mg', 'Before bed', 'Sleep quality, testosterone, >300 enzymes', 'A'],
        ], widths=[90, 70, 100, 130, 80])
    story.append(Paragraph('Tier 2 — Moderate Evidence (Consider)', s['SecHead']))
    tb(story,
        ['Supplement', 'Dose', 'Benefit', 'Notes'],
        [
            ['Beta-Alanine', '3.2g/day', 'Reduces fatigue in 8–15 rep range', 'Tingling (paresthesia) is harmless'],
            ['Citrulline Malate', '6–8g pre', 'Better pump, reduces DOMS by ~40%', 'Underrated, very affordable'],
            ['Ashwagandha KSM-66', '600mg/day', '↓ Cortisol 28%, ↑ T 15–17%', 'Indian adaptogen — widely available'],
            ['Omega-3 Fish Oil', '3g EPA+DHA', 'Reduces inflammation, faster recovery', 'Vegans: algae-based alternative'],
            ['Zinc', '15–30mg/day', 'Testosterone synthesis cofactor', 'Supplement only if deficient (test first)'],
            ['Collagen + Vit C', '15g + 500mg pre-workout', 'Tendon/ligament synthesis', 'Take 60 min before training'],
        ], widths=[100, 80, 160, 130])
    story.append(Paragraph('Tier 3 — No/Weak Evidence (Skip)', s['SecHead']))
    bl(story, s, [
        'BCAAs (if protein adequate): Isolated BCAAs add nothing when total daily protein is sufficient (1.8g/kg+).',
        'Most commercial "testosterone boosters": Studies show negligible effect on actual serum testosterone.',
        'Weight gainers: 90% simple carbohydrates. Better to eat rice. Same effect, 10× cheaper.',
        'Glutamine: Effective post-surgery. Useless for healthy, adequately-nourished athletes.',
        'CLA: Modest fat loss (−0.1kg/week maximum). Not worth the cost or marketing claims.',
        'Nitric oxide boosters (most): Citrulline (Tier 2) is the exception — most others are ineffective.',
    ])
    co(story, s, 'Budget Power Stack (₹1,500/month): Creatine monohydrate ₹400 + Vitamin D3 ₹150 + Magnesium ₹200 + Ashwagandha ₹250 + Whey protein from food = outperforms 90% of expensive stacks.')
    story.append(PageBreak())

    # ── CH7 ──
    story.append(Paragraph('CHAPTER 7 — RECOVERY, SLEEP & CORTISOL MANAGEMENT', s['ChHead']))
    hr(story)
    story.append(Paragraph('Sleep Architecture & Muscle Growth', s['SecHead']))
    story.append(Paragraph(
        'Muscle tissue is built during sleep, not during training. Stage 3 NREM (deep sleep) is when 60–70% of daily Growth Hormone '
        'is released — the pulse responsible for tissue repair, protein synthesis, and fat mobilisation. REM sleep consolidates motor learning, '
        'making new movement patterns automatic. Both stages are essential for athletes.', s['Body']))
    tb(story,
        ['Sleep Variable', 'Optimal', 'When Compromised', 'Fix'],
        [
            ['Duration', '7.5–9 hours', '−23% T, −31% IGF-1 at 6h', 'Prioritise sleep over morning cardio'],
            ['Room temp', '16–19°C', '>22°C disrupts deep sleep', 'Fan / AC + blackout curtains'],
            ['Light', 'Complete darkness', 'Blue light delays melatonin 90 min', 'No screens 60 min before bed'],
            ['Consistency', '±30 min same time', 'Irregular = 25% worse quality', 'Set sleep/wake alarms'],
            ['Pre-sleep food', 'Protein, low sugar', 'High sugar disrupts NREM stage 3', 'Paneer/dahi 90 min before bed'],
        ], widths=[90, 80, 130, 130])
    story.append(Paragraph('Active Recovery Protocols', s['SecHead']))
    bl(story, s, [
        'Contrast showers (3 min hot / 1 min cold × 3 cycles): Reduces DOMS by 30–40%, improves parasympathetic tone.',
        'Light walking (20–30 min on rest days): Promotes blood flow and nutrient delivery without adding training stress.',
        'Foam rolling / myofascial release: Reduces perceived soreness and improves ROM acutely. 30–60 sec per muscle.',
        'Pranayama — 4-7-8 breathing: Activates parasympathetic nervous system, reduces cortisol measurably within 10 minutes.',
        'Epsom salt bath (optional): Transdermal magnesium absorption + heat-induced muscle relaxation.',
    ])
    story.append(Paragraph('Heart Rate Variability (HRV) — Your Recovery Gauge', s['SecHead']))
    story.append(Paragraph(
        'HRV is the variation in time between consecutive heartbeats — a direct measure of autonomic nervous system balance. '
        'High HRV = good recovery, parasympathetic dominance. Low HRV = accumulated fatigue, sympathetic overload. '
        'Measure HRV with a fitness tracker (Garmin, Whoop, or free apps like Elite HRV) first thing every morning. '
        'If HRV is trending down across 3+ days: reduce volume by 30%, prioritise sleep, increase food intake.', s['Body']))
    story.append(PageBreak())

    # ── CH8 ──
    story.append(Paragraph('CHAPTER 8 — ADVANCED TRAINING TECHNIQUES', s['ChHead']))
    hr(story)
    story.append(Paragraph('When Advanced Techniques Are Appropriate', s['SecHead']))
    story.append(Paragraph(
        'Advanced training techniques are tools for intermediate and advanced athletes (12+ months) who have plateaued on straight-set '
        'programming. Beginners extract more benefit from adding weight and reps to basic movements. These techniques extend training volume '
        'beyond what straight sets allow — increasing mechanical tension and metabolic stress in the same or less time.', s['Body']))
    tb(story,
        ['Technique', 'Mechanism', 'Best Exercises', 'When to Use'],
        [
            ['Drop sets', 'Extends time under tension past failure', 'Curls, laterals, pushdowns', 'Final 1–2 sets per session'],
            ['Supersets (antagonist)', 'Reciprocal inhibition potentiation', 'Bi/Tri, Back/Chest pairs', 'Throughout workout'],
            ['Giant sets', 'Metabolic overload, time efficiency', '3–4 isolation exercises', 'Finisher at end of workout'],
            ['Cluster sets', 'High load at sub-maximal fatigue', 'Deadlift, squat, bench', 'Intensification phases'],
            ['Rest-pause', 'Extend set past normal failure', 'Any isolation exercise', 'Advanced, intermediate+'],
            ['Mechanical drop', 'Biomechanical advantage as fatigue rises', 'DB lateral → front raise', 'Advanced athletes'],
            ['Pre-exhaustion', 'Fatigue prime mover via isolation first', 'Cable fly → bench press', 'Chest specialisation'],
            ['Blood flow restriction', 'Metabolic stress at low loads', 'Arms, calves', 'Injury rehab or volume add'],
        ], widths=[90, 130, 130, 110])
    co(story, s, 'Rule of Thumb: Never use advanced techniques as a substitute for progressive overload on the basics. Fancy techniques on top of a weak foundation produce minimal results.')
    story.append(PageBreak())

    # ── CH9 ──
    story.append(Paragraph('CHAPTER 9 — FULL 12-WEEK ANABOLIC TRANSFORMATION PROGRAM', s['ChHead']))
    hr(story)
    story.append(Paragraph('Program Philosophy & Structure', s['SecHead']))
    story.append(Paragraph(
        'This 12-week program is built on a Push/Pull/Legs (PPL) split running 5–6 days per week, with planned deload weeks '
        'and three progressive phases. The program is appropriate for intermediate athletes (12+ months consistent training) '
        'with solid technique on all compound movements. Beginners should run a linear 3-day full-body programme for the first '
        '6 months before transitioning to PPL.', s['Body']))
    tb(story,
        ['Phase', 'Weeks', 'Focus', 'Rep Ranges', 'Sets/Muscle/Week', 'RIR Target'],
        [
            ['Accumulation', '1–4', 'Build volume tolerance', '10–15', '10–14', '3–4'],
            ['Intensification', '5–8', 'Strength + hypertrophy', '6–10', '14–18', '1–2'],
            ['Deload', '9', 'Recovery', 'Any', '50% reduction', '4–5'],
            ['Peaking', '10–12', 'Max intensity', '4–8', '16–20', '0–1'],
        ], widths=[80, 50, 110, 70, 90, 70])
    story.append(Paragraph('Weekly Schedule', s['SecHead']))
    tb(story,
        ['Day', 'Session', 'Muscles Trained', 'Duration'],
        [
            ['Monday', 'Push A — Chest dominant', 'Chest, front delts, triceps', '60–70 min'],
            ['Tuesday', 'Pull A — Back width', 'Lats, upper back, rear delts, biceps', '65–75 min'],
            ['Wednesday', 'Legs A — Quad dominant', 'Quads, hamstrings, glutes, calves', '70–80 min'],
            ['Thursday', 'Push B — Shoulder dominant', 'Delts, chest secondary, triceps', '55–65 min'],
            ['Friday', 'Pull B — Back thickness + Arms', 'Mid/lower back, biceps + triceps', '60–70 min'],
            ['Saturday', 'Legs B — Posterior chain', 'Hamstrings, glutes, quad secondary', '65–75 min'],
            ['Sunday', 'Rest / Active Recovery', 'Walking, mobility, pranayama', '20–30 min'],
        ], widths=[60, 100, 170, 80])
    story.append(Paragraph('Push Day A — Weeks 1–4 (Accumulation)', s['SecHead']))
    tb(story,
        ['#', 'Exercise', 'Sets', 'Reps', 'Rest', 'Tempo', 'Notes'],
        [
            ['A1', 'Barbell Bench Press', '4', '12', '2 min', '3-0-1', 'Controlled descent'],
            ['A2', 'Incline DB Press', '3', '12', '90s', '3-0-1', 'Full stretch at bottom'],
            ['B1', 'Cable Crossover (low)', '3', '15', '60s', '2-1-1', 'Squeeze at peak'],
            ['C1', 'Seated DB OHP', '4', '12', '90s', '3-0-1', 'Full ROM, no arch'],
            ['C2', 'Cable Lateral Raise', '4', '15', '60s', '2-1-1', 'Elbow height'],
            ['D1', 'Tricep Pushdown (rope)', '3', '15', '60s', '2-1-1', 'Lock out fully'],
            ['D2', 'Overhead Tricep Ext.', '3', '12', '60s', '3-0-1', 'Full stretch'],
        ], widths=[20, 120, 35, 35, 40, 50, 140])
    story.append(Paragraph('Pull Day A — Weeks 1–4 (Accumulation)', s['SecHead']))
    tb(story,
        ['#', 'Exercise', 'Sets', 'Reps', 'Rest', 'Notes'],
        [
            ['A1', 'Pull-ups / Lat Pulldown', '4', '10–12', '2 min', 'Full hang to full flex'],
            ['A2', 'Barbell / DB Row', '4', '10', '90s', 'Chest supported reduces cheating'],
            ['B1', 'Seated Cable Row (wide)', '3', '12', '90s', 'Drive elbows back, squeeze'],
            ['B2', 'Face Pull (rope)', '4', '15', '60s', 'External rotation at end'],
            ['C1', 'Rear Delt Fly (cable)', '3', '15', '60s', 'Elbow-out, squeeze at rear'],
            ['D1', 'Barbell Curl', '3', '12', '60s', 'Full ROM, no swing'],
            ['D2', 'Incline DB Curl', '3', '12', '60s', 'Lengthened bicep position'],
        ], widths=[20, 135, 35, 45, 45, 160])
    story.append(Paragraph('Legs Day A — Weeks 1–4 (Accumulation)', s['SecHead']))
    tb(story,
        ['#', 'Exercise', 'Sets', 'Reps', 'Rest', 'Notes'],
        [
            ['A1', 'Barbell Back Squat', '4', '10', '2.5 min', 'Hip crease below parallel'],
            ['A2', 'Romanian Deadlift', '3', '12', '2 min', 'Feel hamstring stretch at bottom'],
            ['B1', 'Leg Press', '4', '15', '90s', 'Full ROM, no knee cave'],
            ['B2', 'Leg Curl (seated)', '4', '12', '90s', 'Pause at peak flex'],
            ['C1', 'Bulgarian Split Squat', '3', '12/leg', '90s', 'Front foot out, torso upright'],
            ['D1', 'Standing Calf Raise', '5', '15', '60s', 'Full ROM — heel drop essential'],
        ], widths=[20, 135, 35, 45, 60, 165])
    story.append(PageBreak())

    # ── CH10 ──
    story.append(Paragraph('CHAPTER 10 — COMPLETE WEEKLY WORKOUT LIBRARY', s['ChHead']))
    hr(story)
    story.append(Paragraph('Push Day B (Shoulder Dominant) — All Phases', s['SecHead']))
    tb(story,
        ['#', 'Exercise', 'Sets', 'Reps', 'Notes'],
        [
            ['A1', 'Seated Barbell OHP', '4', '8–10', 'Heavy. Full lock-out at top.'],
            ['A2', 'DB Arnold Press', '3', '12', 'Rotation maximises all three delt heads'],
            ['B1', 'DB Lateral Raise', '5', '15', '5 sets — delts respond to volume'],
            ['B2', 'Cable Upright Row', '3', '12', 'Elbows flare above shoulders'],
            ['C1', 'Incline DB Press', '4', '12', 'Shoulder-width grip, full stretch'],
            ['D1', 'Skull Crushers', '4', '12', 'EZ bar, controlled descent'],
            ['D2', 'Close-Grip Bench Press', '3', '10', 'Compound tricep finisher'],
        ], widths=[20, 130, 35, 45, 220])
    story.append(Paragraph('Pull Day B (Thickness + Arms Dominant) — All Phases', s['SecHead']))
    tb(story,
        ['#', 'Exercise', 'Sets', 'Reps', 'Notes'],
        [
            ['A1', 'Barbell Deadlift (conventional)', '4', '6', 'King of mass. Brace hard.'],
            ['A2', 'T-Bar Row / Chest-Supported Row', '4', '10', 'Middle back thickness'],
            ['B1', 'Single-Arm DB Row', '3', '12', 'Full stretch at bottom, full retraction'],
            ['B2', 'Straight-Arm Lat Pulldown', '3', '15', 'Isolates lats — no elbow bend'],
            ['C1', 'EZ Bar Curl', '4', '12', 'Supinated at top, full stretch at bottom'],
            ['C2', 'Hammer Curl', '3', '12', 'Brachialis + brachioradialis'],
            ['D1', 'Tricep Pushdown (straight bar)', '4', '15', 'Keep elbows pinned'],
            ['D2', 'Single-Arm Overhead Ext.', '3', '12', 'Long head emphasis'],
        ], widths=[20, 155, 35, 40, 200])
    story.append(Paragraph('Legs Day B (Posterior Chain Dominant) — All Phases', s['SecHead']))
    tb(story,
        ['#', 'Exercise', 'Sets', 'Reps', 'Notes'],
        [
            ['A1', 'Romanian Deadlift', '4', '10', 'Primary hamstring/glute builder'],
            ['A2', 'Leg Curl (lying)', '4', '12', 'Pause 1 sec at peak flexion'],
            ['B1', 'Hip Thrust (barbell)', '4', '12', 'Glute maximiser — drive hips to ceiling'],
            ['B2', 'Sumo Deadlift or Leg Press', '3', '12', 'High-and-wide foot position'],
            ['C1', 'Walking Lunges', '3', '20 steps', 'Quad + glute combination'],
            ['C2', 'Adductor Machine', '3', '15', 'Inner thigh stability'],
            ['D1', 'Seated Calf Raise', '5', '15', 'Soleus — needs 130°+ knee bend to activate'],
        ], widths=[20, 130, 35, 50, 215])
    story.append(Paragraph('Intensification Phase Adjustments (Weeks 5–8)', s['SecHead']))
    story.append(Paragraph(
        'In weeks 5–8, apply the following modifications to all sessions from the Accumulation phase:\n'
        '— Reduce all rep ranges by 3–4 reps (e.g., 12 reps → 8–9 reps)\n'
        '— Increase load by 7.5–12.5% from week 4 end weights\n'
        '— Increase rest periods by 30 seconds for compound lifts\n'
        '— Reduce isolation exercise volume by 1 set each\n'
        '— Add 1 heavy back-off set at end of each compound movement', s['Body']))
    story.append(Paragraph('Peaking Phase Adjustments (Weeks 10–12)', s['SecHead']))
    story.append(Paragraph(
        'Post-deload peaking phase focuses on maximising intensity (RIR 0–1) while managing volume to avoid accumulating excessive fatigue.\n'
        '— Reduce rep ranges further (4–8 reps on main compounds)\n'
        '— Work at 85–92% of 1RM on key lifts\n'
        '— Focus on compound movements; reduce isolation work\n'
        '— Take body measurements and progress photos at weeks 4, 8, and 12\n'
        '— Use week 12 weights as new baseline for next programme cycle', s['Body']))
    story.append(PageBreak())

    # ── CH11 ──
    story.append(Paragraph('CHAPTER 11 — INDIAN DIET TEMPLATES & MACRO BLUEPRINTS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Template A — 70kg Male, Lean Bulk (2,800 kcal)', s['SecHead']))
    tb(story,
        ['Meal', 'Time', 'Foods', 'P', 'C', 'F', 'kcal'],
        [
            ['Breakfast', '7:30 AM', '4 eggs + 2 roti + dahi (200g)', '36g', '42g', '18g', '476'],
            ['Mid-Morning', '10:30 AM', 'Banana + 20 almonds + 200ml milk', '10g', '38g', '12g', '298'],
            ['Lunch', '1:00 PM', '150g chicken + 200g rice + dal + sabzi', '46g', '72g', '10g', '562'],
            ['Pre-WO', '4:00 PM', 'Oats 80g + 1 banana + whey 25g', '32g', '60g', '6g', '426'],
            ['Post-WO', '7:00 PM', '150g chicken + 180g rice + salad', '46g', '65g', '8g', '520'],
            ['Dinner', '9:30 PM', '100g paneer + 2 roti + sabzi + dahi', '28g', '32g', '14g', '362'],
        ], widths=[55, 55, 175, 25, 25, 25, 40])
    story.append(Paragraph('Total: 2,644 kcal | 198g P | 309g C | 68g F', s['Callout']))
    story.append(Paragraph('Template B — 60kg Female, Fat Loss (1,700 kcal)', s['SecHead']))
    tb(story,
        ['Meal', 'Time', 'Foods', 'P', 'C', 'F', 'kcal'],
        [
            ['Breakfast', '7:00 AM', '3 egg whites + 1 egg + 1 roti + green tea', '23g', '18g', '7g', '227'],
            ['Lunch', '12:30 PM', '130g chicken + 100g rice + dal + sabzi', '36g', '42g', '7g', '375'],
            ['Evening', '4:30 PM', 'Greek dahi 200g + cucumber + 10 almonds', '16g', '12g', '9g', '189'],
            ['Dinner', '7:30 PM', '100g paneer + sabzi + 1 roti + salad', '22g', '22g', '12g', '284'],
            ['Pre-Sleep', '9:30 PM', '200ml warm milk + 5 walnuts', '10g', '12g', '9g', '169'],
        ], widths=[55, 55, 195, 25, 25, 25, 40])
    story.append(Paragraph('Total: 1,244 kcal sample — scale portions to reach 1,600–1,800 kcal target', s['Callout']))
    story.append(Paragraph('Template C — 80kg Male, Vegetarian Bulk (3,000 kcal)', s['SecHead']))
    tb(story,
        ['Meal', 'Time', 'Foods', 'P', 'C', 'F', 'kcal'],
        [
            ['Breakfast', '7:30 AM', 'Paneer bhurji 200g + 3 roti + dahi 150g', '44g', '48g', '22g', '572'],
            ['Mid-Morning', '10:30 AM', 'Soya chunks (50g dry) curry + 100g rice', '30g', '42g', '5g', '333'],
            ['Lunch', '1:00 PM', 'Moong dal 200g + 200g rice + sabzi', '28g', '82g', '7g', '507'],
            ['Pre-WO', '4:00 PM', 'Whey 30g + banana + oats 60g', '30g', '58g', '5g', '401'],
            ['Post-WO', '7:00 PM', 'Paneer 150g + 200g rice + salad', '32g', '65g', '14g', '518'],
            ['Dinner', '9:30 PM', 'Chana dal 200g + 2 roti + curd', '28g', '55g', '10g', '426'],
        ], widths=[55, 55, 195, 25, 25, 25, 40])
    story.append(Paragraph('Total: 2,757 kcal | 192g P | 350g C | 63g F — scale rice/roti to reach 3,000 kcal', s['Callout']))
    story.append(Paragraph('Keto Template — 75kg Male, Fat Loss (2,200 kcal, Keto)', s['SecHead']))
    tb(story,
        ['Meal', 'Time', 'Foods', 'P', 'C', 'F', 'kcal'],
        [
            ['Breakfast', '8:00 AM', '4 eggs fried in ghee + spinach sauté', '24g', '3g', '28g', '368'],
            ['Lunch', '1:00 PM', '200g chicken thigh + greens + avocado', '44g', '8g', '32g', '492'],
            ['Evening', '4:30 PM', '50g walnuts + 30g paneer', '10g', '4g', '22g', '254'],
            ['Dinner', '7:30 PM', '200g mutton + cauliflower sabzi + raita', '48g', '12g', '30g', '506'],
        ], widths=[55, 55, 215, 25, 25, 25, 40])
    story.append(Paragraph('Total: 1,620 kcal sample — add fat sources (ghee, coconut oil, nuts) to reach 2,200 kcal', s['Callout']))
    story.append(PageBreak())

    # ── CH12 ──
    story.append(Paragraph('CHAPTER 12 — INJURY PREVENTION, JOINT HEALTH & LONGEVITY', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Longevity Principle', s['SecHead']))
    story.append(Paragraph(
        'The athlete who trains consistently for 5 years will always outperform the athlete who trains harder for 2 years before getting injured. '
        'Injury prevention is not passive maintenance — it is an active, ongoing investment in the machinery that allows you to train. '
        'Most injuries in Indian gym athletes are predictable failures of progressive overload, technique, or recovery management.', s['Body']))
    tb(story,
        ['Injury', 'Root Cause', 'Prevention', 'If It Occurs'],
        [
            ['Lower back pain', 'Poor hip hinge, excessive lumbar load', 'Hip hinge drills, RDL technique, brace always', 'Reduce load, McGill Big 3 rehab'],
            ['Rotator cuff strain', 'Internal rotation imbalance, poor shoulder mechanics', 'Band pull-aparts 3×20 daily, face pulls, external rotation work', 'Reduce pressing, add rotator cuff rehab'],
            ['Patellar knee pain', 'Quad dominance, poor ankle mobility', 'VMO work, foam rolling IT band, ankle mobility', 'Box squats, reduce depth temporarily'],
            ['Bicep tendinopathy', 'Excessive curl load with poor technique', 'Eccentric curls, reduce load', 'Ice, reduce supinated grip work'],
            ['Tennis elbow', 'Excessive grip-heavy exercises', 'Wrist extensor stretches, reduce grip volume', 'Ice, 2-week deload from pulling'],
        ], widths=[80, 100, 140, 130])
    story.append(Paragraph('Warm-Up Protocol (12 Minutes)', s['SecHead']))
    tb(story,
        ['Duration', 'Activity', 'Purpose'],
        [
            ['3 min', 'Light cardio (skip rope / bike)', 'Raise core temperature 1–2°C'],
            ['2 min', 'Dynamic stretching (leg swings, arm circles)', 'Mobilise joints through ROM'],
            ['2 min', 'Activation (glute bridges, band work)', 'Prime target muscles'],
            ['3–4 min', 'Progressive warm-up sets (40% / 60% / 80%)', 'Neural preparation for working weights'],
        ], widths=[60, 200, 180])
    story.append(Paragraph('Joint Nutrition Protocol', s['SecHead']))
    tb(story,
        ['Nutrient', 'Dose', 'Source', 'Primary Benefit'],
        [
            ['Collagen peptides', '15–20g/day', 'Supplement', 'Tendon and cartilage repair'],
            ['Omega-3 (EPA+DHA)', '3g/day', 'Fish oil / fatty fish', 'Reduce joint inflammation'],
            ['Vitamin C', '500–1000mg/day', 'Amla, guava, supplement', 'Collagen synthesis cofactor'],
            ['Curcumin + piperine', '500–1000mg/day', 'Haldi + black pepper', 'Potent anti-inflammatory'],
            ['Glucosamine', '1500mg/day', 'Supplement', 'Moderate evidence for joint comfort'],
        ], widths=[90, 80, 120, 160])
    co(story, s, 'Lifetime Rule: A 10% reduction in training ego produces a 1000% better outcome across a 10-year athletic career. Train hard, recover harder, and stay injury-free above all else.')
    story.append(PageBreak())

    # ── APPENDIX A — GLOSSARY ──
    story.append(Paragraph('APPENDIX A — GLOSSARY OF KEY TERMS', s['ChHead']))
    hr(story)
    glossary = [
        ('1RM (One-Rep Max)', 'The maximum weight you can lift for exactly one repetition with full control.'),
        ('Anabolic', 'Describes a state or process that promotes tissue building, especially muscle.'),
        ('Catabolism', 'The breakdown of muscle tissue for energy — opposite of anabolism.'),
        ('DOMS', 'Delayed Onset Muscle Soreness — muscle soreness 24–72h post-training. Normal adaptation signal.'),
        ('FFMI (Fat-Free Mass Index)', 'A body composition metric accounting for lean mass relative to height. Max natural FFMI ≈ 25.'),
        ('GH (Growth Hormone)', 'Pituitary hormone that stimulates IGF-1 production, fat oxidation, and tissue repair.'),
        ('Hypertrophy', 'Increase in muscle fibre size (cross-sectional area) — the primary goal of bodybuilding.'),
        ('IGF-1', 'Insulin-like Growth Factor 1 — produced in the liver, mediates most of GH\'s anabolic effects.'),
        ('mTOR', 'Mammalian Target of Rapamycin — the master regulator of muscle protein synthesis. Activated by leucine and mechanical tension.'),
        ('MPS (Muscle Protein Synthesis)', 'The rate of protein incorporation into muscle tissue. Training and leucine are the primary drivers.'),
        ('MPB (Muscle Protein Breakdown)', 'The rate of muscle protein degradation. Elevated by cortisol, fasting, and insufficient protein.'),
        ('PCr (Phosphocreatine)', 'The primary energy currency for maximal efforts lasting 1–10 seconds. Replenished by creatine supplementation.'),
        ('Progressive Overload', 'The systematic increase of training demands over time to force continued adaptation.'),
        ('RIR (Reps In Reserve)', 'The number of reps remaining before technical failure. RIR 2 = could do 2 more reps.'),
        ('Satellite Cells', 'Muscle stem cells that activate upon damage to repair and grow muscle fibres by donating nuclei.'),
        ('TDEE (Total Daily Energy Expenditure)', 'Total calories burned in a day including BMR + activity. Your calorie maintenance level.'),
        ('Time Under Tension', 'Total duration a muscle is under load during a set. Influences mechanical tension and metabolic stress.'),
    ]
    for term, defn in glossary:
        story.append(Paragraph(f'<b>{term}</b>: {defn}', s['Body']))

    story.append(PageBreak())

    # ── APPENDIX B — FAQ ──
    story.append(Paragraph('APPENDIX B — FREQUENTLY ASKED QUESTIONS', s['ChHead']))
    hr(story)
    faqs = [
        ('Q: How long before I see visible results?',
         'A: Beginners typically notice strength gains within 2 weeks (neural adaptations) and visible muscle changes within 8–12 weeks of consistent training + adequate nutrition. Body fat reduction becomes visible at approximately 1–1.5kg/month of consistent deficit.'),
        ('Q: Should I train on an empty stomach for fat loss?',
         'A: Fasted cardio burns slightly more fat in the session but produces equivalent fat loss to fed training over 24 hours (total daily energy balance determines fat loss, not session-level substrate utilisation). For resistance training specifically: training in a fed state preserves more muscle. Eat before lifting.'),
        ('Q: Is creatine safe for Indian athletes?',
         'A: Yes. Creatine monohydrate is the most extensively studied supplement in history (500+ RCTs over 30 years). No evidence of harm in healthy athletes at 3–5g/day. The "creatine damages kidneys" myth applies only to individuals with pre-existing kidney disease.'),
        ('Q: How much protein can the body absorb per meal?',
         'A: The old "30g limit" is a myth. The body absorbs all protein eaten — the question is the rate of MPS stimulation. Each meal needs ≥3g leucine (≈30g complete protein) to maximally trigger mTOR. Additional protein at a meal is still used — absorbed more slowly and used for non-muscle functions.'),
        ('Q: I cannot afford whey protein — can I still build muscle?',
         'A: Absolutely. Indian food provides excellent complete protein: eggs, chicken, paneer, soya chunks, and dal are all superior to or equivalent to whey for building muscle when consumed in sufficient quantity. Whey is convenient, not essential.'),
        ('Q: Should women follow this programme?',
         'A: Yes, with modifications. Women build muscle via identical mechanisms to men. Rep ranges, volume, and progressive overload principles apply identically. Women should use the same programme structure with appropriate loads. The primary adjustment: women benefit from slightly higher rep ranges (10–15 primary) and may recover faster, enabling higher frequency.'),
        ('Q: Is it possible to build muscle and lose fat simultaneously?',
         'A: Yes — especially for beginners, detrained athletes, and those with higher body fat (>20% for men, >28% for women). This "body recomposition" slows as athletes become more trained and leaner. At TDEE with high protein (2.2g/kg), trained athletes can slowly recomp. True simultaneous mass gain + fat loss at an advanced level requires very precise execution.'),
        ('Q: How do I know if I\'m overtraining?',
         'A: Persistent fatigue despite adequate sleep, declining performance across multiple sessions, mood changes (irritability, apathy), elevated resting heart rate, sleep disturbances, and recurring minor injuries. True overtraining is rare — most athletes experience "overreaching" which resolves with 1–2 weeks of reduced volume. Address with deload, increased food, and sleep before reducing training long-term.'),
    ]
    for q, a in faqs:
        story.append(Paragraph(q, s['SecHead']))
        story.append(Paragraph(a, s['Body']))

    # ── FINAL PAGE ──
    story.append(PageBreak())
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB', s['Cover3']))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('BUILD YOUR BEAST', s['Cover1']))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('Your transformation starts today. Apply one principle from each chapter this week.', s['Cover3']))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='60%', thickness=1, color=RED, spaceAfter=8))
    story.append(Paragraph('© Royal Fitness Club — All rights reserved.', s['Cover3']))

    doc.build(story)
    from PyPDF2 import PdfReader
    count = len(PdfReader(path).pages)
    print(f'✅ Anabolic Full Guide: {count} pages')

build_extended_anabolic()

# That was a test run. Now check page count needs and plan additions.
