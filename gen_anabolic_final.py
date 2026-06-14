"""Final extension to push Anabolic Full Guide past 50 pages."""
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
    tmp = '/tmp/anabolic_final.pdf'
    doc = SimpleDocTemplate(tmp, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = st(); story = []

    # ── TRAINING SPLITS COMPARED ──
    story.append(Paragraph('TRAINING SPLITS — COMPREHENSIVE COMPARISON GUIDE', s['ChHead']))
    hr(story)
    story.append(Paragraph('Which Split Is Right for You?', s['SecHead']))
    story.append(Paragraph(
        'The training split — how you divide muscle groups across the training week — is one of the most debated topics in '
        'fitness. The reality: the "best" split is the one you can execute consistently with adequate volume, intensity, and recovery. '
        'The table below compares the five most common splits used by Indian gym athletes.', s['Body']))
    tb(story,
        ['Split','Days/Week','Who It\'s For','Weekly Volume/Muscle','Key Advantage','Key Limitation'],
        [
            ['Full Body','3','Beginners, time-limited','6–9 sets','High frequency, fast learning','Low per-session volume'],
            ['Upper/Lower','4','Intermediates 1–2 yr','8–12 sets','Good frequency + volume balance','Less specialisation'],
            ['Push/Pull/Legs (PPL)','5–6','Intermediates 1.5–3 yr','10–18 sets','High volume per muscle','Requires 5–6 days commitment'],
            ['Bro Split (1 muscle/day)','5','Any level','10–20 sets','High per-session focus','Low frequency (1×/week/muscle)'],
            ['Arnold Split (2×/week)','6','Advanced 3+ years','14–22 sets','High frequency + high volume','Very demanding, recovery critical'],
        ], widths=[70, 55, 100, 80, 130, 110])
    story.append(Paragraph('Full Body Workout — 3-Day Template (Beginners)', s['SecHead']))
    tb(story,
        ['Exercise','Sets','Reps','Rest','Day A or B'],
        [
            ['Barbell/Goblet Squat','4','10','2 min','Both days'],
            ['Barbell/DB Bench Press','3','10','90s','Both days'],
            ['Romanian Deadlift','3','10','2 min','Both days'],
            ['Lat Pulldown or Pull-ups','3','10','90s','Both days'],
            ['Seated DB OHP','3','10','90s','Both days'],
            ['Barbell Curl','2','12','60s','Day A'],
            ['Tricep Pushdown','2','12','60s','Day B'],
            ['Plank','3','30–60s hold','45s','Both days'],
        ], widths=[140,50,50,60,140])
    story.append(Paragraph('Upper/Lower Split — 4-Day Template (Intermediate)', s['SecHead']))
    tb(story,
        ['Day','Focus','Key Movements'],
        [
            ['Monday — Upper A','Strength focus (heavy)','Bench press 4×5, Row 4×5, OHP 3×6, Pulldown 3×8'],
            ['Tuesday — Lower A','Quad dominant','Squat 4×6, Leg press 3×10, RDL 3×10, Calf raise 4×15'],
            ['Thursday — Upper B','Hypertrophy focus','Incline DB 4×10, Cable row 4×12, Laterals 5×15, Arms'],
            ['Friday — Lower B','Posterior chain','RDL 4×8, Hip thrust 4×12, Leg curl 4×12, Lunges 3×12'],
        ], widths=[110, 100, 260])
    co(story, s, 'Progression Principle for All Splits: Track every set and aim to beat last session\'s numbers by at least 1 rep or 2.5kg every 1–2 weeks on compound movements.')
    story.append(PageBreak())

    # ── POSTURE & STRUCTURAL BALANCE ──
    story.append(Paragraph('POSTURE CORRECTION & STRUCTURAL BALANCE', s['ChHead']))
    hr(story)
    story.append(Paragraph('Why Posture Matters for Performance', s['SecHead']))
    story.append(Paragraph(
        'Poor posture is epidemic among Indian office workers and students — hours of desk work and phone usage create '
        'predictable muscular imbalances that directly impair training performance and increase injury risk. The most '
        'common pattern: tight hip flexors + weak glutes + tight chest + weak upper back + forward head posture. '
        'This pattern compresses lumbar vertebrae, internally rotates the shoulders, and reduces training ROM on '
        'every major compound movement.', s['Body']))
    tb(story,
        ['Postural Problem','Tight/Overactive Muscles','Weak/Underactive Muscles','Corrective Exercises'],
        [
            ['Forward head posture','SCM, upper traps, pec minor','Deep cervical flexors, lower traps','Chin tucks, face pulls, thoracic extension'],
            ['Rounded shoulders','Pec major/minor, anterior delts','Rhomboids, mid/lower traps, rotator cuff','Band pull-aparts, Y-T-W, face pulls 3×20 daily'],
            ['Anterior pelvic tilt','Hip flexors, lumbar erectors','Glutes, abs, hamstrings','Glute bridges, dead bugs, hip flexor stretches'],
            ['Knee valgus (caving)','Adductors, TFL','Glute medius, VMO','Clamshells, lateral band walks, single-leg press'],
            ['Flat feet / overpronation','Calf complex, peroneals','Tibialis posterior, foot intrinsics','Single-leg calf raises, toe spreads, barefoot walking'],
        ], widths=[90, 100, 100, 160])
    story.append(Paragraph('Daily 10-Minute Posture Correction Routine', s['SecHead']))
    tb(story,
        ['Exercise','Sets × Reps/Duration','Corrects','Notes'],
        [
            ['Thoracic extension over foam roller','1 × 60 sec','Rounded upper back','Vertebrae T4–T10, each segment'],
            ['Hip flexor stretch (kneeling)','3 × 45 sec/side','Anterior pelvic tilt','Squeeze glute of rear leg'],
            ['Dead bug','3 × 10 reps/side','Core/APT','Maintain lumbar contact with floor'],
            ['Band pull-aparts','3 × 20 reps','Rounded shoulders','Shoulder-width grip, pull to chest'],
            ['Glute bridge','3 × 15 reps','Glute activation/APT','Pause 2 seconds at top'],
            ['Face pull (band)','3 × 15 reps','Forward head + rounded shoulders','External rotate at end position'],
            ['World\'s Greatest Stretch','1 × 5/side','Full body mobility','Hip flexor + thoracic + hamstring'],
        ], widths=[130, 90, 100, 140])
    story.append(PageBreak())

    # ── MEAL PREP GUIDE ──
    story.append(Paragraph('WEEKLY MEAL PREP GUIDE — SAVE TIME, STAY ON TRACK', s['ChHead']))
    hr(story)
    story.append(Paragraph('Why Meal Prep Is the Highest-Leverage Nutrition Habit', s['SecHead']))
    story.append(Paragraph(
        'The single biggest reason Indian athletes miss their protein target is not lack of willpower — it is that '
        'high-protein foods require preparation time that is not available on a busy weekday. Meal prepping 2 hours on '
        'Sunday eliminates this problem for 5 days. Research shows people who meal prep eat significantly more protein, '
        'fewer processed foods, and hit their calorie targets more consistently.', s['Body']))
    story.append(Paragraph('Sunday Batch Cook — 2-Hour Protocol', s['SecHead']))
    tb(story,
        ['Time','Task','Output','Serves'],
        [
            ['0:00–0:30','Marinate and cook 1kg chicken breast (oven/air fryer/tawa)','700g cooked chicken','5–6 meals'],
            ['0:00–0:20','Cook 2 cups moong dal','4–5 portions dal','4–5 meals'],
            ['0:20–0:50','Cook large batch white rice (electric cooker)','8–10 portions rice','4–5 meals'],
            ['0:30–0:60','Boil 12 eggs','12 boiled eggs','4 days breakfasts'],
            ['0:40–1:00','Chop all vegetables (onion, tomato, capsicum, cucumber)','Pre-chopped veg','All week sabzi'],
            ['1:00–1:20','Cook 2 different sabzis for variety','8 portions vegetables','4 days'],
            ['1:20–1:40','Portion into containers with macros label','10–12 meal containers','5 work days'],
            ['1:40–2:00','Prepare overnight oats for 3 mornings','3 breakfasts','Mon/Wed/Fri'],
        ], widths=[55, 170, 130, 75])
    story.append(Paragraph('Container & Storage Guide', s['SecHead']))
    tb(story,
        ['Food','Fridge Life','Freezer Life','Best Container'],
        [
            ['Cooked chicken','4 days','3 months','Airtight glass or BPA-free plastic'],
            ['Cooked rice','4–5 days','1 month','Airtight container, spread flat to cool'],
            ['Dal (cooked)','4–5 days','2 months','Glass jar or container'],
            ['Boiled eggs','1 week (in shell)','Not recommended','Egg tray / bowl, unpeeled'],
            ['Chopped vegetables','3–4 days','Not recommended','Airtight container, paper towel layer'],
            ['Overnight oats','3–4 days','Not recommended','Mason jars or sealed bowls'],
        ], widths=[90, 90, 90, 190])
    co(story, s, 'Investment: 2 hours on Sunday = 10 hours saved during the week. Every meal that\'s already made and measured removes a decision that could result in a fast-food compromise. Meal prep is the infrastructure of consistent nutrition.')
    story.append(Paragraph('How to Use Prepped Meals Across the Week', s['SecHead']))
    tb(story,
        ['Day','Breakfast','Lunch','Dinner','Note'],
        [
            ['Mon','Overnight oats + eggs','Prepped chicken + rice + sabzi','Fresh paneer/dal + roti',''],
            ['Tue','Eggs + leftover dal','Prepped chicken + rice','Prepped dal + sabzi + roti',''],
            ['Wed','Overnight oats + eggs','Prepped chicken + rice + sabzi','Fresh sabzi + eggs + roti',''],
            ['Thu','Eggs + dahi','Remaining chicken + rice','Dal + sabzi + roti','Rest day — reduce rice'],
            ['Fri','Overnight oats','Last prepped chicken + rice','Fresh cook or dine out smartly','End of batch'],
            ['Sat–Sun','Fresh cook','Fresh cook','Fresh cook','Enjoy variety'],
        ], widths=[35, 100, 130, 130, 65])
    story.append(PageBreak())

    # ── TROUBLESHOOTING GUIDE ──
    story.append(Paragraph('TROUBLESHOOTING GUIDE — SOLVE THE 15 MOST COMMON PROBLEMS', s['ChHead']))
    hr(story)
    tb(story,
        ['Problem','Most Likely Cause','Solution'],
        [
            ['Not gaining weight on bulk','Underestimating calories eaten (very common)','Track food with MyFitnessPal for 7 days — most people undercount by 20–30%'],
            ['Not losing fat on deficit','Same — underestimating intake, especially fats','Weigh all food with kitchen scale for 2 weeks'],
            ['Strength not improving','Insufficient sleep, insufficient calories, or no progressive overload','Check sleep (7.5h+), increase food by 200 kcal, add 2.5kg to bar'],
            ['Constantly sore muscles','Volume too high, insufficient sleep/protein','Reduce sets by 30%, eat more protein, sleep 8h'],
            ['Shoulder pain on bench','Elbows flared too wide','Tuck elbows to 45–60°, reduce weight, add face pulls'],
            ['Lower back pain on deadlift','Rounding lower back / too heavy','Reduce weight, film from side, focus on bracing'],
            ['No gym motivation','Lack of a compelling goal','Write specific goal (e.g. "bench 100kg by March"), display it'],
            ['Plateau (no size gain 4+ weeks)','Training stimulus stagnated','Change rep ranges, add advanced technique, increase volume'],
            ['Fat gain while bulking','Calorie surplus too large','Reduce surplus to 200–250 kcal; weigh daily, weekly average'],
            ['Poor recovery between sessions','Insufficient sleep or food','Eat more on training days; sleep 8h minimum'],
            ['Can\'t hit protein target','Not planning meals with protein sources','Meal prep (see previous section); add a protein shake if needed'],
            ['Gym intimidation','Unfamiliarity with equipment and culture','Start 6 AM when gym is quiet; follow written program, not guesswork'],
            ['Joint pain (general)','Accumulated stress without deload','Take a deload week immediately; add joint nutrition protocol'],
            ['Feeling weak during workout','Insufficient pre-workout nutrition or sleep','Eat 40–60g carbs 60–90 min before training'],
            ['Bloating / digestive issues','Sudden high-protein diet or new supplement','Increase protein gradually; try digestive enzymes; stay hydrated'],
        ], widths=[100, 140, 200])
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB — THE COMPLETE ANABOLIC SYSTEM', s['Cover2']))
    story.append(Paragraph('Every answer you need is in this guide. Execute consistently. Results are inevitable.', s['Cover3']))
    story.append(Paragraph('© Royal Fitness Club. royalfitnessclub.in', s['Cover3']))

    doc.build(story)
    p = len(PdfReader(tmp).pages)
    print(f'Final extension: {p} pages')

    main = os.path.join(OUT, '00_Anabolic_Full_Guide.pdf')
    w = PdfWriter()
    for path in [main, tmp]:
        for pg in PdfReader(path).pages: w.add_page(pg)
    with open(main, 'wb') as f: w.write(f)
    total = len(PdfReader(main).pages)
    print(f'✅ FINAL Anabolic Full Guide: {total} pages')
    os.remove(tmp)

build()
# just checking
