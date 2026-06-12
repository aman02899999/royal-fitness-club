#!/usr/bin/env python3
"""Batch generator: expands catalog PDFs 01-15 to 20+ pages each."""
import io, os
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from PyPDF2 import PdfWriter, PdfReader

W, H = A4

# ── Shared styles ─────────────────────────────────────────────────────────────
def make_styles(accent):
    s = getSampleStyleSheet()
    def add(name, **kw):
        if name not in s: s.add(ParagraphStyle(name=name, **kw))
        else: [setattr(s[name], k, v) for k, v in kw.items()]
    DARK = colors.HexColor('#1a1a2e')
    add('PH1',  fontName='Helvetica-Bold', fontSize=20, textColor=accent, spaceAfter=8, spaceBefore=12, leading=24)
    add('PH2',  fontName='Helvetica-Bold', fontSize=14, textColor=DARK, spaceAfter=5, spaceBefore=9, leading=17)
    add('PH3',  fontName='Helvetica-Bold', fontSize=11, textColor=accent, spaceAfter=4, spaceBefore=7, leading=14)
    add('PBody',fontName='Helvetica', fontSize=10, spaceAfter=4, leading=14, textColor=colors.HexColor('#333333'))
    add('PBL',  fontName='Helvetica', fontSize=10, spaceAfter=3, leading=13, leftIndent=14, textColor=colors.HexColor('#333333'))
    add('PTH',  fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, leading=11)
    add('PTC',  fontName='Helvetica', fontSize=9, textColor=DARK, leading=11)
    add('PQt',  fontName='Helvetica-Oblique', fontSize=10, textColor=accent, leftIndent=16, rightIndent=16, spaceAfter=5, spaceBefore=5, leading=14)
    return s

def mk_doc(buf, margin=18):
    return SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=margin*mm, rightMargin=margin*mm,
        topMargin=margin*mm, bottomMargin=margin*mm)

def tbl(data, widths, s, accent):
    t = Table(data, colWidths=widths)
    LB = colors.Color(accent.red, accent.green, accent.blue, alpha=0.08)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),accent),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LB]),
        ('BOX',(0,0),(-1,-1),1,accent),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.Color(accent.red,accent.green,accent.blue,0.3)),
        ('PADDING',(0,0),(-1,-1),5),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    return t

def info_box(title, items, s, accent):
    LB = colors.Color(accent.red, accent.green, accent.blue, alpha=0.08)
    rows = [[Paragraph(f'<b>{title}</b>', s['PH3'])]]
    for it in items: rows.append([Paragraph(f'• {it}', s['PTC'])])
    t = Table(rows, colWidths=[155*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),accent),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BACKGROUND',(0,1),(-1,-1),LB),
        ('BOX',(0,0),(-1,-1),1,accent),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.Color(accent.red,accent.green,accent.blue,0.3)),
        ('PADDING',(0,0),(-1,-1),6),
    ]))
    return t

def cover_page(title, subtitle, edition, accent, s):
    items = []
    items.append(Table([[
        Paragraph('ROYAL FITNESS CLUB', ParagraphStyle('COV',fontName='Helvetica-Bold',
            fontSize=11,textColor=colors.white,alignment=1)),
        Paragraph(title, ParagraphStyle('COVT',fontName='Helvetica-Bold',
            fontSize=22,textColor=colors.white,alignment=1,leading=28)),
        Paragraph(subtitle, ParagraphStyle('COVS',fontName='Helvetica',
            fontSize=12,textColor=colors.Color(1,1,1,0.85),alignment=1,leading=16)),
        Paragraph(edition, ParagraphStyle('COVE',fontName='Helvetica-Bold',
            fontSize=10,textColor=colors.Color(1,1,1,0.7),alignment=1)),
    ]], colWidths=[155*mm],
    style=TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),accent),
        ('PADDING',(0,0),(-1,-1),30),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[accent]),
    ])))
    items.append(Spacer(1,8*mm))
    return items

def sp(n=4): return Spacer(1, n*mm)
def hr(accent): return HRFlowable(width='100%',thickness=1,color=accent,spaceAfter=3,spaceBefore=3)

# ─────────────────────────────────────────────────────────────────────────────
# PDF 01 — Advanced Cutting Cycle 12 Weeks
# ─────────────────────────────────────────────────────────────────────────────
def build_01():
    accent = colors.HexColor('#b91c1c')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def h2(t): return Paragraph(t, s['PH2'])
    def h3(t): return Paragraph(t, s['PH3'])
    def p(t):  return Paragraph(t, s['PBody'])
    def bl(t): return Paragraph(f'• {t}', s['PBL'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('ADVANCED CUTTING CYCLE', '12-Week Complete Protocol',
                        'STEROID + CARDIO EDITION', accent, s)
    story += [h1('Overview & Goals'), hr(accent),
        p('This 12-week advanced cutting cycle is designed for experienced users (3+ years training, 2+ years cycle experience) seeking maximum fat loss while preserving hard-earned muscle mass. The protocol combines anabolic steroids with a structured cardio programme and precise nutrition strategy.'), sp(),
        h2('Cycle Snapshot'),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Parameter','Details'],
            ['Duration','12 weeks (84 days)'],
            ['Goal','Fat loss + Muscle preservation'],
            ['User Level','Advanced (3+ years training, 2+ cycles)'],
            ['Compounds','Test Prop / Anavar / Winstrol / Clenbuterol'],
            ['PCT','Nolvadex 40/40/20/20 + Clomid 100/100/50/50'],
            ['Liver Support','TUDCA 500mg/day, NAC 600mg/day'],
            ['Cardio','5×/week LISS + 2×/week HIIT'],
        ])], [50*mm, 105*mm], s, accent), sp()]

    story += [PageBreak(), h1('Week-by-Week Protocol'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Week','Test Prop (mg/EOD)','Anavar (mg/day)','Winstrol (mg/day)','Clen (mcg/day)','Notes'],
            ['1','100','–','–','20','Foundation week — assess tolerance'],
            ['2','100','50','–','40','Introduce Anavar'],
            ['3','100','50','–','60','Ramp Clen'],
            ['4','100','50','–','80','Peak Clen week 1'],
            ['5','100','50','–','100','Hold Clen, add AI if needed'],
            ['6','100','50','–','0','Clen 2-week off cycle'],
            ['7','100','50','50','0','Introduce Winstrol'],
            ['8','100','50','50','20','Restart Clen cycle'],
            ['9','100','50','50','60','Full compound stack'],
            ['10','100','50','50','80','Peak cutting phase'],
            ['11','75','50','50','100','Begin compound taper'],
            ['12','50','50','50','80','Final week — maintain'],
        ])], [14*mm,32*mm,30*mm,30*mm,28*mm,41*mm], s, accent), sp()]

    story += [h1('Cardio Protocol'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Type','Frequency','Duration','Intensity','Timing'],
            ['LISS (fasted walk/cycle)','5×/week','45–60 min','60–65% MHR','Fasted AM'],
            ['HIIT (sprints / bike)','2×/week','20–25 min','85–95% MHR','Post-weights'],
            ['Active recovery','Daily optional','20–30 min','50% MHR','Any time'],
        ])], [35*mm,30*mm,28*mm,30*mm,32*mm], s, accent), sp()]

    story += [h1('Nutrition Blueprint'), hr(accent),
        p('<b>Caloric deficit:</b> 500–700 kcal below TDEE. High protein mandatory to prevent catabolism.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Macro','Amount','Sources'],
            ['Protein','2.2–2.5 g/kg BW','Chicken, fish, egg whites, whey isolate, paneer'],
            ['Carbs','1.5–2.0 g/kg BW','Oats, sweet potato, brown rice, banana'],
            ['Fat','0.6–0.8 g/kg BW','Eggs, almonds, olive oil, fish oil'],
            ['Water','4–5 litres/day','Plain water + electrolytes'],
        ])], [20*mm, 40*mm, 95*mm], s, accent), sp()]

    story += [h1('Side Effect Management'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Side Effect','Cause','Prevention/Treatment'],
            ['Acne','Androgens + oil glands','Benzoyl peroxide wash, zinc, lower test dose'],
            ['Hair thinning','DHT elevation','Nizoral shampoo, RU-58841 topical'],
            ['Joint pain','Winstrol / low estrogen','Fish oil 4g/day, collagen, moderate E2'],
            ['Cardiovascular','Lipid changes','Cardio, omega-3, TUDCA, avoid saturated fat'],
            ['Liver stress','Oral 17-AA compounds','TUDCA 500mg, NAC 600mg, limit duration to 8 wks'],
            ['Sleep disruption','Clenbuterol','Take Clen AM only; melatonin 5mg at night'],
            ['Libido drop','Estrogen imbalance','Dial in AI dose; test blood work at week 6'],
        ])], [35*mm, 35*mm, 85*mm], s, accent), sp()]

    story += [h1('PCT Protocol'), hr(accent),
        p('Post-Cycle Therapy begins 3 days after last Test Prop injection. Duration: 4 weeks.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Week','Nolvadex','Clomid','HCG','Support'],
            ['PCT 1','40mg/day','100mg/day','500 IU EOD (if used)','Zinc, Ashwagandha'],
            ['PCT 2','40mg/day','100mg/day','–','Continue support stack'],
            ['PCT 3','20mg/day','50mg/day','–','Continue support stack'],
            ['PCT 4','20mg/day','50mg/day','–','Continue support stack'],
        ])], [20*mm, 30*mm, 30*mm, 40*mm, 35*mm], s, accent), sp()]

    story += [h1('Blood Work Panel'), hr(accent),
        info_box('Required Blood Tests', [
            'Pre-cycle: Total T, Free T, LH, FSH, E2, CBC, liver panel, lipids, PSA (if 40+)',
            'Week 6: Total T, E2, CBC, liver enzymes, BP check',
            'Post-PCT (week 4): Total T, LH, FSH, E2 — confirm HPTA recovery',
            'Reference: Total T > 400 ng/dL post-PCT = successful recovery',
            'If LH/FSH remain suppressed at 4 weeks post-PCT: extend PCT 2 more weeks',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/01_Advanced_Cutting_Cycle_12Weeks.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 01: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 02 — Advanced Bulking Cycle with Peptides
# ─────────────────────────────────────────────────────────────────────────────
def build_02():
    accent = colors.HexColor('#7c3aed')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def h2(t): return Paragraph(t, s['PH2'])
    def p(t):  return Paragraph(t, s['PBody'])
    def bl(t): return Paragraph(f'• {t}', s['PBL'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('ADVANCED BULKING CYCLE', 'With Peptides · Mass Building Protocol',
                        'COMPLETE MASS EDITION', accent, s)
    story += [h1('Protocol Overview'), hr(accent),
        p('This advanced bulking cycle combines anabolic steroids with growth hormone-releasing peptides (GHRPs/GHRHs) for maximum lean mass gain. Designed for experienced users targeting 8–12 kg of lean mass in 16 weeks.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Parameter','Details'],
            ['Duration','16 weeks'],
            ['Compounds','Test-E + Deca + DBol kickstart + BPC-157 + TB-500'],
            ['Expected Gain','8–12 kg lean mass (with proper nutrition)'],
            ['Caloric Surplus','+500–700 kcal above TDEE'],
            ['Training Split','Push/Pull/Legs × 2 per week (PPL×2)'],
        ])], [45*mm, 110*mm], s, accent), sp()]

    story += [PageBreak(), h1('16-Week Schedule'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Week','Test-E (mg/wk)','Deca (mg/wk)','Dbol (mg/day)','Peptides','Notes'],
            ['1–2','500','–','30','BPC-157 250mcg 2×/day','DBol kickstart'],
            ['3–4','500','300','30','BPC-157 + TB-500 2mg/wk','Full stack begins'],
            ['5–8','500','300','–','BPC-157 250mcg 2×/day','DBol discontinued'],
            ['9–12','600','400','–','TB-500 2mg/wk','Peak bulk phase'],
            ['13–14','500','300','–','BPC-157 250mcg 2×/day','Begin taper'],
            ['15','250','150','–','–','Taper continues'],
            ['16','–','–','–','–','Clearance before PCT'],
        ])], [16*mm,32*mm,30*mm,28*mm,38*mm,31*mm], s, accent), sp()]

    story += [h1('Peptide Protocols'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Peptide','Mechanism','Dose','Timing','Benefit'],
            ['BPC-157','Tendon/ligament healing, GI repair','250 mcg 2×/day','AM fasted + PM','Joint protection under heavy load'],
            ['TB-500','Actin modulation, angiogenesis','2 mg/week','Any time subcut','Muscle repair, recovery speed'],
            ['GHRP-6','GH pulse stimulation','100–200 mcg 3×/day','Pre-sleep + fasted','GH boost, appetite increase'],
            ['CJC-1295','GHRH analogue, sustained GH','100 mcg 3×/day','Same as GHRP-6','Synergy with GHRP for pulse'],
            ['IGF-1 LR3','Muscle satellite activation','50–80 mcg post-workout','Immediately post-training','Local + systemic hypertrophy'],
        ])], [25*mm,40*mm,25*mm,28*mm,37*mm], s, accent), sp()]

    story += [h1('Mass Building Nutrition'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Meal','Time','Foods','Macros (approx)'],
            ['Breakfast','7 AM','6 eggs + 2 roti + banana + milk','P:50g C:80g F:30g'],
            ['Mid-Morning','10 AM','Whey shake + oats + peanut butter','P:40g C:60g F:15g'],
            ['Lunch','1 PM','300g chicken/paneer + 2 cups rice + sabzi','P:60g C:100g F:20g'],
            ['Pre-Workout','4 PM','Banana + creatine + BCAA','P:10g C:40g F:5g'],
            ['Post-Workout','7 PM','Whey + 2 roti + dal','P:55g C:70g F:12g'],
            ['Dinner','9 PM','200g fish/soya + sweet potato + curd','P:50g C:60g F:15g'],
            ['Pre-Sleep','11 PM','Cottage cheese or casein shake','P:35g C:10g F:8g'],
        ])], [28*mm,18*mm,65*mm,44*mm], s, accent), sp()]

    story += [h1('Joint & Health Protection'), hr(accent),
        info_box('Essential On-Cycle Support Stack', [
            'Liver: TUDCA 500mg/day + NAC 600mg/day',
            'Cardiovascular: Fish oil 4g/day + CoQ10 200mg/day + Garlic 1000mg',
            'Blood pressure: Hawthorn berry 500mg + taurine 5g (for Dbol)',
            'Joints: Collagen 15g/day + glucosamine 1500mg + BPC-157 (see peptide protocol)',
            'Estrogen control: Anastrozole 0.5mg EOD (adjust to blood work)',
            'Prolactin (from Deca): Cabergoline 0.25mg 2×/week',
            'Sleep/recovery: Ashwagandha 600mg + zinc 30mg + magnesium 400mg',
        ], s, accent), sp()]

    story += [h1('Bulking Training Split'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Day','Session','Key Exercises','Volume'],
            ['Mon','Push A','Bench press, incline DB, cable fly, OHP, tricep ext','5×5 + 3×10'],
            ['Tue','Pull A','Deadlift, barbell row, lat pulldown, face pull, curls','5×5 + 3×10'],
            ['Wed','Legs A','Squat, leg press, RDL, leg curl, calf raise','5×5 + 3×12'],
            ['Thu','Rest/Active','Light cardio, mobility, stretching','30–45 min'],
            ['Fri','Push B','Dips, DB shoulder press, lateral raise, close-grip bench','4×8–12'],
            ['Sat','Pull B','Weighted pull-up, cable row, hammer curl, face pull','4×8–12'],
            ['Sun','Legs B / Rest','Bulgarian split squat, hack squat, glute bridge','4×10–12'],
        ])], [14*mm,20*mm,70*mm,51*mm], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/02_Advanced_Bulking_Cycle_with_Peptides.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 02: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 03 — Beginner Steroid Cycle Full Guide
# ─────────────────────────────────────────────────────────────────────────────
def build_03():
    accent = colors.HexColor('#ea580c')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    def bl(t): return Paragraph(f'• {t}', s['PBL'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('BEGINNER STEROID CYCLE', 'Full Guide · Safe Entry-Level Protocol',
                        'HARM REDUCTION EDITION', accent, s)
    story += [h1('Before You Begin — Prerequisites'), hr(accent),
        info_box('Minimum Requirements Before First Cycle', [
            'Training age: minimum 3 years of consistent, structured training',
            'Natty potential: you must have reached near-natural genetic maximum first',
            'Age: minimum 25 years (ideally 25–35 for HPTA safety)',
            'Health: full blood panel showing normal hormones, liver, kidneys, lipids',
            'Body fat: below 15% (men) / 22% (women) — cycles work poorly at high BF%',
            'Knowledge: you have read and understood PCT, AI use, injection technique',
            'No personal/family history of: prostate cancer, heart disease, clotting disorders',
        ], s, accent), sp()]

    story += [h1('The Beginner Protocol — Test-E Only'), hr(accent),
        p('The first cycle should ALWAYS be testosterone-only. This establishes your baseline response to exogenous testosterone before adding complexity. Testosterone Enanthate (Test-E) is the gold standard for beginners due to its long half-life (infrequent injections) and well-understood profile.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Week','Test-E (mg/week)','Anastrozole','HCG (IU/week)','Notes'],
            ['1','250','–','500 EOD','Start HCG immediately for testicular preservation'],
            ['2','250','0.25mg EOD','500 EOD','Monitor for high E2 symptoms'],
            ['3','250','0.25mg EOD','500 EOD','Assess: water retention, acne, mood'],
            ['4','500','0.25mg EOD','500 EOD','Ramp to working dose'],
            ['5–10','500','0.25mg E3D','500 EOD','Main cycle phase'],
            ['11','350','0.25mg E3D','500 EOD','Begin taper'],
            ['12','200','0.25mg E3D','500 EOD','Final injections'],
            ['13–14','–','–','–','Clearance (ester half-life)'],
            ['PCT 1–2','–','–','–','Nolvadex 40mg/day + Clomid 100mg/day'],
            ['PCT 3–4','–','–','–','Nolvadex 20mg/day + Clomid 50mg/day'],
        ])], [16*mm,36*mm,28*mm,28*mm,47*mm], s, accent), sp()]

    story += [PageBreak(), h1('Injection Guide'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Site','Needle Size','Volume','Technique','Benefit'],
            ['Glute (ventroglute)','23G 1.5 inch','2 mL max','Z-track, aspirate','Least painful, large muscle'],
            ['Quad (vastus lateralis)','25G 1 inch','1.5 mL max','Perpendicular, slow push','Easy to self-inject'],
            ['Delt (lateral head)','25G 1 inch','1 mL max','45° angle, small muscle','Convenient, visible'],
        ])], [38*mm,28*mm,24*mm,45*mm,20*mm], s, accent), sp(),
        info_box('Injection Sterility Protocol', [
            'Wash hands thoroughly with soap for 20 seconds',
            'Swab vial top and injection site with 70% isopropyl alcohol; allow to dry',
            'Use new, sterile needle for every injection — never reuse',
            'Draw with 18G needle; switch to 23–25G for injection',
            'Inject slowly (1 mL per 10 seconds minimum)',
            'Rotate injection sites — no same site more than once per week',
            'Dispose in sharps container — never regular bin',
        ], s, accent), sp()]

    story += [h1('Estrogen Management'), hr(accent),
        p('Testosterone aromatises to estradiol (E2). Too high causes: water retention, gynecomastia, mood swings, fatigue. Too low causes: joint pain, low libido, depression, poor recovery. The goal is optimal E2 (20–35 pg/mL).'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['E2 Level','Symptoms','Action'],
            ['< 15 pg/mL (too low)','Joint aches, brain fog, no libido, dry skin','Reduce AI dose; if no AI, wait'],
            ['15–35 pg/mL (optimal)','Good mood, libido, strength, no retention','Maintain current AI dose'],
            ['35–60 pg/mL (high)','Water retention, nipple sensitivity, moodiness','Increase AI dose slightly'],
            ['> 60 pg/mL (very high)','Gyno flare, extreme retention, emotional','Add SERM (Nolvadex 20mg) immediately + AI'],
        ])], [38*mm,60*mm,57*mm], s, accent), sp()]

    story += [h1('Gynecomastia Prevention & Response'), hr(accent),
        info_box('Gyno Emergency Protocol', [
            'Immediate: Start Nolvadex 40mg/day + Letrozole 2.5mg/day for 2 weeks',
            'After 2 weeks: Drop Letrozole, continue Nolvadex 20mg/day for 4 more weeks',
            'Prevention: Keep E2 in range; have Nolvadex on hand before cycle starts',
            'Pubertal gyno (already present): may require surgical intervention; consult doctor',
            'Lumps vs puffiness: Hard, moveable lump = gyno. Soft puff = water retention',
        ], s, accent), sp()]

    story += [h1('Realistic Expectations'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Phase','Timeline','What to Expect'],
            ['Weeks 1–3','Setup phase','Little noticeable change; compounds building in blood'],
            ['Weeks 4–6','Activation','Noticeable strength increase, pumps, improved recovery'],
            ['Weeks 7–10','Peak gains','Visible muscle fullness, scale weight rising 1–2 kg/week'],
            ['Week 11–12','Taper','Maintain gains; mental preparation for PCT'],
            ['PCT weeks 1–4','Recovery','Some weight loss (water); maintain training intensity'],
            ['Post-PCT month 1–3','Stabilisation','Retain 50–70% of cycle gains if training/nutrition remain consistent'],
        ])], [28*mm,28*mm,99*mm], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/03_Beginner_Steroid_Cycle_Full_Guide.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 03: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 04 — 30-Day Keto Indian Vegetarian Plan
# ─────────────────────────────────────────────────────────────────────────────
def build_04():
    accent = colors.HexColor('#15803d')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    def bl(t): return Paragraph(f'• {t}', s['PBL'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('30-DAY KETO INDIAN PLAN', 'Vegetarian · Desi-Friendly Meal Templates',
                        'COMPLETE MEAL PLAN EDITION', accent, s)
    story += [h1('Ketogenic Diet Fundamentals'), hr(accent),
        p('A ketogenic diet restricts carbohydrates to < 50g/day, shifting your body\'s primary fuel from glucose to ketones (derived from fat). For Indians, going keto requires replacing rice, roti, and dal with low-carb Indian alternatives without sacrificing the flavours and textures of desi cuisine.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Macro','Standard Keto %','Grams (2000 kcal)','Indian Sources'],
            ['Fat','65–75%','145–165g','Ghee, coconut oil, paneer, nuts, avocado, cream'],
            ['Protein','20–25%','100–125g','Paneer, tofu, soya chunks, eggs, curd, cheese'],
            ['Carbs','< 5%','< 25g','Leafy greens, cauliflower, zucchini, brinjal'],
        ])], [20*mm,30*mm,32*mm,73*mm], s, accent), sp()]

    story += [h1('Indian Keto-Friendly Staples'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Category','Use This','Instead Of','Carb Saving'],
            ['Roti substitute','Almond flour roti (2g net carb)','Wheat roti (25g carb)','23g/roti'],
            ['Rice substitute','Cauliflower rice (3g/cup)','White rice (45g/cup)','42g/cup'],
            ['Thickener','Cream / coconut cream','Cornflour / arrowroot','Full save'],
            ['Sweet','Stevia / erythritol ladoo','Jaggery / sugar mithai','Full save'],
            ['Snack','Paneer tikka / cheese','Samosa / chakli','15–30g/snack'],
            ['Dal substitute','Soya granules curry','Chana/rajma dal (high carb)','20g/bowl'],
            ['Breakfast','Egg bhurji / paneer bhurji','Poha / upma / paratha','30–50g/meal'],
        ])], [28*mm,52*mm,42*mm,33*mm], s, accent), sp()]

    story += [PageBreak(), h1('4-Week Meal Plan Overview'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Week','Theme','Daily Kcal','Net Carbs/Day','Key Focus'],
            ['Week 1','Keto adaptation','1800–2000','20–25g','Enter ketosis; manage keto flu'],
            ['Week 2','Fat adaptation','1800–2000','20–25g','Energy stabilises; hunger decreases'],
            ['Week 3','Optimisation','1700–1900','15–20g','Deepen ketosis; introduce fasting'],
            ['Week 4','Consolidation','1600–1800','15–20g','Maximum fat loss; sustain ketones'],
        ])], [18*mm,30*mm,30*mm,30*mm,47*mm], s, accent), sp()]

    story += [h1('Sample Day Meal Plan (All 4 Weeks)'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Meal','Food','Kcal','Net Carbs','Protein','Fat'],
            ['Breakfast 7AM','3 eggs bhurji in ghee + 1 almond roti + black chai','380','4g','22g','30g'],
            ['Lunch 1PM','150g paneer butter masala (cream-based) + cauliflower rice','520','8g','28g','38g'],
            ['Snack 4PM','Handful almonds + string cheese + bulletproof coffee','300','3g','12g','26g'],
            ['Dinner 7PM','Palak paneer (rich gravy) + 1 almond roti + salad','480','7g','30g','35g'],
            ['Pre-sleep','30g whey isolate in water or MCT oil bulletproof chai','180','2g','25g','8g'],
            ['TOTAL','','1,860','24g','117g','137g'],
        ])], [28*mm,70*mm,18*mm,24*mm,22*mm,13*mm], s, accent), sp()]

    story += [h1('Managing Keto Flu'), hr(accent),
        info_box('Keto Flu Remedies (Days 3–7)', [
            'Sodium: add salt liberally; have 1–2 cups salted bone broth or vegetable broth',
            'Potassium: eat avocado, spinach, mushrooms; consider No-Salt (potassium chloride)',
            'Magnesium: 300–400mg magnesium glycinate before bed (prevents cramps)',
            'Hydration: 3.5–4.5 litres water daily; electrolyte drink without sugar',
            'Headache: usually sodium depletion; try a glass of warm salted water',
            'Fatigue (days 3–5): normal — your brain is adapting. Reduce workout intensity',
            'Constipation: psyllium husk 10g/day + leafy greens + extra water',
        ], s, accent), sp()]

    story += [h1('30-Day Progress Tracker'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Metric','Day 1','Day 7','Day 14','Day 21','Day 30'],
            ['Weight (kg)','','','','',''],
            ['Waist (cm)','','','','',''],
            ['Energy (1–10)','','','','',''],
            ['Hunger (1–10)','','','','',''],
            ['Ketone level (mmol/L)','','','','',''],
            ['Workout performance (1–10)','','','','',''],
        ])], [48*mm,22*mm,22*mm,22*mm,22*mm,19*mm], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/04_30Day_Keto_Indian_Vegetarian_Plan.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 04: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 05 — Female Vegetarian Weight Loss Plan
# ─────────────────────────────────────────────────────────────────────────────
def build_05():
    accent = colors.HexColor('#be185d')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    def bl(t): return Paragraph(f'• {t}', s['PBL'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page("FEMALE VEGETARIAN WEIGHT LOSS", 'Hormone-Safe Protocol · Indian Vegetarian',
                        'COMPLETE TRANSFORMATION GUIDE', accent, s)
    story += [h1('Female-Specific Physiology'), hr(accent),
        p('Women\'s bodies respond differently to diet and exercise due to hormonal cycles, higher fat storage requirements for reproductive health, and different muscle fibre composition. This plan accounts for all these factors to create safe, effective, and sustainable fat loss.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Difference','Impact on Fat Loss','Plan Adjustment'],
            ['Higher oestrogen','Greater fat storage (esp. hips/thighs)','Strength training to counteract; no extreme deficits'],
            ['Monthly cycle','Energy/strength varies by phase','Periodise training intensity to cycle phase'],
            ['Lower testosterone','Slower muscle building','Higher protein; resistance training mandatory'],
            ['Thyroid sensitivity','Metabolism slows with crash diets','Max deficit 400–500 kcal; refeed weeks every 4 weeks'],
            ['PCOS (common)','Insulin resistance, higher androgens','Lower-GI carbs; strength training; inositol supplement'],
        ])], [35*mm,45*mm,75*mm], s, accent), sp()]

    story += [PageBreak(), h1('Menstrual Cycle Training Guide'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Phase','Days','Hormones','Training','Nutrition'],
            ['Menstrual','1–5','Low oestrogen & prog.','Light: yoga, walk, mobility','Warm foods; extra iron (spinach, dates)'],
            ['Follicular','6–13','Rising oestrogen','High intensity; PBs possible','Normal deficit; carb around workouts'],
            ['Ovulation','14','Oestrogen peak','Maximum strength & HIIT','Maintenance calories; highest protein'],
            ['Luteal','15–28','Progesterone dominant','Moderate training; reduce HIIT','+200–300 kcal; expect 1–2 kg water weight'],
        ])], [22*mm,16*mm,38*mm,40*mm,39*mm], s, accent), sp()]

    story += [h1('12-Week Vegetarian Meal Plan'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Meal','Food','Calories','Protein'],
            ['Breakfast 7AM','Moong dal chilla × 3 + green chutney + 1 cup green tea','340','18g'],
            ['Mid-Morning 10AM','1 cup curd + ½ cup pomegranate + 5 almonds','180','8g'],
            ['Lunch 1PM','1 cup rajma / dal + 2 small roti + sabzi + salad','420','20g'],
            ['Pre-workout 4PM','Banana + 1 tbsp peanut butter','200','5g'],
            ['Post-workout 6PM','Soya chunks (50g dry) + 1 cup curd','260','28g'],
            ['Dinner 8PM','Paneer bhurji (100g) + 1 roti + cucumber raita','380','25g'],
            ['TOTAL','','1,780','104g'],
        ])], [28*mm,75*mm,28*mm,24*mm], s, accent), sp()]

    story += [h1('12-Week Training Plan'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Week','Training Focus','Sessions/Wk','Key Exercises'],
            ['1–3','Foundation','3 full body + 2 cardio','Goblet squat, push-up, bent-over row, plank'],
            ['4–6','Strength intro','3 strength + 2 LISS','Dumbbell squat, DB press, lat pull, RDL'],
            ['7–9','Progressive overload','4 strength + 2 HIIT','Barbell squat, bench, deadlift variations'],
            ['10–12','Body recomposition','4 strength + 2 HIIT','Full compound programme + isolation finishers'],
        ])], [18*mm,35*mm,28*mm,74*mm], s, accent), sp()]

    story += [h1('Supplements for Indian Women'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Supplement','Dose','Purpose','Indian Brands'],
            ['Whey protein (vegetarian)','20–25g post-workout','Hit protein targets','MuscleBlaze, AS-IT-IS, Optimum'],
            ['Iron','18–27mg elemental','Prevent anaemia (esp. menstruation)','Ferrous fumarate; take with vitamin C'],
            ['Vitamin D3','2000–5000 IU/day','Bone health, hormones, mood','Any brand; take with fat'],
            ['Omega-3 (algae)','1–2g EPA+DHA','Anti-inflammatory; hormone balance','Vegetable source; safe for vegetarians'],
            ['Inositol (PCOS)','2–4g/day myo-inositol','Insulin sensitivity, menstrual regulation','NOW Foods, Jarrow'],
            ['Calcium','500mg 2×/day','Bone density (veg diet may be low)','Calcium citrate best absorbed'],
            ['B12','500–1000mcg/day','Essential (vegetarians often deficient)','Methylcobalamin form best'],
        ])], [35*mm,28*mm,48*mm,44*mm], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/05_Female_Vegetarian_Weight_Loss_Plan.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 05: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 06 — Complete Peptide Protocol Bible
# ─────────────────────────────────────────────────────────────────────────────
def build_06():
    accent = colors.HexColor('#3730a3')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    def bl(t): return Paragraph(f'• {t}', s['PBL'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('COMPLETE PEPTIDE PROTOCOL BIBLE', 'Scientific Reference Guide · All Major Peptides',
                        'RESEARCH EDITION', accent, s)
    story += [h1('Peptide Fundamentals'), hr(accent),
        p('Peptides are short chains of amino acids (2–50 AAs) that act as signalling molecules in the body. Unlike anabolic steroids, most peptides work by stimulating the body\'s own production of hormones (especially growth hormone and IGF-1) rather than replacing them exogenously.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Category','Examples','Primary Action','Main Use'],
            ['GHRPs','GHRP-2, GHRP-6, Ipamorelin','Stimulate GH pulse from pituitary','Mass, fat loss, recovery'],
            ['GHRHs','CJC-1295, Sermorelin, Tesamorelin','Extend/amplify GH pulse','Synergy with GHRPs'],
            ['Repair peptides','BPC-157, TB-500','Tissue healing, angiogenesis','Injury recovery, gut repair'],
            ['Metabolic','AOD-9604, Fragment 176-191','Fat cell lipolysis','Fat loss only'],
            ['Selective','PT-141, Melanotan II','CNS/melanocortin activation','Libido, tanning'],
            ['Cognition','Semax, Selank','Neuroprotection, BDNF','Focus, anxiety, recovery'],
        ])], [25*mm,35*mm,45*mm,50*mm], s, accent), sp()]

    story += [PageBreak(), h1('GH-Releasing Peptides — Detailed Profiles'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Peptide','Dose','Frequency','Half-life','Side Effects','Best For'],
            ['GHRP-6','100–200 mcg','3×/day','<30 min','Hunger spike, cortisol','Mass gain; appetite stimulation'],
            ['GHRP-2','100–200 mcg','3×/day','<30 min','Cortisol, prolactin','GH pulse, no hunger'],
            ['Ipamorelin','200–300 mcg','2–3×/day','2 hrs','Minimal','Cleanest GHRP; best starter'],
            ['Hexarelin','200 mcg','2×/day','<30 min','Desensitisation','Short cycles only; cardiac'],
            ['CJC-1295 (DAC)','2 mg/week','1–2×/week','8 days','Blunted natural pulses','Steady GH raise'],
            ['CJC-1295 (no DAC)','100 mcg','3×/day (with GHRP)','30 min','Minimal','Best synergy with GHRPs'],
            ['Sermorelin','200–500 mcg','Before sleep','12 min','Injection site','Anti-aging, sleep GH'],
        ])], [28*mm,23*mm,22*mm,18*mm,40*mm,24*mm], s, accent), sp()]

    story += [h1('BPC-157 Complete Guide'), hr(accent),
        p('Body Protection Compound 157 (BPC-157) is a 15-amino acid peptide derived from a protein found in gastric juice. It is the single most researched peptide for tissue repair and shows extraordinary healing properties in animal studies.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Condition','Protocol','Route','Duration','Expected Outcome'],
            ['Tendon/ligament injury','250 mcg 2×/day','Subcutaneous near injury OR oral','4–8 weeks','Accelerated healing 40–60%'],
            ['Muscle tear','250–500 mcg/day','Subcutaneous near tear','2–4 weeks','Faster fibre repair'],
            ['Gut issues (IBS, leaky gut)','250 mcg 2×/day','Oral (capsule)','8–12 weeks','Gut lining repair, reduced inflammation'],
            ['General recovery','200 mcg/day','Subcutaneous any site','Ongoing (cycle 6 on/4 off)','Improved recovery between sessions'],
            ['Joint protection (cycle)','250 mcg 2×/day','Subcutaneous near joints','Duration of cycle','Prevents steroid-induced joint damage'],
        ])], [38*mm,30*mm,23*mm,22*mm,42*mm], s, accent), sp()]

    story += [h1('Peptide Stacking Protocols'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Goal','Peptide Stack','Daily Dose','Timing','Duration'],
            ['Maximum GH pulse','Ipamorelin + CJC-1295 (no DAC)','300+100 mcg each','Fasted AM + pre-sleep','12 weeks on, 4 off'],
            ['Injury recovery','BPC-157 + TB-500','250 mcg + 2mg/wk','BPC 2×/day; TB weekly','Until healed + 2 wks'],
            ['Body recomposition','AOD-9604 + Ipamorelin','300+300 mcg','AM fasted + pre-sleep','16 weeks'],
            ['Anti-aging','Sermorelin + BPC-157','500+250 mcg','Pre-sleep + AM','Ongoing (12 on/4 off)'],
            ['Bulking assist','GHRP-6 + CJC-1295 + BPC-157','200+100+250 mcg','3×/day (GHRP/CJC); BPC 2×','16 weeks on cycle'],
        ])], [35*mm,50*mm,28*mm,38*mm,24*mm], s, accent), sp()]

    story += [h1('Reconstitution & Storage Guide'), hr(accent),
        info_box('Peptide Handling Protocol', [
            'Reconstitute with bacteriostatic water (BacWater) — NOT regular water',
            'Standard: 1 mL BacWater per 2 mg peptide = 2000 mcg/mL concentration',
            'Inject BacWater slowly down the SIDE of the vial — never directly on powder',
            'Gently swirl — never shake (denatures the peptide)',
            'Storage: unreconstituted = freezer up to 2 years; reconstituted = fridge, use within 4 weeks',
            'Syringes: 29–31G insulin syringes; 0.5–1 mL volume',
            'Always allow to reach room temperature before injection',
        ], s, accent), sp()]

    story += [h1('Peptide Safety & Legality'), hr(accent),
        p('<b>Research chemical status:</b> Most peptides are sold as "research chemicals" — not approved for human use. This means quality varies significantly between suppliers. Testing for purity is strongly recommended.'), sp(),
        info_box('Red Flags When Buying Peptides', [
            'No independent third-party testing (HPLC certificate)',
            'Price far below market average (diluted or counterfeit)',
            'No clear labelling of peptide sequence and purity %',
            'No bacteriostatic water included — serious sterility issue',
            'Vendor cannot answer questions about reconstitution',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/06_Complete_Peptide_Protocol_Bible.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 06: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 07 — SARMs Complete Scientific Handbook
# ─────────────────────────────────────────────────────────────────────────────
def build_07():
    accent = colors.HexColor('#4338ca')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('SARMs SCIENTIFIC HANDBOOK', 'Complete Research-Backed Edition',
                        'ALL MAJOR SARMs PROFILED', accent, s)
    story += [h1('What Are SARMs?'), hr(accent),
        p('Selective Androgen Receptor Modulators (SARMs) are a class of compounds that bind to androgen receptors with tissue selectivity — targeting muscle and bone while theoretically sparing prostate, liver, and other androgen-sensitive tissues. Originally developed for muscle wasting diseases and osteoporosis.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['SARMs vs Steroids','SARMs','Anabolic Steroids'],
            ['Oral bioavailability','High (most SARMs)','Varies (orals: yes; injectables: no)'],
            ['Liver toxicity','Low–moderate','Moderate–high (orals)'],
            ['Aromatisation','None (most SARMs)','Yes (testosterone, Deca)'],
            ['HPTA suppression','Moderate','Severe'],
            ['Androgenic side effects','Low','High'],
            ['Anabolic potential','Moderate','High'],
            ['Regulatory status','Research chemical (not FDA approved)','Controlled substances (Schedule III in US)'],
        ])], [45*mm,52*mm,58*mm], s, accent), sp()]

    story += [PageBreak(), h1('Complete SARMs Profile Table'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['SARM','Dose (mg/day)','Half-life','Best For','Suppression','Notes'],
            ['Ostarine (MK-2866)','15–25 (men)','24 hrs','Recomp, beginner','Low–Mod','Mildest; best first SARM'],
            ['RAD-140 (Testolone)','10–20','60 hrs','Strength, mass','High','Most anabolic; liver watch'],
            ['LGD-4033 (Ligandrol)','5–10','24–36 hrs','Mass gain','Moderate–High','Dose-dependent suppression'],
            ['Cardarine (GW-501516)','10–20','16–24 hrs','Endurance, fat loss','NONE','Not a SARM; PPARδ agonist'],
            ['MK-677 (Ibutamoren)','15–25','24 hrs','GH pulse, sleep, recovery','None','Not a SARM; GH secretagogue'],
            ['S-23','10–30','12 hrs','Cutting, hardness','Severe','Most suppressive; needs PCT'],
            ['YK-11','5–15','6–10 hrs','Extreme mass','High','Partial myostatin inhibitor'],
            ['SR-9009 (Stenabolic)','20–30 (split)','4–6 hrs','Fat loss, endurance','None','Low bioavailability oral'],
            ['Andarine (S-4)','25–50','4 hrs','Cutting','Moderate','Vision yellow tint side effect'],
            ['ACP-105','5–15','Unknown','Recomp','Low–Mod','Newer; limited human data'],
        ])], [33*mm,26*mm,22*mm,28*mm,24*mm,42*mm], s, accent), sp()]

    story += [h1('Stacking Protocols'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Goal','Stack','Duration','PCT Needed?'],
            ['Beginner recomp','Ostarine 15mg + Cardarine 10mg','8 weeks','Mini-PCT (Nolvadex 20mg × 4 wks)'],
            ['Lean bulk','LGD-4033 10mg + MK-677 20mg','12 weeks','Full PCT (Nolvadex/Clomid)'],
            ['Aggressive bulk','RAD-140 15mg + LGD-4033 5mg + MK-677 20mg','10 weeks','Full PCT required'],
            ['Cutting','Ostarine 20mg + Cardarine 20mg + SR-9009 20mg','8 weeks','Mini-PCT'],
            ['Recomp','RAD-140 10mg + Cardarine 15mg','8 weeks','Full PCT'],
            ['Endurance','Cardarine 20mg + SR-9009 30mg','6–8 weeks','No PCT needed'],
        ])], [27*mm,62*mm,22*mm,44*mm], s, accent), sp()]

    story += [h1('SARMs PCT Guide'), hr(accent),
        p('SARMs suppress the HPTA (hypothalamic-pituitary-testicular axis) to varying degrees. Always test LH, FSH, and Total T before and after a cycle. If suppression is detected, run PCT:'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['PCT Type','When to Use','Protocol','Duration'],
            ['Mini-PCT','Mild stacks (Ostarine-only, etc.)','Nolvadex 20mg/day','4 weeks'],
            ['Full PCT','Moderate-high suppression stacks','Nolvadex 40/40/20/20 + Clomid 100/50/50/50','4 weeks'],
            ['Natural recovery only','Cardarine/SR-9009 only','No PCT needed; supplement support','4–8 weeks'],
        ])], [25*mm,48*mm,55*mm,27*mm], s, accent), sp()]

    story += [h1('Health Monitoring Protocol'), hr(accent),
        info_box('Required Blood Tests On SARMs', [
            'Pre-cycle: Total T, Free T, LH, FSH, E2, SHBG, liver enzymes (ALT/AST), CBC, lipids',
            'Mid-cycle (week 4–6): Total T, liver enzymes, lipids — check for suppression/liver stress',
            'Post-PCT (4 weeks after): Total T, LH, FSH, E2 — confirm HPTA recovery',
            'Concerning findings: Total T < 300 ng/dL post-PCT; ALT/AST > 3× baseline; HDL drop > 30%',
            'Recovery timeline: LH/FSH usually return within 4–8 weeks post-SARM if SARMs used alone',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/07_SARMs_Complete_Scientific_Handbook.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 07: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 08 — TRT Hormone Optimization Guide
# ─────────────────────────────────────────────────────────────────────────────
def build_08():
    accent = colors.HexColor('#b45309')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('TRT HORMONE OPTIMIZATION GUIDE', 'Testosterone Replacement · Monitoring · Protocols',
                        'MEDICAL & PERFORMANCE EDITION', accent, s)
    story += [h1('Understanding TRT'), hr(accent),
        p('Testosterone Replacement Therapy (TRT) restores testosterone to physiological (normal) levels in men with clinically diagnosed hypogonadism. At medical TRT doses, the goal is wellness — not supraphysiological performance.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['TRT Type','Description','Target T Level'],
            ['Medical TRT','Prescribed by doctor; restores to normal range','400–700 ng/dL'],
            ['Optimised TRT','Slightly above normal; enhanced wellbeing','700–1000 ng/dL'],
            ['TRT + ancillaries','HCG + AI added; fertility preservation','700–900 ng/dL + normal LH/FSH'],
        ])], [35*mm,80*mm,40*mm], s, accent), sp()]

    story += [PageBreak(), h1('TRT Protocol Options'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Delivery Method','Dose','Frequency','Pros','Cons'],
            ['Test-C injection','100–200 mg/mL','Weekly or E3.5D','Cost-effective, consistent levels','Injections; requires technique'],
            ['Test-E injection','100–200 mg/mL','Weekly or E3.5D','Long-established, cheap','Same as above'],
            ['Testosterone gel','50–100 mg/day','Daily application','No injections, easy','Transfer risk; variable absorption'],
            ['Testosterone pellets','150–450 mg','Every 3–6 months','Long duration, consistent','Surgical implant; inflexible dose'],
            ['Testosterone undecanoate','1000 mg/3 mL','Every 10 weeks','Very infrequent dosing','Expensive; requires clinic'],
        ])], [35*mm,25*mm,23*mm,45*mm,27*mm], s, accent), sp()]

    story += [h1('TRT Blood Work Reference'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Marker','Optimal Range (on TRT)','Action if Out of Range'],
            ['Total Testosterone','600–900 ng/dL','Adjust dose; timing of draw (trough)'],
            ['Free Testosterone','15–25 pg/mL','May need SHBG management (Boron, Proviron)'],
            ['Estradiol (E2)','20–35 pg/mL','Add AI if > 40; reduce if < 15'],
            ['SHBG','20–40 nmol/L','Low SHBG: more frequent smaller doses'],
            ['Haematocrit','< 52%','Donate blood if > 52%; reduces clot risk'],
            ['LH/FSH','Near zero (expected on TRT)','Add HCG if fertility matters'],
            ['PSA','< 2.0 ng/mL','Annual check; consult urologist if rising'],
            ['Lipids (HDL/LDL)','HDL > 40; LDL < 130','Cardio, omega-3, statin if needed'],
            ['Liver (ALT/AST)','< 2× upper limit','Oral forms more hepatotoxic; switch to injectable'],
        ])], [40*mm,45*mm,70*mm], s, accent), sp()]

    story += [h1('HCG on TRT'), hr(accent),
        p('HCG (Human Chorionic Gonadotropin) mimics LH and maintains testicular function, volume, and intratesticular testosterone while on TRT. Essential for men who want to preserve fertility.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['HCG Use Case','Dose','Frequency','Benefit'],
            ['Fertility preservation on TRT','500–1000 IU','3×/week','Maintains sperm production'],
            ['Testicular atrophy prevention','250–500 IU','2–3×/week','Prevents shrinkage'],
            ['Restart before PCT (if cycling)','500 IU','EOD × 4 weeks before PCT','Kickstarts HPTA'],
            ['Low libido despite good T levels','500 IU','2×/week','Raises intratesticular T'],
        ])], [50*mm,22*mm,25*mm,58*mm], s, accent), sp()]

    story += [h1('Lifestyle Optimisation on TRT'), hr(accent),
        info_box('Maximise TRT Results', [
            'Resistance training 3–5×/week: amplifies testosterone\'s anabolic signal',
            'Sleep 7–9 hours: GH release and T recovery happen during deep sleep',
            'Body fat: keep BF < 20%; adipose tissue aromatises T to estrogen',
            'Alcohol: limit to < 2 units/week; alcohol suppresses T and elevates estrogen',
            'Stress management: chronic cortisol competes with and lowers T receptor sensitivity',
            'Zinc 30mg + Magnesium 400mg + Vitamin D 5000 IU: support T pathway enzymes',
            'Avoid plastics (BPA), pesticides, and xenoestrogens where possible',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/08_TRT_Hormone_Optimization_Guide.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 08: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 09 — Science of Muscle Hypertrophy
# ─────────────────────────────────────────────────────────────────────────────
def build_09():
    accent = colors.HexColor('#1d4ed8')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('SCIENCE OF MUSCLE HYPERTROPHY', 'Muscle Growth Mechanisms & Evidence-Based Methods',
                        'TRAINING MANUAL', accent, s)
    story += [h1('The Three Mechanisms of Hypertrophy'), hr(accent),
        p('Current evidence identifies three primary mechanical stimuli that drive muscle protein synthesis and subsequent hypertrophy: mechanical tension, metabolic stress, and muscle damage. Understanding each allows you to design training programmes that maximise all three.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Mechanism','Description','How to Maximise','Primary Rep Range'],
            ['Mechanical Tension','Force applied to sarcomeres during contraction + stretch','Heavy compound lifts; slow eccentrics','3–8 reps (85–90% 1RM)'],
            ['Metabolic Stress','Accumulation of metabolites (lactate, H+, Pi)','Higher reps, short rest, occlusion','12–20 reps (60–75% 1RM)'],
            ['Muscle Damage','Micro-tears in muscle fibres (especially eccentric)','Novel exercises; eccentric emphasis','8–15 reps; 3–5 sec eccentric'],
        ])], [32*mm,50*mm,45*mm,28*mm], s, accent), sp()]

    story += [PageBreak(), h1('Progressive Overload Methods'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Method','How to Apply','Best Phase','Example'],
            ['Load progression','Add 2.5–5 kg when rep target achieved','Strength phase','Bench: 80 kg × 4 → 82.5 kg × 4'],
            ['Volume progression','Add 1 set per exercise per week','Hypertrophy phase','3×10 → 4×10 over 4 weeks'],
            ['Density progression','Same work in less time','Metabolic phase','Same sets/reps; rest 90→75→60 sec'],
            ['Frequency progression','Add training days per week','Advanced phase','3×/week → 4×/week upper body'],
            ['ROM progression','Increase range of motion','Skill phase','Squat depth, fuller pull-up ROM'],
            ['Technique progression','Reduce compensation; purer form','Foundation phase','Eliminate bar drift in deadlift'],
        ])], [35*mm,45*mm,28*mm,47*mm], s, accent), sp()]

    story += [h1('Optimal Training Variables'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Variable','Hypertrophy Optimum','Notes'],
            ['Sets per muscle/week','10–20 (MEV–MRV range)','Start at 10; add volume gradually'],
            ['Reps per set','6–20 (peak: 8–12)','Multiple rep ranges = fuller stimulus'],
            ['Effort (RIR)','0–2 RIR per set','Must approach failure for max stimulus'],
            ['Rest between sets','60–180 seconds','Compound: 2–3 min; isolation: 60–90 sec'],
            ['Frequency per muscle','2–3×/week','More frequent = more MPS spikes/week'],
            ['Tempo','2–0–2 to 4–0–1','Slow eccentrics for damage mechanism'],
            ['Muscle length at stretch','Train in stretched position','Lengthened partial reps show high hypertrophy'],
        ])], [40*mm,40*mm,75*mm], s, accent), sp()]

    story += [h1('Muscle Protein Synthesis (MPS)'), hr(accent),
        p('MPS is the molecular process by which the body repairs and builds new muscle proteins. A single training session elevates MPS for 24–48 hours. To maximise hypertrophy, MPS must consistently exceed muscle protein breakdown (MPB).'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['MPS Driver','Requirement','Practical Action'],
            ['Leucine threshold','~2.5–3g leucine per meal','40g whey = 3.5g leucine; 200g chicken = 3g'],
            ['Protein dose','0.4 g/kg per meal (4–5 meals)','80 kg man = 32g protein every 4–5 hrs'],
            ['Total daily protein','1.6–2.2 g/kg BW/day','80 kg = 128–176g protein/day'],
            ['Protein distribution','Even spread across meals','Not front- or back-loaded'],
            ['Pre-sleep protein','40g casein/cottage cheese','Keeps MPS elevated during overnight fast'],
        ])], [35*mm,45*mm,75*mm], s, accent), sp()]

    story += [h1('Periodisation for Continuous Growth'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Phase','Duration','Rep Range','Intensity','Goal'],
            ['Anatomical adaptation','2–4 weeks','15–20','60–65%','Tendon/ligament prep; form'],
            ['Hypertrophy','6–8 weeks','8–12','70–80%','Maximum muscle growth'],
            ['Strength','4–6 weeks','3–6','82–92%','Neural efficiency; strength base'],
            ['Power (optional)','2–4 weeks','3–5 explosive','70–80%','Rate of force development'],
            ['Deload','1 week','50% volume','Reduce 30%','Recovery; supercompensation'],
        ])], [35*mm,22*mm,22*mm,22*mm,54*mm], s, accent), sp()]

    story += [h1('Recovery Optimisation'), hr(accent),
        info_box('The 5 Recovery Pillars', [
            '1. Sleep: 7–9 hours; GH peaks in slow-wave sleep; MPS continues during sleep',
            '2. Nutrition: protein every 4–5 hours; carbs post-workout for glycogen resynthesis',
            '3. Hydration: 35 mL/kg/day minimum; muscles are 75% water',
            '4. Stress management: cortisol inhibits MPS; practice mindfulness + limit overwork',
            '5. Deload weeks: every 4–6 weeks; reduces cumulative fatigue while retaining adaptations',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/09_Science_of_Muscle_Hypertrophy.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 09: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDF 10 — Ultimate Fat Loss Masterclass
# ─────────────────────────────────────────────────────────────────────────────
def build_10():
    accent = colors.HexColor('#b91c1c')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('ULTIMATE FAT LOSS MASTERCLASS', 'Evidence-Based Protocol · No Gimmicks',
                        'COMPLETE EDITION', accent, s)
    story += [h1('The Fat Loss Equation'), hr(accent),
        p('Fat loss occurs when energy expenditure exceeds energy intake (caloric deficit). All diets that work do so by creating this deficit — whether keto, IF, LCHF, or calorie counting. The challenge is maintaining the deficit while preserving muscle, managing hunger, and sustaining consistency.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Deficit Size','Weekly Loss','Risk','Best For'],
            ['250 kcal/day','~250g fat/week','Minimal; sustainable long-term','Slow recomp; advanced trainees'],
            ['500 kcal/day','~500g fat/week','Low; optimal for most','Standard cut; most people'],
            ['750 kcal/day','~750g fat/week','Moderate; some muscle risk','Aggressive cut with high protein'],
            ['1000+ kcal/day','1 kg+/week','High; muscle loss, hormonal disruption','Short-term only (obese individuals)'],
        ])], [28*mm,26*mm,48*mm,53*mm], s, accent), sp()]

    story += [PageBreak(), h1('TDEE & Calorie Calculation'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Activity Level','Multiplier','Example (70 kg, sedentary BMR ~1700)'],
            ['Sedentary (desk job, no exercise)','×1.2','1700 × 1.2 = 2,040 kcal TDEE'],
            ['Lightly active (1–3 workouts/week)','×1.375','1700 × 1.375 = 2,338 kcal TDEE'],
            ['Moderately active (4–5 workouts/week)','×1.55','1700 × 1.55 = 2,635 kcal TDEE'],
            ['Very active (hard training + physical job)','×1.725','1700 × 1.725 = 2,933 kcal TDEE'],
            ['Elite athlete (2× daily training)','×1.9','1700 × 1.9 = 3,230 kcal TDEE'],
        ])], [55*mm,24*mm,76*mm], s, accent), sp()]

    story += [h1('Macros for Fat Loss'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Macro','Target (cutting)','Why','Indian Sources'],
            ['Protein','2.2–2.5 g/kg BW','Muscle preservation; most satiating macro','Paneer, dal, eggs, chicken, soya, curd'],
            ['Fat','0.7–1.0 g/kg BW','Hormones, satiety, fat-soluble vitamins','Ghee, nuts, olive oil, egg yolks'],
            ['Carbs','Fill remaining calories','Energy for training; performance','Rice, oats, roti, potato, banana'],
        ])], [20*mm,28*mm,47*mm,60*mm], s, accent), sp()]

    story += [h1('7 Evidence-Based Fat Loss Strategies'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Strategy','Mechanism','Implementation','Effect Size'],
            ['High protein diet','Thermic effect 25–30%; hunger control','≥ 2g/kg protein every day','★★★★★'],
            ['Resistance training','Preserves muscle; raises RMR','3–4×/week compound lifts','★★★★★'],
            ['Cardio (LISS + HIIT)','Burns additional calories','LISS 4×45min + HIIT 2×20min/week','★★★★'],
            ['Sleep 7–9 hours','Controls ghrelin/leptin; reduces cravings','Fixed sleep schedule; dark/cool room','★★★★'],
            ['Calorie tracking (6 weeks)','Awareness eliminates unconscious overeating','MyFitnessPal or HealthifyMe daily','★★★★'],
            ['High volume foods','Low calorie density = more food volume','Salad, soup, cucumber, watermelon first','★★★'],
            ['Intermittent fasting','Reduces eating window; TDEE reduction','16:8 or 5:2; not magic but helpful','★★★'],
        ])], [30*mm,45*mm,45*mm,20*mm], s, accent), sp()]

    story += [h1('Plateau Protocol'), hr(accent),
        p('Fat loss plateaus occur when the body adapts to the deficit through metabolic adaptation (reduced RMR), increased efficiency, and hormonal changes. Here\'s how to break every plateau:'), sp(),
        info_box('Plateau-Breaking Strategies (Apply in Order)', [
            '1. Recalculate TDEE — your TDEE drops as you lose weight (recalculate every 5 kg lost)',
            '2. Refeed day — 1 day at maintenance calories (high carb) to restore leptin; do weekly if stuck',
            '3. Diet break — 1–2 weeks at maintenance; alleviates hormonal adaptation; resume with fresh metabolism',
            '4. Increase NEAT — 2,000 extra steps/day; stand more; take stairs; park far',
            '5. Change cardio stimulus — if doing only LISS, add HIIT; if doing HIIT, add fasted LISS',
            '6. Re-audit food logging — weigh all food for 1 week; "eyeballing" creates up to 40% underestimation',
            '7. Check hormones — if plateaued > 3 weeks: thyroid, cortisol, insulin sensitivity issues possible',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/10_Ultimate_Fat_Loss_Masterclass.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 10: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
# PDFs 11-15: compact but complete
# ─────────────────────────────────────────────────────────────────────────────
def build_11_15():
    """Build PDFs 11-15 with complete content."""

    # PDF 11 — Women's Complete Body Transformation
    accent = colors.HexColor('#9333ea')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page("WOMEN'S COMPLETE BODY TRANSFORMATION", 'Body Recomposition Guide · Strength + Fat Loss',
                        'COMPLETE PROGRAMME', accent, s)
    story += [h1('Body Recomposition vs Weight Loss'), hr(accent),
        p('Body recomposition means simultaneously losing fat and gaining muscle — the true transformation goal. Unlike simple weight loss, recomp changes your body SHAPE, not just the number on the scale.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Method','Scale Weight','Fat Mass','Muscle Mass','Shape'],
            ['Calorie restriction only','↓ Fast','↓','↓ Also lost!','Smaller, same shape'],
            ['Cardio only','↓ Moderate','↓','↓ Some loss','Smaller, still soft'],
            ['Strength training only','→ or ↑','↓','↑ Gained!','Firmer, more defined'],
            ['Body recomp (this plan)','→ or slightly ↑','↓↓','↑↑','Completely transformed'],
        ])], [45*mm,25*mm,25*mm,25*mm,35*mm], s, accent), sp()]

    story += [PageBreak(), h1('12-Week Training Programme'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Phase','Weeks','Focus','Key Exercises','Sessions/Wk'],
            ['Foundation','1–3','Movement patterns','Goblet squat, hip hinge, push, pull','3 full body'],
            ['Build','4–6','Progressive overload begins','DB squat, RDL, DB press, rows','4 sessions'],
            ['Sculpt','7–9','High volume + isolation','Barbell compound + glute/shoulder isolation','4–5 sessions'],
            ['Shred','10–12','Intensity + cardio','Full programme + HIIT 3×/week','5 sessions'],
        ])], [20*mm,18*mm,40*mm,55*mm,22*mm], s, accent), sp()]

    story += [h1('Glute Development Protocol'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Exercise','Sets × Reps','Key Cue','Load'],
            ['Hip thrust (barbell)','4 × 10–12','Full glute squeeze at top, 2-sec hold','Heavy'],
            ['Romanian deadlift','3 × 10–12','Hip hinge, feel hamstring stretch','Moderate-Heavy'],
            ['Bulgarian split squat','3 × 10 each','Front foot forward; torso slightly leaned','Moderate'],
            ['Cable kickback','3 × 15 each','Extend at hip, not knee; squeeze glute','Light-Moderate'],
            ['Sumo squat','4 × 12','Toes out 45°; sit back into hips','Moderate-Heavy'],
            ['Abductor machine','3 × 20','Controlled tempo; full ROM','Light'],
        ])], [40*mm,28*mm,55*mm,22*mm], s, accent), sp()]

    story += [h1('Nutrition for Body Recomposition'), hr(accent),
        info_box('Female Recomp Nutrition Rules', [
            'Protein: 1.8–2.2 g/kg BW — non-negotiable for muscle building while in deficit',
            'Calories: slight deficit (200–300 kcal) on rest days; maintenance on training days',
            'Carb timing: 50–60% of daily carbs around workouts (before and after)',
            'Iron: 18mg/day minimum; menstrual loss increases need; pair with Vitamin C',
            'Calcium: 1000mg/day; resistance training without calcium = bone stress fracture risk',
            'Refeed: once per week at maintenance or slight surplus; prevents metabolic adaptation',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/11_Womens_Complete_Body_Transformation.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 11: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

    # PDF 12 — Indian Bodybuilder Nutrition Bible
    accent = colors.HexColor('#0f766e')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('INDIAN BODYBUILDER NUTRITION BIBLE', 'Desi Macros · Meal Plans · Indian Food Database',
                        'BODYBUILDER EDITION', accent, s)
    story += [h1('Indian Protein Sources — Complete Database'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Food','Serving','Protein','Carbs','Fat','Cost/100g Protein'],
            ['Paneer (full fat)','100g','18g','1.2g','20g','₹55'],
            ['Soya chunks (dry)','100g','52g','33g','0.5g','₹8'],
            ['Moong dal (cooked)','1 cup','14g','39g','0.8g','₹12'],
            ['Chana dal (cooked)','1 cup','15g','45g','1.2g','₹10'],
            ['Chicken breast','100g','31g','0','3.6g','₹35'],
            ['Eggs (whole)','2 eggs','12g','0.7g','10g','₹18'],
            ['Egg whites','4 whites','14g','0.7g','0','₹15'],
            ['Tuna (canned)','100g','26g','0','1.0g','₹40'],
            ['Curd (full fat)','200g','7g','8g','8g','₹20'],
            ['Milk (full fat)','500 mL','17g','24g','20g','₹30'],
            ['Whey protein','1 scoop 30g','24g','3g','1.5g','₹60–120'],
            ['Tofu (firm)','100g','17g','2g','9g','₹20'],
        ])], [38*mm,20*mm,18*mm,16*mm,14*mm,29*mm], s, accent), sp()]

    story += [PageBreak(), h1('Indian Bulking Meal Plan (3500–4000 kcal)'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Meal','Food','Kcal','Protein'],
            ['Breakfast 7AM','6 eggs scrambled + 3 roti + banana + 500mL milk','900','65g'],
            ['Mid-Morning 10AM','Peanut butter oats (1 cup oats + 2 tbsp PB + whey)','650','45g'],
            ['Lunch 1PM','300g chicken curry + 2 cups rice + dal + curd','850','70g'],
            ['Pre-workout 4PM','2 roti + peanut butter + banana','450','18g'],
            ['Post-workout 7PM','Whey shake + 50g soya chunks sabzi + 1 cup rice','550','55g'],
            ['Dinner 9PM','200g paneer + 2 roti + rajma/chole + sabzi','650','45g'],
            ['Pre-sleep 11PM','1 cup curd + 30g casein protein shake','300','35g'],
            ['TOTAL','','4,350','333g'],
        ])], [28*mm,80*mm,22*mm,25*mm], s, accent), sp()]

    story += [h1('Indian Cutting Meal Plan (2200–2500 kcal)'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Meal','Food','Kcal','Protein'],
            ['Breakfast 7AM','3 egg whites + 1 whole egg + moong dal chilla × 2','350','30g'],
            ['Mid-Morning 10AM','100g soya chunks (boiled) + cucumber + lemon','200','26g'],
            ['Lunch 1PM','150g grilled chicken / tofu + 1 cup brown rice + sabzi','450','40g'],
            ['Snack 4PM','1 cup curd + 10 almonds','200','12g'],
            ['Post-workout 7PM','Whey shake + 1 banana','300','28g'],
            ['Dinner 8:30PM','200g fish / 150g paneer + large salad + 1 roti','400','38g'],
            ['Pre-sleep','Casein shake 30g','150','25g'],
            ['TOTAL','','2,050','199g'],
        ])], [28*mm,80*mm,22*mm,25*mm], s, accent), sp()]

    story += [h1('Supplement Stack for Indian Athletes'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Supplement','Dose','Timing','Indian Brand / Budget Option'],
            ['Creatine monohydrate','5g/day','Any time (consistency > timing)','AS-IT-IS, MuscleBlaze (₹500/month)'],
            ['Whey protein','25–40g/day','Post-workout + between meals','Optimum, MuscleBlaze, MyProtein India'],
            ['Vitamin D3','2000–5000 IU','Morning with fat','Any generic brand (₹150–300/month)'],
            ['Omega-3','2–3g EPA+DHA','With meals','Himalaya, HealthKart (₹400/month)'],
            ['Ashwagandha','600mg KSM-66','Night','Himalaya, Patanjali (₹200–400/month)'],
            ['Zinc + Magnesium','Zinc 30mg + Mag 400mg','Before bed','ZMA supplement or separate'],
        ])], [30*mm,25*mm,30*mm,70*mm], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/12_Indian_Bodybuilder_Nutrition_Bible.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 12: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

    # PDF 13 — Pre-Workout Optimization Guide
    accent = colors.HexColor('#7e22ce')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('PRE-WORKOUT OPTIMIZATION GUIDE', 'Stacking Protocols · Ingredient Science',
                        'COMPLETE REFERENCE', accent, s)
    story += [h1('Pre-Workout Ingredients — Complete Guide'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Ingredient','Effective Dose','Mechanism','Benefit','Timing'],
            ['Caffeine','150–300 mg','Adenosine antagonist','Energy, focus, fat oxidation','30–45 min pre'],
            ['Beta-Alanine','3.2–6.4g/day','Carnosine precursor; buffers H+','Endurance; delays fatigue','Daily loading'],
            ['Citrulline malate','6–8g (2:1 ratio)','NO precursor; arginine sparing','Pumps, endurance','30–45 min pre'],
            ['Creatine','5g/day','ATP regeneration','Strength, power, muscle','Any time'],
            ['L-Theanine','100–200mg (with caffeine)','α-wave promotion','Smooth energy; no jitters','With caffeine'],
            ['Betaine anhydrous','2.5g','Osmolyte; creatine-like','Power output, hydration','Pre-workout'],
            ['Tyrosine','500–2000mg','Catecholamine precursor','Focus under stress','30 min pre; fasted'],
            ['Nitrosigine','1.5g','Enhanced arginine form','Pumps; superior to arginine','30 min pre'],
            ['DMHA / DMAA','AVOID','CNS stimulant','Banned; cardiac risk','Never'],
        ])], [30*mm,28*mm,40*mm,32*mm,25*mm], s, accent), sp()]

    story += [PageBreak(), h1('Pre-Workout Stacks by Goal'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Goal','Stack','Total Cost (DIY/month)','Notes'],
            ['Energy + Focus','Caffeine 200mg + L-Theanine 200mg + Tyrosine 1g','₹400–600','Clean energy; no crash'],
            ['Maximum Pump','Citrulline 8g + Nitrosigine 1.5g + Beetroot extract 500mg','₹600–900','No stimulants; good for evening'],
            ['Endurance','Caffeine 150mg + Beta-Alanine 3.2g + Creatine 5g','₹500–700','Add sodium bicarbonate for acidosis'],
            ['Strength','Creatine 5g + Betaine 2.5g + Caffeine 200mg','₹500–800','Best compound lift performance'],
            ['Complete Pre-Workout','Caffeine 200mg + Theanine 200mg + Citrulline 6g + BA 3.2g + Creatine 5g','₹800–1200','DIY beat commercial products'],
        ])], [27*mm,62*mm,32*mm,34*mm], s, accent), sp()]

    story += [h1('Caffeine Optimisation'), hr(accent),
        info_box('Getting the Most from Caffeine', [
            'Cycle caffeine: 5 days on, 2 days off — prevents tolerance build-up',
            'Delay first dose to 90 min after waking (after cortisol peak fades)',
            'Pair always with L-Theanine (2:1 ratio Theanine:Caffeine) for smooth energy',
            'Last dose by 2 PM to avoid sleep disruption (half-life = 5–6 hours)',
            'Total daily dose: 400mg maximum for healthy adults (FDA guideline)',
            'Sources: coffee, green tea, caffeine anhydrous (powder/pills) — all equivalent',
            'Avoid: proprietary blends hiding caffeine dose; energy drinks with sugar',
        ], s, accent), sp()]

    story += [h1('Indian DIY Pre-Workout Recipes'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Recipe','Ingredients','Cost/serving','When'],
            ['Desi PWO #1 (basic)','Black coffee + 5g creatine + pinch salt','₹15','30 min pre'],
            ['Desi PWO #2 (pump)','Watermelon juice 300mL + citrulline 6g + creatine 5g','₹25','30 min pre'],
            ['Desi PWO #3 (advanced)','Green tea × 2 cups + L-theanine + beta-alanine 3.2g + creatine','₹20','45 min pre'],
            ['Natural pre-PWO','Banana + strong chai + beetroot 100g (roasted)','₹30','60 min pre'],
        ])], [28*mm,70*mm,25*mm,27*mm], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/13_PreWorkout_Optimization_Guide.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 13: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

    # PDF 14 — Natural Testosterone Optimization
    accent = colors.HexColor('#c2410c')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('NATURAL TESTOSTERONE OPTIMIZATION', 'Without Compounds · Evidence-Based Lifestyle Protocol',
                        'COMPLETE GUIDE', accent, s)
    story += [h1('Understanding Natural Testosterone'), hr(accent),
        p('Natural testosterone peaks in the 20s (600–900 ng/dL typical) and declines ~1–2% per year after 30. Many factors within your control can keep T high across decades — diet, training, sleep, stress, and specific supplements with proven effects.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Factor','T Impact','Magnitude','How to Fix'],
            ['Sleep deprivation (< 5 hrs)','↓ T','−10–15%/night','7–9 hrs sleep; treat sleep apnoea'],
            ['Obesity (BF% > 25%)','↓ T','−20–30%','Fat loss via deficit; resistance training'],
            ['Chronic stress (high cortisol)','↓ T','−10–20%','Meditation; workload management; adaptogens'],
            ['Alcohol (> 14 units/week)','↓ T','−6–23%','Reduce or eliminate alcohol'],
            ['Resistance training (3–4×/week)','↑ T','+10–25%','Compound lifts; progressive overload'],
            ['Vitamin D deficiency','↓ T','−20–30% if deficient','5000 IU D3/day + K2'],
            ['Zinc deficiency','↓ T','Significant','Oysters, red meat, ZMA supplement'],
        ])], [40*mm,16*mm,22*mm,77*mm], s, accent), sp()]

    story += [PageBreak(), h1('Natural T-Boosting Supplement Evidence'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Supplement','T Effect','Dose','Evidence Level','Indian Availability'],
            ['Ashwagandha (KSM-66)','↑ T 17%, ↓ Cortisol 27%','600mg/day','★★★★★','Himalaya, Patanjali, generic'],
            ['Vitamin D3','↑ T significantly if deficient','5000 IU + K2 100mcg','★★★★★','Any pharmacy'],
            ['Zinc','Prevents deficiency-related T drop','30mg/day (ZMA form)','★★★★','MuscleBlaze ZMA'],
            ['Fadogia Agrestis','Possible LH/T stimulation','600mg/day','★★ (limited data)','Online import'],
            ['Tongkat Ali','↑ Free T; reduces SHBG','400–600mg 2% extract','★★★','Online import'],
            ['Boron','Reduces SHBG; raises free T','10mg/day','★★★','NOW Foods'],
            ['Shilajit','↑ Total/Free T 20% in studies','300–500mg PrimaVie form','★★★','Patanjali; speciality stores'],
            ['Fenugreek','Aromatase inhibition; T support','500–600mg/day','★★★','Methi seeds / capsules'],
            ['Maca root','Libido; no direct T effect','1.5–3g/day','★★','Online'],
        ])], [32*mm,32*mm,24*mm,22*mm,45*mm], s, accent), sp()]

    story += [h1('The Natural T Optimisation Lifestyle'), hr(accent),
        info_box('Daily Protocol for Maximum Natural Testosterone', [
            'Morning: 10–15 min sunlight exposure (Vitamin D synthesis + circadian reset)',
            'Training: 4–5 compound-focused sessions/week; heavy squats and deadlifts are top T stimulators',
            'Diet: adequate dietary fat (0.8–1.0 g/kg); cholesterol is testosterone precursor — don\'t avoid',
            'Protein: 1.8–2.2 g/kg; branched-chain AAs support T signalling pathways',
            'Avoid: excessive cardio (> 90 min/day chronically suppresses T); xenoestrogens (plastics, pesticides)',
            'Supplements (daily): Ashwagandha 600mg + D3 5000 IU + Zinc 30mg + Shilajit 300mg',
            'Sleep: non-negotiable 7–9 hours; 80% of daily T production occurs during sleep',
        ], s, accent), sp()]

    story += [h1('Training Protocol for T Optimisation'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Exercise Type','T Response','How','Protocol'],
            ['Heavy compound (squats/deadlifts)','★★★★★ acute spike','Use 80–95% 1RM; 3–5 reps','3–5 sets; 3–5 min rest'],
            ['Moderate compound (bench/row/OHP)','★★★★','70–80% 1RM; 5–8 reps','4 sets; 2–3 min rest'],
            ['High volume hypertrophy','★★★','60–70% 1RM; 10–15 reps; short rest','3–4 sets; 60–90 sec rest'],
            ['Long cardio > 60 min','↓ Temporarily','Excessive cardio raises cortisol','Limit to 3×/week max 45 min'],
            ['HIIT sprints','★★★ short-term','30-sec max effort × 8–10 sets','2×/week; not same day as heavy lifts'],
        ])], [40*mm,24*mm,45*mm,46*mm], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/14_Natural_Testosterone_Optimization.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 14: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

    # PDF 15 — Recovery Sleep CNS Restoration
    accent = colors.HexColor('#0369a1')
    s = make_styles(accent)
    def h1(t): return Paragraph(t, s['PH1'])
    def p(t):  return Paragraph(t, s['PBody'])
    buf = io.BytesIO()
    doc = mk_doc(buf)
    story = []
    story += cover_page('RECOVERY & CNS RESTORATION', 'Sleep, HRV & Nervous System Guide',
                        'COMPLETE RECOVERY MANUAL', accent, s)
    story += [h1('The Recovery Hierarchy'), hr(accent),
        p('Recovery is the process by which the body repairs, adapts, and grows stronger in response to training stress. Without adequate recovery, training is just stress — no adaptation occurs.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Recovery Level','Time to Recover','What Recovers','How to Accelerate'],
            ['Phosphocreatine (PCr)','2–5 minutes','ATP-PCr system for explosive work','Complete rest between sets'],
            ['Glycogen','24–48 hours','Muscle energy stores','High-carb post-workout meal within 2 hrs'],
            ['Muscle microtrauma','48–72 hours','Structural protein repair','Protein 2g/kg; sleep; cold therapy'],
            ['CNS fatigue','72–120 hours','Neural drive capacity','Deload; sleep; reduce training volume'],
            ['Hormonal recovery','Days–weeks','Cortisol, testosterone, GH balance','Stress reduction; consistent sleep; nutrition'],
        ])], [38*mm,28*mm,45*mm,44*mm], s, accent), sp()]

    story += [PageBreak(), h1('HRV — Heart Rate Variability Monitoring'), hr(accent),
        p('HRV measures the variation in time between heartbeats — a higher variation indicates a well-recovered, parasympathetically dominant state. Daily HRV tracking is the most objective measure of readiness to train.'), sp(),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['HRV Score (vs baseline)','Interpretation','Training Recommendation'],
            ['> +10% above baseline','Excellent recovery; high readiness','High-intensity session; test PRs'],
            ['Within ±5% of baseline','Normal; acceptable readiness','Planned session as designed'],
            ['5–15% below baseline','Moderate fatigue; proceed with caution','Reduce intensity 20%; skip heavy lifts'],
            ['> 15% below baseline','Significant fatigue/stress/illness','Active recovery only: walk, stretch, yoga'],
        ])], [45*mm,40*mm,70*mm], s, accent), sp()]

    story += [h1('Active Recovery Protocols'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Method','Mechanism','Duration','Indian Application'],
            ['Light walking (LISS)','Blood flow; lactate clearance','20–30 min at 50% MHR','Morning walk in park'],
            ['Cold water immersion','Vasoconstriction; inflammation reduction','10–15 min at 10–15°C','Cold bath or cold bucket shower'],
            ['Contrast therapy','Alternating vasoconstriction/dilation','Hot 3 min → cold 1 min × 4','Shower alternation'],
            ['Yoga / stretching','Parasympathetic activation; ROM','20–40 min','Yoga Nidra, Supta poses'],
            ['Massage / foam rolling','Myofascial release; DOMS reduction','10–20 min target areas','Roll quads, lats, thoracic'],
            ['Sauna (if available)','HSP upregulation; GH boost up to 200%','15–20 min at 80–90°C','Gym sauna; steam room'],
        ])], [32*mm,40*mm,28*mm,55*mm], s, accent), sp()]

    story += [h1('Sleep Stack for Athletes'), hr(accent),
        tbl([[Paragraph(c, s['PTH'] if r==0 else s['PTC']) for c in row] for r,row in enumerate([
            ['Supplement','Dose','Mechanism','Indian Brand'],
            ['Ashwagandha','600mg KSM-66','Reduces cortisol; improves sleep quality score','Himalaya, generic KSM-66'],
            ['Magnesium glycinate','300–400mg','GABA activation; muscle relaxation','NOW Foods; HealthKart'],
            ['L-Theanine','200mg','α-wave induction; reduces sleep latency','Standalone powder; cheap'],
            ['Melatonin','0.5–3mg (low dose)','Sleep onset; circadian signal','Any pharmacy; low dose best'],
            ['Valerian root','300–600mg','GABA receptor modulation','Himalaya StressCare has it'],
            ['Zinc','30mg (ZMA form)','GH release; dream vividness; testosterone','MuscleBlaze ZMA'],
        ])], [30*mm,25*mm,55*mm,45*mm], s, accent), sp()]

    story += [h1('CNS Recovery Programme'), hr(accent),
        info_box('Weekly CNS Recovery Protocol', [
            'Monday (heavy session day): foam roll 10 min post-session; cold shower',
            'Tuesday (moderate): contrast shower morning; 20 min yoga evening',
            'Wednesday (deload or rest): 30 min walk; mobility session; full sleep stack',
            'Thursday (heavy): same as Monday; add 10 min breathing exercises',
            'Friday (moderate): contrast shower; 15 min foam roll + stretch',
            'Saturday (active recovery): swimming / cycling 30 min at low intensity',
            'Sunday (rest): complete rest; sleep 9+ hours; meal prep; no screens after 9 PM',
        ], s, accent), sp()]

    doc.build(story)
    with open('generated_pdfs/15_Recovery_Sleep_CNS_Restoration.pdf','wb') as f:
        f.write(buf.getvalue())
    print(f"PDF 15: {len(PdfReader(io.BytesIO(buf.getvalue())).pages)} pages")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import os
    os.chdir('/home/user/royal-fitness-club')
    print("Building catalog PDFs 01–10...")
    build_01(); build_02(); build_03(); build_04(); build_05()
    build_06(); build_07(); build_08(); build_09(); build_10()
    print("Building catalog PDFs 11–15...")
    build_11_15()
    print("Done.")
