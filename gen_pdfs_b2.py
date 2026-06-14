#!/usr/bin/env python3
"""Generate all 8 PDFs for cs_b2 — Nutrition & Healthy Eating Certificate"""
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
RFC_GREEN=colors.HexColor('#138808'); RFC_ORANGE=colors.HexColor('#FF6600')
RFC_WHITE=colors.white; RFC_LIGHT=colors.HexColor('#F5F5F5'); RFC_GRAY=colors.HexColor('#555555')

S={'h1':ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=22,textColor=RFC_DARK,leading=28,spaceBefore=18,spaceAfter=10),
   'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=17,textColor=RFC_BLUE,leading=22,spaceBefore=14,spaceAfter=7),
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
    bar.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_GREEN),('LINEBELOW',(0,0),(-1,-1),2,RFC_GOLD)]))
    e.append(Spacer(1,8*mm));e.append(bar);e.append(Spacer(1,18*mm))
    logo=Table([['ROYAL FITNESS CLUB']],colWidths=[W-40*mm])
    logo.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_DARK),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),28),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),18),('BOTTOMPADDING',(0,0),(-1,-1),18)]))
    e.append(logo);e.append(Spacer(1,6*mm))
    e.append(HRFlowable(width='100%',thickness=3,color=RFC_GOLD));e.append(Spacer(1,10*mm))
    ct=Table([['Nutrition & Healthy Eating Certificate']],colWidths=[W-40*mm])
    ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_GREEN),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),15),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    e.append(ct);e.append(Spacer(1,14*mm))
    badge=Table([[f'MODULE {mod_num}']],colWidths=[50*mm])
    badge.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_RED),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),13),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    e.append(badge);e.append(Spacer(1,8*mm))
    e.append(Paragraph(mod_title,S['h1']));e.append(Spacer(1,6*mm))
    meta=Table([['Duration',f'{duration} minutes'],['Course Code','CS_B2'],['Level','Beginner'],['Format','Study Guide PDF']],
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

def sd(t,col=RFC_RED):
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

def mt(headers,rows):
    n=len(headers);cw=(W-40*mm)/n;data=[headers]+rows
    t=Table(data,colWidths=[cw]*n)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),RFC_GREEN),('TEXTCOLOR',(0,0),(-1,0),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),('ROWBACKGROUNDS',(0,1),(-1,-1),[RFC_LIGHT,RFC_WHITE]),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),('BOX',(0,0),(-1,-1),1,RFC_GREEN)]))
    return t

def p(t): return Paragraph(t,S['body'])
def h1(t): return Paragraph(t,S['h1'])
def h2(t): return Paragraph(t,S['h2'])
def bl(t): return Paragraph(f'• {t}',S['bullet'])
def sp(n=8): return Spacer(1,n)

# ═══════════════════════════════════
# M1: Macronutrients Deep Dive (60min)
# ═══════════════════════════════════
def gen_b2_m1():
    fname=os.path.join(OUT,'cs_b2_mod1_macronutrients_deep.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(1,'Macronutrients Deep Dive',60)

    e.append(sd('SECTION 1: The Role of Macronutrients in Human Physiology'))
    e.append(sp(6)); e.append(h1('Beyond Calories — What Macros Actually Do'))
    e.append(p('Macronutrients (protein, carbohydrates, and fats) are the three categories of '
               'large molecules that provide energy and structural material to the human body. '
               'While calories determine body weight over time, macronutrient composition '
               'determines body composition — the ratio of muscle to fat — and profoundly '
               'influences hormones, inflammation, satiety, cognitive function, and athletic '
               'performance.'))
    e.append(p('A calorie is not just a calorie in terms of physiological effects. 500 kcal '
               'from chicken breast triggers different hormonal responses, satiety signals, '
               'and metabolic fates than 500 kcal from refined sugar — even though both are '
               '500 kcal.'))
    e.append(mt(['Macronutrient','Energy Density','Primary Functions','Dietary Sources'],
        [['Protein','4 kcal/g','Muscle tissue, enzymes, hormones, antibodies, transport proteins','Chicken, fish, eggs, dairy, legumes, soy'],
         ['Carbohydrates','4 kcal/g','Primary fuel for CNS and high-intensity exercise, glycogen storage, gut microbiome via fibre','Rice, wheat, oats, fruits, vegetables, pulses'],
         ['Fats','9 kcal/g','Hormones, cell membranes, fat-soluble vitamins, brain, long-duration energy','Oils, nuts, seeds, fatty fish, avocado, dairy'],
         ['Alcohol (reference)','7 kcal/g','No nutritional function; suppresses fat oxidation','Beer, wine, spirits — to be minimised'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 2: Protein — A 360° View'))
    e.append(sp(6)); e.append(h1('The Science of Dietary Protein'))
    e.append(h2('Amino Acid Profiles and Essential vs Non-Essential'))
    e.append(p('Proteins are polymers of 20 amino acids connected by peptide bonds. Of the 20, '
               '9 are classified as <b>essential</b> (must be obtained from diet; cannot be '
               'synthesised): histidine, isoleucine, leucine, lysine, methionine, phenylalanine, '
               'threonine, tryptophan, and valine.'))
    e.append(p('The remaining 11 are <b>conditionally essential</b> (normally synthesisable '
               'but required from diet under illness, injury, or rapid growth): arginine, '
               'cysteine, glutamine, glycine, proline, serine, tyrosine, asparagine, aspartate, '
               'glutamate, alanine.'))
    e.append(h2('Complete vs Incomplete Proteins'))
    e.append(mt(['Category','Definition','Examples','Limitation for Vegans'],
        [['Complete protein','Contains all 9 essential amino acids in adequate ratios','Eggs, dairy, meat, fish, soy, quinoa','Most animal proteins are complete'],
         ['Incomplete protein','Missing or low in one or more EAAs','Most plant proteins (grains, legumes, nuts)','Complementary combining needed'],
         ['Complementary pairing','Two incomplete proteins together = complete EAA profile','Rice + lentils (dal+rice), corn + beans','Classic solution in Indian/Latin American diets'],
        ]))
    e.append(sp(8))
    e.append(h2('Leucine: The Anabolic Trigger'))
    e.append(p('Among the 20 amino acids, leucine occupies a unique position: it directly '
               'activates mTORC1, the master regulator of protein synthesis. A minimum '
               'leucine threshold of approximately 2–3g per meal is required to maximally '
               'stimulate muscle protein synthesis (MPS).'))
    e.append(mt(['Food','Protein per 100g','Leucine per 100g','Serves to Achieve 2g Leucine'],
        [['Chicken breast','31g','2.5g','80g chicken'],
         ['Whole eggs','13g','1.1g','~4 eggs (200g)'],
         ['Whey protein powder','80g','9g','25g powder'],
         ['Lentils (cooked)','9g','0.7g','285g lentils'],
         ['Tofu (firm)','8g','0.6g','333g tofu'],
         ['Paneer','18g','1.4g','143g paneer'],
        ]))
    e.append(sp(8))
    e.append(p('This data explains why a 30g scoop of whey efficiently triggers MPS, while '
               'the same amount of a plant source may not — the leucine density differs. '
               'Vegans should target the higher end of protein intake (2.0–2.4g/kg) to '
               'compensate for lower leucine density.'))
    e.append(h2('Protein Metabolism: Digestion to Deposition'))
    for it in ['Stomach: HCl denatures protein; pepsin hydrolyses peptide bonds',
               'Small intestine: pancreatic proteases (trypsin, chymotrypsin) complete breakdown to amino acids and small peptides',
               'Absorption: amino acids cross intestinal epithelium via specific transporters; enter portal circulation',
               'Liver: regulates amino acid release to peripheral tissues; urea cycle removes excess nitrogen',
               'Muscle: uptake driven by insulin and exercise; mTORC1 activation → ribosomal activity → protein synthesis']:
        e.append(bl(it))
    e.append(h2('Protein Timing Revisited'))
    e.append(mt(['Meal','Protein Target','Food Examples','Rationale'],
        [['Breakfast','25–35g','3 eggs + 200g Greek yoghurt + 30g whey in smoothie','Breaks overnight fast; MPS stimulus after 6–8h sleep'],
         ['Lunch','25–40g','200g chicken / fish + legume side','Mid-day MPS stimulus; leucine threshold met'],
         ['Pre-workout (if 2h+ before)','20–30g','Paneer bowl, Greek yoghurt + banana','Amino acids circulating during training'],
         ['Post-workout','25–40g','Whey shake / chicken / eggs within 2h','Maximise post-exercise MPS window'],
         ['Dinner','25–40g','Fish, chicken, dal + rice, tofu curry','Complete EAA profile at final meal'],
         ['Pre-sleep','30–40g casein','Cottage cheese, casein shake','Slow-digesting; sustains MPS for 7–9h of sleep'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 3: Carbohydrates — Structure, Function, and Optimisation'))
    e.append(sp(6)); e.append(h1('Carbohydrates: More Than Just Energy'))
    e.append(h2('Carbohydrate Digestion and Glycaemic Response'))
    e.append(p('All digestible carbohydrates are ultimately converted to monosaccharides '
               '(primarily glucose) before absorption. Glucose enters the bloodstream, '
               'triggering insulin release from pancreatic beta cells. Insulin drives glucose '
               'into muscle (for glycogen synthesis), liver (glycogen), and adipose tissue (fat).'))
    e.append(p('The rate of this process determines the glycaemic response — fast digestion '
               '= rapid glucose spike = rapid insulin spike = subsequent glucose dip '
               '(potential energy crash). Slow digestion = sustained glucose = sustained '
               'energy without excessive insulin spikes.'))
    e.append(h2('Dietary Fibre — The Overlooked Powerhouse'))
    e.append(p('Dietary fibre is the non-digestible carbohydrate component of plant foods. '
               'Despite not contributing energy directly, fibre is arguably the most important '
               'carbohydrate for long-term health:'))
    e.append(mt(['Fibre Type','Source','Health Effect'],
        [['Soluble (viscous)','Oats (beta-glucan), legumes, psyllium, fruits','Lowers LDL cholesterol; slows glucose absorption; prebiotic'],
         ['Insoluble','Wheat bran, vegetables, whole grains','Increases stool bulk; reduces colon transit time; reduces colorectal cancer risk'],
         ['Resistant starch','Cooked-cooled rice/potato, unripe banana, legumes','Fermented by gut bacteria to butyrate; prebiotic; glucose blunting'],
         ['Prebiotic fibre (FOS, inulin)','Garlic, onion, chicory, asparagus, Jerusalem artichoke','Feeds beneficial Bifidobacterium; gut microbiome diversity'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Target fibre intake:</b> 25–38g/day (women at the lower end; men at the '
               'higher end). Most Indians eat 15–20g/day — a significant deficit. Dal (lentils), '
               'whole wheat roti, and sabzi (vegetables) are culturally accessible ways to '
               'reach the target.'))
    e.append(h2('Carbohydrate Loading and Periodisation'))
    e.append(p('Strategic carbohydrate manipulation around training sessions can optimise '
               'performance and body composition simultaneously:'))
    e.append(mt(['Strategy','When','Carb Amount','Goal'],
        [['Carb loading','24–72h pre-endurance event (>90min)','8–12g/kg BW/day','Maximise glycogen stores'],
         ['High-carb training day','Before intense sessions','3–5g/kg','Performance; glycogen full'],
         ['Low-carb training day','Before low-intensity / rest day','1–2g/kg','Enhance fat oxidation adaptation'],
         ['Intra-workout carbs','During sessions >60 minutes','30–60g/hour','Maintain blood glucose'],
         ['Post-workout carbs','Within 30–60min (after protein)','0.8–1.2g/kg','Rapid glycogen resynthesis'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 4: Fats — The Complete Guide'))
    e.append(sp(6)); e.append(h1('Fat Is Not the Enemy'))
    e.append(h2('Essential Fatty Acids'))
    e.append(p('Two polyunsaturated fatty acids cannot be synthesised by the human body and '
               'must be obtained from diet: linoleic acid (omega-6) and alpha-linolenic acid '
               '(ALA, omega-3). They are the "parents" of longer-chain derivatives critical '
               'for physiology:'))
    e.append(mt(['Parent EFA','Derivatives','Sources','Primary Role'],
        [['Linoleic acid (LA) — omega-6','Arachidonic acid (AA)','Sunflower, corn, soybean oil','Eicosanoid precursors — pro-inflammatory signalling (in excess)'],
         ['Alpha-linolenic acid (ALA) — omega-3','EPA → DHA (conversion rate <10%)','Flaxseed, chia, walnuts','Anti-inflammatory; brain DHA requires direct EPA/DHA from fish/algae'],
        ]))
    e.append(sp(8))
    e.append(p('<b>The omega-6:omega-3 ratio problem:</b> Modern diets have omega-6:omega-3 ratios '
               'of 15:1 to 20:1 (vs ancestral ~4:1). This chronic excess of omega-6 drives '
               'systemic low-grade inflammation linked to cardiovascular disease, obesity, '
               'depression, and inflammatory conditions. The solution: reduce refined seed oils '
               '(sunflower, soybean, corn) and increase EPA+DHA from fatty fish, fish oil, or '
               'algae oil supplements.'))
    e.append(h2('Cholesterol — Separating Science from Myth'))
    e.append(p('Dietary cholesterol (found only in animal foods — eggs, shellfish, organ meats) '
               'has a minimal effect on blood cholesterol in most people because the liver '
               'compensates by producing less endogenous cholesterol when dietary intake increases. '
               '"Cholesterol responders" (25% of population) do see modest LDL increases with '
               'high dietary cholesterol, but context matters — egg consumption within a '
               'calorie-controlled diet does not increase cardiovascular risk in most studies.'))
    e.append(mt(['Cholesterol Type','What it Is','Target','Influence'],
        [['LDL-C (LDL cholesterol)','Cholesterol carried by LDL particles','<100 mg/dL optimal; <70 for high risk','Saturated fat, trans fat increase LDL; MUFAs lower it'],
         ['HDL-C (HDL cholesterol)','Cholesterol carried by HDL (reverse transport to liver)','>60 mg/dL protective','Exercise, omega-3, moderate alcohol, mono/polyunsaturated fats increase HDL'],
         ['Triglycerides','Circulating fat in blood','<150 mg/dL','Excess refined carbs, sugar, alcohol raise TG; omega-3, exercise lower TG'],
         ['LDL particle count (LDL-P)','More specific CVD risk marker than LDL-C','Test requires NMR lipoprofile','Small, dense LDL particles more atherogenic than large, buoyant'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 5: Calculating and Tracking Macros'))
    e.append(sp(6)); e.append(h1('Practical Macro Setup'))
    e.append(p('Setting up macros follows a hierarchy: total calories first, then protein, '
               'then fat (minimum for hormones), then fill remaining calories with carbohydrate.'))
    e.append(h2('Step-by-Step Macro Calculation Example'))
    e.append(p('Example: 28-year-old female, 60kg, moderately active (1.55 multiplier), goal: body recomposition'))
    e.append(mt(['Step','Calculation','Result'],
        [['1. BMR (Mifflin-St Jeor)','(10×60)+(6.25×163)−(5×28)−161 = 1380 kcal','1380 kcal'],
         ['2. TDEE','1380 × 1.55','2139 kcal'],
         ['3. Caloric target (250 kcal deficit)','2139 − 250','1889 kcal'],
         ['4. Protein (2.0g/kg)','2.0 × 60kg = 120g × 4 kcal','480 kcal'],
         ['5. Fat (25% of TDEE)','0.25 × 1889 ÷ 9 kcal/g','52g fat = 472 kcal'],
         ['6. Carbohydrates (remaining)','1889 − 480 − 472 = 937 kcal ÷ 4','234g carbs'],
         ['Summary','1889 kcal | 120P / 234C / 52F','Balanced recomp macro set'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 1 (CS_B2) Key Takeaways',[
        'Macros provide energy but also structural, hormonal, and regulatory functions beyond calorie yield',
        'Leucine threshold ~2–3g per meal required to maximally activate MPS via mTORC1',
        'Fibre (25–38g/day) improves glycaemic control, gut microbiome, satiety, and cardiovascular health',
        'Omega-6:omega-3 ratio matters — reduce seed oils, increase EPA+DHA from fish/algae',
        'Macro calculation: calories → protein (2g/kg) → fat (min 15–25%) → fill with carbs',
        'Carbohydrate periodisation (high on training days, lower on rest days) optimises recomposition',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['What is the leucine threshold and why does it make plant proteins potentially inferior for MPS?',
        'Explain resistant starch: how is it formed, and what are its health benefits?',
        'Calculate macros for a 75kg male seeking muscle gain at 2800 kcal total.',
        'Why is the omega-6:omega-3 ratio more important than total fat intake for inflammation?',
        'Distinguish between LDL-C and LDL particle count (LDL-P) as cardiovascular risk markers.',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════
# M2: Micronutrients — Unsung Heroes (55min)
# ═══════════════════════════════════
def gen_b2_m2():
    fname=os.path.join(OUT,'cs_b2_mod2_micronutrients.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(2,'Micronutrients — The Unsung Heroes',55)

    e.append(sd('SECTION 1: Why Micronutrients Are Critical for Athletes'))
    e.append(sp(6));e.append(h1('Vitamins and Minerals in Athletic Performance'))
    e.append(p('While macronutrients provide energy and structure, micronutrients (vitamins and '
               'minerals) are the molecular tools that enable every metabolic reaction in the body. '
               'Without adequate micronutrients, macronutrient metabolism is impaired — like '
               'having excellent fuel in a car with a malfunctioning engine.'))
    e.append(p('Athletes have higher micronutrient requirements than sedentary individuals because '
               'exercise increases metabolic rate, sweat losses, oxidative stress, tissue turnover, '
               'and demand for energy metabolism co-factors.'))
    e.append(mt(['Micronutrient','RDA (general)','Sports Relevance','Best Sources'],
        [['Vitamin D3','600–2000 IU (often more needed)','Testosterone, bone health, muscle function, immune','Sunlight, fatty fish, fortified dairy, D3 supplement'],
         ['Magnesium','310–420 mg','ATP synthesis, muscle contraction, sleep (GABA), >300 enzymes','Pumpkin seeds, spinach, dark chocolate, legumes, nuts'],
         ['Iron','18mg (F) / 8mg (M)','Haemoglobin, oxygen transport, endurance','Red meat, organ meat, spinach + vit C, lentils (non-haem)'],
         ['Zinc','8–11mg','Testosterone synthesis, immune, wound healing, taste/smell','Oysters, red meat, pumpkin seeds, legumes, hemp seeds'],
         ['B12','2.4 mcg','Nerve myelin, DNA synthesis, red blood cells, energy metabolism','Animal products; supplement essential for vegans'],
         ['Calcium','1000–1200 mg','Bone density, muscle contraction, nerve signalling','Dairy, fortified plant milk, ragi (finger millet), sesame'],
         ['Vitamin C','75–90mg (higher for athletes)','Collagen synthesis, antioxidant, iron absorption, immune','Citrus, guava, bell peppers, amla (Indian gooseberry)'],
         ['B-vitamins (B1,B2,B3,B6)','Varied','Co-factors in glycolysis and Krebs cycle — energy metabolism','Whole grains, legumes, meat, dairy, eggs'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 2: Vitamin D — The Hormone Masquerading as a Vitamin'))
    e.append(sp(6));e.append(h1('Vitamin D — Far More Than Bone Health'))
    e.append(p('Vitamin D is technically a prohormone, not a vitamin — the body synthesises it '
               'from cholesterol in the skin upon UVB exposure. It is converted to its active '
               'form (calcitriol / 1,25-dihydroxyvitamin D) by the liver and kidneys.'))
    e.append(p('Vitamin D receptors (VDRs) are found in virtually every cell in the body — '
               'muscle, brain, immune cells, heart, reproductive organs, bone. This explains '
               'its broad physiological effects beyond calcium metabolism.'))
    for it in ['Bone health: regulates calcium and phosphate absorption and bone mineralisation',
               'Muscle function: VDR in muscle cells — low D3 associated with reduced muscle force and increased injury risk',
               'Testosterone: studies show inverse correlation between D3 deficiency and testosterone levels',
               'Immune modulation: reduces autoimmune disease risk; critical for innate immunity (COVID outcomes correlated)',
               'Mental health: low D3 associated with depression, seasonal affective disorder (SAD)',
               'Insulin sensitivity: D3 deficiency impairs insulin signalling']:
        e.append(bl(it))
    e.append(p('<b>Deficiency in India:</b> Paradoxically, despite abundant sunshine, D3 deficiency '
               'affects 70–90% of Indians. Reasons: indoor work, skin melanin (reduces UV synthesis), '
               'limited D3-rich foods in traditional vegetarian diets, cultural practices (covered '
               'clothing, avoiding midday sun). Testing (25-OH-D blood test) is recommended.'))
    e.append(mt(['D3 Status','Blood Level (25-OH-D)','Clinical Significance'],
        [['Deficient','<20 ng/mL (<50 nmol/L)','High risk: osteoporosis, immune dysfunction, muscle weakness'],
         ['Insufficient','20–29 ng/mL','Suboptimal; many biological functions impaired'],
         ['Optimal','40–60 ng/mL','Target range for athletes and health-conscious individuals'],
         ['Toxic (rare)','>150 ng/mL','Hypercalcaemia; requires extremely high supplementation (>10,000 IU/day)'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Supplementation:</b> Most adults in India benefit from 2000–4000 IU Vitamin D3 '
               'daily year-round. Take with K2 (100–200mcg MK-7) to direct calcium to bones '
               '(not arteries). Fat-soluble — take with a fatty meal for optimal absorption.'))
    e.append(sp())

    e.append(sd('SECTION 3: Iron — The Oxygen Carrier'))
    e.append(sp(6));e.append(h1('Iron Deficiency — The Silent Performance Killer'))
    e.append(p('Iron is the central atom of haemoglobin (in red blood cells) and myoglobin '
               '(in muscle cells) — the proteins that carry and store oxygen. Iron deficiency '
               'impairs oxygen delivery to working muscles, reducing VO2 max, endurance capacity, '
               'and cognitive function.'))
    e.append(h2('Haem vs Non-Haem Iron'))
    e.append(mt(['Type','Sources','Absorption Rate','Enhancement/Inhibition'],
        [['Haem iron','Red meat, organ meat, poultry, fish','15–35% absorbed','Not affected by phytates; best bioavailable form'],
         ['Non-haem iron','Lentils, spinach, fortified cereals, tofu, nuts','2–20% absorbed','Enhanced by vitamin C (+2–4×); inhibited by calcium, tea polyphenols, phytates'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Practical tip for vegetarians:</b> Consume non-haem iron sources with vitamin C '
               '(lemon juice, amla, guava, bell peppers). Avoid tea/coffee within 1 hour of '
               'iron-rich meals (tannins inhibit non-haem absorption by up to 60%).'))
    e.append(p('<b>Sports anaemia:</b> Endurance athletes (especially runners) face higher iron '
               'losses through haemolysis (foot-strike destruction of RBCs), sweat, and micro-GI '
               'bleeding. Female endurance athletes are particularly at risk — menstrual losses '
               'compound dietary shortfall.'))
    e.append(p('<b>Iron toxicity:</b> Iron is pro-oxidant in excess — drives free radical '
               'production. Do NOT supplement iron without confirmed deficiency (serum ferritin '
               '<30 ng/mL in athletes; <20 ng/mL in sedentary). Excess iron increases '
               'cardiovascular disease risk.'))
    e.append(sp())

    e.append(sd('SECTION 4: Magnesium — The Macro-Mineral You\'re Probably Deficient In'))
    e.append(sp(6));e.append(h1('Magnesium — 300+ Enzymes, One Mineral'))
    e.append(p('Magnesium is the fourth most abundant mineral in the human body and co-factor '
               'for over 300 enzymatic reactions, including all ATP-generating reactions. '
               'Without magnesium, ATP cannot be utilised — every muscle contraction, nerve '
               'impulse, and DNA synthesis requires Mg²⁺-ATP.'))
    for it in ['Energy metabolism: co-factor for all ATP synthesis (glycolysis, Krebs, ETC)',
               'Muscle function: required for calcium to be pumped out of muscle post-contraction (relaxation)',
               'Protein synthesis: ribosomal activity requires magnesium',
               'Sleep: activates GABA receptors — the brain\'s primary inhibitory neurotransmitter',
               'Blood pressure: relaxes vascular smooth muscle; deficiency is a major driver of hypertension',
               'Insulin sensitivity: magnesium deficiency impairs glucose transporter function (GLUT4)']:
        e.append(bl(it))
    e.append(p('<b>Deficiency prevalence:</b> 60–70% of people in developed countries consume '
               'below the RDA. Soil depletion, refined food consumption, high sugar/alcohol '
               'intake (all increase magnesium excretion), and gut absorption issues contribute.'))
    e.append(mt(['Form','Bioavailability','Best For','Side Effects'],
        [['Magnesium glycinate','High — gentle','Sleep, anxiety, general use','Minimal GI effects'],
         ['Magnesium citrate','Good','Constipation, general deficiency','Loose stools at high dose'],
         ['Magnesium malate','Good','Energy, fibromyalgia','Mild'],
         ['Magnesium oxide','Low (~4%)','NOT recommended','High GI issues'],
         ['Magnesium L-threonate','High (brain crossing)','Cognitive function, memory','Expensive'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Food sources:</b> Pumpkin seeds (156mg/28g), dark chocolate (50mg/28g), '
               'spinach (78mg/half cup cooked), almonds (77mg/28g), black beans (60mg/half cup), '
               'avocado (58mg per avocado), salmon (26mg/85g).'))
    e.append(sp())

    e.append(sd('SECTION 5: Antioxidants — Managing Oxidative Stress'))
    e.append(sp(6));e.append(h1('Free Radicals, Antioxidants, and the Exercise Paradox'))
    e.append(p('Exercise generates reactive oxygen species (ROS) — chemically reactive molecules '
               'with unpaired electrons that damage cell membranes, DNA, and proteins. This is '
               'oxidative stress — and it is both a trigger for adaptation AND a potential '
               'cause of cell damage when excessive.'))
    e.append(p('<b>The hormesis paradox:</b> Mild oxidative stress from exercise triggers '
               'antioxidant enzyme upregulation (superoxide dismutase, catalase, glutathione '
               'peroxidase) — the body\'s internal antioxidant army. Supplementing with '
               'high-dose exogenous antioxidants (vitamin C, E) post-workout may blunt these '
               'adaptive responses, similar to how cold water immersion blunts hypertrophy.'))
    e.append(mt(['Antioxidant','Source','Function','Note for Athletes'],
        [['Vitamin C','Citrus, guava, amla, bell peppers','Aqueous phase antioxidant; regenerates vitamin E; collagen synthesis','Safe to supplement; don\'t mega-dose post-workout'],
         ['Vitamin E','Nuts, seeds, olive oil, avocado','Lipid phase antioxidant; protects cell membranes','Food sources preferred; synthetic form (dl-alpha) less effective'],
         ['Beta-carotene (provitamin A)','Carrots, sweet potato, mango, spinach','Antioxidant; converted to retinol (vit A)','Excess beta-carotene (not retinol) safe; food over supplements'],
         ['Polyphenols','Berries, green tea, turmeric, dark chocolate','Anti-inflammatory; modulate gut microbiome','Beneficial chronically; avoid very high doses acutely post-workout'],
         ['Glutathione','Synthesised in body; boosted by NAC supplement','Master intracellular antioxidant','N-acetyl cysteine (NAC) is an effective precursor supplement'],
         ['Selenium','Brazil nuts, fish, eggs, meat','Glutathione peroxidase co-factor; thyroid function','1–2 Brazil nuts/day provides RDA; excess is toxic'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 6: Gut Health and Microbiome Nutrition'))
    e.append(sp(6));e.append(h1('The Gut-Muscle Axis'))
    e.append(p('The gut microbiome — the trillions of bacteria, fungi, and other microorganisms '
               'in the digestive tract — influences nutrient absorption, inflammation, immune '
               'function, mental health, and increasingly, athletic performance. A diverse, '
               'healthy microbiome is associated with:'))
    for it in ['Better short-chain fatty acid (SCFA) production → anti-inflammatory, gut barrier integrity',
               'Enhanced nutrient absorption (B-vitamins, vitamin K2 synthesised by bacteria)',
               'Reduced systemic inflammation → faster recovery from exercise',
               'Lower depression/anxiety risk via gut-brain axis (vagus nerve signalling)',
               'Better insulin sensitivity → improved glucose partitioning to muscle']:
        e.append(bl(it))
    e.append(mt(['Microbiome Support Strategy','Examples','Mechanism'],
        [['Prebiotics (feed bacteria)','Oats, garlic, onion, banana, chicory, dal','Fermented to SCFAs by beneficial bacteria'],
         ['Probiotics (introduce bacteria)','Curd/dahi, lassi, kefir, kombucha, kimchi, miso','Temporary colonisation; modulate immune signalling'],
         ['Diversity of plant foods','30 different plant foods/week (AIM)','More plant species = more bacterial species'],
         ['Fibre (25–38g/day)','Whole grains, legumes, vegetables, fruits','Primary substrate for gut bacteria'],
         ['Polyphenols','Berries, green tea, turmeric, dark chocolate','Selectively feed Lactobacillus, Bifidobacterium'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 2 (CS_B2) Key Takeaways',[
        'Micronutrients are metabolic co-factors — without them, macronutrient metabolism is impaired',
        'Vitamin D3 deficiency affects 70–90% of Indians; supplement 2000–4000 IU daily with K2',
        'Non-haem iron absorption doubles when consumed with vitamin C; tea/coffee inhibit it',
        'Magnesium cofactors 300+ enzymes including all ATP reactions; 60–70% of people are deficient',
        'Antioxidant hormesis: mild exercise-induced ROS triggers adaptation; mega-dosing post-workout may blunt gains',
        'Gut microbiome diversity (30+ plant foods/week) improves absorption, recovery, and inflammation',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Why do 70–90% of Indians have Vitamin D3 deficiency despite abundant sunshine?',
        'Explain haem vs non-haem iron absorption and give three practical strategies to improve non-haem absorption.',
        'What is the hormesis paradox in antioxidant nutrition for athletes?',
        'Why is magnesium oxide a poor supplement choice compared to magnesium glycinate?',
        'List three prebiotic foods and explain how they benefit the gut microbiome.',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════
# M3: Indian Superfoods & Traditional Nutrition (50min)
# ═══════════════════════════════════════════════════
def gen_b2_m3():
    fname=os.path.join(OUT,'cs_b2_mod3_indian_superfoods.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(3,'Indian Superfoods & Traditional Nutrition Science',50)

    e.append(sd('SECTION 1: Ayurveda Meets Modern Nutrition Science','#1A1A2E'))
    e.append(sp(6));e.append(h1('The Wisdom of Traditional Indian Food Systems'))
    e.append(p('India possesses one of the world\'s richest nutritional traditions — a food '
               'culture developed over thousands of years that, when examined through a modern '
               'scientific lens, reveals remarkable alignment with contemporary nutritional research. '
               'Traditional practices like turmeric in milk, fermentation of idli/dosa batter, '
               'and combination of rice with dal are not mere customs — they are nutritionally '
               'sophisticated strategies.'))
    e.append(p('This module analyses key Indian foods and spices through an evidence-based lens, '
               'helping you leverage India\'s extraordinary food heritage for optimal health and '
               'athletic performance.'))
    e.append(sp())

    e.append(sd('SECTION 2: Indian Superfoods — Evidence-Based Analysis'))
    e.append(sp(6));e.append(h1('Turmeric (Haldi) — The Golden Anti-Inflammatory'))
    e.append(p('Turmeric (Curcuma longa) has been used in Ayurvedic medicine for over 4,000 '
               'years. Modern research has identified curcumin as its primary bioactive compound, '
               'with over 3,000 published peer-reviewed studies examining its effects.'))
    e.append(mt(['Effect','Evidence Level','Notes'],
        [['Anti-inflammatory','Strong (A)','Inhibits NF-κB pathway (master inflammation switch); comparable to some NSAIDs'],
         ['Antioxidant','Strong (A)','Direct radical scavenging + upregulates endogenous antioxidants'],
         ['Joint health','Moderate (B)','Reduces DOMS and joint pain in athletes; meta-analysis: equal to ibuprofen for knee OA'],
         ['Muscle recovery','Moderate (B)','500mg curcumin pre-workout reduces DOMS at 48h post-exercise'],
         ['Brain health','Moderate (B)','Crosses BBB; increases BDNF; may reduce Alzheimer\'s risk'],
         ['Cancer prevention','Preliminary (C)','Multiple mechanisms in vitro; limited RCT data in humans'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Bioavailability problem:</b> Curcumin has poor absorption — rapidly metabolised '
               'in the gut. Solutions: consume with <b>black pepper (piperine)</b> (increases '
               'bioavailability 2000%), cook in fat (fat-soluble), or use BCM-95/Theracurmin '
               'enhanced formulations (20–30× higher bioavailability than standard curcumin).'))
    e.append(p('<b>Practical intake:</b> Daily use of turmeric in cooking (1–2 tsp/day) provides '
               'baseline benefit. For therapeutic effects (anti-inflammatory, recovery), '
               '500–1000mg curcumin with piperine supplement is more reliable.'))
    e.append(sp())

    e.append(h1('Amla (Indian Gooseberry) — The Vitamin C Powerhouse'))
    e.append(p('Amla (Phyllanthus emblica) contains 700mg of Vitamin C per 100g — '
               '20× more than oranges. Unlike synthetic ascorbic acid, amla\'s Vitamin C is '
               'bound to tannins and polyphenols that stabilise it against heat degradation '
               'and provide additional antioxidant synergy.'))
    for it in ['Highest known food source of Vitamin C (per gram)',
               'Powerful antioxidant: reduces oxidised LDL, a primary driver of atherosclerosis',
               'Liver protective: used in Ayurveda for centuries; modern research confirms hepatoprotective effects',
               'Collagen synthesis support: Vitamin C + proline → hydroxylated proline → collagen triple helix',
               'Immune enhancement: stimulates natural killer cells and macrophage activity',
               'Hair and skin: Vitamin C + phytonutrients reduce oxidative hair damage']:
        e.append(bl(it))
    e.append(p('<b>How to use:</b> Fresh amla, amla juice, amla powder (churna), or amla murabba '
               '(preserve). Triphala (ayurvedic formula) combines amla with two other berries — '
               'a traditional tonic with strong modern research support.'))
    e.append(sp())

    e.append(h1('Ashwagandha (Withania somnifera) — The Adaptogen'))
    e.append(p('Ashwagandha is classified as an adaptogen — a plant compound that helps the '
               'body adapt to physical and psychological stress by modulating the HPA axis. '
               'It is one of the most extensively researched Ayurvedic herbs, with strong '
               'evidence for:'))
    e.append(mt(['Effect','Evidence','Dose','Duration'],
        [['Cortisol reduction','Strong (A)','300–600mg KSM-66 extract','8–12 weeks'],
         ['Testosterone increase (males)','Moderate-Strong (B+)','600mg KSM-66','8–12 weeks (+15–18% in studies)'],
         ['VO2 max improvement','Moderate (B)','600mg/day','8 weeks (+4.9% elite athletes)'],
         ['Strength gain (combined w/training)','Moderate (B)','600mg/day','8 weeks (+additional ~1RM increase vs placebo)'],
         ['Sleep quality','Moderate (B)','300–600mg KSM-66','6–8 weeks (reduces sleep onset, improves quality)'],
         ['Anxiety reduction','Strong (A)','300–600mg/day','6–8 weeks (reduces GAD scores)'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Key note:</b> Quality of ashwagandha supplement matters enormously. KSM-66 '
               'and Sensoril are the standardised, clinically tested extracts with established '
               'withanoside content. Generic "ashwagandha powder" may have minimal active '
               'compound concentrations.'))
    e.append(sp())

    e.append(h1('Dal (Legumes) — The Indian Protein Powerhouse'))
    e.append(p('Legumes (dal, rajma, chole, moong, masoor, urad) are the backbone of Indian '
               'vegetarian protein nutrition. They are nutritionally extraordinary:'))
    e.append(mt(['Legume','Protein (100g dry)','Fibre (100g dry)','Key Micronutrients','Notable Benefit'],
        [['Masoor dal (red lentil)','25g','11g','Iron, folate, B1','Fastest-cooking; complete amino upgrade with rice'],
         ['Moong dal (mung bean)','24g','17g','Magnesium, potassium, B-vitamins','Easiest to digest; good sprouted'],
         ['Rajma (kidney bean)','24g','15g','Iron, folate, zinc','Resistant starch; excellent for glucose control'],
         ['Chole (chickpea)','19g','17g','Iron, zinc, magnesium, vitamin B6','Versatile; satiety star (high protein+fibre)'],
         ['Urad dal (black lentil)','25g','18g','Iron, calcium, magnesium','Dal makhani base; overnight soaking improves absorption'],
         ['Soybean','36g','9g','All essential amino acids, isoflavones, omega-3','Highest protein; complete EAA; mild phytoestrogen (safe at normal doses)'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Antinutrients in legumes:</b> Legumes contain phytates (phosphorus storage '
               'compound) and lectins (plant defence proteins) that reduce mineral absorption '
               'and may irritate the gut lining. Mitigated by: soaking 8–12 hours (removes '
               '50–70% phytates), pressure cooking (eliminates lectins), sprouting (increases '
               'bioavailability and digestibility), fermentation (idli/dosa — maximises '
               'absorption and creates B12 from bacteria).'))
    e.append(sp())

    e.append(sd('SECTION 3: Traditional Indian Food Wisdom'))
    e.append(sp(6));e.append(h1('Dal + Rice: A Perfect Protein Story'))
    e.append(p('The combination of dal (legumes) and rice (or roti) is not mere tradition — '
               'it is a brilliant nutritional strategy. Legumes are rich in lysine but low in '
               'methionine; rice/wheat are the opposite. Together, they provide a complete '
               'essential amino acid profile equivalent to animal protein.'))
    e.append(p('This is protein complementation — and it does NOT require eating them in the '
               'same meal. The body maintains an amino acid pool throughout the day; consuming '
               'complementary proteins within the same day is sufficient.'))
    e.append(h2('Fermentation — India\'s Probiotic Heritage'))
    e.append(p('Indian cuisine has a rich fermentation tradition that predates modern probiotic '
               'science by millennia:'))
    e.append(mt(['Fermented Food','Live Cultures','Health Benefit','Traditional Use'],
        [['Curd (dahi)','Lactobacillus bulgaricus, Streptococcus thermophilus','Gut health, lactose digestion, calcium','Served with every meal in South India'],
         ['Idli/Dosa batter','Wild Lactobacillus, Leuconostoc','Increased B-vitamins, reduced phytates, improved protein digestibility','Breakfast staple — natural probiotic vehicle'],
         ['Kanji (fermented rice water)','Lactobacillus varieties','Electrolyte-rich; digestive; post-illness recovery drink','Traditional North/East Indian winter drink'],
         ['Gundruk (Nepal/NE India)','Leuconostoc, Lactobacillus','Vitamin K2, lactic acid bacteria; gut health','Fermented leafy greens'],
         ['Lassi','Lactobacillus acidophilus (curd-based)','Probiotics, calcium, B12, cooling','Traditional cooling summer drink'],
        ]))
    e.append(sp(8))
    e.append(h2('Spices as Medicine — Evidence-Based Summary'))
    e.append(mt(['Spice','Bioactive Compound','Evidence-Based Benefit'],
        [['Turmeric','Curcumin','Anti-inflammatory, antioxidant, joint health'],
         ['Ginger','Gingerols, shogaols','Anti-nausea, anti-inflammatory, reduces DOMS'],
         ['Fenugreek (methi)','4-hydroxyisoleucine, fenugreekine','Lowers blood glucose; increases testosterone in males; improves insulin sensitivity'],
         ['Cinnamon','Cinnamaldehyde, cinnamic acid','Lowers fasting blood glucose; improves insulin sensitivity'],
         ['Black pepper','Piperine','Enhances bioavailability of curcumin 2000%; mild thermogenic'],
         ['Cumin (jeera)','Cuminaldehyde, thymoquinone','Digestive; anti-inflammatory; antimicrobial'],
         ['Moringa','Isothiocyanates, quercetin','Multi-micronutrient (vit A, C, K, iron, calcium); anti-inflammatory'],
         ['Cardamom','Cineole, terpinene','Antioxidant; digestive; blood pressure lowering'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 3 (CS_B2) Key Takeaways',[
        'Indian traditional food wisdom aligns remarkably with modern nutritional science',
        'Turmeric (curcumin with piperine) rivals NSAIDs for joint inflammation; take with fat and black pepper',
        'Amla is the highest Vitamin C food by weight — 700mg/100g vs orange 53mg/100g',
        'Ashwagandha (KSM-66) reduces cortisol, improves testosterone and VO2 max — one of the best-evidenced adaptogens',
        'Dal + rice = complete protein complementation; pressure cooking eliminates antinutrients',
        'Fermentation (idli, dahi, dosa) increases B-vitamins, bioavailability, and provides live probiotic cultures',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Why does consuming turmeric with black pepper increase curcumin bioavailability by 2000%?',
        'Explain protein complementation using the dal+rice example with specific amino acids.',
        'What are antinutrients and how do traditional food preparation methods reduce them?',
        'Compare the Vitamin C content of amla vs orange and explain the stability advantage of amla\'s Vitamin C.',
        'What is KSM-66 and why does it matter when choosing an ashwagandha supplement?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════
# M4: Meal Planning for Different Goals (65min)
# ═══════════════════════════════════════════════════
def gen_b2_m4():
    fname=os.path.join(OUT,'cs_b2_mod4_meal_planning.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(4,'Meal Planning for Different Goals',65)

    e.append(sd('SECTION 1: The Foundation of Successful Meal Planning'))
    e.append(sp(6));e.append(h1('Why Meal Planning Changes Everything'))
    e.append(p('The number one predictor of dietary success is not willpower, motivation, or '
               'knowledge — it is preparation. People who plan their meals eat 30% fewer '
               'calories from processed foods, consume 50% more vegetables, and are twice as '
               'likely to maintain their goal weight. Meal planning removes decision fatigue '
               'from the most important health decision you make every day.'))
    e.append(mt(['Meal Planning Benefit','Mechanism','Quantified Impact'],
        [['Reduces decision fatigue','Choices made in advance without hunger-driven impulse','Reduces impulsive high-calorie choices by 30–50%'],
         ['Saves money','Bulk buying; reduces restaurant/takeaway frequency','Average saving: ₹3000–8000/month for families'],
         ['Ensures nutritional adequacy','Pre-planned variety ensures micronutrient coverage','30+ plant foods/week achievable with planning'],
         ['Supports training goals','Pre/post-workout meals timed appropriately','10–15% better recovery metrics in planned vs unplanned dieters'],
         ['Reduces food waste','Buy only what\'s needed; use ingredients across multiple meals','25–40% reduction in household food waste'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 2: Meal Plans for Fat Loss'))
    e.append(sp(6));e.append(h1('Fat Loss Meal Planning Principles'))
    e.append(p('Effective fat loss meal planning is built on five pillars:'))
    for it in ['Caloric deficit: 300–500 kcal below TDEE (sustainable without muscle loss)',
               'High protein: 2.0–2.4g/kg body weight (preserves lean mass in deficit)',
               'High fibre: 25–38g/day (satiety without excessive calories)',
               'Low energy density: foods with high volume per calorie (vegetables, lean protein)',
               'Adequate fat: minimum 15–20% of calories (hormonal health)']:
        e.append(bl(it))
    e.append(h2('Indian Fat Loss Day (75kg male, 1800 kcal target)'))
    e.append(mt(['Meal','Food','Calories','P/C/F (grams)'],
        [['Breakfast (8am)','3 scrambled eggs + 2 whole wheat bread slices + black coffee','380','27P / 32C / 14F'],
         ['Mid-morning (11am)','1 apple + 200g low-fat Greek yoghurt','200','14P / 30C / 3F'],
         ['Lunch (1pm)','150g chicken breast (grilled) + 1 cup brown rice + 2 cups sabzi (mixed veg curry) + salad','500','45P / 55C / 8F'],
         ['Pre-workout (4pm)','1 banana + 30g whey protein in water','270','27P / 32C / 2F'],
         ['Post-workout (7pm)','150g paneer bhurji (low oil) + 1 roti','320','24P / 25C / 12F'],
         ['Dinner (8:30pm)','1 cup dal + salad + 100g tofu tikka (baked)','330','28P / 30C / 8F'],
         ['TOTAL','','2000 (approx)','165P / 204C / 47F'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Calorie-reducing strategies within Indian cuisine:</b>'))
    for it in ['Use air fryer or minimal oil cooking vs deep-frying (saves 100–300 kcal per dish)',
               'Replace full-fat coconut milk with light coconut milk or yoghurt in curries',
               'Use cauliflower rice (gobi chawal) 2–3 days/week to reduce caloric density of meals',
               'Dahi (curd) as base for marinades instead of cream-based sauces',
               'Increase sabzi (vegetable curry) portion and reduce grain portion to lower energy density']:
        e.append(bl(it))
    e.append(sp())

    e.append(sd('SECTION 3: Meal Plans for Muscle Building'))
    e.append(sp(6));e.append(h1('Muscle Building Nutrition Strategy'))
    e.append(p('Building muscle requires a caloric surplus (typically 200–400 kcal above TDEE), '
               'combined with high protein intake and adequate carbohydrates to fuel training '
               'and spare protein for tissue synthesis.'))
    e.append(p('<b>Key principle:</b> In a caloric surplus with resistance training, roughly '
               '30–50% of weight gained is muscle, 50–70% is fat (in a "dirty bulk"). A '
               'controlled "lean bulk" (+200 kcal/day) maximises muscle:fat gain ratio.'))
    e.append(h2('Indian Muscle Building Day (70kg male, 2800 kcal target)'))
    e.append(mt(['Meal','Food','Calories','P/C/F'],
        [['Breakfast (7:30am)','5 whole eggs + 2 whole wheat paratha + whole milk lassi (300ml)','750','42P / 65C / 28F'],
         ['Mid-morning (10:30am)','30g whey + 1 banana + 30g peanut butter + oats 50g','550','35P / 60C / 16F'],
         ['Lunch (1pm)','200g chicken curry (home cooked) + 2 cups rice + 1 cup dal + 2 cups salad','750','55P / 80C / 18F'],
         ['Pre-workout (4pm)','1 cup curd + 1 banana + handful dates (4–5)','300','10P / 60C / 4F'],
         ['Post-workout (7pm)','30g whey + 50g oats','250','28P / 36C / 3F'],
         ['Dinner (8:30pm)','200g salmon/fish curry + 1.5 cups rice + sabzi','680','48P / 70C / 18F'],
         ['Pre-sleep (10:30pm)','300g cottage cheese (paneer) / casein shake','300','22P / 10C / 15F'],
         ['TOTAL','','2780','240P / 381C / 102F'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 4: Meal Plans for Vegetarians and Vegans'))
    e.append(sp(6));e.append(h1('Plant-Based Performance Nutrition'))
    e.append(p('A well-planned plant-based diet can fully support athletic performance and '
               'muscle building. However, it requires intentional planning to address '
               'potential shortfalls: protein (quantity + quality), B12, iron, zinc, omega-3, '
               'iodine, and Vitamin D3.'))
    e.append(mt(['Nutrient','Vegan Risk','Best Plant Sources','When to Supplement'],
        [['B12','High (no plant sources)','Nutritional yeast, fortified foods','Always — 250–500mcg cyanocobalamin daily'],
         ['Iron (haem)','Moderate (only non-haem)','Dal, spinach, pumpkin seeds, fortified cereals','If ferritin <20 ng/mL; always with Vitamin C'],
         ['Zinc','Moderate (phytate binding)','Hemp seeds, pumpkin seeds, legumes, nuts','Consider 15–25mg zinc if training heavily'],
         ['Omega-3 (EPA/DHA)','High (ALA poorly converts)','Flaxseed, chia, walnuts (ALA)','Algae oil (EPA+DHA source) — 500–1000mg/day'],
         ['Iodine','Moderate (no dairy/seafood)','Iodised salt, seaweed (nori)','Low-dose iodine supplement if low intake'],
         ['Calcium','Low-moderate','Fortified plant milk, ragi, sesame, tofu (calcium-set)','250–500mg calcium if intake low'],
         ['Vitamin D3','High (vegan D3 from lichen)','Fortified plant milk, mushrooms (UV)','2000–4000 IU vegan D3 daily'],
        ]))
    e.append(sp(8))
    e.append(h2('Vegan Protein Day Plan (65kg female, 2000 kcal, 130g protein target)'))
    e.append(mt(['Meal','Food','Protein'],
        [['Breakfast','Tofu scramble (150g firm tofu) + 2 whole wheat toast + edamame (50g)','28g'],
         ['Snack','Soy protein shake + 30g peanut butter + 1 apple','30g'],
         ['Lunch','Rajma chawal (kidney beans 100g dry) + brown rice + spinach salad with hemp seeds','32g'],
         ['Pre-workout','Soy milk smoothie + banana + 20g pea protein','25g'],
         ['Post-workout','Pea protein shake + rice cakes + peanut butter','22g'],
         ['Dinner','Tempeh stir fry (150g) + quinoa + roasted vegetables','35g'],
         ['TOTAL','','~172g protein ✓'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 5: Meal Prep Masterclass'))
    e.append(sp(6));e.append(h1('Batch Cooking for the Week'))
    e.append(p('The most effective meal planning strategy is Sunday batch cooking — preparing '
               'the bulk of the week\'s protein, grains, and vegetables in one 2–3 hour session, '
               'then assembling meals quickly throughout the week.'))
    e.append(mt(['Component','Batch Cook Method','Refrigerator Life','Use In'],
        [['Brown rice / quinoa','Cook 5 cups dry; store in containers','5 days','Lunch bowls, dinner sides, post-workout meals'],
         ['Grilled chicken (600g)','Season, bake at 200°C 25–30 min','4 days','Wraps, salads, dinner protein'],
         ['Hard-boiled eggs (12)','Boil 10–12 min; store unpeeled','1 week','Breakfast, snacks, salad topping'],
         ['Dal (pressure cooker)','2 cups dry lentils; triple quantities','4–5 days','Lunch, dinner with roti/rice'],
         ['Roasted vegetables','3–4 types; toss oil+spices; 200°C 30 min','4 days','Side dishes, bowls, wraps'],
         ['Paneer cubes (400g)','Cut and store, or marinate and bake','3–4 days','Tikka, bhurji, curry, snacks'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 4 (CS_B2) Key Takeaways',[
        'Meal planning is the single highest-leverage dietary habit — preparation beats willpower',
        'Fat loss: 300–500 kcal deficit + 2.0–2.4g/kg protein + high fibre for satiety',
        'Muscle building: 200–400 kcal surplus + 1.8–2.2g/kg protein + carbs to fuel training',
        'Indian cuisine is naturally adaptable — air frying, curd-based marinades, and vegetable-first plating reduce calories',
        'Vegan athletes must supplement B12, algae omega-3, and vitamin D3 without exception',
        'Sunday batch cooking (rice, protein, dal, vegetables) enables daily healthy eating with minimal weekday effort',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Design a fat loss meal plan for a 65kg Indian female at 1600 kcal target.',
        'What is the lean bulk surplus, and why is it preferable to a "dirty bulk" for body composition?',
        'Name 4 nutrients at risk in a vegan diet and provide both food and supplement solutions for each.',
        'Explain how Sunday batch cooking reduces decision fatigue and improves dietary adherence.',
        'How does replacing full-fat coconut milk with light coconut milk in a curry reduce calories while maintaining satisfaction?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════
# M5: Metabolism & Energy Balance (45min)
# ═══════════════════════════════════════════════════
def gen_b2_m5():
    fname=os.path.join(OUT,'cs_b2_mod5_metabolism_energy.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(5,'Metabolism & Energy Balance',45)

    e.append(sd('SECTION 1: What Is Metabolism?'))
    e.append(sp(6));e.append(h1('Metabolism — The Sum of All Chemical Reactions'))
    e.append(p('Metabolism refers to the entirety of chemical reactions that occur within '
               'living cells to maintain life. For body composition and fitness purposes, '
               'we focus on energy metabolism — the processes by which nutrients are '
               'converted to ATP and heat.'))
    e.append(mt(['Metabolic Process','Category','Function','Hormonal Control'],
        [['Glycolysis','Catabolism','Glucose → pyruvate → ATP','Glucagon (promotes), Insulin (promotes via glucose uptake)'],
         ['Beta-oxidation','Catabolism','Fatty acids → Acetyl-CoA → ATP','Adrenaline, glucagon stimulate; insulin inhibits'],
         ['Amino acid catabolism','Catabolism','Amino acids → glucose (gluconeogenesis) or ketones','Cortisol promotes; insulin inhibits'],
         ['Glycogen synthesis','Anabolism','Glucose → glycogen (storage)','Insulin promotes'],
         ['Triglyceride synthesis','Anabolism','Fatty acids + glycerol → stored fat','Insulin promotes; caloric surplus drives'],
         ['Protein synthesis','Anabolism','Amino acids → muscle protein','Insulin + mTORC1 + resistance training'],
        ]))
    e.append(sp(8))

    e.append(h2('BMR — What Determines Your Metabolic Rate'))
    e.append(p('Basal Metabolic Rate (BMR) is determined by multiple factors, some modifiable '
               'and some not:'))
    e.append(mt(['Factor','Influence on BMR','Modifiable?'],
        [['Lean muscle mass','Each kg muscle burns ~13 kcal/day at rest','YES — resistance training increases muscle → increases BMR'],
         ['Body size (height, weight)','Larger bodies have higher absolute BMR','Partially'],
         ['Age','BMR decreases ~1–2% per decade after age 20','Partially — muscle preservation reduces decline'],
         ['Sex','Males average 5–10% higher BMR (more muscle, less fat)','No (biological)'],
         ['Thyroid function','Thyroid hormones (T3, T4) regulate metabolic rate','Yes with medical treatment if impaired'],
         ['Genetics','Individual variation in mitochondrial efficiency','No'],
         ['Temperature adaptation','Living in cold climate increases BMR slightly','No (environment-dependent)'],
        ]))
    e.append(sp(8))
    e.append(p('<b>The most effective way to increase BMR:</b> Build lean muscle mass through '
               'resistance training. A 5kg increase in lean mass increases resting metabolic '
               'rate by approximately 65 kcal/day — not massive in isolation, but compounding '
               'over years plus NEAT and exercise activity creates substantial impact.'))
    e.append(sp())

    e.append(sd('SECTION 2: Metabolic Adaptation — Why Diets Fail'))
    e.append(sp(6));e.append(h1('Metabolic Adaptation: The Diet Plateau Explained'))
    e.append(p('Metabolic adaptation (sometimes called "adaptive thermogenesis") is the body\'s '
               'multi-layered defence against weight loss. When you reduce calories, the body '
               'responds with mechanisms to conserve energy and defend body weight — a '
               'survival system evolved over millions of years.'))
    e.append(mt(['Adaptation','Mechanism','Magnitude','Timeframe'],
        [['RMR reduction','Loss of lean mass; thyroid hormone reduction (T4→T3 conversion decreases)','−100 to −300 kcal/day','2–4 weeks'],
         ['NEAT reduction','Unconscious reduction in fidgeting, posture activity, spontaneous movement','−100 to −400 kcal/day','1–2 weeks'],
         ['TEF reduction','Less food → less energy to digest food','−50 to −100 kcal/day','Immediate'],
         ['Hunger hormones','Ghrelin (appetite UP); leptin (satiety DOWN); peptide YY DOWN','Significantly increases hunger','2–4 weeks'],
         ['Exercise efficiency','Same distance run at lower calorie cost (mass is lower)','−50 to −150 kcal/day','Gradual'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Total metabolic adaptation:</b> After significant weight loss (10%+ body weight), '
               'metabolic adaptation can reduce TDEE by 300–500 kcal/day below what equations '
               'would predict for the new body weight. This is why "The Biggest Loser" '
               'contestants regain weight — their metabolism is chronically suppressed.'))
    e.append(h2('Strategies to Minimise Metabolic Adaptation'))
    for it in ['Moderate deficit only: -500 kcal maximum; never go below 1200 kcal (F) or 1500 kcal (M)',
               'High protein: preserves lean mass, preventing RMR loss from muscle catabolism',
               'Resistance training: maintains or increases lean mass during deficit',
               'Diet breaks: 1–2 weeks at maintenance calories every 8–12 weeks of dieting (restores leptin, reduces ghrelin)',
               'Refeed days: 1–2 days per week at maintenance (smaller version of diet break)',
               'High NEAT: deliberately maintain non-exercise movement (steps target: 8000–10,000/day)']:
        e.append(bl(it))
    e.append(sp())

    e.append(sd('SECTION 3: Insulin — The Master Partitioning Hormone'))
    e.append(sp(6));e.append(h1('Insulin: Far More Than "Fat Storage"'))
    e.append(p('Insulin is a peptide hormone secreted by pancreatic beta cells in response to '
               'elevated blood glucose. It is often demonised in popular culture as "the fat '
               'storage hormone," but this is a profound oversimplification.'))
    e.append(p('<b>What insulin actually does:</b>'))
    for it in ['Drives glucose into muscle cells (via GLUT4 translocation) — muscle glycogen synthesis',
               'Drives glucose into adipose tissue — fat storage when in surplus',
               'Drives amino acids into muscle cells — potent MPS activator (synergistic with leucine)',
               'Inhibits gluconeogenesis (liver stops making glucose from amino acids)',
               'Inhibits lipolysis (fat breakdown) in adipose tissue',
               'Activates glycogen synthase — glycogen storage in liver and muscle',
               'Promotes protein synthesis via PI3K/Akt pathway']:
        e.append(bl(it))
    e.append(p('<b>The truth about insulin and fat:</b> Insulin promotes fat storage only in the '
               'context of caloric surplus. In a caloric deficit, fat is mobilised even with '
               'normal insulin levels because fat oxidation is driven by energy demand, not '
               'insulin alone. You can eat high-carb and lose fat in a deficit; you can eat '
               'low-carb and gain fat in a surplus. Energy balance remains primary.'))
    e.append(h2('Insulin Resistance: Prevention and Reversal'))
    e.append(mt(['Mechanism','Cause','Prevention/Treatment'],
        [['GLUT4 downregulation','Chronic hyperinsulinaemia; excess adipose tissue','Exercise (activates GLUT4 independently of insulin), weight loss'],
         ['Ectopic fat deposition','Caloric surplus; especially fructose-driven hepatic lipogenesis','Caloric restriction; reduced refined sugar; omega-3'],
         ['Chronic inflammation','Adipose tissue macrophage infiltration; elevated IL-6, TNF-α','Anti-inflammatory diet; weight loss; omega-3; exercise'],
         ['Sleep deprivation','Cortisol increase → insulin receptor resistance','8+ hours sleep; sleep hygiene protocol'],
         ['Physical inactivity','Reduced muscle glucose uptake','150+ min/week moderate exercise; reduce sitting'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 5 (CS_B2) Key Takeaways',[
        'Metabolism is the totality of chemical reactions in cells; energy metabolism determines body composition',
        'BMR is primarily determined by lean muscle mass — resistance training increases metabolic rate',
        'Metabolic adaptation reduces TDEE by 300–500 kcal/day after significant weight loss; diet breaks help restore it',
        'Insulin is anabolic and fat-storing — but fat is gained only in a caloric surplus, not from carbs per se',
        'NEAT is the most variable and underrated component of TDEE; 8000–10,000 steps/day burns 200–400 kcal extra',
        'Insulin resistance is driven by excess adipose tissue, inflammation, and inactivity — all modifiable',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['What is adaptive thermogenesis and how much can it reduce expected TDEE after weight loss?',
        'Explain the role of leptin and ghrelin in the metabolic adaptation response to dieting.',
        'Why is insulin not simply "the fat storage hormone" and how does exercise modify its effects?',
        'What is a "diet break" and mechanistically why does it help overcome a fat loss plateau?',
        'How does a 5kg increase in lean muscle mass affect daily resting calorie burn?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════
# M6: Sports Nutrition Fundamentals (55min)
# ═══════════════════════════════════════════════════
def gen_b2_m6():
    fname=os.path.join(OUT,'cs_b2_mod6_sports_nutrition.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(6,'Sports Nutrition Fundamentals',55)

    e.append(sd('SECTION 1: Peri-Workout Nutrition Strategy'))
    e.append(sp(6));e.append(h1('Fuelling the Machine: Before, During, and After'))
    e.append(p('Sports nutrition is the application of nutritional science to optimise athletic '
               'performance, recovery, and adaptation. The peri-workout period (before, during, '
               'and after training) is the highest-leverage nutritional window for athletes.'))
    e.append(h2('Pre-Workout Nutrition (1–3 hours before)'))
    e.append(mt(['Goal','Macronutrient','Amount','Food Examples'],
        [['Top up glycogen','Carbohydrates','1–2g/kg BW','Rice, oats, roti, banana, sweet potato'],
         ['Provide amino acids','Protein','20–30g complete protein','Chicken, fish, Greek yoghurt, paneer, whey'],
         ['Minimise GI distress','Low fat, low fibre','Fat <15g, fibre <5g','Avoid deep-fried, high-fat, large fibre loads'],
         ['Hydration','Water + electrolytes','500ml 2h before; 250ml 15 min before','Water; coconut water; dilute sports drink'],
        ]))
    e.append(sp(8))
    e.append(p('<b>30-minute pre-workout option:</b> When time is limited, a fast-digesting '
               'protein + high-GI carb combination can be consumed 30 minutes before: '
               '25g whey + 1 banana + water. This provides amino acids and quick glucose '
               'without GI discomfort.'))
    e.append(h2('Intra-Workout Nutrition (during sessions >60 min)'))
    e.append(mt(['Session Duration','Carbohydrates','Electrolytes','Notes'],
        [['<60 minutes','Not needed','Water sufficient','Muscle glycogen adequate for <60 min moderate intensity'],
         ['60–90 minutes','15–30g/hour','Sodium 200–500mg/hour if sweating','Sports drink (6–8% carb) or banana half'],
         ['>90 minutes','30–60g/hour','Sodium + potassium + magnesium','Multiple carb sources (maltodextrin + fructose) empties gut faster — 2:1 ratio'],
         ['Endurance events >2.5h','60–90g/hour','Full electrolyte replacement','Requires multi-transporter carb mix (glucose + fructose)'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Multi-transporter carbohydrates:</b> The small intestine has two separate '
               'carbohydrate transporters: SGLT1 (glucose, maltose) and GLUT5 (fructose). '
               'Using both simultaneously allows absorption of 60–90g carbs/hour vs 60g '
               'maximum for glucose alone. This is why most endurance sports products '
               'combine maltodextrin (glucose) with fructose at a 2:1 ratio.'))
    e.append(h2('Post-Workout Nutrition (within 0–2 hours)'))
    e.append(p('Post-workout nutrition serves two primary purposes: initiate muscle protein '
               'synthesis (MPS) and replenish muscle glycogen. These require different nutrients:'))
    e.append(mt(['Goal','Macronutrient','Amount','Timing','Best Foods'],
        [['MPS initiation','Complete protein (leucine-rich)','25–40g','Immediately post (if fasted); within 2h if pre-workout protein eaten','Whey, chicken, eggs, fish, milk, casein'],
         ['Glycogen resynthesis','High-GI carbohydrates','0.8–1.2g/kg BW','ASAP post-workout (if next session within 8h)','White rice, white potato, sports drink, banana, dates'],
         ['Hydration','Water + sodium','1.5L per kg bodyweight lost','During 4h post-workout window','Water + pinch of salt; coconut water; electrolyte drink'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 2: Nutrition for Different Sports Demands'))
    e.append(sp(6));e.append(h1('Sport-Specific Nutritional Demands'))
    e.append(mt(['Sport Type','Energy System','Primary Fuel','Carb Need','Protein Need'],
        [['Power/Strength (Olympic lifting, powerlifting)','ATP-PCr > glycolytic','PCr, glycogen','Moderate (4–6g/kg)','High (1.8–2.2g/kg)'],
         ['Bodybuilding','Glycolytic (moderate)','Glycogen','Moderate-high (4–7g/kg)','High (1.8–2.5g/kg)'],
         ['HIIT / CrossFit','Glycolytic + oxidative','Glycogen + fat','High (5–7g/kg on training days)','High (1.8–2.2g/kg)'],
         ['Endurance running (marathon)','Oxidative','Fat + glycogen (fat majority)','Very high (7–10g/kg day before)','Moderate (1.4–1.7g/kg)'],
         ['Team sport (football, basketball)','Mixed all three','All substrates','High (6–8g/kg)','Moderate-high (1.6–2.0g/kg)'],
         ['Combat sport (boxing, wrestling)','Glycolytic dominant','Glycogen, PCr','Moderate-high (5–7g/kg)','High (1.8–2.5g/kg)'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 3: Weight Cutting and Making Weight (Combat Sports Context)'))
    e.append(sp(6));e.append(h1('Rapid Weight Loss for Competition'))
    e.append(p('Athletes in weight-class sports (boxing, wrestling, judo, powerlifting) '
               'routinely cut weight before weigh-in. Understanding the physiology is critical '
               'for both practitioners and coaches:'))
    e.append(mt(['Weight Cut Method','Weight Lost','Recovery Time Needed','Risks'],
        [['Caloric restriction (4–8 weeks)','Fat mass','N/A — permanent loss (fat)','Muscle loss if insufficient protein; reduced strength'],
         ['Water manipulation (24–48h)','Water + electrolytes (2–5kg)','24h required for rehydration','Impaired performance; cramping; dangerous if >5% BW'],
         ['Glycogen depletion','Glycogen + water (1–3kg)','24–48h carb reload needed','Performance impairment if not refuelled'],
         ['Sweat suit / sauna (acute)','Water (1–3kg)','24–48h rehydration','Dangerous; banned in some sports; cardiac risk'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Safe weight class strategy:</b> Compete as close to walk-around weight as '
               'possible. Chronic severe weight cutting (>5% body weight) impairs long-term '
               'health, bone density, and hormonal function. Use caloric restriction only to '
               'reduce fat mass over the competition preparation period.'))

    e.append(sd('SECTION 4: Hydration Science for Athletes'))
    e.append(sp(6));e.append(h1('Advanced Hydration for Athletic Performance'))
    e.append(p('Elite athletes use sweat rate testing to individualise hydration strategies. '
               'Sweat rates vary from 0.5L/hr (cold weather, low intensity) to 3L/hr (heat, '
               'high intensity). Sodium concentration in sweat also varies (300–1800mg/L) — '
               'the highest sodium sweaters are at greatest risk of exercise-associated '
               'hyponatraemia when over-hydrating with plain water.'))
    e.append(mt(['Hydration Metric','Test Method','Implications for Training'],
        [['Sweat rate','Weigh before/after: (pre-BW − post-BW + fluids consumed) / time','Target to replace 75–80% of fluid losses during exercise'],
         ['Sweat sodium','Commercial sweat patch (Nix Biosensor, FLOW)', 'High sodium sweaters need electrolyte drinks even in short sessions'],
         ['Urine specific gravity','Refractometer; home test: first void USG >1.020 = dehydrated','Useful for pre-competition hydration monitoring'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 6 (CS_B2) Key Takeaways',[
        'Pre-workout: 1–2g carbs/kg + 20–30g protein + minimal fat/fibre 1–3h before training',
        'Intra-workout carbs only needed for sessions >60 minutes; 30–60g/hour using multi-transporter carbs',
        'Post-workout: 25–40g complete protein + high-GI carbs within 2 hours',
        'Sport-specific carbohydrate needs vary dramatically: powerlifters need 4–6g/kg; marathon runners 7–10g/kg',
        'Weight cutting should primarily use fat loss over weeks, not acute water manipulation',
        'Individual sweat rate and sodium concentration testing allows precision hydration programming',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['Explain why multi-transporter carbohydrates (maltodextrin + fructose) allow higher absorption rates than glucose alone.',
        'Compare peri-workout nutrition for a powerlifter vs a marathon runner.',
        'What is sweat rate, how is it calculated, and how does it influence hydration strategy?',
        'Why is acute severe weight cutting (>5% body weight) dangerous, and what is the evidence-based alternative?',
        'What post-workout nutrition protocol would you recommend for an athlete training twice per day?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════
# M7: Supplements — What Works (45min)
# ═══════════════════════════════════════════════════
def gen_b2_m7():
    fname=os.path.join(OUT,'cs_b2_mod7_supplements.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(7,"Supplements — What Works, What Doesn't",45)

    e.append(sd('SECTION 1: The Supplement Industry — Billion-Dollar Confusion'))
    e.append(sp(6));e.append(h1('Supplement Industry Context'))
    e.append(p('The global sports nutrition supplement market exceeds $50 billion annually — '
               'growing 8% per year. Yet the vast majority of products have little to no '
               'credible scientific evidence supporting their performance or health claims. '
               'Understanding evidence evaluation is the most important skill for navigating '
               'the supplement landscape.'))
    e.append(h2('How to Evaluate Supplement Evidence'))
    e.append(mt(['Evidence Level','Description','Example','Trust Level'],
        [['A — Strong RCT evidence','Multiple randomised controlled trials in relevant populations showing consistent results','Creatine, caffeine, protein powder, beta-alanine','High confidence'],
         ['B — Moderate evidence','Some RCTs; results mixed; mechanism plausible','Ashwagandha, HMB, citrulline malate','Contextually useful'],
         ['C — Preliminary','Mostly animal/in vitro; limited human RCTs','Berberine (some human data), ecdysterone','Interesting; not recommended universally'],
         ['D — Weak/No evidence','No quality human RCTs; mechanism speculation','Most "fat burners", BCAAs (when protein adequate)','Not worth buying'],
         ['F — Dangerous','No evidence + known safety concerns','DNP, SARMs, contaminated products','Avoid completely'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 2: Tier 1 Supplements — Strong Evidence'))
    e.append(sp(6));e.append(h1('Evidence-Based Essentials'))

    e.append(h2('1. Creatine Monohydrate'))
    e.append(p('Creatine is the most researched performance supplement in history — over 500 '
               'published peer-reviewed studies. It is also one of the safest.'))
    e.append(mt(['Property','Detail'],
        [['Mechanism','Increases muscle PCr stores by 20%, enabling faster ATP regeneration for repeated high-intensity efforts'],
         ['Performance benefit','5–15% improvement in maximal strength and power; greater training volume capacity; enhanced hypertrophy'],
         ['Dose','3–5g/day (loading not necessary: 3–5g/day reaches saturation in 3–4 weeks)'],
         ['Loading phase (optional)','20g/day (4×5g) for 5–7 days if faster saturation desired; causes GI distress in some'],
         ['Timing','Any time of day; post-workout may be marginally superior'],
         ['Best form','Creatine monohydrate (not creatine HCl, ethyl ester — no evidence superior; higher cost)'],
         ['Safety','Decades of research confirm safety in healthy individuals; no evidence of kidney damage in healthy people at standard doses'],
         ['Myth busting','Water retention (1–2kg initial) is intramuscular, not subcutaneous — reduces with ongoing use'],
        ]))
    e.append(sp(8))

    e.append(h2('2. Caffeine'))
    e.append(p('Caffeine is the world\'s most widely consumed psychoactive substance and one '
               'of the most effective legal ergogenic (performance-enhancing) compounds:'))
    for it in ['Mechanism: adenosine receptor antagonist → blocks fatigue signal; increases dopamine/norepinephrine release',
               'Aerobic endurance: 3–6mg/kg improves time to exhaustion 12–15% and time-trial performance 3%',
               'Strength and power: 3–6mg/kg improves maximal voluntary contraction 3–5%; reduces perceived exertion',
               'Focus and reaction time: acutely improves attention and cognitive performance',
               'Dose: 3–6mg/kg body weight (200–400mg for most); half-life 5–6 hours',
               'Timing: 45–60 minutes before training for peak plasma levels',
               'Tolerance: caffeine tolerance develops within 1–2 weeks; cycle off 2 weeks every 6–8 weeks for resensitisation']:
        e.append(bl(it))
    e.append(p('<b>Responders vs non-responders:</b> CYP1A2 gene variant determines caffeine '
               'metabolism speed. "Fast metabolisers" (AA genotype) benefit most; '
               '"slow metabolisers" (C allele) may experience anxiety and impaired sleep at '
               'standard doses. Genetic testing can identify this.'))
    e.append(sp())

    e.append(h2('3. Protein Supplements (Whey, Casein, Soy, Pea)'))
    e.append(mt(['Type','Source','Digestion Speed','Leucine %','Best Use'],
        [['Whey concentrate','Milk (cheese by-product)','Fast (1–2 hours)','~10%','Post-workout; general protein boost'],
         ['Whey isolate','Filtered whey (>90% protein)','Fast (1–2 hours)','~12%','Post-workout; lactose intolerant; leaner choice'],
         ['Casein','Milk protein (slow-digesting)','Slow (5–7 hours)','~9%','Pre-sleep; between meals for sustained MPS'],
         ['Soy isolate','Soybeans','Moderate','~8%','Complete plant protein; good for vegans'],
         ['Pea isolate','Yellow split peas','Moderate-fast','~8%','Hypoallergenic; vegan; combine with rice protein for complete EAA'],
         ['Rice + pea blend','Combination','Moderate','~7–8%','Better EAA profile than either alone; top vegan choice'],
        ]))
    e.append(sp(8))
    e.append(p('<b>Protein powders are food, not drugs.</b> They are a convenient, cost-effective '
               'way to hit protein targets when whole food is impractical. A lean 30g serving '
               'of whey isolate providing 25g protein costs significantly less than an equivalent '
               'chicken breast serving — making it accessible for regular use.'))

    e.append(sd('SECTION 3: Tier 2 Supplements — Contextually Useful'))
    e.append(sp(6));e.append(h1('Supplements Worth Considering in Specific Contexts'))
    e.append(mt(['Supplement','Evidence','Effective Dose','Context'],
        [['Beta-alanine','B+ strong for 1–4 min efforts','3.2–6.4g/day (may cause tingling/paraesthesia)','Rowing, 400–1500m swimming/running, HIIT'],
         ['Citrulline malate','B moderate','6–8g citrulline, 30–45min pre-workout','Increased training volume; reduced muscle soreness'],
         ['HMB (beta-hydroxy beta-methylbutyrate)','B (mainly in untrained)','3g/day','Beginners; people returning after injury'],
         ['Vitamin D3 + K2','A+ (if deficient, which most are)','2000–4000 IU D3 + 100–200mcg K2','Universal recommendation; test first'],
         ['Omega-3 (EPA+DHA)','A strong','2–3g EPA+DHA combined','Anti-inflammatory; brain; muscle protein synthesis'],
         ['Magnesium glycinate','A (if deficient, most are)','300–400mg before sleep','Sleep; recovery; energy; blood pressure'],
         ['Ashwagandha (KSM-66)','B+ good','300–600mg/day','Cortisol, testosterone support; recovery'],
         ['L-carnitine','C weak','1.5–2g/day (requires insulin for uptake)','Small fat oxidation benefit; sperm motility'],
         ['Collagen + Vitamin C','B moderate','15g collagen + 50mg Vit C, 30–60min pre-exercise','Tendon/ligament health; injury prevention'],
        ]))
    e.append(sp(8))

    e.append(sd('SECTION 4: Supplements to Avoid'))
    e.append(sp(6));e.append(h1('The Useless and the Dangerous'))
    e.append(mt(['Supplement','Why to Avoid','Risk Level'],
        [['Fat burners / thermogenics','Negligible fat loss effect (<0.5kg extra); stimulant-heavy; heart rate + BP increase','High — cardiovascular risk'],
         ['Testosterone boosters (herbal)','No supplement raises testosterone meaningfully in healthy adults; regulatory fraud common','Moderate — false claims; contamination'],
         ['BCAAs (if protein adequate)','Redundant — all BCAA amino acids present in protein; no additive benefit if hitting protein targets','Low (safe but wasteful)'],
         ['Proprietary blends (undisclosed doses)','Ingredients listed without doses — impossible to verify efficacy','Moderate — often underdosed key ingredients'],
         ['SARMs (Selective Androgen Receptor Modulators)','Unapproved drugs; liver toxicity; suppresses natural testosterone; banned in sport','Very High — medical danger'],
         ['DNP (2,4-Dinitrophenol)','Industrial compound; "uncouples" mitochondria; multiple fatalities; uncontrollable hyperthermia','Extreme — life-threatening'],
        ]))
    e.append(sp(8))
    e.append(ib('Module 7 (CS_B2) Key Takeaways',[
        'Evaluate supplements by evidence level: only buy A/B rated supplements with clear mechanisms',
        'Creatine monohydrate: 3–5g/day; increases strength 5–15%; safest performance supplement in existence',
        'Caffeine: 3–6mg/kg, 45–60 min pre-workout; cycle off every 6–8 weeks; respect half-life for sleep',
        'Protein powder is food, not drugs — use to conveniently hit targets, not as a magic ingredient',
        'Vitamin D3+K2, magnesium glycinate, omega-3 EPA+DHA are health essentials that most people need',
        'Fat burners, testosterone boosters, and BCAAs (when protein adequate) are not worth buying',
        'SARMs and DNP are medically dangerous — never use or recommend regardless of marketing claims',
    ],RFC_DARK))
    e.append(sp(8))
    for i,q in enumerate(['What is the mechanism of action of creatine, and why is loading phase not mandatory?',
        'Explain caffeine\'s mechanism via adenosine antagonism and why tolerance develops.',
        'Compare whey concentrate, whey isolate, and casein for different use contexts.',
        'What does "proprietary blend" mean on a supplement label, and why is it a red flag?',
        'A client asks about SARMs they saw advertised online. What do you tell them?',
        ],1):
        e.append(Paragraph(f'{i}. {q}',S['body']))
    doc.build(e)
    print(f'Generated: {fname}')

# ═══════════════════════════════════════════════════
# M8: Final Assessment — CS_B2 (20min)
# ═══════════════════════════════════════════════════
def gen_b2_m8():
    fname=os.path.join(OUT,'cs_b2_mod8_final_assessment.pdf')
    doc=SimpleDocTemplate(fname,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    e=[]
    e+=cover(8,'Final Assessment & Certificate',20)

    e.append(sd('ASSESSMENT INSTRUCTIONS'))
    e.append(sp(6))
    e.append(ib('How to Complete This Assessment',[
        '25 questions covering all 7 modules of CS_B2 Nutrition & Healthy Eating',
        'One correct answer per question (A, B, C, or D)',
        'Passing score: 70% (18/25). Open-book assessment — refer to module notes',
        'Complete in order; target 20 minutes maximum',
    ],RFC_GREEN))
    e.append(sp(12))

    questions=[
        ('1. Leucine activates muscle protein synthesis primarily through which intracellular pathway?',
         ['A) AMPK activation → fatty acid oxidation','B) mTORC1 activation → ribosomal biogenesis and MPS','C) FOXO3 → autophagy induction','D) NF-κB → pro-inflammatory cytokine release'],'B'),
        ('2. Which food pairing creates a complete essential amino acid profile from two incomplete plant proteins?',
         ['A) Broccoli + cauliflower','B) Almonds + walnuts','C) Rice (or roti) + lentils (dal)','D) Spinach + kale'],'C'),
        ('3. Resistant starch is formed when cooked starchy foods are:',
         ['A) Eaten immediately after cooking while hot','B) Frozen and then reheated rapidly','C) Cooled after cooking (retrograde crystallisation)','D) Processed into flour'],'C'),
        ('4. The omega-6:omega-3 ratio in modern diets is approximately:',
         ['A) 1:1 (balanced)','B) 4:1 (ancestral)','C) 15:1 to 20:1 (pro-inflammatory excess)','D) 2:1 (slight imbalance)'],'C'),
        ('5. Which Vitamin D3 blood level is considered optimal for athletes?',
         ['A) <20 ng/mL','B) 20–29 ng/mL','C) 40–60 ng/mL','D) >100 ng/mL'],'C'),
        ('6. What is the recommended strategy to enhance non-haem iron absorption?',
         ['A) Consume with calcium-rich dairy foods','B) Drink tea with the meal','C) Consume with vitamin C-rich foods (lemon, amla, bell pepper)','D) Eat with foods high in phytates (wheat bran)'],'C'),
        ('7. Curcumin bioavailability is most effectively enhanced by:',
         ['A) Taking on an empty stomach with water','B) Combining with black pepper (piperine) and dietary fat','C) High-dose supplementation (5000mg+)','D) Converting to a synthetic form'],'B'),
        ('8. The highest Vitamin C content per gram among common foods is found in:',
         ['A) Orange','B) Lemon','C) Kiwi fruit','D) Amla (Indian gooseberry)'],'D'),
        ('9. KSM-66 refers to:',
         ['A) A synthetic anabolic compound in sports nutrition','B) A standardised ashwagandha root extract with established clinical evidence','C) A creatine formulation with magnesium','D) A type of whey protein hydrolysate'],'B'),
        ('10. In a caloric surplus with high insulin levels, which scenario is correct?',
         ['A) High insulin always causes fat gain regardless of caloric balance','B) Fat gain occurs only when in a caloric surplus — insulin drives storage in that context','C) Carbohydrate intake causes fat gain independent of total calorie intake','D) Insulin prevents muscle protein synthesis at elevated levels'],'B'),
        ('11. Total metabolic adaptation after significant weight loss (10%+ body weight) can reduce TDEE by approximately:',
         ['A) 50–100 kcal/day','B) 100–200 kcal/day','C) 300–500 kcal/day','D) 700–1000 kcal/day'],'C'),
        ('12. Which carbohydrate absorption transporter uses fructose as its substrate?',
         ['A) SGLT1','B) GLUT4','C) GLUT5','D) GLUT2'],'C'),
        ('13. The maximum glucose absorption rate in the small intestine from a single carbohydrate source (e.g., maltodextrin alone) is approximately:',
         ['A) 30g/hour','B) 60g/hour','C) 90g/hour','D) 120g/hour'],'B'),
        ('14. Pre-workout nutrition should MINIMISE which two macronutrients to reduce GI distress?',
         ['A) Protein and carbohydrates','B) Carbohydrates and water','C) Fat and fibre','D) Sodium and potassium'],'C'),
        ('15. Which supplement has the strongest peer-reviewed evidence base for improving strength and power?',
         ['A) BCAAs','B) Testosterone boosters','C) Creatine monohydrate','D) L-carnitine'],'C'),
        ('16. Caffeine\'s primary mechanism as an ergogenic aid is:',
         ['A) Increasing testosterone production acutely','B) Directly stimulating muscle contraction force','C) Blocking adenosine receptors and reducing perceived fatigue','D) Increasing glycogen breakdown rate'],'C'),
        ('17. Whey ISOLATE differs from whey CONCENTRATE primarily in:',
         ['A) Higher fat content in isolate','B) Higher protein content (90%+) and lower lactose in isolate','C) Faster absorption rate of concentrate','D) Different amino acid profile'],'B'),
        ('18. Beta-alanine works primarily for efforts lasting:',
         ['A) <10 seconds (sprint)','B) 1–4 minutes (glycolytic)','C) >60 minutes (endurance)','D) All durations equally'],'B'),
        ('19. Which magnesium form has the highest bioavailability and is best suited for sleep support?',
         ['A) Magnesium oxide','B) Magnesium sulphate (Epsom salt)','C) Magnesium glycinate','D) Magnesium carbonate'],'C'),
        ('20. The "diet break" strategy recommends eating at maintenance calories for 1–2 weeks to:',
         ['A) Build muscle mass during a fat loss phase','B) Restore leptin, reduce ghrelin, and counteract metabolic adaptation','C) Allow liver glycogen to deplete completely before restarting','D) Test whether the previous deficit was too aggressive'],'B'),
        ('21. Antinutrients in legumes (dal) are best reduced by:',
         ['A) Eating raw legumes with vitamin C','B) Grinding into flour and consuming at high temperature','C) Soaking 8–12h + pressure cooking + sprouting or fermentation','D) Adding salt to cooking water only'],'C'),
        ('22. An athlete weighing 70kg performing a 90-minute high-intensity session in moderate heat should consume approximately:',
         ['A) Water only — no carbohydrates or electrolytes needed','B) 30–45g carbohydrates per hour + sodium 200–500mg/hour','C) 90g carbohydrates per hour + no sodium','D) Only BCAAs intra-workout'],'B'),
        ('23. For a vegan athlete, which supplement is NON-NEGOTIABLE (must supplement; no reliable food source)?',
         ['A) Vitamin C','B) Magnesium','C) Vitamin B12','D) Potassium'],'C'),
        ('24. SARMs (Selective Androgen Receptor Modulators) should be avoided because:',
         ['A) They are legal but slightly less effective than creatine','B) They are unapproved drugs with documented liver toxicity, hormonal suppression, and are banned in sport','C) They only work for women; not men','D) They require a doctor prescription but are otherwise safe'],'B'),
        ('25. The Dietary Inflammatory Index (DII) is improved most by increasing which food category?',
         ['A) Processed meats and refined grains','B) Omega-6 seed oils','C) Fatty fish, colourful vegetables, and polyphenol-rich foods','D) High-GI carbohydrates and saturated fat'],'C'),
    ]

    for qtext,opts,ans in questions:
        e.append(Paragraph(qtext,S['q']))
        for opt in opts:
            e.append(Paragraph(opt,S['ans']))
        e.append(sp(10))

    e.append(PageBreak())
    e.append(sd('ANSWER KEY'))
    e.append(sp(8))
    answers=[(a,'') for _,_,a in questions]
    key_data=[['Q','Ans']]
    for i,(a,_) in enumerate(answers):
        key_data.append([str(i+1),a])
    # 5 cols
    cols=5; rows_per_col=5
    all_q=[f'Q{i+1}: {a}' for i,(a,_) in enumerate(answers)]
    per_row=5
    tbl_rows=[all_q[i:i+per_row] for i in range(0,25,per_row)]
    tbl=Table(tbl_rows,colWidths=[(W-40*mm)/per_row]*per_row)
    tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),RFC_GREEN),('TEXTCOLOR',(0,0),(-1,0),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),11),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC'))]))
    e.append(tbl)
    e.append(sp(20))

    # Certificate
    e.append(PageBreak())
    cert=Table([['ROYAL FITNESS CLUB\nNUTRITION & HEALTHY EATING CERTIFICATE']],colWidths=[W-40*mm])
    cert.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),RFC_DARK),('TEXTCOLOR',(0,0),(-1,-1),RFC_WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),18),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),22),('BOTTOMPADDING',(0,0),(-1,-1),22)]))
    e.append(cert)
    e.append(HRFlowable(width='100%',thickness=3,color=RFC_GOLD))
    e.append(sp(16))
    e.append(Paragraph('This certifies that',ParagraphStyle('ct',fontName='Helvetica',fontSize=14,textColor=RFC_DARK,alignment=TA_CENTER,leading=20)))
    e.append(Paragraph('_______________________________________',ParagraphStyle('line',fontName='Helvetica-Bold',fontSize=22,textColor=RFC_DARK,alignment=TA_CENTER,leading=30,spaceAfter=8)))
    e.append(Paragraph('has completed the',ParagraphStyle('ct2',fontName='Helvetica',fontSize=14,textColor=RFC_DARK,alignment=TA_CENTER,leading=20)))
    e.append(Paragraph('Nutrition & Healthy Eating Certificate — CS_B2',ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=17,textColor=RFC_GREEN,alignment=TA_CENTER,leading=24,spaceBefore=8,spaceAfter=12)))
    e.append(Paragraph('demonstrating comprehensive knowledge of macronutrients, micronutrients, Indian superfoods,\nmeal planning, metabolism, sports nutrition, and evidence-based supplementation.',
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

gen_b2_m1(); gen_b2_m2(); gen_b2_m3(); gen_b2_m4()
gen_b2_m5(); gen_b2_m6(); gen_b2_m7(); gen_b2_m8()
print('cs_b2 ALL 8 MODULES COMPLETE.')
