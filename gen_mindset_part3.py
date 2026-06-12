#!/usr/bin/env python3
"""Part 3 extension — pushes Fitness Mindset Guidance to 50+ pages."""
import io
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, HRFlowable)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from PyPDF2 import PdfWriter, PdfReader

W, H = A4
BLUE       = colors.HexColor('#0066cc')
DARK       = colors.HexColor('#1a1a2e')
LIGHT_BLUE = colors.HexColor('#e8f0fe')
GREEN_BG   = colors.HexColor('#e8f4e8')

def build_part3():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm)

    s = getSampleStyleSheet()
    def add_s(name, **kw):
        if name not in s:
            s.add(ParagraphStyle(name=name, **kw))
        else:
            for k, v in kw.items():
                setattr(s[name], k, v)

    add_s('H1', fontName='Helvetica-Bold', fontSize=22, textColor=BLUE,
          spaceAfter=8, spaceBefore=14, leading=26)
    add_s('H2', fontName='Helvetica-Bold', fontSize=15, textColor=DARK,
          spaceAfter=6, spaceBefore=10, leading=18)
    add_s('H3', fontName='Helvetica-Bold', fontSize=12, textColor=BLUE,
          spaceAfter=4, spaceBefore=8, leading=15)
    add_s('Body', fontName='Helvetica', fontSize=10, spaceAfter=5,
          leading=14, textColor=colors.HexColor('#333333'))
    add_s('BulletP', fontName='Helvetica', fontSize=10, spaceAfter=3,
          leading=13, leftIndent=14, bulletIndent=4,
          textColor=colors.HexColor('#333333'))
    add_s('Quote', fontName='Helvetica-Oblique', fontSize=11,
          textColor=BLUE, leftIndent=20, rightIndent=20,
          spaceAfter=6, spaceBefore=6, leading=15)
    add_s('TH', fontName='Helvetica-Bold', fontSize=9,
          textColor=colors.white, leading=12)
    add_s('TC', fontName='Helvetica', fontSize=9,
          textColor=DARK, leading=12)

    def h1(t): return Paragraph(t, s['H1'])
    def h2(t): return Paragraph(t, s['H2'])
    def h3(t): return Paragraph(t, s['H3'])
    def p(t):  return Paragraph(t, s['Body'])
    def bl(t): return Paragraph(f'• {t}', s['BulletP'])
    def qt(t): return Paragraph(f'"{t}"', s['Quote'])
    def sp(n=4): return Spacer(1, n*mm)
    def hr(): return HRFlowable(width='100%', thickness=1, color=BLUE,
                                spaceAfter=4, spaceBefore=4)

    TS = TableStyle
    def tbl(data, widths, header=True):
        t = Table(data, colWidths=widths)
        style = [
            ('BOX', (0,0), (-1,-1), 1, BLUE),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ]
        if header:
            style += [('BACKGROUND', (0,0), (-1,0), BLUE),
                      ('TEXTCOLOR', (0,0), (-1,0), colors.white)]
        t.setStyle(TS(style))
        return t

    def info_box(title, items, bg=LIGHT_BLUE):
        rows = [[Paragraph(f'<b>{title}</b>', s['H3'])]]
        for it in items:
            rows.append([Paragraph(f'• {it}', s['TC'])])
        t = Table(rows, colWidths=[155*mm])
        t.setStyle(TS([
            ('BACKGROUND', (0,0), (-1,0), BLUE),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('BACKGROUND', (0,1), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 1, BLUE),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    story = []

    # ── Appendix D: 60-Day Habit Tracker ──────────────────────────────────────
    story += [PageBreak(), h1('Appendix D: 60-Day Habit Tracker'),
              p('Print this page and place it where you train or eat. Tick each habit daily. A visual record of consistency is one of the most powerful motivation tools available. Never break the chain — but if you do, focus on not breaking it twice in a row.'), sp()]

    tracker_header = [Paragraph('<b>Habit</b>', s['TH'])] + [
        Paragraph(f'<b>W{w}</b>', s['TH']) for w in range(1, 9)]
    tracker_rows = [tracker_header]
    habits = [
        'Morning workout / walk',
        'Protein goal hit (≥1g/kg BW)',
        'Water goal hit (≥3 litres)',
        'Sleep 7–9 hours',
        'No processed food / junk',
        'Evening mindfulness (5+ min)',
        'Journalled intentions',
        'No alcohol / tobacco',
        'Morning sunlight exposure',
        'Stretching / mobility work',
    ]
    for h in habits:
        row = [Paragraph(h, s['TC'])] + [Paragraph('□ □ □ □ □ □ □', s['TC']) for _ in range(8)]
        tracker_rows.append(row)

    widths = [55*mm] + [12.5*mm]*8
    t = Table(tracker_rows, colWidths=widths)
    t.setStyle(TS([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story += [t, sp(),
              p('<i>Each □ = 1 day. 7 checkboxes per week column (W1–W8 = 8 weeks / 56 days).</i>'), sp()]

    # ── Appendix E: 12-Week Mindset Progression Milestones ────────────────────
    story += [PageBreak(), h1('Appendix E: 12-Week Mindset Progression Milestones'),
              p('This appendix maps out what psychological growth looks like week by week across a standard 12-week fitness programme. Use it as a reference to normalise what you are experiencing and to anticipate what comes next.'), sp()]

    milestones = [
        ['<b>Week</b>', '<b>Physical State</b>', '<b>Mindset State</b>', '<b>Key Challenge</b>', '<b>Champion Action</b>'],
        ['1–2', 'DOMS, fatigue, awkward form', 'High motivation, novelty excitement', 'Expecting fast results', 'Document baseline; trust the process'],
        ['3–4', 'Form improving, energy more stable', 'Motivation dip (honeymoon ends)', '"Is this worth it?"', 'Fall in love with the process, not results'],
        ['5–6', 'Noticeable strength gains', 'Building confidence', 'Social pressure from peers', 'Find one supportive person; ignore the rest'],
        ['7–8', 'First visible body changes possible', 'Identity beginning to shift', 'Plateau or slower progress', 'Change one training variable; trust adaptation'],
        ['9–10', 'Significant fitness improvements', 'Habit becomes automatic', 'Complacency risk', 'Set new challenging micro-goals'],
        ['11–12', 'Near transformation complete', 'Champion identity solidifying', '"What\'s next?" anxiety', 'Plan phase 2 before phase 1 ends'],
    ]
    mt = Table([[Paragraph(c, s['TH'] if r==0 else s['TC']) for c in row]
                for r, row in enumerate(milestones)],
               colWidths=[14*mm, 38*mm, 38*mm, 35*mm, 30*mm])
    mt.setStyle(TS([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story += [mt, sp()]

    # ── Appendix F: Mind-Muscle Connection Protocols ──────────────────────────
    story += [PageBreak(), h1('Appendix F: Mind-Muscle Connection Protocols'),
              p('The mind-muscle connection (MMC) is the deliberate focus of conscious attention on the muscle being trained. EMG studies consistently show that athletes with strong MMC activate 20–35% more motor units in the target muscle, leading to superior hypertrophy with the same load.'), sp()]

    story += [h2('F.1 How to Develop Mind-Muscle Connection'),
              bl('Pre-activation touch: Lightly touch the target muscle before each set'),
              bl('Isometric holds: Hold the contracted position for 2 seconds at peak contraction'),
              bl('Slow eccentrics: Lower the weight over 3–4 seconds while focusing on the stretch'),
              bl('Visualisation before sets: Imagine the muscle fibers shortening and lengthening'),
              bl('Reduced weight: Use 60–70% of your working weight when building MMC'),
              bl('Mirror training: Watch the muscle contract when possible'),
              sp()]

    mmc_data = [
        ['<b>Exercise</b>', '<b>Target Muscle</b>', '<b>MMC Cue</b>', '<b>Common Error</b>'],
        ['Push-up / Bench Press', 'Pectorals', '"Push the floor away with your chest, not your hands"', 'Letting shoulders dominate'],
        ['Pull-up / Row', 'Latissimus Dorsi', '"Pull your elbows to your back pockets"', 'Using biceps/forearms primarily'],
        ['Squat', 'Quadriceps/Glutes', '"Push the floor apart, squeeze glutes at top"', 'Passive descent, knee cave'],
        ['Deadlift', 'Hamstrings/Glutes', '"Leg press the floor, hinge hips back on descent"', 'Rounding lower back'],
        ['Shoulder Press', 'Deltoids', '"Push ceiling with the side of your hands"', 'Triceps compensating'],
        ['Curl', 'Biceps', '"Supinate (twist outward) at peak; resist on descent"', 'Swinging elbows forward'],
        ['Tricep Extension', 'Triceps', '"Lock elbow in place; move only the forearm"', 'Shoulder/elbow flaring'],
        ['Calf Raise', 'Gastrocnemius/Soleus', '"Full range: deep stretch → complete plantar flex"', 'Partial range, bouncing'],
    ]
    mmct = Table([[Paragraph(c, s['TH'] if r==0 else s['TC']) for c in row]
                  for r, row in enumerate(mmc_data)],
                 colWidths=[38*mm, 32*mm, 52*mm, 33*mm])
    mmct.setStyle(TS([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story += [mmct, sp()]

    # ── Appendix G: The Mental Strength Glossary ──────────────────────────────
    story += [PageBreak(), h1('Appendix G: The Mental Strength Glossary'),
              p('A comprehensive glossary of psychological terms, mindset concepts, and mental performance frameworks referenced throughout this guide.'), sp()]

    glossary = [
        ('Adaptogen', 'Natural substances (herbs, plants) that help the body adapt to stress and normalise body functions.'),
        ('Amygdala', 'Brain\'s emotional alarm centre; triggers fight-or-flight. Mindfulness training reduces amygdala reactivity.'),
        ('Anhedonia', 'Inability to feel pleasure. Common in overtraining; a sign to rest and recover.'),
        ('Anchoring', 'Using a physical trigger (touch, breath) to access a desired mental state.'),
        ('CAR (Cortisol Awakening Response)', 'Natural cortisol spike in the first 30-45 min of waking. Harness it for intense focus.'),
        ('Cognitive Behavioural Therapy (CBT)', 'Reframing technique: identify thought → challenge it → replace with evidence-based belief.'),
        ('Compounding Effect', 'Small daily improvements accumulating to extraordinary results over months and years.'),
        ('Default Mode Network', 'Brain circuit active during mind-wandering. Meditation reduces DMN hyperactivity (reduces rumination).'),
        ('Dopamine', 'Motivation and reward neurotransmitter. Anticipation of achievement is the primary driver.'),
        ('Fixed vs Growth Mindset', 'Fixed: ability is innate. Growth: ability is built. Growth mindset predicts superior outcomes.'),
        ('Flow State', 'Optimal psychological state of deep immersion in a challenging but achievable task.'),
        ('GRIT', 'Perseverance and passion for long-term goals. Predicts success better than IQ (Duckworth, 2016).'),
        ('Identity-Based Habits', 'Habits driven by who you believe you are, not what you want to achieve.'),
        ('Imposter Syndrome', 'Feeling undeserving of success despite evidence. Counter: build concrete skill, document wins.'),
        ('Intrinsic Motivation', 'Drive from internal satisfaction vs external rewards. Produces longer-lasting consistency.'),
        ('Metacognition', 'Thinking about your thinking. Self-awareness of your mental patterns.'),
        ('Neuroplasticity', 'Brain\'s ability to reorganise itself by forming new neural connections throughout life.'),
        ('Parasympathetic Nervous System', '"Rest and digest" mode. Activated by deep breathing, yoga, nature exposure.'),
        ('Progressive Overload (Mental)', 'Gradually increasing the challenge of your mindset work, like adding weight to a barbell.'),
        ('Psychological Safety', 'Environment where you can attempt, fail, and try again without shame or judgement.'),
        ('Resilience', 'Capacity to recover quickly from difficulties; not absence of difficulty but speed of recovery.'),
        ('Self-Efficacy', 'Belief in your ability to succeed in a specific situation. The strongest predictor of performance.'),
        ('Serotonin', 'Wellbeing neurotransmitter. Boosted by sunlight, exercise, social connection, and tryptophan foods.'),
        ('Stoicism', 'Ancient philosophy focusing on what is in your control; letting go of what isn\'t.'),
        ('Sympathetic Nervous System', '"Fight or flight" mode. Activated by stress, threat, or intense exercise.'),
        ('Visualisation', 'Mental rehearsal of a future action or outcome. Activates same neural pathways as physical practice.'),
        ('Willpower Fatigue', 'Decision fatigue depleting self-control capacity. Automate decisions to preserve willpower for key moments.'),
    ]

    for term, definition in glossary:
        row_data = [[Paragraph(f'<b>{term}</b>', s['H3']),
                     Paragraph(definition, s['Body'])]]
        gt = Table(row_data, colWidths=[52*mm, 103*mm])
        gt.setStyle(TS([
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#aaccee')),
            ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
            ('BACKGROUND', (0,0), (0,-1), LIGHT_BLUE),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story += [gt, Spacer(1, 1.5*mm)]

    story += [sp()]

    # ── Appendix H: Recommended Reading & Resources ───────────────────────────
    story += [PageBreak(), h1('Appendix H: Recommended Reading & Resources'),
              p('This curated reading list extends the concepts in this guide. Each resource has been selected for its direct relevance to the Indian fitness mindset journey.'), sp()]

    books = [
        ['<b>Book</b>', '<b>Author</b>', '<b>Key Lesson</b>', '<b>Best For</b>'],
        ['Atomic Habits', 'James Clear', '1% improvements compound; systems beat goals', 'Habit formation'],
        ['Mindset: The New Psychology of Success', 'Carol Dweck', 'Growth vs fixed mindset determines outcome', 'Self-belief'],
        ['The Power of Now', 'Eckhart Tolle', 'Present-moment awareness eliminates anxiety', 'Stress management'],
        ['Grit', 'Angela Duckworth', 'Passion + perseverance beats talent alone', 'Long-term consistency'],
        ['Can\'t Hurt Me', 'David Goggins', 'The 40% rule: you have far more in reserve', 'Mental toughness'],
        ['The Champion\'s Mind', 'Jim Afremow', 'Sport psychology tools for peak performance', 'Competition mindset'],
        ['Deep Work', 'Cal Newport', 'Focused work is increasingly rare and valuable', 'Discipline and focus'],
        ['The Body Keeps the Score', 'Bessel van der Kolk', 'Trauma\'s physical impact; movement as healing', 'Emotional resilience'],
        ['Why We Sleep', 'Matthew Walker', 'Sleep is the foundation of all performance', 'Sleep optimisation'],
        ['Ikigai', 'Héctor García', 'Japanese concept of life purpose driving longevity', 'Purpose and identity'],
    ]
    bt = Table([[Paragraph(c, s['TH'] if r==0 else s['TC']) for c in row]
                for r, row in enumerate(books)],
               colWidths=[45*mm, 35*mm, 53*mm, 22*mm])
    bt.setStyle(TS([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story += [h2('Essential Books'), bt, sp()]

    story += [h2('Indian Podcasts & YouTube Channels'),
              bl('Fit Tuber (YouTube) — evidence-based Indian nutrition and lifestyle science'),
              bl('Ranveer Allahbadia / BeerBiceps — mindset, entrepreneurship, and Indian wellness culture'),
              bl('Mind Body Soul (YouTube) — Yoga, pranayama, and Ayurveda for modern Indians'),
              bl('Raghav Pande Fitness — practical gym training for Indian beginners'),
              bl('Health and Fitness Hindi — nutrition myths debunked for Indian audience'),
              sp()]

    story += [h2('Apps Recommended for Indian Athletes'),
              bl('HealthifyMe — Indian food database, calorie and macro tracking in Hindi and English'),
              bl('MyFitnessPal — global database with extensive barcode scanning'),
              bl('Headspace / Calm — guided meditation in 5–30 minute sessions'),
              bl('Nike Training Club — free workout programmes for all levels'),
              bl('Wakeout — micro-workouts for busy schedules'),
              bl('Sleep Cycle — smart alarm and sleep quality tracker'),
              sp()]

    # ── Final Motivational Page ────────────────────────────────────────────────
    story += [PageBreak()]
    story += [Table([[Paragraph('YOUR CHAMPION\'S MANIFESTO', ParagraphStyle(
        'BigTitle', fontName='Helvetica-Bold', fontSize=26, textColor=colors.white,
        alignment=1, leading=32))]],
        colWidths=[155*mm],
        style=TS([('BACKGROUND', (0,0), (-1,-1), BLUE),
                  ('PADDING', (0,0), (-1,-1), 18),
                  ('ALIGN', (0,0), (-1,-1), 'CENTER')])),
    sp(6)]

    manifesto_lines = [
        'I train not because I hate my body, but because I love it.',
        'I eat for performance, not just pleasure.',
        'I sleep as a serious training strategy, not a passive activity.',
        'I manage stress as deliberately as I manage my workout programme.',
        'I am consistent on the days motivation is absent.',
        'I do not compare my chapter one to someone else\'s chapter twenty.',
        'I fail forward — every setback carries a lesson.',
        'I invest in my mind as heavily as I invest in my muscles.',
        'I am the product of my daily decisions, not my occasional efforts.',
        'I will still be training, improving, and growing five years from today.',
        '',
        'I am not becoming a champion.',
        'I AM a champion — and I act like it every single day.',
    ]

    for line in manifesto_lines:
        if not line:
            story.append(sp(3))
        else:
            style = ParagraphStyle('MLine', fontName='Helvetica-Bold' if 'I AM' in line else 'Helvetica',
                fontSize=12 if 'I AM' in line else 11,
                textColor=DARK if 'I AM' in line else colors.HexColor('#333333'),
                leading=18, spaceAfter=4, alignment=1)
            story.append(Paragraph(line, style))

    story += [sp(6), hr(),
              Paragraph('Royal Fitness Club — Fitness Mindset Guidance', ParagraphStyle(
                  'Footer', fontName='Helvetica', fontSize=9, textColor=BLUE,
                  alignment=1, leading=12)),
              Paragraph('Your journey. Your transformation. Your legacy.', ParagraphStyle(
                  'Footer2', fontName='Helvetica-Oblique', fontSize=10,
                  textColor=colors.HexColor('#666666'), alignment=1, leading=14))]

    doc.build(story)
    ext_path = '/tmp/mindset_part3.pdf'
    with open(ext_path, 'wb') as f:
        f.write(buf.getvalue())
    return ext_path

def merge():
    base = '/home/user/royal-fitness-club/generated_pdfs/00_Fitness_Mindset_Guidance.pdf'
    ext  = build_part3()
    writer = PdfWriter()
    for src in [base, ext]:
        r = PdfReader(src)
        for pg in r.pages:
            writer.add_page(pg)
    with open(base, 'wb') as f:
        writer.write(f)
    total = len(PdfReader(base).pages)
    print(f'✅ Final Fitness Mindset Guidance: {total} pages')

merge()
