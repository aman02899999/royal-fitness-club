"""Generate Part 2 of Anabolic Full Guide (extension pages) and merge."""
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

def get_styles():
    s = getSampleStyleSheet()
    defs = {
        'ChHead': dict(fontName='Helvetica-Bold', fontSize=15, textColor=RED, spaceBefore=14, spaceAfter=8, leading=20),
        'SecHead': dict(fontName='Helvetica-Bold', fontSize=12, textColor=WHITE, spaceBefore=10, spaceAfter=5, leading=17),
        'Body': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=6, leading=16, alignment=TA_JUSTIFY),
        'Blt': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=4, leading=15, leftIndent=14, firstLineIndent=-10),
        'Callout': dict(fontName='Helvetica-BoldOblique', fontSize=10, textColor=GOLD, spaceBefore=6, spaceAfter=6, leading=16, leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY),
        'Cover2': dict(fontName='Helvetica-Bold', fontSize=18, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4, leading=24),
        'Cover3': dict(fontName='Helvetica', fontSize=11, textColor=LGREY, alignment=TA_CENTER, spaceAfter=6, leading=16),
    }
    for name, kw in defs.items():
        if name not in s:
            s.add(ParagraphStyle(name=name, **kw))
        else:
            for k, v in kw.items(): setattr(s[name], k, v)
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
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 3*mm))

def hr(story): story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#333'), spaceBefore=4, spaceAfter=4))
def bl(story, s, items): [story.append(Paragraph(f'• {i}', s['Blt'])) for i in items]
def co(story, s, t): story.append(Paragraph(f'💡 {t}', s['Callout']))

def build_part2():
    tmp = '/tmp/anabolic_part2.pdf'
    doc = SimpleDocTemplate(tmp, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = get_styles()
    story = []

    # ── FULL 12-WEEK PROGRAM WEEK BY WEEK ──
    story.append(Paragraph('FULL 12-WEEK PROGRAM — WEEK-BY-WEEK PROGRESSIVE TARGETS', s['ChHead']))
    hr(story)
    story.append(Paragraph('How to Read This Table', s['SecHead']))
    story.append(Paragraph(
        'The table below shows progressive weight/rep targets for the five primary compound movements across all 12 weeks. '
        'These are guide targets for a 75kg intermediate male with approximately 18 months training experience. '
        'Adjust starting weights based on your own current capability — the progression rates are the key reference, not the absolute numbers. '
        'Always prioritise technique over hitting the target weight. If form breaks, hold the weight and increase reps instead.', s['Body']))
    tb(story,
        ['Week', 'Phase', 'Squat (kg)', 'Bench (kg)', 'Deadlift (kg)', 'OHP (kg)', 'Row (kg)', 'RIR'],
        [
            ['1', 'Accumulation', '80×12', '65×12', '100×12', '50×12', '60×12', '3–4'],
            ['2', 'Accumulation', '82.5×12', '67.5×12', '102.5×12', '52.5×12', '62.5×12', '3–4'],
            ['3', 'Accumulation', '85×11', '70×11', '105×11', '55×11', '65×11', '2–3'],
            ['4', 'Accumulation', '87.5×10', '72.5×10', '107.5×10', '57.5×10', '67.5×10', '2–3'],
            ['5', 'Intensification', '90×8', '75×8', '110×8', '60×8', '70×8', '2'],
            ['6', 'Intensification', '92.5×8', '77.5×8', '112.5×8', '62.5×8', '72.5×8', '1–2'],
            ['7', 'Intensification', '95×7', '80×7', '115×7', '65×7', '75×7', '1–2'],
            ['8', 'Intensification', '97.5×6', '82.5×6', '117.5×6', '67.5×6', '77.5×6', '1'],
            ['9', 'DELOAD', '80×10', '65×10', '100×10', '50×10', '62.5×10', '4–5'],
            ['10', 'Peaking', '100×5', '85×5', '120×5', '70×5', '80×5', '1'],
            ['11', 'Peaking', '105×4', '87.5×4', '125×4', '72.5×4', '82.5×4', '0–1'],
            ['12', 'Peaking (Test)', '110×3', '90×3', '130×3', '75×3', '85×3', '0'],
        ], widths=[30, 70, 57, 57, 57, 52, 52, 35])
    co(story, s, 'Week 12 is your testing week — attempt new PBs on each primary lift. This data becomes the baseline for your next training cycle.')

    story.append(Paragraph('Weekly Nutrition Adjustments by Phase', s['SecHead']))
    tb(story,
        ['Phase', 'Weeks', 'Calorie Adjustment', 'Protein', 'Carb Strategy', 'Notes'],
        [
            ['Accumulation', '1–4', 'TDEE + 200 kcal', '2.0g/kg', 'Higher carbs on training days', 'Build volume tolerance'],
            ['Intensification', '5–8', 'TDEE + 300 kcal', '2.1g/kg', 'Consistent high carbs daily', 'Support heavier loads'],
            ['Deload', '9', 'TDEE or slight deficit', '2.2g/kg', 'Moderate carbs', 'Prioritise sleep + recovery'],
            ['Peaking', '10–12', 'TDEE + 150 kcal', '2.2g/kg', 'Carb load 24h pre-test day', 'Feel strong and sharp'],
        ], widths=[70, 45, 100, 65, 120, 100])
    story.append(PageBreak())

    # ── EXERCISE TECHNIQUE GUIDE ──
    story.append(Paragraph('EXERCISE TECHNIQUE MASTER GUIDE', s['ChHead']))
    hr(story)
    story.append(Paragraph('Barbell Back Squat — The King of Leg Exercises', s['SecHead']))
    story.append(Paragraph(
        'The back squat is the most effective lower body mass builder in existence. It simultaneously loads the quadriceps, '
        'hamstrings, glutes, erector spinae, and core — making it the most time-efficient exercise for total lower body development. '
        'Poor squat technique is the number one cause of lower back injury in Indian gym athletes.', s['Body']))
    bl(story, s, [
        'Setup: Bar on upper traps (high bar) or rear delts (low bar). Feet shoulder-width or slightly wider. Toes pointed 15–30° outward.',
        'Brace: Take a big breath, brace your core as if taking a punch (360° pressure). This is your intra-abdominal pressure — your natural weightlifting belt.',
        'Descent: Initiate by pushing knees out and sitting between your heels. Hip crease must go below the top of the kneecap (parallel minimum).',
        'Ascent: Drive through the entire foot. Think "push the floor away." Chest up, knees tracking over toes throughout.',
        'Common errors: Forward lean (weak quads/ankles), knees caving (weak glutes/abductors), heel rising (tight ankles — fix with elevated heels temporarily).',
    ])
    story.append(Paragraph('Conventional Deadlift — The Total Body Mass Builder', s['SecHead']))
    story.append(Paragraph(
        'The deadlift builds more total muscle mass than any other exercise. It trains the entire posterior chain '
        '(hamstrings, glutes, erector spinae, traps, lats) plus the quadriceps and core. The learning curve is steep '
        'but the payoff is unparalleled — no other single exercise builds as much total-body density and strength.', s['Body']))
    bl(story, s, [
        'Setup: Bar over mid-foot (touching or 2cm from shins). Hip-width stance. Grip just outside legs. Hip hinge to reach bar — do not squat down to it.',
        'Back: Spine neutral. Chest up, lats tight (think "protect your armpits"). Tension throughout before the bar leaves the floor.',
        'Pull: Leg drive first — push floor away. Bar stays in contact with legs throughout the entire lift.',
        'Lockout: Drive hips forward at the top. Stand fully tall. Do not hyperextend the lower back.',
        'Common errors: Rounded lower back (too heavy/weak posterior chain), bar swinging away from body (lost lat tension), jerking (missed bracing).',
    ])
    story.append(Paragraph('Barbell Bench Press — Chest & Upper Body Mass', s['SecHead']))
    bl(story, s, [
        'Setup: Eyes under the bar. Grip 1.5–2× shoulder width. Retract and depress shoulder blades into the bench — create a stable base.',
        'Arch: Maintain a natural lower back arch — this is structural, not performance-enhancing cheating. Feet flat on the floor.',
        'Descent: Bar travels in a slight arc (not straight down). Touch chest at the lower pec line (around nipple level) — not neck.',
        'Press: Drive bar back and slightly up. Think "bend the bar" to engage lats. Maintain wrist stack over elbows throughout.',
        'Common errors: Shoulder pain (flared elbows — tuck to 45–60°), bar bouncing off chest, loss of shoulder blade retraction during set.',
    ])
    story.append(Paragraph('Overhead Press — Shoulder Mass & Stability', s['SecHead']))
    bl(story, s, [
        'Setup: Barbell on upper chest. Grip just outside shoulder width. Elbows slightly in front of bar at start.',
        'Press: Drive bar straight up and slightly back as it clears the head. Lock out fully — do not stop short.',
        'Core: Actively brace throughout. No lumbar hyperextension — if you need to excessively lean back, the weight is too heavy.',
        'Common errors: Bar path going forward (weak upper back), lower back hyperextension, partial reps (not locking out).',
    ])
    co(story, s, 'Perfect technique on compound lifts is worth 6–12 months of faster progress. Film yourself from the side on your first few sessions with each movement. Technique errors are invisible to the lifter.')
    story.append(PageBreak())

    # ── BODY MEASUREMENT & PROGRESS TRACKING ──
    story.append(Paragraph('BODY MEASUREMENT & PROGRESS TRACKING SYSTEM', s['ChHead']))
    hr(story)
    story.append(Paragraph('Why Track? The Data Advantage', s['SecHead']))
    story.append(Paragraph(
        'Athletes who track body measurements, strength numbers, and nutrition data make progress 2–3× faster than those '
        'who "go by feel." Feelings are unreliable — data is not. A 0.5kg weight increase over 4 weeks feels like nothing '
        'but represents 24g of new muscle tissue (assuming stable body fat). Tracking makes these invisible gains visible and motivating.', s['Body']))
    story.append(Paragraph('Monthly Measurement Protocol', s['SecHead']))
    story.append(Paragraph(
        'Measure first thing in the morning, after toilet, before food or water. Use a flexible tape measure. '
        'Measure at the same anatomical landmarks each time. Take 3 measurements and average them to reduce error.', s['Body']))
    tb(story,
        ['Measurement', 'Landmark', 'Week 1', 'Week 4', 'Week 8', 'Week 12', 'Change'],
        [
            ['Body weight (kg)', 'Morning fasted', '', '', '', '', ''],
            ['Chest (cm)', 'Nipple line, exhaled', '', '', '', '', ''],
            ['Waist (cm)', 'Narrowest point', '', '', '', '', ''],
            ['Hip (cm)', 'Widest point', '', '', '', '', ''],
            ['Upper arm L (cm)', 'Mid bicep, relaxed', '', '', '', '', ''],
            ['Upper arm R (cm)', 'Mid bicep, relaxed', '', '', '', '', ''],
            ['Thigh L (cm)', 'Mid quadricep', '', '', '', '', ''],
            ['Thigh R (cm)', 'Mid quadricep', '', '', '', '', ''],
            ['Calf L (cm)', 'Widest point', '', '', '', '', ''],
            ['Neck (cm)', 'Just below larynx', '', '', '', '', ''],
        ], widths=[100, 100, 40, 40, 40, 40, 50])
    story.append(Paragraph('Strength Progress Tracker', s['SecHead']))
    tb(story,
        ['Lift', 'Wk 1 (kg × reps)', 'Wk 4 (kg × reps)', 'Wk 8 (kg × reps)', 'Wk 12 (kg × reps)', '% Gain'],
        [
            ['Back Squat', '', '', '', '', ''],
            ['Barbell Bench Press', '', '', '', '', ''],
            ['Conventional Deadlift', '', '', '', '', ''],
            ['Overhead Press', '', '', '', '', ''],
            ['Barbell Row', '', '', '', '', ''],
            ['Pull-ups (reps)', '', '', '', '', ''],
            ['Barbell Curl', '', '', '', '', ''],
            ['Leg Press', '', '', '', '', ''],
        ], widths=[100, 78, 78, 78, 78, 48])
    story.append(PageBreak())

    # ── SPORT SPECIFIC PROTOCOLS ──
    story.append(Paragraph('SPORT-SPECIFIC & LIFESTYLE PROTOCOLS FOR INDIAN ATHLETES', s['ChHead']))
    hr(story)
    story.append(Paragraph('Training Around the Indian Work Schedule', s['SecHead']))
    story.append(Paragraph(
        'The most common barrier to consistent training for Indian professionals aged 22–40 is time — specifically, the '
        '10–12 hour workday combined with commuting, family obligations, and social commitments. The solution is not motivation; '
        'it is systematic scheduling. Training must be treated as a non-negotiable appointment with the same rigidity as a work meeting.', s['Body']))
    tb(story,
        ['Scenario', 'Recommended Schedule', 'Session Duration', 'Notes'],
        [
            ['Office worker, 9–6 job', 'Train before work (6–7:30 AM) or after (7–8:30 PM)', '60–70 min', 'Prepare kit night before'],
            ['Shift worker / irregular hours', 'Train same time relative to sleep (3–4h after waking)', '55–65 min', 'Circadian rhythm consistency'],
            ['Business owner / self-employed', 'Mid-morning or early afternoon (10 AM–12 PM)', '60–70 min', 'Protect this block proactively'],
            ['Student (college/university)', 'Between classes or early morning', '60 min', 'Use college gym to save travel'],
            ['Home training (equipment limited)', '3×/week full-body, 45–50 min', '45–50 min', 'Prioritise compound movements'],
        ], widths=[110, 155, 75, 100])
    story.append(Paragraph('Managing Training During Festivals & Family Occasions', s['SecHead']))
    story.append(Paragraph(
        'Indian culture involves 15–20 major festivals and social events per year where high-calorie, celebratory foods are '
        'unavoidable and expected. The physiologically correct approach is not restriction or guilt — it is strategic flexibility. '
        'One day of excess eating does not cause fat gain; it requires 3,500 kcal above maintenance to gain 0.5kg of fat. '
        'A typical festival meal of 3,000–4,000 kcal represents a surplus of 500–1,500 kcal — physiologically inconsequential if surrounded by normal eating.', s['Body']))
    bl(story, s, [
        'Festival strategy: Train the day before to maximise glycogen utilisation and insulin sensitivity.',
        'Eat high protein before the feast to reduce total caloric intake.',
        'Return to normal eating the day after — no "punishment" workouts or extended restriction.',
        'View festival eating as a maintenance break (carb refeed), not a failure.',
    ])
    story.append(Paragraph('Travelling & Training — Maintaining Progress on Business Travel', s['SecHead']))
    bl(story, s, [
        'Hotel room workout: Push-ups (6 variations), plank holds, single-leg squats, pike push-ups. Not ideal, but maintains neural patterns.',
        'Find a local gym: Google Maps "gym near me" + city name. Daily drop-in rates across India: ₹100–300.',
        'Resistance bands: Full upper-body workout possible. Highly packable. Anchor to door hinges.',
        'Maintain protein intake: Order grilled chicken/fish + dal/eggs at any Indian hotel. Avoid deep-fried items during travel.',
    ])
    co(story, s, 'Missing 1–2 sessions during travel causes zero measurable muscle loss (atrophy begins after 2–3 weeks of complete inactivity). Travel anxiety about training is more harmful than the missed sessions.')
    story.append(PageBreak())

    # ── HORMONAL HEALTH FOR NATURAL ATHLETES ──
    story.append(Paragraph('OPTIMISING HORMONAL HEALTH — THE NATURAL ATHLETE ROADMAP', s['ChHead']))
    hr(story)
    story.append(Paragraph('Blood Work — Your Hormonal Report Card', s['SecHead']))
    story.append(Paragraph(
        'Every serious natural athlete should get a blood panel done at least once per year — twice per year if actively '
        'trying to optimise hormonal health. Knowing your actual testosterone level, thyroid function, vitamin status, '
        'and haematology gives you real data to work with rather than guessing. The panel below costs approximately '
        '₹2,500–4,000 at any Thyrocare or SRL Diagnostics lab in India.', s['Body']))
    tb(story,
        ['Test', 'Normal Range', 'Why It Matters', 'What Low Means'],
        [
            ['Total Testosterone', '300–1000 ng/dL (men)', 'Primary anabolic hormone', 'Low energy, poor recovery, reduced libido'],
            ['Free Testosterone', '9–30 ng/dL', 'Bioavailable T (most active)', 'Low despite normal total T → high SHBG'],
            ['SHBG', '10–57 nmol/L', 'Binds testosterone (reduces free T)', 'High SHBG → reduce alcohol, increase zinc'],
            ['Vitamin D', '40–80 ng/mL', 'Testosterone cofactor', 'Supplement 2000–5000 IU D3 daily'],
            ['Zinc', '70–120 mcg/dL', 'T synthesis cofactor, 300+ enzymes', 'Supplement 15–30mg zinc picolinate'],
            ['TSH (Thyroid)', '0.5–4.5 mIU/L', 'Metabolism regulator', 'Fatigue, weight gain, cold sensitivity'],
            ['Haemoglobin', '13.5–17.5 g/dL (men)', 'Oxygen delivery to muscles', 'Iron deficiency → poor endurance'],
            ['HbA1c', '<5.7%', 'Long-term blood sugar control', '>6.5% = insulin resistance affecting gains'],
            ['CRP (inflammation)', '<1 mg/L', 'Systemic inflammation', 'Elevated → prioritise recovery & diet'],
        ], widths=[100, 90, 140, 120])
    story.append(Paragraph('Natural Testosterone Optimisation Protocol — 90-Day Plan', s['SecHead']))
    tb(story,
        ['Week', 'Action Items', 'Expected Impact'],
        [
            ['1–2', 'Start Vitamin D3 (4000 IU) + Zinc (25mg) + Magnesium glycinate (400mg) nightly', 'Foundational micronutrient support'],
            ['1–4', 'Prioritise 7.5–9h sleep. No screens 60 min before bed. Blackout curtains.', '+10–15% T from sleep optimisation alone'],
            ['1–8', 'Compound training 4–5×/week. Squat + deadlift as foundation.', 'Increase androgen receptor density'],
            ['1–12', 'Reduce body fat to 12–18% range (if currently higher)', 'Reduce aromatisation of T to oestrogen'],
            ['2–12', 'Add Ashwagandha KSM-66 (600mg/day)', '↓ Cortisol 28%, ↑ T 15–17% (12-week clinical trial)'],
            ['4–12', 'Manage stress: 10 min pranayama or meditation daily', 'Reduce cortisol baseline, protect pregnenolone'],
            ['12', 'Retest blood panel', 'Measure actual change in T, Vit D, Zinc'],
        ], widths=[50, 230, 160])
    story.append(PageBreak())

    # ── MINDSET & LONG-TERM SUCCESS ──
    story.append(Paragraph('MINDSET, IDENTITY & LONG-TERM SUCCESS', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Identity Shift — From "Someone Who Goes to the Gym" to an Athlete', s['SecHead']))
    story.append(Paragraph(
        'The most reliable predictor of long-term fitness success is not motivation, willpower, or genetics — it is identity. '
        'When your behaviour is driven by "this is who I am" rather than "I should do this," consistency becomes effortless. '
        'The goal of this section is to accelerate that identity shift. Every action you take that aligns with being an athlete '
        'casts a vote for that identity. Each training session, each high-protein meal, each night of adequate sleep — these are '
        'identity votes. After 3–6 months of consistent votes, the identity solidifies.', s['Body']))
    story.append(Paragraph('The 5 Mental Frameworks That Separate Consistent Athletes', s['SecHead']))
    bl(story, s, [
        'Process > Outcome: Focus on the inputs (training quality, protein hitting target, sleep hours) rather than the outputs (scale number, mirror appearance). Inputs are 100% within your control; outcomes have noise. Consistent inputs produce outcomes reliably over time.',
        'Minimum Viable Session: On low-energy days, commit to only 20 minutes. Most of the time, starting creates momentum and you complete the full session. If not — 20 minutes is still an identity vote. Never skip; scale down.',
        'Data Over Feeling: "I feel like I\'ve gained fat" vs "my waist is 1cm smaller than 4 weeks ago." Feelings are real experiences but poor measurements. Track data. Feelings lie routinely; data does not.',
        'Seasons, Not Sessions: A single missed workout has zero physiological consequence. A single poor food choice has zero consequence. Zooming out to the 12-week, 12-month level removes the emotional weight of imperfect individual sessions.',
        'Compare Backwards: The only valid comparison is your past self. Comparing to others in the gym is a guaranteed path to either false confidence or unnecessary discouragement — both are useless. Your only competition is the version of you from 3 months ago.',
    ])
    co(story, s, 'The Indian social environment can be particularly challenging — family pressure around food, peer scepticism about gym culture, festival obligations. Acknowledge these are real challenges, not excuses. Develop specific strategies for each challenge ahead of time rather than being caught unprepared.')
    story.append(Paragraph('Handling Plateaus — The Advanced Problem', s['SecHead']))
    story.append(Paragraph(
        'A plateau is not a failure; it is a signal. It tells you precisely two things: (1) your body has fully adapted to the current '
        'stimulus, and (2) a new challenge is required. The correct response is diagnosis, not panic or volume spam. '
        'Apply the checklist below in order before concluding you have hit a genuine plateau.', s['Body']))
    tb(story,
        ['Check First', 'Question to Ask', 'If No → Action'],
        [
            ['Is progressive overload happening?', 'Has weight/reps increased in the last 3 weeks?', 'Add a small load increment even if uncomfortable'],
            ['Is protein sufficient?', 'Are you consistently hitting 1.8g/kg/day?', 'Increase by 0.3g/kg and track for 2 weeks'],
            ['Are you eating enough?', 'Is scale weight stable or rising on a bulk?', 'Increase calories by 200 kcal/day'],
            ['Is sleep adequate?', 'Are you averaging 7.5+ hours across the week?', 'Prioritise sleep above all else for 2 weeks'],
            ['Is there accumulated fatigue?', 'Do you feel strong and recovered on session 1 of the week?', 'Take a full deload week immediately'],
            ['Is exercise selection optimal?', 'Are you training the muscle through full ROM?', 'Switch to an exercise with better ROM'],
        ], widths=[100, 140, 160])
    story.append(PageBreak())

    # ── ADVANCED NUTRITION — CARB CYCLING ──
    story.append(Paragraph('ADVANCED NUTRITION — CARB CYCLING & REFEED STRATEGY', s['ChHead']))
    hr(story)
    story.append(Paragraph('What Is Carb Cycling?', s['SecHead']))
    story.append(Paragraph(
        'Carb cycling is the practice of strategically varying carbohydrate intake based on training demands — eating more '
        'carbohydrates on training days when muscles need glycogen, and fewer on rest days when the demand is lower. '
        'This approach maximises muscle glycogen on training days (better performance) while improving fat oxidation on rest days. '
        'It also helps manage insulin sensitivity and prevents the metabolic adaptation that occurs with sustained low-calorie dieting.', s['Body']))
    tb(story,
        ['Day Type', 'Carb Target', 'Protein', 'Fat', 'Calorie Approx', 'Example Foods'],
        [
            ['Heavy training day', '4–5g/kg', '2.0g/kg', '0.7g/kg', 'TDEE + 200–300', 'Rice, oats, banana, roti'],
            ['Moderate training day', '3–3.5g/kg', '2.1g/kg', '0.8g/kg', 'TDEE + 0–100', 'Rice, sweet potato'],
            ['Light training day', '2–2.5g/kg', '2.2g/kg', '1.0g/kg', 'TDEE − 150', 'Vegetables, small rice'],
            ['Rest day', '1.5–2g/kg', '2.2g/kg', '1.0–1.2g/kg', 'TDEE − 200–300', 'Vegetables, legumes'],
        ], widths=[90, 65, 55, 50, 75, 125])
    story.append(Paragraph('Refeeds — Metabolic Reset During a Cut', s['SecHead']))
    story.append(Paragraph(
        'A refeed day involves temporarily eating at or slightly above maintenance calories — primarily through increased carbohydrates. '
        'Its primary purpose during a fat loss phase is to restore leptin levels (the satiety hormone that drops during sustained deficits), '
        'replenish glycogen for the following training sessions, and provide a psychological break from restriction. '
        'Refeeds are more valuable the leaner you become — implement every 7–14 days when body fat is below 12% (men) or 20% (women).', s['Body']))
    co(story, s, 'Refeed foods for Indian athletes: 400–500g of white rice (or 8–10 rotis) distributed across the day with lean protein sources. Avoid high-fat refeed foods — you want insulin-mediated glycogen storage, not fat storage.')
    story.append(PageBreak())

    # ── SUPPLEMENTATION TIMING MASTER TABLE ──
    story.append(Paragraph('SUPPLEMENTATION TIMING — COMPLETE DAILY PROTOCOL', s['ChHead']))
    hr(story)
    tb(story,
        ['Supplement', 'Morning', 'Pre-Workout', 'Post-Workout', 'Evening', 'Before Bed'],
        [
            ['Creatine (5g)', '✓ (with water)', '— (already saturated)', '—', '—', '—'],
            ['Whey protein (25g)', '—', '—', '✓ (priority)', '—', '—'],
            ['Caffeine (200mg)', '—', '✓ (45 min before)', '—', '—', '❌ (disrupts sleep)'],
            ['Beta-alanine (1.6g)', '—', '✓ (split 2×1.6g)', '—', '✓ (second dose)', '—'],
            ['Citrulline (6g)', '—', '✓ (30–45 min before)', '—', '—', '—'],
            ['Vitamin D3 (4000 IU)', '✓ (with fat meal)', '—', '—', '—', '—'],
            ['Omega-3 (3g)', '✓ (with food)', '—', '—', '—', '—'],
            ['Zinc (25mg)', '—', '—', '—', '—', '✓ (empty stomach)'],
            ['Magnesium (400mg)', '—', '—', '—', '—', '✓ (30 min before bed)'],
            ['Ashwagandha (300mg)', '—', '—', '—', '—', '✓ (with milk)'],
        ], widths=[100, 65, 75, 80, 65, 75])
    story.append(Paragraph('Month-by-Month Supplement Introduction Schedule', s['SecHead']))
    story.append(Paragraph(
        'Introducing all supplements at once makes it impossible to identify what is working (or causing side effects). '
        'Introduce one supplement per 2–3 weeks and monitor response before adding the next.', s['Body']))
    tb(story,
        ['Month', 'Introduce', 'Rationale'],
        [
            ['Month 1', 'Creatine monohydrate (5g/day)', 'Biggest evidence base, immediate strength benefit'],
            ['Month 2', 'Vitamin D3 (4000 IU) + Magnesium glycinate (400mg)', 'Fix near-universal deficiencies'],
            ['Month 3', 'Whey protein (if dietary protein insufficient)', 'Convenient protein top-up post-workout'],
            ['Month 4', 'Ashwagandha KSM-66 (600mg)', 'Cortisol management, T optimisation'],
            ['Month 5', 'Omega-3 fish oil (3g EPA+DHA)', 'Inflammation, recovery, cardiovascular'],
            ['Month 6', 'Citrulline malate (6g pre-workout)', 'Performance + pump enhancement'],
        ], widths=[60, 180, 200])
    story.append(PageBreak())

    # ── COMPLETE GROCERY GUIDE ──
    story.append(Paragraph('COMPLETE WEEKLY GROCERY GUIDE — MUSCLE BUILDING ON A BUDGET', s['ChHead']))
    hr(story)
    story.append(Paragraph('Weekly Grocery List for a 75kg Male Lean Bulking (2,800 kcal/day)', s['SecHead']))
    tb(story,
        ['Category', 'Items', 'Quantity (weekly)', 'Approx Cost (₹)', 'Protein Contribution'],
        [
            ['Protein — Animal', 'Chicken breast', '700g', '280–350', '217g protein'],
            ['Protein — Animal', 'Eggs', '18 large', '120–150', '108g protein'],
            ['Protein — Dairy', 'Paneer', '300g', '120–180', '54g protein'],
            ['Protein — Dairy', 'Greek dahi', '1kg', '100–150', '70g protein'],
            ['Protein — Plant', 'Soya chunks (dry)', '300g', '60–80', '150g protein'],
            ['Protein — Plant', 'Moong dal', '500g', '70–100', '100g protein'],
            ['Carbohydrates', 'White rice', '2kg', '100–140', '—'],
            ['Carbohydrates', 'Whole wheat flour (atta)', '1kg', '50–70', '—'],
            ['Carbohydrates', 'Oats (rolled)', '500g', '60–90', '—'],
            ['Carbohydrates', 'Banana', '12', '60–80', '—'],
            ['Fats', 'Desi ghee', '200g', '150–250', '—'],
            ['Fats', 'Almonds + walnuts', '200g', '200–300', '—'],
            ['Vegetables', 'Seasonal sabzi (spinach, broccoli, beans)', '1.5kg', '80–150', '—'],
            ['Supplements', 'Creatine (if needed)', '35g', '~50', '+5g/day'],
            ['', 'TOTAL', '', '₹1,450–1,990', '699g+ protein'],
        ], widths=[90, 120, 80, 80, 90])
    co(story, s, 'This weekly grocery plan supports 2,800 kcal/day at ~200g protein for approximately ₹1,600–2,000. This is significantly less than most supplement budgets and produces superior results when executed consistently.')
    story.append(PageBreak())

    # ── FINAL SUMMARY ──
    story.append(Paragraph('CONCLUSION — YOUR 12-WEEK ANABOLIC ROADMAP', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Complete System Summary', s['SecHead']))
    story.append(Paragraph(
        'You now have a complete, evidence-based system for building maximum muscle as an Indian athlete. '
        'Every element — training, nutrition, supplementation, recovery, mindset — has been designed for the Indian context: '
        'our foods, our schedules, our stress environment, and our cultural reality. The information in this guide '
        'is not generic Western bodybuilding advice repackaged. It is a system that can be implemented starting today, '
        'with the foods in your kitchen and the gym in your neighbourhood.', s['Body']))
    story.append(Paragraph('Your First 7 Days — Action Plan', s['SecHead']))
    tb(story,
        ['Day', 'Action', 'Time Required'],
        [
            ['Day 1', 'Take baseline measurements + photos. Log starting body weight.', '15 min'],
            ['Day 1', 'Calculate your TDEE on the RFC Beast Calculator. Set calorie + protein target.', '10 min'],
            ['Day 2', 'Complete Push Day A (Chapter 9). Log every set, rep, and weight.', '65 min'],
            ['Day 3', 'Complete Pull Day A. Focus on form over load.', '70 min'],
            ['Day 4', 'Complete Legs Day A. Film your squat from the side.', '75 min'],
            ['Day 5', 'Rest day: 30 min walk + foam rolling. Review grocery list from this guide.', '45 min'],
            ['Day 6', 'Complete Push Day B. Add ashwagandha and vitamin D to your morning routine.', '65 min'],
            ['Day 7', 'Complete Pull Day B. Review week 1 nutrition data. Adjust if protein target not met.', '70 min'],
        ], widths=[40, 290, 80])
    bl(story, s, [
        'Week 4: Take progress measurements and photos. Compare to baseline. Expect 0.3–0.5kg scale gain + noticeable strength increases.',
        'Week 8: Second check-in. Body composition should be visibly improved. Adjust calories if weight gain too fast (>0.5kg/wk for women, >0.7kg/wk for men).',
        'Week 12: Final photos, measurements, and lifts test. Record new PRs. Plan next cycle.',
    ])
    co(story, s, 'Final Principle: Consistency over perfection. The athlete who trains 4 days a week for 5 years will always outperform the athlete who trains 6 days a week for 1 year and burns out. Build a sustainable practice first.')
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB — BUILD YOUR BEAST', s['Cover2']))
    story.append(Paragraph('© Royal Fitness Club. All rights reserved. For support: royalfitnessclub.in', s['Cover3']))

    doc.build(story)
    page_count = len(PdfReader(tmp).pages)
    print(f'Part 2 generated: {page_count} pages')

    # Merge Part 1 + Part 2
    main_path = os.path.join(OUT, '00_Anabolic_Full_Guide.pdf')
    writer = PdfWriter()
    for pdf_path in [main_path, tmp]:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
    with open(main_path, 'wb') as f:
        writer.write(f)
    total = len(PdfReader(main_path).pages)
    print(f'✅ Merged Anabolic Full Guide: {total} pages total')
    os.remove(tmp)

build_part2()
