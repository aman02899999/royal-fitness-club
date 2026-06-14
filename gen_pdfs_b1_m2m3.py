#!/usr/bin/env python3
"""Generate cs_b1 M2 and M3 PDFs"""
import os, sys
sys.path.insert(0, '/home/user/royal-fitness-club')

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUT = '/home/user/royal-fitness-club/course_pdfs/beginner'
W, H = A4

RFC_RED   = colors.HexColor('#E8001D')
RFC_DARK  = colors.HexColor('#1A1A2E')
RFC_GOLD  = colors.HexColor('#FFD700')
RFC_BLUE  = colors.HexColor('#0066CC')
RFC_GREEN = colors.HexColor('#138808')
RFC_WHITE = colors.white
RFC_LIGHT = colors.HexColor('#F5F5F5')
RFC_GRAY  = colors.HexColor('#555555')

def ST():
    return {
        'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22,
            textColor=RFC_DARK, leading=28, spaceBefore=18, spaceAfter=10),
        'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=17,
            textColor=RFC_BLUE, leading=22, spaceBefore=14, spaceAfter=7),
        'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=13,
            textColor=RFC_DARK, leading=18, spaceBefore=10, spaceAfter=5),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=11,
            textColor=RFC_GRAY, leading=17, spaceAfter=7, alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=11,
            textColor=RFC_GRAY, leading=16, spaceAfter=4, leftIndent=18, bulletIndent=6),
        'caption': ParagraphStyle('cap', fontName='Helvetica', fontSize=9,
            textColor=RFC_GRAY, leading=13, alignment=TA_CENTER),
    }

S = ST()

def cover_page(course_name, mod_num, mod_title, duration, course_code):
    e = []
    bar = Table([['']], colWidths=[W-40*mm], rowHeights=[6])
    bar.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('LINEBELOW',(0,0),(-1,-1),2,RFC_GOLD)]))
    e.append(Spacer(1,8*mm)); e.append(bar); e.append(Spacer(1,18*mm))
    logo = Table([['ROYAL FITNESS CLUB']], colWidths=[W-40*mm])
    logo.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_DARK),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),28),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),18),('BOTTOMPADDING',(0,0),(-1,-1),18)]))
    e.append(logo); e.append(Spacer(1,6*mm))
    e.append(HRFlowable(width='100%',thickness=3,color=RFC_GOLD)); e.append(Spacer(1,10*mm))
    ct = Table([[course_name]], colWidths=[W-40*mm])
    ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_BLUE),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),15),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    e.append(ct); e.append(Spacer(1,14*mm))
    badge = Table([[f'MODULE {mod_num}']], colWidths=[50*mm])
    badge.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),13),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    e.append(badge); e.append(Spacer(1,8*mm))
    e.append(Paragraph(mod_title, S['h1'])); e.append(Spacer(1,6*mm))
    meta = Table([['Duration',f'{duration} minutes'],['Course Code',course_code],
                  ['Level','Beginner'],['Format','Study Guide PDF']],
                 colWidths=[45*mm, W-40*mm-47*mm])
    meta.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),RFC_DARK),('BACKGROUND',(1,0),(1,-1),RFC_LIGHT),
        ('TEXTCOLOR',(0,0),(0,-1),RFC_WHITE),('TEXTCOLOR',(1,0),(1,-1),RFC_DARK),
        ('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTNAME',(1,0),(1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),11),('ALIGN',(0,0),(0,-1),'RIGHT'),('ALIGN',(1,0),(1,-1),'LEFT'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(0,-1),8),('RIGHTPADDING',(0,0),(0,-1),8),('LEFTPADDING',(1,0),(1,-1),10),
        ('LINEBELOW',(0,0),(-1,-2),0.5,colors.white)]))
    e.append(meta); e.append(Spacer(1,14*mm))
    flag = Table([['']*3], colWidths=[(W-40*mm)/3]*3, rowHeights=[8])
    flag.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),colors.HexColor('#FF9933')),
        ('BACKGROUND',(1,0),(1,0),RFC_WHITE),('BACKGROUND',(2,0),(2,0),RFC_GREEN)]))
    e.append(flag); e.append(Spacer(1,8*mm))
    e.append(Paragraph('Part of the Royal Fitness Club Professional Certification Program.',S['caption']))
    e.append(PageBreak())
    return e

def sdiv(text):
    t = Table([[text]], colWidths=[W-40*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),13),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),12)]))
    return t

def ibox(title, items, bg=RFC_DARK):
    rows=[[Paragraph(title, ParagraphStyle('bt',fontName='Helvetica-Bold',fontSize=12,textColor=RFC_WHITE,leading=16))]]
    for item in items:
        rows.append([Paragraph(f'• {item}',ParagraphStyle('bb',fontName='Helvetica',fontSize=11,textColor=RFC_DARK,leading=15,spaceAfter=3))])
    t=Table(rows,colWidths=[W-40*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),bg),('BACKGROUND',(0,1),(-1,-1),RFC_LIGHT),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEBELOW',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),('BOX',(0,0),(-1,-1),1.5,bg)]))
    return t

def mtbl(headers,rows):
    n=len(headers); cw=(W-40*mm)/n
    data=[headers]+rows
    t=Table(data,colWidths=[cw]*n)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),RFC_BLUE),('TEXTCOLOR',(0,0),(-1,0),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),('ROWBACKGROUNDS',(0,1),(-1,-1),[RFC_LIGHT,RFC_WHITE]),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),('BOX',(0,0),(-1,-1),1,RFC_BLUE)]))
    return t

def p(text): return Paragraph(text, S['body'])
def h1(text): return Paragraph(text, S['h1'])
def h2(text): return Paragraph(text, S['h2'])
def h3(text): return Paragraph(text, S['h3'])
def bl(text): return Paragraph(f'• {text}', S['bullet'])
def sp(n=8): return Spacer(1,n)

# ═══════════════════════════════════════════════════
# MODULE 2: Exercise Science Fundamentals (50 min)
# ═══════════════════════════════════════════════════
def gen_b1_m2():
    fname = os.path.join(OUT,'cs_b1_mod2_exercise_science.pdf')
    doc = SimpleDocTemplate(fname, pagesize=A4,
        leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e = []
    e += cover_page('Fitness Foundations Certificate',2,'Exercise Science Fundamentals',50,'CS_B1')

    e.append(sdiv('SECTION 1: Energy Systems — How the Body Fuels Exercise'))
    e.append(sp(6))
    e.append(h1('The Three Energy Systems'))
    e.append(p('Every movement the human body makes is powered by adenosine triphosphate (ATP) — '
               'the universal energy currency of all biological processes. The body cannot store '
               'large quantities of ATP; at rest it contains enough for only 2–3 seconds of '
               'maximal effort. Three interlinked metabolic pathways continuously regenerate ATP '
               'from food substrates.'))
    e.append(p('Understanding which energy system dominates at different exercise intensities '
               'and durations is the cornerstone of intelligent programme design — the difference '
               'between effective conditioning and random exhaustion.'))
    e.append(sp())

    e.append(h2('Pathway 1: Phosphocreatine (ATP-PCr) System'))
    e.append(p('<b>Duration:</b> 0–10 seconds at maximal intensity'))
    e.append(p('The ATP-PCr system (also called the alactic anaerobic system) is the fastest '
               'energy pathway. Creatine phosphate (PCr) stored in the muscle donates its '
               'phosphate group to ADP, instantly regenerating ATP. No oxygen is required; '
               'no lactic acid is produced (hence "alactic").'))
    e.append(p('<b>Enzyme:</b> Creatine kinase (CK) — the rate-limiting enzyme. Activity is '
               'highest in fast-twitch fibres.'))
    for it in ['100m sprint start','Olympic weightlifting (snatch, clean & jerk)','Shot put, discus throw',
               'Basketball tip-off jump','1-rep max attempt in powerlifting']:
        e.append(bl(f'Example: {it}'))
    e.append(p('<b>Recovery:</b> PCr stores recover 50% in ~30 seconds; fully replenished in '
               '3–5 minutes. This governs rest periods in power training — 3+ minutes between '
               'true maximal efforts.'))
    e.append(p('<b>Creatine supplementation</b> (3–5g/day monohydrate) increases muscle PCr '
               'stores by ~20%, enhancing repeated sprint performance and high-intensity training '
               'volume. It is one of the most well-researched and evidence-backed sports supplements.'))
    e.append(sp())

    e.append(h2('Pathway 2: Glycolytic System'))
    e.append(p('<b>Duration:</b> 10 seconds – 2 minutes at high intensity'))
    e.append(p('Glycolysis is the metabolic breakdown of glucose (from blood) or glycogen '
               '(from muscle stores) into pyruvate. This process regenerates ATP without '
               'oxygen — it\'s faster than oxidative phosphorylation but less efficient.'))
    e.append(p('<b>Fate of pyruvate:</b> When oxygen delivery is insufficient (high intensity), '
               'pyruvate is converted to lactate by lactate dehydrogenase (LDH). This allows '
               'glycolysis to continue. Lactate is NOT the cause of muscle fatigue; rather, '
               'concurrent hydrogen ion (H⁺) accumulation lowers intracellular pH, inhibiting '
               'enzyme activity — the burning sensation during intense exercise.'))
    e.append(mtbl(
        ['Step','Substrate','Products','ATP Yield'],
        [['Fast glycolysis','Glucose/Glycogen','Pyruvate → Lactate','2 ATP (glucose), 3 ATP (glycogen)'],
         ['Slow glycolysis','Pyruvate','Acetyl-CoA (enters Krebs)','Feeds oxidative system'],
         ['Lactate shuttle','Lactate','Pyruvate (in liver, heart)','Fuel for other tissues']]
    ))
    e.append(sp(8))
    e.append(p('<b>Lactate threshold (LT):</b> The exercise intensity at which blood lactate '
               'begins to accumulate faster than it is cleared. Training near and above LT is '
               'highly effective for improving anaerobic capacity. Elite endurance athletes have '
               'LT at 85–90% VO2max; untrained individuals at 50–60%.'))
    e.append(p('<b>Training implication:</b> 200m–800m swimming, 400m–1500m running, 1–3 min '
               'HIIT intervals, and high-rep sets (15–25 reps to failure) primarily use this '
               'pathway. Rest intervals of 30–90 seconds maintain glycolytic stress.'))
    e.append(sp())

    e.append(h2('Pathway 3: Oxidative (Aerobic) System'))
    e.append(p('<b>Duration:</b> >2 minutes (dominates endurance activities)'))
    e.append(p('The aerobic system uses oxygen to completely oxidise carbohydrates, fats, and '
               '(to a lesser extent) proteins into CO₂ and H₂O, yielding far more ATP per '
               'molecule than glycolysis. It is the primary system for all activities lasting '
               'more than a few minutes at submaximal intensity.'))
    e.append(mtbl(
        ['Phase','Location','Substrate','ATP Yield per Molecule'],
        [['Glycolysis','Cytoplasm','Glucose → Pyruvate','2'],
         ['Pyruvate decarboxylation','Mitochondrial matrix','Pyruvate → Acetyl-CoA','0'],
         ['Krebs (TCA) cycle','Mitochondrial matrix','Acetyl-CoA → CO₂','2 GTP'],
         ['Oxidative phosphorylation','Inner mitochondrial membrane','NADH, FADH₂ → H₂O','~34'],
         ['Total (from glucose)','—','—','~36–38 ATP'],
         ['Beta-oxidation (fat)','Mitochondria','Fatty acids → Acetyl-CoA','~106–129 ATP per triglyceride'],
        ]
    ))
    e.append(sp(8))
    e.append(p('Fat oxidation produces more total ATP but requires more oxygen per ATP molecule. '
               'This means at very high intensities (>75–85% VO2max), carbohydrate becomes '
               'the dominant fuel despite fat\'s higher energy density — the body prioritises '
               'speed of ATP regeneration.'))
    e.append(ibox('Fuel Substrate Continuum',[
        'REST: ~50–60% fat, 40–50% carbohydrate',
        'LOW INTENSITY (40% VO2max): ~50% fat, 50% carbohydrate',
        'MODERATE INTENSITY (65% VO2max): ~30% fat, 70% carbohydrate',
        'HIGH INTENSITY (85%+ VO2max): ~5% fat, 95% carbohydrate',
        'Post-exercise: Fat oxidation dominates during recovery (EPOC effect)',
    ], RFC_BLUE))
    e.append(sp(8))

    e.append(sdiv('SECTION 2: VO2 Max — The Gold Standard of Fitness'))
    e.append(sp(6))
    e.append(h1('Understanding VO2 Max'))
    e.append(p('VO2 max (maximal oxygen uptake) is the maximum rate at which the body can '
               'consume oxygen during exhaustive exercise. It is measured in ml O₂/kg/min '
               'and represents the ceiling of aerobic energy production.'))
    e.append(p('VO2 max is determined by both central factors (cardiac output — how much '
               'blood the heart pumps per minute) and peripheral factors (oxygen extraction '
               'at the muscle). The Fick Equation captures this relationship:'))
    e.append(p('<b>VO2 max = Cardiac Output max × (a-vO₂) difference max</b>'))
    e.append(p('where (a-vO₂) is the arterio-venous oxygen difference — how much oxygen '
               'working muscles extract from arterial blood.'))
    e.append(mtbl(
        ['Population','Typical VO2 max (ml/kg/min)'],
        [['Sedentary adult male','35–40'],['Sedentary adult female','27–32'],
         ['Trained recreational male','45–55'],['Trained recreational female','38–46'],
         ['Elite marathon runner','70–80'],['Elite cyclist (e.g., VO2 max record)','~97.5'],
         ['Thoroughbred racehorse (reference)','~180']]
    ))
    e.append(sp(8))
    e.append(p('<b>How to improve VO2 max:</b> Zone 4 training (85–95% max HR) produces the '
               'greatest gains. Classic protocols: 4×4 minutes at 90–95% max HR with 3 min '
               'recovery (Norwegian 4×4 protocol). VO2 max improves 15–25% with consistent '
               'training in untrained individuals; elite athletes may gain only 2–5%.'))
    e.append(sp())

    e.append(h2('Lactate Threshold vs VO2 Max in Programming'))
    e.append(p('While VO2 max sets the ceiling, lactate threshold determines the sustainable '
               'percentage of that ceiling. Two athletes with identical VO2 max of 60 ml/kg/min '
               'may have dramatically different performance if their thresholds differ:'))
    e.append(mtbl(
        ['Athlete','VO2 max','Lactate Threshold','Threshold % of VO2 max','Practical Impact'],
        [['Athlete A','60','at 75%','75%','Can sustain higher paces before acidosis'],
         ['Athlete B','60','at 55%','55%','Fades earlier in middle-distance events']]
    ))
    e.append(sp(8))
    e.append(p('This is why experienced coaches focus heavily on threshold training (tempo runs, '
               'lactate threshold intervals) alongside VO2 max development — both determine '
               'real-world performance.'))
    e.append(sp())

    e.append(sdiv('SECTION 3: EPOC and the Afterburn Effect'))
    e.append(sp(6))
    e.append(h1('Excess Post-Exercise Oxygen Consumption (EPOC)'))
    e.append(p('After intense exercise ceases, oxygen consumption remains elevated above '
               'resting levels for minutes to hours. This elevated post-exercise oxygen '
               'consumption is called EPOC (Excess Post-Exercise Oxygen Consumption) — '
               'colloquially known as the "afterburn effect."'))
    e.append(p('<b>What drives EPOC?</b> Multiple processes require oxygen post-exercise:'))
    for it in ['Phosphocreatine resynthesis in muscle (~50% of EPOC)',
               'Restoration of blood and muscle oxygen stores (myoglobin, haemoglobin)',
               'Elevated body temperature (every 1°C rise increases metabolic rate ~10–13%)',
               'Elevated circulating catecholamines (adrenaline, noradrenaline) maintaining metabolism',
               'Gluconeogenesis — converting lactate back to glucose (Cori cycle in liver)',
               'Protein synthesis and repair (ongoing after resistance training for 24–48 hours)']:
        e.append(bl(it))
    e.append(p('<b>Magnitude of EPOC:</b> Low-intensity steady-state cardio produces minimal '
               'EPOC (returning to baseline within 30 minutes). High-intensity interval training '
               '(HIIT) and heavy resistance training produce EPOC lasting 12–24+ hours. '
               'However, total EPOC caloric contribution is often overstated — typically '
               '50–150 extra kcal after a hard 30-min HIIT session.'))
    e.append(ibox('Practical Application of EPOC',[
        'HIIT burns more total calories than steady-state of equal duration (including EPOC)',
        'Heavy compound lifts (deadlift, squat, clean) produce greater EPOC than isolation exercises',
        'Full-body resistance sessions generate more EPOC than split body-part sessions',
        'Training in a glycogen-depleted state amplifies fat oxidation during and after exercise',
        'Don\'t oversell "afterburn" to clients — sustainable consistency matters more than EPOC',
    ], RFC_RED))
    e.append(sp(8))

    e.append(sdiv('SECTION 4: Principles of Progressive Overload'))
    e.append(sp(6))
    e.append(h1('The Foundation of All Training Adaptation'))
    e.append(p('Progressive overload is the most important principle in exercise science. It '
               'states that to continually stimulate adaptation, the training stimulus must be '
               'progressively increased over time — because the body adapts and what was once '
               'a challenge becomes comfortable.'))
    e.append(p('Without progressive overload, adaptation plateaus. With too rapid progression, '
               'overuse injury occurs. The art of programming is finding the optimal rate of '
               'progression for each individual.'))
    e.append(h2('Methods of Applying Progressive Overload'))
    e.append(mtbl(
        ['Method','Example','Best Applied To'],
        [['Increase load (weight)','Add 2.5kg to bench press','Strength/hypertrophy cycles'],
         ['Increase volume (sets×reps)','Go from 3×8 to 4×8','Hypertrophy blocks'],
         ['Decrease rest intervals','Rest 90s instead of 120s','Conditioning/metabolic training'],
         ['Increase frequency','Train muscle 2×/week → 3×/week','Skill, hypertrophy'],
         ['Improve technique','Deeper squat ROM','Powerlifting, Olympic lifting'],
         ['Increase density','Same work in less time','Conditioning, fat loss'],
         ['Increase intensity techniques','Add pause, tempo, bands','Advanced hypertrophy'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>The 2-for-2 Rule:</b> When an athlete completes 2 extra reps beyond the '
               'prescribed rep range on the final set for 2 consecutive sessions, increase '
               'the load by the smallest available increment. Simple, effective, evidence-based.'))
    e.append(p('<b>Double progression:</b> First progress reps within a range (e.g., 8–12 reps), '
               'then increase weight once the top of the range is reached. Example: 60kg × 8 reps '
               '→ 60kg × 10 reps → 60kg × 12 reps → 62.5kg × 8 reps. This is the most '
               'beginner-friendly model of progression.'))
    e.append(sp())

    e.append(sdiv('SECTION 5: Deload Weeks — Planned Recovery'))
    e.append(sp(6))
    e.append(h1('Why Deloading Is Not Optional'))
    e.append(p('Supercompensation theory describes the cycle of stress → fatigue → recovery → '
               'super-compensation (elevated performance baseline). If the next training stimulus '
               'arrives during fatigue accumulation rather than super-compensation, fitness '
               'declines — a condition called overreaching, or in extreme cases, overtraining '
               'syndrome (OTS).'))
    e.append(p('A deload week involves strategically reducing training volume and/or intensity '
               'to allow full recovery while maintaining training frequency. It is not rest — '
               'it is active management of fatigue.'))
    e.append(mtbl(
        ['Deload Type','Volume Reduction','Intensity Reduction','Best For'],
        [['Volume deload','50–60%','None (same weight)','Hypertrophy athletes'],
         ['Intensity deload','Same sets/reps','20–30% weight reduction','Powerlifters peaking'],
         ['Full deload','50%','20%','Advanced athletes, high fatigue'],
         ['Active recovery week','Minimal gym work','Very light','Post-competition'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Frequency:</b> Beginners may deload every 8–12 weeks; intermediate lifters '
               'every 4–8 weeks; advanced athletes every 3–6 weeks, often based on autoregulation '
               '(perceived recovery, bar speed, mood, sleep quality) rather than fixed schedule.'))
    e.append(sp())

    e.append(sdiv('SECTION 6: Neural Adaptations — Getting Stronger Without Growing'))
    e.append(sp(6))
    e.append(h1('Strength vs Size — Two Different Outcomes'))
    e.append(p('In the first 4–8 weeks of resistance training, strength gains dramatically '
               'outpace visible muscle growth. This is because early strength adaptation is '
               'primarily neural — the nervous system learns to operate the muscles more '
               'efficiently, not because fibres have grown.'))
    e.append(p('<b>Neural adaptations include:</b>'))
    for it in ['Increased motor unit recruitment — more fibres activated per contraction',
               'Improved rate coding — motor units fire faster (more force per unit time)',
               'Enhanced motor unit synchronisation — fibres fire more simultaneously',
               'Reduced antagonist co-contraction — opposing muscles inhibit less',
               'Improved inter-muscular coordination — muscles work together more efficiently',
               'Reduced neuromuscular inhibition — Golgi tendon organ becomes less sensitive']:
        e.append(bl(it))
    e.append(p('These neural adaptations explain why beginners gain strength remarkably fast '
               '("newbie gains") without obvious hypertrophy — and why returning athletes '
               'regain strength rapidly after a layoff even before regaining muscle mass.'))
    e.append(ibox('Key Neuromuscular Concepts',[
        'Motor unit = 1 motor neuron + all muscle fibres it innervates (3–2000 fibres)',
        'Size principle: motor units recruited small→large (Henneman\'s size principle)',
        'Muscle failure occurs when firing rate drops below threshold, not when fibres "run out"',
        'Eccentric strength is always greater than concentric — exploit this in training',
        'Rate of force development (RFD) is trainable via explosive and plyometric training',
    ], RFC_GREEN))
    e.append(sp(8))

    e.append(sdiv('SECTION 7: FITT Principle and Adaptation Types'))
    e.append(sp(6))
    e.append(h1('FITT: The Framework for Programme Design'))
    e.append(p('FITT is the foundational programming framework encompassing four '
               'variables that can be manipulated to drive specific adaptations:'))
    e.append(mtbl(
        ['Variable','Definition','Example Manipulation'],
        [['Frequency','How often per week per muscle/modality','Chest: 1×/wk → 2×/wk → 3×/wk'],
         ['Intensity','How hard (% 1RM, RPE, % HRmax)','Squat: 65% 1RM → 75% → 85%'],
         ['Time (duration)','How long each session or set','30 min cardio → 45 min → 60 min'],
         ['Type','Mode of exercise','Running → Cycling → Swimming (cross-training)'],
        ]
    ))
    e.append(sp(8))

    e.append(h2('Specific Adaptation to Imposed Demand (SAID) Principle'))
    e.append(p('The body adapts specifically to the demands placed on it. Training for strength '
               'produces strength adaptation; training for endurance produces endurance adaptation. '
               'Programmes must be constructed to match the goal — a common mistake is training '
               'for aesthetics with endurance protocols, or training for performance with aesthetic '
               'bodybuilding methods.'))
    e.append(mtbl(
        ['Training Goal','Rep Range','Sets','% 1RM','Rest','Primary Adaptation'],
        [['Strength','1–5','3–6','85–100%','3–5 min','Neural, myofibrillar hypertrophy'],
         ['Power','1–5 (explosive)','3–6','30–70%','3–5 min','Neural, RFD, PCr system'],
         ['Hypertrophy','6–20','3–5','65–85%','1–3 min','Sarcoplasmic + myofibrillar hypertrophy'],
         ['Muscular endurance','>20','2–4','<65%','<1 min','Mitochondrial density, lactate tolerance'],
        ]
    ))
    e.append(sp(8))

    e.append(ibox('Module 2 Key Takeaways',[
        'Three energy systems (ATP-PCr, glycolytic, oxidative) work as a continuum — all active simultaneously, with dominance shifting based on intensity and duration',
        'VO2 max sets the ceiling of aerobic performance; lactate threshold determines how much of that ceiling you can sustain',
        'EPOC is real but modest — 50–150 kcal extra after a hard session; training consistency matters far more',
        'Progressive overload is the #1 driver of long-term adaptation — vary the method, not the principle',
        'Deload weeks prevent overreaching and enable supercompensation — they ARE part of training, not time off',
        'Neural adaptations precede hypertrophy — the first 4–8 weeks of gains are largely neurological',
        'SAID principle: train specifically for your goal — strength programmes produce strength, not endurance',
    ], RFC_DARK))
    e.append(sp(8))

    e.append(h2('Review Questions'))
    for i,q in enumerate([
        'What is ATP, and why can\'t the body simply store large amounts of it?',
        'Explain the role of hydrogen ions (not lactate) in muscular fatigue during high-intensity exercise.',
        'What is the Fick Equation, and what does each component tell us about VO2 max?',
        'Describe the 2-for-2 rule and explain why it is an effective approach to progressive overload.',
        'Distinguish between myofibrillar and sarcoplasmic hypertrophy in terms of training stimulus and physiological change.',
    ], 1):
        e.append(Paragraph(f'{i}. {q}', S['body']))

    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════
# MODULE 3: Beginner Training Program Design (40 min)
# ═══════════════════════════════════════════════════
def gen_b1_m3():
    fname = os.path.join(OUT,'cs_b1_mod3_program_design.pdf')
    doc = SimpleDocTemplate(fname, pagesize=A4,
        leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e = []
    e += cover_page('Fitness Foundations Certificate',3,'Beginner Training Program Design',40,'CS_B1')

    e.append(sdiv('SECTION 1: Why Program Design Matters'))
    e.append(sp(6))
    e.append(h1('Random Exercise vs Structured Programming'))
    e.append(p('The difference between people who consistently make progress and those who spin '
               'their wheels for years often comes down to one thing: structured programming. '
               'Random exercise produces random results. A well-designed programme provides a '
               'systematic stimulus that drives measurable, predictable adaptation over weeks, '
               'months, and years.'))
    e.append(p('A training programme is a written document specifying the exercises, sets, reps, '
               'tempo, rest periods, frequency, and progression model for a training period '
               '(typically 4–12 weeks). It removes guesswork and creates accountability.'))
    e.append(ibox('What a Good Programme Provides',[
        'Specificity — exercises match the goal (strength, hypertrophy, fat loss, sport)',
        'Progressive overload — built-in progression model prevents adaptation plateau',
        'Volume management — enough stimulus to grow; not so much to overtrain',
        'Frequency — each muscle group trained often enough for continuous protein synthesis',
        'Recovery — adequate rest between sessions and deload protocols',
        'Balance — pushing/pulling, anterior/posterior, upper/lower ratios maintained',
    ], RFC_BLUE))
    e.append(sp(8))

    e.append(sdiv('SECTION 2: Sets, Reps, and Intensity'))
    e.append(sp(6))
    e.append(h1('Decoding Training Notation'))
    e.append(p('Exercise prescriptions use shorthand notation. Understanding this allows you '
               'to read and write programmes accurately:'))
    e.append(mtbl(
        ['Notation','Meaning','Example'],
        [['3×8','3 sets of 8 reps','Barbell row: 3×8'],
         ['4×6-8','4 sets, 6 to 8 reps','Romanian deadlift: 4×6-8'],
         ['3×8 @ 75% 1RM','3 sets, 8 reps at 75% of 1-rep max','Bench press: 3×8 @ 75%1RM'],
         ['3×8 @ RPE 7','3 sets, 8 reps at Rate of Perceived Exertion 7/10','Squat: 3×8 RPE7'],
         ['3×8 @RIR 3','3 sets, 8 reps, 3 reps in reserve','Row: 3×8 RIR3'],
         ['A1/A2','Paired exercises in superset','A1:Curl, A2:Tricep ext'],
        ]
    ))
    e.append(sp(8))

    e.append(h2('RPE Scale — Autoregulation for Beginners'))
    e.append(p('The Rate of Perceived Exertion (RPE) scale (Borg\'s 6–20 or Zourdos\'s 1–10 '
               'modified scale) allows autoregulation — adjusting load based on daily readiness '
               'rather than a fixed percentage:'))
    e.append(mtbl(
        ['RPE (1–10)','Description','Reps in Reserve (RIR)'],
        [['10','Maximum effort — could not do another rep','0'],
         ['9','Could do 1 more rep','1'],
         ['8','Could do 2 more reps','2'],
         ['7','Could do 3 more reps','3'],
         ['6','Could do 4 more reps','4'],
         ['5 and below','Warm-up territory','5+'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>For beginners:</b> RPE 6–7 on working sets is appropriate. This ensures '
               'sufficient stimulus while maintaining form under fatigue. Moving to RPE 8+ '
               'should be gradual as technique becomes automatic — typically after 4–8 weeks.'))
    e.append(sp())

    e.append(sdiv('SECTION 3: Training Splits'))
    e.append(sp(6))
    e.append(h1('How to Organise Training Frequency'))
    e.append(p('A training split determines which muscle groups or movements are trained on '
               'which days. The optimal split depends on training frequency, recovery capacity, '
               'schedule, and goal.'))
    e.append(mtbl(
        ['Split','Frequency','Who It Suits','Muscle Freq/Week'],
        [['Full Body','2–4×/week','Beginners, <3 days/week','2–4×'],
         ['Upper/Lower','4×/week','Intermediate, 4 days','2×'],
         ['Push/Pull/Legs (PPL)','3–6×/week','Intermediate to advanced','1–2×'],
         ['Body Part Split','5–6×/week','Advanced bodybuilders','1×'],
         ['Hybrid (e.g. PHUL)','4×/week','Intermediate strength+hypertrophy','2×'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Research consensus:</b> Training each muscle group 2× per week produces '
               'greater hypertrophy than 1×/week with equal weekly volume. For beginners, '
               'full-body 3×/week provides 3× frequency — superior for motor learning and '
               'early neural adaptation.'))
    e.append(p('<b>Minimum Effective Dose (MED) for beginners:</b> 10–12 sets per muscle per '
               'week is sufficient for near-maximal hypertrophic response. More is not always '
               'better — recovery must match stimulus.'))
    e.append(sp())

    e.append(sdiv('SECTION 4: Compound vs Isolation Exercises'))
    e.append(sp(6))
    e.append(h1('The Hierarchy of Exercise Selection'))
    e.append(p('Exercises exist on a spectrum from multi-joint compounds to single-joint '
               'isolations. Both have a place in programming, but their priority and proportion '
               'should reflect the goal and training age of the individual.'))
    e.append(mtbl(
        ['Category','Definition','Examples','Best For'],
        [['Primary compound','Multi-joint, >2 muscle groups, heavy load','Squat, deadlift, bench press, overhead press, pull-up','Strength, power, overall mass'],
         ['Secondary compound','Multi-joint, moderate load','Lunge, incline DB press, dumbbell row, cable fly','Hypertrophy, targeted mass'],
         ['Isolation','Single joint, 1–2 muscles','Bicep curl, tricep extension, lateral raise, leg extension','Targeted development, correction, rehab'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>80/20 rule for beginners:</b> 80% of training volume from compound movements, '
               '20% from isolation work. Compounds provide maximum caloric expenditure, '
               'hormonal response, and foundational strength.'))
    e.append(p('<b>Progressive model:</b> Master compound movement pattern first (2–4 weeks), '
               'then add isolation work for lagging muscle groups once the foundation is stable.'))
    e.append(sp())

    e.append(sdiv('SECTION 5: Warm-Up and Cool-Down Science'))
    e.append(sp(6))
    e.append(h1('The Warm-Up — More Than Just Moving Around'))
    e.append(p('A proper warm-up is a structured preparation protocol that optimises '
               'performance and reduces injury risk. It is NOT 5 minutes of cardio followed '
               'by static stretching — that outdated approach may actually impair performance.'))
    e.append(h2('The RAMP Protocol'))
    e.append(mtbl(
        ['Phase','Duration','Goal','Examples'],
        [['R — Raise','5 min','Elevate heart rate, temperature, blood flow','Light cardio, jumping jacks, skipping'],
         ['A — Activate','3–5 min','Wake up key stabilisers','Glute bridges, band walks, face pulls, dead bugs'],
         ['M — Mobilise','3–5 min','Improve range of motion dynamically','Leg swings, hip circles, thoracic rotation, arm circles'],
         ['P — Potentiate','2–3 min','CNS priming, movement prep','Light sets of the planned exercise, explosive jumps'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Static stretching pre-workout:</b> Sustained stretches of >30 seconds '
               'acutely reduce force production by 5–8% by decreasing musculotendinous stiffness. '
               'Reserve static stretching for the cool-down or separate flexibility sessions.'))
    e.append(p('<b>Dynamic warm-up superiority:</b> Dynamic mobility drills maintain or enhance '
               'force production while improving ROM — making them the superior pre-training choice.'))
    e.append(h2('The Cool-Down'))
    e.append(p('The cool-down helps return the body toward homeostasis, manage blood pooling '
               '(preventing post-exercise hypotension), and begin the recovery process:'))
    for it in ['5–10 min light activity (walking, light cycling) to gradually reduce HR',
               'Static stretching for tight areas (holds 30–60 seconds, 2–3 sets)',
               'Foam rolling / myofascial release for targeted tissue quality',
               'Breathing exercises to activate parasympathetic nervous system']:
        e.append(bl(it))
    e.append(sp())

    e.append(sdiv('SECTION 6: Building a 4-Week Beginner Programme'))
    e.append(sp(6))
    e.append(h1('Sample 3-Day Full-Body Programme (Weeks 1–4)'))
    e.append(p('This programme follows a Monday / Wednesday / Friday structure. It is built '
               'around five fundamental movement patterns: squat, hip hinge, vertical push, '
               'vertical pull, and horizontal push/pull.'))
    e.append(mtbl(
        ['Day A — Monday'],
        []
    ))
    e.append(mtbl(
        ['Exercise','Sets','Reps','Rest','Notes'],
        [['Goblet Squat','3','10–12','90s','Heels elevated if needed; focus on depth'],
         ['Romanian Deadlift','3','10–12','90s','Hip hinge pattern; soft knee'],
         ['Dumbbell Bench Press','3','10–12','90s','Control the eccentric (3 sec down)'],
         ['Seated Cable Row','3','10–12','90s','Retract scapulae; avoid shrugging'],
         ['Dumbbell Overhead Press','3','10–12','90s','Neutral spine; brace core'],
         ['Plank','3','30–45s','60s','Posterior pelvic tilt; breathe normally'],
        ]
    ))
    e.append(sp(6))
    e.append(mtbl(
        ['Day B — Wednesday'],
        []
    ))
    e.append(mtbl(
        ['Exercise','Sets','Reps','Rest','Notes'],
        [['Barbell Back Squat','3','8–10','2 min','Or goblet squat if not comfortable with bar'],
         ['Trap Bar Deadlift','3','8–10','2 min','Hip hinge; drive through heels'],
         ['Incline Dumbbell Press','3','10–12','90s','30–45° incline; clavicular pec + anterior delt'],
         ['Lat Pulldown (wide grip)','3','10–12','90s','Pull to upper chest; controlled return'],
         ['Dumbbell Lateral Raise','3','15','60s','Slight forward lean; avoid shrug'],
         ['Ab Wheel Rollout / Dead Bug','3','8–10','60s','Core anti-extension pattern'],
        ]
    ))
    e.append(sp(6))
    e.append(mtbl(
        ['Day C — Friday'],
        []
    ))
    e.append(mtbl(
        ['Exercise','Sets','Reps','Rest','Notes'],
        [['Leg Press','3','12–15','90s','Feet shoulder-width; full ROM'],
         ['Nordic Hamstring Curl / Lying Leg Curl','3','10–12','90s','Slow eccentric; key for hamstring health'],
         ['Push-Up (or weighted)','3','AMRAP','60s','Full ROM; rigid plank body'],
         ['Assisted Pull-Up / Negative Pull-Up','3','8–10','90s','Work towards bodyweight pull-ups'],
         ['Face Pull','3','15–20','60s','External rotation; rear delt + rotator cuff'],
         ['Pallof Press','3','10 each side','60s','Core anti-rotation; standing or kneeling'],
        ]
    ))
    e.append(sp(8))

    e.append(h2('Progression Model — Weeks 1–4'))
    e.append(mtbl(
        ['Week','Volume','Intensity','Focus'],
        [['1','3 sets','RPE 6','Learn movement patterns — technique priority'],
         ['2','3 sets','RPE 7','Add 2.5–5kg to most exercises if form holds'],
         ['3','4 sets','RPE 7–8','Volume increase; note fatigue markers'],
         ['4 (Deload)','2 sets','RPE 5–6','Allow recovery; set stage for next block'],
        ]
    ))
    e.append(sp(8))

    e.append(ibox('Module 3 Key Takeaways',[
        'Training programmes provide structure, accountability, and a built-in progression model',
        'Sets, reps, and intensity must match the goal: strength (1–5, 85%+), hypertrophy (6–20, 65–85%), endurance (20+, <65%)',
        'Beginners benefit most from full-body 3×/week for motor learning and neural adaptation',
        'Compound exercises form the foundation; isolation work complements but doesn\'t replace them',
        'The RAMP warm-up outperforms traditional static stretching for performance and injury prevention',
        'Even a simple 3-day programme produces excellent results if applied consistently with progressive overload',
    ], RFC_DARK))
    e.append(sp(8))

    e.append(h2('Review Questions'))
    for i,q in enumerate([
        'What does RPE 8 mean, and how does autoregulation benefit beginners?',
        'Why is a full-body 3× per week split superior to a body-part split for most beginners?',
        'Explain why static stretching before training may impair performance.',
        'What is the SAID principle, and how does it apply to exercise selection?',
        'Design a progression model for a beginner who starts squatting 60kg for 3×8. What does the next 4 weeks look like?',
    ], 1):
        e.append(Paragraph(f'{i}. {q}', S['body']))

    doc.build(e)
    print(f'Generated: {fname}')

gen_b1_m2()
gen_b1_m3()
print('M2 and M3 done.')
