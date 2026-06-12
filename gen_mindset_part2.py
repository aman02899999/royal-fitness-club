#!/usr/bin/env python3
"""Part 2 extension for Fitness Mindset Guidance PDF - adds ~15 more pages."""
import os, io
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from PyPDF2 import PdfWriter, PdfReader

W, H = A4
BLUE = colors.HexColor('#0066cc')
GOLD = colors.HexColor('#cc8800')
DARK = colors.HexColor('#1a1a2e')
LIGHT_BLUE = colors.HexColor('#e8f0fe')

def build_part2():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm)

    s = getSampleStyleSheet()
    def add_style(name, **kw):
        if name not in s:
            s.add(ParagraphStyle(name=name, **kw))
        else:
            for k, v in kw.items():
                setattr(s[name], k, v)

    add_style('H1', fontName='Helvetica-Bold', fontSize=22, textColor=BLUE,
              spaceAfter=8, spaceBefore=14, leading=26)
    add_style('H2', fontName='Helvetica-Bold', fontSize=15, textColor=DARK,
              spaceAfter=6, spaceBefore=10, leading=18)
    add_style('H3', fontName='Helvetica-Bold', fontSize=12, textColor=BLUE,
              spaceAfter=4, spaceBefore=8, leading=15)
    add_style('Body', fontName='Helvetica', fontSize=10, spaceAfter=5,
              leading=14, textColor=colors.HexColor('#333333'))
    add_style('BulletP', fontName='Helvetica', fontSize=10, spaceAfter=3,
              leading=13, leftIndent=14, bulletIndent=4,
              textColor=colors.HexColor('#333333'))
    add_style('Quote', fontName='Helvetica-Oblique', fontSize=11,
              textColor=BLUE, leftIndent=20, rightIndent=20,
              spaceAfter=6, spaceBefore=6, leading=15)
    add_style('TableH', fontName='Helvetica-Bold', fontSize=9,
              textColor=colors.white, leading=12)
    add_style('TableC', fontName='Helvetica', fontSize=9,
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

    def info_box(title, items, bg=LIGHT_BLUE):
        rows = [[Paragraph(f'<b>{title}</b>', s['H3'])]]
        for item in items:
            rows.append([Paragraph(f'• {item}', s['TableC'])])
        t = Table(rows, colWidths=[155*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), BLUE),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('BACKGROUND', (0,1), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 1, BLUE),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    story = []

    # ── Chapter 13: The Warrior Morning Protocol ──────────────────────────────
    story += [PageBreak(), h1('Chapter 13: The Warrior Morning Protocol'),
              p('How you start your morning determines how your entire day unfolds. Champions treat their mornings like the opening ceremony of a performance — every minute is choreographed with intention. In Indian culture, the concept of <b>Brahma Muhurta</b> (the creator\'s hour, approximately 4:30–6:00 AM) has guided disciplined practitioners for centuries.'), sp()]

    story += [h2('13.1 The Science of Morning Routines'), hr(),
              p('Research published in the <i>Journal of Applied Psychology</i> shows that people who engage in structured morning routines report 41% higher feelings of control, 37% better mood, and 29% greater productivity throughout the day. Morning cortisol peaks naturally between 6:00–8:00 AM — this is when your brain is primed for difficult tasks, decision-making, and intense physical activity.'), sp()]

    story += [h3('The Cortisol Awakening Response (CAR)'),
              p('Within the first 30–45 minutes of waking, cortisol rises 50–160% above baseline. This is your body\'s natural energising mechanism. Champions harness this response instead of wasting it on social media scrolling or anxiety-inducing news.'), sp()]

    morning_table = [
        [Paragraph('<b>Time</b>', s['TableH']),
         Paragraph('<b>Activity</b>', s['TableH']),
         Paragraph('<b>Duration</b>', s['TableH']),
         Paragraph('<b>Purpose</b>', s['TableH'])],
        [p('4:45 AM'), p('Wake without snoozing'), p('0 min'), p('Builds discipline')],
        [p('4:45–5:00'), p('Cold water face wash + 500 ml water'), p('15 min'), p('Activates nervous system')],
        [p('5:00–5:15'), p('Pranayama (Anulom Vilom)'), p('15 min'), p('Calms mind, oxygenates')],
        [p('5:15–5:45'), p('Workout / yoga / walk'), p('30 min'), p('Raises energy, mood')],
        [p('5:45–6:00'), p('Cold shower'), p('15 min'), p('Dopamine +250%')],
        [p('6:00–6:20'), p('High-protein breakfast'), p('20 min'), p('Fuels brain')],
        [p('6:20–6:30'), p('Journalling (3 intentions)'), p('10 min'), p('Sets direction')],
    ]
    t = Table(morning_table, colWidths=[30*mm, 55*mm, 28*mm, 42*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
    ]))
    story += [h3('The 90-Minute Elite Morning Blueprint'), t, sp()]

    story += [qt('Win the morning, win the day. Win enough days, win your life. — Robin Sharma'), sp()]

    story += [h2('13.2 The Discipline Equation'),
              p('Discipline is not about punishment — it is about creating systems that make the right action the <i>easiest</i> action. The discipline equation:'), sp(),
              p('<b>Discipline = Environment Design + Habit Stacking + Identity Alignment</b>'), sp()]

    story += [info_box('Environment Design Checklist', [
        'Place gym shoes beside your bed the night before',
        'Pre-pack your workout bag each Sunday for the week',
        'Remove junk food from the house entirely',
        'Keep your journal and pen on your pillow',
        'Set your phone to grayscale to reduce screen appeal',
        'Place a motivational quote on your bathroom mirror',
        'Lay out your workout clothes the night before',
    ]), sp()]

    story += [h2('13.3 Dealing with Zero-Motivation Days'),
              p('Every champion has days when they want to quit. The difference is not that champions feel more motivated — they have built systems that work <i>despite</i> motivation being absent.'), sp()]

    motivation_strategies = [
        ['<b>Strategy</b>', '<b>How It Works</b>', '<b>When to Use</b>'],
        ['The 5-Second Rule', 'Count 5-4-3-2-1 and physically move before brain protests', 'Every morning when snooze feels tempting'],
        ['Minimum Viable Workout', 'Commit to just 10 minutes; brain usually continues', 'When energy is very low'],
        ['Identity Statement', 'Say "I am a person who trains" not "I will try"', 'When identity feels weak'],
        ['Progress Photo Review', 'Look at before photos to remind yourself of the journey', 'When results feel invisible'],
        ['Accountability Text', 'Text your training partner immediately upon waking', 'When social pressure is needed'],
        ['Future Self Visualisation', 'Spend 2 min imagining your body in 6 months', 'When long-term vision is fading'],
    ]
    ms = Table([[Paragraph(c, s['TableH'] if r==0 else s['TableC'])
                 for c in row] for r, row in enumerate(motivation_strategies)],
               colWidths=[40*mm, 70*mm, 45*mm])
    ms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story += [ms, sp()]

    # ── Chapter 14: Nutrition Psychology ──────────────────────────────────────
    story += [PageBreak(), h1('Chapter 14: Advanced Nutrition Psychology'),
              p('We addressed nutrition psychology in Chapter 4, but this chapter goes deeper into the psychological mechanisms that drive eating behaviour — and how to hack them in your favour. Understanding the <b>food-brain loop</b> is the ultimate weapon against cravings, emotional eating, and dietary inconsistency.'), sp()]

    story += [h2('14.1 The Dopamine-Food Cycle'),
              p('Highly palatable foods (high sugar, fat, salt combinations) trigger dopamine release that rivals addictive substances in some studies. The anticipation of eating actually produces MORE dopamine than the eating itself — which explains why cravings are often worse than the actual satisfaction.'), sp()]

    story += [h3('Breaking the Reward Cycle'),
              bl('Delay, don\'t deny: When a craving hits, wait 20 minutes before deciding'),
              bl('Substitute the ritual, not just the food: If you eat while watching TV, change the environment'),
              bl('Decrease palatability gradually: Slowly reduce sugar in tea over 2 weeks'),
              bl('Time your treats: Schedule them post-workout when insulin sensitivity is highest'),
              bl('Reframe the language: "I choose not to eat this" vs "I can\'t eat this"'),
              sp()]

    story += [h2('14.2 The Indian Festive Challenge'),
              p('Indian culture revolves around food-centric celebrations. Festivals like Diwali, Holi, Eid, and family gatherings create powerful social eating pressure. Research shows Indians consume 40–60% excess calories during festive seasons. The key is not avoidance — it is the <b>Festive Navigation Framework</b>.'), sp()]

    festive_data = [
        [Paragraph('<b>Situation</b>', s['TableH']),
         Paragraph('<b>Mindset Trap</b>', s['TableH']),
         Paragraph('<b>Champion Response</b>', s['TableH'])],
        [p('Diwali sweets offered by relatives'), p('"It\'s rude to refuse" guilt'), p('Take one piece, eat slowly, express genuine appreciation')],
        [p('Wedding buffet'), p('"I\'ll restart Monday" all-or-nothing'), p('Fill 50% plate with sabzi/dal, 30% protein, 20% rice/roti')],
        [p('Office cake celebration'), p('"One piece won\'t matter"'), p('Have a small slice, no seconds, don\'t compensate by skipping meals')],
        [p('Mother insisting extra food'), p('People-pleasing override'), p('"Your food is delicious Maa, I am full and want to savour it"')],
        [p('Late-night family snacking'), p('Boredom + social conformity'), p('Engage with family without eating; drink nimbu paani or herbal tea')],
    ]
    ft = Table([[row[i] for i in range(3)] for row in festive_data],
               colWidths=[45*mm, 50*mm, 60*mm])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story += [ft, sp()]

    story += [h2('14.3 Emotional Eating Triggers — The Indian Context'),
              p('Indian culture has unique stressors that trigger emotional eating: family pressure regarding career, marriage, or body image; exam stress during board season; financial stress in joint families; and seasonal affective patterns during monsoon. Mapping your personal triggers is the first step.'), sp()]

    story += [info_box('Personal Trigger Audit — Complete This Exercise', [
        'List the last 5 times you ate when not physically hungry',
        'Identify the emotion preceding each eating episode',
        'Note the time of day and location for each episode',
        'Identify a non-food alternative for each trigger',
        'Practice the alternative response for 21 consecutive days',
    ]), sp()]

    # ── Chapter 15: Sleep Architecture for Athletes ───────────────────────────
    story += [PageBreak(), h1('Chapter 15: Sleep Architecture for Peak Performance'),
              p('We covered sleep basics in Chapter 5. This chapter explores sleep architecture in depth — the specific sleep stages that drive muscle recovery, fat loss, hormonal balance, and mental performance. This knowledge transforms sleep from a passive rest period into an active performance tool.'), sp()]

    story += [h2('15.1 The Five Sleep Stages'),
              p('A complete sleep cycle lasts approximately 90 minutes. You ideally complete 4–6 cycles per night. Each stage serves distinct physiological functions that directly impact your fitness results.'), sp()]

    sleep_stages = [
        ['<b>Stage</b>', '<b>Type</b>', '<b>Duration</b>', '<b>Fitness Benefit</b>', '<b>Disrupted By</b>'],
        ['Stage 1', 'Light NREM', '5–10 min', 'Transition, minor relaxation', 'Noise, light, stress'],
        ['Stage 2', 'Light NREM', '20 min', 'Heart rate drops, memory consolidation', 'Caffeine, alcohol'],
        ['Stage 3', 'Deep NREM', '20–40 min', 'GH release, tissue repair, immune boost', 'Late alcohol, heat'],
        ['Stage 4', 'Deep NREM', '20–40 min', 'Maximum anabolism, fat burning', 'Stress, cortisol'],
        ['Stage 5', 'REM', '10–60 min', 'Mental recovery, emotional regulation', 'Alcohol, cannabis'],
    ]
    st = Table([[Paragraph(c, s['TableH'] if r==0 else s['TableC'])
                 for c in row] for r, row in enumerate(sleep_stages)],
               colWidths=[20*mm, 24*mm, 24*mm, 52*mm, 35*mm])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story += [st, sp()]

    story += [h2('15.2 Sleep Debt and Recovery'),
              p('One night of 5-hour sleep reduces testosterone by 10–15%, increases ghrelin (hunger hormone) by 28%, and impairs reaction time equivalent to 0.08% blood alcohol. Chronic sleep debt is one of the most underrated obstacles to body transformation.'), sp(),
              p('Sleep debt cannot be fully repaid with one long sleep. The body can recover approximately 30–40% of acute sleep loss with a recovery night, but chronic debt (weeks of short sleep) requires consistent 7–9 hour nights over multiple weeks.'), sp()]

    story += [h3('Indian-Specific Sleep Challenges'),
              bl('Loud joint families: Use ear plugs or white noise apps (e.g., Calm, Rain Rain)'),
              bl('Hot summers: Cool room to 18–21°C, use cotton bedding, fan/AC set on timer'),
              bl('Late dinner culture (9–11 PM): Aim to eat by 8 PM; if later, keep it light'),
              bl('Exam/work culture: "I\'ll sleep after results" is a performance myth — sleep IS the work'),
              bl('Religious fasting: On fast days, prioritise sleep quality to preserve muscle'),
              sp()]

    story += [h2('15.3 Sleep Optimisation Protocol'),
              p('The following protocol is designed for Indian athletes and fitness enthusiasts, accounting for local climate, culture, and common obstacles:'), sp()]

    sleep_protocol = [
        [Paragraph('<b>Timing</b>', s['TableH']),
         Paragraph('<b>Action</b>', s['TableH']),
         Paragraph('<b>Science</b>', s['TableH'])],
        [p('3 hrs before bed'), p('Last heavy meal; switch off harsh overhead lights'), p('Melatonin production begins')],
        [p('2 hrs before bed'), p('Stop screens or use Night Mode (iOS/Android)'), p('Blue light suppresses melatonin by 50%')],
        [p('1 hr before bed'), p('Warm milk with ashwagandha or chamomile tea'), p('Tryptophan → serotonin → melatonin')],
        [p('30 min before bed'), p('5 min Yoga Nidra or body scan meditation'), p('Reduces cortisol 23%')],
        [p('Bedtime'), p('Room temp 18–21°C, complete darkness, phone outside room'), p('Core temp drop signals sleep')],
        [p('Morning'), p('Expose eyes to natural light within 10 min of waking'), p('Anchors circadian rhythm')],
    ]
    spt = Table([[row[i] for i in range(3)] for row in sleep_protocol],
                colWidths=[32*mm, 68*mm, 55*mm])
    spt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story += [spt, sp()]

    # ── Chapter 16: Building Unstoppable Confidence ───────────────────────────
    story += [PageBreak(), h1('Chapter 16: Building Unstoppable Confidence'),
              p('Confidence is not a personality trait — it is a <b>skill built through evidence</b>. Every time you do what you said you would do, you deposit trust into your self-confidence account. Every broken promise to yourself withdraws it. This chapter provides the blueprint for systematically building unshakeable confidence through the fitness journey.'), sp()]

    story += [h2('16.1 The Confidence-Competence Loop'),
              p('Confidence follows competence, not the other way around. Most people wait until they feel confident before they act — champions act first, build competence through repetition, and let confidence emerge as a natural byproduct. The loop works like this:'), sp()]

    story += [p('<b>Action → Competence → Evidence → Belief → Confidence → Bigger Action</b>'), sp()]

    story += [h3('Micro-Win Architecture'),
              p('Build the loop by engineering daily micro-wins — small, deliberate victories that accumulate evidence of your capability:'), sp(),
              bl('Complete the first exercise of your workout (you always complete the rest)'),
              bl('Drink 3 litres of water today (track it hour by hour)'),
              bl('Eat breakfast without checking your phone'),
              bl('Walk 1,000 steps after lunch'),
              bl('Sleep by 10:30 PM tonight'),
              bl('Do 10 push-ups before showering'),
              sp()]

    story += [h2('16.2 Body Image and Indian Society'),
              p('Indian society carries specific body image pressures: aunties commenting on weight at family gatherings, matrimonial site profiles judging appearance, Bollywood standards creating unrealistic benchmarks, and colourism creating additional layers of insecurity. Navigating these requires both mindset work and communication skills.'), sp()]

    story += [info_box('Responding to Unsolicited Body Comments', [
        '"Aap bahut patla/mota ho gaye" → "Thank you for noticing, I am working on my health"',
        '"Tum gym kyun jate ho, already fit ho" → "I train for strength and energy, not just appearance"',
        '"Itna protein kyu khate ho?" → "It helps me recover from training and stay full longer"',
        '"Ye log ki sawaal mat suno" → Internal: These comments are about them, not about you',
        'Neutral deflection: Smile, change subject, do not justify or explain your health choices',
    ]), sp()]

    story += [h2('16.3 The Champion\'s Self-Talk System'),
              p('Research by Dr. Ethan Kross at Michigan shows that referring to yourself in third person (distanced self-talk) significantly improves performance under pressure. "Rahul, you can do this" outperforms "I can do this" in high-stakes moments.'), sp()]

    selftalk = [
        ['<b>Situation</b>', '<b>Negative Self-Talk</b>', '<b>Champion Reframe</b>'],
        ['Missing a workout', '"I have no willpower"', '"I missed today. [Name], what needs to change tomorrow?"'],
        ['Plateau for 3 weeks', '"My body doesn\'t respond"', '"[Name], plateaus mean it\'s time to level up the stimulus"'],
        ['Others progressing faster', '"I\'m the slowest"', '"[Name], your journey has a different timeline. Stay in your lane"'],
        ['Ate off-plan', '"I ruined everything"', '"One meal doesn\'t define a journey. [Name], next meal is perfect"'],
        ['Public gym intimidation', '"Everyone is judging me"', '"[Name], they\'re focused on their own training. You belong here"'],
    ]
    stT = Table([[Paragraph(c, s['TableH'] if r==0 else s['TableC'])
                  for c in row] for r, row in enumerate(selftalk)],
                colWidths=[38*mm, 50*mm, 67*mm])
    stT.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story += [stT, sp()]

    # ── Chapter 17: The Long Game — Staying Consistent for Years ──────────────
    story += [PageBreak(), h1('Chapter 17: The Long Game — Years of Consistency'),
              p('The fitness industry is obsessed with 12-week transformations. Real champions think in years and decades. The compounding effect of consistent effort over time produces results that no short program can match. This final chapter addresses the psychological strategies for maintaining your commitment beyond the initial excitement.'), sp()]

    story += [h2('17.1 The Compounding Effect of Daily Habits'),
              p('James Clear\'s research in "Atomic Habits" shows that a 1% daily improvement compounds to 37× improvement over a year. Conversely, 1% daily decline compounds to near zero. The gap between consistent and inconsistent trainees grows exponentially over time — not linearly.'), sp()]

    compound_table = [
        ['<b>Year</b>', '<b>Consistent (5 sessions/week)</b>', '<b>Inconsistent (2 sessions/week)</b>', '<b>Gap</b>'],
        ['Year 1', '250 sessions, solid foundation', '104 sessions, basic fitness', '146 sessions'],
        ['Year 2', '500+ sessions, notable physique', '200 sessions, marginal progress', '300 sessions'],
        ['Year 3', '750+ sessions, advanced physique', '300 sessions, same as year 1', '450 sessions'],
        ['Year 5', '1,250 sessions, elite body', '500 sessions, moderate fitness', '750 sessions'],
        ['Year 10', '2,500+ sessions, transformed life', '1,000 sessions, average body', '1,500 sessions'],
    ]
    ct = Table([[Paragraph(c, s['TableH'] if r==0 else s['TableC'])
                 for c in row] for r, row in enumerate(compound_table)],
               colWidths=[22*mm, 45*mm, 45*mm, 43*mm])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story += [ct, sp()]

    story += [h2('17.2 Identity Evolution Over Time'),
              p('As your body changes, your identity must evolve to match. Many people lose their results because their identity never caught up with their body. They still see themselves as "someone who struggles with fitness" even after achieving significant results — and behaviour follows identity back to the old norm.'), sp()]

    story += [info_box('Annual Identity Audit — Ask Yourself These Questions', [
        'Does my self-description still include "I am trying to get fit"? (Change to "I am fit")',
        'Do I still frame fitness as sacrifice? (Reframe as privilege)',
        'Do I still apologise for training or eating healthy in social settings?',
        'Have I updated my circle to include people who share my values?',
        'Am I helping others with their fitness journey? (Teaching cements identity)',
        'Does my environment (home, phone, clothes) reflect my new identity?',
    ]), sp()]

    story += [h2('17.3 Managing Life Disruptions'),
              p('Life will disrupt your routine. Travel, illness, exams, relationships, career changes, family responsibilities — all will test your consistency. The question is not whether disruptions will happen, but whether you have a system for returning from them.'), sp()]

    disruptions = [
        ['<b>Disruption</b>', '<b>Minimum Viable Habit</b>', '<b>Return Protocol</b>'],
        ['Travel / vacation', '20-min hotel room bodyweight workout', 'Resume full training on day of return'],
        ['Illness (mild)', 'Walk, stretch, sleep extra', 'Return to 50% intensity first session back'],
        ['Exam season', 'Morning walk + home workouts', 'Schedule gym sessions like study sessions'],
        ['New job / relocation', 'Find new gym within 1 week', 'Make gym registration first priority'],
        ['Relationship stress', '20-min run (best stress relief)', 'Use training as the anchor, not the victim'],
        ['Injury', 'Train around the injury', 'Specialised rehab programme immediately'],
        ['Monsoon / extreme heat', 'Home workout kit ready', 'Pre-planned indoor alternatives'],
    ]
    dt = Table([[Paragraph(c, s['TableH'] if r==0 else s['TableC'])
                 for c in row] for r, row in enumerate(disruptions)],
               colWidths=[42*mm, 55*mm, 58*mm])
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story += [dt, sp()]

    story += [h2('17.4 Your Fitness Legacy'),
              p('Ultimately, your fitness journey is not just about your body. It is about who you become in the process. The discipline you build in the gym spills over into your career, relationships, finances, and mental health. When you transform your body, you transform your life.'), sp(),
              p('You also carry the power to inspire everyone around you. In a country where lifestyle diseases (diabetes, hypertension, obesity) are reaching epidemic proportions, every person who takes their health seriously becomes a change agent in their family and community.'), sp()]

    story += [qt('The body achieves what the mind believes. But more than that — the body becomes what the mind decides to be, consistently, over time. Start now. Your future self is waiting.'), sp()]

    story += [info_box('Your Fitness Legacy Pledge', [
        'I commit to training consistently for at least 3 years before judging my potential',
        'I will celebrate process milestones, not just outcome milestones',
        'I will share my knowledge and inspire at least one person in my circle',
        'I will treat my body as an asset, not an obstacle',
        'I will return from every setback stronger than I left',
        'I am a champion — not because I never fall, but because I always rise',
    ], bg=colors.HexColor('#e8f4e8')), sp()]

    story += [PageBreak(), h1('Appendix C: Yoga & Pranayama Sequence for Fitness Recovery'),
              p('The following sequence is designed for active recovery days and pre-sleep wind-down. Each pose combines physical restoration with mental recalibration — bridging ancient Indian wellness science with modern sports recovery research.'), sp()]

    yoga_seq = [
        ['<b>#</b>', '<b>Asana / Pranayama</b>', '<b>Duration</b>', '<b>Benefit</b>', '<b>How To</b>'],
        ['1', 'Balasana (Child\'s Pose)', '2 min', 'Decompresses spine, calms anxiety', 'Kneel, sit on heels, stretch arms forward, forehead to mat'],
        ['2', 'Anulom Vilom', '5 min', 'Balances nervous system, lowers cortisol', 'Alternate nostril breathing, 4-sec inhale, 4-sec exhale'],
        ['3', 'Supta Matsyendrasana', '90 sec/side', 'Spinal rotation, hip flexor release', 'Lie flat, draw knee across body, extend arm out'],
        ['4', 'Viparita Karani', '5 min', 'Reduces leg swelling, activates rest-digest', 'Legs up wall, arms relaxed by sides'],
        ['5', 'Bhramari (Humming Bee)', '3 min', 'Reduces blood pressure, induces calm', 'Plug ears, hum on exhale, feel skull vibration'],
        ['6', 'Nadi Shodhana', '5 min', 'Pre-sleep parasympathetic activation', '4-7-8 ratio: inhale 4 sec, hold 7, exhale 8'],
        ['7', 'Savasana (Corpse Pose)', '10 min', 'Full system reset, GH release preparation', 'Flat on back, arms at 45°, eyes closed, zero effort'],
    ]
    yt = Table([[Paragraph(c, s['TableH'] if r==0 else s['TableC'])
                 for c in row] for r, row in enumerate(yoga_seq)],
               colWidths=[8*mm, 38*mm, 22*mm, 40*mm, 47*mm])
    yt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story += [yt, sp()]

    story += [h2('Indian Herbs for Recovery and Stress'),
              p('Ayurvedic adaptogens have been validated by modern research for their role in cortisol modulation, testosterone support, and recovery acceleration:'), sp()]

    herbs = [
        ['<b>Herb</b>', '<b>Active Compound</b>', '<b>Benefit</b>', '<b>Dose / Form</b>'],
        ['Ashwagandha', 'Withanolides', 'Lowers cortisol 27%, boosts T by 17%', '300–600 mg root extract daily'],
        ['Brahmi (Bacopa)', 'Bacosides', 'Memory, focus, anxiety reduction', '300 mg standardised extract'],
        ['Shatavari', 'Saponins', 'Hormonal balance, recovery in women', '500 mg daily with milk'],
        ['Shilajit', 'Fulvic acid', 'ATP production, testosterone support', '300 mg resin daily'],
        ['Triphala', 'Tannins, polyphenols', 'Gut health, antioxidant, anti-inflammatory', '1 tsp powder in warm water at night'],
        ['Tulsi (Holy Basil)', 'Eugenol', 'Adaptogen, reduces cortisol', '500 mg extract or fresh leaves in tea'],
    ]
    ht = Table([[Paragraph(c, s['TableH'] if r==0 else s['TableC'])
                 for c in row] for r, row in enumerate(herbs)],
               colWidths=[30*mm, 35*mm, 55*mm, 35*mm])
    ht.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ccddff')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story += [ht, sp()]

    doc.build(story)
    ext_path = '/tmp/mindset_part2.pdf'
    with open(ext_path, 'wb') as f:
        f.write(buf.getvalue())
    return ext_path

def merge():
    base = '/home/user/royal-fitness-club/generated_pdfs/00_Fitness_Mindset_Guidance.pdf'
    ext  = build_part2()
    out  = '/home/user/royal-fitness-club/generated_pdfs/00_Fitness_Mindset_Guidance.pdf'
    writer = PdfWriter()
    for src in [base, ext]:
        r = PdfReader(src)
        for pg in r.pages:
            writer.add_page(pg)
    with open(out, 'wb') as f:
        writer.write(f)
    total = len(PdfReader(out).pages)
    print(f'✅ Merged Fitness Mindset Guidance: {total} pages')

merge()
