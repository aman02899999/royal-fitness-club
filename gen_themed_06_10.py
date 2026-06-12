"""Generate catalog PDFs 06-10 with dark navy theme."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

OUT = '/home/user/royal-fitness-club/generated_pdfs'
DARK = colors.HexColor('#020b18')
NAVY = colors.HexColor('#0a0f1a')
NAVY2 = colors.HexColor('#0d1a2a')
BLUE = colors.HexColor('#0066cc')
GOLD = colors.HexColor('#ffd000')
LGREY = colors.HexColor('#cccccc')
WHITE = colors.white
CYAN = colors.HexColor('#38bdf8')
GREEN = colors.HexColor('#22c55e')
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
        'ChHead': dict(fontName='Helvetica-Bold', fontSize=14, textColor=BLUE, spaceBefore=12, spaceAfter=7, leading=19),
        'SecHead': dict(fontName='Helvetica-Bold', fontSize=11, textColor=WHITE, spaceBefore=8, spaceAfter=4, leading=16),
        'Body': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=5, leading=16, alignment=TA_JUSTIFY),
        'Blt': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15, leftIndent=14, firstLineIndent=-10),
        'Callout': dict(fontName='Helvetica-BoldOblique', fontSize=10, textColor=GOLD, spaceBefore=5, spaceAfter=5, leading=16, leftIndent=10, rightIndent=10),
        'Quote': dict(fontName='Helvetica-Oblique', fontSize=11, textColor=CYAN, spaceBefore=7, spaceAfter=7, leading=18, leftIndent=20, rightIndent=20, alignment=TA_CENTER),
        'TOCItem': dict(fontName='Helvetica', fontSize=10, textColor=LGREY, spaceAfter=3, leading=15),
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
def bl(story, s, items):
    for i in items: story.append(Paragraph(f'• {i}', s['Blt']))
def co(story, s, t): story.append(Paragraph(f'💡 {t}', s['Callout']))
def qt(story, s, t): story.append(Paragraph(f'"{t}"', s['Quote']))
def sp(story, n=4): story.append(Spacer(1, n*mm))

def cover(story, s, num, title, subtitle, tags):
    sp(story, 20)
    story.append(Paragraph('ROYAL FITNESS CLUB', s['Cover3']))
    sp(story, 3)
    story.append(Paragraph(f'RFC PREMIUM GUIDE #{num:02d}', s['Cover3']))
    sp(story, 8)
    story.append(HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=8))
    story.append(Paragraph(title.upper(), s['Cover1']))
    sp(story, 4)
    story.append(Paragraph(subtitle, s['Cover2']))
    sp(story, 6)
    story.append(HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=8))
    sp(story, 4)
    story.append(Paragraph('  ·  '.join(tags), s['Cover3']))
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
    story.append(Paragraph('This guide is for educational and harm-reduction purposes only. It does not constitute medical advice. Consult a qualified healthcare professional before starting any supplementation or pharmaceutical protocol. Individual results vary.', s['Body']))
    story.append(PageBreak())

def mk(path, num, title, subtitle, tags, fn):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = st(); story = []
    cover(story, s, num, title, subtitle, tags)
    fn(story, s)
    doc.build(story, onFirstPage=dark_bg, onLaterPages=dark_bg)
    print(f'  ✓ {os.path.basename(path)}')

# ─── PDF 06 — Complete Peptide Protocol Bible ────────────────────────────────
def pdf06(story, s):
    toc(story, s, [
        ('What Are Peptides? Science & Mechanisms', 3),
        ('GHRP Family: Protocols & Dosing', 4),
        ('GHRH Analogues: CJC-1295 & Sermorelin', 5),
        ('IGF-1 & Insulin-Like Growth Factors', 6),
        ('Healing Peptides: BPC-157 & TB-500', 7),
        ('Stacking Guide & Safety', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — WHAT ARE PEPTIDES?', s['ChHead']))
    hr(story)
    qt(story, s, 'Peptides are the language your cells use to communicate. Learning this language lets you speak directly to your body\'s growth systems.')
    story.append(Paragraph('Peptides are short chains of amino acids (2–50 residues) that act as signalling molecules in the body. Unlike anabolic steroids, which directly bind to androgen receptors, therapeutic peptides typically work by stimulating the body\'s own hormone production pathways. This makes them both more targeted and, in most cases, safer in terms of hormonal suppression profiles. Growth-hormone-releasing peptides (GHRPs) and their analogues represent the most researched category for performance and body composition enhancement.', s['Body']))
    tb(story, ['Peptide Class', 'Mechanism', 'Primary Effect', 'Administration'],
       [['GHRP (e.g. GHRP-6, Ipamorelin)', 'Ghrelin receptor agonist', 'GH pulse stimulation', 'SubQ injection'],
        ['GHRH (e.g. CJC-1295)', 'GHRH receptor agonist', 'Amplifies GH pulse', 'SubQ injection'],
        ['IGF-1 LR3', 'IGF-1 receptor direct', 'Protein synthesis, muscle growth', 'SubQ/IM injection'],
        ['BPC-157', 'Multiple (tendon, GI, CNS)', 'Healing, anti-inflammatory', 'SubQ, oral, or IM'],
        ['TB-500 (Thymosin Beta-4)', 'Actin filament binding', 'Tissue repair, flexibility', 'SubQ injection'],
        ['Melanotan II', 'MC1-R / MC4-R agonist', 'Tanning, libido, appetite', 'SubQ injection']],
       widths=[130, 130, 110, 55])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — GHRP FAMILY PROTOCOLS', s['ChHead']))
    hr(story)
    story.append(Paragraph('GH-Releasing Peptide Comparison', s['SecHead']))
    tb(story, ['GHRP', 'Dose', 'Hunger Effect', 'Cortisol Effect', 'Best Use Case'],
       [['GHRP-2', '100–300mcg', 'Moderate', 'Moderate increase', 'Maximum GH pulse strength'],
        ['GHRP-6', '100–300mcg', 'Strong (very hungry)', 'Moderate increase', 'Bulking — hunger useful'],
        ['Ipamorelin', '100–300mcg', 'Minimal', 'Minimal increase', 'Cutting or lean bulk'],
        ['Hexarelin', '100–200mcg', 'Moderate', 'Low', 'Most potent GHRP available'],
        ['MK-677 (oral GHRP)', '12.5–25mg', 'Moderate', 'Minimal', 'Oral convenience, 24h GH elevation']],
       widths=[90, 80, 90, 90, 175])
    co(story, s, 'Ipamorelin is the most selective GHRP — it causes GH release without elevating cortisol, prolactin, or ACTH. It is the safest choice for long-term use and cutting protocols.')
    story.append(Paragraph('Standard Daily GHRP Protocol', s['SecHead']))
    bl(story, s, [
        'Injection 1: 6:30 AM fasted — GHRP + GHRH. Do not eat for 20 minutes before or after',
        'Injection 2: 30 min post-training — GHRP + GHRH. Amplifies anabolic window',
        'Injection 3: 11 PM pre-sleep — GHRP + GHRH. Maximises overnight GH pulse',
        'Each injection: 100mcg GHRP + 100mcg GHRH in same syringe (compatible)',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — GHRH ANALOGUES', s['ChHead']))
    hr(story)
    tb(story, ['GHRH Analogue', 'Half-Life', 'Dose', 'DAC Version', 'Key Difference'],
       [['CJC-1295 (no DAC)', '30 min', '100mcg per injection', 'No', 'Pulsatile release — mimics natural pattern'],
        ['CJC-1295 (with DAC)', '7–8 days', '2mg per week', 'Yes', 'Continuous elevation — blunts natural pulses'],
        ['Sermorelin', '10–20 min', '200–500mcg nightly', 'No', 'Most natural, weakest signal']],
       widths=[130, 75, 100, 60, 160])
    co(story, s, 'CJC-1295 without DAC is strongly preferred for performance use. The DAC version creates a "GH bleed" that disrupts the natural pulsatile pattern associated with optimal body composition.')
    bl(story, s, [
        'Always pair GHRH with a GHRP — they work synergistically (4–10× amplification)',
        'Do not use GHRH or GHRP within 2 hours of eating — insulin suppresses GH release',
        'Store reconstituted peptides in the refrigerator; bacteriostatic water extends shelf life to 4 weeks',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — IGF-1 & GROWTH FACTORS', s['ChHead']))
    hr(story)
    qt(story, s, 'IGF-1 is the downstream effector of GH — the molecule that actually enters muscle cells and drives protein synthesis.')
    story.append(Paragraph('Insulin-Like Growth Factor 1 (IGF-1) is produced primarily in the liver in response to GH stimulation. It mediates most of the anabolic effects of GH — muscle protein synthesis, satellite cell proliferation, and fat oxidation. Exogenous IGF-1 can be used to amplify these effects beyond what GH stimulation alone achieves.', s['Body']))
    tb(story, ['Form', 'Half-Life', 'Dose', 'Timing', 'Key Action'],
       [['IGF-1 LR3', '20–30 hrs', '20–50mcg/day', 'Post-training, subQ', 'Systemic muscle protein synthesis'],
        ['IGF-1 DES', '20–30 min', '50–150mcg local', 'Intra-workout, local IM', 'Site-specific muscle growth'],
        ['PEG MGF', '24–36 hrs', '200mcg 2× per week', 'Post-training, subQ', 'Satellite cell activation']],
       widths=[80, 80, 90, 120, 155])
    co(story, s, 'IGF-1 LR3 cycle length should be limited to 4–6 weeks maximum. It does not suppress HPTA but may desensitise IGF-1 receptors with prolonged use.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — HEALING PEPTIDES: BPC-157 & TB-500', s['ChHead']))
    hr(story)
    story.append(Paragraph('BPC-157 Protocol', s['SecHead']))
    tb(story, ['Indication', 'Dose', 'Route', 'Duration', 'Expected Result'],
       [['Tendon/ligament injury', '250–500mcg', 'SubQ near injury', '4–8 weeks', 'Accelerated tendon repair'],
        ['Gut/GI issues', '250mcg twice daily', 'Oral solution', '4–6 weeks', 'Mucosal healing, IBS improvement'],
        ['Joint pain', '250–500mcg', 'SubQ near joint', '4–6 weeks', 'Anti-inflammatory, cartilage support'],
        ['Muscle tear', '500mcg', 'SubQ near site', '6–8 weeks', 'Enhanced satellite cell activity']],
       widths=[110, 80, 110, 80, 145])
    story.append(Paragraph('TB-500 Protocol', s['SecHead']))
    tb(story, ['Phase', 'Dose', 'Frequency', 'Duration', 'Notes'],
       [['Loading', '2–4mg', '2× per week', '4–6 weeks', 'SubQ injection anywhere on body'],
        ['Maintenance', '2mg', 'Once per week', 'Ongoing as needed', 'Full body systemic effect']],
       widths=[80, 80, 100, 80, 185])
    co(story, s, 'BPC-157 + TB-500 combined is considered the most powerful healing peptide stack. Many bodybuilders use this combination during injury rehabilitation to return to training faster.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — STACKING GUIDE & SAFETY', s['ChHead']))
    hr(story)
    tb(story, ['Goal', 'Primary Peptides', 'Supporting Peptides', 'Duration'],
       [['Lean muscle mass', 'Ipamorelin + CJC-1295', 'IGF-1 LR3 (4 wks)', '12–16 weeks'],
        ['Fat loss', 'GHRP-2 + CJC-1295', 'T3 (optional)', '12 weeks'],
        ['Injury recovery', 'BPC-157 + TB-500', 'None required', '6–8 weeks'],
        ['General anti-ageing', 'Ipamorelin + CJC-1295', 'MK-677 nightly', 'Year-round (cycled)'],
        ['Sleep optimisation', 'Ipamorelin pre-sleep', 'MK-677 nightly', '8–12 weeks']],
       widths=[100, 130, 130, 65])
    bl(story, s, [
        'Do not run peptide cycles longer than 12–16 weeks without a 4–8 week break',
        'IGF-1 use requires blood glucose monitoring — it can cause hypoglycaemia',
        'Monitor for water retention (GH effect) — usually resolves after Week 2',
        'Rotate injection sites to prevent lipohypertrophy (small fat deposits)',
        'Peptide-related side effects are generally mild and dose-dependent — reduce dose first',
    ])

mk(os.path.join(OUT, '06_Complete_Peptide_Protocol_Bible.pdf'), 6,
   'Complete Peptide Protocol Bible', 'GHRP, GHRH, IGF-1, BPC-157 & TB-500 Complete Reference',
   ['6 Chapters', 'Advanced Guide', 'Science-Backed', 'Harm Reduction'], pdf06)

# ─── PDF 07 — SARMs Complete Scientific Handbook ─────────────────────────────
def pdf07(story, s):
    toc(story, s, [
        ('What Are SARMs? Mechanism of Action', 3),
        ('SARMs Reference: Individual Compound Profiles', 4),
        ('Bulking vs Cutting SARMs Protocols', 5),
        ('SARMs vs Steroids: Risk-Benefit Analysis', 6),
        ('Suppression, PCT & Blood Work', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — WHAT ARE SARMs?', s['ChHead']))
    hr(story)
    qt(story, s, 'SARMs are tissue-selective androgens — the goal of decades of pharmaceutical research to separate the muscle-building effects of testosterone from its other effects.')
    story.append(Paragraph('Selective Androgen Receptor Modulators (SARMs) are a class of therapeutic compounds that bind to androgen receptors with tissue selectivity — activating them in muscle and bone while minimising activation in the prostate, scalp, and other androgen-sensitive tissues. This selectivity profile makes them theoretically safer than anabolic steroids for performance enhancement, though long-term human safety data remains limited.', s['Body']))
    tb(story, ['SARMs Category', 'Selectivity', 'Research Stage', 'Examples'],
       [['Steroidal SARMs', 'Moderate', 'Historical/abandoned', 'Early DHT derivatives'],
        ['Non-steroidal SARMs', 'High', 'Phase I–III trials', 'Ostarine, LGD-4033, RAD-140'],
        ['SARM-like (SPPARM)', 'Very high', 'Phase I–II', 'Enobosarm, MK-677'],
        ['Investigational SARMs', 'Experimental', 'Pre-clinical', 'YK-11, S-23, ACP-105']],
       widths=[120, 90, 110, 105])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — INDIVIDUAL COMPOUND PROFILES', s['ChHead']))
    hr(story)
    tb(story, ['SARM', 'Half-Life', 'Common Dose', 'Primary Effect', 'Suppression Level'],
       [['Ostarine (MK-2866)', '24 hrs', '15–25mg/day', 'Lean muscle, joint healing', 'Low–Moderate'],
        ['LGD-4033 (Ligandrol)', '24–36 hrs', '5–10mg/day', 'Significant lean mass', 'Moderate–High'],
        ['RAD-140 (Testolone)', '16–20 hrs', '10–20mg/day', 'Hardening, strength', 'Moderate–High'],
        ['Cardarine (GW-501516)', '16–24 hrs', '10–20mg/day', 'Endurance, fat oxidation', 'None (PPAR-δ)'],
        ['Andarine (S4)', '4 hrs', '25–50mg/day', 'Vascularity, hardening', 'Moderate'],
        ['YK-11', '6–10 hrs', '5–10mg/day', 'Myostatin inhibition, mass', 'High'],
        ['MK-677 (Ibutamoren)', '24 hrs', '12.5–25mg/day', 'GH secretagogue, sleep', 'None (not SARM)']],
       widths=[115, 65, 80, 130, 100])
    co(story, s, 'Note: Cardarine (GW-501516) is not technically a SARM — it is a PPAR-δ agonist. It was discontinued by GSK due to cancer findings in animal models at high doses. Use with extreme caution.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — BULKING vs CUTTING PROTOCOLS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Lean Bulking Stack', s['SecHead']))
    tb(story, ['Compound', 'Dose', 'Duration', 'Purpose'],
       [['LGD-4033', '5–10mg/day', '8–12 weeks', 'Primary mass builder'],
        ['MK-677', '12.5–25mg/day', '16+ weeks', 'GH secretagogue, sleep, recovery'],
        ['Cardarine (optional)', '10mg/day', '8–12 weeks', 'Endurance, prevents fat gain'],
        ['Ostarine (bridge)', '12.5mg/day during PCT', '4 weeks', 'Muscle preservation during PCT']],
       widths=[100, 80, 80, 165])
    story.append(Paragraph('Cutting Stack', s['SecHead']))
    tb(story, ['Compound', 'Dose', 'Duration', 'Purpose'],
       [['Ostarine', '20–25mg/day', '10–12 weeks', 'Muscle preservation in deficit'],
        ['Cardarine', '20mg/day', '10–12 weeks', 'AMPK activation, fat oxidation'],
        ['Andarine S4', '25mg/day', '8–10 weeks', 'Hardening, vascularity'],
        ['RAD-140 (optional)', '10mg/day (wk 5-10)', '6 weeks', 'Strength + conditioning']],
       widths=[100, 80, 80, 165])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — SARMs vs STEROIDS: RISK-BENEFIT', s['ChHead']))
    hr(story)
    tb(story, ['Criterion', 'SARMs', 'Anabolic Steroids'],
       [['Muscle gain (12 weeks)', '3–6kg lean mass', '6–15kg (compound dependent)'],
        ['Liver toxicity', 'Low–Moderate (oral)', 'Moderate–High (17-aa orals)'],
        ['Cardiovascular risk', 'Low–Moderate', 'Moderate–High'],
        ['HPTA suppression', 'Low–Moderate', 'Significant–Complete'],
        ['Estrogenic effects', 'None (most SARMs)', 'Present (aromatising compounds)'],
        ['Hair loss risk', 'Low (most SARMs)', 'High (DHT derivatives)'],
        ['Virilisation (women)', 'Minimal (low doses)', 'Significant'],
        ['Legal status', 'Research chemical', 'Schedule III (US), various']],
       widths=[130, 140, 155])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — SUPPRESSION, PCT & BLOOD WORK', s['ChHead']))
    hr(story)
    qt(story, s, 'Suppression is a spectrum, not a binary. Even mild SARMs cause measurable LH and FSH reduction — this matters.')
    story.append(Paragraph('SARMs suppress the Hypothalamic-Pituitary-Testicular Axis (HPTA) to varying degrees. Unlike steroids, complete suppression is rare, but partial suppression is nearly universal with even "mild" SARMs like Ostarine at doses above 15mg/day for 8+ weeks. PCT helps restore endogenous testosterone production faster.', s['Body']))
    tb(story, ['SARM Cycle', 'Suppression Level', 'PCT Required?', 'PCT Protocol'],
       [['Ostarine < 15mg, < 6 wks', 'Minimal', 'Optional (mini PCT)', 'Nolvadex 20mg/day × 4 wks'],
        ['Ostarine full dose, 10–12 wks', 'Low–Moderate', 'Yes', 'Nolvadex 40/40/20/20'],
        ['LGD-4033 standard', 'Moderate', 'Yes', 'Clomid 50/25 + Nolvadex 40/20'],
        ['RAD-140 standard', 'Moderate–High', 'Full PCT', 'Clomid 50/50/25/25 + Nolvadex 40/40/20/20'],
        ['YK-11 standard', 'High', 'Full PCT', 'Same as steroid cycle PCT']],
       widths=[130, 90, 90, 115])
    bl(story, s, [
        'Pre-cycle bloods: testosterone total + free, LH, FSH, SHBG, CBC, CMP, lipids',
        'Mid-cycle check (Week 6): testosterone, LH — confirms suppression degree',
        'Post-PCT bloods: 4 weeks after PCT completion — testosterone should be >80% of baseline',
        'If testosterone does not recover within 16 weeks post-cycle, see an endocrinologist',
    ])

mk(os.path.join(OUT, '07_SARMs_Complete_Scientific_Handbook.pdf'), 7,
   'SARMs Complete Scientific Handbook', 'Evidence-Based Guide to Selective Androgen Receptor Modulators',
   ['5 Chapters', 'Scientific Reference', 'Harm Reduction', 'Blood Work Protocols'], pdf07)

# ─── PDF 08 — TRT Hormone Optimisation Guide ─────────────────────────────────
def pdf08(story, s):
    toc(story, s, [
        ('Understanding Low Testosterone', 3),
        ('TRT Protocols: Methods & Dosing', 4),
        ('Monitoring & Optimising Your TRT', 5),
        ('Managing Side Effects', 6),
        ('TRT & Fitness: Training & Nutrition', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — UNDERSTANDING LOW TESTOSTERONE', s['ChHead']))
    hr(story)
    qt(story, s, 'Low testosterone is not an inevitable part of ageing — it is a treatable medical condition with profound quality-of-life implications when left unaddressed.')
    story.append(Paragraph('Testosterone Replacement Therapy (TRT) is a medically supervised protocol for men with clinically low testosterone levels (hypogonadism). Low T is defined as serum testosterone below 300 ng/dL (10.4 nmol/L) by most guidelines, accompanied by symptoms. In India, lifestyle factors, stress, poor sleep, metabolic dysfunction, and environmental exposures have led to a significant increase in younger men presenting with suboptimal testosterone levels.', s['Body']))
    tb(story, ['Symptom Category', 'Common Symptoms', 'Frequency'],
       [['Physical', 'Reduced muscle mass, increased body fat, fatigue, decreased strength', 'Very common'],
        ['Sexual', 'Low libido, erectile dysfunction, reduced morning erections', 'Common'],
        ['Psychological', 'Depression, irritability, poor concentration, lack of drive', 'Common'],
        ['Metabolic', 'Insulin resistance, elevated triglycerides, central adiposity', 'Moderate'],
        ['Sleep', 'Poor sleep quality, sleep apnoea correlation', 'Moderate']],
       widths=[110, 230, 85])
    story.append(Paragraph('Diagnostic Criteria', s['SecHead']))
    tb(story, ['Lab Test', 'Optimal Range (TRT Candidate)', 'Action if Below Range'],
       [['Total Testosterone', '600–1000 ng/dL optimal; < 300 = clinical low', 'TRT evaluation with endocrinologist'],
        ['Free Testosterone', '15–25 pg/mL optimal', 'SHBG investigation'],
        ['SHBG', '20–40 nmol/L', 'If high: reduces free T — may need TRT even with normal total T'],
        ['LH / FSH', 'If low: secondary hypogonadism', 'HCG may restore natural production'],
        ['Estradiol', '20–30 pg/mL', 'Aromatase inhibitor may be needed if elevated']],
       widths=[110, 175, 140])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — TRT PROTOCOLS', s['ChHead']))
    hr(story)
    tb(story, ['Method', 'Dose', 'Frequency', 'Pros', 'Cons'],
       [['Testosterone Cypionate (IM)', '100–200mg/wk', 'Weekly or biweekly', 'Stable levels, affordable', 'Injection required, fluctuation'],
        ['Testosterone Enanthate (IM)', '100–200mg/wk', 'Weekly or biweekly', 'Same as Cypionate', 'Slightly more E2 fluctuation'],
        ['Testosterone Propionate (IM)', '50mg', 'Every other day', 'Stable levels, less conversion', 'Frequent injections'],
        ['Testosterone Gel (topical)', '50–100mg/day', 'Daily', 'No injections', 'Transference risk, absorption varies'],
        ['Testosterone Pellets', '150–450mg', 'Every 3–6 months', 'Convenience, stable', 'Insertion procedure required']],
       widths=[120, 80, 90, 120, 115])
    co(story, s, 'Most TRT specialists recommend starting at 100mg/week and adjusting based on blood work at 8 weeks. Avoid starting high — it is easier to increase than to lower a dose that has caused side effects.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — MONITORING & OPTIMISING', s['ChHead']))
    hr(story)
    story.append(Paragraph('TRT Monitoring Schedule', s['SecHead']))
    tb(story, ['Timepoint', 'Tests Required', 'What to Assess'],
       [['Baseline (pre-TRT)', 'Full hormonal panel + CBC + CMP + PSA + lipids', 'Establish starting point for all markers'],
        ['Week 6–8', 'Total T, Free T, E2, hematocrit, PSA', 'Dose adequacy and estrogen management'],
        ['Week 16', 'Full panel repeat', 'Comprehensive optimisation review'],
        ['Every 6 months (stable)', 'Full panel + PSA + bone density (annual)', 'Long-term safety monitoring'],
        ['Annually', 'Full panel + PSA + cardiovascular risk', 'Comprehensive annual review']],
       widths=[120, 165, 140])
    story.append(Paragraph('Optimisation Targets on TRT', s['SecHead']))
    tb(story, ['Marker', 'Target Range on TRT', 'Adjustment'],
       [['Total Testosterone', '700–1000 ng/dL', 'Increase dose if < 600; reduce if > 1200'],
        ['Estradiol (E2)', '20–35 pg/mL', 'AI if consistently > 40 pg/mL'],
        ['Hematocrit', '< 52%', 'Donate blood or reduce dose if > 52%'],
        ['PSA', '< 4 ng/mL (age-adjusted)', 'If rise > 1.4 in 1 year, urology referral'],
        ['Blood Pressure', '< 130/80', 'Lifestyle, dose adjustment, or medication']],
       widths=[110, 155, 160])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — MANAGING SIDE EFFECTS', s['ChHead']))
    hr(story)
    tb(story, ['Side Effect', 'Cause', 'Management', 'When to Act Urgently'],
       [['Acne', 'Elevated androgens', 'Salicylic acid, adapalene, doxycycline', 'Cystic/scarring acne'],
        ['Hair thinning', 'DHT conversion', 'Nizoral shampoo, finasteride (Rx)', 'If distressing to patient'],
        ['Elevated hematocrit', 'RBC stimulation', 'Donate blood, hydrate, reduce dose', 'If > 54%'],
        ['Gynecomastia', 'Elevated E2', 'Anastrozole 0.25–0.5mg twice weekly', 'Hard gland tissue developing'],
        ['Testicular atrophy', 'LH/FSH suppression', 'HCG 250IU twice per week', 'If fertility desired'],
        ['Mood changes', 'Hormonal fluctuation', 'Split injections to stabilise levels', 'Severe depression or aggression']],
       widths=[90, 90, 140, 105])
    co(story, s, 'HCG co-administration preserves testicular function and natural testosterone production during TRT. Recommended dose: 250–500 IU subcutaneously twice per week.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — TRT & FITNESS', s['ChHead']))
    hr(story)
    qt(story, s, 'TRT brings testosterone to a healthy physiological range — it is not performance enhancement, it is physiological restoration. The fitness benefits are significant nonetheless.')
    tb(story, ['Fitness Parameter', 'Expected Change on TRT', 'Timeline', 'Optimisation Strategy'],
       [['Lean muscle mass', '+2–5kg over 12 months', '3–6 months onset', 'Resistance training 4 days/week'],
        ['Body fat', '-2–4% total body fat', '3–6 months', 'Combined deficit + resistance training'],
        ['Strength', '+10–20% on compound lifts', '2–4 months', 'Progressive overload protocol'],
        ['Energy / libido', 'Significant improvement', '4–6 weeks', 'Sleep, stress management'],
        ['Bone density', 'Gradual improvement', '12–24 months', 'Weight-bearing exercise']],
       widths=[110, 115, 90, 110])
    bl(story, s, [
        'Training on TRT: treat as enhanced recovery — 4–5 resistance sessions per week is optimal',
        'Protein target: 2.0–2.5g per kg bodyweight (enhanced utilisation on TRT)',
        'Cardiovascular exercise critical: TRT increases RBC and can elevate BP — 3× cardio/week mandatory',
        'Sleep quality directly impacts TRT efficacy — target 7–8 hours; address sleep apnoea',
    ])

mk(os.path.join(OUT, '08_TRT_Hormone_Optimization_Guide.pdf'), 8,
   'TRT Hormone Optimisation Guide', 'Complete Protocol for Testosterone Replacement Therapy',
   ['5 Chapters', 'Medical Reference', 'Monitoring Protocols', 'Safety First'], pdf08)

# ─── PDF 09 — Science of Muscle Hypertrophy ──────────────────────────────────
def pdf09(story, s):
    toc(story, s, [
        ('Mechanisms of Muscle Hypertrophy', 3),
        ('Training Variables & Hypertrophy Stimulus', 4),
        ('Protein Synthesis & Nutrition Science', 5),
        ('Recovery Science & Muscle Growth', 6),
        ('Advanced Hypertrophy Techniques', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — MECHANISMS OF MUSCLE HYPERTROPHY', s['ChHead']))
    hr(story)
    qt(story, s, 'Muscle does not grow during training — it grows in response to training, during recovery. Confuse these two things and you will overtrain endlessly.')
    story.append(Paragraph('Skeletal muscle hypertrophy — an increase in muscle fibre cross-sectional area — is mediated by three primary mechanisms that operate synergistically. Understanding these mechanisms allows for precise programming that targets each one optimally. Hypertrophy occurs when protein synthesis exceeds protein breakdown over a sustained period — a state that requires adequate training stimulus, nutritional substrate, and recovery time.', s['Body']))
    tb(story, ['Mechanism', 'Definition', 'Primary Stimulus', 'Optimal Rep Range'],
       [['Mechanical tension', 'Force applied to sarcomeres activates mTOR via mechanosensors', 'Heavy compound lifting, full ROM', '3–8 reps (high load)'],
        ['Metabolic stress', 'Lactate, hydrogen ions, cell swelling signal growth', 'High-rep training with short rest', '10–20+ reps'],
        ['Muscle damage', 'Disrupted Z-bands trigger satellite cell activation', 'Eccentric emphasis, novel stimuli', '6–12 reps, slow eccentric']],
       widths=[105, 160, 120, 80])
    story.append(Paragraph('Fibre Type Recruitment', s['SecHead']))
    tb(story, ['Fibre Type', 'Characteristics', 'Hypertrophy Potential', 'Training Method'],
       [['Type I (Slow Twitch)', 'High endurance, fatigue-resistant, smaller', 'Low–Moderate', 'High rep, short rest, sustained tension'],
        ['Type II A (Fast Oxidative)', 'Intermediate, large hypertrophy capacity', 'High', 'Moderate load, 8–15 reps'],
        ['Type II X (Fast Glycolytic)', 'Maximum force, fatigues quickly', 'Very High', 'Heavy load, low reps, maximum effort']],
       widths=[120, 155, 100, 150])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — TRAINING VARIABLES', s['ChHead']))
    hr(story)
    tb(story, ['Variable', 'Hypertrophy Range', 'Key Research Finding', 'Practical Application'],
       [['Volume', '10–20 sets/muscle/week', 'MEV 10, MAV 16–20 sets/week', 'Start at lower end, progress over months'],
        ['Intensity', '60–85% 1RM', 'Equalises at high effort regardless of load', 'Train to within 2 reps of failure'],
        ['Frequency', '2–3× per muscle/week', 'More sessions with equal volume = superior', 'Full body or upper/lower over bro split'],
        ['Rest periods', '60–180 sec', 'Longer rest = higher strength, same hypertrophy', '90–120 sec for hypertrophy balance'],
        ['ROM (Range of Motion)', 'Full ROM superior', 'Stretch-mediated hypertrophy significant', 'Deep ROM on compounds always'],
        ['Tempo', '2–4 sec eccentric', 'Slow eccentric increases tension time', '2/0/1 or 3/0/1 (lower/pause/raise)']],
       widths=[90, 85, 155, 145])
    co(story, s, 'The most important variable is progressive overload — systematically increasing the challenge over time. Without this, volume and frequency are irrelevant.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — PROTEIN SYNTHESIS & NUTRITION', s['ChHead']))
    hr(story)
    qt(story, s, 'You cannot out-train a protein deficit. Muscle protein synthesis without adequate leucine availability is like a construction project without cement.')
    tb(story, ['Nutrient', 'Hypertrophy Role', 'Optimal Dose', 'Timing Importance'],
       [['Total Protein', 'Substrate for MPS', '1.6–2.2g/kg BW/day', 'Moderate — daily total matters most'],
        ['Leucine', 'mTORC1 activator', '3–4g per meal', 'High — must hit leucine threshold per meal'],
        ['Carbohydrates', 'mTOR signalling, glycogen', '3–5g/kg BW/day', 'Peri-workout timing matters'],
        ['Total Calories', 'Anabolic environment', 'Maintenance to +300 surplus', 'Consistent surplus > nutrient timing'],
        ['Creatine', 'PCr replenishment, cell volume', '5g/day (no loading needed)', 'Daily — consistent saturation key']],
       widths=[95, 120, 100, 110])
    bl(story, s, [
        'Leucine threshold per meal: ~3g — equivalent to 30g high-quality protein',
        'Protein distribution: 4–5 meals of 30–40g protein > 2 large meals (ceiling effect)',
        'Peri-workout protein: 0.4g/kg pre-workout + 0.4g/kg post-workout maximises the anabolic window',
        'Carbohydrate timing: pre/intra-workout carbs maintain training performance and insulin response',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — RECOVERY SCIENCE', s['ChHead']))
    hr(story)
    tb(story, ['Recovery Factor', 'Mechanism', 'Optimal Target', 'Consequence of Deficiency'],
       [['Sleep', 'GH pulse (SWS phase), protein synthesis', '7–9 hours/night', 'Reduced MPS by 40%, elevated cortisol'],
        ['Sleep quality', 'SWS depth determines GH amplitude', 'No alcohol, dark/cool room', 'Blunted GH even with 8 hours'],
        ['Caloric status', 'Substrate availability', 'Maintenance to surplus', 'Muscle catabolism in deficit'],
        ['Protein synthesis window', 'Lasts 24–48h post-training', 'Train each muscle 2× per week', 'Suboptimal weekly MPS volume'],
        ['Stress (cortisol)', 'Anti-anabolic, pro-catabolic', 'Manage life stress', 'Cortisol directly inhibits mTOR']],
       widths=[100, 135, 110, 130])
    co(story, s, 'Sleep is the most underrated hypertrophy tool. One week of 5-hour sleep reduces muscle protein synthesis by ~40% regardless of training or nutrition quality.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — ADVANCED HYPERTROPHY TECHNIQUES', s['ChHead']))
    hr(story)
    tb(story, ['Technique', 'Mechanism', 'Best Application', 'Frequency'],
       [['Drop Sets', 'Extend time in fatigue zone', 'Last set of isolation exercises', '1–2× per session max'],
        ['Cluster Sets', 'Maintain high load with micro-rests', 'Compound lifts for strength/size', 'Main movements 2× per week'],
        ['Mechanical Drop Sets', 'Multiple angles within one set', 'Incline → flat → decline press', 'Once per muscle group per week'],
        ['Myo-Reps', 'Repeated sets near failure', 'Isolation exercises, high rep', 'Works well for arms, shoulders'],
        ['Stretch-Mediated Loading', 'Deep ROM, peak stretch under load', 'Romanian DL, incline curls, flyes', 'All sessions — make it standard'],
        ['Blood Flow Restriction', 'Metabolic stress with light weights', 'Injury rehab, high volume', '2–3× per week at 20–30% 1RM']],
       widths=[110, 125, 125, 65])
    qt(story, s, 'Advanced techniques are the finishing touches on a well-built house. Build the house first: progressive overload, adequate volume, protein, sleep. Then add the decorations.')

mk(os.path.join(OUT, '09_Science_of_Muscle_Hypertrophy.pdf'), 9,
   'Science of Muscle Hypertrophy', 'Evidence-Based Mechanisms, Training Variables & Nutrition Science',
   ['5 Chapters', 'Scientific Reference', 'Evidence-Based', 'Advanced Training'], pdf09)

# ─── PDF 10 — Ultimate Fat Loss Masterclass ──────────────────────────────────
def pdf10(story, s):
    toc(story, s, [
        ('Energy Balance: The True Science of Fat Loss', 3),
        ('Hormones, Metabolism & Adaptation', 4),
        ('Optimal Nutrition Strategy for Fat Loss', 5),
        ('Cardio Science: LISS, HIIT & Zone Training', 6),
        ('Resistance Training for Maximum Fat Loss', 7),
        ('12-Week Fat Loss Blueprint', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — ENERGY BALANCE SCIENCE', s['ChHead']))
    hr(story)
    qt(story, s, 'Fat loss is ultimately a physics problem — but physiology makes it a non-linear, adaptive, hormonal physics problem. Treat it accordingly.')
    story.append(Paragraph('The first law of thermodynamics applies: fat loss requires a sustained caloric deficit. However, the human body is not a static furnace — it is an adaptive system that responds to caloric restriction by reducing total daily energy expenditure (TDEE) through multiple pathways. Understanding these adaptations is what separates effective long-term fat loss strategies from failed crash diets.', s['Body']))
    tb(story, ['TDEE Component', 'Contribution', 'Adaptability', 'Implication'],
       [['Basal Metabolic Rate (BMR)', '60–70%', 'Decreases with muscle loss + adaptation', 'Preserve muscle — it drives BMR'],
        ['Thermic Effect of Food (TEF)', '8–15%', 'Decreases with caloric deficit', 'High protein diet maximises TEF'],
        ['Non-Exercise Activity (NEAT)', '15–30%', 'High — unconsciously reduces in deficit', 'Stay active outside gym; walk more'],
        ['Exercise EE', '5–15%', 'Stable if intensity maintained', 'Maintain training intensity in cut']],
       widths=[140, 80, 130, 175])
    co(story, s, 'The biggest threat to fat loss is NEAT reduction — your body unconsciously moves less when in deficit. Deliberate daily step targets (8,000–12,000 steps) counteract this adaptation.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — HORMONES, METABOLISM & ADAPTATION', s['ChHead']))
    hr(story)
    tb(story, ['Hormone', 'Fat Loss Role', 'Changes in Deficit', 'Management Strategy'],
       [['Leptin', 'Satiety, metabolic rate regulator', 'Drops within days of deficit', 'Diet breaks, refeeds'],
        ['Ghrelin', 'Hunger hormone', 'Increases in deficit', 'High fibre, protein, structured meal timing'],
        ['Insulin', 'Fat storage gate', 'Improves with deficit', 'Lower carb diet amplifies fat oxidation'],
        ['Cortisol', 'Stress hormone, fat storage (visceral)', 'Elevated in severe deficit', 'Moderate deficit; sleep priority'],
        ['T3 (thyroid)', 'Metabolic rate', 'Decreases with severe restriction', 'Avoid extreme deficits > 25% TDEE'],
        ['Testosterone', 'Anabolic, anti-fat', 'Decreases in large deficit', 'Moderate deficit, adequate fat intake']],
       widths=[90, 130, 100, 150])
    story.append(Paragraph('The Diet Break Protocol', s['SecHead']))
    story.append(Paragraph('A diet break (7–14 days at maintenance calories) every 8–12 weeks restores leptin, normalises ghrelin, reduces cortisol, and resets metabolic rate. Research shows that dieters using diet breaks lose the same amount of fat over time as continuous restrictors, while preserving significantly more muscle and maintaining better hormonal health.', s['Body']))
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — OPTIMAL FAT LOSS NUTRITION', s['ChHead']))
    hr(story)
    story.append(Paragraph('The Non-Negotiable Fat Loss Rules', s['SecHead']))
    bl(story, s, [
        'Caloric deficit: 300–500 kcal/day below TDEE. Start conservative — deepen only when fat loss stalls',
        'Protein: 2.0–2.7g/kg bodyweight — highest priority macronutrient for muscle preservation',
        'Fat minimum: 0.7–1.0g/kg bodyweight — critical for hormonal health, especially testosterone',
        'Carbohydrates: the flexible variable — fill remaining calories after protein and fat targets met',
        'Fibre: 30–40g/day minimum — satiety, gut microbiome, appetite regulation',
        'Water: 3–4L/day — research shows optimal hydration improves fat oxidation by 30%',
    ])
    tb(story, ['Day Type', 'Calories', 'Protein', 'Carbs', 'Fat', 'Best For'],
       [['Training day', 'TDEE – 200', '2.2g/kg', '3g/kg', '0.8g/kg', 'Fuel + recovery'],
        ['Rest day', 'TDEE – 500', '2.5g/kg', '1.5g/kg', '1.0g/kg', 'Deeper deficit'],
        ['High carb (weekly)', 'TDEE + 100', '2.0g/kg', '4g/kg', '0.6g/kg', 'Leptin reset, performance']],
       widths=[80, 75, 65, 65, 65, 125])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — CARDIO SCIENCE', s['ChHead']))
    hr(story)
    tb(story, ['Method', 'Intensity', 'Duration', 'Fat Oxidation', 'Best Application'],
       [['LISS (Low Intensity Steady State)', 'Zone 2 (60–70% HRmax)', '40–60 min', 'High during session', 'Daily calorie burn, recovery'],
        ['HIIT (High Intensity Interval)', '>85% HRmax intervals', '15–25 min', 'High (24h EPOC)', '2–3× per week, metabolic'],
        ['Zone 3 (Moderate)', '70–80% HRmax', '30–45 min', 'Moderate', 'Aerobic capacity building'],
        ['Incline Walking', '5–7% grade, 5–6 km/h', '45–60 min', 'High, joint-friendly', 'Daily non-disruptive cardio']],
       widths=[145, 110, 70, 80, 120])
    co(story, s, 'HIIT burns more total calories in less time and produces EPOC (excess post-exercise oxygen consumption) lasting up to 24 hours. However, it stresses the CNS — limit to 2–3 sessions/week maximum alongside resistance training.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — RESISTANCE TRAINING FOR FAT LOSS', s['ChHead']))
    hr(story)
    qt(story, s, 'Cardio creates the deficit. Resistance training determines what fills the resulting space — muscle or fat. Without resistance training, fat loss is partly muscle loss.')
    bl(story, s, [
        'Maintain all heavy compound lifts through a cut — reduce volume before reducing intensity',
        'Train with the same weight as your bulk when possible — this signals "need this muscle"',
        'Superset non-competing muscle groups to increase calorie burn without extending training time',
        'Track strength closely — a 10–15% strength reduction is acceptable; more indicates muscle loss',
        'Abs and core training: every session; low body fat reveals abs — they are built through compound training',
    ])
    story.append(Paragraph('Fat Loss Training Split', s['SecHead']))
    tb(story, ['Day', 'Session', 'Duration', 'Cardio After?'],
       [['Mon', 'Heavy Lower Body (Squat, RDL, Leg Press)', '50 min', '20 min LISS'],
        ['Tue', 'Heavy Upper Push (Bench, OHP, Dips)', '50 min', 'No — recovery'],
        ['Wed', 'HIIT + Core', '35 min', 'HIIT is cardio'],
        ['Thu', 'Heavy Upper Pull (Row, Pullup, Face Pull)', '50 min', '20 min LISS'],
        ['Fri', 'Metabolic Circuit (full body, light)', '45 min', 'Optional LISS'],
        ['Sat/Sun', 'Walk 8,000+ steps, mobility, rest', '60 min walk', 'Walking IS cardio']],
       widths=[50, 175, 70, 90])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — 12-WEEK FAT LOSS BLUEPRINT', s['ChHead']))
    hr(story)
    tb(story, ['Phase', 'Weeks', 'Deficit', 'Cardio', 'Focus'],
       [['Phase 1: Foundation', '1–4', '300–350 kcal', '3× LISS 30 min', 'Habit formation, baseline'],
        ['Phase 2: Acceleration', '5–8', '400–450 kcal', '4× LISS + 1× HIIT', 'Increase intensity, deepen cut'],
        ['Phase 3: Peak', '9–11', '450–500 kcal', '4× LISS + 2× HIIT', 'Maximum fat mobilisation'],
        ['Phase 4: Recomp', '12', 'Maintenance', '2× LISS', 'Diet break, hormonal reset']],
       widths=[120, 55, 80, 130, 140])
    co(story, s, 'Expected total fat loss over 12 weeks following this blueprint: 4–6kg of pure body fat. Scale may show more due to water loss — body fat % and measurements tell the true story.')

mk(os.path.join(OUT, '10_Ultimate_Fat_Loss_Masterclass.pdf'), 10,
   'Ultimate Fat Loss Masterclass', 'Complete Science-Based Fat Loss System',
   ['6 Chapters', 'Science-Based', 'All Levels', 'Hormone-Aware'], pdf10)

print('\n[PDFs 06-10 complete]')
