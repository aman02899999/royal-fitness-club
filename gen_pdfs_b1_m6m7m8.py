#!/usr/bin/env python3
"""Generate cs_b1 M6 (Mindset, 30min), M7 (Common Mistakes, 30min), M8 (Assessment, 20min)"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

OUT = '/home/user/royal-fitness-club/course_pdfs/beginner'
W, H = A4
RFC_RED=colors.HexColor('#E8001D'); RFC_DARK=colors.HexColor('#1A1A2E')
RFC_GOLD=colors.HexColor('#FFD700'); RFC_BLUE=colors.HexColor('#0066CC')
RFC_GREEN=colors.HexColor('#138808'); RFC_WHITE=colors.white
RFC_LIGHT=colors.HexColor('#F5F5F5'); RFC_GRAY=colors.HexColor('#555555')

S={'h1':ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=22,textColor=RFC_DARK,leading=28,spaceBefore=18,spaceAfter=10),
   'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=17,textColor=RFC_BLUE,leading=22,spaceBefore=14,spaceAfter=7),
   'h3':ParagraphStyle('h3',fontName='Helvetica-Bold',fontSize=13,textColor=RFC_DARK,leading=18,spaceBefore=10,spaceAfter=5),
   'body':ParagraphStyle('body',fontName='Helvetica',fontSize=11,textColor=RFC_GRAY,leading=17,spaceAfter=7,alignment=TA_JUSTIFY),
   'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=11,textColor=RFC_GRAY,leading=16,spaceAfter=4,leftIndent=18,bulletIndent=6),
   'caption':ParagraphStyle('cap',fontName='Helvetica',fontSize=9,textColor=RFC_GRAY,leading=13,alignment=TA_CENTER),
   'cert':ParagraphStyle('cert',fontName='Helvetica-Bold',fontSize=15,textColor=RFC_DARK,leading=22,alignment=TA_CENTER,spaceBefore=12,spaceAfter=8),
   'q':ParagraphStyle('q',fontName='Helvetica',fontSize=11,textColor=RFC_DARK,leading=17,spaceAfter=6),
   'ans':ParagraphStyle('ans',fontName='Helvetica',fontSize=10,textColor=RFC_GRAY,leading=14,spaceAfter=3,leftIndent=16),
   }

def cover(course_name,mod_num,mod_title,duration,code):
    e=[]
    bar=Table([['']], colWidths=[W-40*mm], rowHeights=[6])
    bar.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('LINEBELOW',(0,0),(-1,-1),2,RFC_GOLD)]))
    e.append(Spacer(1,8*mm));e.append(bar);e.append(Spacer(1,18*mm))
    logo=Table([['ROYAL FITNESS CLUB']],colWidths=[W-40*mm])
    logo.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_DARK),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),28),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),18),('BOTTOMPADDING',(0,0),(-1,-1),18)]))
    e.append(logo);e.append(Spacer(1,6*mm))
    e.append(HRFlowable(width='100%',thickness=3,color=RFC_GOLD));e.append(Spacer(1,10*mm))
    ct=Table([[course_name]],colWidths=[W-40*mm])
    ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_BLUE),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),15),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    e.append(ct);e.append(Spacer(1,14*mm))
    badge=Table([[f'MODULE {mod_num}']],colWidths=[50*mm])
    badge.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),13),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    e.append(badge);e.append(Spacer(1,8*mm))
    e.append(Paragraph(mod_title,S['h1']));e.append(Spacer(1,6*mm))
    meta=Table([['Duration',f'{duration} minutes'],['Course Code',code],['Level','Beginner'],['Format','Study Guide PDF']],
               colWidths=[45*mm,W-40*mm-47*mm])
    meta.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),RFC_DARK),('BACKGROUND',(1,0),(1,-1),RFC_LIGHT),
        ('TEXTCOLOR',(0,0),(0,-1),RFC_WHITE),('TEXTCOLOR',(1,0),(1,-1),RFC_DARK),
        ('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTNAME',(1,0),(1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),11),('ALIGN',(0,0),(0,-1),'RIGHT'),('ALIGN',(1,0),(1,-1),'LEFT'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(0,-1),8),('RIGHTPADDING',(0,0),(0,-1),8),('LEFTPADDING',(1,0),(1,-1),10),
        ('LINEBELOW',(0,0),(-1,-2),0.5,colors.white)]))
    e.append(meta);e.append(Spacer(1,14*mm))
    flag=Table([['']*3],colWidths=[(W-40*mm)/3]*3,rowHeights=[8])
    flag.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),colors.HexColor('#FF9933')),
        ('BACKGROUND',(1,0),(1,0),RFC_WHITE),('BACKGROUND',(2,0),(2,0),RFC_GREEN)]))
    e.append(flag);e.append(Spacer(1,8*mm))
    e.append(Paragraph('Part of the Royal Fitness Club Professional Certification Program.',S['caption']))
    e.append(PageBreak())
    return e

def sd(t):
    tb=Table([[t]],colWidths=[W-40*mm])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),13),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),12)]))
    return tb

def ib(title,items,bg=RFC_DARK):
    rows=[[Paragraph(title,ParagraphStyle('bt',fontName='Helvetica-Bold',fontSize=12,textColor=RFC_WHITE,leading=16))]]
    for it in items:
        rows.append([Paragraph(f'• {it}',ParagraphStyle('bb',fontName='Helvetica',fontSize=11,textColor=RFC_DARK,leading=15,spaceAfter=3))])
    t=Table(rows,colWidths=[W-40*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),bg),('BACKGROUND',(0,1),(-1,-1),RFC_LIGHT),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEBELOW',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),('BOX',(0,0),(-1,-1),1.5,bg)]))
    return t

def mt(headers,rows):
    n=len(headers);cw=(W-40*mm)/n;data=[headers]+rows
    t=Table(data,colWidths=[cw]*n)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),RFC_BLUE),('TEXTCOLOR',(0,0),(-1,0),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),('ROWBACKGROUNDS',(0,1),(-1,-1),[RFC_LIGHT,RFC_WHITE]),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),('BOX',(0,0),(-1,-1),1,RFC_BLUE)]))
    return t

def p(t): return Paragraph(t,S['body'])
def h1(t): return Paragraph(t,S['h1'])
def h2(t): return Paragraph(t,S['h2'])
def bl(t): return Paragraph(f'• {t}',S['bullet'])
def sp(n=8): return Spacer(1,n)

# ═══════════════════════════════════
# MODULE 6: Mindset, Habits & Goals
# ═══════════════════════════════════
def gen_b1_m6():
    fname=os.path.join(OUT,'cs_b1_mod6_mindset_habits.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover('Fitness Foundations Certificate',6,'Mindset, Habits & Goal Setting',30,'CS_B1')

    e.append(sd('SECTION 1: The Psychology of Behaviour Change'))
    e.append(sp(6))
    e.append(h1('Why Most People Fail to Stay Consistent'))
    e.append(p('Knowledge is not the bottleneck. Most people know that exercise is good for '
               'them and that vegetables are healthier than processed food. The bottleneck is '
               'behaviour — the consistent execution of desired actions despite competing '
               'priorities, low motivation, and environmental friction.'))
    e.append(p('Behavioural science identifies four core reasons fitness programmes fail:'))
    e.append(mt(
        ['Failure Mode','Root Cause','Solution'],
        [['Starting too big','Ambition exceeds current habit capacity','Start with minimum viable workout (20 min 2×/week)'],
         ['Motivation dependency','Treating motivation as a prerequisite','Build habit loops that don\'t require motivation'],
         ['All-or-nothing thinking','One missed session = programme failure','"Never miss twice" rule; session consistency over perfection'],
         ['Identity mismatch','Behaviour conflicts with self-image','Reframe identity: "I am someone who trains"'],
        ]
    ))
    e.append(sp(8))

    e.append(sd('SECTION 2: SMART Goal Framework'))
    e.append(sp(6))
    e.append(h1('Goals That Actually Drive Action'))
    e.append(p('Vague goals produce vague results. "Get fit" is not a goal — it is a wish. '
               'The SMART framework transforms wishes into actionable targets with clear '
               'success criteria:'))
    e.append(mt(
        ['Letter','Stands For','Poor Goal','SMART Goal'],
        [['S','Specific','Get stronger','Increase barbell squat from 60kg to 80kg'],
         ['M','Measurable','Lose weight','Lose 5kg of body fat (measured by DEXA scan)'],
         ['A','Achievable','Run a marathon (never ran before)','Complete 5km non-stop in 12 weeks'],
         ['R','Relevant','Do yoga (hates yoga)','Improve hip mobility by 15° (relevant to squatting)'],
         ['T','Time-bound','Build muscle someday','Gain 3kg of lean mass in 16 weeks'],
        ]
    ))
    e.append(sp(8))
    e.append(h2('Process vs Outcome Goals'))
    e.append(p('<b>Outcome goals</b> (lose 10kg) define the destination. <b>Process goals</b> '
               '(train 3×/week, hit 1.8g protein/kg, sleep 8 hours) define the actions that '
               'produce the destination. Process goals are 100% within your control; outcome '
               'goals are not. Research consistently shows process-goal focus produces better '
               'long-term outcomes than outcome-goal focus alone.'))
    e.append(p('<b>Implementation intentions:</b> "When X, I will Y." Research by Peter '
               'Gollwitzer shows that adding an implementation intention to a goal (e.g., '
               '"When I finish work at 6pm, I will go directly to the gym before going home") '
               'increases follow-through rate by 200–300%.'))
    e.append(sp())

    e.append(sd('SECTION 3: Habit Stacking and Routine Design'))
    e.append(sp(6))
    e.append(h1('Building Fitness into Life'))
    e.append(p('A habit is a behaviour that has become automatic through repetition — it requires '
               'minimal cognitive effort and is triggered by environmental cues. Habit formation '
               'follows a loop: Cue → Routine → Reward (BJ Fogg / Charles Duhigg).'))
    e.append(p('<b>Habit stacking</b> links a new behaviour to an existing habit: '
               '"After [CURRENT HABIT], I will [NEW HABIT]." This is the most reliable '
               'method for inserting exercise into a busy life without relying on willpower.'))
    e.append(ib('Habit Stack Examples for Fitness',[
        'After I make morning coffee → I do 10 minutes of mobility work',
        'After I park my car at work → I take the stairs instead of the lift',
        'After dinner → I lay out tomorrow\'s gym clothes and pack my bag',
        'After brushing teeth → I take my supplements and drink 500ml water',
        'On Sunday evening → I meal prep 4 days of lunches',
    ],RFC_GREEN))
    e.append(sp(8))
    e.append(h2('Environmental Design — The Invisible Architect'))
    e.append(p('Your environment shapes your behaviour more than willpower. Designing your '
               'environment to make healthy choices easy (and unhealthy choices hard) dramatically '
               'increases adherence without requiring motivation:'))
    for it in ['Gym bag packed the night before → removes activation energy barrier in the morning',
               'Protein powder on the counter (not in a cupboard) → increases use frequency',
               'Healthy food at eye level in the fridge; unhealthy food behind or in opaque containers',
               'Gym shoes visible near the door → visual cue triggers training habit',
               'Phone on do-not-disturb 30 minutes before sleep → protects sleep schedule']:
        e.append(bl(it))
    e.append(sp())

    e.append(sd('SECTION 4: Tracking Progress'))
    e.append(sp(6))
    e.append(h1('What Gets Measured Gets Managed'))
    e.append(p('Tracking creates accountability, reveals patterns, and provides objective '
               'feedback that prevents stagnation. However, over-tracking creates obsession '
               'and anxiety — a balance is needed.'))
    e.append(mt(
        ['Metric','How to Track','Frequency','What It Shows'],
        [['Body weight','Morning, after toilet, fasted','Daily — average the week','Energy balance trend (not daily reality)'],
         ['Training log','Sets, reps, weight per exercise','Every session','Strength progress; volume management'],
         ['Progress photos','Same time, lighting, pose','Monthly','Body composition changes invisible on scale'],
         ['Measurements','Tape measure (waist, hips, chest, arms)','Monthly','Recomp; shows muscle gain + fat loss simultaneously'],
         ['Energy/mood journal','Rate 1–10 daily','Daily or weekly','Recovery quality; identify overtraining early'],
         ['Nutrition diary','App like MyFitnessPal','First 4–8 weeks initially','Calibrate portion sizes and macro awareness'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>The scale lie:</b> Body weight fluctuates 1–3kg daily due to hydration, '
               'glycogen, menstrual cycle, bowel content, and sodium intake. Never judge '
               'programme success on one weigh-in. Use 7-day rolling averages.'))
    e.append(sp())

    e.append(sd('SECTION 5: Managing Plateaus and Setbacks'))
    e.append(sp(6))
    e.append(h1('Plateaus Are a Feature, Not a Bug'))
    e.append(p('A training plateau occurs when performance or body composition stops changing '
               'despite continued effort. Far from a failure, plateaus signal that the body has '
               'adapted to the current stimulus — a sign that the programme is working. '
               'The solution is to introduce a new variable to disrupt the adaptation.'))
    e.append(mt(
        ['Plateau Type','Root Cause','Intervention'],
        [['Strength plateau','Neural adaptation complete; need more volume or specificity','Change rep ranges, add volume, change exercise variation'],
         ['Weight loss plateau','TDEE decrease (metabolic adaptation); dietary drift','Diet break or diet phase 2 weeks; reduce calories 100–200kcal; recount macros'],
         ['Muscle gain plateau','Insufficient protein, calories, or volume','Increase protein 0.2g/kg; add 1 working set; verify sleep'],
         ['Motivation plateau','Novelty worn off; intrinsic motivation needed','New training goal; group class; competition; new environment'],
        ]
    ))
    e.append(sp(8))
    e.append(ib('Module 6 Key Takeaways',[
        'Behaviour change fails not from lack of knowledge but from habit architecture and identity mismatch',
        'SMART goals + implementation intentions dramatically increase follow-through',
        'Process goals (actions) are more controllable than outcome goals (results) — focus there first',
        'Habit stacking inserts new fitness habits into existing routines without willpower',
        'Environmental design makes healthy choices the path of least resistance',
        'Track 3–4 key metrics consistently; 7-day average weight vs single daily reading',
        'Plateaus are adaptations — respond with strategic programme changes, not panic',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['What is habit stacking and how does it differ from willpower-based behaviour change?',
        'Write a SMART goal for fat loss that includes both outcome and process components.',
        'Why does the scale fluctuate 1–3kg daily, and why is the 7-day average more meaningful?',
        'What is an implementation intention? Write one for a morning workout habit.',
        'Describe three environmental design changes that would increase training adherence without motivation.',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════
# MODULE 7: Common Beginner Mistakes
# ═══════════════════════════════════
def gen_b1_m7():
    fname=os.path.join(OUT,'cs_b1_mod7_common_mistakes.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover('Fitness Foundations Certificate',7,'Common Beginner Mistakes & How to Avoid Them',30,'CS_B1')

    e.append(sd('SECTION 1: Why Beginners Make Predictable Mistakes'))
    e.append(sp(6))
    e.append(h1('The Four Categories of Beginner Error'))
    e.append(p('Beginning a fitness journey is exciting — but enthusiasm without knowledge '
               'produces a predictable set of mistakes that slow progress, increase injury risk, '
               'and ultimately cause most beginners to quit within 3–6 months. Understanding '
               'these errors — and their solutions — dramatically improves long-term success.'))
    e.append(p('Beginner mistakes cluster into four categories:'))
    for it in ['Training errors (technique, programme structure, volume management)',
               'Nutrition errors (caloric understanding, protein intake, meal timing)',
               'Recovery errors (overtraining, insufficient sleep, ignoring warm-up)',
               'Psychological errors (comparison, impatience, all-or-nothing thinking)']:
        e.append(bl(it))
    e.append(sp())

    e.append(sd('SECTION 2: Training Mistakes'))
    e.append(sp(6))
    e.append(h1('Mistake 1 — Ego Lifting'))
    e.append(p('<b>What it looks like:</b> Using more weight than technique allows. Shortened ROM, '
               'excessive momentum, body contortions, grinding through reps with compromised form.'))
    e.append(p('<b>Why beginners do it:</b> Social comparison on the gym floor; desire to progress '
               'quickly; misunderstanding that more weight always means more stimulus.'))
    e.append(p('<b>The reality:</b> Ego lifting reduces muscle recruitment (partial ROM = partial '
               'stimulus), dramatically increases injury risk (lower back, shoulder impingement, '
               'bicep tear), and builds poor motor patterns that must be unlearned later.'))
    e.append(p('<b>The solution:</b> "Check your ego at the door." Use the minimum weight that '
               'allows perfect technique through full ROM. Ego-check: film yourself from the '
               'side and assess objectively.'))
    e.append(ib('The 10% Rule',['Never increase training load (weight, volume, or distance) by more than 10% per week',
        'This applies to: weight on the bar, total weekly sets, weekly running mileage',
        'The body (especially tendons) needs 6–12 months to fully adapt to new loads',
        'Exceeding 10% is the primary driver of overuse injuries in new exercisers',
        ],RFC_RED))
    e.append(sp(8))

    e.append(h1('Mistake 2 — Cardio for Fat Loss (and Ignoring Resistance Training)'))
    e.append(p('<b>The misconception:</b> Hours on the treadmill burn fat; lifting weights is for '
               '"bulking" and will make you too big.'))
    e.append(p('<b>The science:</b> Resistance training is superior to steady-state cardio for '
               'long-term body composition for multiple reasons:'))
    for it in ['Builds lean muscle mass, which increases resting metabolic rate (RMR) — each kg of muscle burns ~13kcal/day extra',
               'Produces greater EPOC — elevated calorie burn persists for 24–48 hours post-session',
               'Preserves muscle during caloric deficit (without resistance training, 25–40% of weight loss can be muscle)',
               'Bone density improvement — cardio provides no meaningful BMD benefit',
               'Metabolic health: resistance training improves insulin sensitivity comparably to aerobic training']:
        e.append(bl(it))
    e.append(p('<b>Evidence:</b> Studies comparing equal-calorie-burn resistance vs cardio training '
               'show resistance training produces greater fat loss and body recomposition at 12 weeks.'))
    e.append(p('<b>Optimal approach:</b> Combine resistance training (primary) with cardiovascular '
               'exercise (supplementary). For general fitness: 3 resistance sessions + 2 cardio '
               'sessions per week.'))
    e.append(sp())

    e.append(h1('Mistake 3 — Neglecting Compound Movements'))
    e.append(p('Beginners often gravitate toward machine isolations (leg extension, cable curl, '
               'pec deck) over compound barbell movements. While machines have their place, '
               'building a foundation exclusively on isolations delays progress.'))
    e.append(mt(
        ['Compound vs Isolation','Calorie Burn','Muscles Activated','Hormonal Response','Real-World Transfer'],
        [['Barbell Squat (compound)','High','Quads, glutes, hamstrings, core, back','Significant GH + testosterone elevation','High — mirrors functional movement'],
         ['Leg Extension (isolation)','Low','Quadriceps only','Minimal','Low — rarely used in isolation outside gym'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Priority hierarchy for beginners:</b> Master the squat, deadlift, bench press, '
               'overhead press, and row before layering in isolation work. These five movements '
               'train every muscle in the body and build the strength base from which isolation '
               'work becomes meaningful.'))
    e.append(sp())

    e.append(h1('Mistake 4 — Skipping Warm-Up and Cool-Down'))
    e.append(p('The warm-up feels like "wasted time" to beginners eager to start their "real" '
               'workout. This is a false economy. Research consistently shows:'))
    for it in ['Cold muscles generate 15–20% less force than warm muscles',
               'Joint lubricating synovial fluid is more viscous and less protective when cold',
               'Connective tissue (tendons, ligaments) is less extensible at low temperature',
               'Neural activation is slower when cold — reaction time and coordination are impaired',
               'Injury risk increases significantly when jumping into high-intensity exercise from rest']:
        e.append(bl(it))
    e.append(p('Even a 5-minute dynamic warm-up (leg swings, arm circles, bodyweight squat, '
               'band pull-aparts) reduces injury risk and improves performance acutely. This '
               'is not optional — it is the first exercise of every session.'))
    e.append(sp())

    e.append(sd('SECTION 3: Nutrition Mistakes'))
    e.append(sp(6))
    e.append(h1('Mistake 5 — Over-Supplementing'))
    e.append(p('The supplement industry generates billions in revenue selling beginners hope. '
               'Most supplements provide marginal benefit when diet is suboptimal. Beginners '
               'who spend money on fat burners, BCAAs, and proprietary blends while eating '
               'poorly are building on sand.'))
    e.append(mt(
        ['Supplement','Evidence Rating','Worth It?','Notes'],
        [['Creatine monohydrate','A (excellent)','YES — universally','3–5g/day; increases PCr, strength, power'],
         ['Caffeine','A (excellent)','YES — strategically','3–6mg/kg pre-workout; tolerance develops'],
         ['Whey protein','A (good)','YES — if diet protein low','Just concentrated food protein; not magic'],
         ['Vitamin D3 + K2','B (good)','YES — most are deficient','1000–4000 IU D3 + 100mcg K2'],
         ['Omega-3 (EPA+DHA)','B (good)','YES — anti-inflammatory','1–3g EPA+DHA daily; especially if no fatty fish'],
         ['Beta-alanine','B (moderate)','Conditional','Buffers H+; causes tingling; useful for 1–4 min efforts'],
         ['BCAAs','D (poor)','NO if diet protein adequate','Redundant with adequate dietary protein (food has BCAAs)'],
         ['Fat burners','F (no evidence)','NO','Thermogenics have trivial effect; many dangerous'],
         ['Testosterone boosters','F (no evidence)','NO','No supplement increases testosterone meaningfully in healthy adults'],
        ]
    ))
    e.append(sp(8))

    e.append(h1('Mistake 6 — Insufficient Protein'))
    e.append(p('This is the most consistent nutritional error in beginners: dramatically '
               'under-eating protein while training hard. Body recomposition (gaining muscle '
               'while losing fat simultaneously) is most accessible to beginners — but requires '
               'adequate protein to preserve lean tissue during a caloric deficit.'))
    e.append(p('<b>The result of under-eating protein while training:</b> Weight loss occurs, '
               'but 30–40% of that loss is lean muscle — reducing RMR, strength, and '
               'physical capacity. This is "skinny-fat" — losing weight but not improving '
               'body composition.'))
    e.append(p('<b>Target:</b> 1.6–2.2g protein/kg body weight/day. For a 70kg individual: '
               '112–154g protein/day. This requires intentional meal planning — protein '
               'does not "just happen" at adequate levels on a Western diet.'))
    e.append(sp())

    e.append(sd('SECTION 4: Recovery and Sleep Mistakes'))
    e.append(sp(6))
    e.append(h1('Mistake 7 — Training Every Day Without Rest'))
    e.append(p('"More is better" is a dangerous training philosophy. Muscles grow during '
               'recovery, not during training. Programming six or seven heavy sessions per '
               'week without recovery produces diminishing returns and can trigger overtraining '
               'syndrome (OTS) — a serious condition characterised by:'))
    for it in ['Persistent fatigue despite adequate sleep',
               'Declining performance over 2+ weeks despite continued training',
               'Elevated resting heart rate (>5–10bpm above baseline)',
               'Mood disturbance: irritability, depression, decreased motivation',
               'Increased injury frequency',
               'Suppressed immune function (frequent illness)']:
        e.append(bl(it))
    e.append(p('<b>OTS recovery</b> requires 2–6 weeks of drastically reduced training. '
               'Prevention is critical — deload weeks and adequate rest days are the solution.'))
    e.append(p('<b>Optimal beginner schedule:</b> 3 full-body sessions/week with 1 active '
               'recovery day and 3 rest days. This allows full muscle protein synthesis cycles '
               'to complete between sessions.'))
    e.append(ib('Top 10 Beginner Mistakes — Summary',[
        '1. Ego lifting — prioritise technique over weight, always',
        '2. Cardio-only approach — resistance training is essential for body recomposition',
        '3. Avoiding compound lifts — squat/deadlift/press/pull are the foundation',
        '4. Skipping warm-up — 10 minutes RAMP saves months of rehab later',
        '5. Over-supplementing — fix food first; creatine + protein are the only beginner essentials',
        '6. Insufficient protein — track macros for 4–8 weeks to calibrate; 1.6–2.2g/kg/day',
        '7. Training daily without rest — muscles grow during recovery, not training',
        '8. Neglecting sleep — 7–9 hours is non-negotiable; GH release requires deep N3 sleep',
        '9. Comparison to others on social media — genetics, PEDs, lighting, and editing are ubiquitous',
        '10. Programme hopping — spend 12+ weeks on one programme before evaluating and switching',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Why is steady-state cardio inferior to resistance training for long-term fat loss?',
        'What are five signs of overtraining syndrome?',
        'Which two supplements are evidence-backed for beginners, and why?',
        'Explain "ego lifting" and provide three objective ways to check if you are doing it.',
        'Why does programme hopping slow progress? What is the minimum time on one programme before evaluating?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════
# MODULE 8: Final Assessment (20 min)
# ═══════════════════════════════════
def gen_b1_m8():
    fname=os.path.join(OUT,'cs_b1_mod8_final_assessment.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover('Fitness Foundations Certificate',8,'Final Assessment & Certificate',20,'CS_B1')

    # Instructions
    e.append(sd('ASSESSMENT INSTRUCTIONS'))
    e.append(sp(6))
    e.append(ib('How to Complete This Assessment',[
        'This is a 25-question multiple-choice assessment covering all 7 modules',
        'Each question has one correct answer (A, B, C, or D)',
        'Passing score: 70% (18/25 correct)',
        'You may refer to your module notes — this is an open-book assessment',
        'Complete in order; do not skip and return (track time: target 20 minutes)',
        'Answer key is provided at the end of this document',
    ],RFC_BLUE))
    e.append(sp(12))

    # Questions
    e.append(sd('SECTION A: Anatomy & Physiology (Questions 1–7)'))
    e.append(sp(8))
    questions = [
        ('1. Which type of bone is found at the end of long bones and provides a spongy lattice that distributes compressive load?',
         ['A) Compact (cortical) bone','B) Cortical endplate','C) Cancellous (trabecular) bone','D) Periosteum'],'C'),
        ('2. The Sliding Filament Theory of muscle contraction states that:',
         ['A) Myosin and actin filaments both shorten during contraction','B) Actin filaments slide over myosin, shortening the sarcomere','C) ATP is not required for cross-bridge detachment','D) Type I fibres generate more force than Type IIx fibres'],'B'),
        ('3. Which of the four rotator cuff muscles is responsible for shoulder internal rotation?',
         ['A) Infraspinatus','B) Supraspinatus','C) Teres minor','D) Subscapularis'],'D'),
        ('4. The Henneman Size Principle states that:',
         ['A) Larger motor units are always recruited first','B) Motor units are recruited from smallest to largest as force demands increase','C) Type IIx fibres are recruited before Type I at low intensities','D) Motor unit synchronisation decreases with training'],'B'),
        ('5. Which energy system is the primary fuel source during a 200m sprint?',
         ['A) Oxidative phosphorylation','B) Creatine phosphate (ATP-PCr) system','C) Glycolytic (anaerobic) system','D) Beta-oxidation of fats'],'C'),
        ('6. VO2 max is best improved by training in which intensity zone?',
         ['A) 50–60% HRmax (Zone 1 — recovery)','B) 65–75% HRmax (Zone 2 — aerobic base)','C) 85–95% HRmax (Zone 4 — VO2 max zone)','D) 100%+ HRmax (Zone 5 — anaerobic)'],'C'),
        ('7. Growth hormone (GH) is primarily released:',
         ['A) Immediately before exercise','B) During light aerobic exercise','C) During N3 deep sleep (first cycle of the night)','D) After eating a high-carbohydrate meal'],'C'),
    ]
    e.append(sd('SECTION B: Training & Programme Design (Questions 8–14)'))
    questions += [
        ('8. Which rep range is best supported by research for maximising muscle hypertrophy?',
         ['A) 1–5 reps at 90–100% 1RM','B) 6–20 reps at 65–85% 1RM','C) 20–50 reps at 30–50% 1RM','D) No single range; intensity must always exceed 85% 1RM'],'B'),
        ('9. A beginner performs 3 sets of 8 squats at 60kg and completes 10 reps on the final set. Two sessions in a row this happens. According to the 2-for-2 rule, they should:',
         ['A) Continue at 60kg until they can consistently complete 12 reps','B) Immediately increase to 70kg to challenge themselves more','C) Increase to 62.5kg at the next session','D) Reduce to 55kg to practise perfect technique at lower load'],'C'),
        ('10. The SAID principle stands for:',
         ['A) Strength Adaptation In Determined individuals','B) Specific Adaptation to Imposed Demand','C) Standard Assessment for Incremental Development','D) Sequential Adaptation In Development'],'B'),
        ('11. Which training split provides the highest muscle group training frequency per week for a beginner training 3 days per week?',
         ['A) Body part split (chest day, back day, leg day)','B) Push/Pull/Legs split','C) Full-body split','D) Upper/Lower split'],'C'),
        ('12. The RAMP warm-up protocol stands for:',
         ['A) Resistance, Activation, Mobility, Power','B) Raise, Activate, Mobilise, Potentiate','C) Range, Aerobic, Muscle, Preparation','D) Readiness, Activation, Movement, Performance'],'B'),
        ('13. During a deload week, the primary goal is to:',
         ['A) Achieve maximum strength by testing 1RM lifts','B) Rest completely and do no physical activity','C) Reduce training volume to allow fatigue dissipation and enable supercompensation','D) Switch to purely cardiovascular training to maintain calorie burn'],'C'),
        ('14. Which type of exercise produces the greatest Excess Post-Exercise Oxygen Consumption (EPOC)?',
         ['A) 60-minute steady-state walking','B) 30-minute moderate-intensity cycling (60% VO2 max)','C) Heavy compound resistance training and HIIT intervals','D) Light stretching and yoga flow'],'C'),
    ]
    e.append(sd('SECTION C: Nutrition (Questions 15–20)'))
    questions += [
        ('15. The primary driver of muscle protein synthesis (MPS) is activation of which intracellular complex?',
         ['A) AMPK','B) mTORC1','C) FOXO3','D) NF-κB'],'B'),
        ('16. A 30-year-old male, 80kg, 178cm trains 4 days/week. His BMR (Mifflin-St Jeor) is approximately 1850 kcal. What is his TDEE?',
         ['A) 1850 kcal','B) 2220 kcal','C) 2868 kcal','D) 3330 kcal'],'C'),
        ('17. Which fatty acid type is associated with strong anti-inflammatory effects and should be prioritised in an athlete\'s diet?',
         ['A) Saturated fatty acids','B) Trans fatty acids','C) Omega-6 polyunsaturated fatty acids','D) Omega-3 polyunsaturated fatty acids (EPA + DHA)'],'D'),
        ('18. The optimal protein intake per meal to maximally stimulate muscle protein synthesis is approximately:',
         ['A) 5–10g of any protein source','B) 20–40g of a complete, high-leucine protein source','C) 50g+ regardless of leucine content','D) 10–15g immediately before training only'],'B'),
        ('19. Dietary fat intake should NOT fall below approximately what percentage of total calories to protect hormonal health?',
         ['A) 5%','B) 10%','C) 15%','D) 25%'],'C'),
        ('20. A urine colour described as "dark yellow / apple juice" indicates:',
         ['A) Optimal hydration','B) Mild dehydration requiring 250–500ml additional fluid','C) Severe dehydration requiring medical attention','D) Excess vitamin supplementation with no action needed'],'B'),
    ]
    e.append(sd('SECTION D: Recovery, Mindset & Common Mistakes (Questions 21–25)'))
    questions += [
        ('21. DOMS (Delayed-Onset Muscle Soreness) is primarily caused by:',
         ['A) Lactic acid accumulation remaining in the muscle 24–48 hours after exercise','B) Microscopic eccentric muscle fibre damage and subsequent inflammatory response','C) Dehydration and electrolyte imbalance in muscle tissue','D) Insufficient warm-up causing muscle spasm'],'B'),
        ('22. Which supplement has the strongest evidence base and is most universally recommended for strength and power athletes?',
         ['A) BCAAs (branched-chain amino acids)','B) Fat burners/thermogenics','C) Creatine monohydrate (3–5g/day)','D) Testosterone boosters'],'C'),
        ('23. The testosterone:cortisol ratio is most likely to become unfavourable when:',
         ['A) Training sessions are kept under 45 minutes','B) Training is performed in a fully rested, well-fed state','C) High-intensity training sessions consistently exceed 90 minutes','D) Resistance training is combined with 20 minutes of aerobic work'],'C'),
        ('24. Cold water immersion (ice bath) post-workout is BEST suited to which scenario?',
         ['A) A beginner in their first 12-week hypertrophy block','B) An athlete competing in back-to-back games requiring rapid recovery','C) A powerlifter training a new 1RM PR','D) Anyone trying to maximise muscle gain in an off-season'],'B'),
        ('25. According to the SMART goal framework, which of the following is the best example of a specific, measurable goal?',
         ['A) "Get fit and feel healthier this year"','B) "Exercise more consistently starting next month"','C) "Increase my 5km run time from 32 minutes to 26 minutes within 12 weeks"','D) "Lose some weight and build muscle by summer"'],'C'),
    ]

    for qtext, opts, ans in questions:
        e.append(Paragraph(qtext, S['q']))
        for opt in opts:
            e.append(Paragraph(opt, S['ans']))
        e.append(sp(10))

    # Answer Key
    e.append(PageBreak())
    e.append(sd('ANSWER KEY'))
    e.append(sp(8))
    answers = [('C','Cancellous bone'),('B','Sliding filament — actin slides'),
               ('D','Subscapularis — IR'),('B','Henneman size principle'),
               ('C','Glycolytic system — 200m'),('C','Zone 4 85–95% HRmax'),
               ('C','N3 deep sleep — GH pulse'),('B','6–20 reps hypertrophy'),
               ('C','2-for-2 rule → +2.5kg'),('B','SAID principle'),
               ('C','Full body = highest freq for 3-day'),('B','RAMP warm-up'),
               ('C','Deload = reduce volume/fatigue'),('C','HIIT+compounds = max EPOC'),
               ('B','mTORC1 drives MPS'),('C','1850×1.55=2868 kcal'),
               ('D','Omega-3 EPA+DHA anti-inflammatory'),('B','20–40g leucine-rich protein'),
               ('C','15% min fat for hormones'),('B','Dark yellow = mild dehydration'),
               ('B','DOMS = eccentric damage + inflammation'),('C','Creatine monohydrate'),
               ('C','>90 min = cortisol rises, T:C unfavourable'),('B','Back-to-back competition'),
               ('C','SMART — specific 5km in 12 weeks')]
    key_rows=[[f'Q{i+1}',a[0],a[1]] for i,a in enumerate(answers)]
    key_tbl=Table([['Question','Answer','Key Concept']]+key_rows,colWidths=[30*mm,20*mm,W-40*mm-55*mm])
    key_tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),RFC_DARK),('TEXTCOLOR',(0,0),(-1,0),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[RFC_LIGHT,RFC_WHITE]),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC'))]))
    e.append(key_tbl)
    e.append(sp(16))

    # Certificate template
    e.append(PageBreak())
    cert=Table([['ROYAL FITNESS CLUB\nFITNESS FOUNDATIONS CERTIFICATE']],colWidths=[W-40*mm])
    cert.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_DARK),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),20),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),22),('BOTTOMPADDING',(0,0),(-1,-1),22)]))
    e.append(cert)
    e.append(HRFlowable(width='100%',thickness=3,color=RFC_GOLD))
    e.append(sp(16))
    e.append(Paragraph('This is to certify that',S['cert']))
    e.append(Paragraph('_______________________________________',ParagraphStyle('line',fontName='Helvetica-Bold',fontSize=22,textColor=RFC_DARK,alignment=TA_CENTER,leading=30,spaceAfter=8)))
    e.append(Paragraph('has successfully completed the',S['cert']))
    e.append(Paragraph('Fitness Foundations Certificate — CS_B1',ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=18,textColor=RFC_RED,alignment=TA_CENTER,leading=24,spaceBefore=8,spaceAfter=8)))
    e.append(Paragraph('demonstrating mastery of anatomy, exercise science, programme design, nutrition,\nrecovery, mindset, and applied fitness fundamentals.',
                        ParagraphStyle('sub',fontName='Helvetica',fontSize=12,textColor=RFC_GRAY,alignment=TA_CENTER,leading=18,spaceAfter=20)))
    e.append(sp(20))
    sig_data=[['___________________','___________________'],['Instructor Signature','Date']]
    sig=Table(sig_data,colWidths=[(W-40*mm)/2,(W-40*mm)/2])
    sig.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('FONTNAME',(0,0),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),11),('TEXTCOLOR',(0,0),(-1,-1),RFC_DARK)]))
    e.append(sig)
    e.append(sp(20))
    flag=Table([['']*3],colWidths=[(W-40*mm)/3]*3,rowHeights=[8])
    flag.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),colors.HexColor('#FF9933')),
        ('BACKGROUND',(1,0),(1,0),RFC_WHITE),('BACKGROUND',(2,0),(2,0),RFC_GREEN)]))
    e.append(flag)
    doc.build(e)
    print(f'Generated: {fname}')

gen_b1_m6()
gen_b1_m7()
gen_b1_m8()
print('M6, M7, M8 done. cs_b1 COMPLETE.')
