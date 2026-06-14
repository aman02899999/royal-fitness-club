"""Generate 60+ page flagship PDFs for Royal Fitness Club."""
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
DARK = colors.HexColor('#0d0d0d')
GOLD = colors.HexColor('#ffd000')
GREY = colors.HexColor('#888888')
LGREY = colors.HexColor('#cccccc')
WHITE = colors.white

W, H = A4

def base_styles():
    s = getSampleStyleSheet()
    def add(name, **kw):
        if name in s:
            s[name].__dict__.update(kw)
        else:
            s.add(ParagraphStyle(name=name, **kw))
    add('Cover1', fontName='Helvetica-Bold', fontSize=36, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=6, leading=44)
    add('Cover2', fontName='Helvetica-Bold', fontSize=18, textColor=GOLD,
        alignment=TA_CENTER, spaceAfter=4, leading=24)
    add('Cover3', fontName='Helvetica', fontSize=11, textColor=LGREY,
        alignment=TA_CENTER, spaceAfter=6, leading=16)
    add('ChHead', fontName='Helvetica-Bold', fontSize=16, textColor=RED,
        spaceBefore=14, spaceAfter=8, leading=22)
    add('SecHead', fontName='Helvetica-Bold', fontSize=13, textColor=WHITE,
        spaceBefore=10, spaceAfter=5, leading=18)
    add('Body', fontName='Helvetica', fontSize=10, textColor=LGREY,
        spaceAfter=6, leading=16, alignment=TA_JUSTIFY)
    add('Bullet', fontName='Helvetica', fontSize=10, textColor=LGREY,
        spaceAfter=4, leading=15, leftIndent=14, firstLineIndent=-10)
    add('TableHdr', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE,
        alignment=TA_CENTER)
    add('Callout', fontName='Helvetica-BoldOblique', fontSize=11,
        textColor=GOLD, spaceBefore=8, spaceAfter=8, leading=18,
        leftIndent=12, rightIndent=12, alignment=TA_JUSTIFY)
    add('TOCItem', fontName='Helvetica', fontSize=10, textColor=LGREY,
        spaceAfter=3, leading=15)
    add('Footer', fontName='Helvetica', fontSize=8, textColor=GREY,
        alignment=TA_CENTER)
    return s

def cover_page(story, s, title, subtitle, chapters, pages, edition):
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB', s['Cover3']))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(title, s['Cover1']))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(subtitle, s['Cover2']))
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width='80%', thickness=1, color=RED, spaceAfter=10))
    story.append(Paragraph(f'{chapters} Chapters  ·  {pages}+ Pages  ·  {edition}', s['Cover3']))
    story.append(Paragraph('By Royal Fitness Club Expert Team', s['Cover3']))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='40%', thickness=1, color=GOLD))
    story.append(PageBreak())

def disclaimer(story, s):
    story.append(Paragraph('MEDICAL DISCLAIMER', s['ChHead']))
    story.append(Paragraph(
        'This guide is for educational and informational purposes only. It does not constitute medical advice, '
        'diagnosis, or treatment. Always consult a qualified medical professional before beginning any training, '
        'nutrition, or supplementation programme. Individual results vary based on genetics, consistency, '
        'starting condition, and adherence. Royal Fitness Club and its authors accept no liability for any '
        'injury, health issue, or loss arising from use of the information in this guide.', s['Body']))
    story.append(Spacer(1, 6*mm))

def toc(story, s, items):
    story.append(Paragraph('TABLE OF CONTENTS', s['ChHead']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=RED, spaceAfter=8))
    for ch, title, pg in items:
        story.append(Paragraph(f'Chapter {ch} — {title} {"·" * max(1, 55-len(title)-len(str(pg)))} {pg}', s['TOCItem']))
    story.append(PageBreak())

def hr(story):
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#333333'), spaceBefore=6, spaceAfter=6))

def callout(story, s, text):
    story.append(Paragraph(f'💡 {text}', s['Callout']))

def bullet(story, s, items):
    for item in items:
        story.append(Paragraph(f'• {item}', s['Bullet']))

def table(story, headers, rows, col_widths=None):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RED),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#1a1a1a'), colors.HexColor('#111111')]),
        ('TEXTCOLOR', (0,1), (-1,-1), LGREY),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#333333')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(table)
    story.append(Spacer(1, 4*mm))

def add_table(story, headers, rows, col_widths=None):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RED),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#1a1a1a'), colors.HexColor('#111111')]),
        ('TEXTCOLOR', (0,1), (-1,-1), LGREY),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#333333')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 4*mm))

# ─────────────────────────────────────────────────────────────────────────────
# ANABOLIC FULL GUIDE
# ─────────────────────────────────────────────────────────────────────────────
def build_anabolic():
    path = os.path.join(OUT, '00_Anabolic_Full_Guide.pdf')
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm)
    s = base_styles()
    story = []

    cover_page(story, s,
        'ANABOLIC FULL GUIDE',
        'Complete Muscle Building & Transformation Manual',
        10, 60, 'Indian Athletes Edition')

    disclaimer(story, s)
    story.append(PageBreak())

    toc(story, s, [
        (1, 'Muscle Building Fundamentals & Science', 5),
        (2, 'Anabolic Hormones & Natural Optimisation', 10),
        (3, 'Progressive Overload & Advanced Training', 16),
        (4, 'Nutrition Blueprints for Maximum Growth', 22),
        (5, 'Supplement Guide — What Actually Works', 29),
        (6, 'Recovery, Sleep & Cortisol Management', 35),
        (7, 'Advanced Techniques: Drops, Clusters, Supersets', 41),
        (8, 'Full 12-Week Anabolic Transformation Program', 46),
        (9, 'Indian Diet Templates & Macro Blueprints', 53),
        (10, 'Injury Prevention, Joint Health & Longevity', 58),
    ])

    # ── CHAPTER 1 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 1 — MUSCLE BUILDING FUNDAMENTALS & SCIENCE', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Three Mechanisms of Hypertrophy', s['SecHead']))
    story.append(Paragraph(
        'Muscle hypertrophy — the increase in muscle fibre cross-sectional area — occurs through three distinct but '
        'interconnected mechanisms. Understanding each mechanism allows you to structure training intelligently rather '
        'than randomly. Most gym-goers stimulate only one mechanism and wonder why they plateau.', s['Body']))
    bullet(story, s, [
        'Mechanical Tension: The primary driver of hypertrophy. When a muscle fibre is placed under load through its full range of motion, the tension on the sarcomere activates mechanosensors (integrins, focal adhesion kinase) that trigger the mTOR signalling cascade — the master regulator of muscle protein synthesis. Heavier compounds lifts, full ROM, and time under tension all maximise this mechanism.',
        'Metabolic Stress: The "pump" mechanism. Accumulation of lactate, hydrogen ions, and inorganic phosphate during high-rep training creates a cellular environment that increases anabolic hormone secretion locally, stimulates satellite cell activation, and produces cell swelling — all of which signal growth. Isolation exercises, moderate weight (12–20 reps), short rest periods (45–75 sec) maximise this.',
        'Muscle Damage: Eccentric-dominant loading causes micro-tears in the muscle fibre and connective tissue. Repair via satellite cell fusion results in thicker, stronger fibres. Too much damage = overtraining; the right amount = supercompensation. Novel exercises, slow eccentrics (3–4 seconds down), and training with full lengthened-position loading maximise this.',
    ])
    callout(story, s, 'Key Insight: Elite natural bodybuilders train all three mechanisms across their weekly programme — not just "lift heavy and go home".')
    story.append(Paragraph('Muscle Fibre Types & Training Implications', s['SecHead']))
    story.append(Paragraph(
        'Human skeletal muscle contains two primary fibre types — Type I (slow-twitch, oxidative, fatigue-resistant) '
        'and Type II (fast-twitch, glycolytic, high-force). Most muscles contain a mix, with the ratio varying by '
        'individual genetics and muscle function. The glutes and quads are typically more Type I; the triceps and '
        'calves more Type II. Both fibre types grow with resistance training — the key difference is their rep-range sensitivity.', s['Body']))
    add_table(story,
        ['Fibre Type', 'Characteristics', 'Best Rep Range', 'Example Exercises'],
        [
            ['Type I', 'Endurance, fatigue-resistant, smaller', '15–30 reps', 'Cable flyes, leg press (high rep)'],
            ['Type II-A', 'Mix of strength & endurance', '8–15 reps', 'Bench press, rows, squats'],
            ['Type II-X', 'Max power, fatigues quickly', '1–6 reps', 'Deadlifts, heavy OHP, sprints'],
        ],
        col_widths=[50, 130, 80, 130])
    story.append(Paragraph('The Myo-Mechanical Model of Growth', s['SecHead']))
    story.append(Paragraph(
        'Research by Dr. Brad Schoenfeld (2010, 2017) consolidated decades of hypertrophy research into a unified '
        'model. The practical takeaway: volume (sets × reps × load) is the primary driver of growth over time. '
        'For natural athletes, 10–20 weekly hard sets per muscle group is the evidence-based sweet spot. Below 10 '
        'sets is insufficient stimulus; above 25 sets risks overtraining without proportional gain.', s['Body']))
    story.append(Paragraph('Satellite Cells & Muscle Memory', s['SecHead']))
    story.append(Paragraph(
        'Satellite cells are muscle stem cells that lie dormant between the sarcolemma and basal lamina. Training-induced '
        'damage activates them to proliferate, differentiate, and fuse with existing fibres — donating their nuclei. '
        'More nuclei = greater protein synthesis capacity = faster growth. This is the biological basis of "muscle memory": '
        'previously trained muscles retain nuclei even after detraining, allowing rapid regrowth when training resumes. '
        'For Indian athletes returning after a break: regaining lost muscle takes 30–50% less time than building it originally.', s['Body']))
    callout(story, s, 'Practical Rule: 1 hard set close to failure (within 2–3 reps of RIR 0) is worth approximately 3 "comfortable" sets. Train with intent — every set counts.')
    story.append(PageBreak())

    # ── CHAPTER 2 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 2 — ANABOLIC HORMONES & NATURAL OPTIMISATION', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Four Primary Anabolic Hormones', s['SecHead']))
    story.append(Paragraph(
        'Your hormonal environment sets the ceiling for natural muscle-building potential. The four primary anabolic '
        'hormones — Testosterone, Growth Hormone (GH), Insulin-like Growth Factor 1 (IGF-1), and Insulin — work in '
        'concert to regulate protein synthesis, satellite cell activation, fat oxidation, and glycogen storage. '
        'Every lifestyle choice either supports or suppresses these hormones.', s['Body']))
    story.append(Paragraph('Testosterone — The Master Anabolic Hormone', s['SecHead']))
    story.append(Paragraph(
        'Testosterone (T) is produced in Leydig cells of the testes in men (~95%) and in the adrenal glands in both sexes. '
        'Normal male range in India: 300–1000 ng/dL. Testosterone binds to androgen receptors (AR) in muscle cells, '
        'activating gene transcription for contractile proteins (actin, myosin). Higher androgen receptor density = '
        'better response to the same testosterone level. This receptor density is trainable — resistance training increases AR expression.', s['Body']))
    bullet(story, s, [
        'Natural T optimisation: Compound lifts (squat, deadlift, bench) trigger the largest acute T spike.',
        'Sleep 7–9 hours: 60–70% of daily testosterone is produced during slow-wave sleep. One week of 5-hour nights drops T by 10–15%.',
        'Body fat 10–18%: Adipose tissue converts testosterone to oestrogen via aromatase. Staying lean preserves your T.',
        'Zinc & Vitamin D: Both are rate-limiting cofactors for T synthesis. Indian diets are frequently deficient in both.',
        'Stress management: Cortisol is structurally derived from the same precursor as testosterone (pregnenolone). Chronically elevated cortisol "steals" pregnenolone — blunting T production.',
    ])
    story.append(Paragraph('Growth Hormone & IGF-1 Axis', s['SecHead']))
    story.append(Paragraph(
        'GH is released in pulses from the anterior pituitary, primarily during deep sleep (Stage 3 NREM) and in '
        'response to intense exercise. GH itself has modest direct anabolic effects; its primary action is to stimulate '
        'the liver and peripheral tissues to produce IGF-1 — the actual muscle-building signal. IGF-1 activates the '
        'PI3K/Akt/mTOR pathway — the same pathway activated by resistance training — making the two stimuli synergistic.', s['Body']))
    add_table(story,
        ['Factor', 'Effect on GH/IGF-1', 'Practical Action'],
        [
            ['Deep sleep', '↑↑↑ GH pulse amplitude', 'Prioritise 8h, dark room, no screens'],
            ['High-intensity training', '↑↑ acute GH release', 'Include sprint work or heavy compound sets'],
            ['Fasting (16h)', '↑↑ GH (3–5× baseline)', 'Intermittent fasting window'],
            ['Obesity/insulin resistance', '↓↓ GH pulse', 'Maintain healthy body fat'],
            ['Chronic stress', '↓ GH secretion', 'Stress management protocols'],
            ['Protein intake (adequate)', '↑ IGF-1 production', 'Maintain 1.6–2.2g/kg protein daily'],
        ],
        col_widths=[100, 120, 170])
    story.append(Paragraph('Insulin — The Double-Edged Hormone', s['SecHead']))
    story.append(Paragraph(
        'Insulin is perhaps the most misunderstood hormone in fitness. Often demonised in fat-loss contexts, insulin '
        'is powerfully anabolic — it drives amino acids into muscle cells, inhibits muscle protein breakdown (MPB), '
        'and stimulates glycogen synthesis. The key is timing: spike insulin around training when muscles are insulin-sensitive '
        'and uptake is maximised; manage insulin the rest of the day to prevent fat storage and maintain sensitivity.', s['Body']))
    callout(story, s, 'Indian Advantage: Post-workout meals of rice + dal + chicken are near-perfect for insulin-mediated muscle protein synthesis — fast-digesting carbs (rice) + complete protein (chicken) + slowly-digesting protein (dal).')
    story.append(Paragraph('Cortisol — The Catabolic Antagonist', s['SecHead']))
    story.append(Paragraph(
        'Cortisol is released by the adrenal cortex in response to physical and psychological stress. Acutely, cortisol '
        'is essential — it mobilises energy, suppresses inflammation, and enables the fight-or-flight response. Chronically '
        'elevated cortisol is catastrophic for muscle-building: it activates ubiquitin-proteasome pathway (muscle breakdown), '
        'inhibits testosterone synthesis, impairs sleep quality, and promotes visceral fat accumulation. Managing cortisol '
        'is not optional for serious Indian athletes living high-stress urban lives.', s['Body']))
    bullet(story, s, [
        'Training sessions > 75 minutes consistently elevate cortisol without proportional anabolic benefit.',
        'Ashwagandha (KSM-66, 600mg/day) reduces cortisol by 27.9% in clinical trials (Chandrasekhar et al., 2012).',
        'Post-workout carbohydrate consumption blunts cortisol spike by 20–30%.',
        'Meditation 10 minutes daily reduces baseline cortisol measurably within 4 weeks.',
    ])
    story.append(PageBreak())

    # ── CHAPTER 3 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 3 — PROGRESSIVE OVERLOAD & ADVANCED TRAINING SYSTEMS', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Non-Negotiable Law of Progress', s['SecHead']))
    story.append(Paragraph(
        'Progressive overload is the single most important principle in resistance training. Without systematically '
        'increasing the demand placed on muscle tissue over time, the body has no reason to adapt. Adaptation (muscle '
        'growth, strength gain) is the body\'s response to a stimulus that exceeds its current capacity. Once the '
        'body adapts to a given stimulus, that stimulus is no longer sufficient. Progress requires progressively '
        'greater challenges — but "greater" does not always mean "more weight."', s['Body']))
    story.append(Paragraph('10 Methods of Progressive Overload', s['SecHead']))
    add_table(story,
        ['Method', 'How to Apply', 'Best For'],
        [
            ['Add weight', 'Increase load when reps hit top of range', 'Compound lifts (beginner-intermediate)'],
            ['Add reps', 'Same weight, more reps each session', 'Accessory work'],
            ['Add sets', 'Increase weekly volume gradually', 'All training levels'],
            ['Reduce rest', 'Shorten rest by 10s/week', 'Metabolic/conditioning goals'],
            ['Slow eccentric', 'Add 1-second per week to lowering phase', 'Intermediate, muscle damage focus'],
            ['Increase ROM', 'Work through greater joint range', 'Intermediate, muscle length emphasis'],
            ['Better technique', 'Stricter form = greater target muscle activation', 'All levels'],
            ['Increase frequency', 'Train muscle 2x/week → 3x/week', 'Intermediate plateaus'],
            ['Density blocks', 'More total work in same time', 'Advanced athletes'],
            ['Technique advancement', 'Progress to harder exercise variation', 'All levels'],
        ],
        col_widths=[90, 180, 120])
    story.append(Paragraph('Periodisation — The System Behind Progress', s['SecHead']))
    story.append(Paragraph(
        'Periodisation is the systematic variation of training variables (volume, intensity, frequency) over time to '
        'maximise long-term adaptation while managing fatigue. Without periodisation, intensity accumulates without '
        'recovery — leading to overtraining, injury, and plateau. There are three primary periodisation models used '
        'in evidence-based strength and physique programming.', s['Body']))
    bullet(story, s, [
        'Linear Periodisation (LP): Volume decreases, intensity increases week by week. Classic beginner approach. Works well for 8–16 weeks. Example: Week 1 → 4×12 @ 60%, Week 4 → 4×6 @ 80%, Week 8 → 4×3 @ 90%.',
        'Daily Undulating Periodisation (DUP): Different rep ranges on different days for the same muscle group. Monday: 4×5 (strength), Wednesday: 4×12 (hypertrophy), Friday: 4×20 (endurance). Research shows DUP produces 28% greater strength gains vs LP over 12 weeks (Rhea et al., 2002).',
        'Block Periodisation: Distinct training phases (Accumulation → Intensification → Realisation). Most appropriate for advanced athletes. Used by Olympic-level strength athletes.',
    ])
    callout(story, s, 'For Indian athletes aged 18–35 seeking muscle gain: Daily Undulating Periodisation (DUP) in a Push/Pull/Legs split is the most evidence-backed approach for natural hypertrophy.')
    story.append(Paragraph('The Deload — Why Backing Off Makes You Bigger', s['SecHead']))
    story.append(Paragraph(
        'A deload is a planned reduction in training volume and/or intensity, typically for 1 week every 4–8 weeks '
        'of hard training. The purpose is to allow accumulated systemic fatigue to dissipate, enabling the nervous '
        'system to fully express the adaptations built during the preceding training block. Without regular deloads, '
        'fatigue masks fitness — you\'re stronger than you feel, but can\'t access it. Post-deload PRs are the norm '
        'when deloads are implemented correctly.', s['Body']))
    add_table(story,
        ['Deload Type', 'Volume Change', 'Intensity Change', 'Best Use Case'],
        [
            ['Volume deload', '40–60% reduction in sets', 'Same weight', 'Accumulated volume fatigue'],
            ['Intensity deload', 'Same sets', 'Reduce weight by 15–20%', 'Joint/tendon soreness'],
            ['Full deload', '50% reduction in both', 'Both reduced', 'After competition or peaking'],
            ['Active recovery', 'Light cardio, mobility only', 'Very low', 'Severe overreaching, illness'],
        ],
        col_widths=[90, 120, 120, 160])
    story.append(PageBreak())

    # ── CHAPTER 4 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 4 — NUTRITION BLUEPRINTS FOR MAXIMUM MUSCLE GROWTH', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Indian Athlete\'s Nutritional Reality', s['SecHead']))
    story.append(Paragraph(
        'Western bodybuilding nutrition advice is built around chicken breast, broccoli, and whey protein — foods '
        'that are expensive, culturally alien, and often unavailable in Indian homes. This chapter provides a complete, '
        'scientifically accurate nutrition system built entirely around Indian foods. Dal, paneer, eggs, chicken, rice, '
        'roti, and sabzi can build world-class physiques when combined correctly.', s['Body']))
    story.append(Paragraph('Calorie Targets by Goal', s['SecHead']))
    add_table(story,
        ['Goal', 'Calorie Target', 'Protein', 'Carbs', 'Fats'],
        [
            ['Lean Bulk', 'TDEE + 250–350 kcal', '2.0–2.2g/kg', '4–5g/kg', '0.8–1.0g/kg'],
            ['Fat Loss', 'TDEE − 350–500 kcal', '2.2–2.5g/kg', '2–3g/kg', '0.7–0.9g/kg'],
            ['Maintenance/Recomp', 'TDEE ± 0–100 kcal', '1.8–2.2g/kg', '3–4g/kg', '0.8–1.0g/kg'],
        ],
        col_widths=[90, 100, 80, 80, 80])
    story.append(Paragraph('High-Protein Indian Food Sources', s['SecHead']))
    add_table(story,
        ['Food', 'Serving', 'Protein', 'Notes'],
        [
            ['Chicken breast', '100g cooked', '31g', 'Complete protein, highest quality'],
            ['Paneer', '100g', '18g', 'Casein-rich, slow-digesting'],
            ['Eggs (whole)', '2 large', '12g', 'Most bioavailable protein (BV 100)'],
            ['Moong dal (cooked)', '150g', '10g', 'Leucine-rich for muscle synthesis'],
            ['Chana dal', '150g', '12g', 'High fibre + protein combo'],
            ['Greek yogurt (dahi)', '200g', '14g', 'Probiotics + casein protein'],
            ['Soya chunks', '50g dry', '25g', 'Complete plant protein, affordable'],
            ['Fish (rohu/pomfret)', '100g', '22g', 'Omega-3 rich, anabolic'],
            ['Whey protein (supplement)', '30g scoop', '24g', 'Fast-digesting, post-workout ideal'],
            ['Cottage cheese (low-fat)', '100g', '11g', 'Slow-release, good before bed'],
        ],
        col_widths=[100, 80, 70, 150])
    story.append(Paragraph('Nutrient Timing — When to Eat What', s['SecHead']))
    bullet(story, s, [
        'Pre-workout (60–90 min before): 40–60g carbs (rice, banana, oats) + 20–30g protein (egg whites, whey) + minimal fat. Goal: maximise glycogen, raise blood amino acids.',
        'Post-workout (within 45 min): 50–80g fast carbs (rice, fruit, bread) + 30–40g fast protein (whey, chicken breast). Goal: spike insulin to drive nutrients into muscle, suppress MPB.',
        'Pre-sleep meal: 30–40g slow protein (paneer, dahi, eggs) + minimal carbs. Casein-rich proteins maintain positive protein balance for 7 hours during sleep — building muscle while you rest.',
        'Distribute protein across 4–5 meals: leucine threshold (~3g per meal) must be reached each time to maximally activate mTOR. Eating 150g protein in 2 meals is inferior to 4 meals of 37.5g each.',
    ])
    callout(story, s, 'Budget Muscle-Building Meal (₹40–60): 150g cooked rice + 100g soya chunks + 1 egg + spinach sabzi + dahi. Macros: ~650 kcal, 38g protein, 85g carbs, 12g fat.')
    story.append(Paragraph('Hydration — The Forgotten Anabolic Factor', s['SecHead']))
    story.append(Paragraph(
        'Muscle tissue is approximately 75% water. A 2% reduction in body water content decreases strength by 10–20% '
        'and impairs protein synthesis. Indian summers and high-sweat training environments make dehydration a real '
        'performance limiter. Target: 35–45ml per kg bodyweight daily, adding 500ml per hour of intense training. '
        'Electrolytes (sodium, potassium, magnesium) must be replaced in high-sweat athletes — coconut water is an '
        'excellent, affordable electrolyte source for Indian athletes.', s['Body']))
    story.append(PageBreak())

    # ── CHAPTER 5 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 5 — SUPPLEMENT GUIDE — WHAT ACTUALLY WORKS (RANKED)', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Supplement Industry Reality', s['SecHead']))
    story.append(Paragraph(
        'India\'s supplement industry is worth ₹4,500+ crore and growing 15% annually. The marketing is extraordinary; '
        'the evidence for most products is not. This chapter cuts through the noise — ranking supplements by actual '
        'scientific evidence for muscle gain and performance, with specific product recommendations available in Indian markets.', s['Body']))
    story.append(Paragraph('Tier 1 — Strong Evidence (Use These)', s['SecHead']))
    add_table(story,
        ['Supplement', 'Dose', 'Timing', 'Benefit', 'Evidence'],
        [
            ['Creatine Monohydrate', '5g/day', 'Any time', '+5–15% strength, muscle cell hydration', '500+ RCTs'],
            ['Whey Protein', '25–50g/day', 'Post-workout', 'Leucine-rich, fast-absorbing protein', 'Very strong'],
            ['Caffeine', '3–6mg/kg', '45 min pre-workout', '+9–12% strength, endurance, focus', 'Very strong'],
            ['Vitamin D3', '2000–5000 IU/day', 'With fat meal', 'Testosterone production, bone health', 'Strong'],
            ['Magnesium Glycinate', '300–400mg', 'Before bed', 'Sleep quality, testosterone, recovery', 'Strong'],
        ],
        col_widths=[90, 60, 80, 130, 60])
    story.append(Paragraph('Tier 2 — Moderate Evidence (Consider These)', s['SecHead']))
    add_table(story,
        ['Supplement', 'Dose', 'Benefit', 'Notes'],
        [
            ['Beta-Alanine', '3.2g/day', 'Reduces fatigue in 8–15 rep range', 'Tingling (harmless) is normal'],
            ['Citrulline Malate', '6–8g pre', 'Better pump, reduces DOMS', 'Underrated, very affordable'],
            ['Ashwagandha KSM-66', '600mg/day', '↓ Cortisol 28%, ↑ T by 15–17%', 'Indian origin — widely available'],
            ['Omega-3 (Fish Oil)', '3g EPA+DHA', 'Reduces inflammation, improves recovery', 'Vegans: algae-based omega-3'],
            ['Zinc', '15–30mg/day', 'Testosterone synthesis cofactor', 'Only supplement if deficient'],
        ],
        col_widths=[100, 80, 150, 160])
    story.append(Paragraph('Tier 3 — Weak/No Evidence (Skip)', s['SecHead']))
    bullet(story, s, [
        'BCAAs (if consuming adequate protein): Total protein intake matters — isolated BCAAs add nothing when diet is sufficient.',
        'Testosterone boosters (most commercial products): Studies show negligible effect on actual testosterone levels.',
        'Weight gainers (most brands): Expensive calories — 90% simple carbs. Better to eat rice.',
        'Glutamine supplementation: Effective only in post-surgery/hospitalised patients. Useless for healthy athletes.',
        'CLA (Conjugated Linoleic Acid): Modest fat loss effect (−0.1kg/week) at best — not worth cost.',
    ])
    callout(story, s, 'Budget Stack for Indian Athletes (₹1,500–2,000/month): Creatine monohydrate (₹400) + Vitamin D3 (₹150) + Magnesium (₹200) + Protein from food. This outperforms 90% of expensive supplement stacks.')
    story.append(PageBreak())

    # ── CHAPTER 6 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 6 — RECOVERY, SLEEP & CORTISOL MANAGEMENT', s['ChHead']))
    hr(story)
    story.append(Paragraph('Recovery IS Training', s['SecHead']))
    story.append(Paragraph(
        'Every adaptation you seek — larger muscles, greater strength, leaner body — occurs during recovery, not during '
        'training. The workout is the stimulus; recovery is the response. The best training programme in the world '
        'produces zero results if recovery is compromised. Most Indian athletes under-recover due to work stress, '
        'family obligations, poor sleep environments, and inadequate nutrition during rest days.', s['Body']))
    story.append(Paragraph('Sleep Architecture & Muscle Growth', s['SecHead']))
    story.append(Paragraph(
        'Sleep consists of 4–5 cycles of approximately 90 minutes each, alternating between REM and NREM stages. '
        'Stage 3 NREM (deep sleep) is when 60–70% of daily GH is released in its largest pulse. This pulse is '
        'responsible for tissue repair, protein synthesis, and immune function. REM sleep consolidates motor learning '
        '— making new movement patterns automatic. Both are critical for athletes.', s['Body']))
    add_table(story,
        ['Sleep Variable', 'Optimal', 'When Compromised'],
        [
            ['Duration', '7.5–9 hours', 'Below 6h: −23% T, −31% IGF-1, +↑↑ cortisol'],
            ['Room temperature', '16–19°C', 'Above 22°C: disrupted deep sleep'],
            ['Light exposure', 'Complete darkness', 'Blue light within 1h: delays melatonin 90 min'],
            ['Consistency', 'Same time ±30 min', 'Irregular: 25% worse sleep quality'],
            ['Pre-sleep nutrition', 'Protein + low carbs', 'High sugar: disrupts NREM stage 3'],
        ],
        col_widths=[100, 100, 200])
    story.append(Paragraph('Active Recovery Protocols', s['SecHead']))
    bullet(story, s, [
        'Contrast showers (3 min hot / 1 min cold × 3 cycles): Reduces DOMS by 30–40%, improves parasympathetic nervous system tone.',
        'Light walking (20–30 min): Promotes blood flow without adding training stress. Ideal on rest days.',
        'Foam rolling / myofascial release: Reduces perceived soreness and improves ROM acutely.',
        'Pranayama (4-7-8 breathing): Activates parasympathetic nervous system, reduces cortisol within 10 minutes.',
    ])
    callout(story, s, 'The Most Underrated Recovery Tool: Eating enough food. Athletes in a severe calorie deficit cannot adequately recover. If you\'re sore 4+ days after training, eat more.')
    story.append(PageBreak())

    # ── CHAPTER 7 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 7 — ADVANCED TECHNIQUES: DROP SETS, SUPERSETS, CLUSTERS', s['ChHead']))
    hr(story)
    story.append(Paragraph('When to Use Advanced Techniques', s['SecHead']))
    story.append(Paragraph(
        'Advanced training techniques are tools — not requirements. They are most effective for intermediate and '
        'advanced athletes (12+ months consistent training) who have plateaued on straight-set programming. '
        'Beginners extract more benefit from simply adding weight and reps to basic movements. Used correctly, '
        'these techniques extend training volume beyond what straight sets allow, increasing mechanical tension '
        'and metabolic stress in the same or less time.', s['Body']))
    story.append(Paragraph('Drop Sets', s['SecHead']))
    story.append(Paragraph(
        'A drop set involves performing a set to near-failure, then immediately reducing the weight by 15–25% and '
        'continuing for additional reps without rest. Research shows drop sets produce equivalent hypertrophy to '
        '3 traditional sets in one-third the time — making them extremely time-efficient. Best used on isolation '
        'exercises (curls, lateral raises, tricep pushdowns) at the end of a workout.', s['Body']))
    story.append(Paragraph('Supersets & Antagonist Pairing', s['SecHead']))
    story.append(Paragraph(
        'Supersets combine two exercises performed back-to-back with minimal rest. Antagonist supersets '
        '(e.g., bicep curl + tricep extension) are particularly powerful: working the antagonist muscle '
        'actually potentiates the agonist via reciprocal inhibition — allowing you to lift heavier on the '
        'second movement than if rested. This increases total volume by 25–40% in the same workout duration.', s['Body']))
    story.append(Paragraph('Cluster Sets', s['SecHead']))
    story.append(Paragraph(
        'Cluster sets involve intra-set rest periods (10–30 seconds) between mini-sets. Example: instead of '
        '4×6 at 85% 1RM with 3 min rest, perform 4 sets of (2+2+2) with 20 sec between each pair, 3 min between sets. '
        'This allows more total volume at higher intensities than traditional sets — producing superior strength gains '
        'without proportional fatigue accumulation.', s['Body']))
    add_table(story,
        ['Technique', 'Best For', 'Exercise Type', 'When to Use'],
        [
            ['Drop sets', 'Metabolic stress, time efficiency', 'Isolation exercises', 'Last 1–2 sets of workout'],
            ['Supersets', 'Volume, time efficiency', 'Antagonist pairs', 'Throughout workout'],
            ['Giant sets', 'Metabolic conditioning', '3–4 isolation exercises', 'End of workout finisher'],
            ['Cluster sets', 'Strength at high intensity', 'Compound lifts', 'Intensification phases'],
            ['Rest-pause', 'Fatigue management at failure', 'Any', 'Intermediate+'],
            ['Mechanical drop', 'Extend set via easier variation', 'Multi-angle exercises', 'Advanced athletes'],
        ],
        col_widths=[90, 110, 110, 110])
    story.append(PageBreak())

    # ── CHAPTER 8 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 8 — FULL 12-WEEK ANABOLIC TRANSFORMATION PROGRAM', s['ChHead']))
    hr(story)
    story.append(Paragraph('Program Structure Overview', s['SecHead']))
    story.append(Paragraph(
        'This 12-week program is built on a Push/Pull/Legs split run 5 days per week, with one upper-body '
        'frequency day and one full deload week at week 10. The program progresses through three 4-week phases — '
        'Accumulation (building volume tolerance), Intensification (building strength), and Peaking (maximum '
        'intensity, reduced volume). Progressive overload targets are written into every session.', s['Body']))
    add_table(story,
        ['Phase', 'Weeks', 'Rep Ranges', 'Sets/Muscle Group', 'RIR Target'],
        [
            ['Accumulation', '1–4', '10–15', '12–16 sets/week', '3–4'],
            ['Intensification', '5–8', '6–10', '14–18 sets/week', '1–2'],
            ['Deload', '9', 'Any', '50% reduction', '4–5'],
            ['Peaking', '10–12', '4–8', '16–20 sets/week', '0–1'],
        ],
        col_widths=[90, 70, 80, 120, 80])
    story.append(Paragraph('Weekly Schedule', s['SecHead']))
    add_table(story,
        ['Day', 'Session', 'Primary Muscles', 'Duration'],
        [
            ['Monday', 'Push A', 'Chest, front delts, triceps', '60–70 min'],
            ['Tuesday', 'Pull A', 'Back (width + thickness), rear delts, biceps', '65–75 min'],
            ['Wednesday', 'Legs A', 'Quads, hamstrings, glutes, calves', '70–80 min'],
            ['Thursday', 'Push B / Upper', 'Shoulders dominant, chest secondary', '55–65 min'],
            ['Friday', 'Pull B / Arms', 'Back thickness, biceps/triceps priority', '60–70 min'],
            ['Saturday', 'Legs B', 'Hamstring + glute dominant, quad secondary', '65–75 min'],
            ['Sunday', 'Rest / Active Recovery', 'Walking, mobility, pranayama', '20–30 min'],
        ],
        col_widths=[60, 80, 150, 80])
    story.append(Paragraph('Sample Push Day A — Week 1 (Accumulation)', s['SecHead']))
    add_table(story,
        ['Exercise', 'Sets', 'Reps', 'Rest', 'Notes'],
        [
            ['Barbell Bench Press', '4', '12', '2 min', 'Controlled descent 3 sec'],
            ['Incline DB Press', '3', '12', '90 sec', 'Full stretch at bottom'],
            ['Cable Crossover (low)', '3', '15', '60 sec', 'Squeeze at peak contraction'],
            ['Seated OHP (DB)', '4', '12', '90 sec', 'Full ROM, no arching'],
            ['Lateral Raises (cable)', '4', '15', '60 sec', 'Elbow-height, controlled'],
            ['Tricep Pushdown', '3', '15', '60 sec', 'Lock out completely'],
            ['Overhead Tricep Ext.', '3', '12', '60 sec', 'Feel stretch at top'],
        ],
        col_widths=[130, 35, 35, 50, 140])
    callout(story, s, 'Progressive Overload Instruction: Add 2.5kg when you complete the top of the rep range with RIR ≥ 2 for two consecutive sessions.')
    story.append(PageBreak())

    # ── CHAPTER 9 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 9 — INDIAN DIET TEMPLATES & MACRO BLUEPRINTS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Template A — 70kg Male, Lean Bulk (2,800 kcal)', s['SecHead']))
    add_table(story,
        ['Meal', 'Time', 'Foods', 'Protein', 'Carbs', 'Fat'],
        [
            ['Breakfast', '7:30 AM', '4 eggs scrambled + 2 roti + dahi', '34g', '40g', '18g'],
            ['Mid-Morning', '10:30 AM', 'Banana + handful almonds + 200ml milk', '10g', '38g', '12g'],
            ['Lunch', '1:00 PM', '200g chicken + 200g rice + dal + sabzi', '48g', '75g', '12g'],
            ['Pre-Workout', '4:00 PM', '100g oats + whey protein shake', '32g', '55g', '8g'],
            ['Post-Workout', '7:00 PM', '200g rice + 200g chicken/fish + salad', '48g', '70g', '8g'],
            ['Dinner', '9:30 PM', '100g paneer + 2 roti + salad + dahi', '28g', '30g', '14g'],
        ],
        col_widths=[60, 60, 150, 40, 40, 40])
    story.append(Paragraph('Total: 2,810 kcal | 200g Protein | 308g Carbs | 72g Fat', s['Callout']))
    story.append(Paragraph('Template B — 60kg Female, Fat Loss (1,700 kcal)', s['SecHead']))
    add_table(story,
        ['Meal', 'Time', 'Foods', 'Protein', 'Carbs', 'Fat'],
        [
            ['Breakfast', '7:00 AM', '3 egg whites + 1 whole egg + 1 roti + green tea', '22g', '18g', '7g'],
            ['Lunch', '12:30 PM', '150g chicken + 100g rice + dal + sabzi', '36g', '40g', '8g'],
            ['Evening', '4:30 PM', 'Greek yogurt + cucumber + 10 almonds', '16g', '12g', '9g'],
            ['Dinner', '7:30 PM', '100g paneer + sabzi + 1 roti + salad', '22g', '22g', '12g'],
            ['Pre-Sleep', '9:30 PM', '200ml warm milk + small handful walnuts', '10g', '10g', '9g'],
        ],
        col_widths=[60, 60, 165, 40, 40, 40])
    story.append(Paragraph('Total: 1,710 kcal | 106g Protein | 102g Carbs | 45g Fat', s['Callout']))
    story.append(Paragraph('Template C — 80kg Male, Vegetarian Bulk (3,000 kcal)', s['SecHead']))
    add_table(story,
        ['Meal', 'Time', 'Foods', 'Protein', 'Carbs', 'Fat'],
        [
            ['Breakfast', '7:30 AM', '200g paneer bhurji + 3 roti + dahi', '42g', '48g', '22g'],
            ['Mid-Morning', '10:30 AM', '200g soya chunks curry + rice (100g)', '30g', '40g', '6g'],
            ['Lunch', '1:00 PM', '200g moong dal + 200g rice + sabzi', '28g', '80g', '8g'],
            ['Pre-Workout', '4:00 PM', 'Whey protein + banana + 50g oats', '30g', '58g', '5g'],
            ['Post-Workout', '7:00 PM', '150g paneer + 200g rice + salad', '32g', '65g', '14g'],
            ['Dinner', '9:30 PM', '200g chana dal + 2 roti + sabzi + curd', '28g', '55g', '10g'],
        ],
        col_widths=[60, 60, 160, 40, 40, 40])
    story.append(Paragraph('Total: 2,990 kcal | 190g Protein | 346g Carbs | 65g Fat', s['Callout']))
    story.append(PageBreak())

    # ── CHAPTER 10 ──────────────────────────────────────────────────────────
    story.append(Paragraph('CHAPTER 10 — INJURY PREVENTION, JOINT HEALTH & LONGEVITY', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Athlete Who Stays Healthy Wins', s['SecHead']))
    story.append(Paragraph(
        'The athlete who trains consistently for 5 years will always outperform the athlete who trains harder for '
        '2 years before getting injured. Injury prevention is not passive — it is an active, ongoing investment in '
        'the machinery that allows you to train. Most injuries in Indian gym athletes are not freak accidents — '
        'they are predictable failures of progressive overload, technique, or recovery management.', s['Body']))
    story.append(Paragraph('Most Common Injuries & Prevention', s['SecHead']))
    add_table(story,
        ['Injury', 'Root Cause', 'Prevention Protocol'],
        [
            ['Lower back pain', 'Poor hip hinge pattern, excessive lumbar load', 'Hip hinge drills, brace before lift, RDL technique'],
            ['Rotator cuff strain', 'Internal rotation imbalance, poor shoulder mechanics', 'Band pull-aparts 3×20 daily, face pulls, external rotation'],
            ['Knee pain (patellar)', 'Quad dominance, tight IT band, poor ankle mobility', 'VMO strengthening, foam rolling, ankle mobility work'],
            ['Bicep tendinopathy', 'Curl with supinated grip under excessive load', 'Eccentric curls, reduce load, increase recovery time'],
            ['Tennis elbow', 'Excessive gripping, tricep overload', 'Wrist extensor stretches, reduce grip exercises temporarily'],
        ],
        col_widths=[100, 140, 160])
    story.append(Paragraph('Warm-Up Protocol (10–12 minutes)', s['SecHead']))
    bullet(story, s, [
        '3 minutes light cardio (skipping, rowing, bike) — raises core temperature 1–2°C, crucial for tissue pliability.',
        '2 minutes dynamic stretching — leg swings, arm circles, hip circles — through full ROM.',
        '2 minutes activation — glute bridges, band clamshells, scapular retractions — activating target muscles.',
        '2–3 progressive warm-up sets at 40%, 60%, 80% of working weight before the first compound exercise.',
    ])
    story.append(Paragraph('Joint Nutrition Protocol', s['SecHead']))
    add_table(story,
        ['Nutrient', 'Dose', 'Source', 'Benefit'],
        [
            ['Collagen peptides', '15–20g/day', 'Supplement', 'Tendon/cartilage repair (with Vit C)'],
            ['Omega-3', '3g EPA+DHA', 'Fish oil / fatty fish', 'Reduces joint inflammation'],
            ['Vitamin C', '500–1000mg/day', 'Amla, guava, supplement', 'Collagen synthesis cofactor'],
            ['Glucosamine + Chondroitin', '1500mg + 1200mg', 'Supplement', 'Moderate evidence for joint comfort'],
            ['Curcumin (with piperine)', '500–1000mg/day', 'Haldi + black pepper', 'Potent anti-inflammatory'],
        ],
        col_widths=[100, 80, 120, 150])
    callout(story, s, 'Long-Term Rule: Train for decades, not seasons. A 10% reduction in ego at the gym produces a 1000% better outcome over a 10-year athletic career.')

    # ── CONCLUSION ──────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('CONCLUSION — YOUR ANABOLIC BLUEPRINT', s['ChHead']))
    hr(story)
    story.append(Paragraph(
        'You now possess a complete, science-backed system for building muscle as an Indian athlete. The principles '
        'in this guide are not opinion — they are derived from decades of peer-reviewed research and adapted for '
        'the Indian context: our foods, our stress environment, our recovery challenges, and our genetic strengths. '
        'The path is clear. What separates the transformed from the unchanged is not knowledge — it is consistent '
        'application of the fundamentals, week after week, month after month.', s['Body']))
    bullet(story, s, [
        'Train 4–6 days/week with progressive overload as the compass.',
        'Eat 1.8–2.2g protein/kg from Indian food sources. Supplement where food falls short.',
        'Sleep 7.5–9 hours. This is not optional — it is where your results are made.',
        'Manage cortisol: shorter sessions, adequate food, ashwagandha, stress practices.',
        'Deload every 4–8 weeks. Your post-deload PRs will confirm it was correct.',
        'Stay injury-free: warm up, progress sensibly, address imbalances early.',
    ])
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB — BUILD YOUR BEAST', s['Cover2']))
    story.append(Paragraph('www.royalfitnessclub.in', s['Cover3']))

    doc.build(story)
    from PyPDF2 import PdfReader
    count = len(PdfReader(path).pages)
    print(f'Anabolic Full Guide: {count} pages → {path}')

build_anabolic()
print('Part 1 done.')
