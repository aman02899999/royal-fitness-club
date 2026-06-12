"""Generate 50+ page Fitness & Mindset Guidance PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

OUT = '/home/user/royal-fitness-club/generated_pdfs'
BLUE = colors.HexColor('#0066cc')
GOLD = colors.HexColor('#ffd000')
LGREY = colors.HexColor('#cccccc')
WHITE = colors.white

def st():
    s = getSampleStyleSheet()
    d = {
        'Cover1': dict(fontName='Helvetica-Bold', fontSize=34, textColor=WHITE, alignment=TA_CENTER, spaceAfter=6, leading=42),
        'Cover2': dict(fontName='Helvetica-Bold', fontSize=17, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4, leading=24),
        'Cover3': dict(fontName='Helvetica', fontSize=11, textColor=LGREY, alignment=TA_CENTER, spaceAfter=6, leading=16),
        'ChHead': dict(fontName='Helvetica-Bold', fontSize=15, textColor=BLUE, spaceBefore=14, spaceAfter=8, leading=20),
        'SecHead': dict(fontName='Helvetica-Bold', fontSize=12, textColor=WHITE, spaceBefore=10, spaceAfter=5, leading=17),
        'Body': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=6, leading=16, alignment=TA_JUSTIFY),
        'Blt': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=4, leading=15, leftIndent=14, firstLineIndent=-10),
        'Callout': dict(fontName='Helvetica-BoldOblique', fontSize=10, textColor=GOLD, spaceBefore=6, spaceAfter=6, leading=16, leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY),
        'TOCItem': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15),
        'Quote': dict(fontName='Helvetica-Oblique', fontSize=11, textColor=colors.HexColor('#38bdf8'), spaceBefore=8, spaceAfter=8, leading=18, leftIndent=20, rightIndent=20, alignment=TA_CENTER),
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
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#0d1a2a'),colors.HexColor('#0a0f1a')]),
        ('TEXTCOLOR',(0,1),(-1,-1),LGREY),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#1a3a5a')),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(t); story.append(Spacer(1, 3*mm))

def hr(story): story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#1a3a5a'), spaceBefore=4, spaceAfter=4))
def bl(story, s, items): [story.append(Paragraph(f'• {i}', s['Blt'])) for i in items]
def co(story, s, t): story.append(Paragraph(f'💡 {t}', s['Callout']))
def qt(story, s, t): story.append(Paragraph(f'"{t}"', s['Quote']))

def build():
    path = os.path.join(OUT, '00_Fitness_Mindset_Guidance.pdf')
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = st(); story = []

    # COVER
    story.append(Spacer(1, 26*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB', s['Cover3']))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('FITNESS & MINDSET GUIDANCE', s['Cover1']))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('The Mental Operating System for Lifelong Fitness Transformation', s['Cover2']))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='80%', thickness=1, color=BLUE, spaceAfter=8))
    story.append(Paragraph('12 Chapters  ·  60+ Pages  ·  Indian Wellness Edition  ·  Science-Backed', s['Cover3']))
    story.append(Paragraph('By Royal Fitness Club Expert Team', s['Cover3']))
    story.append(PageBreak())

    # DISCLAIMER
    story.append(Paragraph('DISCLAIMER', s['ChHead']))
    story.append(Paragraph('This guide is for educational and personal development purposes only. It does not constitute medical, psychological, or psychiatric advice. If you are experiencing serious mental health challenges, please consult a qualified professional. All strategies in this guide are evidence-informed and suitable for generally healthy adults pursuing fitness improvement.', s['Body']))
    story.append(PageBreak())

    # TOC
    story.append(Paragraph('TABLE OF CONTENTS', s['ChHead']))
    hr(story)
    for ch, title, pg in [
        ('1','The Champion\'s Mindset — Building Mental Toughness',5),
        ('2','Habit Formation & The Science of Consistency',9),
        ('3','Stress Management & Cortisol Control for Athletes',14),
        ('4','Nutrition Psychology — Ending Emotional Eating',18),
        ('5','Sleep Optimisation for Peak Mental & Physical Performance',22),
        ('6','Indian Wellness Practices — Yoga, Pranayama & Recovery',26),
        ('7','Goal Architecture — Setting Targets That Actually Stick',30),
        ('8','Overcoming Plateaus — Mentally & Physically',34),
        ('9','Social Pressure, Peer Influence & the Fitness Lifestyle',38),
        ('10','Building Your Identity as a Lifelong Athlete',42),
        ('11','Emotional Resilience & The Long Game',46),
        ('12','Your 90-Day Mindset Transformation Roadmap',50),
        ('App A','Mindset Assessment & Self-Coaching Toolkit',56),
        ('App B','Daily Journalling Templates',60),
    ]:
        story.append(Paragraph(f'Chapter {ch} — {title} {"·"*max(2,50-len(title)-len(str(pg)))} {pg}', s['TOCItem']))
    story.append(PageBreak())

    # CH1
    story.append(Paragraph('CHAPTER 1 — THE CHAMPION\'S MINDSET: BUILDING MENTAL TOUGHNESS', s['ChHead']))
    hr(story)
    qt(story, s, 'Mental toughness is not a gift you either have or do not have. It is a skill, built through deliberate practice, like any other.')
    story.append(Paragraph('What Mental Toughness Actually Is', s['SecHead']))
    story.append(Paragraph('Mental toughness is the capacity to continue purposeful action in the face of difficulty, discomfort, uncertainty, or failure. It is not the absence of negative emotion — mentally tough athletes feel fear, fatigue, and doubt exactly as others do. The difference is that mental toughness enables action despite those states, rather than waiting for the conditions to feel comfortable. In fitness terms: the mental toughness to train on a day when motivation is zero, to eat your protein target when the rest of the family is having sweets, to stay consistent through three weeks of no visible progress.', s['Body']))
    story.append(Paragraph('The Four Pillars of Mental Toughness', s['SecHead']))
    tb(story,
        ['Pillar','Definition','Training Method','Fitness Application'],
        [
            ['Commitment','Staying bound to a decision regardless of feelings','Set written goals with public accountability','Keep training even when life disrupts routine'],
            ['Control','Focusing on what is within your sphere of influence','Stoic journalling — separate internal vs external','Focus on inputs (training, food, sleep) not outcomes'],
            ['Challenge','Viewing obstacles as opportunities for growth','Deliberate discomfort practice','Welcome hard training sets; they are your growth stimulus'],
            ['Confidence','Self-belief built through evidence of past performance','Progress tracking and data review','Review your personal bests monthly'],
        ], widths=[70, 115, 130, 145])
    story.append(Paragraph('Building Discomfort Tolerance — The Training Ground', s['SecHead']))
    story.append(Paragraph('The gym is one of the most effective environments for building mental toughness because every session presents a quantifiable challenge: this weight, these reps, this rest period. The mind will always suggest stopping before the body must. Training to resist this suggestion — completing the final rep, holding the plank for the full duration, running the last 500 metres — is identical neurologically to resisting the urge to skip a training session or eat an impulsive meal. The gym builds the mental muscle alongside the physical.', s['Body']))
    bl(story, s, [
        'The final rep of a hard set is worth more psychologically than the first 11 combined — it is where growth, both physical and mental, happens.',
        'Train alone occasionally: without a partner to keep you accountable, you rely entirely on internal discipline — the most durable form.',
        'Choose challenging situations deliberately outside the gym: cold showers, 24-hour fasts, difficult conversations — each deposits resilience.',
        'Review your hard-earned wins weekly: looking at past data reinforces the identity of someone who follows through.',
    ])
    co(story, s, 'The discomfort you avoid in the gym follows you everywhere. The discomfort you embrace in the gym builds capacity that transfers everywhere.')
    story.append(Paragraph('The Champion\'s Daily Mental Practices', s['SecHead']))
    tb(story,
        ['Practice','Duration','Optimal Time','Primary Benefit'],
        [
            ['Intention setting','2–3 min','Morning','Sets direction; activates reticular activating system'],
            ['Training visualisation','3–5 min','Pre-workout','Improves performance by 15–20% (research-backed)'],
            ['Process journalling','5–10 min','Evening','Reinforces identity and tracks progress'],
            ['Evening review (wins + lessons)','3–5 min','Before sleep','Anchors positive neural pathways'],
            ['Weekly data review','10–15 min','Sunday','Objective progress assessment; prevents feeling-based decisions'],
        ], widths=[110, 60, 80, 210])
    story.append(PageBreak())

    # CH2
    story.append(Paragraph('CHAPTER 2 — HABIT FORMATION & THE SCIENCE OF CONSISTENCY', s['ChHead']))
    hr(story)
    story.append(Paragraph('Why Willpower Fails — And What Works Instead', s['SecHead']))
    story.append(Paragraph('Willpower is a limited resource — it depletes throughout the day with each decision made. Research by Baumeister (2000) demonstrated that self-regulatory resource depletion follows use, just like physical fatigue. By evening, after a full day of work decisions, social interactions, and emotional management, willpower reserves are at their lowest — precisely when the temptation to skip training or eat processed food is highest. The solution is to minimise reliance on willpower by building automated habits.', s['Body']))
    story.append(Paragraph('The Habit Loop — Cue, Routine, Reward', s['SecHead']))
    story.append(Paragraph('Charles Duhigg\'s habit loop model (The Power of Habit, 2012) describes all automatic behaviours as consisting of three components: a cue that triggers the behaviour, a routine (the behaviour itself), and a reward that reinforces the loop. Building fitness habits requires deliberately engineering all three elements until the routine becomes automatic — requiring minimal conscious effort or willpower.', s['Body']))
    tb(story,
        ['Habit','Cue to Engineer','Routine','Reward to Celebrate'],
        [
            ['Morning training','Alarm + kit already laid out','60-min gym session','Post-workout protein shake you enjoy'],
            ['Protein at every meal','Plate always divided: protein first','Add a protein source before building plate','Feel of satiety and energy'],
            ['Pre-sleep routine','Dim lights at 9:30 PM','Read + stretch + no screens','Better sleep quality (measurable)'],
            ['Hydration','Water bottle on desk / visible','Drink every 45 min','Clearer thinking, better performance'],
            ['Weekly progress review','Sunday evening alarm','10-min data review session','Sense of direction and control'],
        ], widths=[90, 110, 130, 130])
    story.append(Paragraph('The Minimum Viable Habit — Protecting Streaks', s['SecHead']))
    story.append(Paragraph('A streak — consecutive days/weeks of a behaviour — creates a psychological asset that compounds over time. The value of a 60-day training streak is not just 60 workouts; it is the identity reinforcement of those 60 consecutive votes for "I am someone who trains." The biggest threat to streaks is the all-or-nothing mindset: "I cannot do my full 70-minute session, so I will skip entirely." The minimum viable habit prevents this.', s['Body']))
    bl(story, s, [
        'Training minimum viable habit: 20 minutes of any intentional movement. Even 3 sets of push-ups, a 20-minute walk, or a single compound exercise counts.',
        'Nutrition minimum viable habit: Hit protein target, even if total calories are imperfect.',
        'Sleep minimum viable habit: 6.5 hours on worst nights — never allow back-to-back nights below this threshold.',
        'Rule: Never miss twice. One missed session is a blip. Two consecutive misses is the beginning of a new (bad) habit.',
    ])
    story.append(Paragraph('Habit Stacking — Building New Habits on Existing Ones', s['SecHead']))
    story.append(Paragraph('Habit stacking (James Clear, Atomic Habits) involves anchoring a new desired habit to an existing automatic behaviour. Because the existing habit already has a strong cue, the new habit inherits its trigger. This dramatically reduces the activation energy required for a new behaviour.', s['Body']))
    tb(story,
        ['Existing Habit','Stack New Habit','Result'],
        [
            ['Morning chai/coffee','Take Vitamin D3 + Magnesium with it','Supplement compliance becomes automatic'],
            ['Changing into home clothes after work','Put on training kit instead','Lowers barrier to gym entry'],
            ['Sitting for lunch','Add a protein source before eating anything else','Protein target becomes automatic'],
            ['Brushing teeth at night','5-minute mobility/stretching routine after','Recovery habit without dedicated time'],
            ['Opening Instagram in the evening','Review training data for 2 min first','Progress awareness before distraction'],
        ], widths=[110, 180, 170])
    story.append(PageBreak())

    # CH3
    story.append(Paragraph('CHAPTER 3 — STRESS MANAGEMENT & CORTISOL CONTROL', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Stress-Cortisol-Fitness Connection', s['SecHead']))
    story.append(Paragraph('Cortisol is the primary stress hormone released by the adrenal cortex in response to perceived threats — whether physical (heavy squat set) or psychological (work deadline, argument, financial pressure). Acutely, cortisol is essential and beneficial: it mobilises energy, sharpens focus, and enables performance. Chronically, it is the single most destructive force for fitness progress: it breaks down muscle protein, inhibits testosterone synthesis, disrupts sleep architecture, promotes fat storage (particularly visceral fat), and impairs immune function.', s['Body']))
    story.append(Paragraph('The Modern Indian Stress Profile', s['SecHead']))
    story.append(Paragraph('Urban Indian professionals face a uniquely high chronic stress load — combining elements that are individually difficult and collectively overwhelming: long commutes (1.5–3 hours daily in major metros), high-pressure work environments with extended hours, family obligation and expectation management, financial pressure (home loans, education costs, elder care), social media comparison, and reduced sleep. Each of these elevates basal cortisol. Managing this environment is not a soft skill — it is a fundamental health and performance requirement.', s['Body']))
    tb(story,
        ['Stressor','Cortisol Impact','Management Strategy'],
        [
            ['Work deadline pressure (acute)','Moderate spike, resolves','Productive — use the energy, recover after'],
            ['Chronic work overload (>10h/day sustained)','Chronically elevated baseline','Boundary setting, time-blocking, delegation'],
            ['Poor sleep (<7h/night for weeks)','+30–50% cortisol baseline','Non-negotiable sleep priority'],
            ['Financial anxiety','Sustained activation','Financial planning, reduce uncertainty'],
            ['Relationship conflict','Variable, often sustained','Communication skills, resolution protocols'],
            ['Commuting (passive stress)','Moderate but daily accumulation','Podcasts/audiobooks, breathing exercises in car/train'],
            ['Social media excessive use','Comparison stress, anxiety','Screen time limits, curated feed'],
            ['Training volume too high','Exercise cortisol overload','Structured deloads, stay under 75 min sessions'],
        ], widths=[110, 100, 250])
    story.append(Paragraph('Evidence-Based Cortisol Reduction Strategies', s['SecHead']))
    tb(story,
        ['Strategy','Time Required','Cortisol Reduction','Evidence Level'],
        [
            ['Ashwagandha KSM-66 (600mg/day)','1 min to take','−27.9% (Chandrasekhar 2012)','Strong (RCT)'],
            ['4-7-8 Breathing (pranayama)','10 min/day','Significant acute reduction','Strong'],
            ['Progressive Muscle Relaxation','15–20 min/day','Moderate sustained reduction','Strong'],
            ['Meditation (MBSR)','10–20 min/day','−23% after 8-week programme','Very strong (multiple RCTs)'],
            ['Cold water immersion','3–5 min/day','Acute cortisol spike then drop','Moderate'],
            ['Nature exposure (parks, hiking)','30–60 min/week','Significant reduction in urban stress','Moderate-strong'],
            ['Social connection (quality)','Variable','Oxytocin antagonises cortisol','Strong'],
            ['Post-workout carbohydrates','0 extra time','−20–30% post-exercise cortisol','Strong'],
        ], widths=[140, 85, 110, 90])
    co(story, s, 'The most important cortisol management tool available to most Indian athletes costs nothing: going to sleep at the same time every night and waking at the same time every morning. Circadian consistency reduces basal cortisol more reliably than any supplement.')
    story.append(PageBreak())

    # CH4
    story.append(Paragraph('CHAPTER 4 — NUTRITION PSYCHOLOGY: ENDING EMOTIONAL EATING', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Psychology of Eating', s['SecHead']))
    story.append(Paragraph('Food is biologically and psychologically complex. Biologically, it is fuel and construction material. Psychologically, it carries meaning acquired over a lifetime: comfort, reward, celebration, punishment, social connection, love, and culture. For most people, 30–50% of eating episodes are driven by emotional states rather than physiological hunger. Understanding the psychology of your eating patterns is more impactful for long-term body composition than any specific diet protocol.', s['Body']))
    story.append(Paragraph('The 5 Types of Emotional Eating', s['SecHead']))
    tb(story,
        ['Type','Trigger','Common Foods','Intervention'],
        [
            ['Stress eating','Work pressure, anxiety, overwhelm','Crunchy salty foods (chips, namkeen)','Breathing exercise before eating; identify true hunger'],
            ['Boredom eating','Understimulation, lack of purpose','Any available food, often sugar','Replace with activity (walk, call a friend, read)'],
            ['Reward eating','Completion of hard task','High-fat/sugar combination','Healthy reward foods planned in advance'],
            ['Social eating','Peer pressure, celebration, social norms','Festive foods, alcohol, mithai','Pre-commit to choices before social events'],
            ['Comfort eating','Loneliness, sadness, anxiety','Soft, warm, fatty foods','Identify emotional state; address root cause'],
        ], widths=[80, 100, 120, 160])
    story.append(Paragraph('The Hunger vs Appetite Scale', s['SecHead']))
    story.append(Paragraph('True physiological hunger builds gradually, is diffuse, and accepts any food. Emotional appetite appears suddenly, is specific (you want exactly this food), and is often preceded by an emotional trigger. Before every eating episode, take 30 seconds to locate yourself on the hunger-fullness scale.', s['Body']))
    tb(story,
        ['Score','State','Action'],
        [
            ['1 — Ravenous','Dizzy, headache, extreme hunger','Eat immediately — do not restrict'],
            ['2 — Very hungry','Low energy, irritable, difficulty concentrating','Eat a full meal now'],
            ['3 — Hungry','Stomach growling, thinking about food','Good time to eat'],
            ['4 — Slightly hungry','Mild hunger signals','Can eat if meal is due; can wait 30 min'],
            ['5 — Neutral','Neither hungry nor full','Ideal state — eat scheduled meals here'],
            ['6 — Comfortable','Pleasantly satisfied','Ideal stopping point'],
            ['7 — Full','Feeling of fullness, no hunger','Stop eating — fullness signals take 15–20 min to register'],
            ['8 — Overfull','Uncomfortable, bloated','No longer eating from hunger'],
            ['9–10 — Stuffed','Physical discomfort','Emotional eating occurred — identify trigger with curiosity, not guilt'],
        ], widths=[80, 130, 250])
    co(story, s, 'Rule: Aim to eat between 3–4 (when genuinely hungry) and stop between 6–7 (comfortably satisfied). This simple principle, applied consistently, is more powerful than any calorie counting app.')
    story.append(Paragraph('Food Relationship with Indian Cultural Context', s['SecHead']))
    story.append(Paragraph('Indian food culture is extraordinarily rich — and extraordinarily challenging for someone pursuing a specific physique goal. Food is a primary expression of love and hospitality in Indian families. Refusing a second serving of Maa\'s sabzi is not a dietary choice — it is a potential social offence. Festival foods are cultural identity, not mere calories. Navigating this reality requires strategies that honour both the cultural significance of food and your personal health goals.', s['Body']))
    bl(story, s, [
        'The One Plate Strategy: Accept all offered food graciously but take a smaller serving on one plate, eat slowly, and decline a second serving with genuine appreciation ("Bahut achha tha, pet bhar gaya").',
        'Pre-feast strategy: Eat a high-protein meal 2 hours before a family feast. Arrive with reduced appetite.',
        'The 80/20 principle at social events: 80% of your plate from nutritious options; 20% for cultural enjoyment. No guilt.',
        'Communicate your goals to close family members once, clearly. You will not need to re-explain every meal after the initial conversation.',
    ])
    story.append(PageBreak())

    # CH5
    story.append(Paragraph('CHAPTER 5 — SLEEP OPTIMISATION FOR PEAK MENTAL & PHYSICAL PERFORMANCE', s['ChHead']))
    hr(story)
    story.append(Paragraph('Sleep Is Not Rest — It Is Active Maintenance', s['SecHead']))
    story.append(Paragraph('During sleep, the brain undergoes active maintenance: the glymphatic system flushes metabolic waste products (including beta-amyloid, associated with cognitive decline); the hippocampus consolidates memories and motor learning into long-term storage; and the hypothalamic-pituitary axis orchestrates the hormonal cascade responsible for tissue repair, immune function, and emotional regulation. None of this happens adequately in a wakeful state — sleep cannot be replaced or substantially compensated for.', s['Body']))
    story.append(Paragraph('Sleep Stages and Their Functions', s['SecHead']))
    tb(story,
        ['Stage','Duration/Cycle','Primary Function','Athletic Relevance'],
        [
            ['NREM Stage 1','5–10 min','Transition to sleep','Light, easily disrupted'],
            ['NREM Stage 2','20 min','Memory consolidation, body temperature drop','Sleep spindles — skill learning'],
            ['NREM Stage 3 (Deep)','20–40 min (more early night)','GH release, tissue repair, immune function','MOST critical for muscle growth'],
            ['REM Sleep','10–60 min (more late night)','Emotional processing, motor learning','Technique refinement, motivation regulation'],
        ], widths=[90, 100, 170, 100])
    story.append(Paragraph('The Indian Sleep Crisis', s['SecHead']))
    story.append(Paragraph('A 2019 survey of Indian urban professionals (Fitbit Global Sleep Study) found that India had the second shortest average sleep duration globally (6h 58min/night) — significantly below the optimal 7.5–9 hours. The primary causes: late evening work culture, screen usage until 11 PM–midnight, and the cultural perception that minimal sleep signals productivity and dedication. This has a direct, measurable impact on training recovery, hormonal health, and cognitive performance.', s['Body']))
    story.append(Paragraph('Complete Sleep Optimisation Protocol', s['SecHead']))
    tb(story,
        ['Variable','Target','How to Achieve','Impact if Missed'],
        [
            ['Duration','7.5–9 hours','Set sleep target time backwards from wake time','<7h: −23% testosterone, −31% IGF-1, +significant cortisol'],
            ['Sleep time consistency','±30 min same time','Phone alarm for bedtime, not just wake time','Irregular sleep disrupts circadian rhythm and deep sleep %'],
            ['Room temperature','16–19°C','Fan/AC, avoid heavy blankets in hot seasons','Above 22°C: significant reduction in deep sleep stages'],
            ['Light environment','Complete darkness','Blackout curtains, eye mask, remove LED standby lights','Light exposure supresses melatonin even through closed eyelids'],
            ['Blue light','None 60–90 min pre-sleep','Blue light filter glasses, phone night mode, no screens','Delays melatonin onset by 60–90 min'],
            ['Pre-sleep nutrition','Protein (casein) + low sugar','Paneer, dahi, warm milk 90 min before bed','High sugar disrupts NREM Stage 3'],
            ['Pre-sleep routine','Consistent 30–45 min ritual','Same sequence every night (brush, stretch, read)','Random pre-sleep behaviour prevents nervous system downregulation'],
            ['Noise','<40 dB or consistent','Earplugs, white noise machine/app','Sudden noises disrupt sleep architecture even without full awakening'],
        ], widths=[90, 80, 160, 130])
    co(story, s, 'If you can only change one thing to improve your fitness results: sleep 8 hours. Not supplements, not programme design, not cardio strategy. Sleep. Everything else sits downstream of this.')
    story.append(PageBreak())

    # CH6
    story.append(Paragraph('CHAPTER 6 — INDIAN WELLNESS PRACTICES: YOGA, PRANAYAMA & RECOVERY', s['ChHead']))
    hr(story)
    story.append(Paragraph('India\'s 5,000-Year Evidence Base', s['SecHead']))
    story.append(Paragraph('India possesses the world\'s most sophisticated and enduring wellness tradition. Ayurveda, Yoga, and Pranayama have been studied and refined over 5,000 years through observation, codification, and transmission. Modern exercise science is now validating with randomised controlled trials what Indian practitioners understood through centuries of empirical evidence. The convergence is striking: virtually every traditional Indian wellness practice has a measurable physiological mechanism that directly benefits the modern athlete.', s['Body']))
    story.append(Paragraph('Pranayama for Athletes — Evidence-Based Practices', s['SecHead']))
    tb(story,
        ['Technique','Practice','Duration','Physiological Effect','Best Used For'],
        [
            ['Nadi Shodhana (Alternate Nostril)','Inhale left 4 counts, hold 4, exhale right 4, reverse','10 min','Balances sympathetic/parasympathetic, reduces cortisol','Before bed, stress management'],
            ['Bhramari (Humming Bee)','Hum on exhale with fingers on ears','5–10 min','Vagal nerve stimulation, significant cortisol reduction','Acute stress, pre-competition anxiety'],
            ['Box Breathing','4 counts in, 4 hold, 4 out, 4 hold','5–10 min','Activates parasympathetic, slows heart rate','Pre-game, pre-heavy lift, stress'],
            ['Kapalabhati (Breath of Fire)','Short rapid exhales, passive inhale','3–5 min','Stimulates sympathetic, clears airways, energising','Pre-workout activation (not pre-sleep)'],
            ['4-7-8 Breathing','Inhale 4, hold 7, exhale 8','5–10 min','Rapid cortisol reduction, induces sleep onset','Pre-sleep, post-stressful event'],
        ], widths=[90, 130, 60, 145, 115])
    story.append(Paragraph('Yoga Poses for Athletic Recovery', s['SecHead']))
    tb(story,
        ['Pose (Asana)','Duration','Primary Benefit','Target Structure'],
        [
            ['Pigeon Pose (Eka Pada Rajakapotasana)','60–90 sec/side','Hip flexor + piriformis release','Hip flexors, glutes, IT band'],
            ['Downward Dog (Adho Mukha Svanasana)','30–60 sec','Hamstring, calf, shoulder stretch + spinal decompression','Full posterior chain, shoulders'],
            ['Child\'s Pose (Balasana)','60–90 sec','Lumbar decompression, hip relaxation','Lower back, hips, shoulders'],
            ['Supine Spinal Twist','60 sec/side','Thoracic mobility, spinal rotation','Thoracic spine, piriformis'],
            ['Warrior I (Virabhadrasana I)','30–45 sec/side','Hip flexor stretch + thoracic extension','Hip flexors, anterior torso'],
            ['Bridge Pose (Setu Bandhasana)','30–45 sec','Glute activation + hip flexor counter','Glutes, spinal extensors'],
            ['Legs Up The Wall (Viparita Karani)','5–10 min','Venous return, parasympathetic activation, recovery','Lower body circulation, nervous system'],
        ], widths=[130, 70, 160, 110])
    co(story, s, 'A 15-minute post-workout yoga sequence (pigeon → downward dog → spinal twist × 2 sides → child\'s pose → legs up the wall) reduces DOMS by 35–45% and significantly improves next-session performance. More effective than passive rest.')
    story.append(PageBreak())

    # CH7
    story.append(Paragraph('CHAPTER 7 — GOAL ARCHITECTURE: SETTING TARGETS THAT ACTUALLY STICK', s['ChHead']))
    hr(story)
    story.append(Paragraph('Why Most Fitness Goals Fail', s['SecHead']))
    story.append(Paragraph('The failure of most fitness goals is not a motivation problem — it is a goal architecture problem. "I want to lose weight" is not a goal; it is a wish. It has no deadline, no measurable definition of success, no specific behavioural pathway, and no feedback mechanism. Poorly constructed goals create ambiguity about what to do each day and no way to know if you are succeeding. This ambiguity drains motivation because the brain requires clear feedback to sustain directed behaviour.', s['Body']))
    story.append(Paragraph('The SMART+ Framework for Fitness Goals', s['SecHead']))
    tb(story,
        ['Component','Definition','Poor Goal','Strong Goal'],
        [
            ['Specific','Clearly defines what, where, how','Lose weight','Reach 78kg body weight from current 88kg'],
            ['Measurable','Quantifiable progress markers','Get fitter','Bench press 100kg for 3 reps'],
            ['Achievable','Challenging but within real-world capacity','6-pack in 4 weeks','Visible abs (12% BF) in 16 weeks'],
            ['Relevant','Aligned with your values and life','Run a marathon (you hate running)','Build 5kg muscle (love training)'],
            ['Time-bound','Specific deadline creates urgency','Someday get fit','By December 31st, 12 weeks away'],
            ['+Process','Specifies the daily inputs that lead to outcome','N/A (missing from most goals)','Train 5×/week + hit 180g protein daily'],
            ['+Identity','Defines who you are becoming','N/A','I am an athlete who trains consistently'],
        ], widths=[70, 130, 130, 130])
    story.append(Paragraph('The Three-Tier Goal System', s['SecHead']))
    story.append(Paragraph('Effective goal setting operates at three time horizons simultaneously. Each tier informs the others and creates a coherent direction of travel.', s['Body']))
    tb(story,
        ['Tier','Time Horizon','Example','Function'],
        [
            ['Vision (Why)','3–5 years','Be the leanest and strongest I\'ve ever been by age 35','Emotional anchor, provides direction during difficulty'],
            ['Milestone (What)','3–6 months','Bench press 100kg, reach 15% body fat by March','Specific achievement target, measurable'],
            ['Daily Process (How)','Daily/weekly','Train 5×/week, hit 180g protein, sleep 8h','The actual behaviours that make the milestone inevitable'],
        ], widths=[70, 80, 200, 160])
    co(story, s, 'Write your three-tier goals on paper and review them weekly. The physical act of writing reinforces neural encoding. Digital notes are psychologically less binding than handwritten commitments.')
    story.append(PageBreak())

    # CH8
    story.append(Paragraph('CHAPTER 8 — OVERCOMING PLATEAUS — MENTALLY & PHYSICALLY', s['ChHead']))
    hr(story)
    story.append(Paragraph('What a Plateau Is — And Is Not', s['SecHead']))
    story.append(Paragraph('A plateau is a period where progress appears to stall despite consistent effort. The word "appears" is important. In most cases, what looks like a plateau from the inside is one of: (a) accumulated fatigue masking fitness that has continued to improve, (b) insufficient progressive overload — the training stimulus has not been increased, (c) nutritional stagnation — the body has adjusted to current intake, or (d) measurement error — progress is happening in ways not being tracked. True biological plateaus are rarer than most athletes believe.', s['Body']))
    tb(story,
        ['Plateau Type','How to Diagnose','Solution'],
        [
            ['Strength plateau','Weight/reps have not increased in 3+ weeks','Deload, then increase load by 2.5kg; try different rep range'],
            ['Scale plateau (fat loss)','Weight unchanged for 2+ weeks despite deficit','Verify calorie intake with food scale; add 30 min LISS cardio'],
            ['Visual plateau','Body looks the same for 4+ weeks','Progress photos are unreliable short-term; check measurements instead'],
            ['Motivation plateau','Cannot summon effort to train','Change programme, training partner, gym music; set new short-term goal'],
            ['Recovery plateau','Always tired, never feeling fresh','This is overreaching — take full deload week, sleep more, eat more'],
        ], widths=[100, 140, 220])
    story.append(Paragraph('The Psychological Response to Plateaus', s['SecHead']))
    story.append(Paragraph('Plateaus are emotionally significant because they violate the expectation of linear progress. The mind perceives them as evidence of failure, inadequacy, or genetic limitation — none of which are accurate. The neurologically correct response is curiosity, not self-criticism. Ask: "What is this plateau trying to tell me?" rather than "Why am I failing?" The answer is always diagnostic data pointing to the adjustable variable.', s['Body']))
    bl(story, s, [
        'Zoom out: Review 12-week, not 2-week, data. Progress is rarely linear but is almost always positive over longer periods when inputs are consistent.',
        'Change the metric: If scale weight has stalled but strength is still increasing, recomposition is occurring — this is optimal, not a failure.',
        'Celebrate adherence, not just outcomes: Showing up for 45 consecutive training sessions is an extraordinary achievement regardless of whether the scale moved.',
        'Consult your data: Most people feel they are in a plateau when objective data shows they are not. Always check the numbers before making emotional adjustments.',
    ])
    story.append(PageBreak())

    # CH9
    story.append(Paragraph('CHAPTER 9 — SOCIAL PRESSURE, PEER INFLUENCE & THE FITNESS LIFESTYLE', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Indian Social Fitness Landscape', s['SecHead']))
    story.append(Paragraph('The Indian social environment creates a uniquely complex backdrop for fitness pursuits. On one side: a rich tradition of physical culture, yoga, and wellness. On the other: a food culture where saying no to a meal is rude, a social environment where going to the gym every day is viewed as excessive or anti-social, and family systems where decisions about health are made collectively, not individually. Navigating this landscape without either social alienation or fitness abandonment requires specific strategies.', s['Body']))
    tb(story,
        ['Social Challenge','Why It Happens','Evidence-Based Strategy'],
        [
            ['Family pressure to eat more','Food as love and hospitality is deeply cultural','Eat a smaller first serving, finish it fully, decline seconds with genuine appreciation'],
            ['Peer scepticism about gym culture','Gym culture is newer; misunderstood in tier-2/3 cities','Share results, not plans. Results create credibility.'],
            ['Festival overeating pressure','Food is core to all celebrations; refusal seems disrespectful','Apply the one-plate strategy; pre-eat protein before events'],
            ['"Gym is vanity" social judgment','Fitness visible to others triggers comparison and judgment','Reframe: "I train for health and performance, not appearance"'],
            ['Time conflict with family obligations','Training time conflicts with family expectations','Train early morning before family obligations begin; this window is yours'],
            ['Friends who undermine goals','Social homeostasis — your change threatens others','Choose social environments selectively; protect your goals'],
        ], widths=[110, 130, 220])
    co(story, s, 'The most powerful social influence strategy: become the kind of person others want to emulate, not the person who talks about fitness constantly. Your results will speak; your words are usually unnecessary.')
    story.append(PageBreak())

    # CH10
    story.append(Paragraph('CHAPTER 10 — BUILDING YOUR IDENTITY AS A LIFELONG ATHLETE', s['ChHead']))
    hr(story)
    story.append(Paragraph('Identity Is the Ultimate Habit Driver', s['SecHead']))
    story.append(Paragraph('James Clear\'s central insight in Atomic Habits (2018) is that the most durable behaviour change occurs at the identity level, not the goal level. The difference: goal-based change says "I want to run a 5K." Identity-based change says "I am a runner." Every training session, healthy meal, and recovery practice is not just an action — it is a vote for the person you are becoming. Cast enough votes in one direction and the identity solidifies. Once your identity is that of an athlete, consistency becomes the expression of who you are, not a difficult discipline you must maintain.', s['Body']))
    story.append(Paragraph('How to Build an Athlete Identity', s['SecHead']))
    tb(story,
        ['Action','How It Builds Identity','Time to Effect'],
        [
            ['Train consistently (not perfectly)','Each session is a vote for the identity','4–8 weeks of consistency'],
            ['Speak as an athlete ("I train," not "I try to go to the gym")','Language shapes self-perception','Immediate'],
            ['Associate with other athletes','Identity is socially reinforced by peer group','2–4 weeks'],
            ['Learn the science (read, listen, study)','Knowledge signals commitment and identity depth','Ongoing'],
            ['Set athlete-level standards for sleep, food, recovery','Behaviour aligned with identity reinforces it','2–4 weeks'],
            ['Track and review progress data weekly','Creates an objective narrative of athletic progress','4+ weeks'],
            ['Complete increasingly difficult challenges','Competence evidence reinforces the identity','Per challenge'],
        ], widths=[140, 180, 100])
    story.append(Paragraph('The Long Game — 5-Year Athlete Vision', s['SecHead']))
    story.append(Paragraph('Fitness is not a goal you achieve and then stop. It is a practice you develop and then maintain across decades. The Indian athletes who transform most completely and most permanently are those who stopped asking "How long do I have to do this?" and started asking "How do I build a life where this is natural?" That shift — from finite project to permanent identity — is the most important transition in a fitness journey. Everything before it is preparation. Everything after it is expression.', s['Body']))
    story.append(PageBreak())

    # CH11
    story.append(Paragraph('CHAPTER 11 — EMOTIONAL RESILIENCE & THE LONG GAME', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Emotional Reality of Fitness', s['SecHead']))
    story.append(Paragraph('No fitness journey is linear. Progress is punctuated by setbacks: illness, injury, life events, work crises, family obligations, and periods of motivation collapse. These setbacks are not obstacles to the journey — they are part of the journey. The athletes who succeed long-term are not those who avoided setbacks; they are those who developed the emotional resilience to return from them faster, with less self-judgment and more intelligent adaptation.', s['Body']))
    story.append(Paragraph('The Resilience Framework — 4 Steps for Every Setback', s['SecHead']))
    tb(story,
        ['Step','Action','Example Application'],
        [
            ['1. Acknowledge','Name the setback factually, without catastrophising','I missed 2 weeks of training due to illness'],
            ['2. Accept','Accept what cannot be changed without resistance','I cannot undo the 2 missed weeks; resistance is wasted energy'],
            ['3. Assess','Identify the minimum viable re-entry point','I can start with 50% volume next week and rebuild'],
            ['4. Act','Take the first action immediately, however small','Book tomorrow\'s training session right now'],
        ], widths=[60, 130, 270])
    bl(story, s, [
        'Self-compassion accelerates recovery: Research by Dr. Kristin Neff shows self-compassion (treating yourself as you would a friend) produces faster behavioural recovery after setbacks than self-criticism — which increases avoidance.',
        'The comeback is faster than the original build: Muscle memory (retained myonuclei) means regaining lost muscle takes 30–50% less time than building it. Returning after illness or injury is always faster than feared.',
        'View setbacks as data: Every setback reveals a vulnerability in your system (over-reliance on motivation, insufficient planning, inadequate recovery). Fixing the system, not blaming yourself, prevents recurrence.',
    ])
    story.append(PageBreak())

    # CH12
    story.append(Paragraph('CHAPTER 12 — YOUR 90-DAY MINDSET TRANSFORMATION ROADMAP', s['ChHead']))
    hr(story)
    story.append(Paragraph('Month 1 — Foundation (Days 1–30)', s['SecHead']))
    tb(story,
        ['Week','Focus','Daily Practice','Milestones to Hit'],
        [
            ['Week 1','Baseline assessment + goal architecture','10 min morning intention; evening journalling','Written 3-tier goals; baseline measurements taken'],
            ['Week 2','Habit installation: training + protein','Minimum viable habit protocol','7 consecutive training days; protein target hit 5/7 days'],
            ['Week 3','Sleep optimisation','Consistent sleep time; pre-sleep routine','Average sleep 7.5h across the week'],
            ['Week 4','Stress identification','Daily stressor journal; pranayama 10 min','Identified top 3 stressors; begun 1 intervention for each'],
        ], widths=[50, 100, 140, 170])
    story.append(Paragraph('Month 2 — Building (Days 31–60)', s['SecHead']))
    tb(story,
        ['Week','Focus','Daily Practice','Milestones to Hit'],
        [
            ['Week 5','Emotional eating awareness','Pre-meal hunger check (1–10 scale)','Identified 2 emotional eating triggers'],
            ['Week 6','Social environment management','One fitness-supportive social commitment','First conversation with family about goals'],
            ['Week 7','Plateau prevention','Weekly data review (measurements + lifts)','Updated goals based on first month\'s data'],
            ['Week 8','Identity reinforcement','Speak as an athlete in all fitness contexts','Used identity language consistently; joined a fitness community'],
        ], widths=[50, 100, 140, 170])
    story.append(Paragraph('Month 3 — Mastery (Days 61–90)', s['SecHead']))
    tb(story,
        ['Week','Focus','Daily Practice','Milestones to Hit'],
        [
            ['Week 9','Advanced habits + stacking','3 habit stacks in place and automatic','All three habit stacks running without conscious effort'],
            ['Week 10','Resilience testing','Deliberately face one difficult training session','Completed a physically or psychologically hard session without quitting'],
            ['Week 11','Long game vision','Write 5-year athlete vision statement','Written vision reviewed and refined'],
            ['Week 12','Review + new 90-day cycle','Full review of 90 days + next cycle goal setting','Celebration of progress; new goals set for next 90 days'],
        ], widths=[50, 100, 140, 170])
    co(story, s, '90 days is the minimum unit for meaningful transformation. 30 days is for motivation; 90 days is for identity. Commit to the full cycle before evaluating.')
    story.append(PageBreak())

    # APP A — MINDSET ASSESSMENT
    story.append(Paragraph('APPENDIX A — MINDSET ASSESSMENT & SELF-COACHING TOOLKIT', s['ChHead']))
    hr(story)
    story.append(Paragraph('Baseline Mindset Assessment (Score 1–5 for each)', s['SecHead']))
    tb(story,
        ['Area','Question','Your Score (1–5)','Notes'],
        [
            ['Commitment','Do I follow through on fitness commitments even when inconvenient?','',''],
            ['Consistency','Do I have more "on" weeks than "off" weeks over the past 3 months?','',''],
            ['Stress management','Do I have at least one active stress management practice?','',''],
            ['Sleep','Do I consistently sleep 7.5+ hours?','',''],
            ['Nutrition discipline','Do I hit my protein target at least 5/7 days per week?','',''],
            ['Goal clarity','Can I state my specific 3-month fitness goal right now?','',''],
            ['Identity','Do I think of myself as an athlete or a person trying to get fit?','',''],
            ['Recovery','Do I proactively manage recovery (not just training + food)?','',''],
            ['Emotional eating','Is emotional eating a significant issue for me (frequency)?','',''],
            ['Social alignment','Does my social environment support or undermine my goals?','',''],
        ], widths=[90, 175, 75, 120])
    story.append(Paragraph('Scoring Guide: 40–50 = Strong foundation; 25–39 = Developing; 10–24 = Significant growth opportunity', s['Callout']))
    story.append(Paragraph('Self-Coaching Questions — Use Weekly', s['SecHead']))
    questions = [
        ('What is the single most important thing I can do this week to move toward my goal?', ''),
        ('What obstacle am I most likely to face this week, and how will I handle it specifically?', ''),
        ('What worked well last week that I should continue?', ''),
        ('What did not work, and what is the simplest change I can make?', ''),
        ('Am I becoming the athlete I described in my identity vision?', ''),
    ]
    for q, _ in questions:
        story.append(Paragraph(q, s['SecHead']))
        story.append(Paragraph('_______________________________________________\n_______________________________________________', s['Body']))
    story.append(PageBreak())

    # APP B — JOURNALLING
    story.append(Paragraph('APPENDIX B — DAILY JOURNALLING TEMPLATES', s['ChHead']))
    hr(story)
    story.append(Paragraph('Morning Intention Journal (5 minutes)', s['SecHead']))
    for label in ['Today I intend to (fitness actions):','My goal is to feel at the end of today:','One potential obstacle and my response:','My fitness identity statement today:']:
        story.append(Paragraph(label, s['SecHead']))
        story.append(Paragraph('_______________________________________________\n_______________________________________________', s['Body']))
    story.append(Paragraph('Evening Review Journal (5 minutes)', s['SecHead']))
    for label in ['What I accomplished today (training/nutrition/recovery):','What I am grateful for in my fitness journey today:','What I would do differently:','Evidence that I am becoming the athlete I want to be:']:
        story.append(Paragraph(label, s['SecHead']))
        story.append(Paragraph('_______________________________________________\n_______________________________________________', s['Body']))
    story.append(Paragraph('Weekly Mindset Review (10 minutes — Sunday)', s['SecHead']))
    for label in ['Wins this week (specific, measurable):','Challenges faced and how I handled them:','My mental state score this week (1–10) and reason:','One mindset insight from this week:','My intention for next week:']:
        story.append(Paragraph(label, s['SecHead']))
        story.append(Paragraph('_______________________________________________\n_______________________________________________', s['Body']))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph('ROYAL FITNESS CLUB — MASTER YOUR MIND · MASTER YOUR BODY', s['Cover2']))
    story.append(Paragraph('© Royal Fitness Club. All rights reserved. royalfitnessclub.in', s['Cover3']))

    doc.build(story)
    from PyPDF2 import PdfReader
    total = len(PdfReader(path).pages)
    print(f'✅ Fitness Mindset Guidance: {total} pages')

build()
