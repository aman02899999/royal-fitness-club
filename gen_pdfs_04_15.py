#!/usr/bin/env python3
"""Generate catalog PDFs 04-15 with full content."""
import io, os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from PyPDF2 import PdfReader

os.chdir('/home/user/royal-fitness-club')

def make_pdf(filename, title, subtitle, accent_hex, chapters):
    accent = colors.HexColor(accent_hex)
    LB = colors.Color(accent.red, accent.green, accent.blue, alpha=0.07)
    s = getSampleStyleSheet()
    def add(name, **kw):
        if name not in s: s.add(ParagraphStyle(name=name, **kw))
        else: [setattr(s[name], k, v) for k, v in kw.items()]
    add('H1', fontName='Helvetica-Bold', fontSize=20, textColor=accent, spaceAfter=10, spaceBefore=14, leading=25)
    add('H2', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#1a1a2e'), spaceAfter=7, spaceBefore=10, leading=18)
    add('Body', fontName='Helvetica', fontSize=11, spaceAfter=6, leading=16, textColor=colors.HexColor('#333333'))
    add('BL', fontName='Helvetica', fontSize=11, spaceAfter=4, leading=15, leftIndent=14, textColor=colors.HexColor('#333333'))
    add('TH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, leading=13)
    add('TC', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#1a1a2e'), leading=13)

    def h1(t): return Paragraph(t, s['H1'])
    def h2(t): return Paragraph(t, s['H2'])
    def p(t): return Paragraph(t, s['Body'])
    def bl(t): return Paragraph(f'• {t}', s['BL'])
    def sp(n=6): return Spacer(1, n*mm)
    def hr(): return HRFlowable(width='100%', thickness=1, color=accent, spaceAfter=5, spaceBefore=5)

    def tbl(rows, widths):
        t = Table(rows, colWidths=widths)
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),accent), ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LB]),
            ('BOX',(0,0),(-1,-1),1,accent),
            ('INNERGRID',(0,0),(-1,-1),0.5,colors.Color(accent.red,accent.green,accent.blue,0.3)),
            ('PADDING',(0,0),(-1,-1),7), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        return t

    def hrow(data): return [Paragraph(c, s['TH']) for c in data]
    def drow(data): return [Paragraph(c, s['TC']) for c in data]

    def ibox(title_txt, items):
        rows = [[Paragraph('<b>' + title_txt + '</b>', s['H2'])]]
        for it in items:
            rows.append([Paragraph('• ' + it, s['TC'])])
        t = Table(rows, colWidths=[155*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),accent), ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('BACKGROUND',(0,1),(-1,-1),LB), ('BOX',(0,0),(-1,-1),1,accent),
            ('INNERGRID',(0,0),(-1,-1),0.5,colors.Color(accent.red,accent.green,accent.blue,0.3)),
            ('PADDING',(0,0),(-1,-1),7),
        ]))
        return t

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    story = []
    story += [Table([[
        Paragraph('ROYAL FITNESS CLUB', ParagraphStyle('ct', fontName='Helvetica-Bold', fontSize=12, textColor=colors.white, alignment=1)),
        Paragraph(title, ParagraphStyle('tt', fontName='Helvetica-Bold', fontSize=24, textColor=colors.white, alignment=1, leading=30)),
        Paragraph(subtitle, ParagraphStyle('st', fontName='Helvetica', fontSize=13, textColor=colors.Color(1,1,1,0.85), alignment=1, leading=17)),
    ]], colWidths=[155*mm], style=TableStyle([('BACKGROUND',(0,0),(-1,-1),accent), ('PADDING',(0,0),(-1,-1),32)])), sp(10)]

    for i, chapter in enumerate(chapters):
        if i > 0: story.append(PageBreak())
        story.append(h1(chapter['title']))
        story.append(hr())
        for item in chapter['content']:
            t = item[0]
            if t == 'p':   story.append(p(item[1]))
            elif t == 'h2': story.append(h2(item[1]))
            elif t == 'bl': [story.append(bl(x)) for x in item[1]]
            elif t == 'sp': story.append(sp(item[1]))
            elif t == 'tbl':
                rd, widths = item[1], item[2]
                rows = [hrow(rd[0])] + [drow(r) for r in rd[1:]]
                story.append(tbl(rows, [w*mm for w in widths]))
            elif t == 'ibox':
                story.append(ibox(item[1], item[2]))
        story.append(sp())

    doc.build(story)
    with open('generated_pdfs/' + filename, 'wb') as f: f.write(buf.getvalue())
    n = len(PdfReader(io.BytesIO(buf.getvalue())).pages)
    print('  ' + filename + ': ' + str(n) + ' pages')

# ── PDF 04: 30-Day Keto Indian Vegetarian ─────────────────────────────────────
make_pdf('04_30Day_Keto_Indian_Vegetarian_Plan.pdf',
  '30-DAY KETO INDIAN PLAN', 'Vegetarian · Desi-Friendly Meal Templates', '#15803d', [
  {'title': 'Ch 1: Keto Fundamentals', 'content': [
    ('p','A ketogenic diet restricts carbohydrates to under 50g/day, shifting the body from glucose to ketones derived from fat. For Indians, going keto means replacing rice, roti, and dal with low-carb Indian alternatives without losing the flavours of desi cuisine.'),
    ('tbl',[['Macro','Standard Keto %','Grams/day (2000 kcal)','Indian Vegetarian Sources'],
      ['Fat','65–75%','145–165g','Ghee, coconut oil, paneer, nuts, avocado, heavy cream'],
      ['Protein','20–25%','100–125g','Paneer, tofu, soya chunks, eggs, full-fat curd, cheese'],
      ['Net Carbs','< 5%','< 25g','Leafy greens, cauliflower, brinjal, zucchini, mushrooms'],
    ],[22,22,32,79]),
  ]},
  {'title': 'Ch 2: Indian Food Swaps', 'content': [
    ('p','The key to sustainable Indian keto is finding satisfying replacements for high-carb staples. The following swaps maintain cultural and flavour experience while keeping net carbs under 25g per day.'),
    ('tbl',[['Keto Replacement','Net Carbs','High-Carb Original','Net Carbs','Carbs Saved'],
      ['Almond flour roti (1 piece)','2g','Wheat roti (1 piece)','25g','23g'],
      ['Cauliflower rice (1 cup)','3g','White rice (1 cup)','45g','42g'],
      ['Coconut cream curry base','3g','Onion-tomato base (1/2 cup)','12g','9g'],
      ['Erythritol/stevia halwa','2g','Sugar-based mithai (1 piece)','25–35g','23–33g'],
      ['Paneer tikka snack','2g','Samosa (1 piece)','20g','18g'],
      ['Soya granules dry sabzi','5g','Chana dal (1 cup cooked)','28g','23g'],
      ['Egg/paneer bhurji','3g','Poha (1 cup)','32g','29g'],
    ],[40,16,40,16,23]),
  ]},
  {'title': 'Ch 3: 4-Week Meal Plan', 'content': [
    ('tbl',[['Week','Theme','Daily Net Carbs','Calorie Target','Key Focus'],
      ['Week 1','Keto adaptation','20–25g','1800–2000','Enter ketosis; manage keto flu'],
      ['Week 2','Fat adaptation','20–25g','1800–2000','Energy stabilises; hunger decreases'],
      ['Week 3','Optimisation','15–20g','1700–1900','Deepen ketosis; introduce 16:8 IF'],
      ['Week 4','Consolidation','15–20g','1600–1800','Maximum fat loss; sustain ketones'],
    ],[18,28,26,28,55]),
    ('sp',5),
    ('h2','Sample Day Meal Plan'),
    ('tbl',[['Meal','Food','kcal','Net Carbs','Protein'],
      ['Breakfast 7 AM','3-egg bhurji in ghee + 1 almond roti + black chai','360','5g','22g'],
      ['Lunch 12:30 PM','150g paneer butter masala (cream-based) + cauliflower rice','500','8g','28g'],
      ['Snack 4 PM','Mixed nuts + string cheese + bulletproof coffee','290','3g','12g'],
      ['Dinner 7:30 PM','Palak paneer (cream gravy) + 1 almond roti + salad','480','7g','30g'],
      ['Pre-sleep','Whey isolate 30g + MCT tea','170','2g','25g'],
      ['TOTAL','','1,800','25g','117g'],
    ],[28,72,18,20,17]),
  ]},
  {'title': 'Ch 4: Keto Flu & Electrolytes', 'content': [
    ('p','Keto flu (days 3–7) occurs because carbohydrate restriction causes rapid glycogen and water depletion, taking electrolytes with it. It is not a sign of failure — it is a sign you are entering ketosis. Management is entirely nutritional.'),
    ('ibox','Keto Flu Remedies',[
      'Sodium: add salt liberally; have 1–2 cups salted vegetable broth daily',
      'Potassium: eat avocado, spinach, mushrooms; consider potassium chloride (No-Salt)',
      'Magnesium: 300–400mg magnesium glycinate before bed; prevents muscle cramps',
      'Hydration: 3.5–4 litres water daily; add a pinch of Himalayan salt per litre',
      'Headache: usually sodium depletion — try warm salted lemon water first',
      'Fatigue (days 3–5): normal transition; reduce workout intensity temporarily',
      'Constipation: psyllium husk 10g/day + leafy greens + extra water',
    ]),
    ('sp',5),
    ('tbl',[['Ketosis Test Method','Cost','Accuracy','Target'],
      ['Urine ketone strips','Very low (Rs 200/box)','Low once fat-adapted','Trace to moderate'],
      ['Blood ketone meter','Moderate (Rs 1500 + strips)','High','0.5–3.0 mmol/L'],
      ['Breath acetone meter','High (Rs 3000+)','Moderate','Correlation to blood ketones'],
      ['Subjective symptoms','Free','Qualitative','Reduced hunger, mental clarity'],
    ],[38,28,26,63]),
  ]},
  {'title': 'Ch 5: Vegetarian Protein Strategy', 'content': [
    ('p','The biggest challenge of vegetarian keto is hitting protein targets (1.6–2g/kg) while staying under 25g net carbs. Most high-protein Indian foods like dal and legumes are also high in carbs. Focus on the following keto-compatible protein sources.'),
    ('tbl',[['Food','Serving','Protein','Net Carbs','Keto Status'],
      ['Paneer (full fat)','100g','18g','1.2g','Excellent — unlimited'],
      ['Soya chunks (dry)','50g','26g','8g','Good — use daily'],
      ['Whole eggs','3 eggs','18g','1g','Excellent — no limit'],
      ['Tofu (firm)','150g','25g','3g','Excellent — use freely'],
      ['Full-fat curd','200g','7g','6g','Good — 1–2 cups/day'],
      ['Whey isolate','30g scoop','24g','1–2g','Excellent — use daily'],
      ['Moong dal (cooked)','1 cup','14g','20g','Moderate — limits carb budget'],
      ['Rajma/Chana (cooked)','1 cup','15g','28g','Avoid on strict keto'],
    ],[30,20,17,20,68]),
  ]},
  {'title': 'Ch 6: Exercise on Keto + Results Tracker', 'content': [
    ('tbl',[['Exercise Type','Performance on Keto','Recommendation'],
      ['Heavy resistance (1–8 reps)','Slight decrease weeks 1–2','Add 10–25g carbs pre-workout (targeted keto)'],
      ['Moderate hypertrophy (8–15 reps)','Maintained after week 2','No modification needed after adaptation'],
      ['LISS endurance cardio','Excellent once fat-adapted','Best exercise for keto; prioritise LISS'],
      ['HIIT / Sprints','Significantly impaired','Avoid or use targeted/cyclical keto'],
      ['Yoga / Mobility','Unaffected','Ideal keto activity — no glucose dependency'],
    ],[35,45,75]),
    ('sp',5),
    ('tbl',[['Metric','Day 1','Day 7','Day 14','Day 21','Day 30'],
      ['Weight (kg)','','','','',''],
      ['Waist (cm)','','','','',''],
      ['Ketone level (mmol/L)','','','','',''],
      ['Energy (1–10)','','','','',''],
      ['Hunger (1–10)','','','','',''],
      ['Workout performance (1–10)','','','','',''],
    ],[38,22,22,22,22,29]),
  ]},
])

# ── PDF 05: Female Vegetarian Weight Loss ──────────────────────────────────────
make_pdf('05_Female_Vegetarian_Weight_Loss_Plan.pdf',
  'FEMALE VEGETARIAN WEIGHT LOSS', 'Hormone-Safe Protocol · Indian Vegetarian',
  '#be185d', [
  {'title': 'Ch 1: Female Physiology', 'content': [
    ('p','Women\'s bodies respond differently to diet and exercise due to monthly hormonal cycles, higher baseline fat storage requirements, and different muscle fibre composition. An effective female fat-loss plan accounts for these factors rather than fighting against them.'),
    ('tbl',[['Physiological Difference','Impact on Fat Loss','Plan Adjustment'],
      ['Higher oestrogen','Greater fat storage at hips, thighs, and glutes','Strength training to change body shape, not just scale weight'],
      ['Monthly cycle','Energy and strength vary predictably by phase','Periodise training intensity and calories with the cycle'],
      ['Lower testosterone','Slower muscle building than men','Higher relative protein; resistance training non-negotiable'],
      ['Thyroid sensitivity','Metabolism adapts faster to caloric deficits','Maximum 400–500 kcal deficit; refeed weeks every 3–4 weeks'],
      ['PCOS (10–20% of women)','Insulin resistance, irregular cycles, higher androgens','Lower-GI carbs; strength training; myo-inositol supplement'],
    ],[40,42,73]),
  ]},
  {'title': 'Ch 2: Cycle Syncing Training', 'content': [
    ('p','Aligning training with your hormonal cycle leverages natural fluctuations to time hardest sessions when physiologically primed, and recovery sessions when the body needs restoration.'),
    ('tbl',[['Phase','Days','Dominant Hormone','Training Style','Nutrition Adjustment'],
      ['Menstrual','1–5','Low E + progesterone','Light: yoga, walk, gentle mobility','Warm iron-rich foods; extra magnesium'],
      ['Follicular','6–13','Rising oestrogen','High intensity; best time for new PRs','Normal deficit; carbs around workouts'],
      ['Ovulation','14','Oestrogen peak','Maximum strength and HIIT output','Maintenance calories; highest protein day'],
      ['Luteal','15–28','Progesterone dominant','Moderate; reduce HIIT frequency','Add 150–200 kcal; expect 1–2 kg water weight'],
    ],[18,14,30,42,51]),
  ]},
  {'title': 'Ch 3: 12-Week Meal Plan', 'content': [
    ('p','Calibrated for a 55–65 kg woman targeting 1,600–1,800 kcal/day with a 400–500 kcal deficit. All meals use Indian vegetarian ingredients available in any Indian kitchen or market.'),
    ('tbl',[['Meal','Food','kcal','Protein'],
      ['Breakfast 7 AM','3 moong dal chilla + green chutney + green chai (no sugar)','330','18g'],
      ['Mid-morning 10 AM','1 cup low-fat curd + pomegranate seeds + 5 almonds','185','9g'],
      ['Lunch 1 PM','1 cup rajma + 2 small roti + mixed sabzi + kachumber salad','420','20g'],
      ['Pre-workout 4 PM','1 banana + 1 tsp peanut butter','200','4g'],
      ['Post-workout 6 PM','50g soya chunks bhurji + 1 cup low-fat curd','250','28g'],
      ['Dinner 8 PM','100g paneer bhurji + 1 roti + cucumber raita','370','24g'],
      ['TOTAL','','1,755 kcal','103g'],
    ],[28,80,22,25]),
  ]},
  {'title': 'Ch 4: 12-Week Training Programme', 'content': [
    ('tbl',[['Phase','Weeks','Sessions/Week','Focus','Key Exercises'],
      ['Foundation','1–3','3 full body + 2 cardio','Movement patterns; form mastery','Goblet squat, push-up, DB row, plank holds'],
      ['Build','4–6','3 strength + 2 LISS','Progressive overload begins','DB squat, DB bench, lat pulldown, RDL'],
      ['Sculpt','7–9','4 strength + 2 HIIT','Volume + targeted isolation','Barbell squat, bench, deadlift, glute work'],
      ['Shred','10–12','5 sessions + 3 HIIT','Intensity maximisation','Full compound programme + finishers'],
    ],[18,16,28,32,61]),
    ('sp',5),
    ('h2','Glute Development Protocol'),
    ('tbl',[['Exercise','Sets x Reps','Key Cue','Progression'],
      ['Hip thrust (barbell/band)','4 x 10–12','Squeeze glutes at top; 2-second hold','Add 2.5 kg when 12 reps clean'],
      ['Romanian Deadlift','3 x 10–12','Push hips back; feel hamstring stretch','Add 2.5 kg weekly'],
      ['Bulgarian Split Squat','3 x 10/side','Front foot forward; slight forward lean','Add DB when bodyweight is easy'],
      ['Cable kickback','3 x 15/side','Extend at hip only; no knee swing','Increase cable weight monthly'],
      ['Sumo squat','4 x 12','Toes out 45; sit back into hips','Add weight or goblet hold'],
    ],[38,26,55,36]),
  ]},
  {'title': 'Ch 5: Supplements for Indian Women', 'content': [
    ('tbl',[['Supplement','Dose','Purpose','Cost/Month (approx)'],
      ['Whey protein (vegetarian)','20–25g post-workout','Hit protein targets on veg diet','Rs 800–1500'],
      ['Iron','18–27mg elemental','Prevent anaemia (esp. menstruation)','Rs 100–200'],
      ['Vitamin D3 + K2','2000–5000 IU + 100mcg K2','Bone health, hormones, mood','Rs 150–300'],
      ['Omega-3 algae-based','1–2g EPA+DHA','Anti-inflammatory; hormone balance','Rs 600–1200'],
      ['Myo-Inositol (PCOS)','2–4g/day','Insulin sensitivity; menstrual regulation','Rs 400–800'],
      ['Calcium + Magnesium','500mg Ca + 300mg Mg','Bone density, PMS reduction, sleep','Rs 200–400'],
      ['Vitamin B12','500–1000 mcg','Essential; vegetarians commonly deficient','Rs 100–200'],
    ],[38,26,52,39]),
  ]},
  {'title': 'Ch 6: Mindset & Long-Term Success', 'content': [
    ('ibox','Managing the Luteal Phase (Days 15–28) — When Willpower Feels Lowest',[
      'Expect: increased appetite; 1–2 kg water weight gain; lower energy — all NORMAL',
      'Do not: crash diet, skip meals, punish yourself, or do extreme HIIT when exhausted',
      'Do: add 150–200 kcal of complex carbs; allow strength training; prioritise sleep 8+ hrs',
      'Remind yourself: scale weight increase is water/glycogen — your fat loss is still on track',
      'Track weekly averages, not daily weights — luteal fluctuations obscure real progress',
    ]),
    ('sp',5),
    ('ibox','12-Week Progress Metrics',[
      'Body measurements (waist, hips, thighs) — more informative than scale alone for women',
      'Progress photos every 2 weeks: same lighting, clothing, and pose',
      'Strength benchmarks: hip thrust 1RM, squat, push-up reps — performance reflects recomp',
      'Energy levels, sleep quality, cycle regularity — hormonal health indicators',
      'Blood markers at 12 weeks: iron, D3, B12, fasting insulin, thyroid if symptomatic',
    ]),
  ]},
])

# ── PDF 06: Complete Peptide Protocol Bible ─────────────────────────────────────
make_pdf('06_Complete_Peptide_Protocol_Bible.pdf',
  'COMPLETE PEPTIDE PROTOCOL BIBLE', 'All Major Peptides · Scientific Reference',
  '#3730a3', [
  {'title': 'Ch 1: Peptide Fundamentals', 'content': [
    ('p','Peptides are short chains of amino acids (2–50 AAs) that act as signalling molecules. Unlike anabolic steroids, most peptides work by stimulating the body\'s own hormone production rather than replacing it. This makes them a unique category of performance compounds.'),
    ('tbl',[['Peptide Category','Examples','Primary Action','Main Application'],
      ['GHRPs (GH-releasing peptides)','GHRP-2, GHRP-6, Ipamorelin','Stimulate GH pulse from pituitary','Mass gain, fat loss, recovery'],
      ['GHRHs (GH-releasing hormones)','CJC-1295, Sermorelin, Tesamorelin','Extend and amplify GH pulse','Synergy with GHRPs'],
      ['Repair peptides','BPC-157, TB-500','Tissue healing, angiogenesis','Injury recovery, gut repair'],
      ['Metabolic peptides','AOD-9604, Fragment 176-191','Fat cell lipolysis stimulation','Fat loss without muscle loss'],
      ['Melanocortin peptides','PT-141, Melanotan II','CNS and melanocortin activation','Libido enhancement, tanning'],
      ['Cognitive peptides','Semax, Selank','Neuroprotection, BDNF increase','Focus, anxiety, recovery'],
    ],[28,38,48,41]),
  ]},
  {'title': 'Ch 2: GH-Releasing Peptide Profiles', 'content': [
    ('tbl',[['Peptide','Effective Dose','Frequency','Half-life','Key Side Effects','Best Use Case'],
      ['GHRP-6','100–200 mcg','3x/day','< 30 min','Hunger spike, cortisol rise','Mass gain; appetite stimulation'],
      ['GHRP-2','100–200 mcg','3x/day','< 30 min','Cortisol, prolactin elevation','GH pulse without hunger'],
      ['Ipamorelin','200–300 mcg','2–3x/day','2 hours','Minimal','Cleanest GHRP; best for beginners'],
      ['Hexarelin','200 mcg','2x/day','< 30 min','Desensitisation, cardiac effects','Short cycles only; powerful'],
      ['CJC-1295 (DAC)','2 mg/week','1–2x/week','8 days','Blunted natural GH pulses','Steady GH elevation; anti-aging'],
      ['CJC-1295 (no DAC)','100 mcg','3x/day with GHRP','30 min','Minimal','Best synergy with GHRPs'],
      ['Sermorelin','200–500 mcg','Before sleep','12 min','Injection site reaction','Anti-aging; sleep GH optimisation'],
    ],[30,25,24,20,40,36]),
  ]},
  {'title': 'Ch 3: BPC-157 Complete Guide', 'content': [
    ('p','Body Protection Compound 157 (BPC-157) is a 15-amino acid peptide derived from a protein in gastric juice. It shows extraordinary tissue-healing properties and is the most researched peptide for injury recovery.'),
    ('tbl',[['Condition','Protocol','Route','Duration','Expected Outcome'],
      ['Tendon/ligament injury','250 mcg 2x/day near injury site','Subcutaneous or oral','4–8 weeks','Accelerated healing; reduced pain'],
      ['Muscle tear','250–500 mcg/day near tear','Subcutaneous','2–4 weeks','Faster fibre repair; less scar tissue'],
      ['GI issues (IBS, leaky gut)','250 mcg 2x/day','Oral (capsule in water)','8–12 weeks','Gut lining repair; reduced inflammation'],
      ['General recovery (on cycle)','200 mcg/day','Subcutaneous any site','Duration of cycle','Prevents joint damage; recovery speed'],
    ],[38,30,25,22,40]),
  ]},
  {'title': 'Ch 4: Peptide Stacking Protocols', 'content': [
    ('tbl',[['Goal','Peptide Stack','Daily Dose','Timing','Duration'],
      ['Maximum GH pulse','Ipamorelin + CJC-1295 no DAC','300 + 100 mcg each','Fasted AM + pre-sleep','12 weeks on, 4 off'],
      ['Injury recovery','BPC-157 + TB-500','250 mcg + 2mg/wk','BPC 2x/day; TB weekly','Until healed + 2 wks'],
      ['Body recomposition','AOD-9604 + Ipamorelin','300 + 300 mcg','AM fasted + pre-sleep','16 weeks'],
      ['Anti-aging protocol','Sermorelin + BPC-157','500 + 250 mcg','Pre-sleep + AM','Ongoing (12 on/4 off)'],
      ['Bulking assist','GHRP-6 + CJC no DAC + BPC-157','200+100+250 mcg','3x/day (GHRP/CJC); BPC 2x','Duration of cycle'],
    ],[30,45,30,35,35]),
  ]},
  {'title': 'Ch 5: Reconstitution, Storage & Safety', 'content': [
    ('ibox','Peptide Handling Protocol',[
      'Reconstitute with bacteriostatic water (BacWater) — NOT regular sterile water',
      'Standard dilution: 1 mL BacWater per 2 mg peptide = 2000 mcg/mL concentration',
      'Inject BacWater slowly down the SIDE of the vial — never directly on the powder',
      'Gently swirl to mix — never shake (shaking denatures the peptide)',
      'Unreconstituted: store in freezer up to 2 years; Reconstituted: refrigerator, use within 4 weeks',
      'Syringes: 29–31G insulin syringes; 0.5–1 mL volume',
      'Always allow peptide solution to reach room temperature before injection',
    ]),
    ('sp',5),
    ('tbl',[['Red Flag When Buying Peptides','Why It Matters'],
      ['No HPLC purity certificate from third party','Cannot verify actual peptide content or purity'],
      ['Price far below market average','Likely diluted, counterfeit, or improperly stored'],
      ['No bacteriostatic water provided or sold','Vendor does not understand sterile reconstitution requirements'],
      ['No labelling of amino acid sequence and percentage purity','Cannot confirm correct peptide was synthesised'],
      ['Vendor cannot answer basic reconstitution questions','Indicates lack of genuine product knowledge'],
    ],[55,100]),
  ]},
  {'title': 'Ch 6: Peptide Dosing Reference Card', 'content': [
    ('tbl',[['Peptide','Storage','Reconstitution','Injection Site','Injection Time'],
      ['BPC-157','Freezer (unrecon); Fridge (recon)','250 mcg/0.125 mL if 2000 mcg/mL','Near injury or any subcut site','AM fasted + evening'],
      ['TB-500','Freezer (unrecon); Fridge (recon)','2 mg/1 mL','Any subcutaneous site (abdomen easy)','Once weekly (or split 2x)'],
      ['Ipamorelin','Freezer (unrecon); Fridge (recon)','300 mcg/0.15 mL if 2000 mcg/mL','Abdomen subcutaneous','AM fasted; pre-sleep'],
      ['CJC-1295 no DAC','Freezer (unrecon); Fridge (recon)','100 mcg/0.05 mL if 2000 mcg/mL','Abdomen subcutaneous','Same time as Ipamorelin'],
      ['AOD-9604','Freezer (unrecon); Fridge (recon)','300 mcg/0.15 mL if 2000 mcg/mL','Abdomen subcutaneous','AM fasted only'],
    ],[25,35,38,40,17]),
  ]},
])

# ── PDF 07: SARMs Scientific Handbook ──────────────────────────────────────────
make_pdf('07_SARMs_Complete_Scientific_Handbook.pdf',
  'SARMs SCIENTIFIC HANDBOOK', 'Complete Research-Backed Edition',
  '#4338ca', [
  {'title': 'Ch 1: What Are SARMs?', 'content': [
    ('p','Selective Androgen Receptor Modulators (SARMs) bind to androgen receptors with tissue selectivity — targeting muscle and bone while theoretically sparing other androgen-sensitive tissues. Originally developed for muscle-wasting diseases and osteoporosis.'),
    ('tbl',[['Comparison','SARMs','Anabolic Steroids'],
      ['Oral bioavailability','High for most SARMs','Varies; injectables require different delivery'],
      ['Liver toxicity','Low to moderate','Moderate to high for oral 17-alpha alkylated compounds'],
      ['Aromatisation','None for most SARMs','Yes for testosterone-based compounds'],
      ['HPTA suppression','Moderate (dose/compound dependent)','Severe — shuts down natural production'],
      ['Androgenic side effects','Low','High — hair loss, acne, prostate effects'],
      ['Anabolic potential','Moderate','High'],
      ['Legal/regulatory status','Research chemical; not FDA approved for humans','Controlled substances (Schedule III in USA)'],
    ],[40,55,60]),
  ]},
  {'title': 'Ch 2: SARMs Profiles', 'content': [
    ('tbl',[['SARM','Dose mg/day','Half-life','Best Application','HPTA Suppression','Key Note'],
      ['Ostarine (MK-2866)','15–25','24 hrs','Recomp; beginner first SARM','Low–Moderate','Mildest; joint healing benefit'],
      ['RAD-140 (Testolone)','10–20','60 hrs','Strength and mass gain','High','Most anabolic; monitor liver'],
      ['LGD-4033 (Ligandrol)','5–10','24–36 hrs','Lean mass gain','Moderate–High','Dose-dependent suppression'],
      ['Cardarine (GW-501516)','10–20','16–24 hrs','Endurance; fat loss','None (not a SARM)','PPARdelta agonist; cancer studies controversy'],
      ['MK-677 (Ibutamoren)','15–25','24 hrs','GH; sleep; recovery; mass','None (not a SARM)','GH secretagogue; no suppression'],
      ['S-23','10–30','12 hrs','Cutting; muscle hardness','Severe','Most suppressive SARM; full PCT'],
      ['YK-11','5–15','6–10 hrs','Extreme mass gain','High','Partial myostatin inhibitor'],
      ['Andarine (S-4)','25–50','4 hrs','Cutting and recomp','Moderate','Yellow vision tint side effect'],
      ['SR-9009 (Stenabolic)','20–30 (split 4x)','4–6 hrs','Fat loss; endurance','None','Low oral bioavailability issue'],
    ],[30,22,22,40,30,31]),
  ]},
  {'title': 'Ch 3: Stacking Protocols', 'content': [
    ('tbl',[['Goal','Stack','Duration','PCT Needed'],
      ['Beginner recomp','Ostarine 15mg + Cardarine 10mg','8 weeks','Mini-PCT (Nolvadex 20mg x 4 weeks)'],
      ['Lean bulk','LGD-4033 10mg + MK-677 20mg','12 weeks','Full PCT (Nolvadex 40/40/20/20)'],
      ['Aggressive bulk','RAD-140 15mg + LGD-4033 5mg + MK-677 20mg','10 weeks','Full PCT required'],
      ['Cutting phase','Ostarine 20mg + Cardarine 20mg + SR-9009 20mg','8 weeks','Mini-PCT'],
      ['Recomposition','RAD-140 10mg + Cardarine 15mg','8 weeks','Full PCT'],
      ['Endurance only','Cardarine 20mg + SR-9009 30mg','6–8 weeks','No PCT needed'],
    ],[25,62,22,46]),
  ]},
  {'title': 'Ch 4: Health Monitoring', 'content': [
    ('ibox','Required Blood Tests On SARMs',[
      'Pre-cycle: Total T, Free T, LH, FSH, E2, SHBG, liver enzymes (ALT/AST), CBC, lipids',
      'Mid-cycle (week 4–6): Total T, liver enzymes, lipids — check for suppression or liver stress',
      'Post-PCT (4 weeks after): Total T, LH, FSH, E2 — confirm HPTA recovery',
      'Concerning: Total T < 300 ng/dL post-PCT; ALT/AST > 3x baseline; HDL drop > 30%',
      'Recovery timeline: LH/FSH usually return within 4–8 weeks post-SARM cycle',
    ]),
    ('sp',5),
    ('tbl',[['PCT Type','When to Use','Protocol','Duration'],
      ['Mini-PCT','Mild stacks (Ostarine-only, low dose)','Nolvadex 20mg/day','4 weeks'],
      ['Full PCT','Moderate-high suppression (RAD, LGD, S-23)','Nolvadex 40/40/20/20 + Clomid 100/50/50/50','4 weeks'],
      ['Natural recovery only','Non-suppressive compounds (Cardarine, MK-677, SR-9009)','No PCT; supplement support stack only','4–8 weeks'],
    ],[25,52,55,23]),
  ]},
  {'title': 'Ch 5: SARMs Safety Considerations', 'content': [
    ('p','All SARMs currently available are sold as research chemicals — not approved for human use by any regulatory agency. This means product quality is highly variable between suppliers, and long-term human safety data is largely absent. This section covers harm-reduction practices.'),
    ('tbl',[['Risk','Evidence Level','Harm Reduction'],
      ['Liver toxicity (mild-moderate)','Some studies show ALT elevation','Run liver support: TUDCA 250mg + NAC 400mg daily on cycle'],
      ['HPTA suppression','Well-established','Always run PCT; blood test before and after'],
      ['Cardiovascular (lipid changes)','HDL reduction documented','Omega-3 4g/day; cardio; monitor blood lipids mid-cycle'],
      ['Long-term safety unknown','No long-term human studies','Limit cycle lengths; time off between cycles'],
      ['Counterfeit or mislabelled products','Very common in grey market','Purchase only from vendors with HPLC testing certificates'],
    ],[25,30,100]),
    ('sp',5),
    ('ibox','Signs of SARM Suppression (Get Blood Work If You Experience These)',[
      'Significant reduction in libido or sexual function during cycle',
      'Fatigue, lethargy, and low motivation not explained by training load',
      'Testicular ache or noticeable size reduction',
      'Mood changes: irritability, depression, emotional blunting',
      'These are hormonal indicators — do not wait; get LH, FSH, Total T tested',
    ]),
  ]},
])

# ── PDF 08: TRT Hormone Optimization ─────────────────────────────────────────
make_pdf('08_TRT_Hormone_Optimization_Guide.pdf',
  'TRT HORMONE OPTIMIZATION GUIDE', 'Testosterone Replacement · Monitoring · Protocols',
  '#b45309', [
  {'title': 'Ch 1: Understanding TRT', 'content': [
    ('p','Testosterone Replacement Therapy restores testosterone to physiological levels in men with clinically diagnosed hypogonadism. At medical TRT doses, the goal is wellness restoration — not supraphysiological performance. Understanding this distinction is critical.'),
    ('tbl',[['TRT Category','Description','Target Total T Level'],
      ['Medical TRT','Prescribed by doctor; restores to normal physiological range','400–700 ng/dL'],
      ['Optimised TRT','Slightly above average normal; enhanced wellbeing and body composition','700–1000 ng/dL'],
      ['TRT + ancillaries','HCG added for fertility; AI for E2 control; full monitoring protocol','700–900 ng/dL with normal LH/FSH via HCG'],
    ],[35,85,35]),
  ]},
  {'title': 'Ch 2: Protocol Options', 'content': [
    ('tbl',[['Delivery Method','Dose','Frequency','Advantages','Disadvantages'],
      ['Testosterone Cypionate injection','100–200 mg/mL','Weekly or E3.5D','Cost-effective; consistent levels; stable','Requires injection technique; equipment needed'],
      ['Testosterone Enanthate injection','100–200 mg/mL','Weekly or E3.5D','Well-established; widely available; cheap','Same as TC; slight peak-trough variation'],
      ['Testosterone gel','50–100 mg/day','Daily topical application','No injections; easy; stable levels','Transfer risk to family; variable absorption'],
      ['Testosterone pellets','150–450 mg total','Every 3–6 months','Very infrequent; consistent levels','Surgical implant; inflexible dose adjustment'],
      ['Testosterone undecanoate','1000 mg/3 mL','Every 10 weeks','Longest duration; infrequent','Expensive; requires clinic administration'],
    ],[35,25,25,45,25]),
  ]},
  {'title': 'Ch 3: Blood Work Reference', 'content': [
    ('tbl',[['Marker','Optimal Range on TRT','Action if Out of Range'],
      ['Total Testosterone','600–900 ng/dL','Adjust dose; check timing of blood draw (always at trough)'],
      ['Free Testosterone','15–25 pg/mL','May need SHBG management with Boron 10mg or Proviron'],
      ['Estradiol (E2)','20–35 pg/mL','Add AI if > 40; reduce AI if < 15; retest in 4 weeks'],
      ['SHBG','20–40 nmol/L','Low SHBG: more frequent smaller injections; high: standard dosing'],
      ['Haematocrit','< 52%','Donate blood if > 52%; reduces clot risk; check every 3 months'],
      ['LH / FSH','Near zero (expected on TRT)','Add HCG if fertility is a concern'],
      ['PSA','< 2.0 ng/mL','Annual check; consult urologist if rapidly rising'],
      ['HDL Cholesterol','> 40 mg/dL','Omega-3, cardio, statin if needed; TRT can lower HDL'],
      ['ALT / AST (liver)','< 2x upper limit of normal','Injectable TRT has minimal liver impact; switch if using oral'],
    ],[38,42,75]),
  ]},
  {'title': 'Ch 4: HCG on TRT', 'content': [
    ('p','HCG (Human Chorionic Gonadotropin) mimics LH and maintains testicular function, volume, and intratesticular testosterone while on TRT. It is essential for men who wish to preserve fertility on long-term TRT.'),
    ('tbl',[['HCG Use Case','Dose','Frequency','Benefit'],
      ['Fertility preservation on TRT','500–1000 IU','3x/week','Maintains sperm production; prevents azoospermia'],
      ['Testicular atrophy prevention','250–500 IU','2–3x/week','Prevents testicular volume loss during TRT'],
      ['Restart pre-PCT (if cycling)','500 IU','EOD for 4 weeks before PCT','Kickstarts HPTA before SERM therapy'],
      ['Low libido despite good T levels','500 IU','2x/week','Raises intratesticular testosterone'],
    ],[45,22,25,63]),
  ]},
  {'title': 'Ch 5: Lifestyle Optimisation on TRT', 'content': [
    ('ibox','Maximise TRT Results Through Lifestyle',[
      'Resistance training 3–5x/week: amplifies the anabolic signal of exogenous testosterone',
      'Sleep 7–9 hours: GH release and synergy with testosterone occur during deep sleep',
      'Body fat: keep BF under 20%; adipose tissue converts testosterone to estrogen via aromatase',
      'Alcohol: limit to under 2 units/week; alcohol suppresses T and raises estrogen',
      'Stress: chronic cortisol impairs testosterone receptor sensitivity and reduces free T',
      'Micronutrients: Zinc 30mg + Magnesium 400mg + Vitamin D 5000 IU support T pathway enzymes',
      'Avoid xenoestrogens: BPA plastics, pesticides, and certain personal care product ingredients',
    ]),
    ('sp',5),
    ('tbl',[['Common TRT Concern','Explanation','Solution'],
      ['Polycythaemia (high RBC/HCT)','TRT stimulates red blood cell production','Donate blood every 2–3 months; adjust dose if persistent'],
      ['Testicular atrophy','LH suppression shrinks testes over time','Add HCG 250–500 IU 2–3x/week; usually reverses within weeks'],
      ['Fertility impairment','Exogenous T suppresses sperm production','HCG + FSH (or Clomid) can maintain sperm production on TRT'],
      ['Sleep apnoea worsening','TRT can worsen upper airway muscle tone','CPAP if diagnosed; reduce TRT dose if correlated'],
      ['Acne / oily skin','Androgen effect on sebaceous glands','Benzoyl peroxide wash; zinc; lower dose if severe'],
    ],[35,52,68]),
  ]},
])

# ── PDF 09: Science of Muscle Hypertrophy ─────────────────────────────────────
make_pdf('09_Science_of_Muscle_Hypertrophy.pdf',
  'SCIENCE OF MUSCLE HYPERTROPHY', 'Mechanisms, Methods & Evidence-Based Programming',
  '#1d4ed8', [
  {'title': 'Ch 1: The Three Mechanisms', 'content': [
    ('p','Current evidence identifies three primary stimuli driving muscle protein synthesis and hypertrophy: mechanical tension, metabolic stress, and muscle damage. Understanding each allows programme design that maximises all three.'),
    ('tbl',[['Mechanism','Description','How to Maximise','Optimal Rep Range'],
      ['Mechanical Tension','Force applied to sarcomeres during contraction and stretch','Heavy compound lifts with full ROM; slow controlled eccentrics','3–8 reps (85–90% 1RM)'],
      ['Metabolic Stress','Accumulation of lactate, inorganic phosphate, and H+ ions','Higher reps with short rest; occlusion/BFR training','12–20 reps (60–75% 1RM)'],
      ['Muscle Damage','Micro-tears from eccentric and novel loading patterns','Novel exercises; lengthened partials; 3–5 sec eccentric tempo','8–15 reps with slow eccentric'],
    ],[30,50,45,30]),
  ]},
  {'title': 'Ch 2: Evidence-Based Training Variables', 'content': [
    ('tbl',[['Variable','Hypertrophy Optimum','Key Research Finding'],
      ['Sets per muscle per week','10–20 sets (MEV to MRV)','Start at 10; add 1 set/muscle/week until plateau; deload then re-establish MV'],
      ['Reps per set','6–20 (peak stimulus: 8–12)','Multiple rep ranges within 6–20 produce fuller hypertrophy stimulus'],
      ['Effort (RIR)','0–2 reps in reserve per set','Proximity to failure is the strongest predictor of hypertrophy stimulus'],
      ['Rest between sets','60–180 seconds','Compound lifts: 2–3 min; isolation: 60–90 sec for metabolic effect'],
      ['Training frequency','2–3x/week per muscle group','More MPS spikes per week with higher frequency; same total volume'],
      ['Eccentric tempo','2–4 seconds','Slow eccentrics enhance mechanical tension mechanism'],
      ['Range of motion','Full ROM; emphasise stretched position','Lengthened partials show surprisingly high EMG and hypertrophy'],
    ],[42,38,75]),
  ]},
  {'title': 'Ch 3: Progressive Overload Methods', 'content': [
    ('tbl',[['Method','Application','Best Phase','Example'],
      ['Load progression','Add 2.5–5 kg when rep target achieved','Strength base phase','Bench: 80 kg x 4 → 82.5 kg x 4 next session'],
      ['Volume progression','Add 1 set per exercise per week','Hypertrophy phase','3x10 → 4x10 → 5x10 over 3 weeks'],
      ['Density progression','Same total work in less time','Metabolic/conditioning phase','Same sets/reps; rest drops 90→75→60 sec over weeks'],
      ['Frequency progression','Add training days per muscle group','Advanced phase','3x/week → 4x/week upper body as volume tolerance increases'],
      ['ROM progression','Increase range of motion over time','Skill/technique phase','Squat depth improvements; fuller pull-up ROM'],
      ['Technique progression','Reduce compensations; purer muscle activation','Foundation phase','Eliminate bar drift in deadlift; lat engagement in rows'],
    ],[30,45,25,55]),
  ]},
  {'title': 'Ch 4: Muscle Protein Synthesis (MPS)', 'content': [
    ('p','MPS is the molecular process by which the body repairs and builds new muscle proteins. A single training session elevates MPS for 24–48 hours. For hypertrophy, MPS must consistently exceed muscle protein breakdown (MPB). Nutrition is the primary lever.'),
    ('tbl',[['MPS Driver','Requirement','Practical Application'],
      ['Leucine threshold','~2.5–3g leucine per meal to trigger MPS','40g whey = 3.5g leucine; 200g chicken = 3g leucine'],
      ['Protein per meal','0.4 g/kg body weight per meal','80 kg person = 32g protein every 4–5 hours'],
      ['Daily protein total','1.6–2.2 g/kg BW/day','80 kg person = 128–176g total protein daily'],
      ['Protein distribution','Even spread across 4–5 meals','Not front- or back-loaded into 1–2 large meals'],
      ['Pre-sleep protein','40g casein/cottage cheese before bed','Maintains MPS elevation during overnight fast'],
    ],[40,45,70]),
  ]},
  {'title': 'Ch 5: Periodisation & Sample Programme', 'content': [
    ('tbl',[['Phase','Duration','Rep Range','Intensity','Primary Goal'],
      ['Anatomical adaptation','2–4 weeks','15–20','60–65%','Tendon/ligament preparation; form mastery'],
      ['Hypertrophy (accumulation)','6–8 weeks','8–12','70–80%','Maximum muscle growth via volume accumulation'],
      ['Strength (intensification)','4–6 weeks','3–6','82–92%','Neural efficiency; strength base for future hypertrophy'],
      ['Power (optional)','2–4 weeks','3–5 explosive','70–80%','Rate of force development; athletic performance'],
      ['Deload','1 week','Reduce 50% volume','Reduce 30% load','Recovery; supercompensation; avoid overreaching'],
    ],[35,22,22,18,58]),
    ('sp',5),
    ('h2','4-Day Upper/Lower Hypertrophy Template'),
    ('tbl',[['Day','Session','Priority Exercises','Sets x Reps'],
      ['Monday','Upper (strength focus)','Bench press 4x5, Barbell row 4x5, OHP 3x6, Weighted pull-up 3x5','Heavy; 2–3 min rest'],
      ['Tuesday','Lower (strength focus)','Squat 4x5, Romanian DL 3x6, Leg press 3x8, Leg curl 3x8','Heavy; 3 min rest'],
      ['Thursday','Upper (hypertrophy focus)','Incline DB press 4x10, Cable row 3x12, DB shoulder press 3x12, Curl 3x12','Moderate; 75 sec rest'],
      ['Friday','Lower (hypertrophy focus)','Leg press 4x12, Bulgarian split squat 3x10, Hack squat 3x12, Glute bridge 3x15','Moderate; 90 sec rest'],
    ],[18,25,75,37]),
  ]},
])

# ── PDF 10: Ultimate Fat Loss Masterclass ──────────────────────────────────────
make_pdf('10_Ultimate_Fat_Loss_Masterclass.pdf',
  'ULTIMATE FAT LOSS MASTERCLASS', 'Evidence-Based Protocol — No Gimmicks',
  '#b91c1c', [
  {'title': 'Ch 1: The Fat Loss Equation', 'content': [
    ('p','Fat loss occurs when energy expenditure exceeds energy intake — a caloric deficit. All diets that produce fat loss do so by creating this deficit. The challenge is maintaining the deficit while preserving muscle, managing hunger, and sustaining consistency over weeks and months.'),
    ('tbl',[['Deficit Size','Weekly Fat Loss','Risk Level','Best For'],
      ['250 kcal/day','~250g/week','Minimal; highly sustainable','Slow recomp; advanced trainees; long-term dieting'],
      ['500 kcal/day','~500g/week','Low; optimal for most people','Standard cut; best balance of speed and muscle preservation'],
      ['750 kcal/day','~750g/week','Moderate; some muscle loss risk','Aggressive cut with very high protein (2.5g/kg+)'],
      ['1000+ kcal/day','1 kg+/week','High; muscle loss and hormonal disruption likely','Short-term only; obese individuals with medical supervision'],
    ],[28,24,25,78]),
  ]},
  {'title': 'Ch 2: Macros & Calorie Calculation', 'content': [
    ('p','Calculate your TDEE (Total Daily Energy Expenditure) using the Mifflin-St Jeor equation multiplied by your activity factor. Subtract 500 kcal for standard fat loss. Adjust every 3–4 weeks as body weight decreases.'),
    ('tbl',[['Activity Level','Multiplier','Example (70 kg person, BMR ~1650 kcal)'],
      ['Sedentary (desk job, no exercise)','x 1.2','1650 x 1.2 = 1,980 kcal TDEE'],
      ['Lightly active (1–3 workouts/week)','x 1.375','1650 x 1.375 = 2,269 kcal TDEE'],
      ['Moderately active (4–5 sessions/week)','x 1.55','1650 x 1.55 = 2,558 kcal TDEE'],
      ['Very active (hard training + physical job)','x 1.725','1650 x 1.725 = 2,846 kcal TDEE'],
    ],[45,22,88]),
    ('sp',5),
    ('tbl',[['Macro','Cutting Target','Why It Matters','Indian Sources'],
      ['Protein','2.2–2.5 g/kg BW','Muscle preservation; most satiating macro','Paneer, dal, eggs, chicken, soya chunks, curd'],
      ['Fat','0.7–1.0 g/kg BW','Hormones; satiety; fat-soluble vitamins','Ghee, nuts, olive oil, egg yolks, fish oil'],
      ['Carbs','Fill remaining calories','Training performance; glycogen; mood','Rice, oats, roti, sweet potato, banana, fruit'],
    ],[18,28,48,61]),
  ]},
  {'title': 'Ch 3: Evidence-Based Strategies', 'content': [
    ('tbl',[['Strategy','Mechanism','How to Implement','Evidence Rating'],
      ['High protein diet','Thermic effect 25–30%; strongest satiety; muscle preservation','2g+/kg every single day; distribute across 4–5 meals','5/5'],
      ['Resistance training','Preserves muscle during deficit; raises RMR long-term','3–4x/week compound movements; progressive overload','5/5'],
      ['Cardio (LISS + HIIT combo)','Burns additional calories; improves cardiovascular health','LISS 4x45 min + HIIT 2x20 min per week','4/5'],
      ['Sleep 7–9 hours','Controls ghrelin and leptin; reduces cravings by 30%+','Fixed sleep/wake schedule; dark, cool room','4/5'],
      ['Calorie tracking (6 weeks min)','Eliminates unconscious caloric overconsumption','HealthifyMe or MyFitnessPal; weigh food for 1 week','4/5'],
      ['High-volume low-calorie foods','Low calorie density allows larger meal volume','Start meals with salad/soup; eat cucumber and watermelon','3/5'],
      ['Intermittent fasting (16:8)','Reduces eating window; helps some with caloric adherence','Not magic; works only if it reduces total intake','3/5'],
    ],[32,43,48,17]),
  ]},
  {'title': 'Ch 4: Breaking Plateaus', 'content': [
    ('ibox','Plateau-Breaking Protocol (Apply in Order)',[
      '1. Recalculate TDEE — it drops as you lose weight; recalculate every 5 kg of weight loss',
      '2. Refeed day — 1 day at maintenance calories (high carb) weekly to restore leptin',
      '3. Diet break — 1–2 weeks at maintenance; alleviates hormonal adaptation; resume refreshed',
      '4. Increase NEAT — 2000 extra steps per day; stand more; take stairs; park far from entrance',
      '5. Change cardio stimulus — if doing LISS only, add HIIT; if doing HIIT only, add fasted LISS',
      '6. Re-audit food logging — weigh all food for 7 days; eyeballing creates 20–40% underestimation',
      '7. Check hormones — if plateau persists over 3 weeks: thyroid, cortisol, insulin sensitivity',
    ]),
  ]},
  {'title': 'Ch 5: Indian Cutting Meal Plans', 'content': [
    ('h2','Indian Vegetarian Cutting Plan (1800 kcal, 130g protein)'),
    ('tbl',[['Meal','Food','kcal','Protein'],
      ['Breakfast 7 AM','Moong dal chilla x3 + green chutney + chai (no sugar)','340','20g'],
      ['Mid-morning 10 AM','100g soya chunks (boiled, spiced) + cucumber + lemon','200','26g'],
      ['Lunch 1 PM','150g paneer bhurji + 1 roti + mixed sabzi + salad','420','28g'],
      ['Snack 4 PM','1 cup low-fat curd + 10 almonds','200','12g'],
      ['Post-workout 6 PM','Whey shake 30g + 1 banana','280','26g'],
      ['Dinner 8 PM','100g tofu stir-fry (Indian spices) + 1 roti + dal soup','360','24g'],
      ['TOTAL','','1,800 kcal','136g'],
    ],[28,78,22,22]),
    ('sp',5),
    ('h2','Indian Non-Vegetarian Cutting Plan (1800 kcal, 160g protein)'),
    ('tbl',[['Meal','Food','kcal','Protein'],
      ['Breakfast 7 AM','4 egg whites + 1 whole egg bhurji + 1 roti','310','28g'],
      ['Mid-morning 10 AM','30g whey + 100g curd','210','32g'],
      ['Lunch 1 PM','200g grilled chicken + 3/4 cup brown rice + sabzi','460','45g'],
      ['Snack 4 PM','Boiled eggs x2 + cucumber + lemon','160','14g'],
      ['Post-workout 6 PM','Whey shake 30g + 1/2 banana','220','28g'],
      ['Dinner 8 PM','150g fish tikka + large salad + 1 roti','380','36g'],
      ['Pre-sleep','Cottage cheese 150g (low fat)','110','18g'],
      ['TOTAL','','1,850 kcal','201g'],
    ],[28,78,22,22]),
  ]},
  {'title': 'Ch 6: Common Mistakes & Troubleshooting', 'content': [
    ('tbl',[['Mistake','Why It Fails','The Fix'],
      ['Not tracking calories at all','Consistently underestimates intake; impossible to manage what you do not measure','Track accurately for at least 6 weeks to build intuitive awareness'],
      ['Too much cardio, not enough lifting','Accelerates muscle loss; reduces metabolic rate; unsustainable','Prioritise resistance training; add cardio as a deficit tool, not primary method'],
      ['Eating too little protein','Muscle breakdown during deficit; lower satiety; worse body composition result','Minimum 2g/kg bodyweight every single day; non-negotiable'],
      ['Losing more than 1 kg/week','Indicates muscle is being lost not just fat; hormones disrupted','Slow down; add back 200–300 kcal; re-evaluate approach'],
      ['Cheat meals turning into cheat days/weekends','Eliminates entire week\'s deficit in 2 days; zero net progress','Planned refeeds (maintenance for 1 day) are evidence-based; cheat weekends are not'],
      ['Stopping at first plateau','Metabolic adaptation is temporary and reversible; abandoning too early is the biggest mistake','Apply plateau protocol; be patient; results often resume within 1–2 weeks of intervention'],
    ],[35,50,70]),
  ]},
])

print("PDFs 04-10 complete.")
