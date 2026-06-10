#!/usr/bin/env python3
"""Generate 5 styled fitness PDFs with attractive cover pages and templates."""

import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF

W, H = A4  # 595.28 x 841.89 pts

# ────────────────────────────────────────────────────────────
#  BRAND PALETTE  (r, g, b  0-1)
# ────────────────────────────────────────────────────────────
THEMES = {
    "cutting": {
        "bg":       colors.HexColor("#0D0D0D"),
        "accent":   colors.HexColor("#C0392B"),
        "accent2":  colors.HexColor("#E74C3C"),
        "gold":     colors.HexColor("#F39C12"),
        "text":     colors.HexColor("#EEEEEE"),
        "muted":    colors.HexColor("#888888"),
        "row_odd":  colors.HexColor("#1A1A1A"),
        "row_even": colors.HexColor("#141414"),
        "header":   colors.HexColor("#C0392B"),
    },
    "bulking": {
        "bg":       colors.HexColor("#0A0F1A"),
        "accent":   colors.HexColor("#1565C0"),
        "accent2":  colors.HexColor("#42A5F5"),
        "gold":     colors.HexColor("#FFC107"),
        "text":     colors.HexColor("#EEEEEE"),
        "muted":    colors.HexColor("#888888"),
        "row_odd":  colors.HexColor("#111827"),
        "row_even": colors.HexColor("#0D1520"),
        "header":   colors.HexColor("#1565C0"),
    },
    "beginner": {
        "bg":       colors.HexColor("#071209"),
        "accent":   colors.HexColor("#1B5E20"),
        "accent2":  colors.HexColor("#43A047"),
        "gold":     colors.HexColor("#FFCA28"),
        "text":     colors.HexColor("#EEEEEE"),
        "muted":    colors.HexColor("#888888"),
        "row_odd":  colors.HexColor("#0F1F10"),
        "row_even": colors.HexColor("#0A1A0B"),
        "header":   colors.HexColor("#1B5E20"),
    },
    "keto": {
        "bg":       colors.HexColor("#0F0900"),
        "accent":   colors.HexColor("#E65100"),
        "accent2":  colors.HexColor("#FF8F00"),
        "gold":     colors.HexColor("#FFD600"),
        "text":     colors.HexColor("#EEEEEE"),
        "muted":    colors.HexColor("#888888"),
        "row_odd":  colors.HexColor("#1A1000"),
        "row_even": colors.HexColor("#140D00"),
        "header":   colors.HexColor("#E65100"),
    },
    "female": {
        "bg":       colors.HexColor("#0F0A14"),
        "accent":   colors.HexColor("#7B1FA2"),
        "accent2":  colors.HexColor("#CE93D8"),
        "gold":     colors.HexColor("#F06292"),
        "text":     colors.HexColor("#EEEEEE"),
        "muted":    colors.HexColor("#888888"),
        "row_odd":  colors.HexColor("#1A1020"),
        "row_even": colors.HexColor("#140B1A"),
        "header":   colors.HexColor("#7B1FA2"),
    },
}


# ────────────────────────────────────────────────────────────
#  PAGE BACKGROUND CANVAS CALLBACK
# ────────────────────────────────────────────────────────────
def make_page_bg(theme_key, is_cover=False):
    t = THEMES[theme_key]

    def bg(canv, doc):
        canv.saveState()
        # solid dark background
        canv.setFillColor(t["bg"])
        canv.rect(0, 0, W, H, fill=1, stroke=0)

        if is_cover:
            # top accent bar
            canv.setFillColor(t["accent"])
            canv.rect(0, H - 18, W, 18, fill=1, stroke=0)
            # bottom accent bar
            canv.rect(0, 0, W, 8, fill=1, stroke=0)
            # left stripe
            canv.setFillColor(t["accent2"])
            canv.setFillAlpha(0.18)
            canv.rect(0, 0, 6, H, fill=1, stroke=0)
            canv.setFillAlpha(1)

            # decorative diagonal lines bottom-right
            canv.setStrokeColor(t["accent"])
            canv.setStrokeAlpha(0.12)
            canv.setLineWidth(1)
            for i in range(0, 220, 22):
                canv.line(W - i, 0, W, i)
            canv.setStrokeAlpha(1)
        else:
            # inner pages: subtle top line
            canv.setFillColor(t["accent"])
            canv.rect(0, H - 4, W, 4, fill=1, stroke=0)
            canv.rect(0, 0, W, 3, fill=1, stroke=0)
            # left margin line
            canv.setStrokeColor(t["accent2"])
            canv.setStrokeAlpha(0.15)
            canv.setLineWidth(1)
            canv.line(30, 28, 30, H - 28)
            canv.setStrokeAlpha(1)

        # footer text on every page
        canv.setFont("Helvetica", 7)
        canv.setFillColor(t["muted"])
        canv.drawString(36, 10, "AMAN TRAINING CLUB  |  Royal Fitness Club")
        canv.drawRightString(W - 36, 10, f"Page {doc.page}")
        canv.restoreState()

    return bg


# ────────────────────────────────────────────────────────────
#  STYLE HELPERS
# ────────────────────────────────────────────────────────────
def make_styles(theme_key):
    t = THEMES[theme_key]
    styles = {}

    styles["title"] = ParagraphStyle(
        "title",
        fontName="Helvetica-Bold",
        fontSize=30,
        textColor=t["text"],
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=36,
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle",
        fontName="Helvetica",
        fontSize=13,
        textColor=t["accent2"],
        alignment=TA_CENTER,
        spaceAfter=4,
        leading=18,
    )
    styles["tagline"] = ParagraphStyle(
        "tagline",
        fontName="Helvetica-Oblique",
        fontSize=10,
        textColor=t["muted"],
        alignment=TA_CENTER,
        spaceAfter=0,
    )
    styles["section"] = ParagraphStyle(
        "section",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=t["accent2"],
        spaceBefore=14,
        spaceAfter=4,
        borderPad=4,
        leftIndent=0,
        leading=16,
    )
    styles["subsection"] = ParagraphStyle(
        "subsection",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=t["gold"],
        spaceBefore=8,
        spaceAfter=3,
        leading=13,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=9,
        textColor=t["text"],
        spaceBefore=2,
        spaceAfter=2,
        leading=13,
        leftIndent=14,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=9,
        textColor=t["text"],
        spaceBefore=1,
        spaceAfter=1,
        leading=13,
        leftIndent=20,
        bulletIndent=8,
    )
    styles["subbullet"] = ParagraphStyle(
        "subbullet",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=t["muted"],
        spaceBefore=1,
        spaceAfter=1,
        leading=12,
        leftIndent=34,
        bulletIndent=22,
    )
    styles["disclaimer"] = ParagraphStyle(
        "disclaimer",
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        textColor=t["muted"],
        alignment=TA_CENTER,
        spaceAfter=4,
        leading=11,
    )
    styles["toc_item"] = ParagraphStyle(
        "toc_item",
        fontName="Helvetica",
        fontSize=10,
        textColor=t["text"],
        spaceBefore=3,
        spaceAfter=3,
        leading=14,
        leftIndent=20,
    )
    return styles


# ────────────────────────────────────────────────────────────
#  REUSABLE FLOWABLES
# ────────────────────────────────────────────────────────────
def divider(theme_key):
    t = THEMES[theme_key]
    return HRFlowable(
        width="100%", thickness=0.5, color=t["accent2"],
        spaceAfter=6, spaceBefore=4
    )


def section_header(text, theme_key, styles, icon=""):
    t = THEMES[theme_key]
    label = f"{icon}  {text}" if icon else text
    p = Paragraph(f"<b>{label}</b>", styles["section"])
    hr = HRFlowable(
        width="100%", thickness=1.5, color=t["accent"],
        spaceAfter=5, spaceBefore=0
    )
    return [p, hr]


def bullet_item(text, styles, level=0):
    style = "subbullet" if level > 0 else "bullet"
    symbol = "–" if level > 0 else "•"
    return Paragraph(f"{symbol}  {text}", styles[style])


def build_table(headers, rows, theme_key, col_widths=None):
    t = THEMES[theme_key]
    data = [headers] + rows
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), t["header"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#333333")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [t["row_odd"], t["row_even"]]),
        ("TEXTCOLOR", (0, 1), (-1, -1), t["text"]),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 0), (-1, 0), [t["header"]]),
    ]
    tbl.setStyle(TableStyle(style))
    return tbl


# ────────────────────────────────────────────────────────────
#  COVER PAGE BUILDER
# ────────────────────────────────────────────────────────────
def build_cover(
    title_lines, subtitle, edition, theme_key, styles,
    badge_texts=None, disclaimer_text=None
):
    t = THEMES[theme_key]
    items = []

    items.append(Spacer(1, 52 * mm))

    # top badge row
    if badge_texts:
        badge_data = [[b for b in badge_texts]]
        badge_col = [(W - 80) / len(badge_texts)] * len(badge_texts)
        badge_tbl = Table(badge_data, colWidths=badge_col)
        badge_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), t["accent"]),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ]))
        items.append(badge_tbl)
        items.append(Spacer(1, 8 * mm))

    # title
    for line in title_lines:
        items.append(Paragraph(line, styles["title"]))

    items.append(Spacer(1, 4 * mm))

    # accent divider
    items.append(HRFlowable(
        width="60%", thickness=2.5, color=t["accent"],
        spaceAfter=6, spaceBefore=4
    ))

    items.append(Paragraph(subtitle, styles["subtitle"]))
    items.append(Spacer(1, 2 * mm))
    items.append(Paragraph(edition, styles["tagline"]))
    items.append(Spacer(1, 10 * mm))

    # info card
    card_data = [
        [
            Paragraph("<b>AMAN TRAINING CLUB</b>", ParagraphStyle(
                "card_brand", fontName="Helvetica-Bold", fontSize=10,
                textColor=t["accent2"], alignment=TA_CENTER
            )),
        ]
    ]
    card = Table(card_data, colWidths=[W - 80])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1A1A1A")),
        ("BOX", (0, 0), (-1, -1), 1, t["accent"]),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    items.append(card)
    items.append(Spacer(1, 80 * mm))

    if disclaimer_text:
        items.append(Paragraph(disclaimer_text, styles["disclaimer"]))

    items.append(PageBreak())
    return items


# ════════════════════════════════════════════════════════════
#  PDF 1 — ADVANCED CUTTING CYCLE (12 WEEKS)
# ════════════════════════════════════════════════════════════
def generate_cutting_pdf(path):
    TK = "cutting"
    t = THEMES[TK]
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=28, bottomMargin=28
    )
    styles = make_styles(TK)
    items = []

    # ── Cover
    items += build_cover(
        title_lines=["ADVANCED CUTTING", "STEROID CYCLE"],
        subtitle="12-Week Complete Protocol — Dosages · AI · PCT · Supplements",
        edition="AMAN TRAINING CLUB  •  Professional Series  •  2024 Edition",
        theme_key=TK, styles=styles,
        badge_texts=["12 WEEKS", "ADVANCED LEVEL", "FULL PCT INCLUDED", "SUPPLEMENT STACK"],
        disclaimer_text=(
            "⚠  MEDICAL DISCLAIMER: This document is for informational and educational purposes only. "
            "Anabolic steroids are controlled substances in many countries. Always consult a licensed "
            "physician before beginning any hormonal protocol. Misuse may cause serious health risks."
        )
    )

    # ── Table of Contents
    items += section_header("TABLE OF CONTENTS", TK, styles, "📋")
    toc = [
        "1.  Overview & Goals",
        "2.  Core Compound Stack",
        "3.  12-Week Dosage Schedule",
        "4.  Aromatase Inhibitor (AI) Protocol",
        "5.  Clenbuterol & T3 Cycle",
        "6.  HGH Fragment 176-191 & IGF-1 LR3",
        "7.  MENT (Optional Add-On)",
        "8.  Post Cycle Therapy (PCT) — Weeks 13–16",
        "9.  Essential Supplement Stack",
        "10. Training & Nutrition Guidelines",
        "11. Blood Work & Health Monitoring",
    ]
    for item in toc:
        items.append(Paragraph(item, styles["toc_item"]))
    items.append(PageBreak())

    # ── 1. Overview
    items += section_header("1. OVERVIEW & GOALS", TK, styles, "🎯")
    items.append(Paragraph(
        "This advanced 12-week cutting protocol is designed for experienced athletes (minimum 3+ years "
        "of natural training + prior steroid experience) who want to achieve maximum fat loss while "
        "preserving — or even gaining — lean muscle mass. The stack prioritizes <b>hardness</b>, "
        "<b>vascularity</b>, and <b>definition</b> while keeping water retention minimal.",
        styles["body"]
    ))
    items.append(Spacer(1, 3))
    for g in [
        "Aggressive fat loss (target: -8 to -12 lbs body fat over 12 weeks)",
        "Maintain or increase lean muscle mass",
        "Improve muscle hardness, definition, and vascularity",
        "Boost strength despite caloric deficit",
        "Minimize water retention and estrogen-related side effects",
    ]:
        items.append(bullet_item(g, styles))
    items.append(Spacer(1, 4))

    # ── 2. Core Compounds
    items += section_header("2. CORE COMPOUND STACK", TK, styles, "💊")
    compound_rows = [
        ["Testosterone Propionate", "Test Prop", "100–150 mg", "EOD", "Wks 1–12", "Androgenic base"],
        ["Trenbolone Acetate", "Tren Ace", "75–100 mg", "EOD", "Wks 1–12", "Hardening + fat loss"],
        ["Masteron Propionate", "Mast Prop", "100 mg", "EOD", "Wks 1–12", "Anti-estrogen + hardness"],
        ["Primobolan", "Primo", "600 mg", "Weekly", "Wks 1–12", "Lean muscle + low sides"],
        ["Anavar (Oxandrolone)", "Var", "50 mg/day", "Daily", "Wks 1–8", "Strength + hardness"],
        ["Winstrol (Stanozolol)", "Winny", "50 mg/day", "Daily", "Wks 9–12", "Final hardening"],
    ]
    headers = ["Compound", "Short Name", "Dose", "Frequency", "Duration", "Purpose"]
    col_w = [(W - 72) * f for f in [0.21, 0.12, 0.12, 0.13, 0.12, 0.30]]
    items.append(build_table(headers, compound_rows, TK, col_w))
    items.append(Spacer(1, 4))

    # ── 3. Weekly Schedule
    items += section_header("3. 12-WEEK DOSAGE SCHEDULE", TK, styles, "📅")
    sched_headers = ["Week", "Test Prop\n(EOD)", "Tren Ace\n(EOD)", "Mast Prop\n(EOD)", "Primo\n(Weekly)", "Anavar\n(Daily)", "Winny\n(Daily)"]
    sched_rows = [
        ["1", "100 mg", "75 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["2", "100 mg", "75 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["3", "100 mg", "75 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["4", "150 mg", "100 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["5", "150 mg", "100 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["6", "150 mg", "100 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["7", "150 mg", "100 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["8", "150 mg", "100 mg", "100 mg", "600 mg", "50 mg", "—"],
        ["9", "150 mg", "100 mg", "100 mg", "600 mg", "—", "50 mg"],
        ["10", "150 mg", "100 mg", "100 mg", "600 mg", "—", "50 mg"],
        ["11", "150 mg", "100 mg", "100 mg", "600 mg", "—", "50 mg"],
        ["12", "150 mg", "100 mg", "100 mg", "600 mg", "—", "50 mg"],
    ]
    col_w2 = [(W - 72) * f for f in [0.07, 0.13, 0.13, 0.14, 0.14, 0.14, 0.14]]
    items.append(build_table(sched_headers, sched_rows, TK, col_w2))
    items.append(Spacer(1, 4))

    # ── 4. AI Protocol
    items += section_header("4. AROMATASE INHIBITOR (AI) PROTOCOL", TK, styles, "🛡")
    for item in [
        "<b>Arimidex (Anastrozole):</b> 0.5 mg every other day (EOD) throughout the cycle",
        "<b>Cabergoline (Caber):</b> 0.25 mg twice per week to control prolactin (from Tren)",
        "Monitor estrogen via blood work; adjust AI dose based on E2 levels",
        "Target estrogen range: 20–30 pg/mL for optimal fat loss and libido",
        "Do NOT crush E2 to zero — leads to joint pain, low libido, and mood crashes",
    ]:
        items.append(bullet_item(item, styles))

    # ── 5. Clen & T3
    items += section_header("5. CLENBUTEROL & T3 CYCLE", TK, styles, "🔥")
    items.append(Paragraph("<b>Clenbuterol Protocol (2 weeks on / 2 weeks off):</b>", styles["subsection"]))
    for item in [
        "Start: 20 mcg/day → increase by 20 mcg every 2 days",
        "Max: 100–120 mcg/day (women: 80 mcg max)",
        "Always taper down over last 2 days of each ON cycle",
        "Side effects: tremors, insomnia, elevated heart rate — reduce dose if severe",
    ]:
        items.append(bullet_item(item, styles))
    items.append(Paragraph("<b>T3 (Cytomel) Protocol:</b>", styles["subsection"]))
    for item in [
        "Start: 25 mcg/day — Week 1–2",
        "Increase: 50 mcg/day — Week 3–10",
        "Taper: 25 mcg/day — Week 11–12",
        "⚠ Never exceed 75 mcg/day; always taper, never stop cold turkey",
        "Monitor thyroid via blood work before and after cycle",
    ]:
        items.append(bullet_item(item, styles))

    # ── 6. HGH Fragment & IGF-1
    items += section_header("6. HGH FRAGMENT 176-191 & IGF-1 LR3", TK, styles, "💉")
    for item in [
        "<b>HGH Fragment 176-191:</b> 500 mcg/day — split into 2 injections (morning + pre-workout)",
        "Fasted injection protocol provides best fat-burning results",
        "<b>IGF-1 LR3:</b> 40–60 mcg post-workout on training days only",
        "Maximum cycle length for IGF-1 LR3: 4–6 weeks (receptor desensitization)",
        "Reconstitute with bacteriostatic water; store refrigerated",
    ]:
        items.append(bullet_item(item, styles))

    items.append(PageBreak())

    # ── 7. MENT
    items += section_header("7. MENT — OPTIONAL ADD-ON", TK, styles, "⚡")
    items.append(Paragraph(
        "<b>MENT (Trestolone Acetate)</b> is an extremely potent compound, roughly 10× the anabolic "
        "activity of testosterone. It is <b>optional</b> and only recommended for highly advanced users.",
        styles["body"]
    ))
    for item in [
        "Dose: 25 mg/day (injected daily or EOD)",
        "Duration: Weeks 1–6 only",
        "MENT aromatizes heavily — increase AI dose significantly if added",
        "Monitor blood work every 3 weeks if using MENT",
        "Not recommended for first-time or intermediate users",
    ]:
        items.append(bullet_item(item, styles))

    # ── 8. PCT
    items += section_header("8. POST CYCLE THERAPY (PCT) — WEEKS 13–16", TK, styles, "🔄")
    items.append(Paragraph(
        "PCT begins <b>3 days after last short-ester injection</b> (Test Prop / Tren Ace / Mast Prop). "
        "If using Primobolan alone (long ester), begin PCT 14 days after last injection.",
        styles["body"]
    ))
    pct_rows = [
        ["HCG", "500 IU", "Every 3 days", "Wks 13–14", "Kick-start natural testosterone"],
        ["Clomid (Clomiphene)", "50 mg/day", "Daily", "Wks 13–16", "LH/FSH recovery"],
        ["Nolvadex (Tamoxifen)", "20 mg/day", "Daily", "Wks 13–16", "SERM estrogen control"],
        ["Arimidex", "0.25 mg", "EOD", "Wks 13–15", "Gradual AI taper"],
    ]
    pct_headers = ["Compound", "Dose", "Frequency", "Duration", "Purpose"]
    col_w3 = [(W - 72) * f for f in [0.22, 0.14, 0.14, 0.14, 0.36]]
    items.append(build_table(pct_headers, pct_rows, TK, col_w3))

    # ── 9. Supplements
    items += section_header("9. ESSENTIAL SUPPLEMENT STACK", TK, styles, "💊")
    supp_categories = {
        "Liver Support": [
            "Milk Thistle (Silymarin) — 600–800 mg/day",
            "TUDCA (Tauroursodeoxycholic Acid) — 500 mg/day (especially with oral steroids)",
        ],
        "Cardiovascular Support": [
            "Omega-3 Fish Oil — 4–6 g/day (EPA+DHA)",
            "CoQ10 (Ubiquinol) — 200 mg/day",
            "Red Yeast Rice — 1200 mg/day (cholesterol management)",
            "Hawthorn Berry Extract — 500 mg twice daily",
        ],
        "Joint Support": [
            "Glucosamine Sulphate — 1500 mg/day",
            "Chondroitin Sulphate — 1200 mg/day",
            "Collagen Peptides — 10 g/day",
        ],
        "Hormonal Balance": [
            "DIM (Diindolylmethane) — 200 mg/day (estrogen metabolism)",
            "ZMA (Zinc + Magnesium + B6) — nightly before bed",
        ],
        "Urinary/Prostate Health": [
            "Cranberry Extract — 400 mg/day",
            "Saw Palmetto — 320 mg/day",
        ],
        "General Health": [
            "High-quality Multivitamin — daily with meals",
            "Vitamin D3 + K2 — 5000 IU D3 / 100 mcg K2",
            "Electrolytes — daily (especially with Clenbuterol/T3)",
            "Whey Protein — 40–60 g/day around training",
            "BCAAs — 10 g intra-workout",
        ],
    }
    for cat, supps in supp_categories.items():
        items.append(Paragraph(f"<b>{cat}:</b>", styles["subsection"]))
        for s in supps:
            items.append(bullet_item(s, styles))

    # ── 10. Training & Nutrition
    items += section_header("10. TRAINING & NUTRITION GUIDELINES", TK, styles, "🏋")
    items.append(Paragraph("<b>Training Split:</b>", styles["subsection"]))
    for item in [
        "5–6 days/week: Push / Pull / Legs split with 1–2 rest days",
        "Cardio: 30–45 min moderate intensity (LISS) 4–5×/week, fasted preferred",
        "HIIT: 2×/week max — avoid overtraining in caloric deficit",
        "Prioritize compound movements; add isolation for detail/separation",
    ]:
        items.append(bullet_item(item, styles))
    items.append(Paragraph("<b>Nutrition:</b>", styles["subsection"]))
    for item in [
        "Caloric deficit: 300–500 kcal below TDEE",
        "Protein: 1.5–2.0 g/lb lean body mass (minimum 200 g/day)",
        "Carbohydrates: Timed around workouts; reduce on rest days",
        "Fats: 20–25% of total calories (healthy sources only)",
        "Water: Minimum 4 litres/day — increases with Clenbuterol use",
    ]:
        items.append(bullet_item(item, styles))

    # ── 11. Blood Work
    items += section_header("11. BLOOD WORK & HEALTH MONITORING", TK, styles, "🩸")
    for item in [
        "<b>Pre-cycle:</b> Full CBC, testosterone (total + free), LH, FSH, estradiol (E2), liver panel (ALT/AST), lipid panel, kidney function (creatinine, eGFR), thyroid (TSH, T3, T4)",
        "<b>Mid-cycle (Week 6):</b> Testosterone, E2, liver panel, lipid panel, hematocrit",
        "<b>End of cycle (Week 12):</b> Full panel same as pre-cycle",
        "<b>PCT Week 4:</b> Testosterone, LH, FSH, E2 — assess recovery",
        "If ALT/AST >3× upper normal: stop all orals immediately",
        "If hematocrit >52%: donate blood or reduce dosage",
    ]:
        items.append(bullet_item(item, styles))

    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "⚠  This guide is provided for educational purposes only. The use of anabolic steroids without "
        "a prescription is illegal in many jurisdictions and carries significant health risks. "
        "AMAN TRAINING CLUB does not endorse illegal activity. Always consult a medical professional.",
        styles["disclaimer"]
    ))

    doc.build(items,
              onFirstPage=make_page_bg(TK, is_cover=True),
              onLaterPages=make_page_bg(TK, is_cover=False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
#  PDF 2 — ADVANCED BULKING WITH PEPTIDES
# ════════════════════════════════════════════════════════════
def generate_bulking_pdf(path):
    TK = "bulking"
    t = THEMES[TK]
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=28, bottomMargin=28
    )
    styles = make_styles(TK)
    items = []

    items += build_cover(
        title_lines=["ADVANCED STEROID CYCLE", "FOR BULKING", "WITH PEPTIDES"],
        subtitle="12–16 Week Mass Protocol — Compounds · Peptides · AI · PCT",
        edition="AMAN TRAINING CLUB  •  Professional Series  •  2024 Edition",
        theme_key=TK, styles=styles,
        badge_texts=["12–16 WEEKS", "ADVANCED", "PEPTIDE PROTOCOL", "MASS BUILDER"],
        disclaimer_text=(
            "⚠  MEDICAL DISCLAIMER: For educational purposes only. Always consult a licensed physician. "
            "Anabolic steroids and peptides are regulated substances. Misuse carries serious health risks."
        )
    )

    # TOC
    items += section_header("TABLE OF CONTENTS", TK, styles, "📋")
    for item in [
        "1.  Overview — Mass Building Philosophy",
        "2.  Core Compound Stack",
        "3.  12–16 Week Dosage Protocol",
        "4.  Peptide Protocol (IGF-1 LR3 · GHRP-6 · CJC-1295 DAC)",
        "5.  Optional HGH Addition",
        "6.  Aromatase Inhibitor & Prolactin Control",
        "7.  Post Cycle Therapy (PCT)",
        "8.  Essential Supplement Stack",
        "9.  Mass-Building Nutrition Plan",
        "10. Training Programming",
    ]:
        items.append(Paragraph(item, styles["toc_item"]))
    items.append(PageBreak())

    # 1. Overview
    items += section_header("1. OVERVIEW — MASS BUILDING PHILOSOPHY", TK, styles, "🎯")
    items.append(Paragraph(
        "This advanced bulking protocol is engineered to produce <b>maximum lean muscle mass gains</b> "
        "over 12–16 weeks. By combining a potent anabolic base with cutting-edge peptide technology, "
        "this protocol stimulates natural GH release alongside exogenous hormones, creating an "
        "<b>anabolic environment</b> unlike any single-compound approach.",
        styles["body"]
    ))
    for g in [
        "Target lean mass gain: 15–20 lbs over 16 weeks",
        "Strength increase: 20–40 lbs on major compound lifts",
        "Minimize fat accumulation during bulk phase",
        "Maximize recovery speed with peptide GH pulse",
        "Maintain health markers within safe ranges throughout",
    ]:
        items.append(bullet_item(g, styles))

    # 2. Compounds
    items += section_header("2. CORE COMPOUND STACK", TK, styles, "💊")
    rows = [
        ["Testosterone Enanthate", "Test E", "500–750 mg", "Weekly (2 pins)", "12–16 wks", "Anabolic base"],
        ["Nandrolone Decanoate", "Deca", "400–600 mg", "Weekly", "12–16 wks", "Mass + joint lubrication"],
        ["Dianabol (Methandrostenolone)", "Dbol", "30–50 mg/day", "Daily (oral)", "Wks 1–6", "Kick-start strength + size"],
        ["Testosterone Cypionate*", "Test C", "500–750 mg", "Weekly (alt.)", "12–16 wks", "Alternative to Test E"],
    ]
    headers = ["Compound", "Name", "Dose", "Frequency", "Duration", "Role"]
    cw = [(W - 72) * f for f in [0.22, 0.10, 0.13, 0.16, 0.12, 0.27]]
    items.append(build_table(headers, rows, TK, cw))
    items.append(Paragraph("* Test C and Test E are interchangeable. Choose one based on availability.", styles["disclaimer"]))

    # 3. Schedule
    items += section_header("3. 12–16 WEEK DOSAGE PROTOCOL", TK, styles, "📅")
    sched_rows = [
        ["1–2", "500 mg", "400 mg", "30 mg/day", "Ramp up — establish base"],
        ["3–4", "500 mg", "400 mg", "40 mg/day", "Building momentum"],
        ["5–6", "750 mg", "600 mg", "50 mg/day", "Peak loading phase"],
        ["7–8", "750 mg", "600 mg", "—", "Mid-cycle — assess gains"],
        ["9–10", "750 mg", "600 mg", "—", "Continued mass building"],
        ["11–12", "750 mg", "600 mg", "—", "Peak anabolic phase"],
        ["13–14*", "500 mg", "400 mg", "—", "Taper down (16-wk option)"],
        ["15–16*", "500 mg", "—", "—", "Pre-PCT clearance"],
    ]
    sched_headers = ["Weeks", "Test E/C", "Deca", "Dbol", "Notes"]
    cw2 = [(W - 72) * f for f in [0.10, 0.15, 0.12, 0.14, 0.49]]
    items.append(build_table(sched_headers, sched_rows, TK, cw2))
    items.append(Paragraph("* Weeks 13–16 are optional extension — only if running 16-week protocol.", styles["disclaimer"]))

    # 4. Peptides
    items += section_header("4. PEPTIDE PROTOCOL", TK, styles, "🧬")
    items.append(Paragraph(
        "Peptides work synergistically with the anabolic stack by stimulating <b>natural GH release</b> "
        "from the pituitary gland. They enhance recovery, increase GH pulsatility, and improve body "
        "composition beyond what steroids alone can achieve.",
        styles["body"]
    ))
    pep_rows = [
        ["IGF-1 LR3", "40–60 mcg/day", "Post-workout (IM)", "4–6 wks on, 4 wks off", "Muscle cell proliferation, nutrient partitioning"],
        ["GHRP-6", "100 mcg × 3/day", "SC injection", "Throughout cycle", "GH pulse trigger, appetite stimulation"],
        ["CJC-1295 DAC", "2 mg/week", "SC (once weekly)", "Weeks 1–12", "Sustained GH elevation (GHRP amplifier)"],
    ]
    pep_headers = ["Peptide", "Dose", "Route", "Timing", "Function"]
    cw3 = [(W - 72) * f for f in [0.16, 0.14, 0.13, 0.20, 0.37]]
    items.append(build_table(pep_headers, pep_rows, TK, cw3))
    items.append(Paragraph("<b>GHRP-6 injection timing:</b>", styles["subsection"]))
    for item in [
        "Injection 1: Morning (fasted, 30 min before breakfast)",
        "Injection 2: Pre-workout (60 min before training)",
        "Injection 3: Before bed (2+ hours after last meal for max GH pulse)",
        "Always inject GHRP-6 + CJC-1295 together for synergistic effect",
    ]:
        items.append(bullet_item(item, styles))

    items.append(PageBreak())

    # 5. HGH
    items += section_header("5. OPTIONAL HGH ADDITION", TK, styles, "⚡")
    items.append(Paragraph(
        "Human Growth Hormone (HGH) can be added for elite-level results. It significantly enhances "
        "the peptide stack and adds recovery, fat loss, and anti-aging benefits.",
        styles["body"]
    ))
    for item in [
        "<b>Dose:</b> 2–4 IU/day (beginners start at 2 IU; advanced users 4 IU)",
        "<b>Timing:</b> Morning injection (fasted) OR split into 2 × daily doses",
        "<b>Duration:</b> 12–24 weeks (HGH benefits compound over time)",
        "<b>Cost consideration:</b> Pharmaceutical-grade HGH is expensive — budget accordingly",
        "<b>Monitoring:</b> Check IGF-1 levels every 6 weeks; target 250–350 ng/mL",
    ]:
        items.append(bullet_item(item, styles))

    # 6. AI & Prolactin
    items += section_header("6. AI & PROLACTIN CONTROL", TK, styles, "🛡")
    for item in [
        "<b>Arimidex (Anastrozole):</b> 0.5 mg twice weekly (adjust based on E2 blood work)",
        "<b>Cabergoline (Caber):</b> 0.25 mg twice weekly — critical with Deca due to high prolactin risk",
        "Deca/Nandrolone is a 19-nor compound — prolactin control is NON-NEGOTIABLE",
        "Target E2 for bulking: 35–50 pg/mL (slightly higher than cutting for IGF-1/GH synergy)",
        "Do NOT over-suppress estrogen — it impairs muscle growth and joint health",
    ]:
        items.append(bullet_item(item, styles))

    # 7. PCT
    items += section_header("7. POST CYCLE THERAPY (PCT)", TK, styles, "🔄")
    items.append(Paragraph(
        "<b>IMPORTANT:</b> Due to Deca's long half-life, begin PCT <b>3–4 weeks</b> after your last "
        "Deca injection. Test E/C requires 2 weeks clearance.",
        styles["body"]
    ))
    pct_rows = [
        ["HCG", "1000 IU", "Every 3 days", "Wks 1–3 of PCT", "Testicular restart"],
        ["Clomid", "100 mg/day → 50 mg", "Daily", "Wks 1–4 of PCT", "LH stimulation"],
        ["Nolvadex", "40 mg/day → 20 mg", "Daily", "Wks 1–6 of PCT", "Anti-estrogen SERM"],
        ["Vitamin E", "400 IU/day", "Daily", "Throughout PCT", "Antioxidant + fertility"],
    ]
    pct_headers = ["Compound", "Dose", "Frequency", "Duration", "Role"]
    cw4 = [(W - 72) * f for f in [0.17, 0.17, 0.14, 0.17, 0.35]]
    items.append(build_table(pct_headers, pct_rows, TK, cw4))

    # 8. Supplements
    items += section_header("8. ESSENTIAL SUPPLEMENT STACK", TK, styles, "💊")
    supp_data = {
        "Liver Protection": ["TUDCA — 500 mg/day", "Milk Thistle (Silymarin) — 600 mg/day", "NAC (N-Acetyl Cysteine) — 600 mg/day"],
        "Cardiovascular": ["Omega-3 Fish Oil — 4–6 g/day", "CoQ10 — 200 mg/day", "Red Yeast Rice — 1200 mg/day", "Hawthorn Berry — 500 mg 2×/day"],
        "Performance & Recovery": ["Creatine Monohydrate — 5 g/day", "Beta-Alanine — 3.2 g/day", "Whey/Casein Protein — 50–80 g/day", "BCAAs — 10 g intra-workout"],
        "Hormonal & General": ["ZMA — nightly", "Vitamin D3 5000 IU + K2 100 mcg", "High-potency Multivitamin", "Glucosamine + Chondroitin (joint health)"],
    }
    for cat, supps in supp_data.items():
        items.append(Paragraph(f"<b>{cat}:</b>", styles["subsection"]))
        for s in supps:
            items.append(bullet_item(s, styles))

    # 9. Nutrition
    items += section_header("9. MASS-BUILDING NUTRITION PLAN", TK, styles, "🍽")
    for item in [
        "<b>Caloric surplus:</b> +400–600 kcal above TDEE (calculated individually)",
        "<b>Protein:</b> 1.8–2.2 g/lb body weight (minimum 250 g/day for 180 lb athlete)",
        "<b>Carbohydrates:</b> 3–4 g/lb body weight — prioritize around training",
        "<b>Fats:</b> 0.5–0.8 g/lb body weight (essential fatty acids focus)",
        "<b>Meal frequency:</b> 5–7 meals per day for sustained anabolic environment",
        "<b>Pre-workout meal:</b> Complex carbs + protein 2 hours before training",
        "<b>Post-workout:</b> Fast protein + simple carbs within 30 minutes of training",
        "<b>Night meal:</b> Slow-digesting protein (casein) + healthy fats",
    ]:
        items.append(bullet_item(item, styles))

    # 10. Training
    items += section_header("10. TRAINING PROGRAMMING", TK, styles, "🏋")
    for item in [
        "<b>Frequency:</b> 5–6 days/week (Upper/Lower or PPL split)",
        "<b>Volume:</b> 15–20 sets per muscle group per week",
        "<b>Rep ranges:</b> 6–12 for hypertrophy; include heavy 3–5 rep sets for strength",
        "<b>Progressive overload:</b> Aim to add weight or reps every week",
        "<b>Cardio:</b> Limit to 20–30 min LISS 3×/week during mass phase",
        "<b>Sleep:</b> CRITICAL — minimum 8–9 hours for maximum GH release and recovery",
    ]:
        items.append(bullet_item(item, styles))

    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "⚠  This guide is for educational purposes only. AMAN TRAINING CLUB does not endorse illegal "
        "activity. Consult a licensed physician before beginning any hormonal protocol.",
        styles["disclaimer"]
    ))

    doc.build(items,
              onFirstPage=make_page_bg(TK, is_cover=True),
              onLaterPages=make_page_bg(TK, is_cover=False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
#  PDF 3 — BEGINNER STEROID CYCLE
# ════════════════════════════════════════════════════════════
def generate_beginner_pdf(path):
    TK = "beginner"
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=28, bottomMargin=28
    )
    styles = make_styles(TK)
    items = []

    items += build_cover(
        title_lines=["BEGINNER ANABOLIC", "STEROID CYCLE", "FULL GUIDE"],
        subtitle="8–12 Week Foundation Protocol — Safe, Simple & Effective",
        edition="AMAN TRAINING CLUB  •  Beginner Series  •  2024 Edition",
        theme_key=TK, styles=styles,
        badge_texts=["8–12 WEEKS", "BEGINNER FRIENDLY", "SIMPLE PROTOCOL", "FULL PCT"],
        disclaimer_text=(
            "⚠  MEDICAL DISCLAIMER: For educational purposes only. Always consult a licensed physician "
            "before beginning any hormonal protocol. Anabolic steroids are controlled in many countries."
        )
    )

    # TOC
    items += section_header("TABLE OF CONTENTS", TK, styles, "📋")
    for item in [
        "1.  Why Testosterone Only — The Golden Rule",
        "2.  Core Compound: Testosterone Enanthate/Cypionate",
        "3.  Optional Kick-Starter: Dianabol (Weeks 1–6)",
        "4.  8 vs 12 Week Protocol",
        "5.  Aromatase Inhibitor (AI) — Do You Need One?",
        "6.  Post Cycle Therapy (PCT) — The Most Important Part",
        "7.  Essential Supplement Stack",
        "8.  Beginner Training Program",
        "9.  Beginner Nutrition Guide",
        "10. Side Effects — What to Watch For",
    ]:
        items.append(Paragraph(item, styles["toc_item"]))
    items.append(PageBreak())

    # 1. Why Test Only
    items += section_header("1. WHY TESTOSTERONE ONLY — THE GOLDEN RULE", TK, styles, "📖")
    items.append(Paragraph(
        "Every beginner's first cycle should be <b>Testosterone only</b>. This is the most important "
        "rule in bodybuilding pharmacology. Here's why:",
        styles["body"]
    ))
    for item in [
        "Testosterone is the base of ALL steroid cycles — your body already makes it",
        "If side effects occur, you know EXACTLY which compound caused them",
        "Beginners respond incredibly well to testosterone alone — no need to complicate it",
        "Adding multiple compounds before knowing your individual response is dangerous",
        "Test-only cycles are predictable, manageable, and reversible with proper PCT",
        "Expect 15–25 lbs of lean mass on a first Test cycle (with proper training + diet)",
    ]:
        items.append(bullet_item(item, styles))

    # 2. Core Compound
    items += section_header("2. CORE COMPOUND", TK, styles, "💊")
    comp_rows = [
        ["Testosterone Enanthate", "Test E", "300–500 mg", "2 × weekly (Monday/Thursday)", "8–12 weeks"],
        ["Testosterone Cypionate", "Test C", "300–500 mg", "2 × weekly (alternative)", "8–12 weeks"],
    ]
    headers = ["Compound", "Short Name", "Weekly Dose", "Injection Schedule", "Duration"]
    cw = [(W - 72) * f for f in [0.25, 0.12, 0.14, 0.30, 0.19]]
    items.append(build_table(headers, comp_rows, TK, cw))
    items.append(Spacer(1, 4))
    items.append(Paragraph("<b>Dosage recommendation by experience level:</b>", styles["subsection"]))
    dose_rows = [
        ["True Beginner (1st cycle)", "300 mg/week", "Minimal side effects, excellent gains"],
        ["Intermediate Beginner (2nd cycle)", "400 mg/week", "Balanced risk/reward ratio"],
        ["Advanced Beginner (3rd+ cycle)", "500 mg/week", "Maximum beginner gains"],
    ]
    dose_headers = ["Experience Level", "Recommended Dose", "Notes"]
    cw2 = [(W - 72) * f for f in [0.32, 0.22, 0.46]]
    items.append(build_table(dose_headers, dose_rows, TK, cw2))

    # 3. Dbol kick-start
    items += section_header("3. OPTIONAL KICK-STARTER: DIANABOL (WEEKS 1–6)", TK, styles, "⚡")
    items.append(Paragraph(
        "<b>Dianabol</b> can be added to accelerate early gains while Test E/C builds up in your system "
        "(long esters take 3–4 weeks to reach peak blood levels). This is optional — not required.",
        styles["body"]
    ))
    for item in [
        "<b>Dose:</b> 20–30 mg/day (split into 2–3 doses with meals)",
        "<b>Duration:</b> Weeks 1–6 only",
        "Expect rapid weight gain (5–10 lbs in 2–3 weeks) — mostly water + muscle",
        "Water retention will drop after stopping Dbol — this is normal",
        "Increase AI dose during Dbol weeks due to higher aromatization",
        "Requires liver support: TUDCA 500 mg/day throughout Dbol use",
        "<b>Not recommended for true first-timers</b> — run Test only first",
    ]:
        items.append(bullet_item(item, styles))

    # 4. 8 vs 12 weeks
    items += section_header("4. 8 WEEK vs 12 WEEK PROTOCOL", TK, styles, "📅")
    wk_rows = [
        ["8 Weeks", "300–400 mg Test E/C + optional Dbol wks 1–4", "Shorter recovery, less suppression, ideal for 1st cycle"],
        ["10 Weeks", "400–500 mg Test E/C + optional Dbol wks 1–6", "Good balance — recommended for most beginners"],
        ["12 Weeks", "400–500 mg Test E/C + optional Dbol wks 1–6", "Maximum gains, longer recovery needed post-cycle"],
    ]
    wk_headers = ["Protocol", "Stack", "Notes"]
    cw3 = [(W - 72) * f for f in [0.14, 0.42, 0.44]]
    items.append(build_table(wk_headers, wk_rows, TK, cw3))

    items.append(PageBreak())

    # 5. AI
    items += section_header("5. AROMATASE INHIBITOR (AI)", TK, styles, "🛡")
    items.append(Paragraph(
        "Testosterone converts to estrogen via aromatase. <b>Some estrogen is necessary</b> for "
        "muscle growth, mood, and libido. The goal is to <b>keep estrogen in range — not eliminate it</b>.",
        styles["body"]
    ))
    items.append(Paragraph("<b>Option A: Arimidex (Anastrozole) — Recommended</b>", styles["subsection"]))
    for item in [
        "0.5 mg every other day (EOD) as a starting dose",
        "Reduce to 0.25 mg EOD if experiencing low-estrogen symptoms (joint pain, low libido, low mood)",
        "Available as pill; exact dosing is easy",
    ]:
        items.append(bullet_item(item, styles))
    items.append(Paragraph("<b>Option B: Aromasin (Exemestane)</b>", styles["subsection"]))
    for item in [
        "12.5–25 mg every other day",
        "Suicidal AI — permanently deactivates aromatase enzyme (more difficult to titrate)",
        "Better choice for men prone to high estrogen",
    ]:
        items.append(bullet_item(item, styles))
    items.append(Paragraph("<b>Signs of HIGH estrogen:</b> Water retention, gynecomastia (puffy/sensitive nipples), mood swings, high blood pressure", styles["body"]))
    items.append(Paragraph("<b>Signs of LOW estrogen:</b> Joint pain, low libido, depression, fatigue, poor erections", styles["body"]))

    # 6. PCT
    items += section_header("6. POST CYCLE THERAPY (PCT)", TK, styles, "🔄")
    items.append(Paragraph(
        "<b>PCT is non-negotiable.</b> Starting PCT at the wrong time is a common mistake. "
        "For Test Enanthate/Cypionate (long esters): Begin PCT <b>14–18 days</b> after your last injection.",
        styles["body"]
    ))
    pct_rows = [
        ["Clomid (Clomiphene Citrate)", "50 mg/day", "Weeks 1–3 of PCT", "Primary LH/FSH stimulator"],
        ["Nolvadex (Tamoxifen Citrate)", "20 mg/day", "Weeks 1–4 of PCT", "Anti-estrogen, SERM"],
        ["HCG (optional but recommended)", "500 IU EOD", "2 weeks BEFORE PCT", "Testicular size recovery"],
    ]
    pct_headers = ["Compound", "Dose", "Timing", "Purpose"]
    cw4 = [(W - 72) * f for f in [0.30, 0.14, 0.22, 0.34]]
    items.append(build_table(pct_headers, pct_rows, TK, cw4))
    items.append(Paragraph(
        "After PCT, get blood work (testosterone, LH, FSH, E2). If levels have recovered to normal "
        "range, PCT is complete. If suppressed, consult a doctor (TRT may be needed in rare cases).",
        styles["body"]
    ))

    # 7. Supplements
    items += section_header("7. ESSENTIAL SUPPLEMENT STACK", TK, styles, "💊")
    for item in [
        "<b>Milk Thistle / TUDCA:</b> 500–800 mg/day for liver protection (especially with Dbol)",
        "<b>Omega-3 Fish Oil:</b> 3–4 g/day for cholesterol management and cardiovascular health",
        "<b>Vitamin D3 + K2:</b> 5000 IU D3 + 100 mcg K2 daily",
        "<b>Zinc + Magnesium (ZMA):</b> Nightly — supports testosterone production in PCT",
        "<b>Creatine Monohydrate:</b> 5 g/day — amplifies strength and muscle gains",
        "<b>Multivitamin:</b> High-quality daily multivitamin",
        "<b>Whey Protein:</b> To hit protein targets (minimum 1 g/lb body weight)",
        "<b>Blood pressure monitor:</b> Check BP twice weekly — AAS can raise BP",
    ]:
        items.append(bullet_item(item, styles))

    # 8. Training
    items += section_header("8. BEGINNER TRAINING PROGRAM", TK, styles, "🏋")
    items.append(Paragraph("<b>Recommended splits for beginners on cycle:</b>", styles["subsection"]))
    training_rows = [
        ["Monday", "Chest + Triceps", "Bench Press, Incline DB Press, Cable Flyes, Tricep Dips"],
        ["Tuesday", "Back + Biceps", "Deadlifts, Pull-Ups, Barbell Rows, Bicep Curls"],
        ["Wednesday", "REST / Light Cardio", "30 min walk or LISS cardio"],
        ["Thursday", "Shoulders", "OHP, Lateral Raises, Front Raises, Face Pulls"],
        ["Friday", "Legs", "Squats, Leg Press, Romanian Deadlift, Calf Raises"],
        ["Saturday", "Arms + Abs", "Isolation work, Core circuit"],
        ["Sunday", "REST", "Active recovery, stretching"],
    ]
    t_headers = ["Day", "Focus", "Key Exercises"]
    cw5 = [(W - 72) * f for f in [0.14, 0.20, 0.66]]
    items.append(build_table(t_headers, training_rows, TK, cw5))

    # 9. Nutrition
    items += section_header("9. BEGINNER NUTRITION GUIDE", TK, styles, "🍽")
    for item in [
        "<b>Find your TDEE</b> (Total Daily Energy Expenditure) using an online calculator",
        "<b>Bulking:</b> Eat +300–400 kcal above TDEE for lean gaining",
        "<b>Protein:</b> Minimum 1 g/lb body weight (higher = better, up to 2 g/lb)",
        "<b>Carbohydrates:</b> Rice, oats, potatoes, fruits — complex carbs are your energy source",
        "<b>Fats:</b> Eggs, olive oil, avocado, nuts — don't go below 0.3 g/lb body weight",
        "<b>Water:</b> 3–4 litres minimum daily",
        "<b>Meal timing:</b> Pre-workout meal (2 hrs before) + post-workout meal (within 1 hr after)",
    ]:
        items.append(bullet_item(item, styles))

    # 10. Side Effects
    items += section_header("10. SIDE EFFECTS — WHAT TO WATCH FOR", TK, styles, "⚠")
    se_rows = [
        ["Acne (back/shoulders)", "Common", "Good hygiene, salicylic acid wash, reduce dose"],
        ["Hair loss/thinning", "Genetic", "Finasteride or Nizoral shampoo; accept risk if predisposed"],
        ["Water retention", "Common", "Reduce sodium, manage AI dose, drink more water"],
        ["Gynecomastia", "Manageable", "Start Nolvadex 20 mg/day immediately; add AI"],
        ["High blood pressure", "Monitor", "Monitor BP; reduce dose; add Hawthorn Berry supplement"],
        ["Testicular atrophy", "Expected", "Normal on cycle; HCG prevents it; reverses post-PCT"],
        ["Mood changes/aggression", "Possible", "Usually dose-dependent; communicate with people close to you"],
        ["Libido changes", "Common", "Often improves ON cycle; may dip during PCT — temporary"],
    ]
    se_headers = ["Side Effect", "Likelihood", "Management"]
    cw6 = [(W - 72) * f for f in [0.26, 0.14, 0.60]]
    items.append(build_table(se_headers, se_rows, TK, cw6))

    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "⚠  Educational purposes only. AMAN TRAINING CLUB does not endorse illegal use of anabolic "
        "steroids. Consult a licensed physician before beginning any hormonal protocol.",
        styles["disclaimer"]
    ))

    doc.build(items,
              onFirstPage=make_page_bg(TK, is_cover=True),
              onLaterPages=make_page_bg(TK, is_cover=False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
#  PDF 4 — 30-DAY KETO INDIAN VEGETARIAN PLAN
# ════════════════════════════════════════════════════════════
def generate_keto_pdf(path):
    TK = "keto"
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=28, bottomMargin=28
    )
    styles = make_styles(TK)
    items = []

    items += build_cover(
        title_lines=["30-DAY WEIGHT LOSS", "TRANSFORMATION PLAN"],
        subtitle="Keto Indian Vegetarian Diet — Week-by-Week Protocol with Recipes",
        edition="AMAN TRAINING CLUB  •  Nutrition Series  •  2024 Edition",
        theme_key=TK, styles=styles,
        badge_texts=["30 DAYS", "VEGETARIAN", "KETO FRIENDLY", "6 RECIPES INCLUDED"],
        disclaimer_text=None
    )

    # TOC
    items += section_header("TABLE OF CONTENTS", TK, styles, "📋")
    for item in [
        "1.  What is Ketogenic Diet — Indian Vegetarian Approach",
        "2.  Week 1: Transition Phase (Days 1–7)",
        "3.  Week 2: Entering Ketosis (Days 8–14)",
        "4.  Week 3: Deep Ketosis (Days 15–21)",
        "5.  Week 4: Maintenance & Long-Term Habits (Days 22–30)",
        "6.  Full Recipe Guide (6 Recipes)",
        "7.  Exercise Protocol",
        "8.  Keto Tips for Indian Vegetarians",
        "9.  Foods to Eat & Avoid",
        "10. Expected Results & What to Track",
    ]:
        items.append(Paragraph(item, styles["toc_item"]))
    items.append(PageBreak())

    # 1. Introduction
    items += section_header("1. KETO DIET — INDIAN VEGETARIAN APPROACH", TK, styles, "🌿")
    items.append(Paragraph(
        "The <b>Ketogenic diet</b> is a high-fat, moderate-protein, very-low-carbohydrate eating plan "
        "that shifts your body's primary fuel source from glucose to <b>ketones</b> (produced from fat). "
        "This 30-day plan is specifically designed for <b>Indian vegetarians</b>, using familiar ingredients "
        "and traditional recipes adapted for ketogenic macros.",
        styles["body"]
    ))
    items.append(Paragraph("<b>Key Macronutrient Targets:</b>", styles["subsection"]))
    macro_rows = [
        ["Fats", "65–75%", "Paneer, ghee, coconut oil, nuts, seeds, avocado"],
        ["Protein", "20–25%", "Paneer, tofu, eggs (if lacto-ovo), Greek yogurt, dal (limited)"],
        ["Carbohydrates", "5–10%", "Green vegetables ONLY — keep net carbs under 20–25 g/day"],
    ]
    macro_headers = ["Macro", "% of Calories", "Indian Vegetarian Sources"]
    cw = [(W - 72) * f for f in [0.15, 0.16, 0.69]]
    items.append(build_table(macro_headers, macro_rows, TK, cw))
    items.append(Paragraph(
        "Indian vegetarian keto requires replacing rice, roti, and lentils (high-carb staples) with "
        "cauliflower rice, almond flour rotis, paneer, and healthy oils.",
        styles["body"]
    ))

    # 2. Week 1
    items += section_header("2. WEEK 1: TRANSITION PHASE (DAYS 1–7)", TK, styles, "🌅")
    items.append(Paragraph(
        "<b>Goal:</b> Gradually reduce carbohydrates to 50 g/day (not zero immediately — avoid keto flu shock). "
        "Your body is adapting — expect some fatigue and cravings in days 3–5. This is normal.",
        styles["body"]
    ))
    w1_rows = [
        ["Day 1–2", "Breakfast", "Paneer Bhurji (scrambled paneer with vegetables) + masala chai with almond milk"],
        ["Day 1–2", "Lunch", "Palak Paneer + 1 small Almond Flour Roti"],
        ["Day 1–2", "Dinner", "Cauliflower Rice + Mushroom Curry + salad"],
        ["Day 3–4", "Breakfast", "Methi Thepla (almond flour, methi, ghee) + low-carb pickle"],
        ["Day 3–4", "Lunch", "Tofu Stir-Fry with coconut oil + zucchini noodles"],
        ["Day 3–4", "Dinner", "Egg Curry (or Paneer Curry) + cauliflower mash"],
        ["Day 5–7", "Breakfast", "Avocado toast on almond bread + green tea"],
        ["Day 5–7", "Lunch", "Broccoli + Paneer sabzi with ghee tadka"],
        ["Day 5–7", "Dinner", "Spinach soup + grilled paneer tikka"],
    ]
    w1_headers = ["Days", "Meal", "Menu"]
    cw1 = [(W - 72) * f for f in [0.12, 0.12, 0.76]]
    items.append(build_table(w1_headers, w1_rows, TK, cw1))
    items.append(Paragraph("<b>Week 1 Snacks:</b> Handful of almonds/walnuts, paneer cubes with chaat masala, cucumber with coconut chutney", styles["body"]))

    # 3. Week 2
    items += section_header("3. WEEK 2: ENTERING KETOSIS (DAYS 8–14)", TK, styles, "🔥")
    items.append(Paragraph(
        "<b>Goal:</b> Reduce net carbs to 20–25 g/day. By day 10–12, most people enter ketosis. "
        "Signs: sweet/fruity breath, mental clarity, reduced hunger, increased energy.",
        styles["body"]
    ))
    w2_rows = [
        ["Day 8–10", "Breakfast", "Keto Masala Omelette (3 eggs / paneer, veggies, spices, ghee)"],
        ["Day 8–10", "Lunch", "Palak Paneer (no onion gravy) + cauliflower rice"],
        ["Day 8–10", "Dinner", "Zucchini noodles + Avocado-Coconut cream sauce + roasted paneer"],
        ["Day 11–14", "Breakfast", "Chia seed pudding with coconut milk + 10 almonds"],
        ["Day 11–14", "Lunch", "Mixed veg stir-fry (broccoli, capsicum, mushroom) in coconut oil"],
        ["Day 11–14", "Dinner", "Paneer Tikka (grilled, no cream sauce) + mint chutney + salad"],
    ]
    w2_headers = ["Days", "Meal", "Menu"]
    items.append(build_table(w2_headers, w2_rows, TK, cw1))
    items.append(Paragraph("<b>Ketosis testing:</b> Use urine ketone strips (Ketostix) or blood ketone meter. Target: 0.5–3.0 mmol/L", styles["body"]))

    items.append(PageBreak())

    # 4. Week 3
    items += section_header("4. WEEK 3: DEEP KETOSIS (DAYS 15–21)", TK, styles, "⚡")
    items.append(Paragraph(
        "<b>Goal:</b> Maintain 20 g net carbs/day. By now you are fat-adapted. Energy is stable, "
        "hunger is reduced, and fat loss should be clearly visible. This is the most productive week.",
        styles["body"]
    ))
    w3_rows = [
        ["Day 15–17", "Breakfast", "Almond Flour Paratha with ghee + paneer filling"],
        ["Day 15–17", "Lunch", "Paneer Tikka Masala (low-carb gravy) + broccoli"],
        ["Day 15–17", "Dinner", "Egg drop soup / Paneer soup + roasted seeds"],
        ["Day 18–21", "Breakfast", "Coconut milk smoothie (spinach, protein, coconut cream, seeds)"],
        ["Day 18–21", "Lunch", "Methi Paneer Bhurji + cucumber salad with olive oil dressing"],
        ["Day 18–21", "Dinner", "Baked stuffed capsicum (paneer, herbs, cheese)"],
    ]
    w3_headers = ["Days", "Meal", "Menu"]
    items.append(build_table(w3_headers, w3_rows, TK, cw1))

    # 5. Week 4
    items += section_header("5. WEEK 4: MAINTENANCE (DAYS 22–30)", TK, styles, "🌟")
    items.append(Paragraph(
        "<b>Goal:</b> Solidify keto eating habits. You can slightly increase carbs (25–30 g/day) "
        "to find your personal carb threshold. Focus on long-term sustainability.",
        styles["body"]
    ))
    w4_rows = [
        ["Day 22–25", "Breakfast", "Keto Upma (cauliflower + mustard seeds + curry leaves + ghee)"],
        ["Day 22–25", "Lunch", "Dal Makhani (limited quantity, 50 g black lentils) + salad"],
        ["Day 22–25", "Dinner", "Stuffed Bell Peppers with paneer, herbs, cheese filling"],
        ["Day 26–30", "Breakfast", "Smoothie bowl: coconut yogurt + nuts + seeds + berries (½ cup)"],
        ["Day 26–30", "Lunch", "Paneer steak with sautéed spinach + ghee drizzle"],
        ["Day 26–30", "Dinner", "Green vegetable soup + almond flour bread + nut butter"],
    ]
    w4_headers = ["Days", "Meal", "Menu"]
    items.append(build_table(w4_headers, w4_rows, TK, cw1))

    # 6. Recipes
    items += section_header("6. FULL RECIPE GUIDE", TK, styles, "📖")

    recipes = [
        {
            "name": "PANEER BHURJI",
            "time": "Prep: 5 min  •  Cook: 10 min  •  Serves: 2",
            "ingredients": [
                "200 g fresh paneer, crumbled",
                "1 tbsp ghee or coconut oil",
                "½ tsp cumin seeds",
                "½ onion, finely chopped (optional — omit for strict keto)",
                "1 green chilli, finely chopped",
                "½ cup capsicum (bell pepper), diced",
                "Salt, turmeric, coriander powder to taste",
                "Fresh coriander leaves for garnish",
            ],
            "method": [
                "Heat ghee in a pan; add cumin seeds until they splutter",
                "Add green chilli and capsicum; sauté 2 minutes",
                "Add crumbled paneer; mix gently",
                "Season with salt, turmeric, coriander powder",
                "Cook on medium heat for 5 minutes, stirring occasionally",
                "Garnish with fresh coriander; serve hot",
            ],
            "macros": "Calories: ~320 kcal  •  Protein: 22g  •  Fat: 24g  •  Net Carbs: 4g",
        },
        {
            "name": "CAULIFLOWER RICE + MUSHROOM CURRY",
            "time": "Prep: 10 min  •  Cook: 20 min  •  Serves: 2",
            "ingredients": [
                "1 large cauliflower head, grated / pulsed in food processor",
                "250 g mushrooms (button or oyster), sliced",
                "2 tbsp coconut oil",
                "1 cup coconut cream",
                "1 tsp each: cumin, coriander, turmeric, garam masala",
                "2 garlic cloves + 1 inch ginger (paste)",
                "Salt and fresh coriander to taste",
            ],
            "method": [
                "Cauliflower rice: Sauté grated cauliflower in 1 tbsp oil, 5 min. Season with salt. Set aside.",
                "Mushroom curry: Heat 1 tbsp oil; add garlic-ginger paste and fry 1 min",
                "Add spices; stir 30 sec, then add mushrooms",
                "Cook mushrooms until golden (5–7 min)",
                "Add coconut cream; simmer 5 min until sauce thickens",
                "Serve mushroom curry over cauliflower rice",
            ],
            "macros": "Calories: ~380 kcal  •  Protein: 10g  •  Fat: 34g  •  Net Carbs: 8g",
        },
        {
            "name": "KETO ALMOND FLOUR PARATHA",
            "time": "Prep: 10 min  •  Cook: 15 min  •  Makes: 4 parathas",
            "ingredients": [
                "1 cup almond flour (blanched)",
                "2 tbsp psyllium husk (binds the dough)",
                "1 tbsp ghee + extra for cooking",
                "½ tsp ajwain (carom seeds)",
                "Salt to taste",
                "4–5 tbsp warm water (adjust for dough consistency)",
            ],
            "method": [
                "Mix almond flour, psyllium husk, ajwain, and salt in a bowl",
                "Add ghee and mix until crumbly",
                "Add warm water gradually — form soft, pliable dough",
                "Divide into 4 balls; roll between two parchment sheets (prevents sticking)",
                "Cook on medium tawa (griddle) with ghee, 2 min per side until golden",
                "Serve with butter, cream cheese, or low-carb paneer filling",
            ],
            "macros": "Calories: ~210 kcal  •  Protein: 6g  •  Fat: 18g  •  Net Carbs: 3g (per paratha)",
        },
    ]
    for recipe in recipes:
        items.append(KeepTogether([
            Paragraph(f"● {recipe['name']}", styles["subsection"]),
            Paragraph(recipe["time"], styles["disclaimer"]),
            Paragraph("<b>Ingredients:</b>", styles["body"]),
        ] + [bullet_item(i, styles) for i in recipe["ingredients"]] + [
            Paragraph("<b>Method:</b>", styles["body"]),
        ] + [bullet_item(f"Step {n+1}: {s}", styles) for n, s in enumerate(recipe["method"])] + [
            Paragraph(f"<b>Macros per serving:</b>  {recipe['macros']}", styles["body"]),
            Spacer(1, 4),
        ]))

    items.append(PageBreak())

    # 3 more recipes in table format for brevity
    items += section_header("ADDITIONAL RECIPES", TK, styles, "🍳")
    simple_recipes = [
        ["Zucchini Noodles + Avocado Sauce", "2 medium zucchini (spiralized), 1 ripe avocado, 2 tbsp olive oil, lemon juice, garlic, salt, pepper. Blend avocado with oil, lemon, garlic to make sauce. Toss with raw or lightly sautéed zucchini noodles. Serve immediately.", "280 kcal | 6g protein | 26g fat | 5g net carbs"],
        ["Paneer Tikka", "200g paneer cubes, 3 tbsp thick yogurt (or coconut yogurt), 1 tsp each: cumin, coriander, garam masala, chilli powder. Marinate paneer 2+ hrs. Grill or air-fry at 200°C for 12–15 min until charred. Serve with mint chutney.", "340 kcal | 24g protein | 26g fat | 4g net carbs"],
        ["Keto Upma", "2 cups cauliflower, grated fine. 1 tsp mustard seeds, curry leaves, 1 tbsp ghee, green chilli, ginger, salt. Heat ghee, splutter mustard seeds, add curry leaves, chilli, ginger. Add cauliflower, stir-fry 8–10 min until cooked. Season and garnish with coriander.", "190 kcal | 7g protein | 15g fat | 5g net carbs"],
    ]
    sr_headers = ["Recipe", "Quick Method", "Macros (per serving)"]
    cw_sr = [(W - 72) * f for f in [0.22, 0.54, 0.24]]
    items.append(build_table(sr_headers, simple_recipes, TK, cw_sr))

    # 7. Exercise
    items += section_header("7. EXERCISE PROTOCOL", TK, styles, "🏃")
    ex_rows = [
        ["Cardio (Fat Burning)", "3–4×/week", "30–40 min brisk walking, cycling, swimming, or LISS (low intensity steady state)"],
        ["Strength Training", "3×/week", "Bodyweight or gym: squats, push-ups, lunges, planks, resistance bands"],
        ["Yoga / Flexibility", "Daily", "20–30 min morning yoga — improves cortisol levels and aids fat loss"],
        ["Rest Days", "1–2×/week", "Complete rest or light stretching; sleep 7–9 hours"],
    ]
    ex_headers = ["Type", "Frequency", "Details"]
    cw_ex = [(W - 72) * f for f in [0.22, 0.14, 0.64]]
    items.append(build_table(ex_headers, ex_rows, TK, cw_ex))

    # 8. Tips
    items += section_header("8. KETO TIPS FOR INDIAN VEGETARIANS", TK, styles, "💡")
    for tip in [
        "<b>Electrolytes are critical:</b> Keto flushes water (and electrolytes) rapidly. Supplement sodium, potassium, and magnesium daily",
        "<b>Replace dal/rice with paneer:</b> Dal is high-carb; use paneer and tofu as your main protein sources",
        "<b>Cook with ghee and coconut oil:</b> These are your best keto-friendly Indian cooking fats",
        "<b>Use almond flour and coconut flour:</b> Replace wheat atta for chapati, pancakes, and baked goods",
        "<b>Cauliflower is your best friend:</b> Cauliflower rice, cauliflower upma, cauliflower biryani — it replaces rice perfectly",
        "<b>Read labels carefully:</b> Indian packaged foods often hide sugar — check everything",
        "<b>Eat mindfully, not just macros:</b> Stress management and sleep quality matter as much as diet",
    ]:
        items.append(bullet_item(tip, styles))

    # 9. Foods
    items += section_header("9. FOODS TO EAT & AVOID", TK, styles, "🥗")
    food_rows = [
        ["✅ EAT FREELY", "Paneer, tofu, eggs, ghee, coconut oil, olive oil, butter, cream", "Leafy greens (spinach, methi, palak), broccoli, cauliflower, zucchini, capsicum, mushrooms", "Almonds, walnuts, flaxseeds, chia seeds, pumpkin seeds"],
        ["⚠️ EAT IN MODERATION", "Full-fat yogurt, cheese, heavy cream", "Onion, tomato (small amounts), lemon, berries (50g max)", "Cashews (higher carb nut — limit to 10/day)"],
        ["❌ AVOID COMPLETELY", "Rice, wheat roti/naan, bread, pasta, all grains", "Dal/lentils, chickpeas, rajma (all legumes are high-carb)", "Sugar, jaggery, honey, all sweets, fruit juices, soda"],
    ]
    food_headers = ["Category", "Protein/Fats", "Vegetables/Fruits", "Nuts/Seeds"]
    cw_f = [(W - 72) * f for f in [0.18, 0.27, 0.27, 0.28]]
    items.append(build_table(food_headers, food_rows, TK, cw_f))

    # 10. Results
    items += section_header("10. EXPECTED RESULTS & TRACKING", TK, styles, "📊")
    result_rows = [
        ["Week 1", "1–3 kg", "Mostly water weight; some fat. Keto flu possible (fatigue, headache) — hydrate and electrolyte supplement"],
        ["Week 2", "1–2 kg", "Entering ketosis. Energy improving. Mental clarity increasing. Hunger reducing"],
        ["Week 3", "1–2 kg", "Deep ketosis — consistent fat loss. Body composition visibly improving"],
        ["Week 4", "0.5–1.5 kg", "Fat-adapted state. Metabolism optimized. Sustainable long-term fat loss established"],
        ["Total 30-Day", "4–8 kg", "Typical result varies based on starting weight, compliance, and exercise"],
    ]
    r_headers = ["Period", "Expected Loss", "What to Expect"]
    cw_r = [(W - 72) * f for f in [0.16, 0.15, 0.69]]
    items.append(build_table(r_headers, result_rows, TK, cw_r))
    items.append(Paragraph("<b>Track weekly:</b> Body weight (same time, same day), waist measurement, energy levels (1–10), ketone levels (if testing)", styles["body"]))

    doc.build(items,
              onFirstPage=make_page_bg(TK, is_cover=True),
              onLaterPages=make_page_bg(TK, is_cover=False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
#  PDF 5 — FEMALE VEGETARIAN WEIGHT LOSS PLAN
# ════════════════════════════════════════════════════════════
def generate_female_pdf(path):
    TK = "female"
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=28, bottomMargin=28
    )
    styles = make_styles(TK)
    items = []

    items += build_cover(
        title_lines=["FEMALE WEIGHT LOSS", "FULL WEEKLY", "DIET PLAN"],
        subtitle="Vegetarian Indian Meal Plan — 5-Day Program with Daily Menus",
        edition="AMAN TRAINING CLUB  •  Women's Health Series  •  2024 Edition",
        theme_key=TK, styles=styles,
        badge_texts=["5-DAY PLAN", "VEGETARIAN", "INDIAN CUISINE", "WOMEN'S HEALTH"],
        disclaimer_text=None
    )

    # TOC
    items += section_header("TABLE OF CONTENTS", TK, styles, "📋")
    for item in [
        "1.  Introduction — Weight Loss for Indian Women",
        "2.  Daily Calorie & Macro Targets",
        "3.  Day 1 — Balanced Foundation",
        "4.  Day 2 — High Fibre Day",
        "5.  Day 3 — Protein Focus",
        "6.  Day 4 — Light & Detox Day",
        "7.  Day 5 — Satisfying & Sustainable",
        "8.  Grocery Shopping List",
        "9.  Exercise Recommendations for Women",
        "10. Lifestyle Tips for Sustainable Weight Loss",
    ]:
        items.append(Paragraph(item, styles["toc_item"]))
    items.append(PageBreak())

    # 1. Introduction
    items += section_header("1. INTRODUCTION — WEIGHT LOSS FOR INDIAN WOMEN", TK, styles, "💜")
    items.append(Paragraph(
        "This plan is specifically designed for <b>Indian women</b> who want to lose weight sustainably "
        "using familiar, affordable vegetarian Indian foods. No exotic ingredients, no starvation — "
        "just <b>smart, balanced eating</b> with traditional Indian flavours.",
        styles["body"]
    ))
    for point in [
        "Average calorie target: 1200–1400 kcal/day (adjust ±200 kcal based on activity level)",
        "Balanced macros: protein-forward to preserve muscle while losing fat",
        "High fibre to keep you full and support gut health",
        "All meals use ingredients available at any Indian grocery store",
        "No skipping meals — 5 structured eating times per day prevent cravings",
        "Plan allows 1 'free meal' per week (not shown) — enjoy without guilt",
    ]:
        items.append(bullet_item(point, styles))

    # 2. Macros
    items += section_header("2. DAILY CALORIE & MACRO TARGETS", TK, styles, "📊")
    macro_rows = [
        ["Calories", "1200–1400 kcal", "Adjust based on your BMR and activity level"],
        ["Protein", "60–80 g", "Dal, paneer, soya chunks, curd, legumes"],
        ["Carbohydrates", "130–160 g", "Complex carbs: oats, brown rice, roti (2 max/day)"],
        ["Dietary Fibre", "25–35 g", "Vegetables, fruits, whole grains, legumes"],
        ["Fats", "35–45 g", "Healthy fats: ghee (1 tsp/meal), nuts, seeds"],
        ["Water", "8–10 glasses/day", "Plain water + herbal teas + lemon water"],
    ]
    m_headers = ["Nutrient", "Daily Target", "Best Sources"]
    cw_m = [(W - 72) * f for f in [0.18, 0.18, 0.64]]
    items.append(build_table(m_headers, macro_rows, TK, cw_m))

    # Days 1–5 function
    def day_plan(day_num, day_name, meals, notes):
        day_items = []
        day_items += section_header(f"DAY {day_num} — {day_name}", TK, styles, f"{'🌅🍃🌟🌿✨'[day_num-1]}")
        meal_rows = [[m["time"], m["meal"], m["menu"], m["cals"]] for m in meals]
        m_headers2 = ["Time", "Meal", "Menu", "~Kcal"]
        cw_d = [(W - 72) * f for f in [0.12, 0.14, 0.62, 0.12]]
        day_items.append(build_table(m_headers2, meal_rows, TK, cw_d))
        day_items.append(Paragraph(f"<b>Day {day_num} Notes:</b> {notes}", styles["body"]))
        return day_items

    items += day_plan(1, "BALANCED FOUNDATION", [
        {"time": "7:30 AM", "meal": "Breakfast", "menu": "Overnight soaked oats (½ cup rolled oats + skimmed milk + 1 tsp honey + mixed berries + 5 almonds)", "cals": "~280"},
        {"time": "10:30 AM", "meal": "Mid-Morning", "menu": "1 medium apple OR 1 orange + 1 cup green tea (no sugar)", "cals": "~80"},
        {"time": "1:00 PM", "meal": "Lunch", "menu": "2 whole wheat rotis + 1 cup moong dal (yellow lentil soup) + mixed vegetable sabzi (no oil fry, 1 tsp ghee) + salad (cucumber, tomato, onion + lemon)", "cals": "~420"},
        {"time": "4:30 PM", "meal": "Snack", "menu": "Roasted makhana (foxnuts) — 30g OR handful of mixed seeds (pumpkin + sunflower) + lemon water", "cals": "~120"},
        {"time": "7:30 PM", "meal": "Dinner", "menu": "1 cup vegetable daliya (broken wheat khichdi with mixed vegetables) + 1 cup low-fat curd OR 1 cup vegetable soup + 1 roti", "cals": "~350"},
    ], "Total: ~1250 kcal. First day — eat slowly, drink plenty of water. Avoid snacking after 8 PM.")

    items += day_plan(2, "HIGH FIBRE DAY", [
        {"time": "7:30 AM", "meal": "Breakfast", "menu": "2 idli (medium size) + sambar (dal-based) + 1 tsp coconut chutney + green tea", "cals": "~260"},
        {"time": "10:30 AM", "meal": "Mid-Morning", "menu": "1 banana (small) OR 1 cup papaya cubes + 1 glass buttermilk (chaas, no salt)", "cals": "~90"},
        {"time": "1:00 PM", "meal": "Lunch", "menu": "1 cup brown rice + 1 cup rajma masala (kidney beans) + cucumber raita + large salad with olive oil dressing", "cals": "~430"},
        {"time": "4:30 PM", "meal": "Snack", "menu": "Moong dal cheela (1 medium, no oil) + green chutney OR carrot + celery sticks with hummus (2 tbsp)", "cals": "~130"},
        {"time": "7:30 PM", "meal": "Dinner", "menu": "Poha (flattened rice, ½ cup dry) with peas, capsicum, mustard seeds, curry leaves + 1 cup masala milk (low-fat, no sugar)", "cals": "~340"},
    ], "Total: ~1250 kcal. High fibre day aids digestion. Expect fuller feeling. If very hungry, add extra salad or vegetable soup.")

    items.append(PageBreak())

    items += day_plan(3, "PROTEIN FOCUS", [
        {"time": "7:30 AM", "meal": "Breakfast", "menu": "Moong dal cheela (2 medium) with finely chopped vegetables + 1 tsp ghee + green chutney + 1 cup masala chai (low-fat milk, less sugar)", "cals": "~300"},
        {"time": "10:30 AM", "meal": "Mid-Morning", "menu": "10–12 almonds + 1 small pear OR 2 walnuts + 5 dates + 1 glass warm water with lemon", "cals": "~100"},
        {"time": "1:00 PM", "meal": "Lunch", "menu": "2 rotis (wheat/bajra) + 1 cup chana masala (chickpeas) + 100g paneer bhurji (low oil) + sliced onions + lemon", "cals": "~460"},
        {"time": "4:30 PM", "meal": "Snack", "menu": "1 cup low-fat dahi (yogurt) + 1 tsp jeera (roasted cumin) + pinch of black salt OR protein-rich smoothie (banana + milk + 1 tbsp peanut butter)", "cals": "~140"},
        {"time": "7:30 PM", "meal": "Dinner", "menu": "Palak tofu/paneer sabzi (light) + 1 cup clear vegetable soup + 1 small roti OR 1 cup quinoa khichdi", "cals": "~320"},
    ], "Total: ~1320 kcal. Protein-rich day rebuilds muscle. Perfect for the day after or before an exercise session.")

    items += day_plan(4, "LIGHT & DETOX DAY", [
        {"time": "7:30 AM", "meal": "Breakfast", "menu": "1 cup warm water + lemon + ginger (first thing). Breakfast: upma (semolina, 1/4 cup dry) with vegetables + 1 cup green tea", "cals": "~220"},
        {"time": "10:30 AM", "meal": "Mid-Morning", "menu": "1 glass coconut water (natural electrolytes) OR 1 glass amla juice (Indian gooseberry) + 5 almonds", "cals": "~70"},
        {"time": "1:00 PM", "meal": "Lunch", "menu": "1 cup khichdi (moong dal + rice 1:1, thin consistency) + 1 cup mixed vegetable soup (no cream) + 1 cup curd", "cals": "~380"},
        {"time": "4:30 PM", "meal": "Snack", "menu": "Herbal tea (chamomile / ginger-tulsi) + 5–6 roasted almonds OR cucumber + carrot sticks with lemon + chaat masala", "cals": "~80"},
        {"time": "7:30 PM", "meal": "Dinner", "menu": "1 cup moong dal soup (light, watery consistency) + 1 small roti + steamed vegetables (broccoli, beans, carrots) with minimal ghee", "cals": "~300"},
    ], "Total: ~1050 kcal. Intentionally lighter day for digestive rest. Drink 10+ glasses of water. Focus on feeling light and clean.")

    items += day_plan(5, "SATISFYING & SUSTAINABLE", [
        {"time": "7:30 AM", "meal": "Breakfast", "menu": "Vegetable poha (1 cup cooked) with peas, groundnuts, turmeric, lemon + 1 cup masala chai", "cals": "~290"},
        {"time": "10:30 AM", "meal": "Mid-Morning", "menu": "1 medium guava (high fibre, low cal) + 1 glass chaas (buttermilk with cumin and mint)", "cals": "~90"},
        {"time": "1:00 PM", "meal": "Lunch", "menu": "1 cup dal fry (any dal) + 2 rotis + aloo gobhi sabzi (dry, low oil) + large salad with dressing", "cals": "~440"},
        {"time": "4:30 PM", "meal": "Snack", "menu": "Roasted chana (½ cup) + green tea OR 1 small banana + 1 tbsp peanut butter (in moderation)", "cals": "~150"},
        {"time": "7:30 PM", "meal": "Dinner", "menu": "Paneer tikka (grilled, 100g) + 1 cup dal soup + salad + 1 roti OR rice bowl with dal + 2 side vegetables", "cals": "~380"},
    ], "Total: ~1350 kcal. End the week feeling nourished. Plan meals for next week. Celebrate your discipline — not with food, but with acknowledgment.")

    items.append(PageBreak())

    # 8. Shopping list
    items += section_header("8. GROCERY SHOPPING LIST", TK, styles, "🛒")
    shop_categories = {
        "Grains & Pulses": ["Rolled oats", "Brown rice", "Whole wheat flour (atta)", "Bajra/jowar flour", "Semolina (suji)", "Poha (flattened rice)", "Daliya (broken wheat)", "Moong dal", "Chana dal", "Rajma (kidney beans)", "Black chana (kala chana)"],
        "Dairy & Protein": ["Paneer (low-fat)", "Low-fat curd / yogurt", "Skimmed milk", "Buttermilk (chaas)", "Soya chunks / tofu"],
        "Vegetables": ["Spinach (palak)", "Methi leaves", "Broccoli", "Cauliflower", "Capsicum", "Cucumber", "Tomatoes", "Onions", "Carrots", "Peas", "Zucchini / lauki (bottle gourd)"],
        "Fruits": ["Apples", "Oranges", "Bananas (small)", "Papaya", "Guava", "Berries (seasonal)"],
        "Nuts, Seeds & Healthy Fats": ["Almonds", "Walnuts", "Makhana (foxnuts)", "Pumpkin seeds", "Flaxseeds", "Peanuts/peanut butter", "Ghee (pure)", "Coconut oil"],
        "Herbs & Spices": ["Cumin seeds (jeera)", "Mustard seeds", "Turmeric", "Coriander powder", "Garam masala", "Chaat masala", "Green chillies", "Ginger", "Garlic", "Curry leaves", "Coriander/mint leaves"],
    }
    for cat, items_list in shop_categories.items():
        items.append(Paragraph(f"<b>{cat}:</b>", styles["subsection"]))
        items.append(Paragraph(",  ".join(items_list), styles["body"]))

    # 9. Exercise
    items += section_header("9. EXERCISE RECOMMENDATIONS FOR WOMEN", TK, styles, "🧘")
    ex_rows = [
        ["Morning Walk", "Daily", "30 min brisk walk — best fat-burning activity for beginners"],
        ["Strength Training", "3×/week", "Bodyweight: squats, lunges, push-ups, planks. Builds metabolism"],
        ["Yoga / Pilates", "Daily or 4×/week", "Reduces cortisol (stress hormone) — key for women's fat loss"],
        ["Dance / Zumba", "2×/week", "Fun, high-calorie burn — great for motivation and consistency"],
        ["Rest", "1–2 days/week", "Recovery is as important as exercise — prevents burnout"],
    ]
    ex_headers2 = ["Activity", "Frequency", "Notes"]
    cw_ex2 = [(W - 72) * f for f in [0.22, 0.14, 0.64]]
    items.append(build_table(ex_headers2, ex_rows, TK, cw_ex2))
    items.append(Paragraph(
        "<b>Important:</b> Even 30 minutes of daily walking creates a significant calorie deficit over 30 days. "
        "Consistency beats intensity — show up every day, even for short sessions.",
        styles["body"]
    ))

    # 10. Tips
    items += section_header("10. LIFESTYLE TIPS FOR SUSTAINABLE WEIGHT LOSS", TK, styles, "💡")
    for tip in [
        "<b>Drink 8–10 glasses of water daily:</b> Often hunger is actually thirst. Drink a glass before every meal",
        "<b>Sleep 7–9 hours:</b> Poor sleep disrupts hormones (ghrelin/leptin) — directly causes weight gain and cravings",
        "<b>Avoid processed & packaged foods:</b> Namkeen, biscuits, chips, and Indian sweets are calorie-dense and nutrient-poor",
        "<b>Cook at home as much as possible:</b> You control ingredients, oil quantity, and portion size",
        "<b>Eat slowly — chew 20+ times per bite:</b> Signals fullness to your brain; prevents overeating",
        "<b>Don't skip breakfast:</b> It jumpstarts metabolism and prevents mid-morning binging",
        "<b>Manage stress:</b> High cortisol = fat storage (especially belly fat). Yoga, meditation, and deep breathing help",
        "<b>Hormonal awareness:</b> Weight fluctuates with menstrual cycle — track trends, not day-to-day changes",
        "<b>No fad diets:</b> Sustainable weight loss is 0.5–1 kg per week. Anything faster risks muscle loss and rebound",
        "<b>Take weekly progress photos:</b> The mirror shows progress before the scale does — especially with muscle gain",
    ]:
        items.append(bullet_item(tip, styles))

    items.append(Spacer(1, 8))
    items.append(divider(TK))
    items.append(Paragraph(
        "Created by AMAN TRAINING CLUB  •  Royal Fitness Club  •  2024",
        ParagraphStyle("brand_footer", fontName="Helvetica-Bold", fontSize=9,
                       textColor=THEMES[TK]["accent2"], alignment=TA_CENTER)
    ))
    items.append(Paragraph(
        "For personalized coaching and meal plans, contact us through Royal Fitness Club.",
        styles["disclaimer"]
    ))

    doc.build(items,
              onFirstPage=make_page_bg(TK, is_cover=True),
              onLaterPages=make_page_bg(TK, is_cover=False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    out_dir = "/home/user/royal-fitness-club/generated_pdfs"
    os.makedirs(out_dir, exist_ok=True)

    print("Generating PDFs…")

    generate_cutting_pdf(f"{out_dir}/01_Advanced_Cutting_Cycle_12Weeks.pdf")
    generate_bulking_pdf(f"{out_dir}/02_Advanced_Bulking_Cycle_with_Peptides.pdf")
    generate_beginner_pdf(f"{out_dir}/03_Beginner_Steroid_Cycle_Full_Guide.pdf")
    generate_keto_pdf(f"{out_dir}/04_30Day_Keto_Indian_Vegetarian_Plan.pdf")
    generate_female_pdf(f"{out_dir}/05_Female_Vegetarian_Weight_Loss_Plan.pdf")

    print("\nAll 5 PDFs generated successfully!")
    for f in sorted(os.listdir(out_dir)):
        size = os.path.getsize(f"{out_dir}/{f}") // 1024
        print(f"  {f}  ({size} KB)")
