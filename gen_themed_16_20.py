"""Generate catalog PDFs 16-20 with dark navy theme."""
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
    story.append(Paragraph('For educational and harm-reduction purposes only. Not medical advice. Consult a qualified healthcare professional before starting any protocol. Individual results vary.', s['Body']))
    story.append(PageBreak())

def mk(path, num, title, subtitle, tags, fn):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    s = st(); story = []
    cover(story, s, num, title, subtitle, tags)
    fn(story, s)
    doc.build(story, onFirstPage=dark_bg, onLaterPages=dark_bg)
    print(f'  ✓ {os.path.basename(path)}')

# ─── PDF 16 — Beginner Anabolic Cycle Complete Guide ─────────────────────────
def pdf16(story, s):
    toc(story, s, [
        ('Readiness Assessment & Safety Baseline', 3),
        ('Testosterone-Only 12-Week Protocol', 4),
        ('On-Cycle Essentials: Bloodwork & Support', 5),
        ('Training Programme for Your First Cycle', 6),
        ('PCT: Reclaiming Your Natural Testosterone', 7),
        ('Life After Your First Cycle', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — READINESS ASSESSMENT', s['ChHead']))
    hr(story)
    qt(story, s, 'The beginner who enters their first cycle with complete information and a clear protocol is safer than the advanced user who has become complacent.')
    story.append(Paragraph('A beginner anabolic cycle requires careful preparation. The foundation of safe cycle use is pre-cycle blood work, a clear compound selection strategy, an on-cycle support protocol, and a confirmed PCT plan before the cycle begins. Never start a cycle without PCT drugs already secured and ready.', s['Body']))
    tb(story, ['Pre-Cycle Checklist', 'Status Required', 'Why Critical'],
       [['Baseline blood work completed', 'Full panel done', 'Cannot identify suppression without baseline'],
        ['Training age', '2+ years structured training', 'Genetic ceiling should be near-reached first'],
        ['Age', '21+ (25+ recommended)', 'HPTA still maturing before 21'],
        ['PCT drugs secured', 'Clomid + Nolvadex in hand', 'Never start without PCT available'],
        ['Support supplements', 'Liv52, omega-3, BP monitor', 'Organ protection starts on Day 1'],
        ['Trusted contact aware', 'Someone knows your cycle', 'Emergency preparedness']],
       widths=[160, 120, 245])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — TESTOSTERONE-ONLY PROTOCOL', s['ChHead']))
    hr(story)
    story.append(Paragraph('The gold standard first cycle is Testosterone Enanthate 400–500mg per week for 12 weeks. This single-compound protocol maximises gains while making side-effect management straightforward — if anything goes wrong, there is only one compound to adjust.', s['Body']))
    tb(story, ['Week', 'Test E (Mon)', 'Test E (Thu)', 'Weekly Total', 'Key Action'],
       [['1–2', '200mg', '200mg', '400mg', 'Assess injection tolerance, no side effects expected'],
        ['3–4', '250mg', '250mg', '500mg', 'Full dose — monitor for estrogen symptoms'],
        ['5–10', '250mg', '250mg', '500mg', 'Consistent dose — bloodwork at Week 6'],
        ['11–12', '250mg', '250mg', '500mg', 'Final push — track progress photos'],
        ['13–14', 'None', 'None', '0mg', 'Clearance period before PCT'],
        ['15–18', 'PCT only', '—', '—', 'Clomid 50/50/25/25 + Nolvadex 40/40/20/20']],
       widths=[60, 85, 85, 85, 210])
    co(story, s, 'Use only Testosterone Enanthate or Cypionate for your first cycle. Propionate requires more frequent injections and is not ideal for beginners.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — ON-CYCLE ESSENTIALS', s['ChHead']))
    hr(story)
    tb(story, ['Support Item', 'Dose', 'Purpose', 'Start'],
       [['Liv52 DS / TUDCA', '2 tabs Liv52 or 500mg TUDCA', 'Liver protection', 'Day 1'],
        ['Omega-3 fish oil', '4g EPA/DHA combined', 'Lipid protection, cardiovascular', 'Day 1'],
        ['CoQ10', '200mg/day', 'Heart and mitochondrial support', 'Day 1'],
        ['Vitamin D3', '5000 IU/day', 'Hormonal co-factor', 'Day 1'],
        ['Zinc', '25mg/day', 'Testosterone support co-factor', 'Day 1'],
        ['Blood pressure monitor', 'Check weekly', 'Target < 130/80 mmHg', 'Before Day 1'],
        ['Arimidex (on hand)', '0.25mg 2× weekly if needed', 'Estrogen management IF symptoms appear', 'Only if needed']],
       widths=[125, 130, 150, 80])
    bl(story, s, [
        'Week 6 blood panel: testosterone total + free, estradiol, LH, FSH, CBC, CMP, lipids',
        'Estrogen symptoms: tender or itchy nipples, unusual water retention — introduce AI at low dose',
        'Blood pressure above 140/90: reduce sodium, increase cardio, consider reducing dose',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — TRAINING PROGRAMME', s['ChHead']))
    hr(story)
    story.append(Paragraph('On your first cycle, increase training volume by 20–30% above your natural training. Your recovery capacity and protein synthesis are elevated — but not unlimited. Progressive overload on all main compound lifts.', s['Body']))
    tb(story, ['Day', 'Muscles', 'Sets', 'Rep Range', 'Key Exercises'],
       [['Monday', 'Chest + Triceps', '16', '8–12', 'Bench, incline dB, dips, cable push'],
        ['Tuesday', 'Back + Biceps', '16', '8–12', 'Pull-ups, barbell row, cable row, curls'],
        ['Wednesday', 'Legs', '18', '8–15', 'Squat, leg press, RDL, leg curl'],
        ['Thursday', 'Shoulders + Traps', '14', '10–15', 'OHP, lateral raises, face pull, shrugs'],
        ['Friday', 'Arms + Core', '14', '10–15', 'Close grip bench, hammer curls, planks'],
        ['Saturday', 'Cardio + weak points', '10–12', '—', '20 min LISS + 2 weak point exercises'],
        ['Sunday', 'Rest + mobility', '—', '—', 'Foam roll, light stretching']],
       widths=[70, 110, 45, 75, 225])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — POST CYCLE THERAPY', s['ChHead']))
    hr(story)
    qt(story, s, 'PCT is not optional. It is the part of the cycle that determines whether this was a temporary loan or a permanent acquisition.')
    story.append(Paragraph('PCT begins 14–18 days after the last Testosterone Enanthate injection. This allows the long ester to clear the system. Starting PCT too early (with residual testosterone still suppressing the HPTA) wastes your PCT drugs.', s['Body']))
    tb(story, ['PCT Week', 'Clomiphene (Clomid)', 'Tamoxifen (Nolvadex)', 'Expected Status'],
       [['Week 1', '50mg/day', '40mg/day', 'Low energy, low libido — normal'],
        ['Week 2', '50mg/day', '40mg/day', 'Mood swings peak — stay consistent'],
        ['Week 3', '25mg/day', '20mg/day', 'Energy begins returning'],
        ['Week 4', '25mg/day', '20mg/day', 'Libido should be recovering']],
       widths=[80, 120, 120, 205])
    bl(story, s, [
        '4 weeks after PCT completion: blood work. Target testosterone > 80% of pre-cycle baseline',
        'If testosterone below 300 ng/dL at 8 weeks post-PCT: endocrinologist consultation',
        'Continue training hard and eating protein through PCT — hormones + training = muscle retention',
    ])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — LIFE AFTER YOUR FIRST CYCLE', s['ChHead']))
    hr(story)
    story.append(Paragraph('Consolidating Your Gains', s['SecHead']))
    bl(story, s, [
        'Expect to retain 70–80% of cycle gains after full recovery if PCT and training are maintained',
        'Minimum 12 weeks between cycles (ideally cycle length = time off)',
        'Use the off-cycle period to maximise natural gains, solidify new techniques, run blood work',
        'Avoid second cycle until testosterone is confirmed recovered to at least 80% of pre-cycle baseline',
        'Each subsequent cycle should have a clear, specific goal — not just "to do another one"',
    ])
    tb(story, ['Second Cycle Timing', 'What to Assess', 'Green Light Criteria'],
       [['Minimum: 12 weeks off', 'Testosterone recovery', '> 80% of pre-cycle baseline'],
        ['After blood work', 'Lipid profile', 'LDL < 130, HDL > 40'],
        ['After goal review', 'Physique and strength', 'Significant further progress potential'],
        ['After education', 'Next compound knowledge', 'Full understanding of any new compound']],
       widths=[130, 120, 275])

mk(os.path.join(OUT, '16_Beginner_Anabolic_Cycle_Complete_Guide.pdf'), 16,
   'Beginner Anabolic Cycle Complete Guide', 'Your First Cycle: Protocol, Safety, PCT & Long-Term Strategy',
   ['12 Weeks', '6 Chapters', 'Beginner Level', 'Full Safety Protocol'], pdf16)

# ─── PDF 17 — Intermediate Anabolic Cycle Blueprint ──────────────────────────
def pdf17(story, s):
    toc(story, s, [
        ('Intermediate Cycle Principles', 3),
        ('Stack Options: Adding a Second Compound', 4),
        ('16-Week Lean Bulk Protocol', 5),
        ('Estrogen & Prolactin Management', 6),
        ('Advanced Nutrition for Cycle', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — INTERMEDIATE CYCLE PRINCIPLES', s['ChHead']))
    hr(story)
    qt(story, s, 'The intermediate cycle is the most important step in your development. Go too conservative and miss the potential. Go too aggressive and invite avoidable problems.')
    story.append(Paragraph('An intermediate cycle is appropriate for users who have: (1) completed at least one testosterone-only cycle with good recovery, (2) confirmed natural testosterone recovery via blood work, and (3) maximised gains from testosterone alone. The intermediate step typically involves adding a second compound to the testosterone base.', s['Body']))
    tb(story, ['Criterion', 'Requirement for Intermediate Cycle'],
       [['Previous cycles', 'Minimum 1 completed with full PCT recovery'],
        ['Testosterone recovery', 'Confirmed via blood work — at least 80% of baseline'],
        ['Training experience', '3+ years; first cycle gains consolidated'],
        ['Blood work knowledge', 'Understand all markers in your panel'],
        ['Side effect management', 'Know what AI dose works for you from cycle 1'],
        ['New compound research', 'Full understanding of pharmacology, half-life, risks of new compound']],
       widths=[130, 395])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — ADDING A SECOND COMPOUND', s['ChHead']))
    hr(story)
    story.append(Paragraph('Best Second Compound Options', s['SecHead']))
    tb(story, ['Compound', 'Synergy with Test', 'Primary Benefit', 'Main Risk', 'Beginner-Intermediate Suitability'],
       [['Nandrolone (Deca)', 'Excellent — low E2', 'Joint support, mass, recovery', 'Prolactin elevation, sexual side effects', '★★★★ (best first add)'],
        ['Anavar (Oxandrolone)', 'Excellent — oral', 'Lean gains, strength, low risk', 'Liver strain (oral), expensive', '★★★★ (safest oral)'],
        ['Masteron', 'Excellent — anti-E', 'Hardening, anti-oestrogenic', 'Only works < 12% body fat', '★★★ (cutting only)'],
        ['Boldenone (EQ)', 'Good — mild', 'Appetite, endurance, lean mass', 'Slow acting, high RBC, long ester', '★★★ (patience required)'],
        ['Dianabol', 'Good — kick-start', 'Fast mass and strength gains', 'Liver, water retention, BP', '★★★ (short-term oral)']],
       widths=[100, 90, 110, 120, 105])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — 16-WEEK LEAN BULK PROTOCOL', s['ChHead']))
    hr(story)
    story.append(Paragraph('Recommended Intermediate Stack: Testosterone Enanthate + NPP (Nandrolone Phenylpropionate)', s['SecHead']))
    tb(story, ['Week', 'Test E', 'NPP', 'AI', 'Cabergoline', 'Notes'],
       [['1–4', '500mg/wk', '300mg/wk', 'Anastrozole 0.5mg E3D', 'None (monitor)', 'Assess NPP response'],
        ['5–12', '500mg/wk', '350mg/wk', 'Adjust to E2 bloods', '0.25mg 2×/wk if prolactin rises', 'Peak phase'],
        ['13–16', '500mg/wk', '200mg/wk', 'Continue AI', 'Continue Caber', 'Taper NPP early (long recovery)'],
        ['17–18', 'None', 'None', 'Stop AI', 'Stop Caber', 'Clearance (NPP = 1 week)'],
        ['19–22 (PCT)', 'None', 'None', 'None', 'None', 'Clomid + Nolvadex full 4 weeks']],
       widths=[60, 80, 80, 120, 100, 185])
    co(story, s, 'NPP (short ester Nandrolone) is preferred over Deca for intermediate users — it clears faster, making side effect management and PCT timing more controllable.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — ESTROGEN & PROLACTIN MANAGEMENT', s['ChHead']))
    hr(story)
    story.append(Paragraph('Nandrolone elevates prolactin via 19-nor compound mechanism. This requires a different management approach compared to testosterone-only cycles. Prolactin elevation causes sexual dysfunction (the infamous "Deca dick"), potential gynecomastia, and mood changes.', s['Body']))
    tb(story, ['Compound', 'Estrogenic', 'Progestenic', 'Prolactin', 'Management'],
       [['Testosterone', 'Yes (aromatises)', 'No', 'No', 'AI if needed'],
        ['Nandrolone (NPP/Deca)', 'Low', 'Yes', 'Yes (significant)', 'Cabergoline + AI'],
        ['Dianabol', 'High', 'No', 'Mild', 'AI essential'],
        ['Masteron', 'None', 'No', 'No', 'None required'],
        ['Anavar', 'None', 'No', 'No', 'None required']],
       widths=[100, 90, 90, 100, 145])
    co(story, s, 'Cabergoline protocol for Nandrolone use: 0.25mg twice weekly. Do not use bromocriptine as an alternative — it has significantly worse side effects.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — ADVANCED NUTRITION FOR CYCLE', s['ChHead']))
    hr(story)
    qt(story, s, 'An intermediate cycle deserves intermediate-level nutrition diligence. Tracking macros accurately is non-negotiable at this level.')
    tb(story, ['Phase', 'Duration', 'Caloric Strategy', 'Protein Target', 'Carb Strategy'],
       [['Weeks 1–4 (Setup)', '4 weeks', '+200 kcal surplus', '2.0g/kg BW', 'Moderate — 3–4g/kg'],
        ['Weeks 5–12 (Growth)', '8 weeks', '+400 kcal surplus', '2.2g/kg BW', 'High — 4–5g/kg peri-workout'],
        ['Weeks 13–16 (Lean out)', '4 weeks', 'Maintenance to −100', '2.5g/kg BW', 'Reduce slightly, maintain timing'],
        ['PCT Phase', '4–6 weeks', 'Maintenance to +100', '2.3g/kg BW', 'Moderate — 3g/kg for hormone support']],
       widths=[110, 70, 120, 90, 135])
    bl(story, s, [
        'Caloric surplus for Nandrolone + Test stack: 400–500 kcal above TDEE optimal',
        'Higher protein required: Nandrolone significantly increases nitrogen retention — supply the substrate',
        'Carbohydrate timing: 50% of daily carbs around training window (pre + post)',
        'Alcohol: zero during cycle. Nandrolone is processed differently with alcohol present',
    ])

mk(os.path.join(OUT, '17_Intermediate_Anabolic_Cycle_Blueprint.pdf'), 17,
   'Intermediate Anabolic Cycle Blueprint', '16-Week Protocol with Second Compound Integration',
   ['16 Weeks', '5 Chapters', 'Intermediate Level', 'Stack Strategy'], pdf17)

# ─── PDF 18 — Advanced Anabolic Cycle Mastery ────────────────────────────────
def pdf18(story, s):
    toc(story, s, [
        ('Advanced Cycle Philosophy', 3),
        ('Multi-Compound Protocols', 4),
        ('Advanced Cutting Compounds', 5),
        ('Peptide + Steroid Integration', 6),
        ('Long-Term Health & TRT Transition', 7),
    ])
    story.append(Paragraph('CHAPTER 1 — ADVANCED CYCLE PHILOSOPHY', s['ChHead']))
    hr(story)
    qt(story, s, 'Advanced users do not use more — they use smarter. Fewer compounds, better recovery, longer-term health management.')
    story.append(Paragraph('An advanced anabolic user is not defined by the number of compounds used simultaneously but by the depth of knowledge, disciplined monitoring, and long-term strategic thinking applied to every cycle. At advanced levels, the goal shifts from "maximum gains" to "optimal gains with minimum long-term cost." Health preservation becomes the primary KPI.', s['Body']))
    tb(story, ['Advanced Cycle Characteristic', 'Description'],
       [['Bloods every cycle', 'Full panel pre-cycle, mid-cycle, 4 weeks post-PCT — non-negotiable'],
        ['Minimum compounds', 'Use the fewest compounds that achieve the goal — not the maximum tolerated'],
        ['TRT base awareness', 'Consider whether TRT transition is better than repeated cycles'],
        ['Cardiovascular monitoring', 'Echo + carotid IMT every 2–3 years at advanced use level'],
        ['Systematic record keeping', 'Every compound, dose, date, side effect — 5-year log minimum'],
        ['Exit strategy planned', 'Know when and how to transition off cycles permanently']],
       widths=[165, 360])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — MULTI-COMPOUND PROTOCOLS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Advanced Mass Stack (Experienced Users Only)', s['SecHead']))
    tb(story, ['Compound', 'Dose', 'Ester', 'Duration', 'Role in Stack'],
       [['Testosterone Enanthate', '600–800mg/wk', 'Long', '16 weeks', 'Primary anabolic base'],
        ['Boldenone (EQ)', '400–600mg/wk', 'Long', '16 weeks', 'Appetite, RBC, lean mass'],
        ['Anadrol (Oxymetholone)', '50mg/day', 'Oral', 'Weeks 1–4 only', 'Rapid strength kickstart'],
        ['Drostanolone (Masteron)', '400mg/wk', 'Propionate', 'Last 4 weeks', 'Finishing hardness, anti-E2']],
       widths=[130, 80, 80, 100, 135])
    story.append(Paragraph('Advanced Cutting Stack', s['SecHead']))
    tb(story, ['Compound', 'Dose', 'Duration', 'Key Effect'],
       [['Testosterone Propionate', '100–150mg EOD', '12 weeks', 'Base — minimal water retention'],
        ['Trenbolone Acetate', '75–100mg EOD', '12 weeks', 'King of fat loss compounds'],
        ['Masteron Propionate', '100mg EOD', '12 weeks', 'Hardening, natural AI'],
        ['Anavar', '50mg/day', 'Weeks 5–12', 'Strength preservation, dryness'],
        ['Winstrol', '25–50mg/day', 'Weeks 9–12', 'Final hardening effect']],
       widths=[130, 100, 80, 215])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — ADVANCED CUTTING COMPOUNDS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Trenbolone Deep Dive', s['SecHead']))
    qt(story, s, 'Trenbolone is uniquely powerful and uniquely demanding. It rewards discipline and punishes recklessness.')
    story.append(Paragraph('Trenbolone Acetate is a 19-nor compound with approximately 5× the anabolic and androgenic potency of testosterone. It does not aromatise into estrogen but elevates prolactin significantly. It causes direct fat oxidation, creates a pronounced hardening effect, and dramatically reduces appetite. Side effects are dose-dependent and include night sweats, insomnia, aggression, and cardiovascular strain.', s['Body']))
    tb(story, ['Trenbolone Side Effect', 'Mechanism', 'Frequency', 'Management'],
       [['Night sweats', 'Elevated metabolic rate, altered thermoregulation', 'Very common', 'Cool room, moisture-wicking sheets'],
        ['Insomnia', 'CNS stimulation, cortisol effects', 'Common', 'Melatonin 1mg, no stimulants after 12pm'],
        ['Aggression', 'Androgenic CNS effect', 'Common (dose-related)', 'Mindfulness, dose management, communication'],
        ['Tren cough', 'Oil microemboli (propionate)', 'Occasional', 'Slow injection, warm oil, aspirate'],
        ['Prolactin gyno', '19-nor progestenic activity', 'Moderate risk', 'Cabergoline 0.25–0.5mg 2× weekly']],
       widths=[115, 155, 85, 170])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — PEPTIDE + STEROID INTEGRATION', s['ChHead']))
    hr(story)
    story.append(Paragraph('Combining peptides with anabolic compounds creates a multi-axis hormonal enhancement that significantly exceeds the effect of either approach alone. The synergy is primarily at the GH-IGF-1 axis level.', s['Body']))
    tb(story, ['Protocol', 'Compounds', 'Peptides', 'Goal', 'Duration'],
       [['Advanced lean bulk', 'Test E 600mg + EQ 400mg', 'Ipamorelin + CJC + MK-677', 'Maximum lean mass', '16 weeks'],
        ['Advanced cut', 'Test P + Tren A + Mast P', 'GHRP-2 + CJC-1295 + T3', 'Maximum fat loss, preservation', '12 weeks'],
        ['Recomp', 'Test E 300–400mg (TRT+)', 'IGF-1 LR3 + Ipamorelin + MK-677', 'Simultaneous fat loss + muscle', '16 weeks'],
        ['Anti-ageing / maintenance', 'TRT dose only', 'Ipamorelin + CJC year-round (cycled)', 'Long-term health + body comp', 'Year-round']],
       widths=[90, 145, 140, 120, 70])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — LONG-TERM HEALTH & TRT TRANSITION', s['ChHead']))
    hr(story)
    qt(story, s, 'The most successful long-term enhanced athletes are those who manage their health with the same diligence they manage their training. Your future self is a stakeholder in your current choices.')
    story.append(Paragraph('Long-Term Cardiovascular Monitoring', s['SecHead']))
    tb(story, ['Test', 'Frequency', 'Purpose', 'Action Threshold'],
       [['Echocardiogram', 'Every 2–3 years', 'Left ventricular hypertrophy detection', 'LVH Stage 1 = dose reduction'],
        ['Carotid IMT Ultrasound', 'Every 2–3 years', 'Atherosclerosis early detection', 'Any significant plaque = cycle reassessment'],
        ['Calcium Score CT', 'Every 3–5 years', 'Coronary artery calcification', 'Score > 100 = aggressive lipid management'],
        ['Lipid panel (advanced)', 'Every cycle', 'LDL particle size + ApoB', 'ApoB > 130 = intervention'],
        ['Kidney function (eGFR)', 'Every 6 months', 'Creatine + compound metabolites', 'eGFR < 60 = nephrology referral']],
       widths=[120, 90, 165, 150])
    co(story, s, 'TRT transition is a legitimate medical pathway for advanced users whose HPTA does not recover fully. A well-managed TRT protocol often presents fewer long-term risks than repeated supraphysiological cycles.')

mk(os.path.join(OUT, '18_Advanced_Anabolic_Cycle_Mastery.pdf'), 18,
   'Advanced Anabolic Cycle Mastery', 'Multi-Compound Protocols, Peptide Integration & Long-Term Health',
   ['5 Chapters', 'Advanced Level', 'Expert Knowledge', 'Health-First Approach'], pdf18)

# ─── PDF 19 — PCT Post Cycle Therapy Complete Bible ──────────────────────────
def pdf19(story, s):
    toc(story, s, [
        ('HPTA Suppression: The Physiology', 3),
        ('SERM Protocols: Clomid & Nolvadex', 4),
        ('HCG: Bridge & Blast Uses', 5),
        ('PCT for Specific Compounds', 6),
        ('Recovery Optimisation & Monitoring', 7),
        ('When PCT Fails: Next Steps', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — HPTA SUPPRESSION PHYSIOLOGY', s['ChHead']))
    hr(story)
    qt(story, s, 'PCT does not restore your testosterone — it restores your body\'s ability to make testosterone. The distinction matters because it changes how you approach the protocol.')
    story.append(Paragraph('Anabolic steroid use suppresses the Hypothalamic-Pituitary-Testicular Axis (HPTA) through negative feedback. Exogenous androgens signal to the hypothalamus and pituitary that testosterone production is adequate, causing a reduction and eventual cessation of GnRH, LH, and FSH secretion. Without LH, the Leydig cells in the testes reduce and eventually cease testosterone production. PCT uses SERMs to block estrogen receptors in the hypothalamus/pituitary, tricking them into perceiving low estrogen and increasing GnRH → LH → FSH signalling.', s['Body']))
    tb(story, ['Compound Duration', 'Suppression Severity', 'Recovery Without PCT', 'Recovery With PCT'],
       [['< 4 weeks, mild', 'Mild', '2–4 weeks', '1–2 weeks'],
        ['6–10 weeks, moderate', 'Moderate', '3–6 months', '4–6 weeks'],
        ['12–16 weeks, standard', 'Significant', '4–8 months', '4–6 weeks'],
        ['20+ weeks, suppressive', 'Severe', '6–12 months+', '6–10 weeks'],
        ['Blast and cruise (no PCT)', 'Complete', 'Possible permanent deficiency', 'TRT evaluation recommended']],
       widths=[120, 100, 140, 140])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — SERM PROTOCOLS', s['ChHead']))
    hr(story)
    tb(story, ['Protocol', 'Clomid Week 1', 'Clomid Week 2', 'Clomid Week 3', 'Clomid Week 4', 'Notes'],
       [['Mild PCT', 'None', 'None', 'None', 'None', 'Mini PCT: Nolvadex 20mg × 4 wks only'],
        ['Standard PCT', '50mg/day', '50mg/day', '25mg/day', '25mg/day', 'Nolvadex 40/40/20/20 alongside'],
        ['Aggressive PCT', '100mg/day', '50mg/day', '50mg/day', '25mg/day', '+ Nolvadex 40/40/20/20'],
        ['Extended PCT', '50mg/day', '50mg/day', '25mg/day', '25mg/day', 'Continue Nolvadex weeks 5–6: 20mg']],
       widths=[100, 75, 75, 75, 75, 175])
    story.append(Paragraph('Clomid vs Nolvadex: Why Use Both?', s['SecHead']))
    tb(story, ['SERM', 'Receptor Selectivity', 'Primary PCT Use', 'Main Side Effect'],
       [['Clomid (Clomiphene)', 'Hypothalamus/pituitary ERα antagonist', 'LH/FSH stimulation', 'Vision disturbances (1–2%), mood'],
        ['Nolvadex (Tamoxifen)', 'Pituitary ERα antagonist + breast tissue', 'LH stimulation + breast tissue protection', 'Mood changes, joint stiffness (rare)'],
        ['Combined', 'Dual mechanism', 'Maximum axis stimulation', 'Monitor vision carefully on Clomid']],
       widths=[110, 145, 160, 110])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — HCG: BRIDGE & BLAST USES', s['ChHead']))
    hr(story)
    qt(story, s, 'HCG keeps the testes "awake" during a cycle so PCT has less work to do. Think of it as maintaining the engine while the ignition is temporarily bypassed.')
    story.append(Paragraph('Human Chorionic Gonadotropin (HCG) mimics LH at the Leydig cell receptor. Used during a cycle, it prevents testicular atrophy and maintains intratesticular testosterone production, making PCT faster and more complete. It does not, however, restore the HPTA axis itself — SERMs are still required post-HCG.', s['Body']))
    tb(story, ['HCG Protocol', 'Dose', 'Frequency', 'Duration', 'Purpose'],
       [['On-cycle maintenance', '250 IU', 'Twice weekly', 'Throughout cycle', 'Prevent atrophy, maintain fertility'],
        ['Pre-PCT blast', '500 IU', 'Every other day', '2–3 weeks pre-PCT', 'Resensitise Leydig cells'],
        ['Post-cycle bridge', '1000 IU', 'Every other day', '10–14 days', 'Restart production before SERMs'],
        ['TRT co-administration', '250–500 IU', 'Twice weekly', 'Ongoing with TRT', 'Preserve fertility and testicular volume']],
       widths=[120, 60, 95, 100, 150])
    co(story, s, 'Stop HCG at least 3 days before starting SERMs (Clomid/Nolvadex). Running both simultaneously causes HCG to compete with your natural LH signal.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — PCT FOR SPECIFIC COMPOUNDS', s['ChHead']))
    hr(story)
    tb(story, ['Compound(s) Used', 'Wait Before PCT', 'PCT Protocol', 'Duration'],
       [['Testosterone Enanthate only', '14–18 days', 'Nolvadex 40/40/20/20', '4 weeks'],
        ['Test E + Deca (NPP)', '10–14 days (NPP)', 'Clomid 50/50/25/25 + Nolvadex', '6 weeks'],
        ['Test E + Deca long-ester', '21+ days', 'Aggressive PCT 6–8 weeks', '6–8 weeks'],
        ['Test + Tren + Mast', '7–10 days (prop esters)', 'Clomid + Nolvadex + Caber (2 weeks)', '4–6 weeks'],
        ['Oral only (Var, Winstrol)', '7 days', 'Mini PCT: Nolvadex 20mg × 4 wks', '4 weeks'],
        ['SARMs', '3–5 days', 'Nolvadex 40/40/20/20 (all SARMs)', '4 weeks']],
       widths=[160, 90, 185, 90])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — RECOVERY OPTIMISATION', s['ChHead']))
    hr(story)
    tb(story, ['Support Supplement', 'Dose', 'Purpose', 'Duration'],
       [['Vitamin D3', '5000 IU/day', 'Leydig cell receptor support', 'Throughout PCT + 3 months after'],
        ['Zinc', '25–30mg/day', 'Testosterone synthesis co-factor', 'Throughout PCT + 3 months'],
        ['Ashwagandha KSM-66', '600mg/day', 'Cortisol reduction, T support', 'Throughout PCT + 3 months'],
        ['Omega-3', '4g/day', 'Anti-inflammatory, lipid recovery', 'Throughout PCT + ongoing'],
        ['Magnesium glycinate', '400mg before bed', 'Sleep quality, HPTA support', 'Throughout PCT'],
        ['Tribulus (for libido)', '1500mg/day', 'Mild LH stimulation, libido support', 'Weeks 3–4 of PCT only']],
       widths=[120, 80, 190, 135])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — WHEN PCT FAILS', s['ChHead']))
    hr(story)
    qt(story, s, 'A failed PCT is not a catastrophe — it is medical information. It tells you the HPTA needs professional support. Act on it.')
    story.append(Paragraph('PCT failure is defined as testosterone remaining below 300 ng/dL at 8 weeks post-PCT completion, or below 80% of pre-cycle baseline. This requires medical evaluation.', s['Body']))
    bl(story, s, [
        'Step 1: Repeat blood work at 8 and 12 weeks post-PCT — confirm it is persistent, not temporary',
        'Step 2: Consult an endocrinologist — bring your full blood work history',
        'Step 3: HCG stimulation test to determine if issue is testicular or hypothalamic/pituitary',
        'Step 4: Extended SERMs trial under medical supervision (6–12 weeks)',
        'Step 5: If testosterone remains low and symptoms present — TRT is a legitimate therapeutic option',
        'Do NOT immediately restart another cycle — suppression on already-suppressed HPTA is dangerous',
    ])
    co(story, s, 'Many men who "need TRT" after cycles actually have recoverable HPTA dysfunction that was not given enough time. 6–12 months is the full recovery window — not 6 weeks.')

mk(os.path.join(OUT, '19_PCT_Post_Cycle_Therapy_Complete_Bible.pdf'), 19,
   'PCT Post Cycle Therapy Complete Bible', 'Complete Guide to HPTA Recovery After Every Cycle',
   ['6 Chapters', 'Essential Reading', 'All Cycle Users', 'Medical Reference'], pdf19)

# ─── PDF 20 — Anabolic Cycle Nutrition & Supplementation Bible ───────────────
def pdf20(story, s):
    toc(story, s, [
        ('Nutrition Principles for Enhanced Athletes', 3),
        ('Bulking Nutrition: Maximising Anabolic Environment', 4),
        ('Cutting Nutrition on Cycle', 5),
        ('Organ Protection & Support Supplements', 6),
        ('Intra-Cycle Supplementation Strategy', 7),
        ('Post-Cycle Nutrition for Recovery', 8),
    ])
    story.append(Paragraph('CHAPTER 1 — NUTRITION FOR ENHANCED ATHLETES', s['ChHead']))
    hr(story)
    qt(story, s, 'Anabolic compounds are nutrient partitioning agents — they do not create muscle from nothing. They direct protein and calories toward muscle growth at a dramatically higher efficiency. Supply the raw materials.')
    story.append(Paragraph('Enhanced athletes have fundamentally different nutritional requirements from natural athletes. The increased protein synthesis rate, nitrogen retention, and anabolic signalling during a cycle creates a dramatically elevated demand for dietary substrate. Insufficient protein or calories while "on cycle" is the most common reason for below-average results — the compounds cannot build what the nutrition does not provide.', s['Body']))
    tb(story, ['Nutritional Variable', 'Natural Athlete Target', 'Enhanced Athlete Target', 'Reason for Difference'],
       [['Protein (g/kg BW/day)', '1.6–2.0g', '2.2–3.0g', 'Enhanced protein synthesis requires more substrate'],
        ['Total calories (surplus)', '+200–300 kcal', '+300–600 kcal', 'Greater anabolic capacity utilises larger surplus cleanly'],
        ['Carbohydrates (g/kg)', '3–5g', '4–7g (bulking)', 'Increased glucose uptake and glycogen synthesis rate'],
        ['Meal frequency', '3–4 meals', '5–6 meals', 'Sustained amino acid availability for enhanced MPS'],
        ['Protein per meal', '30–40g', '40–60g', 'Higher leucine threshold with elevated MPS']],
       widths=[135, 110, 130, 150])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 2 — BULKING NUTRITION ON CYCLE', s['ChHead']))
    hr(story)
    tb(story, ['Bodyweight', 'TDEE', 'Cycle Surplus', 'Target Kcal', 'Protein', 'Carbs', 'Fat'],
       [['70kg', '2800', '+400', '3200', '175g', '450g', '85g'],
        ['80kg', '3100', '+450', '3550', '200g', '510g', '95g'],
        ['90kg', '3400', '+500', '3900', '225g', '570g', '105g'],
        ['100kg', '3700', '+550', '4250', '250g', '630g', '115g']],
       widths=[70, 60, 80, 80, 70, 70, 60])
    story.append(Paragraph('6-Meal Bulking Day Template', s['SecHead']))
    tb(story, ['Meal #', 'Timing', 'Foods', 'Protein', 'Kcal'],
       [['1', '7:00 AM', '6 eggs + 3 roti + 1 cup full-fat milk + banana', '50g', '730'],
        ['2', '10:30 AM', '200g chicken + 1.5 cups rice + sabzi', '45g', '600'],
        ['3 (pre-workout)', '1:30 PM', '50g oats + 1.5 scoops whey + 1 tbsp PB', '45g', '490'],
        ['4 (post-workout)', '4:30 PM', '2 scoops whey + 60g dextrose + creatine', '55g', '470'],
        ['5', '7:30 PM', '250g paneer or fish + 2 roti + 1 cup daal + veg', '60g', '740'],
        ['6', '10:30 PM', '300ml full-fat milk + 30g casein + 30g almonds', '45g', '520']],
       widths=[55, 65, 230, 60, 55])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 3 — CUTTING NUTRITION ON CYCLE', s['ChHead']))
    hr(story)
    qt(story, s, 'The advantage of cutting on cycle is that muscle preservation is dramatically enhanced — you can run a larger deficit than a natural athlete without the same muscle loss penalty.')
    tb(story, ['Bodyweight', 'TDEE', 'On-Cycle Deficit', 'Target Kcal', 'Protein', 'Carbs', 'Fat'],
       [['80kg', '3100', '−600', '2500', '220g', '240g', '75g'],
        ['90kg', '3400', '−650', '2750', '248g', '270g', '82g'],
        ['100kg', '3700', '−700', '3000', '275g', '300g', '90g']],
       widths=[75, 60, 90, 90, 70, 70, 60])
    co(story, s, 'On-cycle cutting deficit can be 500–700 kcal vs the 300–400 kcal recommended for naturals. The anabolic environment prevents muscle catabolism at this deficit. Do not exceed 700 kcal — cortisol elevation is still a risk.')
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 4 — ORGAN PROTECTION & SUPPORT SUPPLEMENTS', s['ChHead']))
    hr(story)
    story.append(Paragraph('Non-Negotiable On-Cycle Supplements', s['SecHead']))
    tb(story, ['Supplement', 'Dose', 'Primary Protection', 'Take With'],
       [['TUDCA (Tauroursodeoxycholic Acid)', '500mg/day', 'Bile acid transport, hepatocyte protection', 'Any meal'],
        ['UDCA or Liv52 DS (alternative)', '2 tabs twice daily', 'Liver enzyme normalisation', 'Meals'],
        ['Omega-3 (EPA/DHA)', '4–6g/day combined', 'LDL reduction, anti-inflammatory, cardiovascular', 'Meals'],
        ['CoQ10', '200–400mg/day', 'Mitochondrial function, cardiac protection', 'Morning, with fat'],
        ['NAC (N-Acetyl Cysteine)', '600mg twice daily', 'Glutathione precursor, liver + kidney', 'Between meals'],
        ['Hawthorn Berry', '500mg twice daily', 'Blood pressure management, cardiac', 'Morning + evening'],
        ['Vitamin K2 (MK-7)', '200mcg/day', 'Arterial calcification prevention (with D3)', 'With fat']],
       widths=[155, 80, 185, 105])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 5 — INTRA-CYCLE SUPPLEMENTATION', s['ChHead']))
    hr(story)
    tb(story, ['Supplement', 'On-Cycle Role', 'Dose', 'Timing'],
       [['Creatine Monohydrate', 'Cell volume, strength, recovery', '5g/day', 'Any time consistently'],
        ['Whey Isolate', 'Rapid protein synthesis substrate', '1–2 scoops', 'Post-workout + between meals'],
        ['Casein Protein', 'Sustained overnight MPS', '30–40g', 'Pre-sleep'],
        ['BCAA (2:1:1)', 'Anti-catabolic, intra-workout', '10g', 'During training'],
        ['Vitamin C', 'Cortisol reduction, collagen', '1000mg twice daily', 'Morning + post-workout'],
        ['Magnesium Glycinate', 'Sleep quality, CNS, insulin sensitivity', '400mg', 'Before bed'],
        ['Zinc', 'Testosterone co-factor, immune', '25–30mg', 'Before bed (away from calcium)'],
        ['Probiotics', 'Gut health, nutrient absorption', '10B CFU daily', 'With breakfast']],
       widths=[130, 175, 80, 120])
    story.append(PageBreak())

    story.append(Paragraph('CHAPTER 6 — POST-CYCLE NUTRITION', s['ChHead']))
    hr(story)
    qt(story, s, 'Post-cycle nutrition is the final lever between keeping your gains and losing them. PCT drugs restart hormones; nutrition provides the substrate that holds muscle while testosterone is suboptimal.')
    story.append(Paragraph('The post-cycle period (including PCT) is a catabolic risk window. Testosterone is low, cortisol may be elevated, and anabolic signalling is suppressed. Aggressive nutrition counteracts the catabolic environment.', s['Body']))
    tb(story, ['PCT Phase', 'Caloric Strategy', 'Protein Target', 'Carb Approach', 'Fat Strategy'],
       [['Weeks 1–2 (SERM initiation)', 'Maintenance + 100', '2.5g/kg BW', 'Moderate — 3g/kg', '0.8g/kg'],
        ['Weeks 3–4 (Mid PCT)', 'Maintenance', '2.5g/kg BW', 'Timed peri-workout', '0.8g/kg'],
        ['Post-PCT consolidation', 'Small surplus (+150)', '2.2g/kg BW', 'Normal cycling', '0.8–1.0g/kg']],
       widths=[145, 95, 90, 110, 85])
    bl(story, s, [
        'Maintain training intensity and volume through PCT — do not reduce training out of fear of loss',
        'Prioritise sleep during PCT — it is the single most important recovery intervention available',
        'No alcohol during PCT — the HPTA is fragile; do not add pharmacological stress',
        'Continue all on-cycle liver/organ support through PCT and 4 weeks beyond',
        'Avoid large caloric deficits for at least 12 weeks after PCT completion',
    ])

mk(os.path.join(OUT, '20_Anabolic_Cycle_Nutrition_Supplementation_Bible.pdf'), 20,
   'Anabolic Cycle Nutrition & Supplementation Bible', 'Complete Nutritional Strategy for Before, During & After Every Cycle',
   ['6 Chapters', 'Essential Reference', 'Bulking & Cutting', 'Organ Protection'], pdf20)

print('\n[PDFs 16-20 complete]')
