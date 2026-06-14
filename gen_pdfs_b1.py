#!/usr/bin/env python3
"""Generate PDFs for cs_b1 — Fitness Foundations Certificate (8 modules)"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether
import os

OUT = '/home/user/royal-fitness-club/course_pdfs/beginner'
os.makedirs(OUT, exist_ok=True)

# RFC Brand Colors
RFC_RED   = colors.HexColor('#E8001D')
RFC_DARK  = colors.HexColor('#1A1A2E')
RFC_GOLD  = colors.HexColor('#FFD700')
RFC_BLUE  = colors.HexColor('#0066CC')
RFC_GREEN = colors.HexColor('#138808')
RFC_WHITE = colors.white
RFC_LIGHT = colors.HexColor('#F5F5F5')
RFC_GRAY  = colors.HexColor('#555555')

W, H = A4

def styles():
    s = getSampleStyleSheet()
    base = dict(fontName='Helvetica', leading=16, spaceAfter=6)
    d = {
        'cover_title': ParagraphStyle('ct', fontName='Helvetica-Bold', fontSize=32,
            textColor=RFC_WHITE, alignment=TA_CENTER, leading=40, spaceAfter=8),
        'cover_sub': ParagraphStyle('cs', fontName='Helvetica', fontSize=16,
            textColor=RFC_GOLD, alignment=TA_CENTER, leading=22, spaceAfter=6),
        'cover_mod': ParagraphStyle('cm', fontName='Helvetica-Bold', fontSize=22,
            textColor=RFC_WHITE, alignment=TA_CENTER, leading=28, spaceAfter=10),
        'cover_dur': ParagraphStyle('cd', fontName='Helvetica', fontSize=13,
            textColor=RFC_LIGHT, alignment=TA_CENTER, leading=18),
        'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=22,
            textColor=RFC_DARK, leading=28, spaceBefore=18, spaceAfter=10),
        'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=17,
            textColor=RFC_BLUE, leading=22, spaceBefore=14, spaceAfter=7),
        'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=13,
            textColor=RFC_DARK, leading=18, spaceBefore=10, spaceAfter=5),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=11,
            textColor=RFC_GRAY, leading=17, spaceAfter=7, alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=11,
            textColor=RFC_GRAY, leading=16, spaceAfter=4, leftIndent=18,
            bulletIndent=6),
        'key': ParagraphStyle('key', fontName='Helvetica-Bold', fontSize=11,
            textColor=RFC_DARK, leading=16, spaceAfter=4),
        'box_title': ParagraphStyle('bt', fontName='Helvetica-Bold', fontSize=12,
            textColor=RFC_WHITE, leading=16, spaceAfter=4),
        'box_body': ParagraphStyle('bb', fontName='Helvetica', fontSize=11,
            textColor=RFC_DARK, leading=16, spaceAfter=4),
        'quote': ParagraphStyle('q', fontName='Helvetica-Oblique', fontSize=12,
            textColor=RFC_BLUE, leading=18, leftIndent=24, spaceAfter=8,
            spaceBefore=8),
        'caption': ParagraphStyle('cap', fontName='Helvetica', fontSize=9,
            textColor=RFC_GRAY, leading=13, alignment=TA_CENTER),
    }
    return d

ST = styles()

def cover_page(course_name, mod_num, mod_title, duration, course_code):
    """Return a list of flowables forming the cover page."""
    elems = []
    # Top color bar via a table
    bar_data = [['']]
    bar = Table(bar_data, colWidths=[W - 40*mm], rowHeights=[6])
    bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), RFC_RED),
        ('LINEBELOW', (0,0), (-1,-1), 2, RFC_GOLD),
    ]))
    elems.append(Spacer(1, 8*mm))
    elems.append(bar)
    elems.append(Spacer(1, 18*mm))

    # RFC logo-style header
    logo_data = [['ROYAL FITNESS CLUB']]
    logo_tbl = Table(logo_data, colWidths=[W - 40*mm])
    logo_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), RFC_DARK),
        ('TEXTCOLOR', (0,0), (-1,-1), RFC_WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 28),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
    ]))
    elems.append(logo_tbl)
    elems.append(Spacer(1, 6*mm))

    # Gold divider
    elems.append(HRFlowable(width='100%', thickness=3, color=RFC_GOLD))
    elems.append(Spacer(1, 10*mm))

    # Course label
    course_data = [[course_name]]
    course_tbl = Table(course_data, colWidths=[W - 40*mm])
    course_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), RFC_BLUE),
        ('TEXTCOLOR', (0,0), (-1,-1), RFC_WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 15),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elems.append(course_tbl)
    elems.append(Spacer(1, 14*mm))

    # Module number badge
    badge_data = [[f'MODULE {mod_num}']]
    badge = Table(badge_data, colWidths=[50*mm])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), RFC_RED),
        ('TEXTCOLOR', (0,0), (-1,-1), RFC_WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 13),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    elems.append(badge)
    elems.append(Spacer(1, 8*mm))

    # Module title
    elems.append(Paragraph(mod_title, ST['h1']))
    elems.append(Spacer(1, 6*mm))

    # Duration / meta table
    meta_data = [
        ['Duration', f'{duration} minutes'],
        ['Course Code', course_code],
        ['Level', 'Beginner'],
        ['Format', 'Study Guide + Reference PDF'],
    ]
    meta_tbl = Table(meta_data, colWidths=[45*mm, W - 40*mm - 45*mm - 2*mm])
    meta_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), RFC_DARK),
        ('BACKGROUND', (1,0), (1,-1), RFC_LIGHT),
        ('TEXTCOLOR', (0,0), (0,-1), RFC_WHITE),
        ('TEXTCOLOR', (1,0), (1,-1), RFC_DARK),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (0,-1), 8),
        ('RIGHTPADDING', (0,0), (0,-1), 8),
        ('LEFTPADDING', (1,0), (1,-1), 10),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.white),
        ('LINEBELOW', (0,-1), (-1,-1), 0, colors.white),
    ]))
    elems.append(meta_tbl)
    elems.append(Spacer(1, 14*mm))

    # Indian flag tricolor accent strip
    flag_data = [['', '', '']]
    flag = Table(flag_data, colWidths=[(W-40*mm)/3]*3, rowHeights=[8])
    flag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#FF9933')),
        ('BACKGROUND', (1,0), (1,0), RFC_WHITE),
        ('BACKGROUND', (2,0), (2,0), RFC_GREEN),
    ]))
    elems.append(flag)
    elems.append(Spacer(1, 8*mm))

    # Footer note
    elems.append(Paragraph(
        'This document is part of the Royal Fitness Club Professional Certification Program. '
        'All content is curated by certified fitness professionals and sport scientists.',
        ST['caption']))
    elems.append(PageBreak())
    return elems

def info_box(title, items, bg=RFC_DARK, fg=RFC_WHITE):
    """Colored info/key-takeaway box."""
    rows = [[Paragraph(title, ParagraphStyle('bt2', fontName='Helvetica-Bold',
                       fontSize=12, textColor=fg, leading=16))]]
    for item in items:
        rows.append([Paragraph(f'• {item}', ParagraphStyle('bb2', fontName='Helvetica',
                               fontSize=11, textColor=RFC_DARK, leading=15, spaceAfter=3))])
    tbl = Table(rows, colWidths=[W - 40*mm])
    style = [
        ('BACKGROUND', (0,0), (-1,0), bg),
        ('BACKGROUND', (0,1), (-1,-1), RFC_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('BOX', (0,0), (-1,-1), 1.5, bg),
    ]
    tbl.setStyle(TableStyle(style))
    return tbl

def two_col_table(headers, rows):
    data = [headers] + rows
    col_w = (W - 40*mm) / 2
    tbl = Table(data, colWidths=[col_w, col_w])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RFC_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), RFC_WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,1), (-1,-1), RFC_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [RFC_LIGHT, RFC_WHITE]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('BOX', (0,0), (-1,-1), 1, RFC_DARK),
    ]))
    return tbl

def multi_col_table(headers, rows):
    n = len(headers)
    col_w = (W - 40*mm) / n
    data = [headers] + rows
    tbl = Table(data, colWidths=[col_w]*n)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RFC_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), RFC_WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [RFC_LIGHT, RFC_WHITE]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('BOX', (0,0), (-1,-1), 1, RFC_BLUE),
    ]))
    return tbl

def section_divider(text):
    data = [[text]]
    tbl = Table(data, colWidths=[W - 40*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), RFC_RED),
        ('TEXTCOLOR', (0,0), (-1,-1), RFC_WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 13),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    return tbl

# ─────────────────────────────────────────────
# MODULE 1: Anatomy Essentials (45 min)
# ─────────────────────────────────────────────
def gen_b1_m1():
    fname = os.path.join(OUT, 'cs_b1_mod1_anatomy_essentials.pdf')
    doc = SimpleDocTemplate(fname, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm)
    e = []
    e += cover_page('Fitness Foundations Certificate', 1,
                    'How the Body Works — Anatomy Essentials', 45, 'CS_B1')

    # ── SECTION 1 ──
    e.append(section_divider('SECTION 1: Introduction to Human Anatomy'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('Why Anatomy Matters for Fitness', ST['h1']))
    e.append(Paragraph(
        'Before picking up a dumbbell or lacing up your running shoes, understanding the machine '
        'you are training transforms how effectively you exercise. Human anatomy is not just a '
        'medical subject — it is your personal operating manual. Knowing where each muscle is, '
        'how it attaches, and what movement it produces lets you train with precision rather '
        'than guesswork.', ST['body']))
    e.append(Paragraph(
        'In this module we explore the foundational systems of the human body — skeletal, '
        'muscular, and connective tissue — with a practical fitness lens. By the end you will '
        'be able to identify major muscle groups, understand joint mechanics, and appreciate '
        'why proper form protects your body for decades of training.', ST['body']))

    e.append(Paragraph('The Organisation of the Human Body', ST['h2']))
    e.append(Paragraph(
        'The body is organised into levels of complexity: cells → tissues → organs → organ systems → organism. '
        'For fitness professionals, the three most critical organ systems are:', ST['body']))
    for item in [
        'Skeletal System — the rigid framework that provides structure and leverage',
        'Muscular System — the contractile engine that generates movement',
        'Nervous System — the control network that triggers and coordinates muscle contractions',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))
    e.append(Spacer(1, 8))
    e.append(info_box('Key Learning Outcome', [
        'Identify the 206 bones of the human skeleton by region',
        'Distinguish between the axial and appendicular skeleton',
        'Understand how skeletal structure influences exercise selection',
    ], RFC_DARK))
    e.append(Spacer(1, 10))

    # ── SECTION 2 ──
    e.append(section_divider('SECTION 2: The Skeletal System'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('Bones — Far More Than a Scaffold', ST['h1']))
    e.append(Paragraph(
        'The adult human skeleton contains 206 bones. At birth we have roughly 270 — many fuse '
        'during childhood and adolescence, a process completing around age 25. This is why '
        'resistance training programmes for teenagers must be carefully managed: growth plates '
        '(epiphyseal plates) are still cartilaginous and vulnerable to compressive injury.', ST['body']))

    e.append(Paragraph('Axial vs Appendicular Skeleton', ST['h2']))
    e.append(Paragraph(
        'The skeleton is divided into two functional regions:', ST['body']))
    e.append(two_col_table(
        ['AXIAL SKELETON (80 bones)', 'APPENDICULAR SKELETON (126 bones)'],
        [
            ['Skull (22)', 'Shoulder girdle (4)'],
            ['Vertebral column (26)', 'Arms & forearms (6)'],
            ['Rib cage (25)', 'Hands & wrists (54)'],
            ['Hyoid bone (1)', 'Pelvic girdle (2)'],
            ['', 'Legs & feet (60)'],
        ]
    ))
    e.append(Spacer(1, 10))

    e.append(Paragraph('Bone Composition and Density', ST['h2']))
    e.append(Paragraph(
        'Bone is a living tissue composed of an organic matrix (mainly collagen) reinforced '
        'with mineral crystals of hydroxyapatite (calcium phosphate). This composite structure '
        'gives bone its unique property of being both flexible and hard.', ST['body']))
    e.append(Paragraph(
        '<b>Compact bone (cortical):</b> Dense outer shell — 80% of skeletal mass. Provides '
        'mechanical strength and houses the medullary cavity (where red/yellow marrow is found).', ST['body']))
    e.append(Paragraph(
        '<b>Cancellous bone (trabecular):</b> Spongy inner lattice at bone ends. Lighter but still '
        'incredibly strong — oriented along lines of mechanical stress. This architecture is why '
        'bone remodels in response to exercise loads.', ST['body']))
    e.append(Paragraph(
        '<b>Bone remodelling cycle:</b> Osteoclasts resorb old bone; osteoblasts deposit new bone. '
        'Resistance training creates microstress that upregulates osteoblast activity, increasing '
        'bone mineral density (BMD) — a key defence against osteoporosis later in life.', ST['body']))

    e.append(info_box('Fitness Fact — Bone & Exercise', [
        'Weight-bearing exercise increases BMD by 1–3% per year in untrained individuals',
        'Impact sports (basketball, gymnastics) produce highest BMD gains',
        'Swimming, while excellent for cardiovascular health, provides minimal BMD benefit',
        'The "mechanostat" theory: bone adapts to habitual loading thresholds',
    ], RFC_BLUE))
    e.append(Spacer(1, 8))

    e.append(Paragraph('The Vertebral Column — Your Central Tower', ST['h2']))
    e.append(Paragraph(
        'The spine consists of 33 vertebrae grouped into 5 regions, each with distinct '
        'biomechanical properties relevant to exercise programming:', ST['body']))
    e.append(multi_col_table(
        ['Region', 'Vertebrae', 'Normal Curve', 'Primary Movement'],
        [
            ['Cervical', '7 (C1–C7)', 'Lordosis', 'Flexion/Extension/Rotation'],
            ['Thoracic', '12 (T1–T12)', 'Kyphosis', 'Limited — rib attachment'],
            ['Lumbar', '5 (L1–L5)', 'Lordosis', 'Flexion/Extension'],
            ['Sacral', '5 fused', 'Kyphosis', 'None (fused)'],
            ['Coccygeal', '4 fused', '—', 'None (fused)'],
        ]
    ))
    e.append(Spacer(1, 8))
    e.append(Paragraph(
        'The natural S-curve of the spine (two lordoses + two kyphoses) distributes '
        'compressive loads evenly across intervertebral discs. When this neutral alignment is '
        'lost during lifting (e.g., excessive lumbar flexion during deadlifts), shear forces '
        'increase dramatically — a primary cause of disc herniation.', ST['body']))

    e.append(Paragraph('Intervertebral Discs', ST['h2']))
    e.append(Paragraph(
        'Between each pair of vertebrae (except C1–C2) sits an intervertebral disc — a '
        'fibrocartilaginous shock absorber. Each disc has:', ST['body']))
    for item in [
        'Nucleus pulposus — gelatinous core, 70–90% water, absorbs compressive load',
        'Annulus fibrosus — concentric collagen rings providing tensile strength',
        'Cartilaginous endplates — nutrient exchange interface (discs are avascular)',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))
    e.append(Paragraph(
        'Discs lose hydration and height with age and prolonged sitting. Morning workouts '
        'after sleeping involve slightly taller, more hydrated discs — one reason trainers '
        'sometimes recommend lighter spinal loading early in the day.', ST['body']))

    # ── SECTION 3 ──
    e.append(section_divider('SECTION 3: Joints — The Hinges of Movement'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('Classification of Joints', ST['h1']))
    e.append(Paragraph(
        'A joint (articulation) is where two or more bones meet. Joints are classified by '
        'structure and degree of movement:', ST['body']))
    e.append(multi_col_table(
        ['Type', 'Example', 'Movement'],
        [
            ['Fibrous (synarthrosis)', 'Skull sutures', 'None'],
            ['Cartilaginous (amphiarthrosis)', 'Pubic symphysis', 'Slight'],
            ['Synovial (diarthrosis)', 'Knee, shoulder', 'Free'],
        ]
    ))
    e.append(Spacer(1, 8))

    e.append(Paragraph('Synovial Joints — The Workhorse of Exercise', ST['h2']))
    e.append(Paragraph(
        'All major joints involved in gym exercises are synovial. They share common features: '
        'hyaline cartilage on articular surfaces, a joint capsule, synovial membrane producing '
        'synovial fluid, and associated ligaments.', ST['body']))
    e.append(Paragraph(
        '<b>Synovial fluid:</b> A viscous lubricant that reduces friction, distributes load, '
        'and delivers nutrients to articular cartilage. Viscosity decreases with warming up — '
        'explaining why cold joints feel stiff and why warm-up is critical for injury prevention.', ST['body']))

    e.append(Paragraph('Synovial Joint Sub-Types in Fitness', ST['h2']))
    e.append(multi_col_table(
        ['Sub-Type', 'Shape', 'Exercise Example', 'Movements'],
        [
            ['Ball & socket', 'Spherical head + cup', 'Shoulder press', 'All planes + rotation'],
            ['Hinge', 'Convex + concave', 'Bicep curl (elbow)', 'Flexion/Extension'],
            ['Pivot', 'Rounded + ring', 'Forearm rotation', 'Rotation only'],
            ['Condyloid', 'Oval + ellipsoid', 'Wrist (radiocarpal)', 'Flex/Ext + Abd/Add'],
            ['Saddle', 'Reciprocal saddles', 'Thumb CMC', 'Biaxial'],
            ['Plane (gliding)', 'Flat surfaces', 'Foot (intertarsal)', 'Gliding'],
        ]
    ))
    e.append(Spacer(1, 8))

    e.append(Paragraph('Range of Motion (ROM)', ST['h2']))
    e.append(Paragraph(
        'ROM describes the arc of movement possible at a joint. It is constrained by:', ST['body']))
    for item in [
        'Bony architecture (e.g., hip socket depth — acetabular morphology varies 20–30° between individuals)',
        'Ligamentous tension (passive constraint at end-range)',
        'Muscle flexibility and fascial stiffness (active constraint through range)',
        'Joint capsule extensibility',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))
    e.append(Paragraph(
        '<b>Practical implication:</b> Squatting depth is partly determined by hip socket anatomy. '
        'Attempting to force a squat deeper than one\'s bony architecture allows causes posterior '
        'pelvic tilt ("butt wink") — increasing lumbar flexion under load and disc stress. '
        'Programming should respect individual anatomy, not just mirror ideals.', ST['body']))

    # ── SECTION 4 ──
    e.append(section_divider('SECTION 4: The Muscular System'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('Three Types of Muscle Tissue', ST['h1']))
    e.append(multi_col_table(
        ['Type', 'Control', 'Location', 'Characteristics'],
        [
            ['Skeletal', 'Voluntary', 'Attached to bones', 'Striated, fast & slow fibres, fatigable'],
            ['Cardiac', 'Involuntary', 'Heart wall', 'Striated, rhythmic, highly aerobic'],
            ['Smooth', 'Involuntary', 'Visceral organs', 'Non-striated, slow, sustained contraction'],
        ]
    ))
    e.append(Spacer(1, 8))

    e.append(Paragraph('Skeletal Muscle Architecture', ST['h2']))
    e.append(Paragraph(
        'From macro to micro, skeletal muscle is organised in nested sheaths of connective tissue:', ST['body']))
    for item in [
        'Epimysium — outer fascial wrapping of the entire muscle belly',
        'Perimysium — surrounds fascicles (bundles of ~100 muscle fibres)',
        'Endomysium — wraps individual muscle fibres (cells)',
        'Sarcolemma — cell membrane of the muscle fibre',
        'Myofibrils — contractile units running the length of the fibre',
        'Sarcomeres — repeating units of myofibrils containing actin & myosin',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))
    e.append(Paragraph(
        'The sarcomere is the fundamental unit of contraction. Under an electron microscope, '
        'alternating light (I-band, actin) and dark (A-band, myosin) bands create the '
        'characteristic "striped" appearance. During contraction, actin filaments slide past '
        'myosin — the sliding filament theory.', ST['body']))

    e.append(Paragraph('Muscle Fibre Types', ST['h2']))
    e.append(Paragraph(
        'Human skeletal muscle is a mixture of fibre types, genetically determined but '
        'modestly trainable. Understanding fibre types explains individual differences in '
        'athletic performance and guides programme design:', ST['body']))
    e.append(multi_col_table(
        ['Property', 'Type I (Slow)', 'Type IIa (Fast-Ox)', 'Type IIx (Fast-Gly)'],
        [
            ['Colour', 'Red (myoglobin)', 'Red/Pink', 'White'],
            ['Speed', 'Slow', 'Intermediate', 'Fast'],
            ['Fatigue', 'Resistant', 'Intermediate', 'Rapid'],
            ['Power output', 'Low', 'Moderate', 'High'],
            ['Energy system', 'Aerobic (oxidative)', 'Mixed', 'Anaerobic (glycolytic)'],
            ['Mitochondria', 'Many', 'Moderate', 'Few'],
            ['Best for', 'Endurance', 'Middle distance', 'Sprint/Power'],
        ]
    ))
    e.append(Spacer(1, 8))
    e.append(Paragraph(
        '<b>Fibre type distribution:</b> The average untrained person has roughly 50% Type I '
        'and 50% Type II in most limb muscles, though this varies considerably between '
        'individuals and muscles (soleus is ~80% Type I; gastrocnemius ~50%). '
        'Elite marathon runners may be 80–90% Type I; sprinters the reverse.', ST['body']))
    e.append(info_box('Training Tip — Fibre Type Recruitment', [
        'Endurance training (low load, high rep) preferentially recruits Type I fibres',
        'Heavy resistance training (>85% 1RM) recruits all fibre types including Type IIx',
        'Power training (explosive movement) converts some Type IIx to IIa (more sustainable)',
        'You cannot convert Type I to Type II — genetics sets the ceiling, training fills the potential',
    ], RFC_GREEN))
    e.append(Spacer(1, 8))

    # ── SECTION 5 ──
    e.append(section_divider('SECTION 5: Major Muscle Groups for Fitness'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('Upper Body Muscles', ST['h1']))

    e.append(Paragraph('Chest (Pectoralis Major & Minor)', ST['h2']))
    e.append(Paragraph(
        'The pectoralis major is a large fan-shaped muscle with two heads:', ST['body']))
    for item in [
        'Clavicular head (upper chest) — originates from the clavicle; active in incline press',
        'Sternal/costal head (lower chest) — originates from sternum & ribs; primary flat bench muscle',
        'Action: horizontal adduction, flexion, and internal rotation of the humerus',
        'Synergists: anterior deltoid, triceps brachii (in pressing movements)',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))
    e.append(Paragraph(
        'The pectoralis minor lies deep to pectoralis major, attaching from ribs 3–5 to the '
        'coracoid process of the scapula. It protracts and depresses the scapula — important '
        'for shoulder health and often tight in desk workers.', ST['body']))

    e.append(Paragraph('Back (Latissimus Dorsi, Trapezius, Rhomboids)', ST['h2']))
    e.append(multi_col_table(
        ['Muscle', 'Origin', 'Insertion', 'Primary Action', 'Key Exercises'],
        [
            ['Latissimus dorsi', 'Lower 6 thoracic vertebrae, iliac crest', 'Intertubercular groove of humerus', 'Shoulder extension, adduction, internal rotation', 'Pull-up, lat pulldown, row'],
            ['Trapezius (upper)', 'Occipital bone, C1-C7', 'Clavicle, acromion', 'Scapular elevation & upward rotation', 'Shoulder shrug, overhead press'],
            ['Trapezius (mid)', 'T1–T5', 'Spine of scapula', 'Scapular retraction', 'Rows, face pull'],
            ['Trapezius (lower)', 'T6–T12', 'Root of scapular spine', 'Scapular depression', 'Y-raise, dip'],
            ['Rhomboids', 'C7–T5', 'Medial scapular border', 'Scapular retraction & downward rotation', 'Rows, band pull-apart'],
        ]
    ))
    e.append(Spacer(1, 8))

    e.append(Paragraph('Shoulder (Deltoids & Rotator Cuff)', ST['h2']))
    e.append(Paragraph(
        'The deltoid has three distinct heads that act as separate muscles:', ST['body']))
    for item in [
        'Anterior (front) — shoulder flexion, horizontal adduction; hit by pressing and front raises',
        'Lateral (side) — shoulder abduction; isolated by lateral raises (best at >30° abduction)',
        'Posterior (rear) — shoulder extension, horizontal abduction; engaged in rows and face pulls',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))
    e.append(Paragraph(
        '<b>Rotator Cuff (SITS muscles):</b> Four small muscles surrounding the glenohumeral '
        'joint that stabilise the ball within the socket. They are crucial for injury '
        'prevention in overhead athletes and weightlifters:', ST['body']))
    e.append(two_col_table(
        ['Muscle', 'Primary Action'],
        [
            ['Supraspinatus', 'Shoulder abduction (initiation)'],
            ['Infraspinatus', 'External rotation'],
            ['Teres Minor', 'External rotation'],
            ['Subscapularis', 'Internal rotation'],
        ]
    ))
    e.append(Spacer(1, 8))
    e.append(Paragraph(
        '<b>Programming note:</b> For every internal rotation movement (bench press, push-up, '
        'lat pulldown), programme a compensatory external rotation exercise (band ER, face '
        'pull) to prevent anterior shoulder dominance and impingement syndrome.', ST['body']))

    e.append(Paragraph('Arms (Biceps, Triceps, Forearms)', ST['h2']))
    e.append(multi_col_table(
        ['Muscle', 'Heads', 'Main Action', 'Best Exercise'],
        [
            ['Biceps brachii', '2 (short + long)', 'Elbow flexion, supination', 'Barbell/dumbbell curl'],
            ['Brachialis', '1', 'Elbow flexion (strongest)', 'Hammer curl'],
            ['Brachioradialis', '1', 'Elbow flexion (neutral grip)', 'Reverse curl'],
            ['Triceps brachii', '3 (long/lat/med)', 'Elbow extension', 'Close-grip bench, dip, pushdown'],
            ['Forearm flexors', 'Multiple', 'Wrist flexion, grip', 'Deadlift, carries'],
        ]
    ))
    e.append(Spacer(1, 8))

    e.append(Paragraph('Lower Body Muscles', ST['h1']))

    e.append(Paragraph('Quadriceps', ST['h2']))
    e.append(Paragraph(
        'The quadriceps femoris is a group of four muscles on the anterior thigh — the primary '
        'knee extensors and important hip flexors:', ST['body']))
    for item in [
        'Rectus femoris — only quad that crosses the hip; hip flexion + knee extension',
        'Vastus lateralis — outer thigh; often dominant, especially in women',
        'Vastus medialis — inner thigh; the teardrop shape visible in lean individuals; stabilises patella',
        'Vastus intermedius — deep, beneath rectus femoris; pure knee extension',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))
    e.append(Paragraph(
        'The patellar tendon connects all four heads (via patella) to the tibial tuberosity. '
        'Patellar tendinopathy (jumper\'s knee) develops when repetitive tensile loads exceed '
        'the tendon\'s capacity — common in volleyball, basketball, and high-volume squatting.', ST['body']))

    e.append(Paragraph('Hamstrings & Glutes', ST['h2']))
    e.append(multi_col_table(
        ['Muscle', 'Origin', 'Insertion', 'Action'],
        [
            ['Biceps femoris (long)', 'Ischial tuberosity', 'Head of fibula', 'Hip extension + knee flexion'],
            ['Biceps femoris (short)', 'Femur (linea aspera)', 'Head of fibula', 'Knee flexion only'],
            ['Semitendinosus', 'Ischial tuberosity', 'Pes anserinus (tibia)', 'Hip extension + knee flexion + medial rotation'],
            ['Semimembranosus', 'Ischial tuberosity', 'Medial condyle of tibia', 'Hip extension + knee flexion'],
            ['Gluteus maximus', 'Ilium, sacrum, coccyx', 'Gluteal tuberosity, IT band', 'Hip extension + external rotation'],
            ['Gluteus medius', 'Lateral ilium', 'Greater trochanter', 'Hip abduction + internal rotation'],
            ['Gluteus minimus', 'Lateral ilium (lower)', 'Greater trochanter', 'Hip abduction + internal rotation'],
        ]
    ))
    e.append(Spacer(1, 8))
    e.append(info_box('Why Glutes Matter Beyond Aesthetics', [
        'Gluteus maximus is the largest muscle in the body — a primary power producer',
        'Weak glutes cause compensatory lumbar extension during hip-dominant movements',
        'Gluteus medius weakness = knee valgus (collapse inward) during squats and landing',
        'Hip thrust activates glute max ~30% more than squat; include both in programming',
        'Runners with weak glutes show higher rates of IT band syndrome and patellofemoral pain',
    ], RFC_RED))
    e.append(Spacer(1, 8))

    e.append(Paragraph('Calves & Lower Leg', ST['h2']))
    e.append(multi_col_table(
        ['Muscle', 'Origin', 'Action', 'Best Exercise'],
        [
            ['Gastrocnemius', 'Posterior femoral condyles', 'Plantarflexion + knee flexion', 'Standing calf raise'],
            ['Soleus', 'Posterior tibia/fibula', 'Plantarflexion (knee bent)', 'Seated calf raise'],
            ['Tibialis anterior', 'Lateral tibia', 'Dorsiflexion + inversion', 'Toe raises'],
            ['Peroneals', 'Fibula', 'Eversion + plantarflexion', 'Lateral ankle drills'],
        ]
    ))
    e.append(Spacer(1, 8))

    # ── SECTION 6 ──
    e.append(section_divider('SECTION 6: Core Anatomy'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('The Core — Beyond Abs', ST['h1']))
    e.append(Paragraph(
        'The "core" is not merely the rectus abdominis (the "six-pack" muscle). True core '
        'function involves a canister of muscles that stabilise the spine and pelvis during '
        'virtually every movement:', ST['body']))
    e.append(multi_col_table(
        ['Layer', 'Muscle', 'Primary Role'],
        [
            ['Anterior', 'Rectus abdominis', 'Spinal flexion, intra-abdominal pressure'],
            ['Lateral', 'External oblique', 'Rotation, lateral flexion'],
            ['Lateral', 'Internal oblique', 'Rotation (opposite), lateral flexion'],
            ['Deep', 'Transversus abdominis', 'Circumferential stabilisation, IAP'],
            ['Posterior', 'Erector spinae', 'Spinal extension, posture'],
            ['Posterior', 'Multifidus', 'Segmental spinal stabilisation'],
            ['Floor', 'Pelvic floor', 'Intra-abdominal pressure, pelvic organ support'],
            ['Ceiling', 'Diaphragm', 'Breathing, intra-abdominal pressure'],
        ]
    ))
    e.append(Spacer(1, 8))
    e.append(Paragraph(
        'Intra-abdominal pressure (IAP) is the hydrostatic pressure within the abdominal '
        'cavity generated when the diaphragm descends, pelvic floor contracts, and transversus '
        'abdominis co-activates. This creates a rigid cylinder protecting the spine during '
        'heavy loading — the physiological basis for the Valsalva manoeuvre in powerlifting.', ST['body']))

    # ── SECTION 7 ──
    e.append(section_divider('SECTION 7: Tendons, Ligaments & Connective Tissue'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('Tendons vs Ligaments', ST['h1']))
    e.append(two_col_table(
        ['TENDONS', 'LIGAMENTS'],
        [
            ['Connect muscle to bone', 'Connect bone to bone'],
            ['Transmit muscle force', 'Constrain joint movement'],
            ['Primarily Type I collagen', 'Type I + Type III collagen mix'],
            ['Moderate blood supply', 'Poor blood supply (slow healing)'],
            ['Respond well to progressive loading', 'Limited capacity for hypertrophy'],
            ['Can store elastic energy', 'Primarily passive restraints'],
        ]
    ))
    e.append(Spacer(1, 10))
    e.append(Paragraph(
        '<b>Tendon adaptation to training:</b> Unlike muscle, tendon takes 6–12 months to '
        'meaningfully strengthen. This creates a "weak link" window when muscle strength '
        'outpaces tendon adaptation — a common cause of overuse injuries in people who '
        'progress too rapidly. This is why progressive overload must be gradual.', ST['body']))

    e.append(Paragraph('Fascia — The Body\'s Connective Web', ST['h2']))
    e.append(Paragraph(
        'Fascia is a continuous web of connective tissue enveloping every muscle, organ, nerve, '
        'and blood vessel. Far from passive wrapping, fascia:', ST['body']))
    for item in [
        'Transmits force between muscles across joints (myofascial slings)',
        'Contains proprioceptors — contributing to body position sense',
        'Becomes stiffer ("densified") with dehydration, immobility, and chronic stress',
        'Responds to slow, sustained stretching (yin yoga, foam rolling) and hydration',
    ]:
        e.append(Paragraph(f'• {item}', ST['bullet']))

    # ── SECTION 8 ──
    e.append(section_divider('SECTION 8: Introduction to Muscle Hypertrophy'))
    e.append(Spacer(1, 6))
    e.append(Paragraph('What Makes Muscles Grow?', ST['h1']))
    e.append(Paragraph(
        'Hypertrophy (muscle growth) occurs when muscle protein synthesis (MPS) exceeds muscle '
        'protein breakdown (MPB) over time. Three primary mechanisms drive hypertrophy:', ST['body']))
    e.append(multi_col_table(
        ['Mechanism', 'Description', 'Training Method'],
        [
            ['Mechanical tension', 'Force on actin-myosin cross-bridges — the dominant driver', 'Heavy compounds, full ROM, controlled eccentrics'],
            ['Metabolic stress', 'Lactate accumulation, swelling, cell signalling hormones', 'Moderate weight, high reps, short rest, pump work'],
            ['Muscle damage', 'Eccentric-induced micro-tears triggering satellite cell activity', 'Novel exercises, slow eccentrics, full stretch'],
        ]
    ))
    e.append(Spacer(1, 8))
    e.append(Paragraph(
        'Research increasingly shows mechanical tension is the primary driver. Metabolic stress '
        'and muscle damage are secondary pathways. This explains why heavy, progressive training '
        '(even if reps are low) produces substantial hypertrophy when volume is adequate.', ST['body']))
    e.append(Paragraph(
        '<b>Satellite cells</b> are muscle stem cells that reside beneath the basal lamina. '
        'Following mechanical damage or metabolic stress, they activate, proliferate, and fuse '
        'with existing fibres, donating their nuclei. More nuclei = greater synthetic capacity = '
        'larger muscle cell.', ST['body']))
    e.append(Paragraph(
        '<b>mTORC1</b> (mechanistic target of rapamycin complex 1) is the primary anabolic '
        'signalling hub. Resistance training and leucine (from dietary protein) both activate '
        'mTORC1, which upregulates ribosomal biogenesis and protein synthesis. This molecular '
        'basis explains why post-workout protein consumption amplifies training adaptations.', ST['body']))

    e.append(info_box('Module 1 Key Takeaways', [
        'The skeleton provides structure, leverage, and protection — bone is a living, adaptable tissue',
        'Synovial joints enable the wide range of motion required for exercise; anatomy varies between individuals',
        'Three muscle fibre types (I, IIa, IIx) differ in speed, fatigue resistance, and metabolic pathway',
        'Major muscle groups have distinct origins, insertions, and actions — knowing them prevents injury and improves targeting',
        'Hypertrophy requires mechanical tension as the primary stimulus, aided by adequate protein intake',
        'Tendons adapt more slowly than muscles — the primary reason for gradual progression rules',
    ], RFC_DARK))
    e.append(Spacer(1, 8))

    e.append(Paragraph('Quick Review Questions', ST['h2']))
    for i, q in enumerate([
        'What is the difference between compact and cancellous bone, and why does this matter for exercise?',
        'Name the four rotator cuff muscles and explain their collective function.',
        'How do Type I and Type IIx muscle fibres differ in terms of energy system use and fatigue?',
        'Explain the sliding filament theory of muscle contraction.',
        'Why is the transversus abdominis considered the most important "core" muscle for spinal stability?',
    ], 1):
        e.append(Paragraph(f'{i}. {q}', ST['body']))

    doc.build(e)
    print(f'Generated: {fname}')

gen_b1_m1()
print('M1 done.')
