"""Part 3 extension — exercise index, 7-day plans, supplement brands. Merge to final."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from PyPDF2 import PdfReader, PdfWriter
import os

OUT = '/home/user/royal-fitness-club/generated_pdfs'
RED = colors.HexColor('#e8001d')
GOLD = colors.HexColor('#ffd000')
LGREY = colors.HexColor('#cccccc')
WHITE = colors.white

def st():
    s = getSampleStyleSheet()
    d = {
        'ChHead': dict(fontName='Helvetica-Bold', fontSize=15, textColor=RED, spaceBefore=14, spaceAfter=8, leading=20),
        'SecHead': dict(fontName='Helvetica-Bold', fontSize=12, textColor=WHITE, spaceBefore=10, spaceAfter=5, leading=17),
        'Body': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=6, leading=16, alignment=TA_JUSTIFY),
        'Blt': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=4, leading=15, leftIndent=14, firstLineIndent=-10),
        'Callout': dict(fontName='Helvetica-BoldOblique', fontSize=10, textColor=GOLD, spaceBefore=6, spaceAfter=6, leading=16, leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY),
        'Cover2': dict(fontName='Helvetica-Bold', fontSize=16, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4, leading=22),
        'Cover3': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, alignment=TA_CENTER, spaceAfter=5, leading=15),
    }
    for n, kw in d.items():
        if n not in s: s.add(ParagraphStyle(name=n, **kw))
        else:
            for k, v in kw.items(): setattr(s[n], k, v)
    return s

def tb(story, headers, rows, widths=None):
    t = Table([headers]+rows, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),RED),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#1a1a1a'),colors.HexColor('#0f0f0f')]),
        ('TEXTCOLOR',(0,1),(-1,-1),LGREY),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#333')),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(t); story.append(Spacer(1,3*mm))

def hr(story): story.append(HRFlowable(width='100%',thickness=0.5,color=colors.HexColor('#333'),spaceBefore=4,spaceAfter=4))
def bl(story,s,items): [story.append(Paragraph(f'• {i}',s['Blt'])) for i in items]
def co(story,s,t): story.append(Paragraph(f'💡 {t}',s['Callout']))

def build():
    tmp = '/tmp/anabolic_p3.pdf'
    doc = SimpleDocTemplate(tmp, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = st(); story = []

    # ── COMPLETE EXERCISE INDEX ──
    story.append(Paragraph('COMPLETE EXERCISE INDEX — 40 ESSENTIAL MOVEMENTS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Chest Exercises', s['SecHead']))
    tb(story,
        ['Exercise','Primary Muscle','Equipment','Best Rep Range','Difficulty'],
        [
            ['Barbell Bench Press','Pectoralis major (mid)','Barbell + bench','5–12','Intermediate'],
            ['Incline DB Press','Pectoralis major (upper)','DB + incline bench','8–15','Intermediate'],
            ['Decline Bench Press','Pectoralis major (lower)','Barbell + decline bench','8–12','Intermediate'],
            ['Cable Crossover (low)','Pec major (upper)','Cable machine','12–20','Beginner'],
            ['Cable Crossover (high)','Pec major (lower)','Cable machine','12–20','Beginner'],
            ['Push-ups','Pec major + triceps','Bodyweight','15–30','Beginner'],
            ['Dips (chest)','Pec major + triceps','Parallel bars','8–15','Intermediate'],
            ['DB Pullover','Pec major + serratus','DB + flat bench','12–15','Intermediate'],
        ], widths=[110,100,90,75,75])
    story.append(Paragraph('Back Exercises', s['SecHead']))
    tb(story,
        ['Exercise','Primary Muscle','Equipment','Best Rep Range','Difficulty'],
        [
            ['Pull-ups (pronated)','Latissimus dorsi (width)','Pull-up bar','5–12','Intermediate'],
            ['Chin-ups (supinated)','Lats + biceps','Pull-up bar','6–12','Beginner-Int'],
            ['Lat Pulldown','Latissimus dorsi','Cable + bar','8–15','Beginner'],
            ['Barbell Row (bent-over)','Mid back + lats','Barbell','5–10','Intermediate'],
            ['T-Bar Row','Mid back thickness','T-bar','6–12','Intermediate'],
            ['Seated Cable Row','Mid + lower back','Cable machine','8–15','Beginner'],
            ['Single-Arm DB Row','Lats + mid back','DB + bench','8–12','Beginner'],
            ['Face Pull (rope)','Rear delts + rotator cuff','Cable','15–20','Beginner'],
            ['Straight-Arm Pulldown','Latissimus dorsi isolation','Cable','12–20','Beginner'],
        ], widths=[110,100,90,75,75])
    story.append(Paragraph('Shoulder Exercises', s['SecHead']))
    tb(story,
        ['Exercise','Primary Muscle','Equipment','Best Rep Range','Difficulty'],
        [
            ['Barbell OHP','Anterior + medial delts','Barbell','4–10','Intermediate'],
            ['DB Arnold Press','All 3 delt heads','Dumbbells','8–15','Intermediate'],
            ['DB Lateral Raise','Medial deltoid','Dumbbells','12–20','Beginner'],
            ['Cable Lateral Raise','Medial deltoid','Cable','12–20','Beginner'],
            ['Rear Delt Fly (cable)','Posterior deltoid','Cable','15–20','Beginner'],
            ['Upright Row','Medial delts + traps','Barbell / cable','8–15','Beginner'],
        ], widths=[110,100,90,75,75])
    story.append(Paragraph('Arm Exercises', s['SecHead']))
    tb(story,
        ['Exercise','Primary Muscle','Equipment','Best Rep Range','Difficulty'],
        [
            ['Barbell Curl','Biceps brachii','Barbell / EZ bar','8–15','Beginner'],
            ['Incline DB Curl','Biceps (lengthened)','DB + incline bench','10–15','Beginner'],
            ['Hammer Curl','Brachialis + brachioradialis','Dumbbells','10–15','Beginner'],
            ['Concentration Curl','Biceps peak isolation','Dumbbell','12–15','Beginner'],
            ['Tricep Pushdown (rope)','Triceps (all heads)','Cable','12–20','Beginner'],
            ['Skull Crusher (EZ bar)','Triceps long head','EZ bar','8–12','Intermediate'],
            ['Close-Grip Bench Press','Triceps + chest','Barbell','6–12','Intermediate'],
            ['Overhead Tricep Extension','Triceps long head','DB / cable','10–15','Beginner'],
        ], widths=[110,100,90,75,75])
    story.append(Paragraph('Leg Exercises', s['SecHead']))
    tb(story,
        ['Exercise','Primary Muscle','Equipment','Best Rep Range','Difficulty'],
        [
            ['Back Squat','Quads, glutes, hamstrings','Barbell + rack','5–12','Intermediate'],
            ['Romanian Deadlift','Hamstrings + glutes','Barbell / DB','8–12','Intermediate'],
            ['Leg Press','Quads, glutes','Leg press machine','10–20','Beginner'],
            ['Bulgarian Split Squat','Quads + glutes','DB / barbell','8–12/leg','Intermediate'],
            ['Hip Thrust (barbell)','Gluteus maximus','Barbell + bench','8–15','Beginner'],
            ['Leg Curl (lying/seated)','Hamstrings','Machine','10–15','Beginner'],
            ['Walking Lunges','Quads + glutes','DB / barbell','12–20 steps','Beginner'],
            ['Standing Calf Raise','Gastrocnemius','Machine / free','15–25','Beginner'],
            ['Seated Calf Raise','Soleus','Machine','15–25','Beginner'],
        ], widths=[110,100,90,75,75])
    story.append(PageBreak())

    # ── 7-DAY SAMPLE MEAL PLAN ──
    story.append(Paragraph('COMPLETE 7-DAY MEAL PLAN — NON-VEGETARIAN (2,800 KCAL/DAY)', s['ChHead']))
    hr(story)
    days = [
        ('MONDAY (Training — Push Day)',
         [('Breakfast 7:30 AM','4 eggs scrambled + 2 roti + dahi 150g + green tea','36g P / 40g C / 18g F'),
          ('Mid-Morning 10:30 AM','Banana + 20 almonds + 200ml milk','12g P / 38g C / 12g F'),
          ('Lunch 1:00 PM','150g chicken breast + 200g rice + dal + sabzi','46g P / 74g C / 10g F'),
          ('Pre-Workout 4:30 PM','80g oats + 1 banana + 25g whey','32g P / 60g C / 5g F'),
          ('Post-Workout 7:00 PM','150g chicken + 180g rice + salad','44g P / 64g C / 8g F'),
          ('Dinner 9:30 PM','100g paneer + 2 roti + sabzi','26g P / 30g C / 14g F')]),
        ('TUESDAY (Training — Pull Day)',
         [('Breakfast 7:30 AM','3 eggs + 2 egg whites + 2 roti + dahi','34g P / 36g C / 14g F'),
          ('Mid-Morning 10:30 AM','Apple + cottage cheese 100g + 10 walnuts','16g P / 28g C / 14g F'),
          ('Lunch 1:00 PM','150g fish (rohu/pomfret) + 200g rice + sabzi','38g P / 72g C / 10g F'),
          ('Pre-Workout 4:30 PM','100g oats + milk 200ml + 1 banana','24g P / 65g C / 8g F'),
          ('Post-Workout 7:00 PM','150g chicken + 180g rice + curd','44g P / 68g C / 8g F'),
          ('Dinner 9:30 PM','200g moong dal + 2 roti + sabzi','24g P / 50g C / 6g F')]),
        ('WEDNESDAY (Training — Legs Day)',
         [('Breakfast 7:30 AM','4 eggs whole + 2 roti + milk 200ml','34g P / 38g C / 18g F'),
          ('Mid-Morning 10:30 AM','Dahi 200g + banana + 15 almonds','16g P / 35g C / 10g F'),
          ('Lunch 1:00 PM','200g chicken + 200g rice + sabzi + dal','52g P / 74g C / 10g F'),
          ('Pre-Workout 4:30 PM','Banana + 30g whey protein','26g P / 28g C / 2g F'),
          ('Post-Workout 7:30 PM','200g rice + 150g chicken + salad','44g P / 72g C / 8g F'),
          ('Dinner 9:30 PM','100g paneer + 1.5 roti + sabzi + curd','24g P / 26g C / 14g F')]),
    ]
    for day, meals in days:
        story.append(Paragraph(day, s['SecHead']))
        tb(story, ['Meal','Foods','Macros'],
           [[m, f, mac] for m, f, mac in meals],
           widths=[100, 270, 90])

    story.append(Paragraph('THURSDAY (Rest Day — Lower Calories)', s['SecHead']))
    tb(story, ['Meal','Foods','Macros'],
       [['Breakfast 8:00 AM','3 eggs + 1.5 roti + green vegetables','24g P / 28g C / 14g F'],
        ['Lunch 1:00 PM','150g chicken + 150g rice + dal','38g P / 56g C / 8g F'],
        ['Evening 5:00 PM','Dahi 150g + cucumber + handful nuts','12g P / 12g C / 10g F'],
        ['Dinner 8:00 PM','150g fish + sabzi + 1 roti + salad','32g P / 20g C / 8g F'],
        ['Pre-sleep 10 PM','200ml warm milk + small handful almonds','10g P / 12g C / 10g F']],
       widths=[100, 290, 90])
    story.append(Paragraph('Total Thursday (rest day): ~2,300 kcal | 116g P | 128g C | 50g F', s['Callout']))
    story.append(Paragraph('FRIDAY / SATURDAY / SUNDAY follow the same pattern as Mon/Tue/Wed', s['Body']))
    story.append(Paragraph('Adjust rice/roti quantities to hit your specific calorie target. Every 100g cooked rice = 130 kcal / 28g carbs. Every medium roti = 90 kcal / 18g carbs.', s['Body']))
    story.append(PageBreak())

    # ── 7-DAY VEGETARIAN PLAN ──
    story.append(Paragraph('COMPLETE 7-DAY MEAL PLAN — VEGETARIAN (2,600 KCAL/DAY)', s['ChHead']))
    hr(story)
    story.append(Paragraph('Monday to Sunday — Training Days', s['SecHead']))
    tb(story, ['Meal','Time','Foods','P','C','F','kcal'],
       [['Breakfast','7:30 AM','Paneer bhurji (150g) + 2 roti + dahi 150g','34g','36g','20g','462'],
        ['Mid-Morning','10:30 AM','Soya chunks (40g dry) + milk 200ml','28g','30g','6g','290'],
        ['Lunch','1:00 PM','Moong dal 200g + 200g rice + sabzi','26g','76g','6g','470'],
        ['Pre-Workout','4:30 PM','Oats 80g + whey 25g + banana','30g','60g','5g','405'],
        ['Post-Workout','7:00 PM','Paneer 100g + 200g rice + curd 150g','28g','68g','14g','506'],
        ['Dinner','9:30 PM','Chana dal 200g + 1.5 roti + sabzi','22g','50g','8g','364']],
       widths=[70,55,190,25,25,25,40])
    story.append(Paragraph('Daily Total: ~2,497 kcal | 168g P | 320g C | 59g F — adjust rice for exact target', s['Callout']))
    story.append(Paragraph('Rest Day Vegetarian (reduce carbs by ~100g):', s['SecHead']))
    tb(story, ['Meal','Foods','Macros'],
       [['Breakfast','3 eggs + 1 roti + dahi + green tea','20g P / 22g C / 12g F'],
        ['Lunch','Paneer 100g + dal + small bowl rice + sabzi','28g P / 40g C / 14g F'],
        ['Evening','Greek dahi 200g + fruits + nuts','16g P / 25g C / 10g F'],
        ['Dinner','Soya chunks + sabzi + 1 roti + curd','24g P / 28g C / 8g F']],
       widths=[100, 270, 100])
    story.append(PageBreak())

    # ── INDIAN SUPPLEMENT BRANDS ──
    story.append(Paragraph('INDIA SUPPLEMENT GUIDE — TRUSTED BRANDS & WHERE TO BUY', s['ChHead']))
    hr(story)
    story.append(Paragraph('Protein Supplements', s['SecHead']))
    tb(story,
        ['Brand','Product','Price Range','Notes','Where to Buy'],
        [
            ['MuscleBlaze','Whey Gold / Raw Whey','₹1,500–3,500/kg','Most popular in India, 3rd party tested','Amazon, Flipkart, local stores'],
            ['Optimum Nutrition','Gold Standard Whey','₹3,500–6,000/kg','Global gold standard, excellent mixability','Amazon, ON India website'],
            ['MyFitFuel','100% Whey Protein','₹1,800–3,000/kg','Indian brand, good value','Amazon, MFF website'],
            ['Nakpro','Whey Concentrate','₹1,200–1,800/kg','Budget option, decent quality','Amazon, Big Basket'],
            ['Dymatize','ISO100 Hydrolysate','₹4,000–7,000/kg','Premium hydrolysed whey, fast absorption','Amazon, specialty stores'],
        ], widths=[80, 90, 80, 150, 100])
    story.append(Paragraph('Creatine', s['SecHead']))
    tb(story,
        ['Brand','Product','Price','Notes'],
        [
            ['MuscleBlaze','Creatine Monohydrate','₹400–600/500g','Micronised, excellent value'],
            ['Nakpro','Creatine','₹350–500/500g','Budget pick, same molecule as premium brands'],
            ['Optimum Nutrition','Micronised Creatine','₹800–1,200/300g','Premium but not necessary vs MuscleBlaze'],
            ['Healthkart HK Vitals','Creatine Monohydrate','₹350–500/250g','Widely available offline'],
        ], widths=[90, 120, 100, 190])
    story.append(Paragraph('Vitamins & Minerals', s['SecHead']))
    tb(story,
        ['Supplement','Recommended Brand','Price','Notes'],
        [
            ['Vitamin D3','HealthKart, NOW Foods, Carbamide Forte','₹150–400','Get D3 (cholecalciferol) not D2. 2000–5000 IU dose.'],
            ['Magnesium','Now Foods Magnesium Glycinate, Himalayan Organics','₹400–700','Glycinate form = best absorption, no laxative effect'],
            ['Zinc','Carbamide Forte, HealthKart','₹200–400','Picolinate or bisglycinate form. 15–25mg elemental zinc.'],
            ['Omega-3','NOW Foods Fish Oil, MuscleBlaze Fish Oil','₹400–800','Check EPA+DHA per serving, not just total fish oil'],
            ['Ashwagandha','KSM-66 (Ixoreal), Himalaya, MuscleBlaze','₹250–600','Look for KSM-66 or Sensoril extract on label'],
        ], widths=[80, 140, 80, 200])
    co(story, s, 'Warning: Counterfeit supplements are common in India. Always buy from Amazon, Flipkart, or brand websites. Avoid gym stall purchases without receipts. Check lot numbers on brand websites.')
    story.append(PageBreak())

    # ── BODY FAT MEASUREMENT METHODS ──
    story.append(Paragraph('BODY COMPOSITION MEASUREMENT — METHODS COMPARED', s['ChHead']))
    hr(story)
    story.append(Paragraph('How to Accurately Track Body Fat in India', s['SecHead']))
    story.append(Paragraph(
        'Body fat percentage is the single most important body composition metric — more useful than scale weight alone. '
        'A person can gain muscle while losing fat, with the scale not moving, yet transform their physique dramatically. '
        'Several measurement methods are available in India at different price points.', s['Body']))
    tb(story,
        ['Method','Accuracy','Cost','Availability','Best For'],
        [
            ['US Navy Formula (tape measure)','±3–5%','Free','Anyone with tape','Baseline + ongoing tracking'],
            ['Skinfold calipers','±3–4%','₹300–500 (caliper)','Gym / self-measure','Weekly tracking'],
            ['DEXA Scan','±1–2%','₹2,500–5,000/scan','Major cities (Thyrocare, hospitals)','Accurate baseline, bi-annual'],
            ['Bioelectrical Impedance (BIA)','±4–8%','Free (most gym machines)','Any gym','Directional, not precision'],
            ['Hydrostatic weighing','±1–2%','₹1,000–2,000','Limited to research labs','Research purposes'],
            ['RFCs Beast Calculator (Navy Formula)','±3–5%','Free','Website, instant','Regular tracking — recommended'],
        ], widths=[110, 55, 90, 100, 120])
    story.append(Paragraph('Reading Your Body Fat — What the Numbers Mean', s['SecHead']))
    tb(story,
        ['Category','Men','Women','Visual Description'],
        [
            ['Essential fat','3–5%','10–13%','Dangerous if below — organ and hormone protection only'],
            ['Athletic','6–13%','14–20%','Visible abs, muscle separation clearly visible'],
            ['Fitness','14–17%','21–24%','Lean, athletic look; some muscle definition'],
            ['Average','18–24%','25–31%','Healthy range; some softness, no visible abs'],
            ['Obese','>25%','>32%','Health risks increase; prioritise fat loss first'],
        ], widths=[90, 70, 70, 220])
    co(story, s, 'Target range for optimal anabolic environment in men: 10–16% body fat. Below 8% or above 22%, testosterone production is compromised. Women: 16–24% for optimal hormonal health.')
    story.append(PageBreak())

    # ── SCIENTIFIC REFERENCES ──
    story.append(Paragraph('SCIENTIFIC REFERENCES & FURTHER READING', s['ChHead']))
    hr(story)
    story.append(Paragraph('Key Research Papers Referenced in This Guide', s['SecHead']))
    refs = [
        'Schoenfeld, B.J. (2010). The mechanisms of muscle hypertrophy and their application to resistance training. Journal of Strength and Conditioning Research, 24(10), 2857–2872.',
        'Schoenfeld, B.J., Ogborn, D., Krieger, J.W. (2017). Dose-response relationship between weekly resistance training volume and increases in muscle mass: A systematic review and meta-analysis. Journal of Sports Sciences, 35(11), 1073–1082.',
        'Morton, R.W. et al. (2018). A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training–induced gains in muscle mass and strength in healthy adults. British Journal of Sports Medicine, 52(6), 376–384.',
        'Chandrasekhar, K., Kapoor, J., Anishetty, S. (2012). A prospective, randomized double-blind, placebo-controlled study of safety and efficacy of a high-concentration full-spectrum extract of Ashwagandha root in reducing stress and anxiety in adults. Indian Journal of Psychological Medicine, 34(3), 255–262.',
        'Cribb, P.J., Hayes, A. (2006). Effects of supplement timing and resistance exercise on skeletal muscle hypertrophy. Medicine & Science in Sports & Exercise, 38(11), 1918–1925.',
        'Leproult, R., Van Cauter, E. (2011). Effect of 1 week of sleep restriction on testosterone levels in young healthy men. JAMA, 305(21), 2173–2174.',
        'Kreider, R.B. et al. (2017). International Society of Sports Nutrition position stand: safety and efficacy of creatine supplementation in exercise, sport, and medicine. Journal of the International Society of Sports Nutrition, 14(1), 18.',
        'Stokes, T. et al. (2018). Recent perspectives regarding the role of dietary protein for the promotion of muscle hypertrophy with resistance exercise training. Nutrients, 10(2), 180.',
        'Rhea, M.R. et al. (2002). A comparison of linear and daily undulating periodized programs with equated volume and intensity for strength. Journal of Strength and Conditioning Research, 16(2), 250–255.',
        'Antonio, J. et al. (2014). The effects of consuming a high protein diet (4.4 g/kg/d) on body composition in resistance-trained individuals. Journal of the International Society of Sports Nutrition, 11(1), 19.',
    ]
    for i, ref in enumerate(refs, 1):
        story.append(Paragraph(f'{i}. {ref}', s['Body']))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB — COMPLETE ANABOLIC SYSTEM', s['Cover2']))
    story.append(Paragraph('All content is for educational purposes. Consult a medical professional before beginning any programme.', s['Cover3']))
    story.append(Paragraph('© Royal Fitness Club. royalfitnessclub.in', s['Cover3']))

    doc.build(story)
    p2 = len(PdfReader(tmp).pages)
    print(f'Part 3: {p2} pages')

    main = os.path.join(OUT, '00_Anabolic_Full_Guide.pdf')
    w = PdfWriter()
    for p in [main, tmp]:
        for pg in PdfReader(p).pages: w.add_page(pg)
    with open(main, 'wb') as f: w.write(f)
    total = len(PdfReader(main).pages)
    print(f'✅ Final Anabolic Full Guide: {total} pages')
    os.remove(tmp)

build()
