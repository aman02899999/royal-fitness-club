"""Generate catalog PDFs 11-15 with dark navy theme."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

OUT = '/home/user/royal-fitness-club/generated_pdfs'
DARK = colors.HexColor('#020b18')
NAVY = colors.HexColor('#0a0f1a')
NAVY2 = colors.HexColor('#0d1a2a')
BLUE = colors.HexColor('#0066cc')
GOLD = colors.HexColor('#ffd000')
LGREY = colors.HexColor('#cccccc')
WHITE = colors.white
CYAN = colors.HexColor('#38bdf8')
W, H = A4

def dark_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.restoreState()

def st():
    s = getSampleStyleSheet()
    d = {
        'Cover1': dict(fontName='Helvetica-Bold', fontSize=32, textColor=WHITE, alignment=TA_CENTER, spaceAfter=6, leading=40),
        'Cover2': dict(fontName='Helvetica-Bold', fontSize=16, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4, leading=22),
        'Cover3': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, alignment=TA_CENTER, spaceAfter=4, leading=15),
        'ChHead': dict(fontName='Helvetica-Bold', fontSize=14, textColor=BLUE, spaceBefore=12, spaceAfter=7, leading=19),
        'SecHead': dict(fontName='Helvetica-Bold', fontSize=11, textColor=WHITE, spaceBefore=8, spaceAfter=4, leading=16),
        'Body': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=5, leading=16, alignment=TA_JUSTIFY),
        'Blt': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15, leftIndent=14, firstLineIndent=-10),
        'Callout': dict(fontName='Helvetica-BoldOblique', fontSize=10, textColor=GOLD, spaceBefore=5, spaceAfter=5, leading=16, leftIndent=10, rightIndent=10),
        'Quote': dict(fontName='Helvetica-Oblique', fontSize=11, textColor=CYAN, spaceBefore=7, spaceAfter=7, leading=18, leftIndent=20, rightIndent=20, alignment=TA_CENTER),
        'TOCItem': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15),
    }
    for n, kw in d.items():
        if n not in s: s.add(ParagraphStyle(name=n, **kw))
        else:
            for k, v in kw.items(): setattr(s[n], k, v)
    return s

def tb(story, headers, rows, widths=None):
    t = Table([headers]+rows, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[NAVY2, NAVY]),
        ('TEXTCOLOR',(0,1),(-1,-1),LGREY),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#1a3a5a')),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(t); story.append(Spacer(1, 3*mm))

def hr(story): story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#1a3a5a'), spaceBefore=4, spaceAfter=4))
def bl(story, s, items):
    for i in items: story.append(Paragraph(f'• {i}', s['Blt']))
def co(story, s, t): story.append(Paragraph(f'💡 {t}', s['Callout']))
def qt(story, s, t): story.append(Paragraph(f'"{t}"', s['Quote']))
def sp(story, n=4): story.append(Spacer(1, n*mm))

def cover(story, s, num, title, subtitle, tags):
    sp(story, 20)
    story.append(Paragraph('ROYAL FITNESS CLUB', s['Cover3']))
    sp(story, 3)
    story.append(Paragraph(f'RFC PREMIUM GUIDE #{num:02d}', s['Cover3']))
    sp(story, 8)
    story.append(HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=8))
    story.append(Paragraph(title.upper(), s['Cover1']))
    sp(story, 4)
    story.append(Paragraph(subtitle, s['Cover2']))
    sp(story, 6)
    story.append(HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=8))
    sp(story, 4)
    story.append(Paragraph('  ·  '.join(tags), s['Cover3']))
    sp(story, 4)
    story.append(Paragraph('© Royal Fitness Club — For Members Only', s['Cover3']))
    story.append(PageBreak())

def toc(story, s, chapters):
    story.append(Paragraph('TABLE OF CONTENTS', s['ChHead']))
    hr(story)
    sp(story, 2)
    for i, (ch, pg) in enumerate(chapters, 1):
        dots = '·' * max(2, 55 - len(ch) - len(str(pg)))
        story.append(Paragraph(f'Chapter {i} — {ch}  {dots}  {pg}', s['TOCItem']))
    sp(story, 6)
    story.append(Paragraph('DISCLAIMER', s['ChHead']))
    hr(story)
    story.append(Paragraph('This guide is for educational purposes only. Not medical advice. Consult a qualified healthcare professional before starting any protocol. Individual results vary.', s['Body']))
    story.append(PageBreak())

def mk(path, num, title, subtitle, tags, fn):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = st(); story = []
    cover(story, s, num, title, subtitle, tags)
    fn(story, s)
    doc.build(story, onFirstPage=dark_bg, onLaterPages=dark_bg)
    print(f'  ✓ {os.path.basename(path)}')

# ─── PDF 11 — Women's Complete Body Transformation ───────────────────────────
def pdf11(story, s):
    toc(story, s, [
        ('Body Transformation Fundamentals for Women', 3),
        ('Resistance Training Programme (12 Weeks)', 4),
        ('Nutrition Architecture', 5),
        ('Cardio, Recovery & Hormonal Balance', 6),
        ('Progress Tracking & Mindset', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — BODY TRANSFORMATION FUNDAMENTALS', s['ChHead']))
    hr(story)
    qt(story, s, 'A body transformation is not a six-week project. It is the first year of your new permanent lifestyle. Begin with that timeframe in mind.')
    story.append(Paragraph('The complete female body transformation involves simultaneously building lean muscle mass and reducing body fat — a process called body recomposition that is particularly effective for women who are new to or returning to structured resistance training. The result is a smaller, harder, more defined physique rather than simple weight loss which often leaves the body soft and metabolically compromised.', s['Body']))
    tb(story, ['Starting Point', 'Goal', 'Expected Timeline', 'Primary Method'],
       [['Beginner (no training history)', 'Foundation + 4–6kg muscle', '12–16 weeks', 'Full body 3× + nutrition'],
        ['Intermediate (some training)', 'Defined physique + 2–3kg muscle', '12 weeks', 'Upper/lower 4× + cut'],
        ['Advanced (consistent trainer)', 'Peak conditioning', '16+ weeks', 'PPL 5× + aggressive nutrition']],
       widths=[130, 130, 100, 165])
    co(story, s, 'Women gain muscle at approximately half the rate of men due to lower testosterone. This is actually an advantage — lean muscle gain means minimal fat gain compared to male "bulking" phases.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — 12-WEEK RESISTANCE PROGRAMME', s['ChHead']))
    hr(story)
    story.append(Paragraph('Phase 1 — Foundation (Weeks 1–4)', s['SecHead']))
    tb(story, ['Exercise', 'Sets', 'Reps', 'Rest', 'Key Form Cue'],
       [['Goblet Squat', '3', '12–15', '60 sec', 'Chest up, knees track over toes'],
        ['Romanian Deadlift (dumbbells)', '3', '12', '60 sec', 'Hip hinge — push hips back first'],
        ['Dumbbell Hip Thrust', '3', '15', '60 sec', 'Squeeze glutes at top, chin tuck'],
        ['Dumbbell Row', '3', '12 each', '60 sec', 'Elbow drives back, squeeze at top'],
        ['Dumbbell Overhead Press', '3', '12', '60 sec', 'Core tight, do not arch lower back'],
        ['Plank', '3', '30–45 sec', '45 sec', 'Straight line head to heels, breathe']],
       widths=[145, 40, 55, 55, 180])
    story.append(Paragraph('Phase 2 — Progressive (Weeks 5–8)', s['SecHead']))
    tb(story, ['Day', 'Focus', 'Volume', 'Intensity'],
       [['Day 1 (Mon)', 'Lower body strength', '16–18 sets', '70–75% 1RM'],
        ['Day 2 (Wed)', 'Upper body + core', '16–18 sets', '65–70% 1RM'],
        ['Day 3 (Fri)', 'Full body metabolic', '14 sets', 'Circuit format, 60% 1RM'],
        ['Day 4 (Sat)', 'Lower body emphasis (glutes/hamstrings)', '16 sets', '70% 1RM']],
       widths=[100, 130, 90, 105])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — NUTRITION ARCHITECTURE', s['ChHead']))
    hr(story)
    qt(story, s, 'You can build and reveal your best physique eating real Indian food. Supplements are optional; protein, vegetables and calories are not.')
    tb(story, ['Goal', 'Calories', 'Protein', 'Carbs', 'Fat', 'Notes'],
       [['Recomposition (beginner)', 'Maintenance', '2.0g/kg', '3.0g/kg', '0.8g/kg', 'Lose fat and gain muscle simultaneously'],
        ['Fat loss (intermediate)', 'TDEE − 350', '2.3g/kg', '2.0g/kg', '0.8g/kg', 'Cut at controlled rate'],
        ['Muscle focus (after cut)', 'TDEE + 200', '2.0g/kg', '4.0g/kg', '0.7g/kg', 'Lean bulk phase after fat loss']],
       widths=[145, 70, 70, 70, 50, 120])
    story.append(Paragraph('Daily Meal Framework', s['SecHead']))
    bl(story, s, [
        'Breakfast: protein + complex carb + healthy fat (moong dal chilla, eggs, Greek yoghurt)',
        'Lunch: protein + vegetables + moderate carb (dal, sabzi, brown rice or 1 roti)',
        'Pre-workout (if afternoon training): banana + whey/paneer',
        'Post-workout: protein-rich meal within 2 hours (chicken/paneer + carb source)',
        'Dinner: protein + vegetables, lower carb if sedentary evening',
        'Optional snack: handful of nuts, low-fat dahi, or protein shake',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — CARDIO, RECOVERY & HORMONES', s['ChHead']))
    hr(story)
    tb(story, ['Week', 'Cardio Type', 'Duration', 'Frequency', 'Heart Rate Zone'],
       [['1–4', 'Brisk walking / cycling', '30 min', '3×/week', '55–65% HRmax (Zone 2)'],
        ['5–8', 'Incline treadmill + HIIT', '30 + 15 min', '4×/week', 'Zone 2 + HIIT Zone 4'],
        ['9–12', 'Mixed cardio + HIIT', '2 LISS + 2 HIIT', '4×/week', 'Varied zones for max fat loss']],
       widths=[60, 120, 80, 80, 185])
    co(story, s, 'Women should NOT do fasted cardio during the luteal phase (Days 15–28) — cortisol is already elevated and fasted training can worsen hormonal disruption. Train fed in this phase.')
    story.append(Paragraph('Hormonal Optimisation Supplements', s['SecHead']))
    bl(story, s, [
        'Iron: 18mg/day (food-based or supplement) — low iron causes fatigue, impairs training',
        'Omega-3 (EPA/DHA): 2g/day — reduces inflammation, supports hormonal health',
        'Magnesium glycinate: 300mg before bed — sleep quality, PMS, muscle recovery',
        'Vitamin D3: 2000–5000 IU/day — critical for muscle function and hormone synthesis',
        'Ashwagandha KSM-66: 600mg/day — cortisol reduction, strength improvement in women',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — PROGRESS TRACKING & MINDSET', s['ChHead']))
    hr(story)
    qt(story, s, 'The transformation that lasts is the one you enjoy building. Chase performance. The aesthetic follows.')
    tb(story, ['Metric', 'How to Measure', 'Track Frequency', 'Healthy Progress Rate'],
       [['Body weight', 'Morning, fasted, same day weekly', 'Weekly (7-day average)', '0.5–0.8kg fat loss/week'],
        ['Body measurements', 'Chest, waist, hips, thighs, arms', 'Every 2 weeks', 'Waist −1cm/month'],
        ['Progress photos', 'Same pose, lighting, time', 'Every 4 weeks', 'Compare month 1 vs 3'],
        ['Strength', 'Log all lifts — sets, reps, weight', 'Every session', '+2.5–5% monthly on compounds'],
        ['Energy & mood', '1–10 daily score journal', 'Daily', 'Should improve by Week 6–8']],
       widths=[100, 130, 100, 145])
    bl(story, s, [
        'Non-scale victories: fitting old clothes, better posture, improved stamina, confident mindset',
        'If scale stalls for 10+ days: check sleep, stress, tracking accuracy before changing diet',
        'Compare current photos to 4 weeks ago, not to social media — context is everything',
        '12-week transformation is 1/4 of a year. A lifetime of consistency is the true target.',
    ])

mk(os.path.join(OUT, '11_Womens_Complete_Body_Transformation.pdf'), 11,
   "Women's Complete Body Transformation", '12-Week System Built for Female Physiology',
   ['12 Weeks', '5 Chapters', 'Female Specific', 'Beginner to Advanced'], pdf11)

# ─── PDF 12 — Indian Bodybuilder Nutrition Bible ──────────────────────────────
def pdf12(story, s):
    toc(story, s, [
        ('Indian Food Science for Bodybuilding', 3),
        ('Protein Sources: Complete Indian Guide', 4),
        ('Bulking Meal Plans — Indian Style', 5),
        ('Cutting Meal Plans — Indian Style', 6),
        ('Supplement Strategy for Indian Athletes', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — INDIAN FOOD SCIENCE FOR BODYBUILDING', s['ChHead']))
    hr(story)
    qt(story, s, 'India has the world\'s richest vegetarian food culture. It also has one of the most protein-deficient average diets. These two facts are not contradictory — they are an opportunity.')
    story.append(Paragraph('The traditional Indian diet is primarily carbohydrate-dominant — rice, roti, daal, sabzi — with protein often playing a secondary role. For bodybuilders, this nutritional architecture needs strategic restructuring. The good news: Indian cuisine offers world-class protein sources (paneer, daal, eggs, chicken, fish) and an extraordinary array of anti-inflammatory spices (turmeric, ginger, black pepper, cumin) that support recovery and hormonal health.', s['Body']))
    tb(story, ['Indian Food', 'Protein (100g)', 'Carbs (100g)', 'Fat (100g)', 'Bodybuilding Rating'],
       [['Paneer', '18g', '1g', '20g', '★★★★★ (protein + fat)'],
        ['Chicken breast', '31g', '0g', '3g', '★★★★★ (lean protein king)'],
        ['Whole eggs', '13g', '1g', '10g', '★★★★★ (complete protein)'],
        ['Moong dal (cooked)', '7g', '19g', '0.4g', '★★★★ (high-volume protein)'],
        ['Rajma (cooked)', '9g', '22g', '0.5g', '★★★★ (excellent bulking food)'],
        ['Greek yoghurt', '10g', '3g', '5g', '★★★★ (probiotic + protein)'],
        ['Roti (1 piece)', '3g', '15g', '0.5g', '★★★ (complex carb base)'],
        ['Brown rice (cooked)', '2.5g', '23g', '0.2g', '★★★ (quality carb source)']],
       widths=[110, 80, 80, 80, 175])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — PROTEIN SOURCES COMPLETE GUIDE', s['ChHead']))
    hr(story)
    tb(story, ['Source', 'Serving', 'Protein', 'Cost Rating', 'Best Used In'],
       [['Chicken breast (cooked)', '150g', '47g', 'Low', 'Lunch/dinner — versatile'],
        ['Whole eggs', '3 eggs', '18g', 'Very Low', 'Breakfast, pre-bed'],
        ['Paneer', '100g', '18g', 'Moderate', 'Sabzi, bhurji, tikka'],
        ['Whey protein', '1 scoop (30g)', '24g', 'Moderate', 'Post-workout, between meals'],
        ['Greek yoghurt', '200g', '20g', 'Moderate', 'Snack, raita base'],
        ['Tuna (canned)', '1 can (100g)', '25g', 'Very Low', 'Quick meal, salads'],
        ['Soya chunks (rehydrated)', '50g dry', '25g', 'Very Low', 'Curry base, ideal for vegetarians'],
        ['Moong dal', '100g cooked', '7g', 'Very Low', 'Soup, chilla, dal'],
        ['Roasted chana', '50g', '10g', 'Very Low', 'Snack, portable protein']],
       widths=[130, 80, 60, 75, 180])
    co(story, s, 'Indian bodybuilder protein priority order: chicken breast → eggs → paneer/soya chunks → whey protein → dal. Aim for at least 3 of these sources daily.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — BULKING MEAL PLANS', s['ChHead']))
    hr(story)
    story.append(Paragraph('3500–4000 kcal Bulking Day (80kg athlete)', s['SecHead']))
    tb(story, ['Meal', 'Foods', 'Protein', 'Kcal'],
       [['7 AM Breakfast', '6 eggs + 4 roti + 1 cup full-fat milk', '45g', '700'],
        ['10 AM Mid-morning', '200g paneer bhurji + 2 slices bread', '38g', '520'],
        ['1 PM Pre-workout', '2 cups rice + 200g chicken curry + salad', '42g', '680'],
        ['3 PM Pre-workout shake', '1.5 scoops whey + 1 banana + 30g oats', '42g', '480'],
        ['6 PM Post-workout', '2 scoops whey + 50g dextrose', '50g', '400'],
        ['8 PM Dinner', '200g fish + 3 roti + 1 cup daal + sabzi', '55g', '720'],
        ['10 PM Night', '300ml milk + 30g casein protein', '40g', '360']],
       widths=[90, 195, 60, 55])
    story.append(Paragraph('Total: ~3860 kcal, ~312g protein', s['Body']))
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — CUTTING MEAL PLANS', s['ChHead']))
    hr(story)
    story.append(Paragraph('1800–2000 kcal Cutting Day (80kg athlete)', s['SecHead']))
    tb(story, ['Meal', 'Foods', 'Protein', 'Kcal'],
       [['7 AM Breakfast', '4 egg whites + 2 whole eggs + spinach omelette', '30g', '280'],
        ['10 AM Mid-morning', '200g Greek yoghurt + 10 almonds', '22g', '240'],
        ['1 PM Lunch', '150g grilled chicken + 1 cup brown rice + salad', '38g', '440'],
        ['4 PM Pre-workout', '1 scoop whey + 1 apple', '24g', '230'],
        ['7 PM Dinner', '200g paneer tikka + 2 roti + raita (small)', '44g', '580'],
        ['9 PM Night', '1 scoop casein + water', '24g', '130']],
       widths=[90, 205, 60, 55])
    story.append(Paragraph('Total: ~1900 kcal, ~182g protein. Adjust roti/rice portions to hit exact calorie target.', s['Body']))
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — SUPPLEMENT STRATEGY', s['ChHead']))
    hr(story)
    qt(story, s, 'Supplements supplement a good diet. They do not replace one. Get the food right first — then fill the specific gaps with supplements.')
    tb(story, ['Supplement', 'Priority', 'Dose', 'Indian-Specific Note'],
       [['Whey Protein (isolate)', 'Essential', '1–2 scoops/day', 'Dymatize, Optimum Nutrition reliable in India'],
        ['Creatine Monohydrate', 'Essential', '5g/day', 'Unflavoured — add to shake or water'],
        ['Vitamin D3', 'Essential', '2000–5000 IU', 'Most Indians significantly deficient'],
        ['Omega-3', 'High', '2–3g EPA/DHA', 'International Fish Oil — avoid cheap Indian brands'],
        ['Zinc + Magnesium', 'High', '25mg Zn + 300mg Mg', 'ZMA tablets widely available'],
        ['Ashwagandha KSM-66', 'Moderate', '600mg/day', 'Himalaya or KSM-66 standardised extract'],
        ['Multivitamin', 'Moderate', 'As directed', 'Fills micronutrient gaps in Indian diet'],
        ['Pre-workout', 'Optional', 'As directed', 'Caffeine + beta-alanine most evidenced']],
       widths=[120, 65, 100, 180])
    bl(story, s, [
        'Spend on food before supplements — 500g chicken costs less than one bottle of most supplements',
        'Indian brands: MuscleBlaze and AS-IT-IS are reliable for whey protein',
        'Avoid testosterone boosters — the evidence is weak and the claims are exaggerated',
        'Protein bars: read labels — most Indian protein bars have less protein than advertised',
    ])

mk(os.path.join(OUT, '12_Indian_Bodybuilder_Nutrition_Bible.pdf'), 12,
   'Indian Bodybuilder Nutrition Bible', 'Complete Nutrition System Using Indian Foods',
   ['5 Chapters', 'India-Specific', 'Veg & Non-Veg', 'Meal Plans Included'], pdf12)

# ─── PDF 13 — Pre-Workout Optimisation Guide ─────────────────────────────────
def pdf13(story, s):
    toc(story, s, [
        ('Pre-Workout Science: What Actually Works', 3),
        ('Caffeine Optimisation Protocol', 4),
        ('Nitric Oxide & Blood Flow Compounds', 5),
        ('Mental Focus Nootropics for Training', 6),
        ('Building Your Custom Pre-Workout Stack', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — PRE-WORKOUT SCIENCE', s['ChHead']))
    hr(story)
    qt(story, s, 'A great pre-workout is not a product you buy — it is a system you build: food timing, caffeine, blood flow, and mental preparation.')
    story.append(Paragraph('The pre-workout window (60–90 minutes before training) represents the highest-leverage nutritional and supplementation opportunity in the day. Optimal pre-workout preparation maximises training performance, which in turn maximises the training stimulus, which drives muscle growth and fat loss. The most evidence-based pre-workout compounds are inexpensive, well-researched, and available individually — not bundled into expensive proprietary blends.', s['Body']))
    tb(story, ['Compound', 'Evidence Grade', 'Effect', 'Dose', 'Timing'],
       [['Caffeine', 'A (very strong)', 'Performance +3–12%, focus, fat oxidation', '3–6mg/kg BW', '45–60 min pre'],
        ['Creatine', 'A (very strong)', 'Strength, power, muscle volume', '5g daily', 'Any time (consistent)'],
        ['Beta-Alanine', 'B (strong)', 'Muscular endurance, reduces fatigue', '3.2–6.4g/day', 'Daily loading'],
        ['Citrulline Malate', 'B (strong)', 'Blood flow, pump, endurance', '6–8g', '60 min pre'],
        ['Beetroot / NO3', 'B (good)', 'Nitric oxide, endurance', '500mg NO3 equiv', '60–90 min pre'],
        ['Tyrosine', 'C (moderate)', 'Mental focus, stress resistance', '500mg–2g', '60 min pre'],
        ['Alpha-GPC', 'C (moderate)', 'Acetylcholine, mind-muscle', '300–600mg', '60 min pre']],
       widths=[105, 90, 160, 80, 90])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — CAFFEINE OPTIMISATION', s['ChHead']))
    hr(story)
    qt(story, s, 'Caffeine tolerance is a real phenomenon. Using it strategically — not habitually — is the difference between a training tool and a dependency.')
    story.append(Paragraph('Caffeine is the single most evidence-backed sports performance compound available. At appropriate doses, it increases strength by 3–7%, endurance by 5–12%, and fat oxidation by 10–15% during exercise. However, chronic daily use leads to complete tolerance within 1–2 weeks, eliminating virtually all performance benefit. Strategic use — reserved for training days with mandatory caffeine-free days — preserves the ergogenic effect.', s['Body']))
    tb(story, ['User Type', 'Daily Caffeine', 'Recommended Strategy', 'Pre-Workout Dose'],
       [['Non-user / beginner', '< 50mg', 'Start at 100mg pre-workout', '100–150mg'],
        ['Moderate user', '100–200mg (1–2 coffees)', 'No coffee on training days', '150–200mg pre'],
        ['Heavy user (> 3 coffees)', '300–500mg', 'Caffeine cycling protocol', '200–300mg pre (after 5-day break)'],
        ['Elite protocol', 'Minimal daily use', '5 days off caffeine, then 3–6mg/kg pre-competition', '3–6mg/kg body weight']],
       widths=[110, 95, 165, 105])
    co(story, s, 'Caffeine cycling protocol: 5 caffeine-free days every 4 weeks restores full sensitivity. Use decaf coffee, green tea (low caffeine) or nothing on off days.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — NITRIC OXIDE & BLOOD FLOW', s['ChHead']))
    hr(story)
    story.append(Paragraph('Nitric oxide (NO) is a vasodilator that increases blood flow to working muscles, resulting in improved nutrient and oxygen delivery, greater "the pump" sensation, and potentially enhanced hypertrophy through cell swelling mechanisms. L-Citrulline is the primary evidence-backed NO precursor.', s['Body']))
    tb(story, ['Compound', 'Mechanism', 'Dose', 'Time to Effect', 'Synergies'],
       [['L-Citrulline', 'Arginine precursor → NO via NOS', '6g', '60 min', 'Malate 2:1 ratio helps'],
        ['Citrulline Malate', 'Same + malate reduces lactate', '8g (6g citrulline)', '60 min', 'Caffeine, beetroot'],
        ['Beetroot Powder', 'Direct NO3 → NO2 → NO', '500mg NO3', '60–90 min', 'Citrulline synergy'],
        ['L-Arginine', 'Direct NO precursor (poor bioavailability)', '3–6g', '45 min', 'Less effective than citrulline'],
        ['Pine Bark Extract (Pycnogenol)', 'eNOS activation + antioxidant', '200mg', '30–45 min', 'Citrulline stack']],
       widths=[115, 130, 70, 75, 135])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — NOOTROPICS FOR TRAINING', s['ChHead']))
    hr(story)
    story.append(Paragraph('Mental focus, the mind-muscle connection, and psychological arousal are trainable variables that substantially impact training quality. The following nootropic compounds improve training performance through CNS mechanisms.', s['Body']))
    tb(story, ['Nootropic', 'Effect', 'Dose', 'Safety Profile', 'Note'],
       [['L-Tyrosine', 'Dopamine, noradrenaline precursor', '500mg–2g', 'Excellent', 'Best under stress or sleep deprivation'],
        ['Alpha-GPC', 'Acetylcholine precursor, power output', '300–600mg', 'Good', 'Pairs well with caffeine'],
        ['Huperzine A', 'AChE inhibitor — prolongs acetylcholine', '50–100mcg', 'Moderate', 'Cycle 2 weeks on/2 off'],
        ['Rhodiola Rosea', 'Adaptogen — reduces perceived effort', '200–600mg', 'Excellent', 'Consistent use > single dose'],
        ['DMAE', 'Precursor to choline', '300–500mg', 'Good', 'May cause vivid dreams']],
       widths=[105, 140, 90, 80, 110])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — BUILDING YOUR CUSTOM STACK', s['ChHead']))
    hr(story)
    story.append(Paragraph('Custom Pre-Workout Tiers', s['SecHead']))
    tb(story, ['Tier', 'Budget', 'Stack', 'Expected Benefit'],
       [['Essential (low budget)', '<₹1000/month', 'Caffeine (200mg) + Creatine 5g', 'Performance +8%, strength +5%'],
        ['Standard', '₹1000–3000/month', '+ Citrulline 6g + Beta-Alanine 3.2g', 'Performance +15%, endurance +12%'],
        ['Advanced', '₹3000–6000/month', '+ Alpha-GPC + Beetroot + Tyrosine', 'Maximum focus + blood flow + performance'],
        ['Elite', '>₹6000/month', 'Full stack + systematic caffeine cycling', 'Peak optimisation protocol']],
       widths=[100, 110, 175, 140])
    story.append(Paragraph('30-Minute Pre-Workout Protocol', s['SecHead']))
    bl(story, s, [
        'T – 90 min: Meal if using food-based pre-workout. 40g carbs + 30g protein',
        'T – 60 min: Citrulline 6g + Beta-Alanine 3.2g + Beetroot 500mg',
        'T – 45 min: Caffeine dose (capsule or black coffee)',
        'T – 20 min: Alpha-GPC or Tyrosine (cognitive focus)',
        'T – 5 min: Warm-up begins. Mental priming — set your session intention',
    ])
    co(story, s, 'The best pre-workout ever created is not available in any store: 8 hours of quality sleep, a well-timed protein and carb meal, strong intention, and a playlist that elevates your state.')

mk(os.path.join(OUT, '13_PreWorkout_Optimization_Guide.pdf'), 13,
   'Pre-Workout Optimisation Guide', 'Evidence-Based Performance Enhancement Before Every Session',
   ['5 Chapters', 'Science-Based', 'Custom Stack Builder', 'All Levels'], pdf13)

# ─── PDF 14 — Natural Testosterone Optimisation ──────────────────────────────
def pdf14(story, s):
    toc(story, s, [
        ('Testosterone: Physiology & Natural Production', 3),
        ('Lifestyle Factors That Drive Testosterone Up', 4),
        ('Nutrition for Natural Testosterone Production', 5),
        ('Evidence-Based Natural Testosterone Supplements', 6),
        ('Training Protocols for Maximum Natural T', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — TESTOSTERONE PHYSIOLOGY', s['ChHead']))
    hr(story)
    qt(story, s, 'Natural testosterone optimisation is not about reaching pharmacological levels. It is about ensuring you reach your genetic ceiling — and most men fall 30–50% short of it due to lifestyle.')
    story.append(Paragraph('Testosterone is produced primarily in the Leydig cells of the testes in response to Luteinising Hormone (LH) released by the pituitary gland. The Hypothalamic-Pituitary-Gonadal (HPG) axis regulates this cascade — the hypothalamus releases GnRH, which stimulates the pituitary to release LH and FSH, which in turn stimulate testicular testosterone production. Natural optimisation targets every level of this axis.', s['Body']))
    tb(story, ['HPG Axis Level', 'Hormone', 'Natural Optimisation Method'],
       [['Hypothalamus', 'GnRH pulsatile release', 'Reduce cortisol, ensure adequate sleep, maintain body fat < 20%'],
        ['Pituitary', 'LH + FSH release', 'Zinc adequacy, vitamin D, avoid excess oestrogen from adipose tissue'],
        ['Testes', 'Testosterone synthesis', 'Cholesterol substrate, LH signal, temperature (avoid tight underwear, hot baths)'],
        ['Circulation', 'Free vs bound T', 'Reduce SHBG: avoid excess alcohol, manage insulin, boron supplementation']],
       widths=[105, 100, 320])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — LIFESTYLE FACTORS', s['ChHead']))
    hr(story)
    tb(story, ['Factor', 'Effect on Testosterone', 'Magnitude', 'Actionable Target'],
       [['Sleep (quantity)', 'Direct: GH + T synthesised during SWS', '−15% per hour below 7h', '7–9 hours consistently'],
        ['Sleep (quality)', 'Deep sleep phases produce GH + T', 'Up to −30% with poor quality', 'Dark, cool room; address sleep apnoea'],
        ['Body fat %', 'Adipose tissue converts T → E2 (aromatase)', '−1–3% T per 1% BF above 20%', 'Maintain < 15–18% for men'],
        ['Chronic stress', 'Cortisol competes with T for precursors', 'Up to −20–40% with chronic stress', 'Stress management non-negotiable'],
        ['Alcohol', 'Inhibits Leydig cell function acutely', '−25% for 24h after heavy drinking', 'Limit to < 2 drinks/occasion'],
        ['Sunlight / D3', 'Vitamin D receptor in Leydig cells', '+25% T increase with D3 normalisation', '20 min sunlight daily or supplement']],
       widths=[110, 125, 100, 145])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — NUTRITION FOR TESTOSTERONE', s['ChHead']))
    hr(story)
    qt(story, s, 'Testosterone is synthesised from cholesterol. A zero-fat diet is a zero-testosterone diet. Dietary fat is not the enemy.')
    tb(story, ['Nutrient', 'Testosterone Role', 'Target', 'Best Indian Sources'],
       [['Dietary Fat', 'Cholesterol precursor for T synthesis', '0.8–1.2g/kg BW/day', 'Eggs, ghee, nuts, coconut, full-fat dairy'],
        ['Zinc', 'Co-factor for testosterone synthesis + 5-ARD', '25–40mg/day', 'Pumpkin seeds, meat, shellfish'],
        ['Vitamin D3', 'Leydig cell receptor ligand', '4000–6000 IU/day', 'Sun exposure + D3 supplement'],
        ['Magnesium', 'Reduces SHBG binding (frees T)', '400–500mg/day', 'Dark leafy greens, seeds, supplement'],
        ['Boron', 'Reduces SHBG, increases free T', '6–10mg/day', 'Supplement (not well-sourced in food)'],
        ['Omega-3', 'Reduces inflammation → less T suppression', '2–3g EPA/DHA/day', 'Fatty fish (salmon), flaxseed, capsules']],
       widths=[90, 130, 90, 165])
    bl(story, s, [
        'Avoid: excessive soy — phytoestrogens weakly compete at E2 receptors',
        'Avoid: processed vegetable oils (omega-6 dominant) — pro-inflammatory, suppresses T',
        'Include: cruciferous vegetables (broccoli, cauliflower) — DIM reduces E2 conversion',
        'Include: garlic and onion — allicin and quercetin support Leydig cell function',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — NATURAL TESTOSTERONE SUPPLEMENTS', s['ChHead']))
    hr(story)
    tb(story, ['Supplement', 'Evidence Grade', 'Effect', 'Dose', 'Realistic Expectation'],
       [['Ashwagandha (KSM-66)', 'B (good RCT evidence)', 'T +10–20%, cortisol −25%', '600mg/day', 'Noticeable in 8–12 weeks'],
        ['Vitamin D3', 'B (strong correlation)', 'T +25% in D3-deficient men', '4000–6000 IU/day', 'Significant if deficient (most Indians are)'],
        ['Zinc', 'B (especially if deficient)', 'T restoration in deficiency', '25–40mg/day', 'Significant if deficient; minimal if replete'],
        ['Boron', 'C (modest evidence)', 'Free T +28% (one key study)', '6–10mg/day', 'Modest, consistent benefit'],
        ['Fenugreek (Testofen)', 'B (several RCTs)', 'Free T +17%, libido improvement', '600mg standardised', 'Noticeable libido effect'],
        ['Tongkat Ali (LJ100)', 'B (good evidence)', 'T +37% (stressed, older men)', '200–400mg/day', 'Strong for men with stress or suboptimal T'],
        ['D-Aspartic Acid', 'C (inconsistent)', 'Short-term LH stimulus', '2–3g/day', 'Minimal in healthy young men']],
       widths=[110, 80, 130, 90, 115])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — TRAINING FOR MAXIMUM NATURAL T', s['ChHead']))
    hr(story)
    tb(story, ['Training Variable', 'Testosterone Effect', 'Optimal Range', 'Common Mistake'],
       [['Resistance training', 'Acute T spike + chronic elevation', '3–5 sessions/week', 'Too much volume → cortisol > T'],
        ['Compound movements', 'More T release than isolation', 'Squat, deadlift, bench = priority', 'All machines, no compounds'],
        ['Intensity (load)', 'Heavy loads (75–85% 1RM) = highest T response', '3–8 rep range ideal', 'All light weight high reps'],
        ['Session duration', 'T begins declining after 45–60 min', '45–70 min max', 'Long 90–120 min sessions'],
        ['Rest periods', 'Short rest (<60 sec) elevates T acutely', '90–120 sec balanced', 'Marathon rest (3–5 min for T impact)']],
       widths=[110, 140, 120, 155])
    co(story, s, 'The highest natural T-producing training protocol: heavy compound movements (squat, deadlift, bench, rows) at 75–85% 1RM, 3–5 sets, 3–5 reps, 4–5 sessions per week, 60 min max duration.')

mk(os.path.join(OUT, '14_Natural_Testosterone_Optimization.pdf'), 14,
   'Natural Testosterone Optimisation', 'Maximise Your Natural T Production Through Lifestyle, Nutrition & Training',
   ['5 Chapters', 'Natural Methods Only', 'Evidence-Based', 'All Men'], pdf14)

# ─── PDF 15 — Recovery, Sleep & CNS Restoration ──────────────────────────────
def pdf15(story, s):
    toc(story, s, [
        ('Why Recovery Is Your Most Important Training Variable', 3),
        ('Sleep Architecture & Optimisation', 4),
        ('CNS Recovery: Monitoring & Restoration', 5),
        ('Active Recovery Techniques', 6),
        ('Supplement Stack for Recovery', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — RECOVERY: YOUR MOST IMPORTANT VARIABLE', s['ChHead']))
    hr(story)
    qt(story, s, 'You do not get fit from training. You get fit from recovering from training. Training is only the stimulus.')
    story.append(Paragraph('Recovery is the biological process by which the body repairs and adapts to the stress of training. Muscle protein synthesis, glycogen replenishment, hormonal restoration, and connective tissue repair all occur during recovery — not during training. The training session provides the stimulus; recovery provides the adaptation. Elite athletes do not train harder than amateurs — they recover better.', s['Body']))
    tb(story, ['Recovery System', 'Primary Process', 'Time Required', 'Bottleneck Factor'],
       [['Muscle tissue', 'Protein synthesis, satellite cell activation', '24–72 hours', 'Protein intake, sleep quality'],
        ['Glycogen', 'Glucose conversion and storage', '12–24 hours', 'Carbohydrate intake timing'],
        ['Central Nervous System', 'Neurotransmitter replenishment', '24–96 hours (heavy sessions)', 'Sleep, intensity management'],
        ['Connective tissue', 'Collagen synthesis, tendon remodelling', '72 hours to weeks', 'Vitamin C, collagen, hydration'],
        ['Hormonal', 'Cortisol normalisation, T restoration', '24–48 hours', 'Sleep, stress management']],
       widths=[110, 155, 100, 160])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — SLEEP ARCHITECTURE & OPTIMISATION', s['ChHead']))
    hr(story)
    qt(story, s, 'The majority of your testosterone and growth hormone is released during deep sleep. Miss the sleep; miss the gains.')
    tb(story, ['Sleep Stage', 'Duration per Cycle', 'Recovery Function', 'Disrupted By'],
       [['N1 (Light Sleep)', '5–10 min', 'Transition to deeper stages', 'Noise, light, anxiety'],
        ['N2 (NREM)', '20–25 min', 'Memory consolidation, cell repair', 'Inconsistent schedule'],
        ['N3 (Deep / SWS)', '20–40 min', 'GH release, muscle repair, immune function', 'Alcohol, stimulants, stress'],
        ['REM', '20–25 min', 'Brain recovery, emotional processing', 'Alcohol, THC, late meals']],
       widths=[110, 90, 175, 150])
    story.append(Paragraph('Sleep Optimisation Protocol', s['SecHead']))
    bl(story, s, [
        'Consistent sleep/wake schedule — same time 7 days per week (most important variable)',
        'Room temperature: 18–20°C — core temperature drop initiates and maintains sleep',
        'Complete darkness: blackout curtains or sleep mask — even faint light disrupts melatonin',
        'No screens 60–90 min before bed — blue light suppresses melatonin by up to 50%',
        'No alcohol: disrupts REM and N3 sleep even at low doses',
        'Last meal 2–3 hours before bed — digestion increases core temperature',
        'Magnesium glycinate 300mg before bed — proven to increase deep sleep duration',
        'Consistent morning light exposure: 10+ min direct sunlight anchors circadian rhythm',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — CNS RECOVERY MONITORING', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Central Nervous System (CNS) is often the limiting factor in high-frequency training. Unlike muscles, CNS fatigue is not visible and is easily confused with laziness or lack of motivation. Systematic monitoring prevents overtraining and ensures training quality remains high.', s['Body']))
    tb(story, ['CNS Fatigue Indicator', 'How to Measure', 'Action Threshold', 'Recovery Protocol'],
       [['Morning resting HR', 'Check on waking before rising', '+7 BPM above baseline', 'Reduce intensity/volume that day'],
        ['Grip strength test', 'Dynamometer or hang test', '> 5% below baseline', 'De-load or rest day'],
        ['HRV (Heart Rate Variability)', 'HRV4Training app, Oura Ring', '> 2 RMSSD below 7-day avg', 'Active recovery only'],
        ['Mood/motivation (1–10)', 'Daily journal rating', 'Score < 5 for 3+ days', 'Mandatory rest or deload week'],
        ['Sleep quality rating', 'Morning score 1–10', '< 6 for 3+ days', 'Address sleep environment first']],
       widths=[115, 120, 115, 125])
    co(story, s, 'A deload week (50–60% of normal volume at normal intensity) every 4–6 weeks prevents accumulated CNS fatigue. Plan it proactively — do not wait for forced rest from injury.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — ACTIVE RECOVERY TECHNIQUES', s['ChHead']))
    hr(story)
    tb(story, ['Technique', 'Mechanism', 'Duration', 'Frequency', 'Evidence Grade'],
       [['Zone 2 Walking', 'Blood flow, lactate clearance, fat oxidation', '30–45 min', 'Daily', 'A (very strong)'],
        ['Foam Rolling', 'Fascial pressure, pain reduction, mobility', '10–15 min', 'Post-training', 'B (good)'],
        ['Contrast Showers', 'Vasoconstriction/dilation, lymphatic', '10 min (alternating)', '4× per week', 'B (good)'],
        ['Yoga / Stretching', 'ROM, parasympathetic activation', '20–30 min', '3–4× per week', 'B (good)'],
        ['Cold Water Immersion', 'Inflammation reduction (acute)', '10–15 min at 10–15°C', '2–3× per week', 'B (moderate)'],
        ['Sauna', 'Heat shock proteins, GH release', '15–20 min at 80–100°C', '2–3× per week', 'B (growing)'],
        ['Massage', 'DOMS reduction, tissue quality', '60 min', 'Weekly', 'A (strong for DOMS)']],
       widths=[115, 130, 90, 80, 80])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — SUPPLEMENT STACK FOR RECOVERY', s['ChHead']))
    hr(story)
    qt(story, s, 'The best recovery supplement stack contains nothing exotic — sleep, protein, creatine, and consistency outperform every trending product.')
    tb(story, ['Supplement', 'Recovery Role', 'Dose', 'Timing', 'Priority'],
       [['Magnesium Glycinate', 'Deep sleep quality, muscle relaxation', '300–400mg', 'Before bed', 'Essential'],
        ['Creatine', 'PCr replenishment, cell hydration', '5g/day', 'Any time (consistent)', 'Essential'],
        ['Whey / Casein Protein', 'MPS substrate provision', '30–40g', 'Post-workout + pre-sleep', 'Essential'],
        ['Tart Cherry Extract', 'Antioxidant, DOMS reduction, melatonin', '480mg twice daily', 'Morning + evening', 'High'],
        ['Collagen + Vitamin C', 'Tendon/ligament synthesis', '15g + 500mg Vit C', '1h pre-training', 'High'],
        ['Ashwagandha', 'Cortisol reduction, sleep quality', '600mg', 'Evening', 'Moderate'],
        ['Melatonin (if needed)', 'Sleep onset (circadian support)', '0.5–1mg', '30 min before bed', 'Situational'],
        ['BPC-157 (advanced)', 'Accelerated tissue repair', '250–500mcg/day', 'SubQ near injury', 'Advanced only']],
       widths=[115, 130, 80, 90, 80])
    bl(story, s, [
        'Recovery nutrition window: 30g protein + 50–80g carbs within 2 hours post-training',
        'Hydration: minimum 3L/day — dehydration by even 2% significantly impairs recovery',
        'Alcohol: even 2–3 drinks reduces muscle protein synthesis by 37% for 12–24 hours',
    ])

mk(os.path.join(OUT, '15_Recovery_Sleep_CNS_Restoration.pdf'), 15,
   'Recovery, Sleep & CNS Restoration', 'Complete System for Maximising Recovery Between Sessions',
   ['5 Chapters', 'Sleep Science', 'CNS Monitoring', 'Evidence-Based'], pdf15)

print('\n[PDFs 11-15 complete]')
