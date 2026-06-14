#!/usr/bin/env python3
"""Generate cs_b1 M4 (Nutrition 101, 55min) and M5 (Recovery & Sleep, 35min)"""
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

RFC_RED   = colors.HexColor('#E8001D')
RFC_DARK  = colors.HexColor('#1A1A2E')
RFC_GOLD  = colors.HexColor('#FFD700')
RFC_BLUE  = colors.HexColor('#0066CC')
RFC_GREEN = colors.HexColor('#138808')
RFC_WHITE = colors.white
RFC_LIGHT = colors.HexColor('#F5F5F5')
RFC_GRAY  = colors.HexColor('#555555')

S = {
    'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22, textColor=RFC_DARK, leading=28, spaceBefore=18, spaceAfter=10),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=17, textColor=RFC_BLUE, leading=22, spaceBefore=14, spaceAfter=7),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=13, textColor=RFC_DARK, leading=18, spaceBefore=10, spaceAfter=5),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=11, textColor=RFC_GRAY, leading=17, spaceAfter=7, alignment=TA_JUSTIFY),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=11, textColor=RFC_GRAY, leading=16, spaceAfter=4, leftIndent=18, bulletIndent=6),
    'caption': ParagraphStyle('cap', fontName='Helvetica', fontSize=9, textColor=RFC_GRAY, leading=13, alignment=TA_CENTER),
}

def cover(course_name, mod_num, mod_title, duration, code):
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
    meta = Table([['Duration',f'{duration} minutes'],['Course Code',code],['Level','Beginner'],['Format','Study Guide PDF']],
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
    e.append(Paragraph('Part of the Royal Fitness Club Professional Certification Program.', S['caption']))
    e.append(PageBreak())
    return e

def sd(text):
    t = Table([[text]], colWidths=[W-40*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),13),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),12)]))
    return t

def ib(title, items, bg=RFC_DARK):
    rows=[[Paragraph(title,ParagraphStyle('bt',fontName='Helvetica-Bold',fontSize=12,textColor=RFC_WHITE,leading=16))]]
    for it in items:
        rows.append([Paragraph(f'• {it}',ParagraphStyle('bb',fontName='Helvetica',fontSize=11,textColor=RFC_DARK,leading=15,spaceAfter=3))])
    t=Table(rows,colWidths=[W-40*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),bg),('BACKGROUND',(0,1),(-1,-1),RFC_LIGHT),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEBELOW',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),('BOX',(0,0),(-1,-1),1.5,bg)]))
    return t

def mt(headers, rows):
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

def p(t): return Paragraph(t, S['body'])
def h1(t): return Paragraph(t, S['h1'])
def h2(t): return Paragraph(t, S['h2'])
def bl(t): return Paragraph(f'• {t}', S['bullet'])
def sp(n=8): return Spacer(1,n)

# ═══════════════════════════════════════════
# MODULE 4: Nutrition 101 (55 min)
# ═══════════════════════════════════════════
def gen_b1_m4():
    fname = os.path.join(OUT,'cs_b1_mod4_nutrition_101.pdf')
    doc = SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e = []
    e += cover('Fitness Foundations Certificate',4,'Nutrition 101 — Fuelling Your Body',55,'CS_B1')

    e.append(sd('SECTION 1: Why Nutrition Is the Foundation'))
    e.append(sp(6))
    e.append(h1('Food as Fuel, Structure, and Information'))
    e.append(p('Nutrition is not merely about calories. The food you eat serves three fundamental roles: '
               'it provides energy (fuel) for all biological processes; it provides structural building '
               'blocks (protein, minerals) for tissue repair and growth; and it provides regulatory '
               'signals (vitamins, phytonutrients, omega-3s) that modulate gene expression, hormones, '
               'and inflammation.'))
    e.append(p('The phrase "you cannot out-train a bad diet" is not cliché — it is physiology. A '
               'caloric deficit of 500 kcal per day takes 5 minutes to consume in a fast-food meal. '
               'Burning those 500 kcal through exercise takes 45–60 minutes of vigorous training. '
               'Nutrition provides the leverage.'))
    e.append(ib('Core Nutrition Principles',[
        'Energy balance (calories in vs calories out) primarily determines body weight',
        'Macronutrient composition determines body composition (muscle vs fat)',
        'Micronutrients ensure metabolic processes function optimally',
        'Meal timing can modulate performance and recovery (though less important than total intake)',
        'Hydration affects performance, cognition, and every biochemical reaction in the body',
    ],RFC_DARK))
    e.append(sp(8))

    e.append(sd('SECTION 2: Macronutrients — The Big Three'))
    e.append(sp(6))
    e.append(h1('Proteins — The Building Blocks'))
    e.append(p('Protein is composed of amino acids — 20 in total, of which 9 are essential '
               '(cannot be synthesised by the body and must be obtained from food). Proteins '
               'function as structural components (muscle, collagen, hair, nails), enzymes, '
               'hormones (insulin, glucagon), immune factors (antibodies), and transporters (haemoglobin).'))
    e.append(p('<b>For fitness:</b> Dietary protein provides the amino acids required for muscle '
               'protein synthesis (MPS). The most important amino acid for MPS is leucine — a '
               'branched-chain amino acid (BCAA) that directly activates the mTORC1 signalling '
               'cascade. A threshold of ~2–3g leucine per meal is required to maximally stimulate MPS.'))
    e.append(mt(
        ['Protein Quality Measure','Definition','High Scorers','Low Scorers'],
        [['Biological Value (BV)','% nitrogen absorbed from protein that is retained','Egg (100), Whey (104), Milk (91)','Wheat (54), Corn (60)'],
         ['PDCAAS','Amino acid profile vs human needs (0–1 scale)','Casein (1.0), Soy (1.0), Whey (1.0)','Wheat gluten (0.25)'],
         ['DIAAS','Updated; digestion in small intestine','Beef (~1.1), Egg (~1.1)','Most plant proteins <1.0'],
        ]
    ))
    e.append(sp(8))
    e.append(h2('Protein Requirements for Different Goals'))
    e.append(mt(
        ['Population','Recommendation (g/kg BW/day)','Notes'],
        [['Sedentary adult','0.8','Minimum; prevents deficiency'],
         ['Recreational exerciser','1.2–1.6','Maintains lean mass'],
         ['Resistance training (hypertrophy)','1.6–2.2','Upper range during caloric deficit'],
         ['Endurance athlete','1.4–1.7','Protein for oxidation + repair'],
         ['During caloric deficit (fat loss)','2.2–3.1','Prevents muscle loss (leucine-rich)'],
         ['Older adults (>60)','1.6–2.2','Anabolic resistance requires more protein per meal'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Protein distribution:</b> Spreading protein intake across 3–4 meals (20–40g each) '
               'maximises 24-hour MPS compared to skewing protein to one meal. This is a practical '
               'reason for breakfast protein — skipping it reduces daily MPS potential.'))
    e.append(sp())

    e.append(h1('Carbohydrates — The Performance Fuel'))
    e.append(p('Carbohydrates are the body\'s preferred fuel for moderate-to-high intensity exercise. '
               'They are classified by structure:'))
    e.append(mt(
        ['Class','Chain Length','Examples','Digestion Speed'],
        [['Monosaccharides','1 unit','Glucose, fructose, galactose','Immediate'],
         ['Disaccharides','2 units','Sucrose (table sugar), lactose, maltose','Fast'],
         ['Oligosaccharides','3–10 units','FOS (prebiotic fibres)','Slow/fermented'],
         ['Polysaccharides','10+ units','Starch (amylose/amylopectin), glycogen','Slow → very slow'],
         ['Dietary fibre','Non-digestible','Cellulose, pectin, beta-glucan','Not digested — fermented'],
        ]
    ))
    e.append(sp(8))
    e.append(h2('Glycaemic Index (GI) and Glycaemic Load (GL)'))
    e.append(p('<b>Glycaemic Index</b> rates how quickly a food raises blood glucose relative to '
               'pure glucose (GI=100). <b>Glycaemic Load</b> accounts for portion size: GL = (GI × '
               'grams of carb) / 100. GL is more practically relevant — watermelon has a high GI '
               'but a low GL due to its high water content.'))
    e.append(mt(
        ['GI Category','GI Range','Examples','Sports Context'],
        [['Low GI','<55','Oats, legumes, basmati rice, most fruits','Pre-workout (sustained energy)'],
         ['Medium GI','55–69','White rice, corn, banana','Mixed — versatile'],
         ['High GI','>70','White bread, rice cakes, sports drinks, dates','Post-workout (rapid glycogen resynthesis)'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Carbohydrate loading:</b> In the 24–72 hours before endurance events lasting '
               '>90 minutes, increasing carbohydrate to 8–12g/kg/day maximises glycogen stores '
               '(~500g total: ~400g muscle + ~100g liver). This delays glycogen depletion and '
               '"hitting the wall" (bonking).'))
    e.append(sp())

    e.append(h1('Fats — The Essential Macronutrient'))
    e.append(p('Dietary fat is not the enemy — it is essential for hormone production '
               '(testosterone, oestrogen, cortisol all require cholesterol), fat-soluble '
               'vitamin absorption (A, D, E, K), cell membrane integrity, brain function '
               '(60% of the brain is fat), and as the primary fuel at rest and low intensities.'))
    e.append(mt(
        ['Fat Type','Structure','Examples','Health Effects'],
        [['Saturated','No double bonds','Butter, coconut oil, red meat fat','Neutral at moderate intake; excess may increase LDL-C'],
         ['Monounsaturated (MUFA)','1 double bond','Olive oil, avocado, nuts','Improves lipid profile; anti-inflammatory'],
         ['Polyunsaturated (PUFA)','2+ double bonds','Omega-3 (fish, flaxseed), Omega-6 (sunflower)','Essential; omega-3 anti-inflammatory; balance omega-6:3 ratio'],
         ['Trans fats','Artificially hydrogenated','Partial hydrogenation products (rare now)','Strongly increase CVD risk; minimise or avoid'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Omega-3 fatty acids:</b> EPA (eicosapentaenoic acid) and DHA (docosahexaenoic acid) '
               'are the most bioactive omega-3s. They reduce inflammation, improve insulin sensitivity, '
               'support brain health, and may enhance muscle protein synthesis. Target 1–3g EPA+DHA '
               'per day via fatty fish (2×/week) or fish/algae oil supplementation.'))
    e.append(p('<b>Dietary fat requirement for athletes:</b> 20–35% of total calories from fat; '
               'never below 15% (disrupts hormone production). Fat intake below 15% suppresses '
               'testosterone production — counterproductive for any athletic goal.'))
    e.append(sp())

    e.append(sd('SECTION 3: TDEE — Total Daily Energy Expenditure'))
    e.append(sp(6))
    e.append(h1('Calculating Your Caloric Target'))
    e.append(p('TDEE (Total Daily Energy Expenditure) is the total calories your body burns '
               'in 24 hours. It is composed of four components:'))
    e.append(mt(
        ['Component','Abbreviation','% of TDEE','Description'],
        [['Basal Metabolic Rate','BMR','60–75%','Calories to maintain basic life functions at rest'],
         ['Thermic Effect of Activity','TEA','15–30%','Calories burned during planned exercise'],
         ['Non-Exercise Activity Thermogenesis','NEAT','10–20%','All movement outside planned exercise (walking, fidgeting, posture)'],
         ['Thermic Effect of Food','TEF','8–12%','Calories burned digesting food (protein TEF highest ~25–30%)'],
        ]
    ))
    e.append(sp(8))
    e.append(h2('Mifflin-St Jeor Equation (Most Accurate Widely Used)'))
    e.append(p('<b>BMR for males:</b> (10 × weight kg) + (6.25 × height cm) − (5 × age) + 5'))
    e.append(p('<b>BMR for females:</b> (10 × weight kg) + (6.25 × height cm) − (5 × age) − 161'))
    e.append(mt(
        ['Activity Level','Multiplier','Example'],
        [['Sedentary (desk job, no exercise)','1.2','BMR × 1.2'],
         ['Lightly active (1–3 days/week exercise)','1.375','BMR × 1.375'],
         ['Moderately active (3–5 days/week)','1.55','BMR × 1.55'],
         ['Very active (6–7 days hard exercise)','1.725','BMR × 1.725'],
         ['Extremely active (physical job + training)','1.9','BMR × 1.9'],
        ]
    ))
    e.append(sp(8))
    e.append(h2('Caloric Targets by Goal'))
    e.append(mt(
        ['Goal','Deficit/Surplus','Weekly Weight Change','Notes'],
        [['Aggressive fat loss','-750 kcal/day (max)','~0.7kg/week loss','Risk of muscle loss above this'],
         ['Moderate fat loss','-500 kcal/day','~0.5kg/week','Optimal for body composition'],
         ['Gentle fat loss','-250 kcal/day','~0.25kg/week','Best for athletes maintaining performance'],
         ['Maintenance','0','0kg','Recomp possible for beginners'],
         ['Lean bulk','+200–300 kcal/day','~0.1–0.2kg/week','Minimises fat gain'],
         ['Standard bulk','+500 kcal/day','~0.25–0.5kg/week','Faster mass, more fat gain'],
        ]
    ))
    e.append(sp(8))

    e.append(sd('SECTION 4: Meal Timing for Performance'))
    e.append(sp(6))
    e.append(h1('The Anabolic Window — Fact and Fiction'))
    e.append(p('The "anabolic window" concept — that protein must be consumed within 30 minutes '
               'post-workout or gains are lost — is largely a myth when total daily protein '
               'intake is adequate. Research shows the window is likely 4–6 hours around '
               'training when factoring in pre-workout protein.'))
    e.append(p('However, the peri-workout (around training) window does matter when:'))
    for it in ['Training in a fasted state (morning without breakfast)',
               'Performing two training sessions in one day',
               'Training sessions exceed 90 minutes',
               'Competing in endurance events with rapid recovery requirements']:
        e.append(bl(it))
    e.append(mt(
        ['Timing','Recommendation','Rationale'],
        [['Pre-workout (1–3 hrs before)','20–40g protein + carbohydrate + low fat','Amino acids available during training; glycogen topped up'],
         ['Intra-workout (>60 min sessions)','30–60g carbs/hr (sports drink, banana, gels)','Maintains blood glucose; spares glycogen'],
         ['Post-workout (within 0–2 hrs)','20–40g complete protein + carbohydrate','MPS initiation; glycogen resynthesis'],
         ['Before sleep','30–40g casein protein','Slow-digesting; sustains MPS overnight; GH release during sleep'],
        ]
    ))
    e.append(sp(8))

    e.append(sd('SECTION 5: Hydration'))
    e.append(sp(6))
    e.append(h1('Water — The Forgotten Nutrient'))
    e.append(p('The human body is 60–70% water by mass. Even mild dehydration (1–2% body weight '
               'loss as sweat) demonstrably impairs endurance performance by 5–10%, cognitive '
               'function, and mood. At 5% dehydration, heat stroke risk rises sharply.'))
    e.append(p('<b>Daily fluid needs:</b> Approximately 35–45ml per kg body weight per day for '
               'sedentary adults. Add 500–750ml per hour of moderate exercise; more in heat and humidity.'))
    e.append(mt(
        ['Indicator','Optimal','Mild Dehydration','Severe Dehydration'],
        [['Urine colour','Pale yellow (lemonade)','Dark yellow (apple juice)','Dark amber / orange'],
         ['Body weight change','<1% loss','1–3% loss','>3% loss'],
         ['Thirst sensation','Absent or mild','Noticeable','Intense'],
         ['Performance impact','Baseline','−5–10%','−20–30%+'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Electrolytes:</b> Sweat contains sodium, chloride, potassium, magnesium, and '
               'calcium. For sessions under 60 minutes, water suffices. For longer sessions in '
               'heat, sodium (the primary sweat electrolyte at 500–2000mg/hr) must be replaced '
               'to prevent hyponatraemia — dangerously low blood sodium from over-hydrating '
               'with pure water.'))
    e.append(ib('Hydration Strategy for Training',[
        'Drink 500ml water 2 hours pre-workout; another 250ml 15–20 minutes before',
        'Drink 150–250ml every 15–20 minutes during training',
        'Weigh before and after — each 1kg lost ≈ 1L of fluid to replace',
        'Electrolyte drink for sessions >60 minutes; hot weather; heavy sweaters',
        'Coffee/tea count toward hydration — the mild diuretic effect is offset by the fluid volume',
    ], RFC_BLUE))
    e.append(sp(8))

    e.append(sd('SECTION 6: Reading Nutrition Labels'))
    e.append(sp(6))
    e.append(h1('Decoding the Nutrition Facts Panel'))
    e.append(p('Understanding nutrition labels is a practical skill that empowers food choice. '
               'Indian packaged food labels (FSSAI regulations) include serving size, energy, '
               'protein, carbohydrate (total and sugars), fat (total, saturated, trans), '
               'dietary fibre, and sodium.'))
    e.append(h2('Key Label Elements'))
    for item in [
        '<b>Serving size:</b> The reference amount for all values. Always check — a packet may contain 2–3 servings',
        '<b>Calories per serving:</b> Total energy. Remember 1 cal on label = 1 kcal in science',
        '<b>% Daily Value:</b> Based on a 2000 kcal diet — adjust for your TDEE',
        '<b>Added sugars vs total sugars:</b> Fruit has natural sugar (less concerning); added sugar should be minimised',
        '<b>Sodium:</b> Target <2300mg/day for general health; athletes may need more if sweat rate is high',
        '<b>Ingredient list:</b> Ingredients listed in descending order by weight — first ingredient is most abundant',
    ]:
        e.append(bl(item))
    e.append(p('<b>5/20 rule:</b> 5% Daily Value or less = low in that nutrient; 20%+ = high. '
               'Apply to nutrients you want more of (fibre, protein, vitamins) and those '
               'you want to limit (saturated fat, sodium, added sugar).'))
    e.append(ib('Module 4 Key Takeaways',[
        'Macronutrients (protein, carbs, fat) provide energy and structural/regulatory functions',
        'Protein: 1.6–2.2g/kg/day for athletes; distribute across 3–4 meals with 20–40g per meal',
        'Carbohydrates are the primary fuel for moderate-to-high intensity exercise; choose GI appropriately',
        'Fats are essential — never go below 15% of calories; prioritise unsaturated and omega-3 sources',
        'TDEE = BMR × activity multiplier; set caloric target by adding/subtracting from maintenance',
        'Hydration: pale urine, 35–45ml/kg body weight/day baseline; add 500–750ml per training hour',
        'Read labels critically — serving size, added sugar, sodium, and ingredient order matter most',
    ], RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate([
        'What is PDCAAS and why does it matter for plant-based eaters?',
        'Calculate the TDEE for a 30-year-old male, 75kg, 175cm, who trains 4 days/week.',
        'Explain glycogen depletion ("bonking") and how carbohydrate loading prevents it.',
        'Why is dietary fat below 15% of calories harmful for athletes?',
        'What is the difference between Glycaemic Index and Glycaemic Load? Give an example where GI is misleading.',
    ], 1):
        e.append(Paragraph(f'{i}. {q}', S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════
# MODULE 5: Recovery & Sleep Science (35 min)
# ═══════════════════════════════════════════
def gen_b1_m5():
    fname = os.path.join(OUT,'cs_b1_mod5_recovery_sleep.pdf')
    doc = SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e = []
    e += cover('Fitness Foundations Certificate',5,'Recovery & Sleep Science',35,'CS_B1')

    e.append(sd('SECTION 1: The Recovery Equation'))
    e.append(sp(6))
    e.append(h1('Adaptation Happens During Recovery, Not Training'))
    e.append(p('A common misconception is that training builds muscle and fitness. It doesn\'t — '
               'training is a catabolic (breaking down) stimulus. Exercise creates damage and '
               'metabolic fatigue. It is the recovery period between sessions that produces the '
               'anabolic response (building up), resulting in a stronger, fitter, larger muscle.'))
    e.append(p('This is the fundamental principle underlying periodisation: training stress → '
               'fatigue → recovery → supercompensation. If recovery is insufficient, fatigue '
               'accumulates and performance declines — the definition of overtraining syndrome (OTS).'))
    e.append(ib('The Recovery Equation',[
        'Adaptation = Training Stress + Recovery',
        'Too little stress → no adaptation (undertraining)',
        'Too much stress → no recovery time → overtraining',
        'The "optimal" zone is where progress consistently occurs',
        'Recovery capacity varies by individual: genetics, sleep quality, nutrition, age, life stress',
    ], RFC_DARK))
    e.append(sp(8))

    e.append(sd('SECTION 2: Physiological Muscle Repair Process'))
    e.append(sp(6))
    e.append(h1('What Happens After a Training Session'))
    e.append(p('In the hours and days after resistance training, a cascade of events rebuilds '
               'damaged muscle fibres stronger than before. Understanding this timeline helps '
               'determine optimal training frequency and recovery nutrition strategies.'))
    e.append(mt(
        ['Time Post-Exercise','Process','Nutritional Support'],
        [['0–2 hours','Acute inflammation: neutrophils arrive; inflammatory cytokines (IL-6, TNF-α) released','Post-workout protein 20–40g; rehydrate'],
         ['2–24 hours','Macrophage infiltration; satellite cell activation; MPS elevated','High protein diet; sleep (GH pulse)'],
         ['24–48 hours','Protein synthesis peaks (may take 48–72h for large compound lifts)','Continue 1.6–2.2g protein/kg; sleep; light activity'],
         ['48–72 hours','Collagen synthesis in tendons/connective tissue','Vitamin C for collagen synthesis; omega-3'],
         ['72h+','Return to baseline for most muscle groups; tendons may still be remodelling','Continue nutrition; progressive training stimulus'],
        ]
    ))
    e.append(sp(8))
    e.append(h2('Delayed-Onset Muscle Soreness (DOMS)'))
    e.append(p('DOMS is the muscular pain and stiffness experienced 24–72 hours after unfamiliar '
               'or intense exercise, peaking at ~48 hours. It results from microscopic damage '
               'to muscle fibres and the inflammatory response — not from lactic acid (which '
               'clears within 30–60 minutes post-exercise).'))
    e.append(p('<b>DOMS triggers:</b> Eccentric muscle actions, novel exercises, high volume, '
               'high stretch under load (deep ROM). Squats cause more DOMS than leg press partly '
               'due to greater eccentric demand at the bottom of the movement.'))
    for it in ['DOMS does not accurately reflect training quality — experienced athletes experience less DOMS from the same stimulus',
               'Training through moderate DOMS is safe and may accelerate recovery via blood flow',
               'Analgesic interventions (ice bath, NSAIDs) may blunt the inflammatory signal and impair long-term adaptation',
               'The "repeated bout effect" — after 2–3 sessions, DOMS from the same exercise is dramatically reduced']:
        e.append(bl(it))
    e.append(sp())

    e.append(sd('SECTION 3: Sleep — The Most Powerful Recovery Tool'))
    e.append(sp(6))
    e.append(h1('Sleep Architecture and Athletic Performance'))
    e.append(p('Sleep is the single most powerful recovery and adaptation tool available. '
               'During sleep, the body releases its highest pulse of growth hormone (GH), '
               'consolidates motor memory, repairs tissue, modulates immune function, and '
               'resets the hypothalamic-pituitary-adrenal (HPA) axis that governs stress '
               'and cortisol levels.'))
    e.append(h2('Sleep Stages'))
    e.append(mt(
        ['Stage','Type','Duration','Key Functions'],
        [['N1 (NREM)','Light sleep','5–10 min','Transition; easily awakened'],
         ['N2 (NREM)','Confirmed sleep','20–30 min','Sleep spindles; memory consolidation begins; ~50% of total sleep'],
         ['N3 (NREM)','Deep / Slow wave','20–40 min','GH release; physical repair; immune function; hardest to wake from'],
         ['REM','Rapid Eye Movement','10–60 min (increases toward morning)','Emotional regulation; motor learning; creativity; dreams'],
        ]
    ))
    e.append(sp(8))
    e.append(p('<b>Cycling:</b> A complete sleep cycle takes ~90 minutes and repeats 4–6 times. '
               'Deep N3 sleep dominates early cycles (first half of night); REM dominates later '
               '(second half). Sleeping 6 instead of 8 hours disproportionately cuts REM sleep '
               'in the second half of the night.'))
    e.append(p('<b>Growth Hormone pulse:</b> The largest GH secretion occurs during the first '
               'N3 episode (~1 hour after sleep onset). GH drives protein synthesis, fat '
               'mobilisation, and tissue repair. Alcohol, high-GI carbohydrates before bed, and '
               'cortisol all suppress this GH pulse.'))
    e.append(h2('Sleep and Athletic Performance — The Research'))
    e.append(p('Studies on sleep extension in athletes show dramatic performance improvements '
               'even in well-rested individuals:'))
    e.append(mt(
        ['Research Finding','Source'],
        [['Basketball players sleeping 10h/night showed 5% sprint speed improvement + 9% improved free throw accuracy','Mah et al., Stanford, 2011'],
         ['Sleep restriction to 6h/night for 2 weeks = same cognitive impairment as 24-48h total deprivation','Van Dongen et al., 2003'],
         ['Injury risk doubles for athletes sleeping <8h vs ≥8h/night in a season','Milewski et al., 2014'],
         ['1 night of poor sleep increases cortisol by 15–20% the next day, blunting testosterone response','Leproult & Van Cauter, 2011'],
         ['Testosterone decreases 10–15% after one week of 5h sleep vs 8h','Leproult & Van Cauter, 2011'],
        ]
    ))
    e.append(sp(8))
    e.append(ib('Sleep Optimisation Protocol',[
        'Target 7–9 hours for general adults; 8–10 hours for elite athletes in heavy training',
        'Consistent bed/wake time: even weekends — circadian rhythm is anchored to consistency',
        'Temperature: sleep in 18–21°C room (cooler = deeper sleep)',
        'Light: eliminate blue light 60–90 minutes before bed (use blue-light glasses or Night Shift)',
        'Avoid alcohol within 3 hours of sleep — increases N1, suppresses N3 and REM',
        'Magnesium glycinate (300–400mg) before bed may improve sleep quality via GABA modulation',
        'Napping: 20-minute "power nap" restores alertness without sleep inertia; avoid >2pm if sleep is challenging',
    ], RFC_BLUE))
    e.append(sp(8))

    e.append(sd('SECTION 4: Active Recovery Strategies'))
    e.append(sp(6))
    e.append(h1('Foam Rolling and Myofascial Release'))
    e.append(p('Self-myofascial release (SMR) using foam rollers, massage balls, and sticks '
               'applies pressure to soft tissue, temporarily increasing tissue compliance, '
               'blood flow, and ROM. It does not "break up" knots or scar tissue in the '
               'traditional sense — it works primarily through neurological pathways (Golgi '
               'tendon organ stimulation reducing muscle tone).'))
    e.append(p('<b>Evidence summary:</b>'))
    for it in ['30–60 seconds per muscle group with moderate pressure sufficient to feel sensation but not unbearable pain',
               'Increases ROM acutely (5–15%) without impairing force production (unlike static stretching)',
               'Post-workout: reduces DOMS perception when combined with stretching',
               'Best used before training on tight areas and after training for recovery',
               'Blood flow restriction (BFR) light exercise on recovery days accelerates metabolite clearance']:
        e.append(bl(it))
    e.append(h2('Active Recovery Exercise'))
    e.append(p('Light aerobic activity on rest days (20–30 minutes at 40–60% max HR) significantly '
               'accelerates lactate clearance, maintains neural sensitivity, increases blood flow '
               'to repairing tissue, and combats stiffness — while avoiding additional training stress.'))
    e.append(mt(
        ['Recovery Activity','Intensity','Duration','Benefits'],
        [['Walking','Very light','20–45 min','NEAT, blood flow, mental recovery'],
         ['Swimming','Light (60% HRmax)','20–30 min','Full-body, joint-decompressing'],
         ['Yoga/stretching','Light','30–60 min','Flexibility, parasympathetic activation'],
         ['Light cycling','40–55% HRmax','20–30 min','Lower-body circulation, low impact'],
         ['Mobility drills','N/A','15–20 min','Joint ROM maintenance, neuromuscular'],
        ]
    ))
    e.append(sp(8))

    e.append(sd('SECTION 5: Cortisol, Stress, and Recovery'))
    e.append(sp(6))
    e.append(h1('The Cortisol-Testosterone Seesaw'))
    e.append(p('Cortisol is the primary catabolic hormone, released by the adrenal cortex in '
               'response to physical and psychological stress. In the short term, cortisol is '
               'adaptive — it mobilises energy stores and modulates inflammation. '
               'Chronically elevated cortisol, however, is profoundly anti-anabolic:'))
    for it in ['Suppresses testosterone and IGF-1 (anabolic hormones)',
               'Promotes muscle protein breakdown (gluconeogenesis from amino acids)',
               'Impairs sleep quality, creating a feedback loop of poor recovery',
               'Reduces immune function, increasing upper respiratory illness risk',
               'Increases appetite for high-calorie foods (via appetite-regulating hormones)']:
        e.append(bl(it))
    e.append(p('<b>Training dose:</b> Exercise sessions under 60–75 minutes generally maintain '
               'a favourable testosterone:cortisol (T:C) ratio. Sessions exceeding 90 minutes '
               'at high intensity often show a declining T:C ratio. This is a key reason why '
               '"more" training is not always "better."'))
    e.append(h2('Stress Management for Recovery'))
    for it in ['Meditation / breathwork: activates parasympathetic nervous system, reducing HPA axis activity',
               'Perceived control: planning and periodisation reduce psychological uncertainty stress',
               'Social recovery: enjoyable social activities lower cortisol more than passive watching TV',
               'Nature exposure: 20 minutes in natural environments measurably reduces salivary cortisol']:
        e.append(bl(it))
    e.append(sp())

    e.append(sd('SECTION 6: Cold Therapy — When and Why'))
    e.append(sp(6))
    e.append(h1('Cold Water Immersion (CWI) and Ice Baths'))
    e.append(p('Cold water immersion (8–15°C, 10–20 minutes) is widely used for recovery '
               'in professional sport. It works by:'))
    for it in ['Vasoconstriction reducing metabolic by-product accumulation in tissue',
               'Reducing perceived pain and soreness (analgesic effect)',
               'Decreasing muscle temperature, slowing enzymatic degradation processes',
               'Stimulating norepinephrine release (3–5× baseline) — improving mood and alertness']:
        e.append(bl(it))
    e.append(p('<b>The hypertrophy trade-off:</b> Cold water immersion acutely blunts the '
               'inflammatory signalling (IL-6, mTOR) that drives hypertrophy. Studies show '
               'that regular post-workout CWI over 10–12 weeks reduces strength and hypertrophy '
               'gains compared to active recovery. Therefore:'))
    e.append(mt(
        ['Scenario','CWI Appropriate?','Reason'],
        [['Competition, back-to-back games','YES','Recovery speed > adaptation'],
         ['Mid-hypertrophy block training','NO','Blunts anabolic signalling'],
         ['Endurance event recovery','YES','Reduces systemic inflammation quickly'],
         ['Team sport in-season','YES','Performance maintained throughout season'],
         ['Off-season hypertrophy phase','NO','Maximise adaptation'],
        ]
    ))
    e.append(sp(8))
    e.append(ib('Module 5 Key Takeaways',[
        'Adaptation occurs during recovery — training is the stimulus; rest is when you actually grow',
        'Sleep is the most powerful recovery tool: 8+ hours for athletes; prioritise N3 deep sleep for GH release',
        'DOMS peaks at 48h and is caused by eccentric muscle damage, not lactic acid',
        'Active recovery (light cardio, walking, swimming) accelerates waste removal and reduces stiffness',
        'Chronic cortisol elevation suppresses testosterone and impairs muscle protein synthesis — manage life stress',
        'Cold water immersion aids performance recovery but may blunt hypertrophy — use contextually',
    ], RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate([
        'Describe the supercompensation model. What happens if the next training session is timed during the fatigue phase?',
        'Explain the difference between N3 and REM sleep in terms of their athletic recovery functions.',
        'Why does alcohol before bed impair recovery, and which hormone does it primarily suppress?',
        'When is cold water immersion appropriate, and when should it be avoided? Explain the mechanistic reason.',
        'What is the testosterone:cortisol ratio, and why is session duration relevant to it?',
    ], 1):
        e.append(Paragraph(f'{i}. {q}', S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

gen_b1_m4()
gen_b1_m5()
print('M4 and M5 done.')
