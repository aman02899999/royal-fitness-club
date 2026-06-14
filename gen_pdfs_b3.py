#!/usr/bin/env python3
"""Generate all 8 PDFs for cs_b3 — Body Transformation Blueprint"""
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
RFC_GREEN=colors.HexColor('#138808'); RFC_PURPLE=colors.HexColor('#6A0DAD')
RFC_WHITE=colors.white; RFC_LIGHT=colors.HexColor('#F5F5F5'); RFC_GRAY=colors.HexColor('#555555')
RFC_ORANGE=colors.HexColor('#E65C00')

S={'h1':ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=22,textColor=RFC_DARK,leading=28,spaceBefore=18,spaceAfter=10),
   'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=17,textColor=RFC_PURPLE,leading=22,spaceBefore=14,spaceAfter=7),
   'h3':ParagraphStyle('h3',fontName='Helvetica-Bold',fontSize=13,textColor=RFC_DARK,leading=18,spaceBefore=10,spaceAfter=5),
   'body':ParagraphStyle('body',fontName='Helvetica',fontSize=11,textColor=RFC_GRAY,leading=17,spaceAfter=7,alignment=TA_JUSTIFY),
   'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=11,textColor=RFC_GRAY,leading=16,spaceAfter=4,leftIndent=18,bulletIndent=6),
   'caption':ParagraphStyle('cap',fontName='Helvetica',fontSize=9,textColor=RFC_GRAY,leading=13,alignment=TA_CENTER),
   'q':ParagraphStyle('q',fontName='Helvetica',fontSize=11,textColor=RFC_DARK,leading=17,spaceAfter=6),
   'ans':ParagraphStyle('ans',fontName='Helvetica',fontSize=10,textColor=RFC_GRAY,leading=14,spaceAfter=3,leftIndent=16),
   }

def cover(mod_num,mod_title,duration):
    e=[]
    bar=Table([['']], colWidths=[W-40*mm], rowHeights=[6])
    bar.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_ORANGE),('LINEBELOW',(0,0),(-1,-1),2,RFC_GOLD)]))
    e.append(Spacer(1,8*mm));e.append(bar);e.append(Spacer(1,18*mm))
    logo=Table([['ROYAL FITNESS CLUB']],colWidths=[W-40*mm])
    logo.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_DARK),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),28),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),18),('BOTTOMPADDING',(0,0),(-1,-1),18)]))
    e.append(logo);e.append(Spacer(1,6*mm))
    e.append(HRFlowable(width='100%',thickness=3,color=RFC_GOLD));e.append(Spacer(1,10*mm))
    ct=Table([['Body Transformation Blueprint']],colWidths=[W-40*mm])
    ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_ORANGE),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),15),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    e.append(ct);e.append(Spacer(1,14*mm))
    badge=Table([[f'MODULE {mod_num}']],colWidths=[50*mm])
    badge.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),13),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    e.append(badge);e.append(Spacer(1,8*mm))
    e.append(Paragraph(mod_title,S['h1']));e.append(Spacer(1,6*mm))
    meta=Table([['Duration',f'{duration} minutes'],['Course Code','CS_B3'],['Level','Beginner'],['Format','Study Guide PDF']],
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

def sd(t,col=RFC_ORANGE):
    tb=Table([[t]],colWidths=[W-40*mm])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),col),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
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

def mt(headers,rows,hcol=RFC_ORANGE):
    n=len(headers);cw=(W-40*mm)/n;data=[headers]+rows
    t=Table(data,colWidths=[cw]*n)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),hcol),('TEXTCOLOR',(0,0),(-1,0),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),('ROWBACKGROUNDS',(0,1),(-1,-1),[RFC_LIGHT,RFC_WHITE]),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),('BOX',(0,0),(-1,-1),1,hcol)]))
    return t

def p(t): return Paragraph(t,S['body'])
def h1(t): return Paragraph(t,S['h1'])
def h2(t): return Paragraph(t,S['h2'])
def bl(t): return Paragraph(f'• {t}',S['bullet'])
def sp(n=8): return Spacer(1,n)

# ═══════════════════════════════════════
# M1: Body Composition Understanding (40min)
# ═══════════════════════════════════════
def gen_b3_m1():
    fname=os.path.join(OUT,'cs_b3_mod1_body_composition.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(1,'Body Composition: Understanding What You\'re Working With',40)

    e.append(sd('SECTION 1: Beyond Body Weight'))
    e.append(sp(6));e.append(h1('What Is Body Composition?'))
    e.append(p('Body weight is a crude, often misleading metric. Two people can weigh exactly '
               'the same — 70kg — but have vastly different physiques, health profiles, and '
               'functional capacities. Body composition describes the proportion and amount of '
               'different tissues that make up total body weight.'))
    e.append(mt(['Component','% of Body Weight (typical male)','% of Body Weight (typical female)','Key Points'],
        [['Lean mass (muscle)','40–45%','30–35%','Metabolically active; primary transformation target'],
         ['Fat mass','15–20% (healthy male)','20–25% (healthy female)','Essential fat + storage fat; excess storage drives health risk'],
         ['Bone mineral','4–5%','3–4%','Increases with resistance training; decreases with age if sedentary'],
         ['Water','55–60%','50–55%','Fluctuates daily; most body weight variation is water, not fat'],
         ['Organs, connective tissue','15–20%','15–20%','Relatively constant; not the target of body composition change'],
        ]))
    e.append(sp(8))
    e.append(h2('Essential Fat vs Storage Fat'))
    e.append(p('<b>Essential fat</b> is the minimum amount required for normal physiological '
               'function — nervous system, hormonal production, cell membrane integrity, '
               'reproductive function. Men require ~3–5% essential fat; women 10–13% (higher '
               'due to sex-specific fat in breasts, uterus, and hormonal reserves).'))
    e.append(p('<b>Storage fat</b> is energy reserve — triglycerides stored in adipose tissue. '
               'Some storage fat is protective (cushions organs). Excess storage fat is the '
               'target of body transformation — reducing it improves health markers, '
               'aesthetics, and athletic performance.'))
    e.append(p('<b>Minimum body fat thresholds:</b> Going below ~5% (men) or ~12% (women) '
               'disrupts hormonal function (loss of menstruation in women — "the female '
               'athlete triad"; testosterone suppression in men), impairs immune function, '
               'and reduces bone density. Extreme leanness is NOT health.'))
    e.append(sp())

    e.append(sd('SECTION 2: How to Measure Body Composition'))
    e.append(sp(6));e.append(h1('Body Composition Assessment Methods'))
    e.append(mt(['Method','Accuracy','Cost','Practical Use','Limitation'],
        [['DEXA scan','±1–2%','Moderate-high','Gold standard for clinical assessment','Radiation exposure; limited access'],
         ['BodPod (air displacement)','±1–3%','Moderate','Good laboratory method','Lab access needed; expensive'],
         ['Hydrostatic weighing','±1–3%','Moderate','Research setting gold standard','Inconvenient; requires full submersion'],
         ['3/4-site skinfold calipers','±3–4% (skilled)','Low','Practical; reproducible with experience','Requires skilled practitioner; multiple sites'],
         ['Bioelectrical impedance (BIA)','±3–5%','Low (home scales)','Convenient; consistent time of day','Hydration-sensitive; wide error margin'],
         ['Progress photos + measurements','Qualitative','Free','Most actionable for transformation tracking','No precise body fat %'],
         ['BMI (Body Mass Index)','Very inaccurate','Free','Population screening only','Ignores muscle mass; meaningless for athletes'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Practical recommendation:</b> Use DEXA scan at start and every 12–16 weeks '
               'for accurate body composition. Between scans, use monthly measurements '
               '(tape measure) + weekly photos + 7-day average body weight to track '
               'trend. BMI is irrelevant for anyone training.'))

    e.append(sd('SECTION 3: Healthy Body Fat Ranges'))
    e.append(sp(6));e.append(h1('What Percentage of Body Fat Should You Target?'))
    e.append(mt(['Category','Males (BF%)','Females (BF%)','Description'],
        [['Essential fat','3–5%','10–13%','Minimum for organ and hormone function'],
         ['Athletic','6–13%','14–20%','Competitive athletes; high training demands'],
         ['Fitness','14–17%','21–24%','Excellent health; visible muscle definition'],
         ['Acceptable','18–24%','25–31%','Good health; normal risk profile'],
         ['Obese','>25%','>32%','Elevated risk for metabolic disease, CVD, T2D'],
        ]))
    e.append(sp(8))
    e.append(p('<b>The "fitness" range (14–17% male, 21–24% female) is the ideal target</b> '
               'for most recreational fitness enthusiasts — achievable with consistent training '
               'and nutrition, sustainable long-term, and associated with excellent metabolic '
               'health without the performance costs of extreme leanness.'))
    e.append(p('<b>Waist circumference</b> is a simple, powerful proxy for visceral fat '
               '(the metabolically dangerous fat around organs): men <94cm (low risk), '
               '94–102cm (moderate), >102cm (high); women <80cm (low), 80–88cm (moderate), '
               '>88cm (high risk).'))

    e.append(sd('SECTION 4: Body Composition vs Body Weight'))
    e.append(sp(6));e.append(h1('Body Recomposition — The Holy Grail'))
    e.append(p('Body recomposition — simultaneously gaining muscle and losing fat — is '
               'the ultimate transformation goal. For many years, conventional wisdom held '
               'that you had to choose: either bulk (gain muscle + fat) or cut (lose fat + '
               'some muscle). Modern research challenges this dichotomy.'))
    e.append(p('<b>Recomposition is most achievable for:</b>'))
    for it in ['Beginners (first 1–2 years of consistent training) — "newbie recomp" is well-documented',
               'Individuals returning to training after a long layoff (muscle memory facilitates rapid regain)',
               'Overweight/obese individuals (large fat stores provide endogenous caloric substrate for muscle synthesis)',
               'Individuals with high training volume and high protein intake at maintenance calories']:
        e.append(bl(it))
    e.append(p('<b>Mechanism:</b> Caloric deficit drives fat oxidation; resistance training + '
               'high protein stimulates muscle protein synthesis using the liberated fatty acids '
               'as energy substrate. The body preferentially rebuilds muscle at the expense of '
               'fat stores — particularly in beginners where mTORC1 sensitivity is high.'))
    e.append(ib('Module 1 (CS_B3) Key Takeaways',[
        'Body weight is a poor proxy for transformation success; body composition (muscle vs fat) is what matters',
        'Essential fat is the physiological minimum: 3–5% (men), 10–13% (women); never go below this',
        'DEXA scan is the most accurate practical method; combine with photos and tape measurements',
        'Target body fat for most recreational athletes: 14–17% (men), 21–24% (women) — "fitness" range',
        'Waist circumference >102cm (men) />88cm (women) indicates high visceral fat and metabolic risk',
        'Body recomposition (simultaneous muscle gain + fat loss) is most achievable for beginners and returning athletes',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['What is the difference between essential fat and storage fat? What are the minimum safe levels?',
        'Compare DEXA scan vs BIA scales for body composition measurement.',
        'Why is BMI a flawed metric for trained individuals? Provide a specific example.',
        'Explain body recomposition and which populations are most likely to achieve it.',
        'A client loses 5kg over 12 weeks but looks worse (less definition). Explain what likely happened.',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════
# M2: Fat Loss Science & Hormones (60min)
# ═══════════════════════════════════════
def gen_b3_m2():
    fname=os.path.join(OUT,'cs_b3_mod2_fat_loss_hormones.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(2,'Fat Loss Science & Hormones',60)

    e.append(sd('SECTION 1: The Physiology of Fat Loss'))
    e.append(sp(6));e.append(h1('How the Body Actually Burns Fat'))
    e.append(p('Fat loss requires adipose tissue to release stored triglycerides into the '
               'bloodstream for use as fuel. This process — lipolysis — is regulated by '
               'hormones and depends fundamentally on a negative energy balance (caloric deficit).'))
    e.append(p('Lipolysis proceeds in three steps:'))
    for it in ['Hormone-sensitive lipase (HSL) cleaves triglycerides → 3 fatty acids + glycerol',
               'Fatty acids enter the bloodstream bound to albumin → transported to tissues',
               'In mitochondria, beta-oxidation converts fatty acids → Acetyl-CoA → ATP via Krebs/ETC']:
        e.append(bl(it))
    e.append(p('<b>Critical concept:</b> Dietary fat restriction alone does not cause body fat '
               'loss. Fat is oxidised only when total caloric expenditure exceeds intake. '
               'The body is energy-balance governed — the specific macronutrient composition '
               'is secondary to total caloric deficit.'))
    e.append(p('<b>"Fat burning zone" myth:</b> Low-intensity exercise does burn a higher '
               '<i>percentage</i> of calories from fat. But higher-intensity exercise burns '
               'more total calories, including more absolute fat calories. A 60-min walk '
               'burns ~250 kcal (65% fat = 163 kcal fat). A 30-min run burns ~350 kcal '
               '(35% fat = 122 kcal fat). Walking burns slightly more fat calories per session '
               'but the run burns more total calories and produces far greater EPOC.'))

    e.append(sd('SECTION 2: The Hormonal Landscape of Fat Loss'))
    e.append(sp(6));e.append(h1('Six Hormones That Make or Break Your Transformation'))

    e.append(h2('1. Insulin — The Gatekeeper'))
    e.append(p('Insulin is produced by pancreatic beta cells in response to rising blood glucose. '
               'It is a powerful anabolic and anti-lipolytic hormone:'))
    for it in ['High insulin: promotes glucose uptake, glycogen synthesis, protein synthesis, fat storage; INHIBITS lipolysis',
               'Low insulin (fasting, low-carb diet): enables lipolysis; releases fatty acids from adipose tissue',
               'Chronic hyperinsulinaemia (from excess refined carbs/calories): develops insulin resistance, impairing glucose disposal']:
        e.append(bl(it))
    e.append(p('<b>Practical implication:</b> Carbohydrates are not the enemy, but refined, '
               'high-GI carbs consumed in excess keep insulin chronically elevated, suppressing '
               'lipolysis between meals. Replacing refined carbs with low-GI options and '
               'adequate protein reduces fasting insulin and facilitates fat oxidation.'))

    e.append(h2('2. Glucagon — The Mobiliser'))
    e.append(p('Glucagon is secreted by pancreatic alpha cells when blood glucose falls. '
               'It opposes insulin: promotes glycogenolysis (liver glycogen → glucose), '
               'gluconeogenesis (protein/fat → glucose), and lipolysis. The insulin:glucagon '
               'ratio determines net metabolic state. In a caloric deficit + exercise, '
               'this ratio falls, favouring fat mobilisation.'))

    e.append(h2('3. Cortisol — The Double-Edged Sword'))
    e.append(p('Cortisol (the primary glucocorticoid) is released by the adrenal cortex in '
               'response to physical/psychological stress. It has context-dependent effects:'))
    e.append(mt(['Context','Cortisol Effect','Outcome'],
        [['Acute (during exercise)','Promotes lipolysis; mobilises energy; anti-inflammatory','Beneficial — drives fat mobilisation during training'],
         ['Acute (post-exercise)','Drops back to baseline with adequate recovery','Anabolic window opens'],
         ['Chronic elevation (stress, poor sleep, overtraining)','Promotes visceral fat deposition; breaks down muscle protein; suppresses testosterone','Detrimental — gains muscle AND fat simultaneously; impairs recovery'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Visceral fat and cortisol:</b> Visceral adipocytes (belly fat cells) have '
               '4× more cortisol receptors than subcutaneous fat cells. Chronic stress '
               'selectively promotes visceral fat accumulation — explaining the classic '
               '"stressed belly" seen in high-cortisol individuals regardless of diet.'))

    e.append(h2('4. Leptin — The Starvation Signal'))
    e.append(p('Leptin is secreted by adipose tissue in proportion to fat stores. It signals '
               'to the hypothalamus that energy reserves are adequate, suppressing hunger and '
               'increasing metabolic rate. As fat mass decreases during dieting, leptin falls:'))
    for it in ['Reduced leptin → hypothalamus increases hunger (ghrelin rises)',
               'Reduced leptin → metabolic rate falls (NEAT decreases unconsciously)',
               'Reduced leptin → reproductive axis suppressed (in severe deficit — explains amenorrhoea in female athletes)',
               'Reduced leptin → thyroid hormone conversion impaired (T4 → T3 reduces)']:
        e.append(bl(it))
    e.append(p('<b>Leptin resistance:</b> In obesity, leptin levels are chronically elevated '
               'but the hypothalamus becomes desensitised — analogous to insulin resistance. '
               'The brain no longer receives the "I\'m full" signal correctly, driving '
               'continued hunger despite large fat stores.'))

    e.append(h2('5. Ghrelin — The Hunger Hormone'))
    e.append(p('Ghrelin is secreted by the stomach, primarily before meals, signalling hunger '
               'to the hypothalamus. It rises in a caloric deficit (within days of dieting) '
               'and remains elevated — a key driver of diet fatigue and rebound eating. '
               'Strategies to manage ghrelin:'))
    for it in ['High protein meals: strongest satiety macronutrient — blunts ghrelin rise most effectively',
               'High volume foods: vegetables, soups, salads create gastric stretch that suppresses ghrelin',
               'Sleep: sleep deprivation increases ghrelin by 15–20% (a key reason poor sleep causes overeating)',
               'Regular meal timing: established eating windows reduce anticipatory ghrelin spikes']:
        e.append(bl(it))

    e.append(h2('6. Thyroid Hormones (T3, T4) — The Metabolic Rate Regulator'))
    e.append(p('Thyroid hormones (primarily triiodothyronine, T3) regulate the basal metabolic '
               'rate by modulating mitochondrial activity in virtually every cell. In prolonged '
               'caloric restriction:'))
    for it in ['T4 → T3 conversion decreases (caloric deficit reduces deiodinase enzyme activity)',
               'Reverse T3 (rT3) increases — an inactive T3 form that blocks T3 receptors',
               'Net effect: metabolic rate falls 10–20% in prolonged severe deficit',
               'Reverse: eating at maintenance for 2 weeks restores T3 and metabolic rate']:
        e.append(bl(it))

    e.append(sd('SECTION 3: Spot Reduction and Regional Fat Distribution'))
    e.append(sp(6));e.append(h1('The Truth About Spot Reduction'))
    e.append(p('<b>Spot reduction is a myth.</b> Doing 1000 crunches per day will not preferentially '
               'reduce abdominal fat. Fat is mobilised systemically from fat stores based on '
               'genetics and hormonal gradients — not from adjacent muscle activity.'))
    e.append(p('Regional fat distribution is primarily determined by:'))
    e.append(mt(['Determinant','Influence','Implication'],
        [['Genetics (FTO, MC4R genes)','40–70% of body fat distribution is heritable','Cannot be overridden; work within your genotype'],
         ['Sex hormones','Oestrogen: gluteofemoral fat (hips, thighs); Testosterone: spares visceral fat (until low T)','Explains sex differences in fat distribution'],
         ['Cortisol','Promotes visceral (abdominal) fat deposition via visceral adipocyte cortisol receptors','Stress management directly reduces belly fat accumulation'],
         ['Insulin resistance','Drives ectopic fat (liver, muscle) + visceral fat accumulation','Exercise + weight loss improves insulin sensitivity → preferentially reduces visceral fat'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Good news:</b> Visceral fat (the dangerous kind around organs) is the first '
               'fat lost with caloric restriction and exercise — before subcutaneous fat '
               'responds. Internal health improvements occur before visible aesthetic changes, '
               'which is why early body composition improvement shows up in blood markers before '
               'the mirror.'))

    e.append(sd('SECTION 4: Optimal Fat Loss Rate'))
    e.append(sp(6));e.append(h1('How Fast Should You Lose Fat?'))
    e.append(mt(['Rate','Kcal Deficit','Pros','Cons'],
        [['0.5% BW/week (gradual)','250–350 kcal/day','Preserves maximum muscle; sustainable; minimal metabolic adaptation','Very slow progress; less motivating'],
         ['1% BW/week (moderate)','500–700 kcal/day','Good balance of speed and muscle preservation; recommended for most','Some metabolic adaptation; some hunger'],
         ['1.5% BW/week (aggressive)','700–1000 kcal/day','Faster results; useful when overweight/obese','Significant muscle loss without high protein + resistance training; high hunger'],
         ['2%+ BW/week (extreme)','1000+ kcal/day','Rapid short-term results','High muscle loss; metabolic suppression; unsustainable; NOT recommended'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Research consensus:</b> 0.5–1% body weight per week is the evidence-based '
               'target for athletes and fitness enthusiasts who want to preserve muscle. '
               'For overweight individuals, up to 1.5% per week is acceptable with '
               'adequate protein (2.0–2.4g/kg) and resistance training.'))
    e.append(ib('Module 2 (CS_B3) Key Takeaways',[
        'Lipolysis requires HSL activation via catecholamines + low insulin; only possible in caloric deficit',
        'Cortisol: beneficial acutely during training (mobilises fat); detrimental chronically (visceral fat deposition)',
        'Leptin falls with fat loss → hunger rises, metabolic rate drops → diet breaks restore leptin',
        'Ghrelin rises within days of dieting; high protein, high volume foods, and adequate sleep are the best mitigations',
        'Thyroid T3 reduces with prolonged restriction → metabolic adaptation; 2-week diet breaks restore T3',
        'Spot reduction is a myth; visceral fat is preferentially lost first with deficit and exercise',
        'Optimal fat loss rate: 0.5–1% body weight per week to preserve lean mass',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Explain why chronic stress (cortisol) specifically promotes visceral fat accumulation.',
        'What is leptin resistance and how does it contribute to the difficulty of weight loss in obesity?',
        'Debunk the "fat burning zone" myth with specific calorie calculations.',
        'How does sleep deprivation increase ghrelin and impair fat loss?',
        'Why does T3 decrease during a prolonged caloric deficit, and what is the practical intervention?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════
# M3: Muscle Building for Beginners (55min)
# ═══════════════════════════════════════
def gen_b3_m3():
    fname=os.path.join(OUT,'cs_b3_mod3_muscle_building.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(3,'Muscle Building for Beginners',55)

    e.append(sd('SECTION 1: The Foundations of Hypertrophy'))
    e.append(sp(6));e.append(h1('What Makes a Muscle Actually Grow?'))
    e.append(p('Skeletal muscle hypertrophy (growth in size) occurs when muscle protein synthesis '
               '(MPS) consistently exceeds muscle protein breakdown (MPB) over days, weeks, '
               'and months. This net positive protein balance results in larger muscle fibres '
               'with more contractile proteins (actin and myosin) and, ultimately, a larger '
               'muscle belly.'))
    e.append(p('Three primary mechanical and metabolic stimuli drive hypertrophy, and '
               'understanding their relative contribution guides optimal programme design:'))
    e.append(mt(['Mechanism','Contribution','Training Application','Evidence Strength'],
        [['Mechanical tension (primary driver)','~60–70% of hypertrophic signal','Heavy compound lifts (>60% 1RM), full ROM, controlled eccentrics, stretched position loading','Very strong — Schoenfeld et al., meta-analyses'],
         ['Metabolic stress (pump)','~20–25%','High-rep sets (15–30 reps), short rest (<90s), blood flow restriction, supersets, dropsets','Moderate — mechanism debated but effect real'],
         ['Muscle damage','~10–15%','Novel exercises, slow eccentrics (4–5s), stretched position under load (RDL, deep squat, flyes)','Moderate — may initiate satellite cell activation'],
        ]))
    e.append(sp(8))
    e.append(h2('Myofibrillar vs Sarcoplasmic Hypertrophy'))
    e.append(mt(['Type','What Grows','Training Stimulus','Outcome','Look'],
        [['Myofibrillar','Actin and myosin protein content — the contractile machinery','Heavy loads (>75% 1RM); lower reps (3–8)','Denser, stronger muscle — "hard" look','Strength athlete physique'],
         ['Sarcoplasmic','Glycogen, water, organelles in the muscle cell — the "fuel tank"','Moderate loads, higher reps (8–20), pump work','Larger cell diameter without proportional strength gain','Bodybuilder "full" look'],
        ]))
    e.append(sp(8))
    e.append(p('Both types of hypertrophy occur with resistance training. The relative '
               'proportion depends on rep range and loading scheme. Most evidence suggests '
               'a spectrum of 6–20 reps produces optimal total hypertrophy when combined '
               'with adequate volume and progressive overload.'))

    e.append(sd('SECTION 2: Volume — The Most Important Training Variable for Hypertrophy'))
    e.append(sp(6));e.append(h1('How Many Sets Do You Need?'))
    e.append(p('Training volume — typically expressed as weekly sets per muscle group — is the '
               'strongest predictor of hypertrophy in research and practice. More volume '
               'produces more hypertrophy up to a recovery-limited ceiling ("maximum adaptive '
               'volume"), beyond which additional sets become junk volume.'))
    e.append(mt(['Volume Category','Sets/Muscle/Week','Who It\'s For','Note'],
        [['Minimum Effective Volume (MEV)','10–12 sets','Beginners; maintenance','Sufficient for near-maximal beginner response'],
         ['Moderate Volume','12–18 sets','Intermediate; most recreationally training','Good balance of stimulus and recovery'],
         ['High Volume','18–25 sets','Advanced; well-recovered; periodised','Requires programmed deloads; high-protein diet'],
         ['Maximum Adaptive Volume (MAV)','25–35 sets','Specialisation phases only; very advanced','Beyond this = recovery deficit'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Progressive volume:</b> Start at MEV (10–12 sets/week/muscle) and add 2 sets '
               'per muscle per week across a 4–6 week mesocycle, then deload and restart '
               'slightly above previous MEV. This is "volume progression" — a key element '
               'of long-term hypertrophy planning.'))
    e.append(p('<b>Hard sets only:</b> Volume only counts as "hard" sets — taken to within '
               '3 reps of failure (RPE 7+). Warm-up sets, feeder sets at RPE 5 do not '
               'contribute meaningfully to the hypertrophic stimulus. Quality over quantity.'))

    e.append(sd('SECTION 3: Exercise Selection for Maximum Hypertrophy'))
    e.append(sp(6));e.append(h1('The Best Exercises for Each Muscle Group'))
    e.append(mt(['Muscle Group','Primary Exercise','Secondary','Isolation','Notes'],
        [['Chest','Barbell bench press, incline DB press','Dip, cable crossover','Pec deck, cable flye','Incline hits clavicular head better; stretch-focused at bottom'],
         ['Back (width)','Pull-up, lat pulldown','Cable pullover','Straight-arm pulldown','Full shoulder extension → full lat activation'],
         ['Back (thickness)','Barbell row, cable row','DB row, machine row','Face pull (rear delt/mid-trap)','Elbow close to body = lat; elbow out = rhomboid/trap'],
         ['Shoulders','Barbell OHP, DB press','Arnold press','Lateral raise (15–30 reps)','Lateral raise best at 30° scaption; avoid shrugging'],
         ['Biceps','Incline DB curl (stretched)','Barbell curl, preacher curl','Concentration curl, cable curl','Stretch position (incline, cable from high) superior for hypertrophy'],
         ['Triceps','Close-grip bench, dip','Skull crusher','Pushdown (pronated), overhead cable ext.','Long head (bulk of tricep) best hit with arm overhead'],
         ['Quadriceps','Back squat, leg press','Front squat, hack squat','Leg extension (for terminal knee ext.)','Knee over toe = more quad; hip hinge = more glute'],
         ['Hamstrings','Romanian deadlift, Nordic curl','Leg curl, good morning','Seated leg curl','Stretched position (at hip AND knee) = most damage + growth'],
         ['Glutes','Hip thrust, Bulgarian split squat','Squat, deadlift','Kickback, abduction','Hip thrust activates glute max 30%+ more than squat'],
         ['Calves','Standing calf raise','Donkey calf raise','Seated calf raise (soleus)','Full ROM: heel below level of step; hold stretch at bottom'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 4: Anabolic Hormones and Muscle Growth'))
    e.append(sp(6));e.append(h1('The Hormonal Environment for Muscle Building'))
    e.append(mt(['Hormone','Role in Hypertrophy','How Training Affects It','Optimise By'],
        [['Testosterone','Androgen receptor binding → increased gene transcription for MPS; IGF-1 production','Heavy compound lifts (>75% 1RM) produce acute testosterone spike; long-term baseline increases with training','Heavy compound training; adequate dietary fat (>15%); sleep 8h; stress management'],
         ['Growth Hormone (GH)','IGF-1 production (liver); fat mobilisation; collagen synthesis','Exercise (especially heavy + metabolic) → GH pulse; biggest pulse during N3 sleep','Deep sleep; training intensity; avoid alcohol pre-sleep'],
         ['IGF-1 (Insulin-like Growth Factor 1)','Satellite cell activation; protein synthesis via PI3K/Akt/mTOR pathway','Exercise and high protein diet increase liver IGF-1 production','High protein diet; resistance training; adequate calories'],
         ['Insulin','GLUT4 → amino acid uptake; synergistic with mTOR for MPS','Post-workout carb+protein spike → insulin elevation drives amino acid into muscle','Post-workout protein + carbohydrate; adequate carb intake during muscle-building phase'],
        ]))
    e.append(sp(8))
    e.append(p('<b>The "hormone spike" myth:</b> Acute post-exercise testosterone and GH spikes '
               'from training are real but do NOT directly cause hypertrophy. The local '
               'mechanical stimulus (mTORC1 in the trained muscle) is the primary driver. '
               'Hormone spikes are correlated with, not causal of, hypertrophy — explaining '
               'why upper body exercises cause systemic testosterone spikes but don\'t '
               'produce upper body growth proportional to the spike.'))
    e.append(ib('Module 3 (CS_B3) Key Takeaways',[
        'Hypertrophy requires MPS > MPB consistently; mechanical tension is the primary stimulus (~60–70%)',
        'Volume (sets/week/muscle) is the most important training variable for hypertrophy; start at 10–12 hard sets',
        'Progress volume over each mesocycle (+2 sets/week), then deload; begin next cycle above previous MEV',
        'Stretch-position loading (incline curls, RDL, full ROM squats) produces greatest muscle damage and growth signal',
        'Hip thrust produces 30%+ greater glute max activation than squat — include both for complete development',
        'Anabolic hormones (testosterone, GH, IGF-1) create a permissive environment but local mTORC1 is the primary driver',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Explain the three mechanisms of hypertrophy and their relative contribution.',
        'What is the difference between MEV (minimum effective volume) and MAV (maximum adaptive volume)?',
        'Why does the incline dumbbell curl produce more hypertrophy than a standard standing barbell curl?',
        'Describe volume progression across a 6-week mesocycle starting at 12 sets for biceps.',
        'What is the "hormone spike" myth and why doesn\'t the acute testosterone response from squats build upper body muscle?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════
# M4: Cardio for Body Composition (45min)
# ═══════════════════════════════════════
def gen_b3_m4():
    fname=os.path.join(OUT,'cs_b3_mod4_cardio_composition.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(4,'Cardio for Body Composition',45)

    e.append(sd('SECTION 1: The Role of Cardio in Body Transformation'))
    e.append(sp(6));e.append(h1('Cardio: Tool, Not Treatment'))
    e.append(p('Cardiovascular exercise is a tool — one of many in the body transformation '
               'toolkit. When used strategically, it accelerates fat loss, improves '
               'cardiovascular health, and supports recovery. When used excessively or '
               'inappropriately, it interferes with resistance training adaptations, '
               'increases recovery demands, and can drive muscle loss.'))
    e.append(p('The key question is not "should I do cardio?" but "how much cardio, '
               'what type, and when — to maximise fat loss while preserving muscle?"'))
    e.append(mt(['Cardio Type','Duration','Intensity','Calorie Burn','Muscle Interference','Best For'],
        [['LISS (Low-Intensity Steady State)','30–60 min','50–65% HRmax','200–400 kcal/hr','Minimal','Fat loss; recovery; joint health; beginners'],
         ['MISS (Moderate)','20–40 min','65–75% HRmax','350–500 kcal/hr','Low','General conditioning; fat loss'],
         ['HIIT (High-Intensity Interval)','15–25 min work time','85–95% HRmax (efforts)','300–600 kcal/hr (+ EPOC)','Moderate','Fat loss; VO2 max; time efficiency'],
         ['Sprints (Anaerobic)','10–20 min','>95% HRmax (efforts)','200–400 kcal (very short duration)','Moderate-high if excessive','Power; sprint fitness; body composition'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 2: HIIT vs LISS — Evidence Review'))
    e.append(sp(6));e.append(h1('What Actually Works Better for Fat Loss?'))
    e.append(p('The HIIT vs LISS debate has generated hundreds of studies. The evidence shows:'))
    e.append(mt(['Factor','HIIT Advantage','LISS Advantage'],
        [['Time efficiency','Equal fat loss in 25 min vs 60 min steady state','More total calorie burn per session if equal time available'],
         ['EPOC','Significantly higher EPOC (12–24+ hours)','Minimal EPOC'],
         ['Cardiovascular adaptation','Greater VO2 max gains','Mitochondrial density at low intensity'],
         ['Muscle interference','Can interfere with strength/hypertrophy if excessive','Minimal interference even at high frequency'],
         ['Recovery demand','High — needs 48h recovery; CNS taxing','Low — can do daily without meaningful fatigue accumulation'],
         ['Adherence','Lower (intensity makes it less enjoyable)','Higher (sustainable, pleasant, social)'],
         ['Injury risk','Moderate-high (especially running-based)','Low'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Evidence-based recommendation:</b> Use primarily LISS (walking, cycling, '
               'swimming) for the bulk of cardio volume (3–5 sessions/week), adding 1–2 '
               'HIIT sessions/week for cardiovascular fitness and time efficiency. This '
               'preserves recovery capacity for resistance training while maximising '
               'fat-loss-supporting calorie expenditure.'))

    e.append(sd('SECTION 3: Concurrent Training — The Interference Effect'))
    e.append(sp(6));e.append(h1('Can You Do Strength and Cardio Together?'))
    e.append(p('The "interference effect" describes the well-documented phenomenon where '
               'concurrent endurance and resistance training produces inferior strength and '
               'hypertrophy gains compared to resistance training alone, and inferior '
               'endurance adaptations compared to endurance training alone.'))
    e.append(p('<b>Molecular mechanism:</b> AMPK (activated by endurance training) '
               'inhibits mTORC1 (activated by resistance training). These two signalling '
               'pathways are essentially antagonistic — chronic concurrent training creates '
               'a chronic state of partial inhibition of both.'))
    e.append(p('<b>Mitigating the interference effect:</b>'))
    for it in ['Separate resistance and cardio sessions by at least 6 hours (ideally 24 hours)',
               'Perform resistance training first in any combined session; never cardio first',
               'Favour low-impact cardio (cycling, swimming) over running to reduce CNS and leg fatigue',
               'Limit HIIT to 2×/week maximum when hypertrophy is the primary goal',
               'Adequate caloric and protein intake is even more critical when doing concurrent training']:
        e.append(bl(it))
    e.append(mt(['Scenario','Interference Level','Strategy'],
        [['Cardio before weights (same session)','HIGH','Always lift first; cardio depletes glycogen and creates pre-fatigue'],
         ['Cardio immediately after weights','MODERATE','Acceptable; replenish carbs/protein first'],
         ['Cardio 6h+ separate from weights','LOW','Good separation; AMPK/mTOR conflict minimised'],
         ['Cardio on rest days from weights','VERY LOW','Ideal — no acute interference with lifting sessions'],
         ['LISS cardio (walking) any time','MINIMAL','Walking AMPK stimulus is weak; virtually no interference'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 4: Cardio Prescription for Transformation Phases'))
    e.append(sp(6));e.append(h1('Periodising Cardio Around Your Training Goal'))
    e.append(mt(['Phase','Goal','Resistance Training','Cardio Volume','Cardio Type'],
        [['Muscle building (bulk)','Maximise hypertrophy','4–5 sessions/week, high volume','2–3 sessions/week, 20–30 min each','LISS; low intensity; joint-decompressing (cycling)'],
         ['Fat loss (cut)','Maximise fat loss + muscle preservation','3–4 sessions/week (lower volume to aid recovery)','4–6 sessions/week, 30–60 min each','Majority LISS; 1–2 HIIT for VO2 maintenance'],
         ['Maintenance/recomp','Maintain muscle, slow fat reduction','3–4 sessions/week','3–4 sessions/week, 30–45 min','Mix LISS and HIIT; prioritise enjoyment for adherence'],
         ['Athletic performance','Sport-specific conditioning','2–3 sessions/week','Sport practice + 1–2 conditioning sessions','Sport-specific; energy system matched to sport demands'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 4 (CS_B3) Key Takeaways',[
        'Cardio is a tool to increase caloric expenditure; it does not selectively burn fat in isolation from caloric deficit',
        'LISS (walking, cycling) has minimal muscle interference and can be done 5–6×/week; HIIT: maximum 2×/week during hypertrophy phases',
        'The interference effect (AMPK vs mTOR conflict) is minimised by separating cardio from resistance training by 6+ hours',
        'Always lift weights before cardio in any combined session — never the reverse',
        'During a cut: increase cardio volume before decreasing calories — preserves energy for training and micronutrient adequacy',
        'Walking (LISS) is underrated: 10,000 steps/day burns 300–500 extra kcal with virtually zero recovery cost',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Explain the AMPK-mTOR conflict (interference effect) at a molecular level.',
        'Compare calorie burn of HIIT vs LISS including EPOC.',
        'A client wants to do cardio immediately before their weight training session. What do you recommend and why?',
        'How should cardio volume change when transitioning from a muscle-building phase to a fat loss phase?',
        'Why is cycling a better cardio choice than running during a hypertrophy phase?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════
# M5: Tracking, Measuring & Adjusting (40min)
# ═══════════════════════════════════════
def gen_b3_m5():
    fname=os.path.join(OUT,'cs_b3_mod5_tracking_adjusting.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(5,'Tracking, Measuring & Adjusting Your Plan',40)

    e.append(sd('SECTION 1: The Science of Feedback Loops'))
    e.append(sp(6));e.append(h1('Why Measurement Is Non-Negotiable'))
    e.append(p('A body transformation programme without systematic tracking is like driving '
               'cross-country without a GPS — you might eventually get there, but you\'ll '
               'waste significant time taking wrong turns. Measurement provides the feedback '
               'loop that separates effective, adaptive programming from hopeful guesswork.'))
    e.append(p('Tracking serves three functions:'))
    for it in ['Accountability: the act of recording food/training increases adherence by 30–40% in meta-analyses',
               'Diagnosis: identifies WHY progress has stalled (calories drifted, protein insufficient, training load dropped)',
               'Adjustment: data-driven changes to diet or training are more targeted and effective than subjective guesses']:
        e.append(bl(it))
    e.append(h2('The Minimum Effective Tracking Stack'))
    e.append(mt(['Metric','Tool','Frequency','Time to Track'],
        [['Body weight','Digital scale (0.1kg accuracy)','Daily (morning, after toilet, fasted)','30 seconds'],
         ['7-day average weight','Spreadsheet or Cronometer/MyFitnessPal','Weekly','5 minutes'],
         ['Training performance','Training log (notebook or app)','Every session','5 minutes'],
         ['Progress photos','Phone camera (same conditions)','Monthly','10 minutes'],
         ['Tape measurements','Tape measure (waist, hips, chest, arms, thighs)','Monthly','10 minutes'],
         ['Nutrition (initial 4–8 weeks)','MyFitnessPal, Cronometer','Daily initially','10–15 minutes'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 2: Interpreting Scale Weight'))
    e.append(sp(6));e.append(h1('Why the Scale Lies (Daily) but Tells the Truth (Weekly)'))
    e.append(p('Body weight fluctuates 1–3kg daily due to factors unrelated to fat gain or '
               'loss. Understanding these fluctuations prevents panic-driven decision changes:'))
    e.append(mt(['Factor','Weight Increase','Scale Reading Duration','Misinterpretation Risk'],
        [['High-sodium meal','Increased water retention (1g Na retains 3g water)','1–2 days','Appears as fat gain — it\'s water'],
         ['High-carb meal','Glycogen storage (1g glycogen stores 3g water)','2–3 days','Training day "gain" — it\'s glycogen + water'],
         ['Menstrual cycle (female)','0.5–3kg fluid retention in luteal phase','7–14 days premenstrual','Weight gain is hormonal water, not fat'],
         ['GI contents','Food in transit through digestive system','Same day','Morning vs evening weight varies 1–2kg by contents'],
         ['Hydration status','1L water = 1kg','Hours','Dehydrated = lighter; does not reflect body fat'],
        ]))
    e.append(sp(8))
    e.append(p('<b>The 7-day average method:</b> Add daily weights from Monday–Sunday, divide '
               'by 7. Compare THIS week\'s average to LAST week\'s average. Movement of the '
               '7-day average by 0.5–1kg over 2+ weeks signals real change. One-day swings '
               'are noise.'))
    e.append(p('<b>Decision rule:</b> Only adjust diet or training if the 7-day average '
               'moves in the wrong direction for 2+ consecutive weeks. Single-week stalls '
               'are normal fluctuation.'))

    e.append(sd('SECTION 3: Making Data-Driven Adjustments'))
    e.append(sp(6));e.append(h1('When and How to Adjust Your Programme'))
    e.append(mt(['Scenario','Diagnosis','Adjustment'],
        [['Weight average not moving down for 2+ weeks (fat loss goal)','Caloric intake crept up, NEAT reduced, or metabolic adaptation','Reduce calories 100–200 kcal/day; or increase NEAT (add 2000 steps/day)'],
         ['Weight average dropping >1.5% BW/week (loss too fast)','Deficit too aggressive; muscle loss risk high','Add 200–300 kcal from protein + carbs; ensure 2.0g protein/kg'],
         ['Strength declining despite training (fat loss phase)','Under-fuelled; low glycogen; sleep deprived','Refeed day (extra 200–300g carbs); check sleep; reduce HIIT frequency'],
         ['No strength progression for 3+ weeks (muscle building phase)','Insufficient volume, calories, or protein; technique plateau','Add 1 set per muscle/session; check macros; consider 3-day deload'],
         ['Weight gaining too fast (>0.5% BW/week in bulk)','Surplus too large; excess fat gain','Reduce surplus by 200 kcal; check weekend dietary drift'],
         ['Progress photos not changing despite scale movement','Weight loss is water/muscle not fat (no resistance training)','Add resistance training; increase protein to 2.0–2.2g/kg'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 4: Long-Term Progress Tracking'))
    e.append(sp(6));e.append(h1('The 12-Week Review Framework'))
    e.append(p('Every 12–16 weeks, conduct a comprehensive transformation review:'))
    for it in ['Compare DEXA or skinfold measurements to baseline — quantify lean mass change',
               'Review training log for strength progress on key lifts (squat, bench, deadlift, pull-up)',
               'Compare month 1 vs month 3 progress photos in identical conditions',
               'Reassess goal: body composition (are you at target % BF?), performance (strength benchmarks hit?), health (blood markers improved?)',
               'Plan next 12-week block: maintenance phase? New cut? New bulk? Sport focus?']:
        e.append(bl(it))
    e.append(ib('Module 5 (CS_B3) Key Takeaways',[
        'Tracking creates the feedback loop that enables data-driven adjustments; accountability alone improves adherence 30–40%',
        'Daily scale weight is noise; 7-day average is signal — only adjust based on 2+ weeks of average trends',
        'Body weight fluctuates 1–3kg daily from sodium, carbohydrates, hydration, menstrual cycle, and GI contents',
        'Fat loss stall: first increase NEAT (steps) or reduce 100–200 kcal before cutting more; maintain protein',
        'Strength declining in a deficit: refeed day with extra carbs; check sleep; reduce HIIT',
        '12-week comprehensive review: reassess body composition, strength benchmarks, health markers, and plan next phase',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Why is the 7-day average weight more meaningful than any individual daily weigh-in?',
        'A female client sees 2kg of weight gain over 10 days during her luteal phase. She panics. What do you tell her?',
        'A client\'s fat loss has stalled for 3 weeks. Their training has not changed. What are the two most likely explanations and interventions?',
        'When should you add calories in a fat loss phase, and what metrics trigger this decision?',
        'Design a 12-week progress tracking protocol for a beginner starting their first body transformation.',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════
# M6: Mindset for Transformation (35min)
# ═══════════════════════════════════════
def gen_b3_m6():
    fname=os.path.join(OUT,'cs_b3_mod6_transformation_mindset.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(6,'Mindset for Transformation',35)

    e.append(sd('SECTION 1: The Psychology of Physical Change'))
    e.append(sp(6));e.append(h1('Why Transformation Is 20% Physical, 80% Psychological'))
    e.append(p('The knowledge to transform a body is straightforward. Eat in a caloric deficit '
               'or surplus depending on goal, train with progressive overload, sleep 8 hours, '
               'manage stress, and repeat consistently for months and years. Simple — but not easy.'))
    e.append(p('The bottleneck is almost never knowledge or technique — it is consistent '
               'execution over time despite boredom, stress, social pressure, missed sessions, '
               'bad weeks, and the natural human preference for immediate gratification over '
               'delayed, compound results. Mindset is the performance edge.'))
    e.append(h2('Growth Mindset vs Fixed Mindset in Fitness'))
    e.append(mt(['Scenario','Fixed Mindset Response','Growth Mindset Response'],
        [['Miss 2 training sessions','Programme is ruined; give up for the week','Never miss twice; get back on track tomorrow'],
         ['Plateau after 8 weeks','My body just can\'t change; genetics are against me','Plateau = adaptation signal; time to strategically adjust'],
         ['Someone else has a better physique','They\'re genetically gifted; it\'s unfair','Different starting point, different timeline; focus on my journey'],
         ['Fail to hit protein target for 3 days','I\'m bad at nutrition; I\'ll never figure this out','I\'ve identified a weak point; here\'s how I\'ll fix it'],
        ]))
    e.append(sp(8))
    e.append(h2('Self-Compassion in Fitness'))
    e.append(p('Research by Kristin Neff (University of Texas) consistently shows that '
               'self-compassion (treating oneself with kindness after setbacks) produces better '
               'long-term behaviour change outcomes than self-criticism — counterintuitively. '
               'Self-criticism activates the threat system (cortisol, shame), triggering '
               'avoidance and abandonment of goals.'))
    e.append(p('Self-compassion after a setback activates the soothing/contentment system — '
               'producing the psychological safety needed to reflect, learn, and re-engage.'))

    e.append(sd('SECTION 2: Motivation vs Discipline'))
    e.append(sp(6));e.append(h1('The Motivation Trap'))
    e.append(p('Motivation is the feeling of wanting to take action. It is episodic, '
               'unpredictable, and peaks in the early weeks of a new programme. Relying on '
               'motivation ensures failure because it inevitably wanes — as stress increases, '
               'results slow down, and novelty fades.'))
    e.append(p('<b>Discipline</b> is showing up to training and eating well when you don\'t '
               'feel motivated — because you\'ve committed to the process regardless of '
               'feeling. Discipline is built through:'))
    for it in ['Habit stacking (linking training to existing routines)',
               'Reducing friction (gym bag packed, food prepped, alarm set)',
               'Removing decisions (same training time, same weekly meal structure)',
               'Identity anchoring ("I am someone who trains — missing is an exception, not the default")']:
        e.append(bl(it))
    e.append(p('<b>The 5-minute rule:</b> On low-motivation days, commit to starting '
               'training for only 5 minutes. If still not feeling it, you can leave. '
               'In practice, 95% of the time the session continues once started — '
               'inertia is the biggest obstacle, not energy.'))

    e.append(sd('SECTION 3: Social Environment and Transformation'))
    e.append(sp(6));e.append(h1('Your Environment Shapes Your Results'))
    e.append(p('Jim Rohn\'s observation that "you are the average of the five people you '
               'spend the most time with" has empirical support: obesity is socially contagious '
               '(Christakis & Fowler, 2007, NEJM), with a person\'s obesity risk increasing '
               '57% if a close friend becomes obese. The reverse is true — surrounding '
               'yourself with active, health-conscious people dramatically increases adherence.'))
    for it in ['Training partner: accountability increases adherence by 50–65% in research',
               'Online community: RFC community, fitness accountability groups → social reinforcement',
               'Avoid "saboteurs" — social contacts who mock fitness goals, pressure you to deviate, or comment negatively on progress',
               'Communicate your goals clearly to household members — meal prep, shopping habits, and schedule affect them']:
        e.append(bl(it))

    e.append(sd('SECTION 4: Reframing Setbacks as Data'))
    e.append(sp(6));e.append(h1('Every Setback Contains Information'))
    e.append(p('Setbacks are not failures — they are data points revealing gaps in '
               'programme design, habit architecture, or stress management. The '
               'most effective transformers treat every missed session, dietary '
               'deviation, and plateau as diagnostic information:'))
    e.append(mt(['Setback','Data It Contains','Adjustment'],
        [['Missed 3 sessions in 1 week','Training time not protected; competing priorities','Lock training in calendar like meetings; change to morning session'],
         ['Binge eating on weekends','Caloric restriction too aggressive during week; social triggers','Increase daily calories by 100–200 kcal; create a restaurant strategy'],
         ['Plateau in fat loss at week 8','Metabolic adaptation; probable NEAT reduction','Diet break week + step count audit; resume with 200 kcal reduction'],
         ['Loss of gym motivation at week 6','Programme novelty faded; no new goals visible','New exercise variation; enter a fitness challenge; change training location'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 6 (CS_B3) Key Takeaways',[
        'Knowledge is not the bottleneck; consistent execution over months is — mindset determines this',
        'Growth mindset: setbacks = information; fixed mindset: setbacks = identity threat',
        'Self-compassion after setbacks outperforms self-criticism for long-term behaviour change',
        'Motivation is episodic and unreliable; discipline built on identity ("I am a person who trains") is durable',
        'The 5-minute rule overcomes inertia on low-motivation days: commit to starting, not finishing',
        'Social environment is as powerful as programme design — training partners, accountability groups, and household alignment matter',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Explain the difference between self-compassion and self-indulgence in the context of fitness setbacks.',
        'Why does motivation reliably decline at weeks 6–8 and what structures prevent the resulting programme abandonment?',
        'Describe three specific ways to improve social environment support for body transformation.',
        'What is the 5-minute rule and what psychological principle underlies it?',
        'Reframe the following as data: "I ate a whole pizza last Saturday night and my weight jumped 1.5kg."',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════════
# M7: Lifestyle Optimisation — Sleep, Stress & NEAT (35min)
# ═══════════════════════════════════════════════════════
def gen_b3_m7():
    fname=os.path.join(OUT,'cs_b3_mod7_lifestyle_optimization.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(7,'Lifestyle Optimisation: Sleep, Stress & NEAT',35)

    e.append(sd('SECTION 1: Sleep — The Cornerstone of Transformation'))
    e.append(sp(6));e.append(h1('Sleep Deprivation: The Hidden Saboteur'))
    e.append(p('Of all lifestyle factors that influence body composition, sleep is the most '
               'underrated and the most actionable. The evidence is unambiguous: insufficient '
               'sleep systematically undermines every aspect of body transformation.'))
    e.append(mt(['Sleep Deprivation Effect','Mechanism','Magnitude'],
        [['Increased fat gain (less muscle) from same caloric surplus','Elevated cortisol + reduced GH; poor nutrient partitioning','Sleeping 5.5h = only 18% of weight gained is muscle vs 50% at 8.5h (Nedeltcheva 2010)'],
         ['Increased hunger','Ghrelin +15–20%; leptin −15–18%','400–500 extra kcal consumed per day on sleep-deprived days'],
         ['Reduced testosterone','Restricting to 5h/night for 1 week drops testosterone 10–15%','Equal to 10–15 years of aging'],
         ['Impaired training performance','Reaction time, strength, power output, endurance all decrease with <7h','5–15% performance reduction across measures'],
         ['Reduced insulin sensitivity','Cortisol + reduced GLUT4 expression','Equivalent to pre-diabetic state after 6 days of 4h sleep'],
         ['Impaired muscle recovery','Reduced GH; increased cortisol; impaired protein synthesis overnight','Longer time between sessions needed; greater risk of overreaching'],
        ]))
    e.append(sp(8))
    e.append(h2('Sleep Extension — The Performance Drug'))
    e.append(p('If sleep could be bottled as a supplement, it would be the most powerful '
               'performance enhancer ever discovered. Sleep extension studies show:'))
    for it in ['Stanford Basketball study (Mah 2011): 10h sleep/night → 5% sprint speed, 9% free throw accuracy',
               'Rugby players: 2 additional hours of sleep/night → 20–24% faster 40m sprint times',
               'Swimmers: 9–10h sleep vs normal → improved reaction time, turn time, kick stroke',
               'General training: muscle protein synthesis peaks during N3 deep sleep; 8+ hours required to complete multiple cycles']:
        e.append(bl(it))

    e.append(sd('SECTION 2: Stress Management for Body Composition'))
    e.append(sp(6));e.append(h1('The Cortisol-Body Composition Connection'))
    e.append(p('Chronic psychological stress activates the HPA axis, producing chronically '
               'elevated cortisol. For body transformation, this is deeply counterproductive:'))
    for it in ['Cortisol promotes visceral fat deposition (visceral adipocytes have 4× cortisol receptors vs subcutaneous)',
               'Cortisol stimulates appetite for high-calorie foods (especially sugar and fat)',
               'Cortisol suppresses testosterone (antagonist relationship)',
               'Cortisol inhibits growth hormone secretion (impairs overnight recovery)',
               'Cortisol is catabolic — promotes muscle protein breakdown for gluconeogenesis']:
        e.append(bl(it))
    e.append(h2('Evidence-Based Stress Reduction Strategies'))
    e.append(mt(['Strategy','Effect on Cortisol','Time Required','Evidence Level'],
        [['Diaphragmatic breathing (4-7-8, box breathing)','Activates parasympathetic; acute cortisol reduction','5–10 min daily','A — immediate effects well-documented'],
         ['Meditation (mindfulness-based)','10–15% reduction in salivary cortisol over 8 weeks','10–20 min daily','A — strong meta-analytic support'],
         ['Nature exposure (green/blue spaces)','Measurable cortisol reduction in 20 min','20–30 min outdoors','B — consistent findings'],
         ['Social connection (positive)','Oxytocin release → cortisol reduction','Varies','B — strong epidemiological data'],
         ['Progressive muscle relaxation','Reduces sympathetic activity; lowers cortisol','15–20 min','B — clinical evidence'],
         ['Journaling (expressive writing)','Processes emotional load; reduces rumination-related cortisol','10–15 min before bed','B — Pennebaker paradigm'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 3: NEAT — Non-Exercise Activity Thermogenesis'))
    e.append(sp(6));e.append(h1('NEAT: The Secret to Sustainable Fat Loss'))
    e.append(p('Non-Exercise Activity Thermogenesis (NEAT) encompasses all calorie-burning '
               'movement that isn\'t deliberate exercise: walking to work, climbing stairs, '
               'fidgeting, standing, household chores, grocery shopping, spontaneous movement.'))
    e.append(p('<b>NEAT varies enormously between people:</b> Studies show NEAT varies up '
               'to 2000 kcal/day between individuals of similar body size. This variation '
               'explains why some people seem to "eat anything and not gain weight" — they '
               'have high spontaneous NEAT.'))
    e.append(mt(['NEAT Activity','Calories Burned/Hour','vs Sedentary Sitting'],
        [['Standing','80–100 kcal/hr','vs sitting (70 kcal/hr) = 10–30 kcal/hr extra'],
         ['Walking (slow, 4km/hr)','150–200 kcal/hr','80–130 kcal/hr extra'],
         ['Walking (brisk, 6km/hr)','250–350 kcal/hr','180–280 kcal/hr extra'],
         ['Fidgeting/postural movement','50–100 kcal/hr above sitting','Varies widely between individuals'],
         ['Household chores','150–250 kcal/hr','80–180 kcal/hr extra'],
         ['Standing desk (full workday)','~100 extra kcal/8hr day','Small but accumulates'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Why NEAT matters more than gym cardio for most people:</b> A person who '
               'trains 5 hours/week but sits for 12+ hours/day has a fundamentally lower '
               'total calorie burn than an "untrained" person who walks everywhere, stands '
               'at work, and takes the stairs. Exercise alone cannot compensate for '
               'a sedentary lifestyle.'))
    e.append(h2('NEAT Optimisation Strategies'))
    for it in ['10,000 steps/day target: burns 300–500 extra kcal with no recovery cost; walk after meals (improves glucose control)',
               'Standing desk or desk riser: adds 30–60 min standing per day; reduces sedentary time',
               'Walk during phone calls: accumulates 30–60 min of movement on work days without time cost',
               'Stairs > lift: 5 flights of stairs/day = 2km equivalent of NEAT',
               'Parking deliberately further: 10 min walk each way = 100–150 kcal extra/day',
               'Active commute: cycling or walking to work transforms commute time into NEAT']:
        e.append(bl(it))
    e.append(p('<b>NEAT suppression during dieting:</b> When calories are reduced, the body '
               'unconsciously reduces NEAT by 200–400 kcal/day — less fidgeting, slower '
               'movement, more resting. This is a key component of metabolic adaptation. '
               'Consciously targeting steps (using a step counter) counteracts this '
               'suppression.'))
    e.append(ib('Module 7 (CS_B3) Key Takeaways',[
        'Sleep is non-negotiable: 5.5h vs 8.5h of sleep changes the muscle:fat ratio of weight gained from 50:50 to 18:82',
        'Ghrelin rises and leptin falls with sleep deprivation — adding 400–500 kcal of daily hunger',
        'Chronic cortisol from stress selectively deposits visceral fat and suppresses testosterone and GH',
        'Meditation, diaphragmatic breathing, and nature exposure are evidence-based cortisol reducers',
        'NEAT varies up to 2000 kcal/day between similar-sized individuals — the key to "effortless" leanness',
        'Protect NEAT during dieting by consciously tracking steps (target 8000–10,000/day) as the body suppresses it unconsciously',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['What does the Nedeltcheva 2010 study reveal about sleep duration and body composition changes during a caloric surplus?',
        'Explain the three mechanisms by which sleep deprivation increases daily caloric intake.',
        'What is NEAT suppression and how does it contribute to metabolic adaptation during dieting?',
        'Compare the NEAT calorie burn of a "gym 5×/week but sedentary otherwise" person vs a "no gym but walks everywhere" person.',
        'Describe two breathing techniques that reduce acute cortisol and explain the mechanism.',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════
# M8: Final Assessment CS_B3 (20min)
# ═══════════════════════════════════════
def gen_b3_m8():
    fname=os.path.join(OUT,'cs_b3_mod8_final_assessment.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(8,'Final Assessment & Certificate',20)

    e.append(sd('ASSESSMENT INSTRUCTIONS'))
    e.append(sp(6))
    e.append(ib('How to Complete This Assessment',[
        '25 questions covering all 7 modules of CS_B3 Body Transformation Blueprint',
        'One correct answer per question (A, B, C, or D)',
        'Passing score: 70% (18/25). Open-book assessment',
        'Target completion: 20 minutes',
    ],RFC_ORANGE))
    e.append(sp(12))

    questions=[
        ('1. What body fat percentage range is classified as "fitness" for adult males?',
         ['A) 3–5%','B) 6–13%','C) 14–17%','D) 18–24%'],'C'),
        ('2. Body recomposition is MOST achievable in which population?',
         ['A) Advanced athletes with years of training','B) Beginners in their first 1–2 years of resistance training','C) Overweight individuals doing cardio only','D) Athletes during a competition season peak'],'B'),
        ('3. Lipolysis is the process of:',
         ['A) Muscle protein synthesis stimulated by leucine','B) Glycogen breakdown to glucose','C) Triglycerides → fatty acids + glycerol (fat release from adipose tissue)','D) Beta-oxidation of fatty acids in mitochondria'],'C'),
        ('4. Chronic cortisol elevation preferentially deposits fat in which location?',
         ['A) Gluteofemoral (hips and thighs)','B) Subcutaneous fat (beneath skin everywhere)','C) Intramuscular fat (IMTG)','D) Visceral (abdominal, around organs)'],'D'),
        ('5. Which statement about the "fat burning zone" is most accurate?',
         ['A) Low-intensity exercise burns more total fat calories than high-intensity','B) Low-intensity burns a higher fat percentage but high-intensity burns more total calories and absolute fat','C) The fat burning zone does not exist','D) Running at >75% HRmax burns 100% carbohydrates with no fat oxidation'],'B'),
        ('6. Leptin is secreted by:',
         ['A) The pancreas in response to high blood glucose','B) The hypothalamus in response to caloric restriction','C) Adipose tissue in proportion to fat stores','D) The liver in response to physical exercise'],'C'),
        ('7. Sleep restricting to 5.5 hours vs 8.5 hours during a caloric surplus results in (Nedeltcheva 2010):',
         ['A) Identical body composition change between groups','B) Only 18% of weight gained as muscle (vs 50% at 8.5h) — primarily fat gain in the sleep-deprived group','C) Greater muscle gain in the sleep-deprived group due to anabolic adaptation','D) No difference in hormones but slightly worse mood'],'B'),
        ('8. The primary molecular reason the "interference effect" occurs is:',
         ['A) Lactic acid from cardio impairs muscle protein synthesis directly','B) AMPK (activated by endurance training) inhibits mTORC1 (required for hypertrophy)','C) Cardio burns the glycogen needed for lifting weights','D) Running causes micro-tears in leg muscles that compete for amino acids'],'B'),
        ('9. To minimise concurrent training interference, cardio should ideally be separated from resistance training by:',
         ['A) 30 minutes','B) 1–2 hours','C) At least 6 hours (ideally 24 hours or different days)','D) No separation needed — do cardio first always'],'C'),
        ('10. The Minimum Effective Volume (MEV) for hypertrophy per muscle group per week is approximately:',
         ['A) 3–5 hard sets','B) 6–9 hard sets','C) 10–12 hard sets','D) 20–25 hard sets'],'C'),
        ('11. Which mechanism of hypertrophy is considered the primary driver (~60–70% of signal)?',
         ['A) Metabolic stress / pump','B) Muscle damage from eccentric loading','C) Mechanical tension on actin-myosin crossbridges','D) Growth hormone release during training'],'C'),
        ('12. The hip thrust produces greater glute max activation than the squat by approximately:',
         ['A) 5%','B) 10%','C) 30%+','D) Equal activation — no difference'],'C'),
        ('13. A 7-day average weight shows no change for 2 consecutive weeks during a fat loss programme. The FIRST adjustment should be:',
         ['A) Immediately reduce calories by 500 kcal','B) Add 2 HIIT sessions per week','C) Increase NEAT by 2000 steps/day or reduce calories 100–200 kcal','D) Switch to a ketogenic diet'],'C'),
        ('14. Which of the following causes the most significant daily body weight fluctuation?',
         ['A) Actual fat gain or loss','B) Muscle protein synthesis changes','C) High sodium meal causing water retention + glycogen storage','D) Basal metabolic rate variation'],'C'),
        ('15. Waist circumference above which measurement indicates HIGH metabolic risk in men?',
         ['A) 80cm','B) 88cm','C) 94cm','D) 102cm'],'D'),
        ('16. NEAT (Non-Exercise Activity Thermogenesis) can vary between similar-sized individuals by up to:',
         ['A) 100–200 kcal/day','B) 300–500 kcal/day','C) 500–1000 kcal/day','D) 1500–2000 kcal/day'],'D'),
        ('17. Sleep deprivation of 1 week (5h/night) reduces testosterone in males by approximately:',
         ['A) 1–2%','B) 5%','C) 10–15%','D) 25–30%'],'C'),
        ('18. The optimal fat loss rate to preserve lean mass for most recreational athletes is:',
         ['A) 0.1–0.2% body weight/week','B) 0.5–1% body weight/week','C) 1.5–2% body weight/week','D) 2–3% body weight/week'],'B'),
        ('19. Growth mindset vs fixed mindset: when a person hits a training plateau, growth mindset responds by:',
         ['A) Concluding their genetics are the limiting factor','B) Quitting the current programme immediately','C) Treating the plateau as an adaptation signal and strategically adjusting variables','D) Reducing training frequency to "avoid overtraining"'],'C'),
        ('20. Which type of cardio is most appropriate during a hypertrophy block due to minimal muscle interference?',
         ['A) 2× weekly HIIT running sessions','B) 4× weekly sprint training','C) 3–4× weekly LISS (low-intensity cycling, walking)','D) Daily heavy rowing machine intervals'],'C'),
        ('21. The Nedeltcheva 2010 study on sleep and body composition found that:',
         ['A) Sleep duration does not affect body composition during caloric surplus','B) Greater muscle gain occurred with 5.5h vs 8.5h sleep','C) 8.5h sleep resulted in 50% of weight gained as lean mass vs 18% at 5.5h','D) Sleep only affects recovery from endurance training, not resistance training'],'C'),
        ('22. Which of the following is the most accurate statement about spot reduction?',
         ['A) Ab exercises burn abdominal fat preferentially through increased local blood flow','B) Spot reduction is scientifically proven for the abdominal region only','C) Fat is mobilised systemically based on genetics/hormones — not adjacent to contracting muscle','D) Spot reduction works for subcutaneous but not visceral fat'],'C'),
        ('23. Ghrelin levels are most effectively managed by:',
         ['A) Eating one large meal per day','B) High protein intake + adequate sleep + high-volume vegetables','C) Low-fat, high-carbohydrate meals before training','D) Extended overnight fasting (>16 hours)'],'B'),
        ('24. The 5-minute rule for low motivation days states:',
         ['A) Rest is mandatory when motivation is below 5/10','B) Commit to only 5 minutes of training, with permission to stop after','C) 5 minutes of meditation before training replaces motivation','D) 5 grams of caffeine should be consumed before training'],'B'),
        ('25. NEAT is unconsciously suppressed by how many calories per day when dieting?',
         ['A) 25–50 kcal/day','B) 50–100 kcal/day','C) 100–200 kcal/day','D) 200–400 kcal/day'],'D'),
    ]

    for qtext,opts,ans in questions:
        e.append(Paragraph(qtext,S['q']))
        for opt in opts:
            e.append(Paragraph(opt,S['ans']))
        e.append(sp(10))

    e.append(PageBreak())
    e.append(sd('ANSWER KEY'))
    e.append(sp(8))
    all_q=[f'Q{i+1}: {a}' for i,(_,_,a) in enumerate(questions)]
    per_row=5
    tbl_rows=[all_q[i:i+per_row] for i in range(0,25,per_row)]
    tbl=Table(tbl_rows,colWidths=[(W-40*mm)/per_row]*per_row)
    tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),RFC_ORANGE),('TEXTCOLOR',(0,0),(-1,0),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),11),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC'))]))
    e.append(tbl)
    e.append(sp(20))

    e.append(PageBreak())
    cert=Table([['ROYAL FITNESS CLUB\nBODY TRANSFORMATION BLUEPRINT CERTIFICATE']],colWidths=[W-40*mm])
    cert.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_DARK),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),18),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),22),('BOTTOMPADDING',(0,0),(-1,-1),22)]))
    e.append(cert)
    e.append(HRFlowable(width='100%',thickness=3,color=RFC_GOLD))
    e.append(sp(16))
    e.append(Paragraph('This certifies that',ParagraphStyle('ct',fontName='Helvetica',fontSize=14,textColor=RFC_DARK,alignment=TA_CENTER,leading=20)))
    e.append(Paragraph('_______________________________________',ParagraphStyle('line',fontName='Helvetica-Bold',fontSize=22,textColor=RFC_DARK,alignment=TA_CENTER,leading=30,spaceAfter=8)))
    e.append(Paragraph('has completed the',ParagraphStyle('ct2',fontName='Helvetica',fontSize=14,textColor=RFC_DARK,alignment=TA_CENTER,leading=20)))
    e.append(Paragraph('Body Transformation Blueprint — CS_B3',ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=17,textColor=RFC_ORANGE,alignment=TA_CENTER,leading=24,spaceBefore=8,spaceAfter=12)))
    e.append(Paragraph('demonstrating comprehensive knowledge of body composition, fat loss science, muscle building,\ncardiovascular training, progress tracking, transformation mindset, and lifestyle optimisation.',
                        ParagraphStyle('sub',fontName='Helvetica',fontSize=11,textColor=RFC_GRAY,alignment=TA_CENTER,leading=17,spaceAfter=20)))
    e.append(sp(20))
    sig=Table([['___________________','___________________'],['Instructor Signature','Date']],
              colWidths=[(W-40*mm)/2,(W-40*mm)/2])
    sig.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),11)]))
    e.append(sig)
    e.append(sp(20))
    flag=Table([['']*3],colWidths=[(W-40*mm)/3]*3,rowHeights=[8])
    flag.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),colors.HexColor('#FF9933')),
        ('BACKGROUND',(1,0),(1,0),RFC_WHITE),('BACKGROUND',(2,0),(2,0),RFC_GREEN)]))
    e.append(flag)
    doc.build(e)
    print(f'Generated: {fname}')

gen_b3_m1(); gen_b3_m2(); gen_b3_m3(); gen_b3_m4()
gen_b3_m5(); gen_b3_m6(); gen_b3_m7(); gen_b3_m8()
print('cs_b3 ALL 8 MODULES COMPLETE.')
print('ALL 24 BEGINNER COURSE PDFs GENERATED.')
