"""Generate all 20 catalog PDFs with dark navy theme."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os

OUT = '/home/user/royal-fitness-club/generated_pdfs'
DARK = colors.HexColor('#020b18')
NAVY = colors.HexColor('#0a0f1a')
NAVY2 = colors.HexColor('#0d1a2a')
BLUE = colors.HexColor('#0066cc')
BLUE2 = colors.HexColor('#0052a3')
GOLD = colors.HexColor('#ffd000')
LGREY = colors.HexColor('#cccccc')
MGREY = colors.HexColor('#888888')
WHITE = colors.white
CYAN = colors.HexColor('#38bdf8')
GREEN = colors.HexColor('#22c55e')
RED = colors.HexColor('#ef4444')

W, H = A4

def dark_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.restoreState()

def st():
    s = getSampleStyleSheet()
    d = {
        'Cover1': dict(fontName='Helvetica-Bold', fontSize=32, textColor=WHITE, alignment=TA_CENTER, spaceAfter=6, leading=40),
        'Cover2': dict(fontName='Helvetica-Bold', fontSize=16, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4, leading=22),
        'Cover3': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, alignment=TA_CENTER, spaceAfter=4, leading=15),
        'CoverBig': dict(fontName='Helvetica-Bold', fontSize=48, textColor=GOLD, alignment=TA_CENTER, spaceAfter=0, leading=56),
        'ChHead': dict(fontName='Helvetica-Bold', fontSize=14, textColor=BLUE, spaceBefore=12, spaceAfter=7, leading=19),
        'SecHead': dict(fontName='Helvetica-Bold', fontSize=11, textColor=WHITE, spaceBefore=8, spaceAfter=4, leading=16),
        'Body': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=5, leading=16, alignment=TA_JUSTIFY),
        'Blt': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15, leftIndent=14, firstLineIndent=-10),
        'Callout': dict(fontName='Helvetica-BoldOblique', fontSize=10, textColor=GOLD, spaceBefore=5, spaceAfter=5, leading=16, leftIndent=10, rightIndent=10),
        'Quote': dict(fontName='Helvetica-Oblique', fontSize=11, textColor=CYAN, spaceBefore=7, spaceAfter=7, leading=18, leftIndent=20, rightIndent=20, alignment=TA_CENTER),
        'TOCItem': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15),
        'GreenTxt': dict(fontName='Helvetica-Bold', fontSize=10, textColor=GREEN, spaceAfter=3, leading=15),
        'RedTxt': dict(fontName='Helvetica-Bold', fontSize=10, textColor=RED, spaceAfter=3, leading=15),
        'Badge': dict(fontName='Helvetica-Bold', fontSize=9, textColor=DARK, alignment=TA_CENTER, spaceAfter=2, leading=13),
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
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[NAVY2, NAVY]),
        ('TEXTCOLOR',(0,1),(-1,-1),LGREY),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#1a3a5a')),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(t); story.append(Spacer(1, 3*mm))

def hr(story): story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#1a3a5a'), spaceBefore=4, spaceAfter=4))
def ghr(story): story.append(HRFlowable(width='60%', thickness=1.5, color=GOLD, spaceBefore=6, spaceAfter=6))
def bl(story, s, items):
    for i in items: story.append(Paragraph(f'• {i}', s['Blt']))
def co(story, s, t): story.append(Paragraph(f'💡 {t}', s['Callout']))
def qt(story, s, t): story.append(Paragraph(f'"{t}"', s['Quote']))
def sp(story, n=4): story.append(Spacer(1, n*mm))

def cover(story, s, num, title, subtitle, tags):
    sp(story, 20)
    story.append(Paragraph('ROYAL FITNESS CLUB', s['Cover3']))
    sp(story, 3)
    story.append(Paragraph(f'<font color="#ffd000">RFC</font> PREMIUM GUIDE #{num:02d}', s['Cover3']))
    sp(story, 8)
    story.append(HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=8))
    story.append(Paragraph(title.upper(), s['Cover1']))
    sp(story, 4)
    story.append(Paragraph(subtitle, s['Cover2']))
    sp(story, 6)
    story.append(HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=8))
    sp(story, 4)
    tag_str = '  ·  '.join(tags)
    story.append(Paragraph(tag_str, s['Cover3']))
    sp(story, 4)
    story.append(Paragraph('© Royal Fitness Club — For Members Only', s['Cover3']))
    story.append(PageBreak())

def toc(story, s, chapters):
    story.append(Paragraph('TABLE OF CONTENTS', s['ChHead']))
    hr(story)
    sp(story, 2)
    for i, (ch, pg) in enumerate(chapters, 1):
        dots = '·' * max(2, 55 - len(ch) - len(str(pg)))
        story.append(Paragraph(f'Chapter {i} — {ch}  {dots}  {pg}', s['TOCItem']))
    sp(story, 6)
    story.append(Paragraph('DISCLAIMER', s['ChHead']))
    hr(story)
    story.append(Paragraph('This guide is for educational purposes only and does not constitute medical or professional advice. Always consult a qualified healthcare provider before starting any supplementation, pharmaceutical, or training protocol. All information is provided for harm-reduction and educational purposes. Individual results vary.', s['Body']))
    story.append(PageBreak())

def mk(path, num, title, subtitle, tags, chapters_fn):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = st(); story = []
    cover(story, s, num, title, subtitle, tags)
    chapters_fn(story, s)
    doc.build(story, onFirstPage=dark_bg, onLaterPages=dark_bg)
    print(f'  ✓ {os.path.basename(path)}')

# ─── PDF 01 — Advanced Cutting Cycle 12 Weeks ────────────────────────────────
def pdf01(story, s):
    toc(story, s, [
        ('Cycle Architecture & Goals', 3),
        ('Week 1–4: Foundation Phase', 4),
        ('Week 5–8: Peak Intensity Phase', 5),
        ('Week 9–12: Hardening & Finish', 6),
        ('Nutrition Protocol', 7),
        ('Side Effect Management', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — CYCLE ARCHITECTURE & GOALS', s['ChHead']))
    hr(story)
    qt(story, s, 'A cutting cycle is not about losing weight — it is about revealing the muscle you have already built.')
    story.append(Paragraph('This 12-week advanced cutting cycle is designed for experienced users who have completed at least two previous anabolic cycles. The primary objective is maximal fat loss while preserving lean muscle tissue. Caloric deficit, high-protein nutrition, and precise compound selection work together to achieve a hard, vascular, competition-ready physique.', s['Body']))
    story.append(Paragraph('Compounds Used', s['SecHead']))
    tb(story, ['Compound', 'Dose', 'Frequency', 'Purpose'],
       [['Testosterone Propionate', '100mg EOD', 'Every other day', 'Muscle preservation base'],
        ['Trenbolone Acetate', '75–100mg EOD', 'Every other day', 'Fat oxidation, hardening'],
        ['Masteron Propionate', '100mg EOD', 'Every other day', 'Anti-estrogen, density'],
        ['Anavar (Oxandrolone)', '50mg/day', 'Oral daily', 'Strength preservation'],
        ['Winstrol (Stanozolol)', '25–50mg/day (wk 9-12)', 'Oral/injectable', 'Final hardening effect']],
       widths=[120, 70, 90, 145])
    co(story, s, 'Stacking Masteron eliminates the need for an AI in most users — its DHT derivative nature suppresses aromatisation naturally.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — WEEK 1–4: FOUNDATION PHASE', s['ChHead']))
    hr(story)
    story.append(Paragraph('The first four weeks establish the hormonal environment for fat loss. Begin with a 500 kcal daily deficit and introduce compounds at the lower end of dosing ranges to assess individual response.', s['Body']))
    tb(story, ['Week', 'Test P', 'Tren A', 'Masteron P', 'Calories', 'Key Focus'],
       [['1', '100mg EOD', '75mg EOD', '100mg EOD', 'Deficit 400', 'Acclimatisation'],
        ['2', '100mg EOD', '75mg EOD', '100mg EOD', 'Deficit 500', 'Cardio 4×/wk'],
        ['3', '100mg EOD', '100mg EOD', '100mg EOD', 'Deficit 550', 'Training intensity ↑'],
        ['4', '100mg EOD', '100mg EOD', '100mg EOD', 'Deficit 550', 'Assess body composition']],
       widths=[40, 80, 80, 90, 80, 105])
    bl(story, s, [
        'Morning fasted cardio 30 min (LISS) 4 days/week from Week 1',
        'Training: Push/Pull/Legs split, 5 days/week, RPE 8–9',
        'Protein: minimum 2.5g per kg bodyweight daily',
        'Water intake: 4–5 litres per day; electrolytes critical with Tren',
        'Sleep: 7–8 hours; Tren suppresses deep sleep in some users — melatonin 1mg helps',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — WEEK 5–8: PEAK INTENSITY', s['ChHead']))
    hr(story)
    story.append(Paragraph('Weeks 5–8 represent the peak of both training intensity and caloric restriction. The physique should begin showing visible enhancement. Cardio volume increases and water manipulation techniques are introduced.', s['Body']))
    tb(story, ['Week', 'Tren A', 'Cardio', 'Deficit', 'Water (L)', 'Addition'],
       [['5', '100mg EOD', '5×30min LISS', '600 kcal', '5L', 'Anavar 50mg/day'],
        ['6', '100mg EOD', '5×30min LISS', '600 kcal', '5L', 'Continue Anavar'],
        ['7', '100mg EOD', '3 LISS + 2 HIIT', '600 kcal', '4.5L', 'Monitor bloods'],
        ['8', '100mg EOD', '3 LISS + 2 HIIT', '700 kcal', '4L', 'Progress photos']],
       widths=[40, 80, 100, 80, 70, 105])
    co(story, s, 'HIIT sessions: 20 minutes, 30s all-out / 90s recovery × 10 rounds. Do NOT do HIIT the day after heavy leg training.')
    bl(story, s, [
        'Add T3 (Liothyronine) 25–50mcg if fat loss stalls for more than 10 days',
        'Clenbuterol 40–120mcg/day (2-weeks-on / 2-weeks-off protocol optional)',
        'Reduce training volume by 10% to compensate for caloric deficit — intensity stays high',
        'Check hematocrit at Week 8 blood panel — Tren increases RBC significantly',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — WEEK 9–12: HARDENING & FINISH', s['ChHead']))
    hr(story)
    qt(story, s, 'The final four weeks separate the committed from the casual. This phase demands discipline that most will not match.')
    story.append(Paragraph('The final phase introduces Winstrol for a finishing effect — increased vascularity, joint tightness, and an extremely hard, dry look. Carbohydrate cycling is implemented for final conditioning.', s['Body']))
    tb(story, ['Day Type', 'Carbs (g)', 'Protein (g)', 'Fat (g)', 'Total Kcal', 'Training'],
       [['High Carb', '250', '280', '50', '2580', 'Legs / Back'],
        ['Moderate Carb', '150', '280', '60', '2220', 'Chest / Shoulders'],
        ['Low Carb', '60', '300', '70', '2050', 'Arms / Cardio'],
        ['Zero Carb', '20', '320', '80', '2080', 'Rest / Cardio only']],
       widths=[80, 65, 80, 60, 80, 110])
    co(story, s, 'Winstrol dries joints significantly. Use Glucosamine 1500mg + Chondroitin 1200mg + Fish Oil 4g daily throughout this phase.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — NUTRITION PROTOCOL', s['ChHead']))
    hr(story)
    story.append(Paragraph('Advanced Macro Blueprint', s['SecHead']))
    tb(story, ['Macronutrient', 'Target', 'Best Sources', 'Timing'],
       [['Protein', '2.5–3g/kg BW', 'Chicken, eggs, whey, paneer', 'Every 3–4 hours'],
        ['Carbohydrates', '1.5–2g/kg BW', 'Rice, sweet potato, oats', 'Pre/post training only'],
        ['Fats', '0.8–1g/kg BW', 'Almonds, olive oil, avocado', 'Morning and evening'],
        ['Fibre', '30–40g/day', 'Vegetables, flaxseed', 'With every meal'],
        ['Water', '4–5L/day', 'Plain water, electrolytes', 'Consistent throughout']],
       widths=[100, 80, 130, 115])
    story.append(Paragraph('Key Supplements', s['SecHead']))
    bl(story, s, [
        'Whey Isolate: 30–40g post-workout and between meals',
        'Creatine Monohydrate: 5g daily (maintain strength during cut)',
        'BCAA: 10g intra-workout',
        'Multivitamin + Vitamin D3 5000IU + Zinc 25mg',
        'Liv52 or TUDCA 500mg/day for hepatoprotection (oral compounds)',
        'N-Acetyl Cysteine (NAC) 600mg twice daily — antioxidant, liver support',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — SIDE EFFECT MANAGEMENT', s['ChHead']))
    hr(story)
    tb(story, ['Side Effect', 'Compound', 'Management', 'When to Seek Help'],
       [['Night sweats', 'Trenbolone', 'Cool room, moisture-wicking sheets', 'If fever > 38°C'],
        ['Hair thinning', 'All DHT compounds', 'Nizoral shampoo, finasteride (off-cycle)', 'If rapid shedding'],
        ['Acne', 'Tren, Mast, Var', 'Salicylic acid wash, doxycycline', 'If cystic, see dermatologist'],
        ['Aggression', 'Trenbolone', 'Mindfulness, reduce dose', 'If affects relationships'],
        ['Cardiovascular', 'All compounds', 'Cardio, omega-3 4g, CoQ10 200mg', 'Chest pain — ER immediately'],
        ['Insomnia', 'Trenbolone', 'Melatonin 1mg, no stimulants after 2pm', 'If persists > 2 weeks']],
       widths=[90, 80, 130, 125])
    co(story, s, 'Run bloods at Week 0, Week 8, and 4 weeks post-cycle PCT. Minimum panel: CBC, CMP, lipids, PSA, testosterone (total + free), LH, FSH, estradiol.')
    qt(story, s, 'Blood work is not optional — it is the feedback system that keeps you safe and progressing.')

mk(os.path.join(OUT, '01_Advanced_Cutting_Cycle_12Weeks.pdf'), 1,
   'Advanced Cutting Cycle', '12-Week Protocol for Maximum Definition',
   ['12 Weeks', '6 Chapters', 'Advanced Level', 'Competition Ready'], pdf01)

# ─── PDF 02 — Advanced Bulking Cycle with Peptides ───────────────────────────
def pdf02(story, s):
    toc(story, s, [
        ('Bulking Cycle Overview & Compound Selection', 3),
        ('Peptide Integration Protocol', 4),
        ('Week-by-Week Training Schedule', 5),
        ('Caloric Surplus & Macros', 6),
        ('Recovery Optimisation', 7),
        ('Cycle End Assessment', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — BULKING CYCLE OVERVIEW', s['ChHead']))
    hr(story)
    qt(story, s, 'Mass is built in surplus, revealed in deficit. The quality of your bulk determines the quality of your cut.')
    story.append(Paragraph('This advanced 16-week bulking cycle pairs traditional anabolic compounds with growth-hormone-releasing peptides (GHRPs and GHRHs) for maximal lean mass accrual with minimal fat gain. Peptide use allows a more controlled hormonal environment, supporting IGF-1 elevation, improved sleep, and enhanced recovery alongside the traditional compounds.', s['Body']))
    tb(story, ['Compound', 'Dose', 'Frequency', 'Role'],
       [['Testosterone Enanthate', '500–750mg/wk', 'Mon + Thu', 'Mass base'],
        ['Deca-Durabolin (NPP)', '400mg/wk', 'Mon + Thu', 'Joint support, mass'],
        ['Dianabol (Methandrostenolone)', '30–50mg/day', 'Daily oral (wk 1–6)', 'Fast-start kickstart'],
        ['GHRP-6 or Ipamorelin', '100–200mcg', '3× daily subQ', 'GH pulse, hunger stimulation'],
        ['CJC-1295 (no DAC)', '100mcg', '3× daily with GHRP', 'GHRH synergy'],
        ['Mk-677 (Ibutamoren)', '12.5–25mg/day', 'Oral nightly', 'GH secretagogue, sleep quality']],
       widths=[130, 80, 100, 115])
    co(story, s, 'Peptides are injected subcutaneously in the abdomen, 20 minutes before meals and before bed. Use bacteriostatic water for reconstitution.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — PEPTIDE INTEGRATION PROTOCOL', s['ChHead']))
    hr(story)
    story.append(Paragraph('GH-releasing peptides work synergistically — a GHRP creates a pulse, while a GHRH (like CJC-1295) amplifies its magnitude. The combined effect can increase GH pulse amplitude by 4–10× baseline.', s['Body']))
    tb(story, ['Time', 'Peptide', 'Dose', 'Notes'],
       [['6:30 AM (fasted)', 'GHRP-6 + CJC-1295', '100mcg each', 'Pre-breakfast, potentiates GH'],
        ['Post-training', 'Ipamorelin + CJC-1295', '150mcg each', 'Anabolic window amplification'],
        ['11:00 PM (pre-sleep)', 'Ipamorelin + CJC-1295', '100mcg each', 'Sleep GH pulse — do not eat 2h before']],
       widths=[120, 120, 80, 105])
    bl(story, s, [
        'Store reconstituted peptides at 2–8°C; use within 28 days',
        'GHRP-6 causes significant hunger — time injection before a large meal intentionally',
        'Ipamorelin is hunger-neutral — preferred for users who struggle with appetite control',
        'MK-677 causes water retention and may increase fasting glucose — monitor if diabetic risk',
        'IGF-1 bloods at baseline and Week 8 to confirm peptide efficacy',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — WEEK-BY-WEEK TRAINING', s['ChHead']))
    hr(story)
    tb(story, ['Weeks', 'Split', 'Volume', 'Key Lifts', 'Recovery'],
       [['1–4', 'PPL 6 days', 'Moderate (12–16 sets)', 'Squat, Bench, Deadlift', 'Full rest Sunday'],
        ['5–8', 'PPL + Arms', 'High (16–20 sets)', 'Add heavy Romanian DL', 'Deload Sat'],
        ['9–12', 'Upper/Lower 4 days', 'Very high (20+ sets)', 'Maximum load progressive', 'Active recovery 3 days'],
        ['13–16', 'PPL + Specialisation', 'High with intensity', 'Weak point focus', 'Strategic deload wk 15']],
       widths=[60, 90, 100, 140, 85])
    co(story, s, 'Progressive overload is the single non-negotiable variable. If you are not adding weight or reps each week, your nutrition is the problem — not the training.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — CALORIC SURPLUS & MACROS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Bulk Phase Macro Targets', s['SecHead']))
    tb(story, ['Body Weight', 'TDEE Estimate', 'Surplus', 'Protein', 'Carbs', 'Fats'],
       [['70kg', '3000 kcal', '+500 = 3500', '210g', '490g', '80g'],
        ['80kg', '3400 kcal', '+500 = 3900', '240g', '550g', '90g'],
        ['90kg', '3800 kcal', '+600 = 4400', '270g', '630g', '100g'],
        ['100kg', '4200 kcal', '+600 = 4800', '300g', '700g', '110g']],
       widths=[70, 80, 100, 70, 70, 70])
    bl(story, s, [
        'Eat every 3 hours — 5–6 meals. Anabolic hormones demand constant substrate delivery',
        'Indian bulk staples: rice, roti, daal, paneer, chicken, eggs, banana, full-fat milk',
        'Mass gainer only if reaching calorie targets from food alone is not feasible',
        'Creatine monohydrate: 5g daily (non-negotiable for mass phase)',
        'Digestive enzymes with large meals to improve nutrient assimilation',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — RECOVERY OPTIMISATION', s['ChHead']))
    hr(story)
    qt(story, s, 'Growth happens outside the gym. Recovery is not rest — it is the actual work.')
    tb(story, ['Recovery Tool', 'Frequency', 'Duration', 'Benefit'],
       [['Sleep', 'Every night', '8–9 hours', 'GH pulse, protein synthesis'],
        ['Foam Rolling', 'Post-training', '10–15 min', 'Fascial release, blood flow'],
        ['Contrast Shower', '4× per week', '10 min', 'Inflammation reduction'],
        ['Massage', 'Weekly', '60 min', 'Tissue quality, CNS recovery'],
        ['Deload Week', 'Every 4 weeks', '7 days 50% volume', 'Tendon, CNS restoration']],
       widths=[100, 90, 90, 145])
    co(story, s, 'Peptide-enhanced sleep quality should produce noticeably deeper, more restorative sleep within 2–3 weeks. If not, reassess dosing timing.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — CYCLE END ASSESSMENT', s['ChHead']))
    hr(story)
    story.append(Paragraph('Post-Cycle Metrics Checklist', s['SecHead']))
    bl(story, s, [
        'Body weight change — expected gain: 6–12kg total (3–5kg lean with clean bulk)',
        'Strength benchmarks — expect 10–20% increases on main lifts',
        'Body fat % — should remain within +2–3% of starting point with clean diet',
        'Waist measurement — if waist increased > 4cm, surplus was excessive',
        'Blood panel: testosterone (total + free), estradiol, LH, FSH, CBC, lipids, liver enzymes',
        'Blood pressure: target < 130/80 — if elevated, address before PCT',
    ])
    story.append(Paragraph('PCT Initiation Timeline', s['SecHead']))
    tb(story, ['Compound Last Injection', 'Wait Before PCT', 'PCT Protocol'],
       [['Test Enanthate (250mg)', '14–18 days', 'Clomid 50/50/25/25 + Nolvadex 40/40/20/20'],
        ['Deca (NPP)', '10–14 days', 'Extended PCT — 6 weeks minimum'],
        ['All peptides', 'Discontinue cycle end', 'Continue MK-677 through PCT (optional)']],
       widths=[150, 100, 175])

mk(os.path.join(OUT, '02_Advanced_Bulking_Cycle_with_Peptides.pdf'), 2,
   'Advanced Bulking Cycle with Peptides', '16-Week Mass Protocol + GHRP/GHRH Integration',
   ['16 Weeks', '6 Chapters', 'Advanced Level', 'Peptide Stack'], pdf02)

# ─── PDF 03 — Beginner Steroid Cycle Full Guide ───────────────────────────────
def pdf03(story, s):
    toc(story, s, [
        ('Is a Steroid Cycle Right for You?', 3),
        ('First Cycle: Testosterone Only Protocol', 4),
        ('Training Programme for Beginners', 5),
        ('Nutrition for Maximum Gains', 6),
        ('On-Cycle Support & Blood Work', 7),
        ('Post Cycle Therapy (PCT)', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — IS A STEROID CYCLE RIGHT FOR YOU?', s['ChHead']))
    hr(story)
    qt(story, s, 'The most dangerous cycle is the one entered without knowledge. Education is your best protection.')
    story.append(Paragraph('Before beginning any anabolic cycle, it is essential to complete a honest self-assessment. Anabolic steroids carry real risks that are amplified by insufficient natural training base, poor nutrition habits, inadequate sleep, and absence of medical monitoring. This guide is designed for harm reduction — to ensure that if someone is going to use, they do so with maximum safety.', s['Body']))
    story.append(Paragraph('Readiness Checklist', s['SecHead']))
    tb(story, ['Criterion', 'Minimum Requirement', 'Why It Matters'],
       [['Training age', '3+ years consistent resistance training', 'Maximise receptors, base strength'],
        ['Age', '23+ years (25+ recommended)', 'HPTA still developing before 23'],
        ['Blood work', 'Baseline panel completed', 'Know your starting point'],
        ['Body fat', '<20% male, <28% female', 'High BF = high aromatisation risk'],
        ['Nutrition knowledge', 'Macro tracking for 6+ months', 'Compounds amplify habits — good and bad'],
        ['Support person', 'Trusted person aware of cycle', 'Medical emergency preparedness']],
       widths=[100, 155, 170])
    co(story, s, 'If you cannot consistently gain muscle naturally, adding anabolic compounds will not solve the problem. Fix nutrition and training first.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — FIRST CYCLE: TESTOSTERONE ONLY', s['ChHead']))
    hr(story)
    story.append(Paragraph('The universally recommended first cycle is Testosterone Enanthate or Testosterone Cypionate, 400–500mg per week, for 12 weeks. This is not conservative advice — it is optimal advice. Testosterone is the foundation of all anabolic protocols and introducing multiple compounds simultaneously makes it impossible to identify the source of any side effect.', s['Body']))
    tb(story, ['Week', 'Testosterone E', 'Aromasin/Arimidex', 'HCG', 'Notes'],
       [['1–12', '250mg Mon + 250mg Thu', 'Only if gyno symptoms', '250IU 2×/wk (optional)', 'Assess response Week 3'],
        ['13–14', 'None', 'Continue if needed', 'Discontinue', 'Clearance period'],
        ['15–18 (PCT)', 'None', 'Taper off', 'None', 'Clomid + Nolvadex']],
       widths=[50, 130, 110, 100, 135])
    co(story, s, 'Do NOT take an AI (aromatase inhibitor) pre-emptively. Only introduce one if you develop gynaecological symptoms (itchy, tender nipples). Crashing estrogen is worse than elevated estrogen.')
    bl(story, s, [
        'Inject with a 23-gauge 1.5" needle into the gluteus medius or ventral gluteus',
        'Rotate injection sites every time — build a 4-site rotation minimum',
        'Aspirate optional but a good habit for new users',
        'Warm the oil to body temperature before injection (hold in hands 2 minutes)',
        'Draw with an 18G needle, swap to 23G for injection — keep everything sterile',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — TRAINING FOR BEGINNERS ON CYCLE', s['ChHead']))
    hr(story)
    story.append(Paragraph('On-cycle beginner training should be higher volume than natural training, but not recklessly so. The biggest mistake beginners make is insufficient volume — muscles on cycle can tolerate and require more stimulus. The second mistake is insufficient recovery — you are not recovering faster on cycle unless you are also sleeping and eating correctly.', s['Body']))
    tb(story, ['Day', 'Muscle Group', 'Sets', 'Rep Range', 'Rest'],
       [['Monday', 'Chest + Triceps', '16–18', '8–12', '90 sec'],
        ['Tuesday', 'Back + Biceps', '16–18', '8–12', '90 sec'],
        ['Wednesday', 'Legs + Calves', '18–20', '8–15', '2 min'],
        ['Thursday', 'Shoulders + Traps', '14–16', '10–15', '90 sec'],
        ['Friday', 'Arms + Forearms', '14–16', '10–15', '75 sec'],
        ['Saturday', 'Weak points or cardio', '12–14', 'Mixed', '60–90 sec'],
        ['Sunday', 'Rest + mobility', '—', '—', '—']],
       widths=[75, 120, 50, 80, 60])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — NUTRITION FOR MAXIMUM GAINS', s['ChHead']))
    hr(story)
    qt(story, s, 'Your compounds are multipliers, not replacements. Multiply poor nutrition and you get amplified poor results.')
    tb(story, ['Meal', 'Timing', 'Composition', 'Approx Kcal'],
       [['Meal 1', '7:00 AM', '6 whole eggs + 2 roti + 1 banana', '650'],
        ['Meal 2', '10:30 AM', '200g chicken + 1 cup rice + salad', '550'],
        ['Pre-workout', '1:00 PM', '50g oats + 1 scoop whey + 1 apple', '450'],
        ['Post-workout', '4:00 PM', '2 scoops whey + 50g dextrose', '380'],
        ['Meal 5', '7:00 PM', '200g paneer/chicken + 2 roti + veg', '600'],
        ['Night meal', '10:00 PM', '250ml full fat milk + 30g casein', '320']],
       widths=[65, 70, 185, 75])
    story.append(Paragraph('Total: ~2950 kcal — adjust based on actual bodyweight and scale movement', s['Body']))
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — ON-CYCLE SUPPORT & BLOOD WORK', s['ChHead']))
    hr(story)
    tb(story, ['Supplement', 'Dose', 'Purpose', 'Timing'],
       [['Liv52 / TUDCA', '500mg TUDCA or 2 tabs Liv52', 'Liver protection', 'With meals'],
        ['Omega-3', '4g EPA/DHA combined', 'Lipid profile protection', 'With meals'],
        ['CoQ10', '200mg', 'Cardiovascular support', 'Morning'],
        ['Vitamin D3', '5000 IU', 'Hormonal support, immunity', 'Morning with fat'],
        ['Zinc', '25mg', 'Testosterone co-factor', 'Before bed'],
        ['NAC', '600mg twice daily', 'Liver + antioxidant', 'Morning + evening'],
        ['Hawthorn Berry', '500mg', 'Blood pressure management', 'Morning']],
       widths=[100, 130, 130, 65])
    co(story, s, 'Blood work protocol: Pre-cycle baseline → Week 6 check → 4 weeks post-PCT. This 3-point system catches problems early and confirms recovery.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — POST CYCLE THERAPY (PCT)', s['ChHead']))
    hr(story)
    story.append(Paragraph('PCT begins 14–18 days after the last testosterone injection (for Enanthate/Cypionate). Do not start PCT earlier — residual testosterone will suppress endogenous recovery.', s['Body']))
    tb(story, ['PCT Week', 'Clomid', 'Nolvadex (Tamoxifen)', 'Notes'],
       [['Week 1', '50mg/day', '40mg/day', 'Expect lethargy, low libido — normal'],
        ['Week 2', '50mg/day', '40mg/day', 'Mood fluctuation peaks this week'],
        ['Week 3', '25mg/day', '20mg/day', 'Energy begins returning'],
        ['Week 4', '25mg/day', '20mg/day', 'Final week — bloods 4 weeks after']],
       widths=[80, 100, 120, 175])
    bl(story, s, [
        'Maintain training intensity and volume through PCT — muscle loss is hormonal + training deficit combined',
        'Caloric surplus or maintenance through PCT — now is not the time to cut',
        'Avoid alcohol completely during PCT — liver is processing PCT drugs AND recovering',
        'Zinc, Vitamin D, ashwagandha all support natural testosterone recovery',
        'If bloods show testosterone below 300ng/dL at 8 weeks post-PCT, see an endocrinologist',
    ])
    qt(story, s, 'PCT is not the end of the cycle — it is the most important part of it. Skip it and you risk permanent HPTA suppression.')

mk(os.path.join(OUT, '03_Beginner_Steroid_Cycle_Full_Guide.pdf'), 3,
   'Beginner Steroid Cycle', 'Complete First-Cycle Guide with PCT & Blood Work Protocol',
   ['12 Weeks', '6 Chapters', 'Beginner Level', 'Safety First'], pdf03)

# ─── PDF 04 — 30-Day Keto Indian Vegetarian Plan ─────────────────────────────
def pdf04(story, s):
    toc(story, s, [
        ('Ketogenic Diet Fundamentals', 3),
        ('Indian Vegetarian Keto Food List', 4),
        ('Week 1–2 Meal Plans', 5),
        ('Week 3–4 Meal Plans', 6),
        ('Keto Flu & Electrolyte Management', 7),
        ('Progress Tracking & Adjustments', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — KETOGENIC DIET FUNDAMENTALS', s['ChHead']))
    hr(story)
    qt(story, s, 'Ketosis is a metabolic state, not a diet trend. It is how your body has operated for the majority of human history.')
    story.append(Paragraph('The ketogenic diet shifts the body from carbohydrate-based energy production to fat-based. When carbohydrate intake falls below approximately 20–50g of net carbs per day, the liver converts fatty acids into ketone bodies (primarily beta-hydroxybutyrate) which serve as an efficient fuel for the brain and muscles. This state — nutritional ketosis — typically takes 2–7 days to achieve and results in accelerated fat oxidation.', s['Body']))
    tb(story, ['Macronutrient', 'Standard Diet', 'Ketogenic Diet', 'Indian Vegetarian Keto'],
       [['Fat', '25–35%', '65–75%', '70% (paneer, ghee, nuts, coconut)'],
        ['Protein', '15–25%', '20–25%', '22% (paneer, daal, Greek yoghurt, eggs)'],
        ['Carbohydrates', '45–60%', '5–10%', '8% (20–30g net carbs/day)'],
        ['Fibre', '25g/day', '25g/day', 'From keto vegetables only']],
       widths=[105, 85, 100, 135])
    co(story, s, 'For vegetarians: Paneer, full-fat Greek yoghurt, heavy cream, ghee, coconut oil, nuts, seeds, and low-carb vegetables are your foundation foods.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — INDIAN VEGETARIAN KETO FOOD LIST', s['ChHead']))
    hr(story)
    story.append(Paragraph('EAT FREELY — High Fat, Low Carb', s['SecHead']))
    tb(story, ['Category', 'Foods', 'Typical Net Carbs'],
       [['Dairy & Eggs', 'Paneer, full-fat yoghurt, ghee, heavy cream, butter, eggs', '1–3g per serving'],
        ['Oils & Fats', 'Coconut oil, mustard oil, olive oil, sesame oil', '0g'],
        ['Nuts & Seeds', 'Almonds, walnuts, macadamia, flaxseed, chia, pumpkin seeds', '2–5g per 30g'],
        ['Vegetables', 'Spinach, cauliflower, broccoli, cabbage, zucchini, cucumber, mushrooms', '2–6g per cup'],
        ['Condiments', 'Turmeric, cumin, coriander, ginger, garlic, coconut cream', '<3g per serving']],
       widths=[100, 205, 120])
    story.append(Paragraph('AVOID — High Carb Foods', s['SecHead']))
    tb(story, ['Food Group', 'Examples', 'Why Avoid'],
       [['Grains', 'Rice, wheat, roti, bread, pasta, oats, poha, upma', 'Immediate glucose spike, exits ketosis'],
        ['Legumes', 'All daal, chana, rajma, moong (high-carb)', 'Despite protein content, too many carbs'],
        ['Fruit', 'Mango, banana, grapes, apple, papaya', 'High fructose — anti-ketogenic'],
        ['Root Vegetables', 'Potato, sweet potato, carrot, beetroot', 'Starchy carbohydrates']],
       widths=[100, 200, 125])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — WEEK 1–2 MEAL PLANS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Week 1: Keto Adaptation', s['SecHead']))
    tb(story, ['Day', 'Breakfast', 'Lunch', 'Dinner', 'Net Carbs'],
       [['Mon', 'Paneer bhurji (3 eggs) + tea with cream', 'Palak paneer + salad', 'Cauliflower rice + stir-fry', '18g'],
        ['Tue', 'Avocado + 2 boiled eggs + coffee with coconut oil', 'Paneer tikka + cucumber raita', 'Broccoli paneer curry', '20g'],
        ['Wed', 'Coconut flour pancakes + ghee', 'Tofu stir-fry with spinach', 'Egg curry (no potato)', '22g'],
        ['Thu', 'Full-fat yoghurt + chia seeds + walnuts', 'Paneer salad + olive oil dressing', 'Zucchini with paneer', '19g'],
        ['Fri', 'Scrambled eggs (4) + mushrooms in butter', 'Cauliflower soup + paneer', 'Mixed vegetable curry (keto)', '21g']],
       widths=[40, 125, 110, 125, 55])
    co(story, s, 'Week 1 keto flu is real — see Chapter 5. Increase salt, potassium, and magnesium aggressively during days 3–7.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — WEEK 3–4 MEAL PLANS', s['ChHead']))
    hr(story)
    story.append(Paragraph('By Week 3, you should be fully keto-adapted: energy stable, cravings minimal, mental clarity improved. This phase targets deeper fat burning.', s['Body']))
    tb(story, ['Meal', 'Options', 'Approx Kcal', 'Net Carbs'],
       [['Breakfast', 'Paneer omelette (150g paneer + 3 eggs)', '520', '4g'],
        ['Lunch', 'Keto thali: palak paneer + cauliflower sabzi + raita', '580', '12g'],
        ['Snack', '30g walnuts + 1 tbsp peanut butter (no sugar)', '260', '4g'],
        ['Dinner', 'Grilled paneer + sautéed spinach + coconut chutney', '490', '8g'],
        ['Night', '200ml coconut milk + 1 tbsp chia seeds', '170', '4g']],
       widths=[80, 175, 80, 70])
    story.append(Paragraph('Total: ~2020 kcal, ~32g net carbs', s['Body']))
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — KETO FLU & ELECTROLYTE MANAGEMENT', s['ChHead']))
    hr(story)
    qt(story, s, 'Keto flu is not your body rejecting ketosis — it is your kidneys adjusting to insulin reduction. The fix is electrolytes, not carbohydrates.')
    tb(story, ['Electrolyte', 'Keto Daily Target', 'Best Sources', 'Deficiency Symptoms'],
       [['Sodium', '3000–5000mg', 'Salt, salted nuts, pickle', 'Headache, fatigue, brain fog'],
        ['Potassium', '3000–4000mg', 'Avocado, spinach, mushrooms', 'Muscle cramps, palpitations'],
        ['Magnesium', '300–500mg', 'Almonds, dark chocolate (90%+), supplement', 'Insomnia, cramps, anxiety'],
        ['Phosphorus', '700mg', 'Paneer, nuts, seeds', 'Bone ache, weakness']],
       widths=[90, 100, 150, 135])
    co(story, s, 'Keto electrolyte drink recipe: 500ml water + ¼ tsp salt + ¼ tsp No Salt (potassium) + 200mg magnesium powder. Drink twice daily during Week 1–2.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — PROGRESS TRACKING', s['ChHead']))
    hr(story)
    tb(story, ['Week', 'Expected Fat Loss', 'Expected Adaptation', 'Measurement Method'],
       [['1', '1–3kg (mostly water)', 'Entering ketosis', 'Scale daily, average weekly'],
        ['2', '0.5–1kg true fat', 'Keto-adapted', 'Scale + waist measurement'],
        ['3', '0.5–1kg true fat', 'Full adaptation', 'Scale + body fat % (calipers)'],
        ['4', '0.5–1kg true fat', 'Optimised fat burning', 'Full measurements + photos']],
       widths=[60, 110, 110, 145])
    bl(story, s, [
        'Take measurements on the same morning, same conditions, same day of week',
        'Progress photos: same pose, same lighting, same time of day (morning, fasted)',
        'Energy levels are the most reliable real-time indicator of ketosis quality',
        'If fat loss stalls: check for hidden carbs in condiments and sauces',
        'Test ketones: urine strips (cheap, less accurate) or blood meter (gold standard, target 0.5–3 mmol/L)',
    ])

mk(os.path.join(OUT, '04_30Day_Keto_Indian_Vegetarian_Plan.pdf'), 4,
   '30-Day Keto Indian Vegetarian Plan', 'Ketogenic Diet Protocol Adapted for Indian Cuisine',
   ['30 Days', '6 Chapters', 'All Levels', 'Vegetarian Friendly'], pdf04)

# ─── PDF 05 — Female Vegetarian Weight Loss Plan ─────────────────────────────
def pdf05(story, s):
    toc(story, s, [
        ('Female Physiology & Fat Loss Differences', 3),
        ('Caloric & Macro Blueprint for Women', 4),
        ('12-Week Training Programme', 5),
        ('Hormonal Health & Cycle Syncing', 6),
        ('Vegetarian Meal Plan (4 Weeks)', 7),
        ('Mindset, Plateaus & Long-Term Strategy', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — FEMALE PHYSIOLOGY & FAT LOSS', s['ChHead']))
    hr(story)
    qt(story, s, 'Fat loss for women is a hormonal event as much as a caloric one. Treat it that way and the results become dramatically more predictable.')
    story.append(Paragraph('Female fat loss differs from male fat loss in several key ways. Women have approximately 40–60% lower testosterone, meaning muscle building and fat loss from resistance training occurs more slowly. Women carry proportionally more alpha-2 adrenergic receptors in hip, thigh, and gluteal fat — these receptors resist fat mobilisation, creating the stubborn lower-body fat that characterises female physiology. Understanding these differences prevents frustration and informs strategy.', s['Body']))
    tb(story, ['Variable', 'Female Physiology', 'Strategy Implication'],
       [['Testosterone', '15–70 ng/dL (vs 300–1000 male)', 'Resistance training essential — more critical than for men'],
        ['Oestrogen', 'Cyclical, protective of muscle', 'Leverage follicular phase for high intensity'],
        ['Cortisol sensitivity', 'Higher, especially under restriction', 'Avoid extreme deficits; 300–400 kcal max'],
        ['Fat distribution', 'Gluteofemoral > visceral', 'Lower body fat mobilises last — patience required'],
        ['Metabolic rate', '5–10% lower than male at same weight', 'Accurate TDEE calculation critical']],
       widths=[100, 155, 170])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — CALORIC & MACRO BLUEPRINT', s['ChHead']))
    hr(story)
    tb(story, ['Weight', 'Est. TDEE (Moderate)', 'Deficit', 'Protein', 'Carbs', 'Fats'],
       [['55kg', '1900 kcal', '−350 = 1550', '130g', '160g', '55g'],
        ['65kg', '2100 kcal', '−400 = 1700', '150g', '180g', '60g'],
        ['75kg', '2300 kcal', '−400 = 1900', '170g', '200g', '65g'],
        ['85kg', '2500 kcal', '−450 = 2050', '185g', '215g', '70g']],
       widths=[70, 110, 100, 70, 70, 70])
    co(story, s, 'Never go below 1200 kcal for women. Below this threshold, metabolic adaptation, hormonal disruption, and muscle loss become significant. A 300–400 kcal deficit is both sustainable and effective.')
    story.append(Paragraph('Top Vegetarian Protein Sources for Women', s['SecHead']))
    bl(story, s, [
        'Paneer: 18g protein per 100g — best single vegetarian protein source',
        'Greek yoghurt (full-fat): 10g per 100g — probiotic benefits for gut and hormone health',
        'Tofu (firm): 8g per 100g — complete amino acid profile',
        'Lentils (cooked daal): 9g per 100g — also high in iron critical for women',
        'Quinoa: 4g per 100g cooked — complete protein, all essential amino acids',
        'Chickpeas: 9g per 100g cooked — versatile, high satiety',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — 12-WEEK TRAINING PROGRAMME', s['ChHead']))
    hr(story)
    story.append(Paragraph('Phase 1: Foundation (Weeks 1–4)', s['SecHead']))
    tb(story, ['Day', 'Workout', 'Duration', 'Focus'],
       [['Mon', 'Full body resistance', '45 min', 'Compound movements, form'],
        ['Tue', 'Cardio (walking/cycling)', '30 min', 'Zone 2 fat burning'],
        ['Wed', 'Lower body resistance', '40 min', 'Glutes, hamstrings, quads'],
        ['Thu', 'Yoga / mobility', '30 min', 'Recovery, flexibility'],
        ['Fri', 'Upper body + core', '40 min', 'Shoulders, back, abs'],
        ['Sat', 'HIIT or dance cardio', '25 min', 'Calorie burn, fun'],
        ['Sun', 'Rest / light walk', '20 min', 'Recovery']],
       widths=[50, 130, 70, 175])
    co(story, s, 'Weeks 5–8: Increase resistance training to 4 days/week. Add a second HIIT session. Focus compound lifts: squats, Romanian deadlifts, hip thrusts, rows.')
    co(story, s, 'Weeks 9–12: Peak intensity. 4 resistance days + 2 cardio sessions. Progressive overload on every lift. Advanced HIIT 2× per week.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — HORMONAL HEALTH & CYCLE SYNCING', s['ChHead']))
    hr(story)
    qt(story, s, 'Your menstrual cycle is a performance asset, not a limitation — when you train and eat in sync with it.')
    tb(story, ['Cycle Phase', 'Days', 'Hormones', 'Recommended Training', 'Nutrition Tip'],
       [['Menstruation', '1–5', 'Low E + P', 'Light yoga, walking', 'Iron-rich foods, reduce salt'],
        ['Follicular', '6–13', 'Rising E', 'High intensity, heavy lifting', 'Moderate carbs, high protein'],
        ['Ovulation', '14', 'Peak E', 'Maximum performance week', 'Pre-workout carbs, push hard'],
        ['Luteal', '15–28', 'Rising P, falling E', 'Moderate intensity, pilates', 'Increase calories slightly, complex carbs']],
       widths=[80, 45, 80, 130, 140])
    bl(story, s, [
        'Iron supplementation for women who menstruate: 18mg/day (food-based preferred)',
        'Omega-3 (EPA/DHA): 2–3g/day reduces menstrual cramping and inflammation',
        'Magnesium glycinate 300mg: reduces PMS symptoms and improves sleep quality',
        'Calcium 500mg + Vitamin D3: critical for female bone density protection',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — VEGETARIAN MEAL PLAN', s['ChHead']))
    hr(story)
    tb(story, ['Meal', 'Example', 'Protein', 'Carbs', 'Fat', 'Kcal'],
       [['Breakfast', 'Moong dal chilla × 3 + curd', '22g', '40g', '8g', '320'],
        ['Mid-morning', 'Greek yoghurt + berries + flaxseed', '12g', '18g', '6g', '172'],
        ['Lunch', 'Rajma brown rice (small) + salad', '18g', '55g', '4g', '330'],
        ['Pre-workout', '1 banana + 10g peanut butter', '5g', '30g', '5g', '185'],
        ['Dinner', 'Palak tofu + 1 roti + cucumber raita', '20g', '35g', '10g', '310'],
        ['Night snack', '150ml warm milk + 1 tsp ashwagandha', '5g', '8g', '4g', '88']],
       widths=[80, 150, 55, 55, 45, 50])
    story.append(Paragraph('Total: ~1405 kcal — adjust portions to meet individual caloric target', s['Body']))
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — MINDSET & LONG-TERM STRATEGY', s['ChHead']))
    hr(story)
    qt(story, s, 'The scale is one data point. Progress photos, strength numbers, energy levels, and how your clothes fit are four more. Use all five.')
    bl(story, s, [
        'Expect 0.4–0.7kg fat loss per week — anything more is likely muscle + water + fat',
        'Strength gains in the gym confirm muscle preservation during fat loss — track your lifts',
        'Take a diet break at Week 8 (eat at maintenance for 7–10 days) to reset leptin and reduce adaptation',
        'Social eating: budget 300–400 kcal for eating out by reducing carbs at other meals that day',
        'Sleep 7–9 hours — this is as important as the diet and training. Seriously.',
        'Progress photos every 4 weeks, same conditions — comparison over 12 weeks reveals transformation',
    ])
    co(story, s, 'The 12-week programme is a starting point, not a destination. Women who see the best long-term results treat fitness as a permanent lifestyle, not a temporary project.')

mk(os.path.join(OUT, '05_Female_Vegetarian_Weight_Loss_Plan.pdf'), 5,
   'Female Vegetarian Weight Loss Plan', '12-Week Protocol Designed for Women\'s Physiology',
   ['12 Weeks', '6 Chapters', 'Female Specific', 'Hormone Optimised'], pdf05)

print('\n[PDFs 01-05 complete]')
