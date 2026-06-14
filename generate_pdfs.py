#!/usr/bin/env python3
"""Elite Fitness Guide Series — 15 Premium Research-Based PDFs."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)

W, H = A4
SERIES = "ELITE FITNESS GUIDE SERIES"

THEMES = {
    "cutting":     {"bg":"#0B0B0B","accent":"#B71C1C","accent2":"#EF5350","gold":"#FF8F00","text":"#F0F0F0","muted":"#777777","row_odd":"#1C1C1C","row_even":"#141414","hdr":"#B71C1C","ibg":"#1A0A0A","wbg":"#1F1200"},
    "bulking":     {"bg":"#080D17","accent":"#0D47A1","accent2":"#2196F3","gold":"#FFC107","text":"#F0F0F0","muted":"#777777","row_odd":"#0F1825","row_even":"#0A1020","hdr":"#0D47A1","ibg":"#0A0F1A","wbg":"#1A1200"},
    "beginner":    {"bg":"#060F07","accent":"#1B5E20","accent2":"#4CAF50","gold":"#FFCA28","text":"#F0F0F0","muted":"#777777","row_odd":"#0E1A0F","row_even":"#091209","hdr":"#1B5E20","ibg":"#0A1A0B","wbg":"#1A1400"},
    "keto":        {"bg":"#0E0700","accent":"#E65100","accent2":"#FF9800","gold":"#FFD600","text":"#F0F0F0","muted":"#777777","row_odd":"#1A0F00","row_even":"#120A00","hdr":"#E65100","ibg":"#180C00","wbg":"#1A1A00"},
    "female":      {"bg":"#0C080F","accent":"#6A1B9A","accent2":"#BA68C8","gold":"#F48FB1","text":"#F0F0F0","muted":"#777777","row_odd":"#150D1E","row_even":"#0F0915","hdr":"#6A1B9A","ibg":"#130A1C","wbg":"#1A0F15"},
    "peptide":     {"bg":"#060B0E","accent":"#00695C","accent2":"#26C6DA","gold":"#64FFDA","text":"#F0F0F0","muted":"#777777","row_odd":"#0A1015","row_even":"#060C10","hdr":"#00695C","ibg":"#071012","wbg":"#0A1400"},
    "sarms":       {"bg":"#0A0714","accent":"#4527A0","accent2":"#9575CD","gold":"#B388FF","text":"#F0F0F0","muted":"#777777","row_odd":"#130F1E","row_even":"#0D0A17","hdr":"#4527A0","ibg":"#0F0C1A","wbg":"#1A1200"},
    "trt":         {"bg":"#060610","accent":"#1A237E","accent2":"#5C6BC0","gold":"#FFD54F","text":"#F0F0F0","muted":"#777777","row_odd":"#0C0C1A","row_even":"#080812","hdr":"#1A237E","ibg":"#0A0A18","wbg":"#1A1000"},
    "hypertrophy": {"bg":"#0B0B0B","accent":"#BF360C","accent2":"#FF7043","gold":"#FFAB40","text":"#F0F0F0","muted":"#777777","row_odd":"#1A1410","row_even":"#120E0A","hdr":"#BF360C","ibg":"#180E08","wbg":"#1A1400"},
    "fatloss":     {"bg":"#080D08","accent":"#1B5E20","accent2":"#69F0AE","gold":"#CCFF90","text":"#F0F0F0","muted":"#777777","row_odd":"#0F180A","row_even":"#0A1006","hdr":"#1B5E20","ibg":"#0C1408","wbg":"#1A1400"},
    "women_fit":   {"bg":"#0F0814","accent":"#880E4F","accent2":"#F06292","gold":"#F8BBD9","text":"#F0F0F0","muted":"#777777","row_odd":"#180D20","row_even":"#110818","hdr":"#880E4F","ibg":"#160A1E","wbg":"#1A0E15"},
    "indian":      {"bg":"#0D0800","accent":"#F57F17","accent2":"#FFB300","gold":"#FFF176","text":"#F0F0F0","muted":"#777777","row_odd":"#1A1200","row_even":"#120D00","hdr":"#F57F17","ibg":"#180F00","wbg":"#1A1600"},
    "preworkout":  {"bg":"#0A0A12","accent":"#C62828","accent2":"#EF5350","gold":"#FF8A65","text":"#F0F0F0","muted":"#777777","row_odd":"#18101A","row_even":"#120C14","hdr":"#C62828","ibg":"#160C1A","wbg":"#1A0E00"},
    "natural_t":   {"bg":"#080C08","accent":"#2E7D32","accent2":"#66BB6A","gold":"#A5D6A7","text":"#F0F0F0","muted":"#777777","row_odd":"#0F180F","row_even":"#0A1008","hdr":"#2E7D32","ibg":"#0C1A0C","wbg":"#1A1400"},
    "recovery":    {"bg":"#07080E","accent":"#01579B","accent2":"#4FC3F7","gold":"#80DEEA","text":"#F0F0F0","muted":"#777777","row_odd":"#0A0F18","row_even":"#060A12","hdr":"#01579B","ibg":"#080C16","wbg":"#0A1400"},
}

def hx(c): return colors.HexColor(c)

def make_bg(tk, is_cover=False):
    t = THEMES[tk]
    def bg(canv, doc):
        canv.saveState()
        canv.setFillColor(hx(t["bg"])); canv.rect(0, 0, W, H, fill=1, stroke=0)
        if is_cover:
            canv.setFillColor(hx(t["accent"])); canv.rect(0, H-20, W, 20, fill=1, stroke=0)
            canv.rect(0, 0, W, 10, fill=1, stroke=0)
            canv.setFillColor(hx(t["accent2"])); canv.setFillAlpha(0.12)
            canv.rect(0, 0, 7, H, fill=1, stroke=0); canv.setFillAlpha(1)
            canv.setStrokeColor(hx(t["accent"])); canv.setStrokeAlpha(0.09); canv.setLineWidth(0.8)
            for i in range(0, 300, 26): canv.line(W-i, 0, W, i)
            canv.setStrokeAlpha(1)
            canv.setFont("Helvetica-Bold", 7); canv.setFillColor(colors.white)
            canv.drawCentredString(W/2, H-13, SERIES)
        else:
            canv.setFillColor(hx(t["accent"])); canv.rect(0, H-4, W, 4, fill=1, stroke=0)
            canv.rect(0, 0, W, 3, fill=1, stroke=0)
            canv.setStrokeColor(hx(t["accent2"])); canv.setStrokeAlpha(0.10); canv.setLineWidth(0.7)
            canv.line(32, 24, 32, H-24); canv.setStrokeAlpha(1)
        canv.setFont("Helvetica", 7); canv.setFillColor(hx(t["muted"]))
        canv.drawString(36, 10, f"{SERIES}  •  Professional Edition")
        canv.drawRightString(W-36, 10, f"Page {doc.page}")
        canv.restoreState()
    return bg

def mk(tk):
    t = THEMES[tk]
    def ps(n, **kw): return ParagraphStyle(n, **kw)
    s = {}
    s["T1"]  = ps("T1",  fontName="Helvetica-Bold",   fontSize=30, textColor=hx(t["text"]),    alignment=TA_CENTER, leading=36, spaceAfter=4)
    s["T2"]  = ps("T2",  fontName="Helvetica-Bold",   fontSize=22, textColor=hx(t["text"]),    alignment=TA_CENTER, leading=26, spaceAfter=4)
    s["sub"] = ps("sub", fontName="Helvetica",         fontSize=12, textColor=hx(t["accent2"]), alignment=TA_CENTER, leading=16, spaceAfter=3)
    s["tag"] = ps("tag", fontName="Helvetica-Oblique", fontSize=9,  textColor=hx(t["muted"]),   alignment=TA_CENTER)
    s["SH"]  = ps("SH",  fontName="Helvetica-Bold",   fontSize=12, textColor=hx(t["accent2"]), spaceBefore=12, spaceAfter=3, leading=15)
    s["SSH"] = ps("SSH", fontName="Helvetica-Bold",   fontSize=10, textColor=hx(t["gold"]),    spaceBefore=7,  spaceAfter=2, leading=13)
    s["B"]   = ps("B",   fontName="Helvetica",         fontSize=8.8,textColor=hx(t["text"]),   spaceBefore=2,  spaceAfter=2, leading=13, leftIndent=12)
    s["BJ"]  = ps("BJ",  fontName="Helvetica",         fontSize=8.8,textColor=hx(t["text"]),   spaceBefore=2,  spaceAfter=2, leading=13, leftIndent=12, alignment=TA_JUSTIFY)
    s["BL"]  = ps("BL",  fontName="Helvetica",         fontSize=8.8,textColor=hx(t["text"]),   spaceBefore=1,  spaceAfter=1, leading=13, leftIndent=20, bulletIndent=8)
    s["SBL"] = ps("SBL", fontName="Helvetica",         fontSize=8.2,textColor=hx(t["muted"]),  spaceBefore=1,  spaceAfter=1, leading=12, leftIndent=34, bulletIndent=22)
    s["DIS"] = ps("DIS", fontName="Helvetica-Oblique", fontSize=7.5,textColor=hx(t["muted"]),  alignment=TA_CENTER, spaceAfter=3, leading=11)
    s["TOC"] = ps("TOC", fontName="Helvetica",         fontSize=9.5,textColor=hx(t["text"]),   spaceBefore=3, spaceAfter=3, leading=13, leftIndent=18)
    s["RN"]  = ps("RN",  fontName="Helvetica-Oblique", fontSize=8,  textColor=hx(t["accent2"]),spaceBefore=1, spaceAfter=1, leading=11, leftIndent=10)
    s["CC"]  = ps("CC",  fontName="Helvetica-Bold",    fontSize=9,  textColor=hx(t["accent2"]), alignment=TA_CENTER)
    s["CM"]  = ps("CM",  fontName="Helvetica",         fontSize=8,  textColor=hx(t["muted"]),   alignment=TA_CENTER)
    return s

def tbl(headers, rows, tk, cw=None):
    t = THEMES[tk]
    hdr_ps = ParagraphStyle('_th', fontName="Helvetica-Bold", fontSize=7.5,
                            textColor=colors.white, alignment=TA_CENTER,
                            leading=9, spaceAfter=0, spaceBefore=0)
    cell_ps = ParagraphStyle('_td', fontName="Helvetica", fontSize=7.5,
                             textColor=hx(t["text"]), alignment=TA_CENTER,
                             leading=9, spaceAfter=0, spaceBefore=0)
    def to_p(text, ps):
        if isinstance(text, str):
            return Paragraph(text.replace('\n', '<br/>'), ps)
        return text
    data = [[to_p(h, hdr_ps) for h in headers]] + \
           [[to_p(c, cell_ps) for c in row] for row in rows]
    tb = Table(data, colWidths=cw, repeatRows=1)
    tb.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  hx(t["hdr"])),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#2A2A2A")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [hx(t["row_odd"]),hx(t["row_even"])]),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    return tb

def sh(text, tk, s, icon=""):
    label = f"{icon}  {text}" if icon else text
    return [Paragraph(f"<b>{label}</b>", s["SH"]),
            HRFlowable(width="100%", thickness=1.5, color=hx(THEMES[tk]["accent"]),
                       spaceAfter=4, spaceBefore=0)]

def bl(text, s, lv=0):
    return Paragraph(("–" if lv else "•") + "  " + text, s["SBL" if lv else "BL"])

def rn(text, tk, s):
    t = THEMES[tk]
    tb = Table([[Paragraph(f"🔬  <i>{text}</i>", s["RN"])]], colWidths=[W-72])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["ibg"])),
                             ("BOX",(0,0),(-1,-1),0.5,hx(t["accent2"])),
                             ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                             ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return tb

def wb(text, tk, s):
    t = THEMES[tk]
    tb = Table([[Paragraph(f"⚠️  <b>IMPORTANT:</b>  {text}", s["B"])]], colWidths=[W-72])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["wbg"])),
                             ("BOX",(0,0),(-1,-1),0.8,hx(t["gold"])),
                             ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                             ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return tb

def cover(title_lines, subtitle, tagline, tk, s, badges=None, disclaimer=None, edition="Research-Based  •  Professional Edition  •  2024"):
    t = THEMES[tk]; items = []; items.append(Spacer(1, 44*mm))
    if badges:
        bw = (W-80)/len(badges)
        bt = Table([[b for b in badges]], colWidths=[bw]*len(badges))
        bt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["accent"])),
                                 ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
                                 ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
                                 ("FONTSIZE",(0,0),(-1,-1),6.5),
                                 ("ALIGN",(0,0),(-1,-1),"CENTER"),
                                 ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                 ("TOPPADDING",(0,0),(-1,-1),5),
                                 ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        items += [bt, Spacer(1,6*mm)]
    for line in title_lines:
        st = s["T1"] if len(line) < 26 else s["T2"]
        items.append(Paragraph(line, st))
    items += [Spacer(1,3*mm),
              HRFlowable(width="55%", thickness=2.5, color=hx(t["accent"]), spaceAfter=5, spaceBefore=3),
              Paragraph(subtitle, s["sub"]), Spacer(1,2*mm), Paragraph(tagline, s["tag"]),
              Spacer(1,8*mm)]
    ed = Table([[Paragraph(f"<b>{SERIES}</b>", s["CC"]),
                 Paragraph(edition, s["CM"])]], colWidths=[(W-80)*0.56,(W-80)*0.44])
    ed.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#141414")),
                             ("BOX",(0,0),(-1,-1),1,hx(t["accent"])),
                             ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
                             ("LINEAFTER",(0,0),(0,-1),0.5,hx(t["muted"]))]))
    items += [ed, Spacer(1,65*mm)]
    if disclaimer:
        items.append(Paragraph(disclaimer, s["DIS"]))
    items.append(PageBreak())
    return items

def new_doc(path):
    return SimpleDocTemplate(path, pagesize=A4,
                              leftMargin=36, rightMargin=36,
                              topMargin=26, bottomMargin=26)

# ════════════════════════════════════════════════════════════
# PDF 01 — ADVANCED CUTTING CYCLE (12 WEEKS)
# ════════════════════════════════════════════════════════════
def pdf_cutting(path):
    TK="cutting"; doc=new_doc(path); s=mk(TK); items=[]
    DISC="⚠ MEDICAL DISCLAIMER: This document is for informational and educational purposes only. Anabolic steroids are controlled substances in many jurisdictions. Always consult a licensed physician before beginning any hormonal protocol. Misuse carries serious health risks including cardiovascular damage, liver toxicity, hormonal disruption, and psychological effects."
    items += cover(["ADVANCED CUTTING","STEROID CYCLE","12-WEEK COMPLETE PROTOCOL"],
                   "Compounds · AI Management · Clenbuterol · T3 · HGH · PCT · Full Supplement Stack",
                   "Maximum fat loss · Lean muscle preservation · Peak conditioning",
                   TK, s, badges=["12 WEEKS","ADVANCED","CUTTING PHASE","FULL PCT"],disclaimer=DISC)

    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Protocol Philosophy & Expected Outcomes","2.  Core Compound Stack & Mechanisms of Action",
               "3.  12-Week Dosage Schedule (Complete Timeline)","4.  Estrogen Management — AI Protocol",
               "5.  Clenbuterol & T3 Thermogenic Stack","6.  HGH Fragment 176-191 & IGF-1 LR3",
               "7.  MENT — Optional Advanced Add-On","8.  Post Cycle Therapy (PCT) — Weeks 13–16",
               "9.  Essential Health & Support Supplement Stack","10. Training, Nutrition & Cardio Strategy",
               "11. Blood Work — What to Test & When","12. Side Effect Management Guide"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. PROTOCOL PHILOSOPHY & EXPECTED OUTCOMES", TK, s, "🎯")
    items.append(Paragraph("This advanced 12-week cutting protocol is designed for experienced athletes with a minimum of 3 years of natural training and at least one prior anabolic cycle. The compound selection prioritizes <b>hardness</b>, <b>vascularity</b>, and <b>fat oxidation</b> while aggressively controlling water retention and estrogenic side effects.", s["BJ"]))
    items.append(rn("Studies show that testosterone + trenbolone combinations produce superior fat-free mass retention during caloric deficit compared to testosterone alone, with trenbolone's unique binding affinity for the androgen receptor (AR) being approximately 5× greater than testosterone.", TK, s))
    items.append(Spacer(1,4))
    items.append(Paragraph("<b>Who This Protocol Is For:</b>", s["SSH"]))
    for x in ["Athletes with 3+ years of consistent, structured resistance training",
               "Individuals who have completed at least one successful testosterone-only cycle",
               "Body fat 15–20%+ seeking to reach 8–12% competition or aesthetic physique",
               "Those with baseline blood work confirming normal lipid, liver, and hormonal values",
               "Athletes who understand the legal status of these compounds in their jurisdiction"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Realistic Expected Outcomes:</b>", s["SSH"]))
    rows=[["Metric","Conservative","Aggressive"],["Body Fat Loss","6–8 lbs","10–14 lbs"],
          ["Lean Mass Change","-0 to +3 lbs","+3–6 lbs"],["Strength Change","±5%","+5–10%"],
          ["Vascularity","Moderate improvement","Significant improvement"],
          ["Cycle Duration","12 weeks","12 weeks"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.30,0.35,0.35]]))

    items += sh("2. CORE COMPOUND STACK & MECHANISMS OF ACTION", TK, s, "💊")
    compounds=[
        ("Testosterone Propionate","Test Prop","100–150 mg EOD","Wks 1–12","Base androgen — maintains physiological androgen levels, prevents muscle catabolism in caloric deficit. Propionate ester chosen for fast clearance pre-PCT."),
        ("Trenbolone Acetate","Tren Ace","75–100 mg EOD","Wks 1–12","Potent 19-nor androgen — 5× AR binding affinity vs testosterone. Dramatically increases nitrogen retention, IGF-1 production, and nutrient partitioning. Does not aromatize — zero water retention."),
        ("Masteron Propionate","Mast Prop","100 mg EOD","Wks 1–12","DHT derivative — anti-estrogenic properties by competing for aromatase enzyme. Adds significant muscle hardness and density. SHBG binding increases free testosterone."),
        ("Primobolan","Primo","600 mg/wk","Wks 1–12","Methenolone enanthate — highly anabolic with very low androgenic ratio. Exceptional lean mass preservation with minimal side effects. Historically the compound of choice for elite-level aesthetic athletes."),
        ("Anavar","Oxandrolone","50 mg/day","Wks 1–8","Mild oral DHT derivative — increases phosphocreatine synthesis in muscle, significantly improving strength without mass. Very favorable safety profile among oral steroids."),
        ("Winstrol","Stanozolol","50 mg/day","Wks 9–12","DHT derivative — reduces SHBG dramatically (up to 50%), dramatically freeing bound testosterone. Adds final-stage dryness, vascularity, and muscle separation."),
    ]
    headers=["Compound","Short","Dose","Duration","Mechanism & Purpose"]
    cw=[(W-72)*f for f in [0.18,0.09,0.13,0.12,0.48]]
    items.append(tbl(headers,[[c[0],c[1],c[2],c[3],c[4]] for c in compounds],TK,cw))

    items += sh("3. 12-WEEK DOSAGE SCHEDULE — PHASE BREAKDOWN", TK, s, "📅")
    items.append(Paragraph("Three distinct phases: <b>Foundation (Wks 1–4)</b> — establishing blood levels; <b>Loading (Wks 5–8)</b> — peak anabolic environment; <b>Finisher (Wks 9–12)</b> — maximum conditioning with oral compound swap. All short-ester injectables (Test P, Tren A, Mast P) are dosed <b>Every Other Day (EOD)</b>. Primo is split into two equal injections weekly.", s["B"]))
    ph=[["Phase","Weeks","EOD Injectables (per pin)","Primobolan (wk)","Oral Compound"],
        ["Foundation","1–4","Test P 100mg + Tren A 75mg + Mast P 100mg","2 × 300mg = 600mg","Anavar 50mg/day"],
        ["Loading",   "5–8","Test P 150mg + Tren A 100mg + Mast P 100mg","2 × 300mg = 600mg","Anavar 50mg/day"],
        ["Finisher",  "9–12","Test P 150mg + Tren A 100mg + Mast P 100mg","2 × 300mg = 600mg","Winstrol 50mg/day"]]
    items.append(tbl(ph[0],[r for r in ph[1:]],TK,[(W-72)*f for f in [0.13,0.09,0.38,0.22,0.18]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Day-Wise Weekly Injection Schedule (EOD Rotation — Foundation Phase Wks 1–4):</b>", s["SSH"]))
    day=[["Day","Injectables (EOD Pin)","Dose Per Compound","Primo + Oral","AI / Ancillary"],
         ["Monday","Test P + Tren A + Mast P","100mg + 75mg + 100mg","Primo 300mg · Anavar 25mg AM","Arimidex 0.5mg"],
         ["Tuesday","— No injection —","—","Anavar 25mg PM","Cabergoline 0.25mg"],
         ["Wednesday","Test P + Tren A + Mast P","100mg + 75mg + 100mg","Anavar 25mg AM","Arimidex 0.5mg"],
         ["Thursday","— No injection —","—","Anavar 25mg PM","—"],
         ["Friday","Test P + Tren A + Mast P","100mg + 75mg + 100mg","Primo 300mg · Anavar 25mg AM","Arimidex 0.5mg"],
         ["Saturday","— No injection —","—","Anavar 25mg PM","Cabergoline 0.25mg"],
         ["Sunday","Test P + Tren A + Mast P","100mg + 75mg + 100mg","Anavar 25mg AM","—"],
    ]
    items.append(tbl(day[0],[r for r in day[1:]],TK,[(W-72)*f for f in [0.13,0.23,0.22,0.24,0.18]]))
    items.append(Paragraph("<i>Loading Phase (Wks 5–8): Increase Test P → 150mg, Tren A → 100mg per EOD pin. Finisher Phase (Wks 9–12): Swap Anavar → Winstrol 50mg/day split AM/PM.</i>", s["DIS"]))
    items.append(PageBreak())

    items += sh("4. ESTROGEN MANAGEMENT — AI PROTOCOL", TK, s, "🛡")
    items.append(Paragraph("Estrogen management is arguably the most critical skill in anabolic cycle management. Too high → water retention, gynecomastia, high blood pressure, mood instability. Too low → joint pain, low libido, erectile dysfunction, depression, impaired muscle growth. <b>The goal is optimal estrogen — not zero estrogen.</b>", s["BJ"]))
    items.append(rn("Optimal E2 for cutting phases: 20–30 pg/mL. Estradiol below 10 pg/mL causes significant joint pain and impaired collagen synthesis. Estradiol above 50 pg/mL causes water retention that masks conditioning.", TK, s))
    items.append(Paragraph("<b>Arimidex (Anastrozole) — Primary AI:</b>", s["SSH"]))
    for x in ["Starting dose: 0.5 mg every other day (EOD) — adjust based on blood work E2 levels",
               "Mechanism: Reversible competitive inhibitor of aromatase enzyme (CYP19A1)",
               "If E2 is high (>40 pg/mL on blood work): increase to 0.5 mg daily",
               "If symptoms of low E2 appear (joint pain, low libido): reduce to 0.25 mg EOD",
               "Always adjust based on lab values, not symptoms alone — symptoms are unreliable"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Cabergoline (Caber) — Prolactin Control:</b>", s["SSH"]))
    for x in ["Dose: 0.25 mg twice weekly throughout cycle (Trenbolone is a 19-nor compound)",
               "Mechanism: Dopamine D2 receptor agonist — suppresses pituitary prolactin release",
               "19-nor compounds (Tren, Deca) can elevate prolactin leading to gynecomastia, erectile dysfunction, and lactation in extreme cases",
               "Target prolactin: <15 ng/mL. Check via blood work at Week 6"]:
        items.append(bl(x, s))
    items.append(wb("Never run Trenbolone without having Cabergoline on hand. Prolactin-induced gynecomastia does NOT respond to Nolvadex — it requires a dopamine agonist (Caber or Pramipexole).", TK, s))

    items += sh("5. CLENBUTEROL & T3 THERMOGENIC STACK", TK, s, "🔥")
    items.append(Paragraph("<b>Clenbuterol — Beta-2 Adrenergic Agonist:</b>", s["SSH"]))
    items.append(Paragraph("Clenbuterol is not an anabolic steroid — it is a sympathomimetic bronchodilator that stimulates β2-adrenergic receptors, increasing cellular cAMP, which activates lipase enzymes to break down stored triglycerides (lipolysis). It also slightly increases basal metabolic rate (BMR) through thermogenesis.", s["BJ"]))
    for x in ["Protocol: 2 weeks ON / 2 weeks OFF (prevents receptor desensitization)",
               "Start: 20 mcg/day → increase by 20 mcg every 2 days until effective dose",
               "Men: maximum 100–120 mcg/day | Women: maximum 80 mcg/day",
               "Always taper down over final 2 days of each ON cycle",
               "Side effects: tremors, insomnia, elevated heart rate, muscle cramps (take taurine 3g/day to mitigate cramps)",
               "Potassium supplementation (200–400 mg/day) reduces cramping and cardiac risk"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>T3 (Cytomel / Liothyronine) — Thyroid Hormone:</b>", s["SSH"]))
    items.append(Paragraph("T3 is the active form of thyroid hormone that directly controls metabolic rate. Exogenous T3 supplementation during a cut increases basal metabolic rate by 10–30%, dramatically accelerating fat loss. The trade-off: T3 is also mildly catabolic at high doses and can suppress natural thyroid production.", s["BJ"]))
    rows=[["Phase","T3 Dose","Duration","Notes"],
          ["Ramp-Up","25 mcg/day","Wks 1–2","Start low to assess tolerance"],
          ["Therapeutic","50 mcg/day","Wks 3–10","Primary fat-burning dose"],
          ["Taper","25 mcg/day","Wks 11–12","Mandatory taper — never stop cold turkey"],
          ["Recovery","Stop","Post-cycle","Thyroid recovers in 2–4 weeks"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.16,0.16,0.16,0.52]]))
    items.append(wb("Never exceed 75 mcg T3/day and never stop abruptly. Cold turkey cessation can cause hypothyroid crash (extreme fatigue, weight gain, depression). Always taper over minimum 2 weeks.", TK, s))

    items += sh("6. HGH FRAGMENT 176-191 & IGF-1 LR3", TK, s, "💉")
    items.append(Paragraph("<b>HGH Fragment 176-191</b> is a 16-amino-acid peptide corresponding to the fat-metabolizing region of human growth hormone. Unlike full HGH, it does not affect insulin sensitivity or IGF-1 levels — it <i>only</i> targets adipose tissue. It activates β3-adrenergic receptors in fat cells and inhibits lipogenesis while stimulating lipolysis.", s["BJ"]))
    for x in ["Dose: 250–500 mcg/day, split into 2 injections",
               "Optimal timing: Fasted morning injection + pre-workout injection for maximum lipolysis",
               "Administer subcutaneously (SC) into abdominal fat — targets visceral and subcutaneous adipose",
               "No effect on blood glucose — safe for diabetics (unlike full HGH)",
               "Reconstitute with bacteriostatic water; stable 4 weeks refrigerated"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>IGF-1 LR3 (Long R3 Insulin-Like Growth Factor-1)</b>", s["SSH"]))
    for x in ["Dose: 40–60 mcg post-workout on training days only (5 days/week maximum)",
               "Mechanism: Binds IGF-1 receptors with 3× greater affinity than native IGF-1; 120-hour half-life vs 15 min for native IGF-1",
               "Effect: Muscle cell hyperplasia (new satellite cell proliferation) + hypertrophy — unique dual mechanism",
               "Cycle length: 4 weeks maximum then 4-week break (receptor downregulation occurs)",
               "Do NOT inject fasted — IGF-1 LR3 is hypoglycemic; consume 30g carbs before injecting"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    items += sh("7. MENT (TRESTOLONE) — OPTIONAL ADD-ON", TK, s, "⚡")
    items.append(Paragraph("MENT (7α-methyl-19-nortestosterone / Trestolone Acetate) is one of the most potent anabolic compounds ever synthesized — estimated at <b>10× the anabolic potency of testosterone</b> by weight. It was originally developed as a male contraceptive and is used sparingly by advanced athletes for short loading phases.", s["BJ"]))
    items.append(rn("MENT binds to the androgen receptor with 2,300% the activity of testosterone and aromatizes at a rate approximately 7× greater. This means aggressive AI use is mandatory if MENT is added.", TK, s))
    for x in ["Dose: 25 mg/day (injected daily or every other day — short ester)",
               "Duration: Weeks 1–6 ONLY — not for full cycle use",
               "AI consideration: Double or triple AI dose when running MENT due to extreme aromatization",
               "Blood work every 3 weeks is mandatory when MENT is included",
               "NOT recommended for users without extensive cycle experience and established AI dosing knowledge"]:
        items.append(bl(x, s))

    items += sh("8. POST CYCLE THERAPY (PCT) — WEEKS 13–16", TK, s, "🔄")
    items.append(Paragraph("PCT begins <b>3 days</b> after the last short-ester injection (Test Prop, Tren Ace, Mast Prop). For Primobolan (long ester), begin 14 days after last injection. The goal of PCT is to restore the hypothalamic-pituitary-testicular (HPT) axis to full function by eliminating estrogen feedback suppression and stimulating LH/FSH production.", s["BJ"]))
    pct=[["Compound","Dose","Schedule","Duration","Mechanism"],
         ["HCG","500 IU","Every 3 days","Wks 13–14","LH analog — directly stimulates Leydig cells to resume testosterone production; prevents testicular atrophy from becoming permanent"],
         ["Clomid","50 mg","Daily","Wks 13–16","SERM — blocks E2 receptors at pituitary, removing negative feedback; brain perceives low estrogen and ramps up GnRH → LH → FSH"],
         ["Nolvadex","20 mg","Daily","Wks 13–16","SERM — anti-estrogenic at pituitary/hypothalamus; also protects breast tissue from gynecomastia during hormonal fluctuation"],
         ["Arimidex","0.25 mg","EOD","Wks 13–15","Gradual AI taper — prevents estrogen rebound as Clomid/Nolvadex raise LH which briefly increases T and thus E2"]]
    items.append(tbl(pct[0],[r for r in pct[1:]],TK,[(W-72)*f for f in [0.17,0.10,0.13,0.13,0.47]]))
    items.append(rn("Blood work at PCT Week 4: total testosterone, free testosterone, LH, FSH, E2. Target recovery: total T >400 ng/dL, LH >2 mIU/mL. If suppressed at Week 8 post-PCT, consult an endocrinologist.", TK, s))

    items += sh("9. HEALTH & SUPPORT SUPPLEMENT STACK", TK, s, "💊")
    supp_rows=[
        ["Liver Support","TUDCA (Tauroursodeoxycholic Acid)","500 mg/day","Prevents cholestasis; superior to Milk Thistle for oral AAS protection. Upregulates bile secretion and prevents hepatocyte apoptosis."],
        ["Liver Support","Milk Thistle (Silymarin 80%)","600 mg/day","Flavonoid complex — scavenges hepatotoxic free radicals, increases glutathione, inhibits NF-κB inflammatory pathway in liver cells."],
        ["Liver Support","NAC (N-Acetyl Cysteine)","600 mg/day","Glutathione precursor — most studied hepatoprotective antioxidant. Also reduces LDL oxidation and cardiovascular inflammation."],
        ["Cardiovascular","Omega-3 (EPA+DHA combined)","4–6 g/day","Reduces triglycerides 20–50%, decreases platelet aggregation, lowers resting heart rate, anti-inflammatory via COX pathway inhibition."],
        ["Cardiovascular","CoQ10 (Ubiquinol form)","200–400 mg/day","Mitochondrial electron carrier — statins and AAS deplete CoQ10. Ubiquinol form is 8× more bioavailable than ubiquinone."],
        ["Cardiovascular","Red Yeast Rice","1200 mg/day","Contains monacolin K (natural lovastatin analog) — reduces LDL cholesterol. Use when off-cycle if lipids remain elevated."],
        ["Cardiovascular","Hawthorn Berry Extract","500 mg 2×/day","Vasodilatory — reduces systemic vascular resistance, lowers blood pressure, improves cardiac output through flavonoid action on endothelium."],
        ["Joint Support","Glucosamine + Chondroitin","1500 + 1200 mg/day","Structural precursors for cartilage and synovial fluid — critical with Winstrol (reduces SHBG and can cause dry joints)"],
        ["Joint Support","Collagen Peptides (Type I+II+III)","10–15 g/day","Provides hydroxyproline and glycine for connective tissue synthesis. Take with Vitamin C for maximum collagen cross-linking."],
        ["Hormonal","DIM (Diindolylmethane)","200 mg/day","Cruciferous vegetable derivative — shifts estrogen metabolism toward 2-hydroxyestrone (less potent) and away from 16-alpha-hydroxyestrone (more potent/carcinogenic)."],
        ["Hormonal","ZMA (Zinc+Magnesium+B6)","As directed, nightly","Zinc is a 5-alpha reductase cofactor; magnesium improves sleep quality and testosterone production. Deficiency common in athletes sweating heavily."],
        ["General","Vitamin D3 + K2","5000 IU + 100 mcg/day","D3 is essential for testosterone production (LH receptor expression), immune function, and mood. K2 directs calcium to bones and away from arteries."],
        ["General","Electrolytes (full spectrum)","Daily","Clenbuterol and T3 dramatically increase electrolyte excretion. Sodium, potassium, magnesium, phosphorus all depleted rapidly."],
        ["Performance","Creatine Monohydrate","5 g/day","Increases phosphocreatine stores — 3–8% strength increase across all rep ranges. Prevents strength loss during caloric deficit. No loading needed."],
    ]
    items.append(tbl(["Category","Supplement","Dose","Mechanism & Benefit"],[r for r in supp_rows],TK,[(W-72)*f for f in [0.14,0.21,0.13,0.52]]))
    items.append(PageBreak())

    items += sh("10. TRAINING, NUTRITION & CARDIO STRATEGY", TK, s, "🏋")
    items.append(Paragraph("<b>Training — Volume & Frequency:</b>", s["SSH"]))
    for x in ["5–6 days/week: Push/Pull/Legs or Upper/Lower split",
               "Volume: 15–20 working sets per muscle group per week (AAS allows higher MRV)",
               "Prioritize compound movements for anabolic stimulus; add isolation for detail/separation",
               "Keep workouts ≤75 minutes — cortisol spikes after 90 min actively opposes fat loss"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Cardio Protocol:</b>", s["SSH"]))
    for x in ["LISS (Low Intensity Steady State): 35–45 min fasted, 4–5×/week — primary fat-burning cardio",
               "Heart rate zone: 60–70% max HR (fat oxidation zone) — roughly 115–135 BPM for most adults",
               "HIIT: Maximum 2×/week — excessive HIIT in deficit causes muscle catabolism",
               "Step count target: 8,000–12,000 daily steps (NEAT significantly impacts total calorie burn)"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Nutrition Targets:</b>", s["SSH"]))
    rows=[["Macro","Target","Notes"],
          ["Calories","TDEE - 300 to -500 kcal","Aggressive deficits risk muscle catabolism even on AAS"],
          ["Protein","1.5–2.0 g/lb LBM","AAS dramatically increases nitrogen retention — protein utilization is enhanced; minimum 200g for 200lb athlete"],
          ["Carbohydrates","Timed around training","Reduce on rest days; carb cycle for adherence"],
          ["Fats","20–25% of calories","Never below 0.3 g/lb — fats are required for steroidogenesis and hormone production"],
          ["Water","4+ litres/day","Increases to 5–6L with Clenbuterol/T3 due to increased sweating and thermogenesis"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.14,0.24,0.62]]))

    items += sh("11. BLOOD WORK — WHAT TO TEST & WHEN", TK, s, "🩸")
    bw_rows=[["Timing","Tests Required","Action Triggers"],
             ["Pre-Cycle (Baseline)","Total T, Free T, LH, FSH, E2, Prolactin, CBC, CMP (liver/kidney), Lipids (LDL/HDL/Trigs), HbA1c, TSH, PSA","Do NOT start if ALT/AST >2× ULN, LDL >160, or hematocrit >50%"],
             ["Week 4 (On-Cycle)","E2, Prolactin, Hematocrit, ALT/AST","Stop orals if ALT >3× ULN. Adjust AI if E2 out of range. Donate blood if hematocrit >52%"],
             ["Week 8 (Mid-Cycle)","Full panel — same as baseline","Assess lipid changes; verify liver recovery between oral switches"],
             ["Week 12 (End of Cycle)","Full panel","Confirm baseline reference for PCT planning"],
             ["PCT Week 4","Total T, Free T, LH, FSH, E2","LH/FSH should be rising. Total T should be >200 ng/dL minimum"],
             ["4 Wks Post-PCT","Full panel","Total T target: pre-cycle baseline. If <300 ng/dL, extend recovery or consult physician"]]
    items.append(tbl(bw_rows[0],[r for r in bw_rows[1:]],TK,[(W-72)*f for f in [0.17,0.40,0.43]]))

    items += sh("12. SIDE EFFECT MANAGEMENT GUIDE", TK, s, "⚕")
    se_rows=[["Side Effect","Cause","Prevention","Treatment"],
             ["Acne (back/shoulders)","Androgen receptor stimulation of sebaceous glands","Shower immediately post-workout; use salicylic acid body wash; reduce androgens","Topical benzoyl peroxide; antibiotics (minocycline); Accutane for severe cases — post-cycle"],
             ["Hair Thinning/MPB","DHT and androgenic metabolites attacking genetically susceptible follicles","Topical Finasteride or Ketoconazole shampoo — do not use oral Finasteride on Tren cycles","Accept genetic predisposition; lower androgenic compounds if priority"],
             ["High Blood Pressure","Increased red blood cell production, sodium/water retention","Monitor BP twice weekly; limit sodium; Hawthorn Berry supplement","Reduce cycle dose; donate blood if hematocrit elevated; consider lisinopril if persistent"],
             ["Gynecomastia (Puffy Nipples)","Estrogen or Prolactin acting on breast tissue","Run AI proactively; run Caber for Tren; avoid starting cycle without AI on hand","Nolvadex 40mg/day immediately for E2-based gyno; Caber for prolactin-based gyno"],
             ["Insomnia / Night Sweats","Trenbolone-specific — unknown precise mechanism","Avoid late training; keep room cool; consider 100–200mg Diphenhydramine","Lower Tren dose; some athletes find splitting EOD dose helps"],
             ["Testicular Atrophy","HPT axis suppression — normal physiological response","HCG 500 IU 2×/week throughout cycle prevents significant atrophy","HCG in PCT reverses atrophy; resolves with successful PCT"]]
    items.append(tbl(se_rows[0],[r for r in se_rows[1:]],TK,[(W-72)*f for f in [0.17,0.18,0.30,0.35]]))
    items.append(Spacer(1,8))
    items.append(Paragraph("⚠ This guide is for educational purposes only. Always consult a licensed medical professional before beginning any hormonal protocol.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 02 — ADVANCED BULKING WITH PEPTIDES
# ════════════════════════════════════════════════════════════
def pdf_bulking(path):
    TK="bulking"; doc=new_doc(path); s=mk(TK); items=[]
    DISC="⚠ MEDICAL DISCLAIMER: Educational and informational purposes only. Consult a licensed physician before beginning any hormonal protocol."
    items += cover(["ADVANCED STEROID CYCLE","FOR BULKING WITH PEPTIDES","12–16 WEEK MASS PROTOCOL"],
                   "Testosterone · Nandrolone · Dianabol · IGF-1 LR3 · GHRP-6 · CJC-1295 · Full PCT",
                   "Maximum lean mass accumulation · GH pulse amplification · Peptide synergy",
                   TK, s, badges=["12–16 WEEKS","ADVANCED","MASS BUILDER","PEPTIDE STACK"],disclaimer=DISC)
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Mass Building Philosophy & Realistic Expectations","2.  Core Compound Stack & Mechanisms",
               "3.  12–16 Week Dosage Timeline","4.  Peptide Protocol — IGF-1 LR3, GHRP-6, CJC-1295 DAC",
               "5.  Optional HGH Addition","6.  AI & Prolactin Management",
               "7.  Post Cycle Therapy (PCT)","8.  Mass-Phase Nutrition Science",
               "9.  Training Programming for Maximum Hypertrophy","10. Essential Supplement Stack",
               "11. Blood Work Schedule","12. Common Mistakes & How to Avoid Them"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. MASS BUILDING PHILOSOPHY", TK, s, "🎯")
    items.append(Paragraph("This protocol is engineered to produce <b>maximum lean muscle mass</b> over 12–16 weeks by combining a powerful anabolic base with cutting-edge peptide technology that amplifies natural GH pulsatility. The philosophy is <b>synergistic overload</b> — each compound serves a distinct mechanism with minimal overlap.", s["BJ"]))
    items.append(rn("A landmark study published in the New England Journal of Medicine demonstrated that testosterone + resistance training produced significantly more lean mass than either alone, confirming the synergistic relationship between androgens and mechanical load.", TK, s))
    rows=[["Metric","12-Week Result","16-Week Result"],["Lean Mass Gain","12–18 lbs","18–28 lbs"],
          ["Strength Increase (Squat/Bench)","30–60 lbs","50–80 lbs"],["Body Fat Change","±2%","±2–4%"],
          ["Recovery Speed","40–60% improvement","40–60% improvement"],
          ["Peptide Synergy Benefit","Additional 10–20% lean mass vs AAS alone","Same"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.32,0.34,0.34]]))

    items += sh("2. CORE COMPOUND STACK & MECHANISMS", TK, s, "💊")
    comps=[["Testosterone Enanthate","Test E","500–750 mg","2 pins/wk","12–16 wks","Primary anabolic — stimulates AR, increases protein synthesis, IGF-1 production, and nitrogen retention. Enanthate ester = 7–8 day half-life; stable blood levels with twice-weekly dosing."],
           ["Nandrolone Decanoate","Deca","400–600 mg","Weekly","12–16 wks","19-nor androgen — superior nitrogen retention (higher than testosterone), collagen synthesis stimulation (joint healing), low androgenic side effects. Aromatizes mildly; elevates prolactin — requires Cabergoline."],
           ["Dianabol (Methandrostenolone)","Dbol","30–50 mg","Daily oral","Wks 1–6","Oral 17-alpha alkylated — rapid AR activation, dramatically increases glycogen uptake and nitrogen retention. Used as 'kick-start' while long-ester Test/Deca build up. Aromatizes heavily — AI mandatory."]]
    items.append(tbl(["Compound","Name","Dose","Frequency","Duration","Mechanism & Role"],[r for r in comps],TK,[(W-72)*f for f in [0.18,0.09,0.11,0.12,0.11,0.39]]))

    items += sh("3. 12–16 WEEK DOSAGE TIMELINE", TK, s, "📅")
    items.append(Paragraph("The protocol divides into 3 phases. The <b>Kick-Start Phase (Wks 1–6)</b> uses Dbol to rapidly elevate anabolic state while long esters build up. The <b>Main Mass Phase (Wks 7–12)</b> achieves peak anabolic environment. The optional <b>Extension Phase (Wks 13–16)</b> is for athletes aiming for maximum gains.", s["B"]))
    sched=[["Phase","Weeks","Test E/C (per wk)","Deca (per wk)","Oral Dbol + AI Protocol"],
           ["Kick-Start","1–2","500mg (250mg Mon+Thu)","400mg (Mon)","Dbol 30mg/day · Arimidex 0.5mg EOD · Caber 0.25mg Tue+Fri"],
           ["Kick-Start","3–4","500mg (250mg Mon+Thu)","400mg (Mon)","Dbol 40mg/day · same AI · strength rises rapidly"],
           ["Kick-Start","5–6","750mg (375mg Mon+Thu)","600mg (Mon)","Dbol 50mg/day · same AI · monitor liver (TUDCA mandatory)"],
           ["Main Mass","7–12","750mg (375mg Mon+Thu)","600mg (Mon)","Dbol stopped · Arimidex 0.5mg EOD · Caber 0.25mg Tue+Fri"],
           ["Extension*","13–14","500mg (250mg Mon+Thu)","400mg (Mon)","Arimidex 0.25mg EOD · Caber 0.25mg Tue+Fri · taper phase"],
           ["Extension*","15–16","500mg (250mg Mon+Thu)","— stopped","Arimidex 0.25mg EOD · Deca clearing · pre-PCT prep"]]
    items.append(tbl(sched[0],[r for r in sched[1:]],TK,[(W-72)*f for f in [0.14,0.09,0.20,0.18,0.39]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Day-Wise Weekly Injection & Dosing Schedule:</b>", s["SSH"]))
    day=[["Day","Test E/C","Deca","AI & Ancillary","Oral (Kick-Start Wks 1–6)"],
         ["Monday","375mg (Main) / 250mg (Kick)","400–600mg","Arimidex 0.5mg","Dbol 15–25mg with meal"],
         ["Tuesday","—","—","Cabergoline 0.25mg","Dbol 15–25mg with meal"],
         ["Wednesday","—","—","—","Dbol 15–25mg with meal"],
         ["Thursday","375mg (Main) / 250mg (Kick)","—","Arimidex 0.5mg","Dbol 15–25mg with meal"],
         ["Friday","—","—","Cabergoline 0.25mg","Dbol 15–25mg with meal"],
         ["Saturday","—","—","—","Dbol 15–25mg with meal"],
         ["Sunday","—","—","—","Dbol 15–25mg with meal"]]
    items.append(tbl(day[0],[r for r in day[1:]],TK,[(W-72)*f for f in [0.13,0.20,0.18,0.25,0.24]]))
    items.append(Paragraph("<i>After Wks 1–6: Remove Dbol. Continue Test E/C + Deca with same AI protocol through the main mass phase.</i>", s["DIS"]))
    items.append(PageBreak())

    items += sh("4. PEPTIDE PROTOCOL", TK, s, "🧬")
    items.append(Paragraph("Peptides work at a fundamentally different level than anabolic steroids — they modulate <b>endogenous GH release</b> from the pituitary, increase satellite cell proliferation, enhance nutrient partitioning, and accelerate recovery. Their use alongside AAS produces results that neither can achieve alone.", s["BJ"]))
    peps=[["IGF-1 LR3","Long R3 Insulin-Like Growth Factor-1","40–60 mcg post-workout","Training days only (5×/wk max)","4–6 wks on / 4 wks off","Binds IGF-1R with 3× greater affinity than native IGF-1; half-life ~20 hours vs 15 min for native IGF-1. Directly stimulates muscle cell hyperplasia (new cell creation) and hypertrophy simultaneously. Most powerful muscle-building peptide available."],
          ["GHRP-6","Growth Hormone Releasing Hexapeptide","100 mcg × 3/day","Fasted morning, pre-workout, pre-bed","Throughout cycle","Ghrelin receptor agonist — triggers acute GH pulse from pituitary. Each injection produces a natural GH spike within 30 min. Strong hunger stimulation (beneficial during bulk). Pair with CJC-1295 for amplified GH pulse (5–10× individual peptide effect)."],
          ["CJC-1295 DAC","Modified GHRH Analog with Drug Affinity Complex","2 mg once weekly","SC injection any time","Wks 1–12","GHRH analog with extended half-life (8 days due to DAC modification). Elevates baseline GH by 2–10× over normal physiological levels. Acts as a 'GH tide' beneath which GHRP-6 creates larger individual spikes."]]
    items.append(tbl(["Peptide","Full Name","Dose","Timing","Protocol","Mechanism & Effect"],[r for r in peps],TK,[(W-72)*f for f in [0.12,0.18,0.13,0.13,0.14,0.30]]))
    items.append(Paragraph("<b>Practical Injection Protocol:</b>", s["SSH"]))
    for x in ["Injection 1 (Morning, fasted): GHRP-6 100 mcg + CJC-1295 100 mcg (non-DAC, if using daily option) subcutaneously",
               "Injection 2 (Pre-workout, 60 min before): GHRP-6 100 mcg — amplifies intra-workout GH and IGF-1",
               "Injection 3 (Pre-bed, 2+ hrs after last meal): GHRP-6 100 mcg — capitalizes on sleep GH pulse",
               "IGF-1 LR3: 40–60 mcg IM (intramuscular) into the worked muscle, within 30 min post-training",
               "CJC-1295 DAC 2 mg SC once weekly — any consistent day"]:
        items.append(bl(x, s))
    items.append(wb("IGF-1 LR3 causes transient hypoglycemia. Always eat 20–30g carbohydrates before injecting. Have glucose tablets nearby. Never inject fasted.", TK, s))

    items += sh("5. OPTIONAL HGH ADDITION", TK, s, "⚡")
    items.append(Paragraph("Pharmaceutical-grade Human Growth Hormone can be added to the peptide stack for compounding benefits. HGH works via the same pituitary/IGF-1 axis but provides <b>exogenous</b> GH rather than stimulating endogenous production.", s["B"]))
    rows=[["HGH Quality","Source","Dose Range","Effect on IGF-1","Notes"],
          ["Pharmaceutical Grade","Prescription only","2–4 IU/day","IGF-1 rises 100–300 ng/mL","Gold standard — exact concentration; expensive"],
          ["Generic (176aa)","Research peptide suppliers","4–6 IU/day","Variable","Purity varies — test with kit before use"],
          ["Fragment 176-191","Peptide supplier","500 mcg/day","Minimal IGF-1 effect","Fat loss only; no anabolic benefit"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.17,0.18,0.14,0.18,0.33]]))
    for x in ["Optimal timing: 2 IU fasted morning + 2 IU early afternoon (avoids nighttime hypoglycemia)",
               "Monitor fasting glucose and HbA1c — HGH causes insulin resistance; kits should include extra insulin sensitivity supplements",
               "IGF-1 blood test target on HGH: 250–350 ng/mL — above 400 ng/mL increases acromegaly risk with long-term use"]:
        items.append(bl(x, s))

    items += sh("6. AI & PROLACTIN MANAGEMENT", TK, s, "🛡")
    items.append(Paragraph("Bulking protocols present unique estrogen management challenges. <b>Some estrogen elevation is actually desirable</b> during a mass phase — estrogen contributes to IGF-1 production, glycogen storage, and synovial joint fluid production. The target E2 for bulking is higher (35–50 pg/mL) than cutting (20–30 pg/mL).", s["BJ"]))
    items.append(rn("Research shows estradiol >50 pg/mL correlates with increased water retention and gynecomastia risk, while estradiol <15 pg/mL during a mass phase impairs IGF-1 signaling and reduces glycogen storage capacity — both counterproductive to muscle growth.", TK, s))
    for x in ["<b>Arimidex:</b> 0.5 mg twice weekly (Mon/Thu) — start conservative; adjust based on E2 blood work",
               "<b>Cabergoline:</b> 0.25 mg twice weekly — NON-NEGOTIABLE with Deca. Nandrolone activates progesterone and prolactin receptors; prolactin-induced gyno does not respond to Nolvadex",
               "Signs you need more AI: water weight, puffy nipples, high BP, lethargy, emotional blunting",
               "Signs you need less AI: joint cracking, low libido, depression, difficulty maintaining erection, poor pumps"]:
        items.append(bl(x, s))

    items += sh("7. POST CYCLE THERAPY (PCT)", TK, s, "🔄")
    items.append(wb("Deca-Durabolin has a half-life of approximately 15 days. PCT timing is critical: begin PCT 3–4 WEEKS after last Deca injection, and 2 weeks after last Test E/C injection. Starting PCT too early while Nandrolone is still active will suppress HPT axis recovery.", TK, s))
    pct=[["Compound","Dose","Timeline","Purpose & Mechanism"],
         ["HCG","1000 IU","Every 3 days for 3 wks pre-PCT","LH analog — directly stimulates Leydig cell testosterone production. Prevents permanent testicular desensitization. Run before SERM therapy begins."],
         ["Clomid","100 mg/day wk1, 50 mg/day wks2–4","4 weeks","SERM — blocks ER at pituitary/hypothalamus, removes negative feedback, dramatically increases GnRH → LH → FSH cascade. Most powerful SERM for HPT axis restart."],
         ["Nolvadex","40 mg/day wk1, 20 mg/day wks2–6","6 weeks","SERM — anti-estrogenic at breast tissue + pituitary. Lower suppressive risk than Clomid for mood. Preferred solo SERM for milder cases; combined with Clomid for heavy cycles."],
         ["Vitamin E (Tocopherol)","400 IU/day","Throughout PCT","Antioxidant — protects Leydig cells from oxidative damage during hormonal fluctuation; improves fertility markers during PCT"]]
    items.append(tbl(pct[0],[r for r in pct[1:]],TK,[(W-72)*f for f in [0.15,0.20,0.18,0.47]]))

    items += sh("8. MASS-PHASE NUTRITION SCIENCE", TK, s, "🍽")
    items.append(Paragraph("Nutrition is the foundation of mass building — anabolic compounds amplify your body's response to food, but they cannot create muscle from nothing. The mass-phase nutrition strategy optimizes <b>caloric surplus, protein synthesis windows, and insulin sensitivity</b>.", s["BJ"]))
    items.append(Paragraph("<b>Caloric Surplus Calculation:</b>", s["SSH"]))
    for x in ["Calculate TDEE: BMR (Mifflin-St Jeor) × Activity Factor (1.55 for moderate training)",
               "Mass phase surplus: +400–600 kcal above TDEE (lean bulk) or +600–1000 kcal (aggressive bulk)",
               "AAS reduces fat storage risk — larger surpluses are better tolerated than natural training",
               "Weigh weekly (same time, same conditions); adjust calories if gaining >1.5 lbs/week (excess fat)"]:
        items.append(bl(x, s))
    rows=[["Macro","Calculation","Example (200 lb Athlete)","Timing"],
          ["Protein","1.8–2.2 g/lb body weight","360–440 g/day","Evenly distributed — every 3–4 hours"],
          ["Carbohydrates","3–4 g/lb body weight","600–800 g/day","Majority around workouts; reduce at night"],
          ["Fats","0.5–0.8 g/lb body weight","100–160 g/day","Morning and evening; avoid peri-workout"],
          ["Total Calories","TDEE + 400–600","~3,800–4,200 kcal","Consistent daily intake"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.12,0.28,0.28,0.32]]))

    items += sh("9. TRAINING FOR MAXIMUM HYPERTROPHY", TK, s, "🏋")
    items.append(Paragraph("On AAS, your <b>Maximum Recoverable Volume (MRV)</b> significantly increases — you can train harder, more frequently, and recover faster. The key is exploiting this recovery advantage without crossing into overtraining, which even AAS cannot fully prevent.", s["BJ"]))
    for x in ["<b>Frequency:</b> Each muscle group 2–3×/week. AAS increases protein synthesis duration from 24–36 hrs (natural) to 48+ hours",
               "<b>Volume:</b> 20–25 sets/muscle/week (natural MRV ~15–20 sets; AAS extends this)",
               "<b>Progressive overload:</b> Add weight, reps, or sets every session — non-negotiable for mass gain",
               "<b>Rep ranges:</b> 5–8 reps for compound movements (neurological strength); 10–15 for isolation (metabolic hypertrophy)",
               "<b>Sleep:</b> 8–9 hours minimum — 70% of GH release occurs during deep sleep. Non-negotiable for maximizing peptide and HGH benefits"]:
        items.append(bl(x, s))

    items += sh("10. ESSENTIAL SUPPLEMENT STACK", TK, s, "💊")
    supps=[["TUDCA","500 mg/day","Liver protection for Dbol (oral 17-alpha alkylated compound); prevents cholestasis"],
           ["Milk Thistle","600 mg/day","Sylimarin complex — hepatoprotective, anti-inflammatory for liver"],
           ["Omega-3 (EPA+DHA)","5–6 g/day","Manages LDL/HDL ratio; anti-inflammatory; reduces AAS-induced dyslipidemia"],
           ["CoQ10 (Ubiquinol)","300 mg/day","Mitochondrial support; cardiovascular protection; energy production"],
           ["Creatine Monohydrate","5 g/day","Increases ATP production; 5–15% strength gain; improves high-rep performance on mass exercises"],
           ["Beta-Alanine","3.2 g/day","Increases muscle carnosine; buffers lactic acid; enables extra reps in 8–15 rep range"],
           ["Whey + Casein Protein","50–80 g/day total","Whey post-workout (fast); casein pre-bed (slow) — maximizes 24hr protein synthesis"],
           ["Zinc + Magnesium (ZMA)","Nightly","Improves sleep quality; supports testosterone production; cofactor for 300+ enzymatic reactions"],
           ["Vitamin D3 + K2","5000 IU + 100 mcg","Testosterone production cofactor; muscle function; immune regulation"],
           ["Glucosamine + Chondroitin","1500+1200 mg","Joint protection — heavy lifting + Deca on joints, but heavy loading still stresses cartilage"]]
    items.append(tbl(["Supplement","Dose","Evidence & Purpose"],[r for r in supps],TK,[(W-72)*f for f in [0.20,0.14,0.66]]))
    items.append(Spacer(1,8))
    items.append(Paragraph("⚠ For educational purposes only. Consult a licensed medical professional before beginning any hormonal protocol.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 03 — BEGINNER STEROID CYCLE
# ════════════════════════════════════════════════════════════
def pdf_beginner(path):
    TK="beginner"; doc=new_doc(path); s=mk(TK); items=[]
    DISC="⚠ MEDICAL DISCLAIMER: For educational purposes only. Anabolic steroids are controlled substances. Always consult a licensed physician."
    items += cover(["BEGINNER ANABOLIC","STEROID CYCLE","COMPLETE GUIDE"],
                   "Testosterone-Only Foundation · Safe Protocols · Full PCT · Side Effect Management",
                   "Evidence-based · Minimal risk · Maximum results for first cycles",
                   TK, s, badges=["8–12 WEEKS","BEGINNER","TESTOSTERONE ONLY","COMPLETE PCT"],disclaimer=DISC)
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  The Golden Rule — Why Testosterone Only","2.  Understanding How Anabolic Steroids Work",
               "3.  Testosterone Enanthate / Cypionate — Core Compound","4.  Optional Kick-Starter: Dianabol",
               "5.  8 vs 10 vs 12 Week Protocols — Which Is Right For You?","6.  Aromatase Inhibitor — Complete Guide",
               "7.  Recognizing & Managing Side Effects","8.  Post Cycle Therapy — The Most Critical Phase",
               "9.  Blood Work — Complete Testing Guide","10. Training Program for Beginners on Cycle",
               "11. Nutrition Blueprint — Eating for Growth","12. Supplement Stack"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. THE GOLDEN RULE — WHY TESTOSTERONE ONLY", TK, s, "📖")
    items.append(Paragraph("Every first cycle should be <b>Testosterone only</b>. This is not a suggestion — it is the most important rule in anabolic steroid use for beginners. Here is the science and logic behind it:", s["BJ"]))
    items.append(rn("Testosterone was the first anabolic steroid synthesized (1935, Ruzicka & Butenandt). Every other anabolic steroid is a structural modification of testosterone. Your body naturally produces testosterone — making it the most understood, most researched, and most predictable compound available.", TK, s))
    for x in ["<b>Isolation principle:</b> With one compound, any side effect you experience is immediately identifiable. Add multiple compounds and you cannot know which caused which reaction",
               "<b>Maximum response:</b> Beginners respond more dramatically to first cycles than advanced users. You will gain 15–25 lbs on testosterone alone — more compounds do not improve beginner results significantly",
               "<b>Reversibility:</b> A testosterone-only cycle with proper PCT is the most recoverable AAS protocol. More complex stacks suppress the HPT axis more severely",
               "<b>Establish your AI dose:</b> Every person aromatizes differently. Testosterone only lets you find your exact AI requirement before adding more variables",
               "<b>Baseline biomarkers:</b> First cycle establishes how your liver, lipids, and hormones respond — critical data for future protocols"]:
        items.append(bl(x, s))

    items += sh("2. HOW ANABOLIC STEROIDS WORK — THE SCIENCE", TK, s, "🔬")
    items.append(Paragraph("Understanding the mechanism helps you make informed decisions, recognize side effects early, and manage your cycle intelligently.", s["B"]))
    items.append(Paragraph("<b>The Androgen Receptor (AR) Pathway:</b>", s["SSH"]))
    for x in ["Testosterone enters the cell and binds to the androgen receptor (AR) in the cytoplasm",
               "The testosterone-AR complex translocates to the nucleus and binds to Androgen Response Elements (AREs) on DNA",
               "This activates transcription of muscle-specific genes: myosin heavy chain, actin, IGF-1, and more",
               "Result: increased protein synthesis, nitrogen retention, and satellite cell activation",
               "Also reduces catabolic gene expression — your body degrades muscle protein more slowly"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Why Supraphysiological Doses Build More Muscle:</b>", s["SSH"]))
    items.append(Paragraph("Natural testosterone levels peak at 400–800 ng/dL. At 500 mg/week of Test E, blood levels reach approximately 2,000–3,500 ng/dL. This 3–5× supraphysiological level saturates and overstimulates androgen receptors, driving protein synthesis at rates impossible to achieve naturally.", s["BJ"]))
    items.append(rn("The landmark Bhasin study (1996, NEJM) demonstrated men given 600mg testosterone/week for 10 weeks gained 13 lbs of lean mass with NO exercise — compared to 4 lbs in natural trainees WITH exercise. This definitively established the dose-response relationship between testosterone and muscle mass.", TK, s))

    items += sh("3. TESTOSTERONE ENANTHATE/CYPIONATE — COMPLETE BREAKDOWN", TK, s, "💊")
    rows=[["Property","Testosterone Enanthate","Testosterone Cypionate"],
          ["Ester","Enanthic acid (C7)","Cypionate acid (C8)"],
          ["Half-Life","7–8 days","8–10 days"],
          ["Injection Frequency","2× weekly (e.g., Mon/Thu)","2× weekly or once weekly"],
          ["Time to Steady State","~3.5 weeks","~4 weeks"],
          ["Common Brands","Generic, Testoviron","Depo-Testosterone, generic"],
          ["Interchangeable?","Yes — nearly identical","Yes — nearly identical"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.28,0.36,0.36]]))
    items.append(Paragraph("<b>Dosage by Experience Level:</b>", s["SSH"]))
    dose_rows=[["Experience","Weekly Dose","Expected Lean Gain","Notes"],
               ["True beginner (1st ever cycle)","300 mg/wk","12–15 lbs","Minimal side effects; excellent results; establish response"],
               ["Intermediate beginner (2nd cycle)","400 mg/wk","15–20 lbs","Balanced risk/reward; well-tolerated by most"],
               ["Advanced beginner (3rd+ cycle)","500 mg/wk","18–25 lbs","Maximum beginner benefit; manage AI carefully"]]
    items.append(tbl(dose_rows[0],[r for r in dose_rows[1:]],TK,[(W-72)*f for f in [0.28,0.17,0.18,0.37]]))

    items += sh("4. OPTIONAL KICK-STARTER: DIANABOL", TK, s, "⚡")
    items.append(Paragraph("Testosterone Enanthate/Cypionate takes 3–4 weeks to reach therapeutic blood levels (due to the long ester). Some athletes add <b>Dianabol</b> for the first 4–6 weeks to feel immediate effects while the long ester builds up. This is optional and <b>not recommended for a true first cycle</b>.", s["B"]))
    items.append(wb("Do not add Dianabol to your FIRST ever cycle. Run testosterone only first to establish your response to AAS before adding another compound. Dianabol causes significant liver stress and requires additional supplements.", TK, s))
    for x in ["Dose if added: 20–30 mg/day split into 2–3 doses with meals",
               "Duration: Weeks 1–6 ONLY (oral AAS should not exceed 6–8 weeks continuously)",
               "Expect rapid weight gain (5–12 lbs in 3 weeks) — mix of muscle, glycogen, and water",
               "Water weight will decrease when Dbol is discontinued — this is normal and expected",
               "Mandatory additions with Dbol: TUDCA 500mg/day + increase AI dose due to higher aromatization"]:
        items.append(bl(x, s))

    items += sh("5. PROTOCOL SELECTION — 8 vs 10 vs 12 WEEKS", TK, s, "📅")
    prot_rows=[["Protocol","Stack","PCT Start","Best For"],
               ["8-Week (Conservative)","300–400mg Test E, optional Dbol wks 1–4","14–16 days after last injection","Absolute beginners; minimal suppression; fastest recovery"],
               ["10-Week (Recommended)","400–500mg Test E, optional Dbol wks 1–6","14–16 days after last injection","Best balance of results vs recovery; recommended for most"],
               ["12-Week (Extended)","400–500mg Test E, optional Dbol wks 1–6","14–18 days after last injection","Maximum gains; longer recovery needed; experienced beginners"]]
    items.append(tbl(prot_rows[0],[r for r in prot_rows[1:]],TK,[(W-72)*f for f in [0.19,0.35,0.21,0.25]]))
    items.append(Spacer(1,4))
    sched=[["Weeks","Test E/C (2×/wk)","Dbol (optional)","Arimidex (EOD)","Notes"],
           ["1–2","150–250mg Mon + 150–250mg Thu","20mg/day with meals","0.5mg every other day","Start AI from day 1; assess tolerance"],
           ["3–4","150–250mg Mon + 150–250mg Thu","30mg/day with meals","0.5mg every other day","Blood work optional at Wk 4; note any symptoms"],
           ["5–6","150–250mg Mon + 150–250mg Thu","30mg/day with meals","0.5mg every other day","Stop Dbol end of Wk 6; liver enzymes normalise"],
           ["7–10","150–250mg Mon + 150–250mg Thu","— stopped","0.5mg every other day","Core training weeks; prioritise progressive overload"],
           ["11–12","150–250mg Mon + 150–250mg Thu","—","0.5mg every other day","Final weeks; prepare nutrition + PCT supplies"]]
    items.append(tbl(sched[0],[r for r in sched[1:]],TK,[(W-72)*f for f in [0.09,0.25,0.20,0.18,0.28]]))
    items.append(Spacer(1,6))
    items.append(Paragraph("<b>Day-Wise Weekly Dosing Schedule (Testosterone Twice-Weekly Protocol):</b>", s["SSH"]))
    day=[["Day","Test E/C Injection","AI (Arimidex)","Oral Dbol (if using)","Notes"],
         ["Monday","YES — 150–250mg (Pin 1 of 2)","0.5mg (take with meal)","15mg with breakfast","Inject glute or quad; rotate sites"],
         ["Tuesday","—","—","15mg with breakfast","Rest or cardio day"],
         ["Wednesday","—","0.5mg (EOD from Mon)","15mg with breakfast","AI dose falls here if EOD"],
         ["Thursday","YES — 150–250mg (Pin 2 of 2)","0.5mg (take with meal)","15mg with breakfast","Second injection; maintain 3–4 day gap"],
         ["Friday","—","—","15mg with breakfast","Training day — strength should be elevated"],
         ["Saturday","—","0.5mg (EOD from Thu)","15mg with breakfast","AI dose; active recovery"],
         ["Sunday","—","—","—","Rest day; prep food and supplements for week"]]
    items.append(tbl(day[0],[r for r in day[1:]],TK,[(W-72)*f for f in [0.12,0.22,0.18,0.20,0.28]]))
    items.append(Paragraph("<i>Tip: Set phone reminders for injection days (Mon + Thu) and AI days (Mon, Wed, Fri, Sun for EOD) to avoid missed doses.</i>", s["DIS"]))
    items.append(PageBreak())

    items += sh("6. AROMATASE INHIBITOR — COMPLETE GUIDE", TK, s, "🛡")
    items.append(Paragraph("<b>Aromatization</b> is the conversion of testosterone to estradiol (E2) by the enzyme aromatase (CYP19A1), found primarily in fat cells, liver, brain, and muscle. At supraphysiological testosterone doses, aromatization increases proportionally — making AI use necessary for most men.", s["BJ"]))
    items.append(rn("Approximately 0.3% of testosterone is converted to estradiol in healthy males. At 500mg/week testosterone, aromatization can produce 3–5× normal estradiol levels without AI intervention. Individual aromatization rate varies significantly based on body fat percentage and genetic factors.", TK, s))
    items.append(Paragraph("<b>Signs of HIGH estrogen (over-aromatization):</b>", s["SSH"]))
    for x in ["Gynecomastia — puffy, tender, or itchy nipples (glandular tissue forming under nipple)",
               "Water retention — smooth, bloated appearance; elevated blood pressure",
               "Mood instability — emotional, anxious, irritable; similar to PMS symptoms",
               "Erection difficulty — ED despite high testosterone is often caused by high E2",
               "Fatigue and sluggishness"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Signs of LOW estrogen (over-suppression with AI):</b>", s["SSH"]))
    for x in ["Joint pain and cracking — estrogen lubricates joints; crash causes intense joint discomfort",
               "Very low libido and erectile dysfunction — estrogen is pro-sexual for men in optimal range",
               "Depression, anxiety, cognitive fog",
               "Poor workout pumps — estrogen helps glycogen storage and muscle fullness"]:
        items.append(bl(x, s))
    ai_rows=[["AI Option","Mechanism","Starting Dose","Adjustment"],
             ["Arimidex (Anastrozole) — Recommended","Reversible competitive inhibitor of aromatase","0.5 mg EOD","Increase to 0.5 mg/day if E2 high; decrease to 0.25 mg EOD if low"],
             ["Aromasin (Exemestane)","Suicidal/irreversible aromatase inactivator","12.5 mg EOD","12.5 mg/day if E2 high; 12.5 mg E3D if low"],
             ["Letrozole (Letro)","Most potent AI — use only for gyno emergencies","2.5 mg/day (short-term only)","NOT for routine cycle management — can crash E2 rapidly"]]
    items.append(tbl(ai_rows[0],[r for r in ai_rows[1:]],TK,[(W-72)*f for f in [0.25,0.28,0.18,0.29]]))

    items += sh("7. SIDE EFFECTS — RECOGNITION & MANAGEMENT", TK, s, "⚕")
    se=[["Side Effect","Probability","Early Signs","Intervention"],
        ["Acne","High (70–80%)","Breakouts on back, shoulders, chest","Salicylic acid wash daily; benzoyl peroxide topical; reduce androgens; Accutane post-cycle for severe"],
        ["Hair Loss (MPB)","Genetic (20–40%)","Increased shedding; hairline recession","Topical Finasteride 0.025% solution; Nizoral 2% shampoo 2×/wk; accept genetic risk"],
        ["Water Retention","High (60–80%)","Puffiness in face/extremities; weight gain >1.5 lbs/wk","Reduce AI dose if caused by low E2; low sodium diet; adequate hydration (counterintuitive but helps)"],
        ["Gynecomastia","Moderate (20–30%)","Puffy/sensitive nipples","Nolvadex 20mg/day immediately; add/increase AI"],
        ["Elevated BP","Moderate (30–50%)","BP >130/85 consistently","Monitor weekly; reduce sodium; add Hawthorn Berry; consult doctor if >140/90"],
        ["Mood Changes","Moderate (20–40%)","Increased irritability or aggression","Usually dose-dependent; communicate with partner/family; lower dose if severe"]]
    items.append(tbl(se[0],[r for r in se[1:]],TK,[(W-72)*f for f in [0.17,0.14,0.24,0.45]]))

    items += sh("8. POST CYCLE THERAPY — THE MOST CRITICAL PHASE", TK, s, "🔄")
    items.append(Paragraph("PCT is often neglected or done poorly — this is the most common mistake in AAS use. <b>Failing PCT leads to prolonged low testosterone</b>, which causes loss of all cycle gains, depression, lethargy, sexual dysfunction, and potentially permanent hypogonadism in extreme cases.", s["BJ"]))
    items.append(Paragraph("<b>PCT Start Timing (for Testosterone Enanthate/Cypionate):</b>", s["SSH"]))
    items.append(Paragraph("Wait <b>14–18 days</b> after your last injection before starting SERMs. The long ester must clear before SERMs can work — starting too early means the exogenous testosterone still suppresses your HPT axis while SERMs try to restart it.", s["B"]))
    pct=[["Compound","Weeks 1–2","Weeks 3–4","Notes"],
         ["Clomid (Clomiphene)","50 mg/day","50 mg/day","Primary LH/FSH stimulator — most powerful SERM for HPT restart. May cause visual disturbances (blurry vision) — stop immediately if this occurs"],
         ["Nolvadex (Tamoxifen)","20 mg/day","20 mg/day","Anti-estrogenic SERM — synergistic with Clomid; also protects breast tissue"],
         ["HCG (optional)","500 IU E3D (2 wks BEFORE PCT)","Stop at PCT start","Restores testicular size and sensitivity; start 2 weeks after last injection, run for 2 weeks, then begin Clomid/Nolvadex"]]
    items.append(tbl(pct[0],[r for r in pct[1:]],TK,[(W-72)*f for f in [0.22,0.18,0.18,0.42]]))
    items.append(rn("Post-PCT blood work target: Total Testosterone >400 ng/dL, LH >2 mIU/mL, FSH >2 mIU/mL. If values remain suppressed 8 weeks post-PCT, consult an endocrinologist regarding TRT evaluation.", TK, s))

    items += sh("9–12. BLOOD WORK, TRAINING, NUTRITION & SUPPLEMENTS", TK, s, "📊")
    items.append(Paragraph("<b>Minimum Blood Work Protocol:</b>", s["SSH"]))
    bw=[["When","Tests"],["Pre-cycle (baseline)","CBC, CMP (liver/kidney), Lipids, Total T, Free T, LH, FSH, E2, Prolactin, TSH, PSA"],
        ["Week 4 on-cycle","E2, Hematocrit, ALT/AST"],["End of cycle (Week 10–12)","Full panel"],
        ["PCT Week 4","Total T, LH, FSH, E2"],["8 wks post-PCT","Full panel — confirm recovery"]]
    items.append(tbl(bw[0],[r for r in bw[1:]],TK,[(W-72)*f for f in [0.25,0.75]]))
    items.append(Paragraph("<b>Training Split:</b> Push/Pull/Legs 5–6 days/week. Focus on compound movements (squat, deadlift, bench, row, OHP). Progressive overload every session. Sleep 8+ hours.", s["B"]))
    items.append(Paragraph("<b>Nutrition:</b> +300–500 kcal surplus. Protein: 1.5–2.0 g/lb body weight minimum. Carbohydrates: primary energy source around workouts. Fats: 20–25% of calories. Water: 3–4 litres/day.", s["B"]))
    supps=[["TUDCA","500 mg/day","Liver protection (essential with Dbol)"],
           ["Milk Thistle","600 mg/day","Hepatoprotective antioxidant"],
           ["Omega-3","4 g/day","Cardiovascular & lipid management"],
           ["Creatine","5 g/day","Strength + recovery"],
           ["Vitamin D3+K2","5000 IU+100 mcg","Testosterone production & bone health"],
           ["ZMA","Nightly","Sleep quality + hormonal support"],
           ["Blood Pressure Monitor","—","Check BP twice weekly throughout cycle"]]
    items.append(tbl(["Supplement","Dose","Purpose"],[r for r in supps],TK,[(W-72)*f for f in [0.22,0.14,0.64]]))
    items.append(Spacer(1,8)); items.append(Paragraph("⚠ Educational purposes only. Always consult a licensed physician.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 04 — 30-DAY KETO INDIAN VEGETARIAN
# ════════════════════════════════════════════════════════════
def pdf_keto(path):
    TK="keto"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["30-DAY WEIGHT LOSS","TRANSFORMATION PLAN","KETO INDIAN VEGETARIAN"],
                   "4-Week Ketogenic Protocol · Week-by-Week Menus · 6 Full Recipes · Exercise Plan",
                   "Science-backed fat loss · Indian ingredients · Sustainable & delicious",
                   TK, s, badges=["30 DAYS","VEGETARIAN","KETO SCIENCE","6 RECIPES"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  The Science of Ketogenic Dieting","2.  Indian Vegetarian Keto — Adapting the Protocol",
               "3.  Week 1 — Transition Phase (Days 1–7)","4.  Week 2 — Entering Ketosis (Days 8–14)",
               "5.  Week 3 — Deep Ketosis (Days 15–21)","6.  Week 4 — Maintenance (Days 22–30)",
               "7.  Complete Recipe Collection (6 Recipes)","8.  Exercise Protocol",
               "9.  Foods to Eat, Limit & Avoid","10. Supplement Stack for Keto Success",
               "11. Troubleshooting — Common Problems & Solutions","12. Expected Results & Progress Tracking"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. THE SCIENCE OF KETOGENIC DIETING", TK, s, "🔬")
    items.append(Paragraph("The ketogenic diet is a high-fat, moderate-protein, very-low-carbohydrate dietary pattern that induces a metabolic state called <b>ketosis</b>. In ketosis, the liver converts fatty acids into <b>ketone bodies</b> (primarily beta-hydroxybutyrate, acetoacetate, and acetone) which serve as an alternative fuel for the brain and muscles.", s["BJ"]))
    items.append(rn("Multiple meta-analyses (Johnston 2006, Bueno 2013, Gibson 2015) demonstrate ketogenic diets produce greater short-term fat loss compared to low-fat diets, with superior effects on appetite suppression via reduced ghrelin levels and increased satiety hormones.", TK, s))
    items.append(Paragraph("<b>Why Keto Works for Fat Loss:</b>", s["SSH"]))
    for x in ["<b>Reduced insulin levels:</b> Carbohydrate restriction drops insulin dramatically — insulin's primary role is fat storage. Low insulin = fat burning mode",
               "<b>Increased fat oxidation:</b> With glucose unavailable, cells upregulate fat-burning enzymes; mitochondrial fat oxidation increases 2–3×",
               "<b>Appetite suppression:</b> Ketones suppress ghrelin (hunger hormone); high fat + protein meals provide superior satiety",
               "<b>Water weight reduction:</b> Every gram of glycogen is stored with ~3g of water. Depleting glycogen removes 5–10 lbs of water in Week 1",
               "<b>Preserved muscle mass:</b> Adequate protein intake + ketones as muscle fuel prevents catabolism better than low-calorie low-carb diets"]:
        items.append(bl(x, s))
    rows=[["Macro","Standard Diet","Ketogenic Diet","Physiological Effect"],
          ["Carbohydrates","50–55%","5% (20–25g net/day)","Glucose depleted → ketosis triggered in 2–4 days"],
          ["Fats","30–35%","65–75%","Primary fuel source; supports fat-soluble vitamins"],
          ["Protein","15–20%","20–25%","Preserved muscle mass; gluconeogenesis minimal"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.18,0.17,0.22,0.43]]))

    items += sh("2. INDIAN VEGETARIAN KETO — THE ADAPTATION", TK, s, "🌿")
    items.append(Paragraph("Traditional Indian vegetarian diets are naturally <b>high in carbohydrates</b> — rice, roti, dal, and lentils are staples. Adapting to keto requires strategic substitutions that preserve authentic Indian flavours using familiar spices and cooking methods.", s["BJ"]))
    sub_rows=[["Traditional Indian Food","Keto Substitute","Macros Comparison"],
              ["White rice (1 cup = 45g carbs)","Cauliflower rice (1 cup = 5g net carbs)","90% carb reduction; same volume and texture"],
              ["Wheat roti (1 = 15g carbs)","Almond flour roti (1 = 3g net carbs)","80% carb reduction; similar texture"],
              ["Dal (moong, 1 cup = 38g carbs)","Paneer (100g = 1.2g carbs)","High protein, zero carbs replacement"],
              ["Idli (2 = 30g carbs)","Paneer bhurji (same calories = 2g carbs)","Better protein-to-carb ratio"],
              ["Potato sabzi (1 cup = 30g carbs)","Cauliflower/Broccoli sabzi (1 cup = 6g carbs)","80% carb reduction; same cooking method"],
              ["Cow's milk chai (1 cup = 12g carbs)","Almond/coconut milk chai (1 cup = 2g carbs)","83% carb reduction; rich flavour maintained"]]
    items.append(tbl(sub_rows[0],[r for r in sub_rows[1:]],TK,[(W-72)*f for f in [0.28,0.28,0.44]]))

    items += sh("3. WEEK 1 — TRANSITION PHASE (DAYS 1–7)", TK, s, "🌅")
    items.append(Paragraph("<b>Goal:</b> Reduce carbohydrates to 50g/day (not immediate zero — minimizes keto flu severity). The body is adapting from glucose metabolism to fat metabolism. Expect some fatigue, headaches, and cravings on Days 3–5 — this is the <b>keto flu</b>, a temporary adaptation response.", s["B"]))
    items.append(wb("Keto flu symptoms (fatigue, headache, brain fog, irritability) are caused by electrolyte depletion — not carb withdrawal. They are PREVENTED by aggressive electrolyte supplementation from Day 1.", TK, s))
    w1=[["Day","Breakfast","Lunch","Dinner","Snack"],
        ["1–2","Paneer Bhurji (200g paneer, ghee, capsicum, spices) + masala chai (almond milk)","Palak paneer (no cream gravy) + 1 small almond flour roti","Cauliflower rice + mushroom-coconut curry","10 almonds + green tea"],
        ["3–4","Methi thepla (almond flour, methi, ghee, ajwain) + pickle","Tofu stir-fry with coconut oil + zucchini noodles","Egg/paneer curry (no potato) + cauliflower mash","Paneer cubes + chaat masala"],
        ["5–7","Avocado + 2 eggs (if lacto-ovo) or paneer on almond bread","Broccoli + paneer sabzi with ghee tadka","Spinach soup + grilled paneer tikka + salad","Roasted pumpkin seeds (30g)"]]
    items.append(tbl(w1[0],[r for r in w1[1:]],TK,[(W-72)*f for f in [0.07,0.24,0.24,0.24,0.21]]))

    items += sh("4. WEEK 2 — ENTERING KETOSIS (DAYS 8–14)", TK, s, "🔥")
    items.append(Paragraph("<b>Goal:</b> Reduce net carbs to 20–25g/day. By Days 10–12, most individuals achieve measurable ketosis. <b>Signs of ketosis:</b> slightly sweet/fruity breath (acetone), reduced hunger, improved mental clarity, stable energy without blood sugar crashes, and mild diuresis.", s["B"]))
    items.append(Paragraph("Test ketosis with urine strips (Ketostix) or blood ketone meter. <b>Target: 0.5–3.0 mmol/L</b> (nutritional ketosis). Above 3.0 mmol/L indicates very deep ketosis — reduce fat slightly if eating too much.", s["B"]))
    w2=[["Day","Breakfast","Lunch","Dinner"],
        ["8–10","Keto masala omelette (3 eggs/paneer, vegetables, ghee) + chai","Palak paneer (no gravy) + cauliflower rice","Zucchini noodles + avocado-coconut sauce + grilled paneer"],
        ["11–14","Chia seed pudding (coconut milk, seeds, cinnamon, stevia)","Mixed vegetable stir-fry (broccoli, capsicum, mushroom) + paneer","Paneer tikka (grilled, no cream sauce) + mint chutney + salad"]]
    items.append(tbl(w2[0],[r for r in w2[1:]],TK,[(W-72)*f for f in [0.08,0.31,0.31,0.30]]))
    items.append(PageBreak())

    items += sh("5. WEEK 3 — DEEP KETOSIS (DAYS 15–21)", TK, s, "⚡")
    items.append(Paragraph("<b>Goal:</b> Maintain 20g net carbs/day. By Week 3, you are <b>fat-adapted</b> — your mitochondria have upregulated fat oxidation enzymes, you experience stable energy throughout the day, exercise performance normalizes (after Week 2 dip), and hunger is significantly reduced.", s["B"]))
    w3=[["Day","Breakfast","Lunch","Dinner"],
        ["15–17","Almond flour paratha + ghee + paneer filling","Paneer tikka masala (low-carb coconut gravy) + broccoli","Egg drop soup / paneer soup + roasted flaxseeds"],
        ["18–21","Coconut milk smoothie (spinach, protein, coconut cream, seeds)","Methi paneer bhurji + cucumber salad (olive oil dressing)","Baked stuffed capsicum (paneer, herbs, cheese)"]]
    items.append(tbl(w3[0],[r for r in w3[1:]],TK,[(W-72)*f for f in [0.08,0.31,0.31,0.30]]))

    items += sh("6. WEEK 4 — MAINTENANCE (DAYS 22–30)", TK, s, "🌟")
    items.append(Paragraph("<b>Goal:</b> Consolidate fat-adapted state and discover your personal carb tolerance. Slowly increase net carbs from 20g → 25–30g/day. Some people find 30g/day maintains ketosis; others need to stay below 20g. This week establishes your sustainable long-term keto baseline.", s["B"]))
    w4=[["Day","Breakfast","Lunch","Dinner"],
        ["22–25","Keto upma (cauliflower, mustard seeds, curry leaves, ghee)","Dal makhani (small portion, 50g black lentils) + salad","Stuffed bell peppers (paneer, herbs, cheese)"],
        ["26–30","Smoothie bowl (coconut yogurt, nuts, seeds, ½ cup berries)","Paneer steak + sautéed spinach + ghee drizzle","Green vegetable soup + almond bread + nut butter"]]
    items.append(tbl(w4[0],[r for r in w4[1:]],TK,[(W-72)*f for f in [0.08,0.31,0.31,0.30]]))

    items += sh("7. COMPLETE RECIPE COLLECTION", TK, s, "📖")
    recipes=[
        ("PANEER BHURJI","Prep: 5 min  Cook: 10 min  Serves: 2  |  Macros: ~320 kcal · 22g protein · 24g fat · 4g net carbs",
         ["200g paneer (fresh, crumbled)","1 tbsp ghee","½ tsp cumin seeds","1 green chilli, chopped","½ cup capsicum (diced)","Turmeric, coriander, salt to taste","Fresh coriander to garnish"],
         ["Heat ghee; splutter cumin seeds","Add chilli, capsicum; sauté 2 min","Add crumbled paneer; season with spices","Cook 5 min on medium heat; garnish with coriander"]),
        ("CAULIFLOWER RICE + MUSHROOM CURRY","Prep: 10 min  Cook: 20 min  Serves: 2  |  Macros: ~380 kcal · 10g protein · 34g fat · 8g net carbs",
         ["1 large cauliflower (grated)","250g mushrooms (sliced)","2 tbsp coconut oil","1 cup coconut cream","1 tsp each: cumin, coriander, turmeric, garam masala","Garlic-ginger paste, salt, coriander"],
         ["Sauté grated cauliflower in 1 tbsp oil 5 min; season with salt; set aside","Heat 1 tbsp oil; fry garlic-ginger paste 1 min","Add spices; stir 30 sec; add mushrooms; cook until golden (5–7 min)","Add coconut cream; simmer 5 min; serve over cauliflower rice"]),
        ("KETO ALMOND FLOUR PARATHA","Prep: 10 min  Cook: 15 min  Makes: 4  |  Macros: ~210 kcal · 6g protein · 18g fat · 3g net carbs each",
         ["1 cup almond flour (blanched)","2 tbsp psyllium husk","1 tbsp ghee + extra for cooking","½ tsp ajwain (carom seeds)","Salt to taste","4–5 tbsp warm water"],
         ["Mix almond flour, psyllium husk, ajwain, salt","Add ghee; mix until crumbly","Add warm water gradually; form soft pliable dough","Roll between parchment sheets; cook on medium tawa 2 min per side with ghee"]),
        ("ZUCCHINI NOODLES + AVOCADO SAUCE","Prep: 10 min  Serves: 2  |  Macros: ~280 kcal · 6g protein · 26g fat · 5g net carbs",
         ["2 medium zucchini (spiralized)","1 ripe avocado","2 tbsp olive oil","Juice of 1 lemon","2 garlic cloves","Salt, pepper, fresh basil"],
         ["Blend avocado, olive oil, lemon, garlic until smooth sauce","Lightly sauté zucchini noodles 2 min OR serve raw for crunch","Toss noodles with avocado sauce; season; serve immediately"]),
        ("PANEER TIKKA","Prep: 2 hrs marination  Cook: 15 min  Serves: 2  |  Macros: ~340 kcal · 24g protein · 26g fat · 4g net carbs",
         ["200g paneer (cubed)","3 tbsp thick yogurt or coconut yogurt","1 tsp each: cumin, coriander, garam masala, chilli powder","Lemon juice, salt","Capsicum + onion chunks (optional)"],
         ["Marinate paneer in yogurt + spices for 2+ hours (overnight is best)","Thread on skewers with vegetables","Grill, air-fry (200°C, 12 min), or bake (220°C, 15 min) until charred","Serve with mint chutney"]),
        ("KETO UPMA","Prep: 5 min  Cook: 12 min  Serves: 2  |  Macros: ~190 kcal · 7g protein · 15g fat · 5g net carbs",
         ["2 cups cauliflower (grated fine)","1 tsp mustard seeds","Curry leaves, green chilli, ginger","1 tbsp ghee","Salt, turmeric to taste","Fresh coriander"],
         ["Heat ghee; splutter mustard seeds and curry leaves","Add green chilli, ginger; sauté 30 sec","Add grated cauliflower; mix well with spices","Cook on medium heat 8–10 min; stir regularly; garnish with coriander"]),
    ]
    for rname, rinfo, ing, method in recipes:
        block=[Paragraph(f"<b>► {rname}</b>", s["SSH"]),
               Paragraph(rinfo, s["DIS"]),
               Paragraph("<b>Ingredients:</b>", s["B"])]
        for i in ing: block.append(bl(i, s))
        block.append(Paragraph("<b>Method:</b>", s["B"]))
        for n,m in enumerate(method): block.append(bl(f"Step {n+1}: {m}", s))
        block.append(Spacer(1,4))
        items.append(KeepTogether(block))

    items += sh("8. EXERCISE PROTOCOL", TK, s, "🏃")
    ex=[["Type","Frequency","Duration","Protocol"],
        ["Brisk Walking / LISS Cardio","4–5×/week","30–40 min","Target 60–65% max heart rate — primary fat-burning zone on keto"],
        ["Strength Training","3×/week","40–50 min","Compound movements: squats, deadlifts, push-ups, rows — preserves muscle"],
        ["Yoga / Flexibility","Daily","20–30 min","Morning yoga reduces cortisol — high cortisol impairs fat loss and disrupts ketosis"],
        ["HIIT (optional)","1–2×/week","15–20 min","Only in Weeks 3–4 when fat-adapted; avoid in Week 1–2"]]
    items.append(tbl(ex[0],[r for r in ex[1:]],TK,[(W-72)*f for f in [0.22,0.14,0.12,0.52]]))

    items += sh("9–12. FOODS, SUPPLEMENTS, TROUBLESHOOTING & RESULTS", TK, s, "📊")
    items.append(Paragraph("<b>Foods to Eat Freely:</b> Paneer, tofu, ghee, coconut oil, olive oil, butter, all leafy greens (spinach, methi, palak), broccoli, cauliflower, zucchini, capsicum, mushrooms, almonds, walnuts, chia seeds, pumpkin seeds, flaxseeds", s["B"]))
    items.append(Paragraph("<b>Foods to Limit:</b> Full-fat yogurt (count carbs), onions (use small amounts), tomatoes (limit to 2 tbsp), berries (50g max), cashews (max 10/day)", s["B"]))
    items.append(Paragraph("<b>Foods to AVOID Completely:</b> Rice, wheat flour, all bread/pasta, all dal/legumes (in large quantities), potatoes, all sugar, jaggery, honey, packaged snacks, fruit juice, sodas", s["B"]))
    items.append(Paragraph("<b>Essential Supplements for Keto:</b>", s["SSH"]))
    ksupp=[["Supplement","Dose","Why Critical on Keto"],
           ["Sodium (salt)","Add ½ tsp pink salt to water daily","Keto causes rapid sodium excretion; deficiency causes keto flu, headaches, cramping"],
           ["Magnesium Glycinate","300–400 mg nightly","Keto depletes magnesium; deficiency causes insomnia, muscle cramps, anxiety"],
           ["Potassium","1000–3500 mg from food or supplement","Heart rhythm regulation; depleted by keto diuresis"],
           ["MCT Oil","1–2 tbsp/day","Instantly converts to ketones; eliminates keto flu; improves mental clarity"],
           ["Vitamin D3","2000–5000 IU/day","Fat-soluble vitamin; important when reducing food variety"],
           ["Fibre supplement (Psyllium Husk)","10–15 g/day in water","Gut health; prevents keto-related constipation"]]
    items.append(tbl(ksupp[0],[r for r in ksupp[1:]],TK,[(W-72)*f for f in [0.22,0.16,0.62]]))
    items.append(Paragraph("<b>Expected Results by Week:</b>", s["SSH"]))
    res=[["Week","Expected Weight Loss","What's Happening"],
         ["1","2–4 kg","Primarily water and glycogen. Keto flu possible Days 3–5 — hydrate and supplement electrolytes"],
         ["2","0.5–1.5 kg","Entering ketosis. Fat burning beginning. Energy starting to stabilize"],
         ["3","0.5–1.2 kg","Deep ketosis — consistent fat burning. Body composition visibly improving. Energy excellent"],
         ["4","0.3–1 kg","Fat-adapted state. Sustainable long-term fat loss established. Hunger dramatically reduced"],
         ["Total (30 days)","4–8 kg","Variable based on starting weight, compliance, and exercise. All fat + some water"]]
    items.append(tbl(res[0],[r for r in res[1:]],TK,[(W-72)*f for f in [0.12,0.20,0.68]]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 05 — FEMALE VEGETARIAN WEIGHT LOSS
# ════════════════════════════════════════════════════════════
def pdf_female(path):
    TK="female"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["FEMALE WEIGHT LOSS","COMPLETE WEEKLY DIET PLAN","VEGETARIAN INDIAN EDITION"],
                   "5-Day Meal Plan · Daily Menus · Grocery List · Women's Exercise Guide · Lifestyle Tips",
                   "Science-based · Sustainable · Designed for Indian women's metabolism",
                   TK, s, badges=["5-DAY PLAN","VEGETARIAN","WOMEN'S HEALTH","INDIAN FOODS"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Female Physiology & Weight Loss — The Differences That Matter",
               "2.  Daily Calorie & Macro Targets for Indian Women","3.  Day 1 — Balanced Foundation",
               "4.  Day 2 — High Fibre Focus","5.  Day 3 — Protein Priority",
               "6.  Day 4 — Light & Detox Day","7.  Day 5 — Satisfying & Sustainable",
               "8.  Complete Grocery Shopping List","9.  Women's Exercise Protocol",
               "10. Hormonal Awareness — Training With Your Cycle","11. Supplement Guide for Women",
               "12. 10 Habits for Sustainable Long-Term Fat Loss"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. FEMALE PHYSIOLOGY — THE DIFFERENCES THAT MATTER", TK, s, "💜")
    items.append(Paragraph("Women's bodies respond to diet and exercise differently than men's due to <b>hormonal, metabolic, and physiological differences</b>. Understanding these differences prevents frustration and allows you to work <i>with</i> your biology rather than against it.", s["BJ"]))
    items.append(rn("Women have approximately 20–25% body fat naturally (vs 15–20% in men) due to evolutionary requirements for reproduction. Estrogen actively promotes fat storage in the hips, thighs, and breasts — this fat is hormonally important and the last to be mobilized during fat loss.", TK, s))
    items.append(Paragraph("<b>Key Differences Affecting Fat Loss:</b>", s["SSH"]))
    diffs=[["Factor","Women","Men","Implication for Women"],
           ["Basal Metabolic Rate","10–15% lower than men","Higher due to more muscle mass","Women require fewer calories for the same body weight"],
           ["Hormonal Fluctuation","Cyclical (28-day cycle)","Relatively stable","Training and diet should adapt to menstrual phase"],
           ["Fat Oxidation","Higher % fat during exercise","More glucose-dependent","Women are naturally better fat-burners during cardio"],
           ["Muscle Building","Slower (lower T, higher E)","Faster","Resistance training is essential but results take longer — be patient"],
           ["Thyroid Sensitivity","More prone to hypothyroidism","Less common","Very low calorie diets can suppress thyroid in women — avoid <1000 kcal/day"],
           ["Cortisol Response","Higher cortisol to stress","Lower","Sleep, stress management, and recovery are CRITICAL for women's fat loss"]]
    items.append(tbl(diffs[0],[r for r in diffs[1:]],TK,[(W-72)*f for f in [0.20,0.20,0.18,0.42]]))

    items += sh("2. DAILY TARGETS FOR INDIAN WOMEN", TK, s, "📊")
    macro_rows=[["Nutrient","Target","Best Indian Vegetarian Sources","Why It Matters"],
                ["Calories","1200–1400 kcal","Adjust ±200 based on BMR × activity","Below 1200 kcal suppresses thyroid and triggers muscle loss"],
                ["Protein","60–80 g/day","Dal, paneer, soya, curd, rajma, chana, tofu","Preserves muscle during caloric deficit; increases satiety 2× vs fats/carbs"],
                ["Complex Carbs","130–150 g/day","Oats, brown rice, roti (2 max), sweet potato","Primary energy source; stabilizes blood sugar; prevents cravings"],
                ["Dietary Fibre","28–35 g/day","Vegetables, fruits, legumes, oats","Slows digestion; feeds gut microbiome; improves hormone metabolism"],
                ["Healthy Fats","35–45 g/day","Ghee (1 tsp/meal), nuts, seeds, avocado","Required for estrogen production and fat-soluble vitamin absorption"],
                ["Water","8–10 glasses","Plain water + herbal teas + lemon water","Reduces appetite; flushes metabolic byproducts; improves skin"]]
    items.append(tbl(macro_rows[0],[r for r in macro_rows[1:]],TK,[(W-72)*f for f in [0.14,0.14,0.32,0.40]]))

    def day_section(num, name, icon, meals, note):
        out=[]
        out += sh(f"DAY {num} — {name}", TK, s, icon)
        meal_rows=[[m[0],m[1],m[2],m[3]] for m in meals]
        out.append(tbl(["Time","Meal","Menu","~kcal"],[r for r in meal_rows],TK,[(W-72)*f for f in [0.12,0.13,0.63,0.12]]))
        out.append(Paragraph(f"<b>Day {num} Focus:</b> {note}", s["B"]))
        return out

    items += day_section(3,"BALANCED FOUNDATION","🌅",[
        ("7:30 AM","Breakfast","Overnight oats (½ cup rolled oats + low-fat milk + 1 tsp honey + mixed berries + 5 almonds)","~280"),
        ("10:30 AM","Mid-Morning","1 medium apple + 1 cup green tea (no sugar)","~80"),
        ("1:00 PM","Lunch","2 whole wheat rotis + 1 cup moong dal + mixed vegetable sabzi (1 tsp ghee) + large salad with lemon dressing","~420"),
        ("4:30 PM","Snack","30g roasted makhana (foxnuts) OR mixed seeds + lemon water","~120"),
        ("7:30 PM","Dinner","1 cup vegetable daliya (broken wheat khichdi) + 1 cup low-fat curd","~350"),
    ],"Total ~1250 kcal. Eat slowly — aim for 20 chews per bite. Drink a glass of water 20 min before each meal.")

    items += day_section(4,"HIGH FIBRE FOCUS","🍃",[
        ("7:30 AM","Breakfast","2 medium idli + sambar (dal-based) + 1 tsp coconut chutney","~260"),
        ("10:30 AM","Mid-Morning","1 small banana + 1 glass buttermilk (chaas, cumin, mint)","~90"),
        ("1:00 PM","Lunch","1 cup brown rice + 1 cup rajma masala + cucumber raita + salad","~430"),
        ("4:30 PM","Snack","Moong dal cheela (1 medium, minimal oil) + green chutney","~130"),
        ("7:30 PM","Dinner","Poha (½ cup dry) with peas, capsicum, mustard seeds + 1 cup warm turmeric milk","~340"),
    ],"Total ~1250 kcal. High fibre supports gut microbiome and estrogen metabolism — important for women's weight loss.")

    items.append(PageBreak())
    items += day_section(5,"PROTEIN PRIORITY","🌟",[
        ("7:30 AM","Breakfast","2 moong dal cheelas (vegetables, 1 tsp ghee) + green chutney + masala chai (low-fat milk)","~300"),
        ("10:30 AM","Mid-Morning","10–12 almonds + 1 small pear + lemon water","~100"),
        ("1:00 PM","Lunch","2 rotis + chana masala + 100g paneer bhurji (low oil) + sliced onions + lemon","~460"),
        ("4:30 PM","Snack","1 cup low-fat dahi + 1 tsp jeera + pinch black salt","~140"),
        ("7:30 PM","Dinner","Palak paneer (light) + 1 roti + vegetable clear soup","~320"),
    ],"Total ~1320 kcal. Protein-rich day rebuilds muscle. Best on strength training days.")

    items += day_section(6,"LIGHT & DETOX","🌿",[
        ("7:30 AM","Breakfast","Warm water + lemon + ginger (on waking). Then: upma (semolina ¼ cup dry, mixed veg) + green tea","~220"),
        ("10:30 AM","Mid-Morning","1 glass coconut water OR amla juice + 5 almonds","~70"),
        ("1:00 PM","Lunch","1 cup khichdi (thin, moong dal + rice 1:1) + 1 cup vegetable soup + curd","~380"),
        ("4:30 PM","Snack","Herbal tea (ginger-tulsi) + cucumber + carrot sticks with lemon","~80"),
        ("7:30 PM","Dinner","1 cup moong dal soup + 1 small roti + steamed vegetables (broccoli, beans)","~300"),
    ],"Total ~1050 kcal. Intentionally lighter. Drink 10+ glasses of water. Gut reset day.")

    items += day_section(7,"SATISFYING & SUSTAINABLE","✨",[
        ("7:30 AM","Breakfast","Vegetable poha (1 cup cooked, peas, groundnuts, lemon) + masala chai","~290"),
        ("10:30 AM","Mid-Morning","1 medium guava (high fibre, very low cal) + 1 glass buttermilk","~90"),
        ("1:00 PM","Lunch","1 cup dal fry + 2 rotis + aloo gobhi sabzi (low oil) + large salad","~440"),
        ("4:30 PM","Snack","½ cup roasted chana + green tea","~150"),
        ("7:30 PM","Dinner","Paneer tikka (grilled, 100g) + 1 cup dal soup + salad + 1 roti","~380"),
    ],"Total ~1350 kcal. End the week nourished. Plan next week's meals. Celebrate your discipline.")

    items += sh("8. GROCERY SHOPPING LIST", TK, s, "🛒")
    shop=[["Category","Items to Buy"],
          ["Grains & Pulses","Rolled oats, brown rice, whole wheat flour (atta), suji (semolina), poha, daliya, moong dal, chana dal, rajma, black chana, soya chunks"],
          ["Dairy & Protein","Paneer (low-fat), low-fat curd/yogurt, skimmed milk, buttermilk (chaas), tofu"],
          ["Vegetables","Spinach, methi, broccoli, cauliflower, capsicum, cucumber, tomatoes, onions, carrots, peas, lauki (bottle gourd), zucchini"],
          ["Fruits","Apples, oranges, small bananas, papaya, guava, berries (seasonal), amla"],
          ["Nuts, Seeds & Fats","Almonds, walnuts, makhana (foxnuts), pumpkin seeds, flaxseeds, groundnuts, ghee (pure cow)"],
          ["Herbs & Spices","Cumin seeds, mustard seeds, turmeric, coriander powder, garam masala, chaat masala, curry leaves, ginger, garlic, green chillies, fresh coriander, mint"]]
    items.append(tbl(shop[0],[r for r in shop[1:]],TK,[(W-72)*f for f in [0.22,0.78]]))

    items += sh("9. WOMEN'S EXERCISE PROTOCOL", TK, s, "🧘")
    ex=[["Activity","Frequency","Duration","Science-Backed Benefit"],
        ["Brisk Walking","Daily","30 min","Highest compliance; burns 150–200 kcal; reduces cortisol; improves insulin sensitivity"],
        ["Strength Training","3×/week","35–45 min","Increases resting metabolic rate; prevents muscle loss; improves bone density (critical for women >30)"],
        ["Yoga / Pilates","4–6×/week","20–30 min","Reduces cortisol by 20–30%; improves leptin sensitivity; regulates menstrual cycle"],
        ["Dance / Zumba","2×/week","40–60 min","High adherence (enjoyable); burns 300–400 kcal/hr; positive neurological effects"],
        ["Rest & Recovery","1–2 days","Full day","Muscle repair occurs during rest; sleep >7 hrs is mandatory for fat loss in women"]]
    items.append(tbl(ex[0],[r for r in ex[1:]],TK,[(W-72)*f for f in [0.18,0.13,0.12,0.57]]))

    items += sh("10. HORMONAL AWARENESS — TRAINING WITH YOUR CYCLE", TK, s, "🌙")
    cycle=[["Phase","Days","Hormones","Training Recommendation"],
           ["Menstrual","1–5","Low E, low P","Light exercise; yoga; walking. Energy may be low — be kind to yourself"],
           ["Follicular","6–13","Rising E","Increasing energy; great for strength training and HIIT; E increases pain tolerance"],
           ["Ovulatory","14","Peak E","Peak strength and power; best time for heavy lifts and intense workouts"],
           ["Luteal","15–28","High P","Moderate intensity; some fatigue; cravings increase — plan healthy snacks; reduce HIIT"]]
    items.append(tbl(cycle[0],[r for r in cycle[1:]],TK,[(W-72)*f for f in [0.16,0.10,0.18,0.56]]))
    items.append(rn("Research shows women can lift 15–20% more weight during the follicular and ovulatory phases compared to the luteal phase. Training intensity should be periodized around the menstrual cycle for optimal results and reduced injury risk.", TK, s))

    items += sh("11. SUPPLEMENT GUIDE FOR WOMEN", TK, s, "💊")
    supp=[["Supplement","Dose","Benefits Specific to Women"],
          ["Iron (if deficient)","18 mg/day (with Vitamin C)","Menstruation causes iron loss; deficiency causes fatigue, poor recovery, reduced aerobic capacity"],
          ["Folate / Vitamin B9","400–800 mcg","DNA synthesis; red blood cell production; essential for women of reproductive age"],
          ["Calcium + Vitamin D3","1000 mg Ca + 2000 IU D3","Bone density protection; muscle function; PMS symptom reduction"],
          ["Magnesium Glycinate","300–400 mg nightly","Reduces PMS symptoms by 40%; improves sleep; reduces cortisol; muscle relaxation"],
          ["Omega-3 (EPA+DHA)","2–3 g/day","Reduces menstrual pain; anti-inflammatory; improves body composition"],
          ["Ashwagandha (KSM-66)","300–600 mg/day","Adaptogen — reduces cortisol 20–30%; improves thyroid function; reduces stress eating"],
          ["Probiotics (multi-strain)","10–50 billion CFU/day","Gut health critical for estrogen metabolism; reduces bloating; improves mood"]]
    items.append(tbl(supp[0],[r for r in supp[1:]],TK,[(W-72)*f for f in [0.22,0.14,0.64]]))

    items += sh("12. 10 HABITS FOR LONG-TERM FAT LOSS", TK, s, "💡")
    for i,tip in enumerate([
        "<b>Drink water before every meal:</b> 500mL 20 min before eating reduces calorie intake by 13% (verified in clinical trials)",
        "<b>Sleep 7–9 hours:</b> Sleep deprivation raises ghrelin (hunger hormone) by 24% and leptin (satiety hormone) drops by 18% — directly causing weight gain",
        "<b>Prioritize protein at breakfast:</b> High-protein breakfast reduces total calorie intake by 400 kcal throughout the day vs carb-heavy breakfast",
        "<b>Cook at home 5+ days/week:</b> Home-cooked meals contain 25–50% fewer calories than restaurant equivalents of 'healthy' foods",
        "<b>Take progress photos weekly:</b> Body measurements and photos show fat loss 2–3 weeks before the scale does (especially when building muscle)",
        "<b>Manage stress actively:</b> Chronic high cortisol = belly fat accumulation. Yoga, breathing exercises, and nature walks are scientifically validated interventions",
        "<b>Eat slowly and mindfully:</b> Satiety signals take 15–20 min to reach the brain. Eating slowly naturally reduces portion size by 15–20%",
        "<b>Don't skip breakfast:</b> Breakfast eaters have 25% better weight management outcomes over 12 months vs breakfast skippers",
        "<b>Track weekly, not daily:</b> Body weight fluctuates 1–3 kg daily from water and digestion. Track weekly average to see real trends",
        "<b>Sustainable &gt; aggressive:</b> Aim for 0.5–1 kg/week loss. Faster loss (crash diets) leads to 95% regain within 2 years; gradual loss shows 30% better retention",
    ], 1): items.append(Paragraph(f"{i}. {tip}", s["BL"]))
    items.append(Spacer(1,8))
    items.append(Paragraph("Professional nutrition guidance always recommended. Results vary based on individual metabolism, activity level, and consistency.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 06 — THE COMPLETE PEPTIDE BIBLE
# ════════════════════════════════════════════════════════════
def pdf_peptides(path):
    TK="peptide"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["THE COMPLETE","PEPTIDE PROTOCOL BIBLE"],
                   "BPC-157 · TB-500 · GHK-Cu · Semax · Selank · Epithalon · PT-141 · AOD-9604 · Stacking Guide",
                   "Mechanism of action · Clinical dosing · Injection protocols · Full stacking guide",
                   TK, s, badges=["10+ PEPTIDES","MECHANISM GUIDE","DOSING PROTOCOLS","STACKING GUIDE"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  What Are Peptides? — The Science Explained","2.  BPC-157 — Body Protective Compound",
               "3.  TB-500 (Thymosin Beta-4) — Systemic Tissue Repair","4.  GHK-Cu — Copper Peptide",
               "5.  Semax — Cognitive Enhancement Peptide","6.  Selank — Anti-Anxiety & Nootropic",
               "7.  Epithalon — Telomere & Anti-Aging Peptide","8.  PT-141 — Sexual Function Peptide",
               "9.  AOD-9604 — Fat Loss Peptide","10. DSIP — Delta Sleep-Inducing Peptide",
               "11. Strategic Stacking Guide","12. Reconstitution, Storage & Injection Guide"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. WHAT ARE PEPTIDES? THE SCIENCE", TK, s, "🔬")
    items.append(Paragraph("Peptides are short chains of amino acids (2–50 amino acids) that act as <b>biological signaling molecules</b>. Unlike anabolic steroids (which force supraphysiological responses), peptides work by <b>activating, amplifying, or modulating your body's own biological pathways</b> — often with a significantly more favorable safety profile.", s["BJ"]))
    items.append(rn("The peptide research field exploded after the discovery that specific amino acid sequences could modulate growth factor expression, cellular repair mechanisms, and neurotransmitter function without the systemic side effects of full-length hormones.", TK, s))
    rows=[["Property","Small Molecule Drugs","Anabolic Steroids","Peptides"],
          ["Mechanism","Enzyme inhibition / receptor blockade","Nuclear AR activation","Receptor activation / signaling modulation"],
          ["Specificity","Variable","Systemic (all AR-containing tissues)","Often highly tissue-selective"],
          ["Safety Profile","Variable","Significant systemic side effects","Generally favorable; short half-lives"],
          ["Detectability (WADA)","Variable","Long detection windows","Most are short-window or undetectable"],
          ["Legal Status","RX or OTC","Schedule III (USA) — controlled","Research chemicals (grey area in most countries)"]]
    items.append(tbl(rows[0],[r for r in rows[1:]],TK,[(W-72)*f for f in [0.22,0.20,0.22,0.36]]))
    items.append(Paragraph("<b>Administration Routes:</b>", s["SSH"]))
    for x in ["<b>Subcutaneous (SC):</b> Injected into fat layer under skin — standard for most peptides (BPC-157, TB-500, GHRP, CJC)",
               "<b>Intramuscular (IM):</b> Injected into muscle — used for IGF-1 LR3 (local muscle effect), some GHRP protocols",
               "<b>Intranasal:</b> Nasal spray — Semax, Selank, DSIP can be administered this way (less efficient but needlefree)",
               "<b>Oral:</b> Most peptides are degraded by digestive enzymes; generally ineffective. Exception: BPC-157 has oral activity for gut conditions"]:
        items.append(bl(x, s))

    items += sh("2. BPC-157 — BODY PROTECTIVE COMPOUND", TK, s, "💊")
    items.append(Paragraph("<b>Full name:</b> Body Protection Compound-157. A 15-amino acid peptide derived from a protective protein found in human gastric juice. BPC-157 is the most versatile peptide available, with healing effects documented across muscles, tendons, ligaments, gut, nerves, and brain.", s["BJ"]))
    items.append(Paragraph("<b>Mechanism of Action:</b>", s["SSH"]))
    for x in ["<b>Angiogenesis:</b> Upregulates VEGF (Vascular Endothelial Growth Factor) — grows new blood vessels to injured tissue, dramatically accelerating healing",
               "<b>Growth factor modulation:</b> Increases expression of PDGF, EGF, and bFGF — key signaling proteins for tissue repair",
               "<b>Nitric oxide pathway:</b> Modulates NO production; vasodilatory effects improve local blood flow to injury site",
               "<b>Gut healing:</b> Repairs intestinal epithelium; increases gastric mucosal blood flow; protects against NSAID-induced damage",
               "<b>Tendon and ligament repair:</b> Accelerates collagen organization and tendon fibroblast proliferation by 2–3×"]:
        items.append(bl(x, s))
    bpc_rows=[["Application","Dose","Protocol","Route","Duration"],
              ["Injury healing (tendon/muscle)","250–500 mcg/day","Split into 2 injections","SC near injury site","Until healed (typically 4–8 wks)"],
              ["Gut healing (IBS, ulcers, leaky gut)","250 mcg 2×/day","Morning + evening","SC or oral (capsule)","4–8 weeks"],
              ["Systemic recovery & prevention","200–300 mcg/day","Once daily","SC (abdominal)","Cycle 8 wks on / 4 wks off"],
              ["Brain/nerve healing","200–400 mcg/day","2× daily","SC (nape of neck area or systemic)","4–6 weeks"]]
    items.append(tbl(bpc_rows[0],[r for r in bpc_rows[1:]],TK,[(W-72)*f for f in [0.25,0.14,0.16,0.13,0.32]]))
    items.append(rn("Animal studies (Sikiric et al., multiple publications in Journal of Physiology-Paris) demonstrate BPC-157 heals Achilles tendon transection 2–3× faster than untreated controls, with superior collagen organization in healed tissue. Human trials are currently in Phase II for IBD.", TK, s))

    items += sh("3. TB-500 (THYMOSIN BETA-4)", TK, s, "💉")
    items.append(Paragraph("<b>TB-500</b> is a synthetic analog of Thymosin Beta-4 (Tβ4), a naturally occurring 43-amino acid protein found in virtually all human cells. It regulates <b>actin polymerization</b> — the process that drives cellular movement, wound healing, and tissue repair throughout the body.", s["BJ"]))
    for x in ["<b>Mechanism:</b> Sequesters G-actin monomers, promoting cell migration to injury sites; activates wound healing cascades; potent anti-inflammatory via NF-κB pathway inhibition",
               "<b>Systemic effect:</b> Unlike BPC-157 (local), TB-500 acts systemically — benefits whole-body healing simultaneously",
               "<b>Cardiovascular:</b> Promotes cardiac cell survival after injury; studied in heart failure patients (Phase II trials)",
               "<b>CNS healing:</b> Promotes neural stem cell migration; studied for stroke recovery"]:
        items.append(bl(x, s))
    tb_rows=[["Phase","Dose","Frequency","Duration"],
             ["Loading (active injury)","2–2.5 mg","2× weekly","6 weeks"],
             ["Maintenance (prevention)","2 mg","Once per week","Ongoing (cycle 12 wks on / 4 wks off)"],
             ["Performance (recovery)","1–2 mg","Once weekly","8–12 weeks"]]
    items.append(tbl(tb_rows[0],[r for r in tb_rows[1:]],TK,[(W-72)*f for f in [0.28,0.18,0.18,0.36]]))
    items.append(Paragraph("<b>BPC-157 + TB-500 Stack (Gold Standard Healing Protocol):</b>", s["SSH"]))
    for x in ["BPC-157 250 mcg + TB-500 2 mg on the same day, both SC — synergistic local + systemic healing",
               "Often called 'Wolverine Stack' — dramatically accelerates recovery from almost any musculoskeletal injury",
               "Can safely be run alongside any other protocol (AAS, SARMs, natural)"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    items += sh("4–7. GHK-Cu · SEMAX · SELANK · EPITHALON", TK, s, "🧬")
    peptide_mini=[
        ("GHK-Cu (COPPER PEPTIDE)","A naturally occurring tripeptide (Gly-His-Lys) that binds copper. Found in blood, saliva, and urine; declines with age.","Activates ~4,000 human genes; upregulates collagen, elastin, and antioxidant enzymes; anti-inflammatory; promotes hair follicle survival; potent wound healing","Skin injection/topical: 0.1–2mg/day SC or applied topically as 0.1–1% cream. Best for skin aging, hair loss prevention, wound repair."),
        ("SEMAX (ACTH 4-7-Pro-Gly-Pro)","Synthetic analog of the neuropeptide ACTH. Developed in Russia in the 1980s for cognitive enhancement and stroke rehabilitation.","Increases BDNF (Brain-Derived Neurotrophic Factor) by up to 800%; enhances dopamine and serotonin signaling; potent neuroprotective effects; improves memory consolidation","600–900 mcg/day intranasal (3 drops each nostril, 2–3 daily). Use in 2–4 week cycles for cognitive enhancement. Excellent for study, work performance, or post-injury neurological recovery."),
        ("SELANK (TKP-OH)","Synthetic heptapeptide analog of Tuftsin. Anxiolytic and nootropic — developed at the Russian Institute of Molecular Genetics.","Modulates GABAergic system (similar mechanism to benzodiazepines but without tolerance/dependence); increases serotonin metabolism; anti-anxiety without sedation; improves information processing speed","250–500 mcg/day intranasal. Use for: anxiety disorders, social anxiety, cognitive stress, PCT mood management (excellent for hormonal transitions)."),
        ("EPITHALON (EPITALON)","Tetrapeptide (Ala-Glu-Asp-Gly) synthesized by the pineal gland. The most studied anti-aging peptide in existence.","Activates telomerase enzyme — extends telomere length in aging cells; normalizes melatonin production; antioxidant; tumor suppressive in animal models; extends lifespan in animal studies by 24–68%","5–10 mg/day SC for 10-day cycles, 2–3 times per year. Often combined with sleep protocols. Intranasal option: 20 mcg/day."),
    ]
    for pname, desc, mech, dose in peptide_mini:
        items.append(Paragraph(f"<b>► {pname}</b>", s["SSH"]))
        items.append(Paragraph(desc, s["B"]))
        items.append(Paragraph(f"<b>Mechanism:</b> {mech}", s["B"]))
        items.append(Paragraph(f"<b>Protocol:</b> {dose}", s["B"]))
        items.append(Spacer(1,4))

    items += sh("8–10. PT-141 · AOD-9604 · DSIP", TK, s, "⚡")
    misc_peps=[
        ("PT-141 (BREMELANOTIDE)","Melanocortin receptor agonist (MC3R, MC4R) — works centrally in the brain's limbic system (hypothalamus) to generate sexual arousal. The only peptide that directly activates desire rather than addressing peripheral circulation (unlike sildenafil/Viagra).","1–2 mg SC 45–90 min before sexual activity. Side effects: temporary nausea (use 0.5 mg to test), flushing. Cycle 2×/week maximum. Approved by FDA (2019) as Vyleesi for women's hypoactive sexual desire disorder."),
        ("AOD-9604","The C-terminal fragment of human growth hormone (HGH amino acids 176–191) that specifically targets fat metabolism without the growth-promoting or insulin-dysregulating effects of full HGH.","500 mcg/day SC, fasted AM injection. Directly stimulates β3-adrenergic receptors in fat cells → lipolysis. No effect on blood glucose or IGF-1. Ideal addition to cutting protocols for targeted fat loss."),
        ("DSIP (DELTA SLEEP-INDUCING PEPTIDE)","Naturally occurring neuropeptide in brain and GI tract. Reduces ACTH and cortisol; modulates sleep architecture by promoting deep slow-wave (delta) sleep. Also protects against oxidative stress.","100–200 mcg SC 30–60 min before bed. Use in 2-week cycles. Excellent for athletes with high stress loads, post-training insomnia, or those needing improved recovery sleep quality."),
    ]
    for pname, mech, dose in misc_peps:
        items.append(Paragraph(f"<b>► {pname}</b>", s["SSH"]))
        items.append(Paragraph(mech, s["B"]))
        items.append(Paragraph(f"<b>Protocol:</b> {dose}", s["B"]))
        items.append(Spacer(1,4))

    items += sh("11. STRATEGIC STACKING GUIDE", TK, s, "🎯")
    stacks=[["Goal","Stack","Daily Protocol","Duration"],
            ["Injury recovery & performance","BPC-157 + TB-500","BPC-157 250mcg AM + PM; TB-500 2mg 2×/week","6–8 weeks"],
            ["Mass building (with AAS/SARMs)","IGF-1 LR3 + GHRP-6 + CJC-1295","IGF-1 LR3 50mcg post-workout; GHRP-6 100mcg 3×/day; CJC-1295 DAC 2mg/wk","12–16 weeks"],
            ["Anti-aging & longevity","Epithalon + GHK-Cu + BPC-157","10-day Epithalon cycle 2×/year; GHK-Cu daily; BPC-157 ongoing low dose","Year-round"],
            ["Cognitive optimization","Semax + Selank","Semax 600mcg AM intranasal; Selank 250mcg PM intranasal","2–4 week cycles"],
            ["Fat loss acceleration","AOD-9604 + HGH Fragment 176-191","AOD 500mcg fasted AM; HGH Fragment 500mcg split AM/pre-workout","12 weeks"],
            ["Sleep & recovery","DSIP + BPC-157 + Epithalon","DSIP 150mcg pre-bed; BPC-157 250mcg AM; Epithalon 10-day cycles","Cyclical"]]
    items.append(tbl(stacks[0],[r for r in stacks[1:]],TK,[(W-72)*f for f in [0.22,0.22,0.32,0.24]]))

    items += sh("12. RECONSTITUTION, STORAGE & INJECTION GUIDE", TK, s, "🔬")
    items.append(Paragraph("<b>Reconstitution Protocol:</b>", s["SSH"]))
    for x in ["Use only bacteriostatic water (BAC water) — not sterile water. BAC water contains 0.9% benzyl alcohol which prevents microbial growth",
               "Inject BAC water slowly down the SIDE of the vial — never directly onto the peptide powder (can degrade it)",
               "Swirl gently to mix — never shake vigorously (breaks peptide bonds)",
               "Standard reconstitution: 2mL BAC water per 5mg vial = 2.5 mcg/μL concentration",
               "Use 1mL insulin syringe (U-100) for all SC injections — smallest gauge available (27–31G)"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Storage Rules:</b>", s["SSH"]))
    for x in ["Lyophilized (dry powder): Stable at room temperature for 6–12 months, or refrigerated for 2+ years",
               "Reconstituted solution: Refrigerate at 2–8°C; stable for 4–6 weeks; discard if cloudy or precipitate forms",
               "Never freeze reconstituted peptides (ice crystals destroy structure)",
               "Protect all peptides from light — UV radiation degrades amino acid bonds"]:
        items.append(bl(x, s))
    items.append(wb("Source peptides only from verified, reputable suppliers with third-party HPLC purity testing certificates. Impure peptides are at best ineffective and at worst dangerous. Always request a Certificate of Analysis (CoA) before purchasing.", TK, s))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 07 — SARMs COMPLETE HANDBOOK
# ════════════════════════════════════════════════════════════
def pdf_sarms(path):
    TK="sarms"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["SARMs","COMPLETE SCIENTIFIC HANDBOOK"],
                   "RAD-140 · LGD-4033 · Ostarine · Cardarine · YK-11 · MK-677 · S23 · Full Stacking Guide",
                   "Mechanism of action · Tissue selectivity · Dosing · Mini-PCT · Side effect management",
                   TK, s, badges=["8 SARMs PROFILED","MECHANISM GUIDE","STACK PROTOCOLS","MINI-PCT"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  What Are SARMs? — Science & Tissue Selectivity","2.  RAD-140 (Testolone) — Most Anabolic SARM",
               "3.  LGD-4033 (Ligandrol) — Premier Mass Building SARM","4.  Ostarine (MK-2866) — Versatile & Mild",
               "5.  Cardarine (GW-501516) — Endurance & Fat Loss","6.  YK-11 — Myostatin Inhibitor",
               "7.  MK-677 (Ibutamoren) — GH Secretagogue","8.  S23 — Most Suppressive SARM",
               "9.  Bulking · Cutting · Recomp Stack Protocols","10. Mini-PCT for SARMs",
               "11. Blood Work & Health Monitoring","12. SARMs vs AAS — Complete Comparison"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. WHAT ARE SARMs? — THE SCIENCE", TK, s, "🔬")
    items.append(Paragraph("<b>Selective Androgen Receptor Modulators (SARMs)</b> are a class of drugs designed to activate androgen receptors in a <b>tissue-selective</b> manner — producing anabolic effects in muscle and bone while minimizing androgenic effects in other tissues (prostate, skin, liver, etc.).", s["BJ"]))
    items.append(rn("SARMs were originally developed in the 1990s by pharmaceutical companies as treatments for muscle wasting diseases, osteoporosis, and male hypogonadism. None have received FDA approval for these uses, but extensive research exists confirming their anabolic activity.", TK, s))
    items.append(Paragraph("<b>How Tissue Selectivity Works:</b>", s["SSH"]))
    for x in ["SARMs are non-steroidal compounds that bind the androgen receptor (AR) with high affinity",
               "Unlike testosterone, SARMs produce different <b>conformational changes</b> in the AR depending on the tissue",
               "In muscle: SARM-AR complex recruits coactivator proteins that drive anabolic gene expression",
               "In prostate/scalp: SARM-AR complex recruits different coactivators with weaker or no androgenic activity",
               "Result: muscle-building effects similar to testosterone with fraction of androgenic side effects"]:
        items.append(bl(x, s))
    compare=[["Compound","Anabolic Ratio","Androgenic Ratio","Liver Toxicity","Suppression Level"],
             ["Testosterone (baseline)","100","100","Low (injectable)","Complete (expected)"],
             ["RAD-140","~890","~3","None (non-17aa)","Moderate–High"],
             ["LGD-4033","~500","~4","None","Moderate"],
             ["Ostarine","~30","~1","None","Mild–Moderate"],
             ["YK-11","Extremely high*","Moderate","Unknown","High"],
             ["S23","~830","~98","None","Very High"],
             ["MK-677","N/A (not true SARM)","None","None","None (raises GH)"]]
    items.append(tbl(compare[0],[r for r in compare[1:]],TK,[(W-72)*f for f in [0.22,0.15,0.15,0.15,0.33]]))

    items += sh("2. RAD-140 (TESTOLONE)", TK, s, "⚡")
    items.append(Paragraph("RAD-140 is the most anabolic SARM ever developed — with an anabolic:androgenic ratio of approximately 90:1 compared to testosterone's 1:1. Originally developed by Radius Health for muscle-wasting diseases, it produces <b>significant lean mass gains comparable to low-dose testosterone</b>.", s["BJ"]))
    rad=[["Parameter","Details"],["Chemical Name","2-chloro-4-[[(1R,2S)-2-hydroxy-2-methyl-1-[4-(trifluoromethyl)phenyl]propyl]amino]-3-methylbenzonitrile"],
         ["Half-Life","60 hours (dose once daily)"],["Anabolic:Androgenic","90:1 (vs testosterone 1:1)"],
         ["Dose Range","8–15 mg/day"],["Cycle Length","8–12 weeks"],
         ["Suppression Level","Moderate–High (mini-PCT required)"],
         ["Best For","Lean muscle mass, strength, body recomposition"],
         ["Stacking Partners","MK-677, Cardarine, LGD-4033 (bulking stack)"]]
    items.append(tbl(["Parameter","Details"],[r[1:] if r[0]!="Parameter" else r[1:] for r in rad[1:]],TK,[(W-72)*f for f in [0.30,0.70]]))
    for x in ["Expected results: 8–12 lbs lean mass over 12 weeks (first cycle); superior to most oral steroids",
               "Does not aromatize — no estrogen-related side effects, no AI required",
               "May cause hair shedding in DHT-sensitive individuals (binds scalp AR despite selectivity claims)",
               "Neurological benefits: RAD-140 is neuroprotective in animal studies; enhanced mood and focus commonly reported",
               "Blood work: Check testosterone and LH/FSH at baseline and Week 8; expect 30–60% suppression"]:
        items.append(bl(x, s))

    items += sh("3. LGD-4033 (LIGANDROL)", TK, s, "💪")
    items.append(Paragraph("LGD-4033 (Ligandrol) was developed by Ligand Pharmaceuticals and studied clinically in Phase I trials. It is the <b>most studied SARM in human clinical trials</b>, with a published Phase I safety study at doses of 0.1–1 mg/day showing significant lean mass gains even at microdose levels.", s["BJ"]))
    items.append(rn("Basaria et al. (2013, The Lancet) Phase I trial: LGD-4033 at 1 mg/day for 21 days produced a statistically significant 1.21 kg lean mass gain with dose-dependent suppression of LH, FSH, and total testosterone. At 1 mg/day, no serious adverse events were reported.", TK, s))
    for x in ["<b>Dose:</b> 5–10 mg/day (5mg is sufficient for lean bulking; 10mg for aggressive bulking)",
               "<b>Half-life:</b> 24–36 hours — once daily dosing",
               "<b>Best use:</b> 8–12 week bulking or recomposition cycles",
               "<b>Expected results:</b> 10–15 lbs lean mass over 12 weeks at 10mg/day with proper diet",
               "<b>Water retention:</b> Moderate (1–3 lbs) — more than RAD-140 due to mild estrogenic activity",
               "<b>Suppression:</b> Moderate — mini-PCT recommended; recovery typically complete in 4–6 weeks"]:
        items.append(bl(x, s))

    items += sh("4. OSTARINE (MK-2866)", TK, s, "🎯")
    items.append(Paragraph("Ostarine (Enobosarm) is the mildest and most studied SARM — the safest entry point for SARM use. It was developed by GTx Inc. and studied extensively in Phase II trials for cancer cachexia and osteoporosis. Its mild profile makes it ideal for beginners, recomposition, and joint healing.", s["BJ"]))
    for x in ["<b>Dose:</b> 15–25 mg/day for mass/recomp; 10–15 mg for joint healing",
               "<b>Half-life:</b> 23–26 hours — once daily dosing",
               "<b>Suppression:</b> Mild — many users need no PCT after 8-week cycles at 15–20mg",
               "<b>Joint healing:</b> Demonstrated improvement in collagen synthesis and joint integrity markers",
               "<b>Female-friendly:</b> 5–10 mg/day is one of the safest anabolic compounds for women",
               "<b>Stacking:</b> Excellent base for all stacks; pairs well with Cardarine for recomp"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    items += sh("5–8. CARDARINE · YK-11 · MK-677 · S23", TK, s, "📊")
    others=[
        ("CARDARINE (GW-501516)","PPAR-δ (Peroxisome Proliferator-Activated Receptor Delta) agonist — technically NOT a SARM but classified with them. Dramatically increases fat oxidation and endurance by switching cells from glucose to fat metabolism.","CRITICAL WARNING: GW-501516 was abandoned by GlaxoSmithKline in 2007 when animal studies showed it caused cancerous tumors at extremely high doses (>10× human dose for 2 years). Use at your own risk; keep doses low and cycles short.","10 mg/day (4–8 weeks maximum). Benefits: endurance increases 30–60%; LISS cardio capacity dramatically improved; fat loss accelerated. Do NOT exceed 8-week cycles."),
        ("YK-11","Partially activates androgen receptor (SARM activity) AND inhibits Myostatin — the body's natural muscle growth limiter. Theoretically allows muscle mass beyond genetic ceiling. YK-11 is the most experimental compound in this guide.","Extremely limited human data exists. Mechanism is promising but safety profile is largely unknown. Animal data shows liver enzyme elevation at high doses. NOT recommended for beginners.","5–10 mg/day, 6 weeks maximum. High suppression — full PCT required. Liver support (TUDCA, NAC) mandatory."),
        ("MK-677 (IBUTAMOREN)","Ghrelin receptor agonist and GH secretagogue — increases GH and IGF-1 WITHOUT suppressing the HPT axis. Not a true SARM. Dramatically improves sleep quality, recovery, skin, hair, and produces moderate anabolic effects over months of use.","25 mg nightly before bed (capitalizes on nocturnal GH pulse). Benefits: GH increases 30–100%; IGF-1 rises 50–100%; dramatically improved deep sleep; noticeable joint and connective tissue improvement over 3+ months. Side effects: water retention, increased appetite, potential insulin resistance (monitor fasting glucose).","Cycle length: Can be run long-term (6–12 months). No PCT required. Stack with any compound safely."),
        ("S23","The most potent and most suppressive SARM available. Almost identical androgenic activity to anabolic steroids. Produces extreme hardness, vascularity, and dry lean mass gains. Studied as a male contraceptive — causes complete suppression of sperm production at certain doses.","Full PCT required (same as steroid cycle). NOT a beginner compound.","10–30 mg/day, 6–8 weeks. Expect suppression at 100% of testosterone production. Use lowest effective dose. Excellent for cutting/recomp in experienced users."),
    ]
    for pname, mech, warning, dose in others:
        items.append(Paragraph(f"<b>► {pname}</b>", s["SSH"]))
        items.append(Paragraph(mech, s["B"]))
        if warning: items.append(wb(warning, TK, s))
        items.append(Paragraph(f"<b>Protocol:</b> {dose}", s["B"]))
        items.append(Spacer(1,4))

    items += sh("9. STACK PROTOCOLS", TK, s, "🗂")
    stacks=[["Goal","Stack","Doses","Duration","PCT"],
            ["Lean Bulk","RAD-140 + MK-677","RAD-140 10mg/day + MK-677 25mg nightly","12 weeks","Mini-PCT 4 weeks"],
            ["Aggressive Bulk","LGD-4033 + MK-677 + RAD-140","LGD 10mg + RAD 10mg + MK-677 25mg","10 weeks","Full PCT 6 weeks"],
            ["Cutting/Recomp","Ostarine + Cardarine","Ostarine 20mg/day + Cardarine 10mg/day","8 weeks","Optional mini-PCT"],
            ["Advanced Cutting","RAD-140 + Cardarine + S23","RAD 10mg + GW 10mg + S23 15mg","8 weeks","Full PCT required"],
            ["Women's Recomp","Ostarine only","10 mg/day","8 weeks","None needed at this dose"],
            ["Joint Healing","Ostarine + BPC-157","Ostarine 15mg/day + BPC-157 250mcg 2×/day","8 weeks","None / mini-PCT"]]
    items.append(tbl(stacks[0],[r for r in stacks[1:]],TK,[(W-72)*f for f in [0.18,0.22,0.24,0.13,0.23]]))

    items += sh("10–12. MINI-PCT · BLOOD WORK · SARMs vs AAS", TK, s, "🔄")
    items.append(Paragraph("<b>Mini-PCT for SARMs (most cycles):</b>", s["SSH"]))
    for x in ["Clomid 25–50 mg/day for 4 weeks (lower dose than AAS PCT) + Nolvadex 20 mg/day for 4 weeks",
               "Start mini-PCT 24–48 hours after last dose (SARMs have short half-lives vs AAS long esters)",
               "For S23, RAD-140 at high dose, or YK-11: use full AAS-level PCT protocol (Clomid 50mg + Nolvadex 20mg for 6 weeks)",
               "MK-677: no PCT required — does not suppress HPT axis"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Minimum Blood Work:</b>", s["SSH"]))
    bw=[["Timing","Tests"],["Pre-SARMs","Total T, Free T, LH, FSH, E2, CBC, CMP, Lipids"],
        ["Week 6 on-cycle","Total T, LH, FSH (check suppression level)"],
        ["Post-PCT (4 wks)","Total T, LH, FSH, E2 — confirm recovery"]]
    items.append(tbl(bw[0],[r for r in bw[1:]],TK,[(W-72)*f for f in [0.25,0.75]]))
    items.append(Paragraph("<b>SARMs vs AAS — Key Differences:</b>", s["SSH"]))
    comp=[["Factor","SARMs","Anabolic Steroids"],
          ["Mechanism","Non-steroidal AR modulation","Steroidal AR activation"],
          ["Liver toxicity","Generally none (non-17-alpha alkylated)","Orals: significant; injectables: minimal"],
          ["Estrogen conversion","None (except LGD: mild)","Yes — varies by compound"],
          ["Hair loss risk","Lower (selective)","Higher (DHT conversion)"],
          ["Cardiovascular impact","Moderate (lipid changes)","Significant (HDL suppression)"],
          ["PCT complexity","Mini-PCT usually sufficient","Full PCT typically required"],
          ["Legal status","Unscheduled research chemical (most countries)","Schedule III controlled substance (USA)"]]
    items.append(tbl(comp[0],[r for r in comp[1:]],TK,[(W-72)*f for f in [0.24,0.38,0.38]]))
    items.append(Spacer(1,8))
    items.append(Paragraph("⚠ SARMs are not approved for human use by any regulatory agency. For research purposes only. Consult a physician.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 08 — TRT & HORMONE OPTIMIZATION
# ════════════════════════════════════════════════════════════
def pdf_trt(path):
    TK="trt"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["TESTOSTERONE REPLACEMENT","THERAPY (TRT)","COMPLETE OPTIMIZATION GUIDE"],
                   "Protocols · Dosing · Blood Work · Aromatase Management · Thyroid · Sexual Health",
                   "Evidence-based hormone optimization for health, vitality & body composition",
                   TK, s, badges=["TRT PROTOCOLS","BLOOD WORK GUIDE","HORMONE OPTIMIZATION","SIDE EFFECT MANAGEMENT"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Low Testosterone — Symptoms, Causes & Diagnosis",
               "2.  The Hypothalamic-Pituitary-Testicular (HPT) Axis",
               "3.  TRT Protocols — Types, Doses & Administration",
               "4.  Optimizing Free vs Total Testosterone",
               "5.  Estrogen Management on TRT","6.  HCG on TRT — Fertility & Testicular Health",
               "7.  Thyroid Optimization — The Missing Piece",
               "8.  DHT, 5-Alpha Reductase & Hair Loss Management",
               "9.  Blood Work — Complete Testing & Interpretation Guide",
               "10. Cardiovascular Health on TRT","11. Sexual Function & Libido Optimization",
               "12. Long-Term TRT — Lifestyle, Sleep & Synergistic Optimization"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. LOW TESTOSTERONE — SYMPTOMS, CAUSES & DIAGNOSIS", TK, s, "🩺")
    items.append(Paragraph("Low testosterone (hypogonadism) affects an estimated <b>2–4% of adult men</b>, with subclinical low-normal testosterone (300–450 ng/dL) affecting a much larger population. Symptoms often present years before lab values fall below clinical cutoffs, causing significant quality-of-life impairment.", s["BJ"]))
    items.append(rn("A major American urological study found that men with total testosterone <300 ng/dL have a 42% increased cardiovascular risk, significantly reduced bone density, and a 3× higher incidence of metabolic syndrome compared to men with optimal T levels (600–900 ng/dL).", TK, s))
    items.append(Paragraph("<b>Symptoms of Low Testosterone:</b>", s["SSH"]))
    symp=[["Category","Symptoms","Severity"],
          ["Physical","Decreased muscle mass, increased body fat (especially abdominal), reduced strength, fatigue even after adequate sleep, decreased body/facial hair","Often attributed to aging; frequently missed for years"],
          ["Sexual","Reduced libido, erectile dysfunction, decreased morning erections, reduced ejaculate volume, infertility","Major quality of life impact; often first symptom noticed"],
          ["Psychological","Depression, anxiety, irritability, reduced motivation, cognitive fog, poor concentration, low confidence","Often misdiagnosed as depression — antidepressants are NOT the solution if cause is hormonal"],
          ["Metabolic","Insulin resistance, type 2 diabetes risk, dyslipidemia (high LDL, low HDL), visceral fat accumulation","Forms a negative feedback loop — fat cells convert T to estrogen, worsening T deficiency"]]
    items.append(tbl(symp[0],[r for r in symp[1:]],TK,[(W-72)*f for f in [0.14,0.51,0.35]]))

    items += sh("2. THE HYPOTHALAMIC-PITUITARY-TESTICULAR (HPT) AXIS", TK, s, "🔬")
    items.append(Paragraph("Understanding the HPT axis is essential for interpreting blood work, understanding why TRT suppresses natural production, and making informed decisions about HCG, AI, and PCT:", s["B"]))
    for x in ["<b>Hypothalamus</b> releases GnRH (Gonadotropin-Releasing Hormone) in pulses every 1–3 hours",
               "<b>Pituitary gland</b> responds to GnRH by releasing LH (Luteinizing Hormone) and FSH (Follicle-Stimulating Hormone)",
               "<b>LH</b> travels to Leydig cells in the testes → stimulates testosterone production",
               "<b>FSH</b> travels to Sertoli cells → stimulates sperm production (spermatogenesis)",
               "<b>Testosterone</b> feeds back to hypothalamus and pituitary → reduces GnRH, LH, FSH (negative feedback)",
               "<b>TRT effect:</b> Exogenous testosterone triggers strong negative feedback → LH and FSH fall to near zero → testes stop producing testosterone and sperm → testicular atrophy over months"]:
        items.append(bl(x, s))
    items.append(Paragraph("This is why <b>HCG is critical</b> on TRT for men who want to maintain fertility or prevent complete testicular atrophy.", s["B"]))

    items += sh("3. TRT PROTOCOLS — TYPES, DOSES & ADMINISTRATION", TK, s, "💉")
    protocols=[["Protocol","Dose","Frequency","Pros","Cons"],
               ["Testosterone Enanthate (IM)","100–200 mg","Every 7–14 days","Inexpensive; familiar; stable","Peaks and troughs with 14-day schedule; requires injection"],
               ["Testosterone Enanthate (Sub-Q)","80–150 mg","Every 5–7 days (split)","More stable levels; less SHBG elevation; smaller needle","Less conventional; requires more frequent injections"],
               ["Testosterone Cypionate (IM)","100–200 mg","Every 7–14 days","Slightly longer half-life than Enanthate; widely available","Same as Enanthate"],
               ["Testosterone Propionate","25–50 mg","Every 2–3 days","Very stable blood levels; fast adjustment","Daily or EOD injections; more painful"],
               ["Testosterone Gel/Cream","50–100 mg topical","Daily application","Non-invasive; very stable levels","Transfer risk to women/children; variable absorption"],
               ["Testosterone Pellets","Implanted pellets","Every 3–6 months","Zero administration burden","Surgical insertion; dose adjustment difficult"]]
    items.append(tbl(protocols[0],[r for r in protocols[1:]],TK,[(W-72)*f for f in [0.22,0.13,0.14,0.25,0.26]]))
    items.append(Paragraph("<b>Optimal TRT Dose Principle:</b> The goal is to bring total testosterone into the <b>upper-normal physiological range (700–1000 ng/dL)</b>, not simply above the clinical cutoff (300 ng/dL). Many men feel optimal at 900+ ng/dL while still remaining within a physiological range that minimizes cardiovascular and prostate risk.", s["BJ"]))

    items += sh("4. FREE VS TOTAL TESTOSTERONE — OPTIMIZATION", TK, s, "📊")
    items.append(Paragraph("Total testosterone measures ALL testosterone in blood. However, only <b>2–4% of testosterone is 'free'</b> (unbound to proteins) and biologically active. The rest is bound to SHBG (Sex Hormone Binding Globulin) or albumin.", s["BJ"]))
    items.append(rn("Research demonstrates that free testosterone is a superior predictor of clinical outcomes (muscle mass, libido, energy) compared to total testosterone. A man with total T of 700 ng/dL but very high SHBG may have the same symptoms as a man with total T of 400 ng/dL and normal SHBG.", TK, s))
    items.append(Paragraph("<b>How to Optimize Free Testosterone:</b>", s["SSH"]))
    for x in ["<b>Reduce SHBG:</b> SHBG rises with age, insulin sensitivity, thyroid dysfunction, and low androgen levels. TRT itself reduces SHBG somewhat",
               "<b>Optimize thyroid:</b> Hypothyroidism dramatically increases SHBG — correcting T3/T4 liberates bound testosterone",
               "<b>Maintain healthy body weight:</b> Obesity increases SHBG and aromatase activity simultaneously",
               "<b>Adequate zinc:</b> Zinc inhibits SHBG synthesis in the liver — supplement 25–50 mg/day",
               "<b>Boron:</b> 10 mg/day boron has been shown to reduce SHBG by 9% and increase free T by 25% in a clinical study",
               "<b>Injection frequency:</b> More frequent TRT injections (2–3×/week) maintain more stable free T levels vs once-weekly peaks"]:
        items.append(bl(x, s))
    items.append(PageBreak())

    items += sh("5. ESTROGEN MANAGEMENT ON TRT", TK, s, "🛡")
    items.append(Paragraph("Estrogen management on TRT requires a more nuanced approach than during cycle use. <b>Men on TRT need adequate estrogen</b> for cardiovascular health, bone density, cognitive function, and sexual desire. Aggressive AI use on TRT is one of the most common and harmful mistakes.", s["BJ"]))
    items.append(wb("Multiple studies show that men with very low estrogen on TRT have WORSE cardiovascular outcomes than men with optimally elevated estrogen. Do NOT attempt to suppress E2 to low levels — it increases atherosclerosis risk, reduces bone density, and causes sexual dysfunction.", TK, s))
    items.append(Paragraph("<b>TRT Estrogen Targets:</b>", s["SSH"]))
    for x in ["Total T 700–1000 ng/dL with E2 30–50 pg/mL = optimal for most men (some feel best at E2 40–60 pg/mL)",
               "Symptoms matter more than numbers — adjust AI based on how you feel AND blood work together",
               "If AI is needed: Anastrozole 0.25 mg twice weekly maximum — start lower than AAS protocols",
               "Consider Aromasin over Arimidex for TRT — suicidal AI provides less fluctuation in E2 levels"]:
        items.append(bl(x, s))

    items += sh("6. HCG ON TRT — FERTILITY & TESTICULAR HEALTH", TK, s, "💊")
    for x in ["<b>Standard TRT dose:</b> 500 IU HCG 2× weekly alongside TRT injections",
               "<b>Fertility-focused:</b> 1000–2000 IU 3× weekly + consider FSH (Gonal-F or Follistim) if sperm count remains low",
               "<b>Testicular atrophy prevention:</b> 250 IU EOD (smaller, more frequent) maintains testicular size better than large infrequent doses",
               "<b>Mechanism:</b> HCG mimics LH — directly stimulates Leydig cells in testes to maintain function and size",
               "<b>HCG storage:</b> Reconstitute with bacteriostatic water; refrigerate; stable 60 days"]:
        items.append(bl(x, s))

    items += sh("7–9. THYROID · DHT · BLOOD WORK GUIDE", TK, s, "🩸")
    items.append(Paragraph("<b>Thyroid Optimization on TRT:</b>", s["SSH"]))
    items.append(Paragraph("The thyroid-testosterone relationship is bidirectional — low T reduces T3/T4 conversion, and low thyroid further depresses testosterone. Testing TSH alone is insufficient; demand <b>full thyroid panel</b> (TSH, Free T3, Free T4, Reverse T3, TPO antibodies).", s["B"]))
    thyroid=[["Test","Optimal Range","Action if Out of Range"],
             ["TSH","0.5–2.0 mIU/L","TSH >2.5 with symptoms: consider thyroid support"],
             ["Free T3","3.5–4.2 pg/mL","Low Free T3 with normal T4: impaired T4→T3 conversion; consider T3 supplementation"],
             ["Free T4","1.2–1.7 ng/dL","Low T4: primary hypothyroidism; may require T4 (Synthroid) or combination T4+T3"],
             ["Reverse T3","<15 ng/dL","High rT3 = T3 is being blocked; often caused by chronic stress or caloric restriction"]]
    items.append(tbl(thyroid[0],[r for r in thyroid[1:]],TK,[(W-72)*f for f in [0.14,0.22,0.64]]))
    items.append(Paragraph("<b>DHT & Hair Loss Management:</b>", s["SSH"]))
    for x in ["Testosterone converts to DHT via 5-alpha reductase enzyme — DHT is the primary cause of male pattern baldness (MPB) in genetically susceptible men",
               "5-alpha reductase inhibitors (Finasteride 1mg, Dutasteride 0.5mg) reduce scalp DHT by 60–90%",
               "Caution: Finasteride can cause permanent sexual side effects ('Post-Finasteride Syndrome') in a small percentage of men — research thoroughly before use",
               "Alternative: Topical Finasteride (0.025–0.1% solution applied to scalp) — reduces scalp DHT with minimal systemic absorption"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Complete TRT Blood Work Panel:</b>", s["SSH"]))
    bw=[["Frequency","Panel"],
        ["Baseline (before TRT)","Total T, Free T, LH, FSH, E2, Prolactin, SHBG, DHT, CBC, CMP, Lipids, PSA, TSH, Free T3, Free T4, HbA1c, Ferritin, Vitamin D"],
        ["3 months post-start","Total T, Free T, E2, SHBG, CBC (hematocrit), PSA, Lipids, CMP"],
        ["Every 6 months (stable)","Total T, Free T, E2, SHBG, CBC, PSA, Lipids, CMP"],
        ["Annually","Full panel same as baseline"]]
    items.append(tbl(bw[0],[r for r in bw[1:]],TK,[(W-72)*f for f in [0.22,0.78]]))

    items += sh("10–12. CARDIOVASCULAR · SEXUAL HEALTH · LIFESTYLE", TK, s, "❤")
    items.append(Paragraph("<b>Cardiovascular Monitoring on TRT:</b>", s["SSH"]))
    for x in ["TRT increases red blood cell production — check hematocrit every 3–6 months. If >52%: donate blood or reduce dose",
               "TRT may worsen dyslipidemia (especially HDL). Omega-3 4–6g/day is non-negotiable",
               "Blood pressure: Monitor monthly; target <130/80. Reduce sodium; exercise cardiovascular training",
               "Recent large studies (TRAVERSE trial, 2023) found TRT does NOT increase cardiovascular events in hypogonadal men with pre-existing cardiovascular disease"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Optimizing Sexual Function on TRT:</b>", s["SSH"]))
    for x in ["Libido usually improves within 3–6 weeks of TRT initiation",
               "If libido remains low despite optimal T: check E2 (too high or too low), prolactin (elevated = dopamine issue), thyroid (low T3), and zinc/vitamin D deficiency",
               "PT-141 (Bremelanotide): 1–2 mg SC 45–90 min before activity — acts centrally on desire circuits regardless of hormonal status",
               "Tadalafil (Cialis): 5 mg daily (low-dose) improves blood flow and may improve T response by increasing testicular blood circulation"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Lifestyle Synergy with TRT:</b> Resistance training 4×/week (amplifies TRT response by upregulating AR density). Sleep 7–9 hours (testosterone peaks during REM sleep — poor sleep negates TRT). Maintain body fat 10–18% (higher fat = more aromatization; lower fat = less conversion). Minimize alcohol (directly suppresses Leydig cell function).", s["B"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 09 — SCIENCE OF MUSCLE HYPERTROPHY
# ════════════════════════════════════════════════════════════
def pdf_hypertrophy(path):
    TK="hypertrophy"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["THE SCIENCE OF","MUSCLE HYPERTROPHY","COMPLETE TRAINING MANUAL"],
                   "Mechanisms · Volume Landmarks · Progressive Overload · Periodization · 3 Full Programs",
                   "Evidence-based training science for maximum lean muscle growth",
                   TK, s, badges=["EVIDENCE-BASED","VOLUME SCIENCE","3 PROGRAMS","PERIODIZATION"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Three Mechanisms of Muscle Hypertrophy","2.  Volume Landmarks — MEV, MV, MAV, MRV",
               "3.  Progressive Overload — The Master Variable","4.  Rep Ranges & Their Applications",
               "5.  Training Frequency — How Often Should You Train?","6.  Rest Periods — The Science",
               "7.  Periodization Models — Linear, Undulating, Block",
               "8.  Mind-Muscle Connection & Execution Quality","9.  Deload Protocols",
               "10. Program 1 — PPL (Push/Pull/Legs) 5-Day","11. Program 2 — Upper/Lower 4-Day",
               "12. Program 3 — Full Body 3-Day (Beginners)"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. THREE MECHANISMS OF MUSCLE HYPERTROPHY", TK, s, "🔬")
    items.append(Paragraph("Muscle hypertrophy (growth) results from three distinct but overlapping stimuli, identified and refined by Dr. Brad Schoenfeld's seminal 2010 review in the Journal of Strength and Conditioning Research:", s["B"]))
    mechs=[["Mechanism","Definition","How to Train for It","Evidence Level"],
           ["Mechanical Tension","Force generated during muscle contraction and stretch — the primary driver of hypertrophy","Heavy loads (65–85% 1RM); full range of motion; controlled eccentric phase; compound movements","Strongest evidence; most important driver"],
           ["Metabolic Stress","Accumulation of metabolites (lactate, hydrogen ions, phosphate) in muscle — creates hypoxic 'pump' environment","Moderate loads (65–75% 1RM); shorter rest periods (60–90s); isolation exercises; occlusion/BFR training","Moderate evidence; meaningful contributor"],
           ["Muscle Damage","Micro-tears in muscle fibers (especially eccentric phase) triggering satellite cell activation and repair/growth","Eccentric emphasis; novel exercises; extreme stretch positions; lower frequency (recovery time needed)","Emerging evidence; may contribute but not required"]]
    items.append(tbl(mechs[0],[r for r in mechs[1:]],TK,[(W-72)*f for f in [0.20,0.25,0.33,0.22]]))
    items.append(rn("Dr. Brad Schoenfeld's meta-analyses (2017, 2019) demonstrate that volume-equated protocols emphasizing mechanical tension produce equal or superior hypertrophy to high-metabolic-stress protocols, confirming mechanical tension as the primary driver.", TK, s))

    items += sh("2. VOLUME LANDMARKS — MEV, MV, MAV, MRV", TK, s, "📊")
    items.append(Paragraph("Volume landmarks describe the range of weekly sets per muscle group that produce specific training responses. These concepts, developed by Dr. Mike Israetel (Renaissance Periodization), provide a framework for programming volume rationally rather than arbitrarily.", s["BJ"]))
    vl=[["Landmark","Acronym","Definition","Typical Range (sets/muscle/week)","Application"],
        ["Minimum Effective Volume","MEV","Minimum sets needed to make gains above maintenance","4–8 sets","Deload weeks; returning from break; beginners"],
        ["Maintenance Volume","MV","Sets needed to maintain current muscle mass with no effort to grow","6–10 sets","Cutting phases; competition prep; high-stress periods"],
        ["Maximum Adaptive Volume","MAV","The 'sweet spot' — volume range producing the most hypertrophy","10–20 sets","Primary training volume for most cycles"],
        ["Maximum Recoverable Volume","MRV","Maximum sets from which you can recover before the next session","15–25+ sets","Upper limit; approach only in peak weeks; AAS elevates this"]]
    items.append(tbl(vl[0],[r for r in vl[1:]],TK,[(W-72)*f for f in [0.22,0.09,0.27,0.18,0.24]]))
    items.append(Paragraph("<b>Practical Application:</b>", s["SSH"]))
    for x in ["Start a new training block at MEV; add 2 sets/muscle/week each week",
               "When performance begins declining (DOMS excessive, strength drops, sleep worsens) — you've exceeded MRV",
               "After 4–6 weeks at MAV, deload back to MEV; reset and begin again with slightly higher MAV",
               "Natural athletes: MRV ≈ 15–25 sets/muscle/week. On AAS/SARMs: MRV increases to 25–35+ sets"]:
        items.append(bl(x, s))

    items += sh("3. PROGRESSIVE OVERLOAD — THE MASTER VARIABLE", TK, s, "⚡")
    items.append(Paragraph("Progressive overload is the single most important variable in hypertrophy training. Your body only adapts (grows) when subjected to a stimulus <b>greater than previous stimuli</b>. Without overload, you maintain — never grow.", s["B"]))
    po=[["Method","Description","Best Applied To","Rate of Progress"],
        ["Load Progression","Add weight to the bar each session or weekly","Compound movements (squat, bench, deadlift, OHP)","0.5–2.5 kg/session for beginners; monthly for advanced"],
        ["Rep Progression","Add reps within target rep range before increasing weight","All exercises; when load jumps are too large","1–2 extra reps per session; increase load when top of range hit"],
        ["Set Progression","Add a working set each week (volume accumulation)","When load/rep progress stalls","1 set/exercise/week added over a mesocycle"],
        ["Density Progression","Same work in less time (reduce rest periods)","Metabolic training; body composition phase","5–10 seconds less rest per session"],
        ["ROM Progression","Increase range of motion over time","Mobility-limited movements; deficit deadlifts","Small incremental ROM increase per session"],
        ["Technique Progression","Better execution = more stimulus from same load","All exercises (especially beginners)","Continuous; reduces injury risk while increasing effective load"]]
    items.append(tbl(po[0],[r for r in po[1:]],TK,[(W-72)*f for f in [0.20,0.27,0.27,0.26]]))

    items += sh("4–6. REP RANGES · FREQUENCY · REST PERIODS", TK, s, "📋")
    reps=[["Rep Range","% 1RM","Primary Adaptation","Best Exercises"],
          ["1–5 reps","90–100%","Neural strength; maximal force production; some hypertrophy","Powerlifts (squat, bench, deadlift, OHP); cleans"],
          ["6–10 reps","75–85%","PRIMARY hypertrophy zone; strength-hypertrophy blend","Compound movements + heavy isolation (DB curl, leg press)"],
          ["10–15 reps","65–75%","Hypertrophy-focused; metabolic stress; excellent for isolation","All isolation movements; cables; machines"],
          ["15–30 reps","50–65%","Metabolic stress; endurance; useful for volume work","Cables, bands, light isolation; finisher sets"]]
    items.append(tbl(reps[0],[r for r in reps[1:]],TK,[(W-72)*f for f in [0.14,0.10,0.38,0.38]]))
    items.append(rn("Schoenfeld 2017 meta-analysis: hypertrophy is statistically equal across rep ranges 1–30 when volume is equated (sets × reps × weight). However, higher loads (6–12 reps) achieve the same hypertrophy in fewer sets, making them more time-efficient.", TK, s))
    items.append(Paragraph("<b>Training Frequency:</b> Each muscle group responds to protein synthesis stimulation approximately <b>every 48–72 hours</b>. Training a muscle 2× per week allows 2 protein synthesis spikes vs once per week = theoretically 2× the growth stimulus. For most natural athletes: 2× per week per muscle group is optimal. 3× is marginal benefit for advanced athletes.", s["B"]))
    items.append(Paragraph("<b>Rest Periods:</b> 3–5 minutes for compound/strength sets (allows full ATP-PCr recovery); 1–2 minutes for isolation/metabolic sets (maintained metabolic stress). Shorter rest ≠ better hypertrophy when using free weights — full recovery enables heavier sets = more tension.", s["B"]))

    items += sh("7. PERIODIZATION MODELS", TK, s, "📅")
    items.append(PageBreak())
    per=[["Model","Structure","Best For","Frequency of Change"],
         ["Linear Periodization","Volume decreases as intensity increases over weeks/months","Beginners and powerlifters; predictable strength progression","Every 3–6 months (full cycle)"],
         ["Undulating Periodization (DUP)","Volume and intensity vary weekly or daily","Intermediate-advanced; prevents neural adaptation plateau","Weekly or daily"],
         ["Block Periodization","Distinct training blocks (accumulation → intensification → realization)","Advanced athletes; competition preparation","Every 3–6 week blocks"],
         ["Autoregulation (RPE-based)","Load and volume adjusted daily based on readiness (RPE scale)","Advanced athletes; variable life stress; most sophisticated","Daily"]]
    items.append(tbl(per[0],[r for r in per[1:]],TK,[(W-72)*f for f in [0.22,0.32,0.25,0.21]]))

    items += sh("8–9. MIND-MUSCLE CONNECTION & DELOADS", TK, s, "🧠")
    for x in ["<b>Mind-muscle connection (MMC):</b> Deliberately focusing attention on the target muscle during contraction increases muscle activation by 15–20% (Snyder & Leech, 2009). For isolation exercises, MMC is critical — for compound movements, external focus ('push the floor away') produces more force",
               "<b>Stretch-mediated hypertrophy:</b> New research (2022–2024) demonstrates that exercises producing maximum tension at full stretch (spider curls, incline curls, Romanian deadlifts, deep squats) produce superior hypertrophy vs exercises only loading the shortened position",
               "<b>Eccentric emphasis:</b> Eccentric phase (lowering) produces greater muscle tension per motor unit recruited — slowing the eccentric to 2–4 seconds increases hypertrophic stimulus significantly"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Deload Protocol:</b> After 4–6 weeks of hard training, perform a 1-week deload: reduce volume by 50% (keep same exercises and intensity), reduce sets to 2–3 per exercise, eliminate drop sets and intensification techniques. Deloads prevent cumulative fatigue from masking fitness gains and allow connective tissue recovery.", s["B"]))

    items += sh("10. PROGRAM 1 — PPL 5-DAY SPLIT", TK, s, "💪")
    ppl=[["Day","Focus","Exercises","Sets × Reps"],
         ["Monday","Push (Chest/Shoulders/Triceps)","Barbell Bench Press · Incline DB Press · Cable Lateral Raises · Shoulder Press · Tricep Pushdown · Skull Crushers","4×6–8 · 3×10–12 · 3×15–20 · 3×10–12 · 3×12–15 · 3×12–15"],
         ["Tuesday","Pull (Back/Biceps)","Barbell Row · Pull-Ups/Pulldowns · Seated Cable Row · Face Pulls · EZ Bar Curl · Hammer Curls","4×6–8 · 4×8–12 · 3×10–12 · 3×15–20 · 3×10–12 · 3×12–15"],
         ["Wednesday","Legs (Quads/Hams/Calves)","Barbell Squat · Leg Press · Romanian Deadlift · Leg Curl · Walking Lunges · Calf Raises","4×6–8 · 4×10–12 · 4×10–12 · 3×12–15 · 3×12–15 · 5×15–20"],
         ["Thursday","Push 2 (Shoulders/Chest/Triceps)","OHP · Arnold Press · Cable Flyes · Incline Bench · Overhead Tricep Extension · Lateral Raises","4×8–10 · 3×10–12 · 3×12–15 · 3×10–12 · 3×12–15 · 4×15–20"],
         ["Friday","Pull 2 (Back/Biceps/Rear Delts)","Deadlift · Wide Pulldown · Single-Arm DB Row · Reverse Flyes · Preacher Curl · Incline DB Curl","4×4–6 · 4×8–12 · 3×10–12 · 3×15–20 · 3×10–12 · 3×12–15"],
         ["Sat/Sun","Rest + Optional Cardio","30–45 min LISS walking/cycling","N/A"]]
    items.append(tbl(ppl[0],[r for r in ppl[1:]],TK,[(W-72)*f for f in [0.12,0.22,0.42,0.24]]))

    items += sh("11–12. UPPER/LOWER 4-DAY & FULL BODY 3-DAY", TK, s, "🗓")
    ul=[["Day","Focus","Key Exercises","Sets × Reps"],
        ["Monday","Upper — Strength","Bench Press · OHP · Barbell Row · Pull-Ups · Bicep Curl · Tricep Extension","4×4–6 · 4×4–6 · 4×4–6 · 4×6–8 · 3×8–10 · 3×8–10"],
        ["Tuesday","Lower — Strength","Squat · Romanian Deadlift · Leg Press · Leg Curl · Calf Raises","4×4–6 · 4×6–8 · 4×8–10 · 3×8–10 · 4×15–20"],
        ["Thursday","Upper — Hypertrophy","Incline DB Press · Lateral Raises · Seated Row · Pullovers · Preacher Curl · Pushdowns","3×10–15 each — focus on contraction quality and MMC"],
        ["Friday","Lower — Hypertrophy","Front Squat/Hack Squat · Bulgarian SSQ · Leg Ext · Lying Leg Curl · Seated Calf","3×12–15 each — full ROM; slow eccentric"]]
    items.append(tbl(ul[0],[r for r in ul[1:]],TK,[(W-72)*f for f in [0.12,0.22,0.42,0.24]]))
    fb=[["Day","Exercises","Sets × Reps"],
        ["Monday (Full Body A)","Squat 3×5 · Bench 3×5 · Row 3×5 · OHP 2×10 · Curl 2×12 · Push-up 2×max","Progressive overload on main 3 lifts each session"],
        ["Wednesday (Full Body B)","Deadlift 1×5 · OHP 3×5 · Chin-Up 3×5 · DB Bench 2×10 · Face Pull 2×15 · Plank 2×60s","Alternate A/B; add 2.5kg each session when all reps completed"],
        ["Friday (Full Body C)","Front Squat 3×8 · Incline Press 3×8 · Pendlay Row 3×8 · Dips 2×10 · Reverse Curl 2×12","Technique focus day — videos or mirror"]]
    items.append(tbl(fb[0],[r for r in fb[1:]],TK,[(W-72)*f for f in [0.24,0.50,0.26]]))
    items.append(Spacer(1,8)); items.append(Paragraph("Progressive overload without periodization leads to plateau. Periodize your training — systematically vary volume and intensity every 4–6 weeks for continuous progress.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 10 — ULTIMATE FAT LOSS MASTERCLASS
# ════════════════════════════════════════════════════════════
def pdf_fatloss(path):
    TK="fatloss"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["ULTIMATE FAT LOSS","MASTERCLASS"],
                   "Energy Balance · Macros · Cardio Science · Fat Burners · Metabolic Adaptation · Contest Prep",
                   "Evidence-based fat loss from physique athletes and sports science research",
                   TK, s, badges=["FAT LOSS SCIENCE","CARDIO PROTOCOLS","FAT BURNER STACK","CONTEST PREP"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  The Science of Fat Loss — Energy Balance","2.  Calculating Your Deficit — TDEE, BMR & Activity Factor",
               "3.  Macronutrient Strategy for Fat Loss","4.  Cardio Science — LISS vs HIIT vs Zone 2",
               "5.  Metabolic Adaptation — The Plateau Explained","6.  Diet Breaks & Refeeds",
               "7.  Natural Fat Burner Stack — Evidence-Based","8.  Clenbuterol & ECA Stack",
               "9.  T3 & Thyroid Optimization for Fat Loss","10. 12-Week Contest Prep Protocol",
               "11. Peak Week — Water, Carbs & Final Conditioning","12. Maintaining Results Long-Term"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. THE SCIENCE OF FAT LOSS", TK, s, "🔬")
    items.append(Paragraph("Fat loss is governed by one unbreakable law: <b>energy balance</b>. You must consume less energy than you expend. However, the <i>quality</i> of your deficit — which macros, what types of training, and how you manage metabolic adaptation — determines whether you lose fat vs muscle.", s["BJ"]))
    items.append(rn("A meta-analysis of 53 weight loss trials (Sacks 2009, NEJM) found that the specific macronutrient composition of caloric-deficit diets mattered far less than overall energy deficit for weight loss. However, high-protein diets (>1.2g/lb) consistently preserved significantly more lean mass during deficit.", TK, s))
    items.append(Paragraph("<b>The Three Laws of Fat Loss:</b>", s["SSH"]))
    for x in ["<b>Law 1 — Energy Deficit:</b> 1 lb of fat = approximately 3,500 kcal. A 500 kcal/day deficit = ~1 lb fat loss/week theoretically. In practice, metabolic adaptation reduces this. Aim for 0.5–1 lb/week for maximum muscle preservation",
               "<b>Law 2 — Protein Priority:</b> High protein preserves lean mass in deficit. Protein has the highest thermic effect (25–30% of calories burned in digestion). Minimum 1.0 g/lb body weight; optimal 1.5–2.0 g/lb during aggressive cuts",
               "<b>Law 3 — Training Stimulus:</b> Resistance training while in caloric deficit sends a 'survival' signal to preserve muscle. Without resistance training, 25–40% of weight loss comes from muscle mass"]:
        items.append(bl(x, s))

    items += sh("2. CALCULATING YOUR DEFICIT — TDEE & BMR", TK, s, "📊")
    items.append(Paragraph("<b>Step 1 — Calculate BMR (Mifflin-St Jeor equation):</b>", s["SSH"]))
    items.append(Paragraph("Men: BMR = 10 × weight(kg) + 6.25 × height(cm) − 5 × age + 5", s["B"]))
    items.append(Paragraph("Women: BMR = 10 × weight(kg) + 6.25 × height(cm) − 5 × age − 161", s["B"]))
    act=[["Activity Level","Multiplier","Description"],
         ["Sedentary","BMR × 1.2","Desk job; no exercise"],
         ["Light Activity","BMR × 1.375","1–3 workouts/week"],
         ["Moderate Activity","BMR × 1.55","3–5 workouts/week"],
         ["Very Active","BMR × 1.725","Hard training 6–7 days/week"],
         ["Extremely Active","BMR × 1.9","Athlete or physical labor + daily training"]]
    items.append(tbl(act[0],[r for r in act[1:]],TK,[(W-72)*f for f in [0.24,0.18,0.58]]))
    items.append(Paragraph("<b>Deficit Recommendations by Goal:</b>", s["SSH"]))
    def_rows=[["Goal","Deficit","Weekly Fat Loss","Muscle Preservation"],
              ["Slow Recomp","100–200 kcal","0.1–0.2 lbs","Excellent (muscle gain possible)"],
              ["Moderate Cut","300–400 kcal","0.5–0.7 lbs","Very good (minimal loss)"],
              ["Aggressive Cut","500–600 kcal","0.8–1.0 lbs","Good (high protein critical)"],
              ["Show Cut","600–800 kcal","1.0–1.5 lbs","Moderate (AAS/SARMs + high protein essential)"]]
    items.append(tbl(def_rows[0],[r for r in def_rows[1:]],TK,[(W-72)*f for f in [0.20,0.15,0.18,0.47]]))

    items += sh("3. MACRONUTRIENT STRATEGY FOR FAT LOSS", TK, s, "🍽")
    macro=[["Macro","Fat Loss Target","Why","Food Sources"],
           ["Protein","1.5–2.0 g/lb BW","Muscle preservation + satiety + TEF (25–30% burned in digestion)","Chicken, fish, eggs, Greek yogurt, cottage cheese, tofu, paneer"],
           ["Fats","0.35–0.5 g/lb BW","Hormonal health; fat-soluble vitamins; satiety; never go below 40g/day total","Olive oil, avocado, nuts, eggs, fatty fish"],
           ["Carbohydrates","Fill remaining calories","Primary energy for training performance; not the enemy — only context matters","Oats, sweet potato, rice, fruits, vegetables"],
           ["Fibre","35–50 g/day","Gut health; slows digestion; significantly improves satiety; improves insulin sensitivity","All vegetables, legumes, oats, psyllium husk"]]
    items.append(tbl(macro[0],[r for r in macro[1:]],TK,[(W-72)*f for f in [0.14,0.18,0.36,0.32]]))
    items.append(Paragraph("<b>Carb Cycling — Advanced Strategy:</b> On training days eat higher carbs (around workouts); on rest days reduce carbs. This optimizes muscle glycogen while increasing fat burning on low-activity days. Example: 200g carbs on training days; 80–100g on rest days.", s["B"]))

    items += sh("4. CARDIO SCIENCE — LISS vs HIIT vs ZONE 2", TK, s, "🏃")
    items.append(Paragraph("All three cardio modalities burn calories and accelerate fat loss — the differences are in sustainability, muscle preservation, and metabolic stress:", s["B"]))
    cardio=[["Type","Heart Rate Zone","Duration","Calories (approx)","Best Use Case","Muscle Preservation"],
            ["LISS (Low Intensity Steady State)","50–65% max HR","30–60 min","200–350 kcal","Daily fat-burning maintenance; fasted cardio; recovery days","Excellent — minimal muscle stress"],
            ["Zone 2 (Aerobic Base)","65–75% max HR","45–90 min","300–500 kcal","Mitochondrial development; metabolic flexibility; endurance base","Very good"],
            ["HIIT (High Intensity Interval)","80–95% max HR","15–25 min","200–400 kcal (+ EPOC)","2–3×/week max; high calorie afterburn (EPOC); time-efficient","Poor if excessive — avoid >3×/week in deficit"],
            ["Sprint Intervals","95–100% max HR","10–15 min","250–400 kcal (+ EPOC)","Weekly power maintainer; high EPOC; preserves fast-twitch muscle","Good — if brief and infrequent"]]
    items.append(tbl(cardio[0],[r for r in cardio[1:]],TK,[(W-72)*f for f in [0.18,0.14,0.11,0.12,0.28,0.17]]))
    items.append(rn("Greer 2015 meta-analysis: HIIT and LISS produce equivalent fat loss when total calories burned are equated. HIIT is time-efficient but higher injury risk and greater muscle catabolism risk in caloric deficit. Recommendation: LISS primary (4–5×/week) + HIIT secondary (1–2×/week).", TK, s))
    items.append(PageBreak())

    items += sh("5–6. METABOLIC ADAPTATION & REFEEDS", TK, s, "⚡")
    items.append(Paragraph("<b>Metabolic Adaptation</b> is the reduction in metabolic rate that occurs in response to caloric deficit. The body adapts to reduce energy expenditure, protecting against starvation. This is why fat loss plateaus — what was once a 500 kcal deficit becomes 200 kcal or less over weeks.", s["BJ"]))
    items.append(Paragraph("<b>Four Components of Metabolic Adaptation:</b>", s["SSH"]))
    for x in ["<b>Reduced BMR</b> (~5–10%): Fewer calories needed for basic body functions as body weight drops",
               "<b>Adaptive thermogenesis</b> (~5–15%): Beyond what weight loss predicts — body actively reduces heat production",
               "<b>Reduced NEAT</b> (~10–25%): Non-exercise activity thermogenesis drops (you fidget less, move less instinctively)",
               "<b>Reduced exercise efficiency</b> (~5%): Body becomes more efficient at exercise, burning fewer calories for same work"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Refeed Strategy (Targeted Leptin Restoration):</b>", s["SSH"]))
    for x in ["Leptin is the primary satiety hormone and metabolic regulator — it drops 50% within 7 days of caloric deficit",
               "A high-carbohydrate refeed day (TDEE + 20–30% surplus from carbs ONLY) temporarily restores leptin, reversing some adaptive thermogenesis",
               "Frequency: 1 refeed day per week during aggressive cuts; 1 per 2 weeks during moderate cuts",
               "Refeed protocol: Increase carbohydrates to 3–4× normal intake; keep protein HIGH; keep fats LOW (fat doesn't restore leptin)",
               "Diet break (1–2 weeks at TDEE): More powerful than refeeds for reversing adaptation; every 8–12 weeks on extended cuts"]:
        items.append(bl(x, s))

    items += sh("7. NATURAL FAT BURNER STACK — EVIDENCE-BASED", TK, s, "💊")
    natural=[["Supplement","Dose","Mechanism","Evidence Level"],
             ["Caffeine (anhydrous)","3–6 mg/kg body weight","Increases adrenaline (epinephrine) release → mobilizes fat stores (lipolysis); increases BMR 3–11%; synergistic with all other fat burners","Very strong — most researched fat loss compound"],
             ["Green Tea Extract (EGCG)","400–500 mg EGCG/day","Inhibits COMT enzyme — prolongs noradrenaline activity; additive fat-burning effect with caffeine","Strong — multiple meta-analyses confirm 3–5% additional fat loss vs placebo"],
             ["L-Carnitine","2–3 g/day (L-Carnitine L-Tartrate)","Transports fatty acids into mitochondria for oxidation — rate-limiting step in fat metabolism. Works best with carbohydrates","Moderate — requires adequate tissue carnitine saturation over 4+ weeks"],
             ["Yohimbine HCl","0.2 mg/kg body weight, fasted","Alpha-2 adrenergic receptor antagonist — blocks the 'anti-fat-burning' receptors found in stubborn fat areas (lower abdomen, hips, thighs)","Moderate — significant for fasted cardio; no effect with elevated insulin"],
             ["Synephrine (Bitter Orange)","10–20 mg","Adrenergic agonist (beta-3 receptor) — increases metabolic rate without the cardiovascular side effects of ephedrine","Moderate — gentler alternative to ephedrine; synergistic with caffeine"],
             ["CLA (Conjugated Linoleic Acid)","3.2 g/day","Reduces fat cell (adipocyte) differentiation; mild fat oxidation increase","Weak-moderate — modest effects (0.5 lb/month vs placebo)"]]
    items.append(tbl(natural[0],[r for r in natural[1:]],TK,[(W-72)*f for f in [0.20,0.18,0.43,0.19]]))
    items.append(Paragraph("<b>Optimal Natural Stack Timing:</b> Caffeine + EGCG fasted 30 min before cardio. Yohimbine fasted with cardio (insulin blocks Yohimbine's effect). L-Carnitine + carbohydrates. Take caffeine by 2 PM to avoid sleep disruption.", s["B"]))

    items += sh("8–9. CLENBUTEROL, ECA & T3", TK, s, "🔥")
    items.append(Paragraph("<b>ECA Stack (Ephedrine + Caffeine + Aspirin):</b>", s["SSH"]))
    for x in ["<b>Ephedrine:</b> 20–25 mg + <b>Caffeine:</b> 200 mg + <b>Aspirin:</b> 81 mg — taken 2–3× daily",
               "Synergistic mechanism: Ephedrine (beta-adrenergic agonist) increases noradrenaline; caffeine blocks adenosine AND inhibits phosphodiesterase (prolongs cAMP effect); aspirin (prostaglandin inhibition) extends the thermogenic response",
               "Cycle: 3 weeks ON (build tolerance) / 1 week OFF. Never exceed 3× daily dose",
               "Avoid if: hypertension, heart conditions, anxiety disorders, thyroid disease"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Clenbuterol (see PDF 01 for full protocol):</b> 20→120 mcg/day, 2 weeks on/off. Beta-2 agonist — thermogenic + mild anabolic. More powerful than ECA; more side effects.", s["B"]))
    items.append(Paragraph("<b>T3 Thyroid Protocol (see PDF 01 for full details):</b> 25→50→25 mcg/day tapered protocol. Dramatically increases metabolic rate. Mandatory taper — cold turkey causes hypothyroid crash.", s["B"]))

    items += sh("10–12. CONTEST PREP · PEAK WEEK · MAINTENANCE", TK, s, "🏆")
    items.append(Paragraph("<b>12-Week Contest Prep Framework:</b>", s["SSH"]))
    prep=[["Weeks","Deficit","Cardio Volume","Compounds (optional)","Focus"],
          ["12–10","500 kcal","30 min LISS 4×/wk","None / natural stack","Establish discipline; set macro targets"],
          ["9–7","500–600 kcal","40 min LISS 5×/wk","Clen/ECA if desired","Accelerate fat loss; refeed 1×/week"],
          ["6–4","500–700 kcal","45 min LISS 6×/wk + 2× HIIT","T3 25–50 mcg if using","Address stubborn fat; diet break optional"],
          ["3–2","600–700 kcal","50 min 2×/day or 60 min 1×/day","Peak compounds if using","Final detail; reduce water-retaining foods"],
          ["1 (Peak Week)","Carb deplete → Carb load","Minimal (just pump sessions)","Diuretics only if very experienced","See Peak Week protocol below"]]
    items.append(tbl(prep[0],[r for r in prep[1:]],TK,[(W-72)*f for f in [0.10,0.12,0.18,0.20,0.40]]))
    items.append(Paragraph("<b>Peak Week Protocol:</b>", s["SSH"]))
    for x in ["Days 7–5 (Depletion): Reduce carbs to 50g/day; increase cardio to 2×/day; glycogen depletes for max carb loading response",
               "Days 4–3 (Loading): 600–800g carbs/day from clean sources; reduce training volume dramatically",
               "Day 2: Moderate carbs (400g); assess fullness; adjust if needed",
               "Day 1 (Show Day): Small carb and sodium doses with good food; stay hydrated; avoid new foods",
               "Water: Drink normally until night before; slight reduction day of show. Never extreme dehydration — dangerous and rarely improves conditioning"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Maintaining Results (Post-Cut Reverse Diet):</b> Increase calories by 50–100 kcal/week over 8–12 weeks back to maintenance TDEE. Rapid post-cut calorie increase triggers fat regain ('rebound'). Reverse dieting allows metabolic rate to normalize while minimizing fat regain.", s["B"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 11 — WOMEN'S COMPLETE BODY TRANSFORMATION
# ════════════════════════════════════════════════════════════
def pdf_women_fit(path):
    TK="women_fit"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["WOMEN'S COMPLETE","BODY TRANSFORMATION","GUIDE"],
                   "12-Week Training · Nutrition · Hormone Awareness · Supplements · Anavar Protocol",
                   "Science-designed for female physiology — lean, strong, and confident",
                   TK, s, badges=["12 WEEKS","FEMALE PHYSIOLOGY","TRAINING + DIET","SUPPLEMENT STACK"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Female Physiology & Body Composition Science","2.  The 12-Week Transformation Framework",
               "3.  Weeks 1–4: Foundation Phase","4.  Weeks 5–8: Intensification Phase",
               "5.  Weeks 9–12: Peak Phase","6.  Nutrition for Women's Body Recomposition",
               "7.  Cardio & Fat Burning Protocols for Women","8.  Training With Your Menstrual Cycle",
               "9.  Evidence-Based Supplement Stack for Women","10. Anavar Protocol for Women (Advanced)",
               "11. Primobolan for Women (Advanced)","12. Progress Tracking & Long-Term Strategies"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. FEMALE PHYSIOLOGY & BODY COMPOSITION SCIENCE", TK, s, "💜")
    items.append(Paragraph("Women's body composition responds to diet and training differently than men's due to distinct hormonal profiles — primarily higher estrogen and lower testosterone. Understanding these differences enables a training and nutrition approach that <b>works with</b> female physiology, not against it.", s["BJ"]))
    diffs=[["Factor","Women","Men","Strategic Implication"],
           ["Testosterone","20–60 ng/dL (15–30× lower)","300–1000 ng/dL","Slower muscle growth; longer timeframe needed — be patient"],
           ["Estrogen","Cyclical 30–400 pg/mL","15–60 pg/mL (stable)","Promotes fat storage in hips/thighs; estrogen-dominant fat patterns"],
           ["Fat oxidation","Higher at rest and during exercise","More glucose-dependent","Women are natural fat-burners; LISS cardio highly effective"],
           ["Muscle fiber distribution","Higher type I (endurance) ratio","Higher type II (fast-twitch)","Higher reps (12–20) often produce better female hypertrophy"],
           ["Strength:weight ratio","Generally lower","Generally higher","But women gain strength at similar RATE as men — neural adaptation"],
           ["Cortisol sensitivity","Higher cortisol response to stress","Lower","Sleep and stress management are CRITICAL for women's physique goals"]]
    items.append(tbl(diffs[0],[r for r in diffs[1:]],TK,[(W-72)*f for f in [0.20,0.20,0.18,0.42]]))

    items += sh("2. 12-WEEK TRANSFORMATION FRAMEWORK", TK, s, "📅")
    framework=[["Phase","Weeks","Caloric Target","Training Focus","Cardio","Expected Result"],
               ["Foundation","1–4","Mild deficit (-250 kcal)","Learn movements; build neuromuscular connection","3× 30min LISS/week","5–8 lbs fat loss; strength foundation built"],
               ["Intensification","5–8","Moderate deficit (-400 kcal)","Increase volume; progressive overload; add intensity techniques","4× 35min/week + 1× HIIT","Additional 5–7 lbs fat; visible muscle shape"],
               ["Peak","9–12","Aggressive deficit (-500 kcal)","Max volume; minimal rest; focus on weak points","5× 40min LISS + 2× HIIT","Final 3–5 lbs fat; conditioning peak; lean physique"]]
    items.append(tbl(framework[0],[r for r in framework[1:]],TK,[(W-72)*f for f in [0.13,0.09,0.16,0.23,0.17,0.22]]))

    items += sh("3–5. PHASE TRAINING PROGRAMS", TK, s, "🏋")
    items.append(Paragraph("<b>Weeks 1–4 — Foundation Program (3 days/week):</b>", s["SSH"]))
    phase1=[["Day","Muscle Groups","Key Exercises","Sets × Reps"],
            ["Day A","Full Body","Goblet Squat · Romanian Deadlift · DB Bench · Seated Row · Shoulder Press · Plank","3×12–15 each"],
            ["Day B","Full Body","Bulgarian Split Squat · Hip Thrust · Incline DB Press · Pull-Ups/Assisted · Lateral Raises · Dead Bug","3×12–15 each"],
            ["Day C","Full Body","Sumo Deadlift · Step-Ups · Cable Flyes · Face Pull · Arnold Press · Russian Twist","3×15–20 each"]]
    items.append(tbl(phase1[0],[r for r in phase1[1:]],TK,[(W-72)*f for f in [0.10,0.18,0.44,0.28]]))
    items.append(Paragraph("<b>Weeks 5–8 — Intensification (4 days/week, Upper/Lower):</b>", s["SSH"]))
    phase2=[["Day","Focus","Exercises (4 sets each)","Intensity Technique"],
            ["Mon/Thu","Upper (Strength+Volume)","Bench Press · OHP · Barbell Row · Chin-Ups · Cable Flyes · Lateral Raises","Drop sets on last set of isolation"],
            ["Tue/Fri","Lower (Glutes/Legs priority)","Hip Thrust · RDL · Hack Squat · Leg Curl · Walking Lunge · Calf Raise","Pause reps on hip thrust and RDL"]]
    items.append(tbl(phase2[0],[r for r in phase2[1:]],TK,[(W-72)*f for f in [0.10,0.20,0.42,0.28]]))
    items.append(Paragraph("<b>Weeks 9–12 — Peak (5 days/week, PPL-style):</b> Full PPL split — same exercises as intensification phase with added volume (5 sets), shorter rest (60–75s), supersets for isolation work, and additional glute/shoulder specialization work on accessory days.", s["B"]))

    items += sh("6–7. NUTRITION & CARDIO FOR WOMEN", TK, s, "🍽")
    macro=[["Macro","Target","Why","Top Foods"],
           ["Protein","0.8–1.2 g/lb body weight","Muscle preservation + satiety — women often under-eat protein","Paneer, Greek yogurt, eggs, chicken, fish, tofu, legumes"],
           ["Carbohydrates","100–180 g/day","Training performance; thyroid function; serotonin production (mood)","Oats, brown rice, sweet potato, fruits, vegetables"],
           ["Fats","50–70 g/day","Estrogen production; skin health; fat-soluble vitamins","Avocado, nuts, olive oil, fatty fish, ghee"],
           ["Calories","BMR × 1.4 - 300–500","Moderate deficit for sustainable results without hormonal disruption","Quality whole foods; avoid ultra-processed foods"]]
    items.append(tbl(macro[0],[r for r in macro[1:]],TK,[(W-72)*f for f in [0.14,0.18,0.32,0.36]]))
    items.append(Paragraph("<b>Women's Cardio Priority Order:</b>", s["SSH"]))
    for x in ["<b>Priority 1 — LISS Walking (daily):</b> 8,000–12,000 steps/day. Zero muscle stress; high fat burning; cortisol-neutral",
               "<b>Priority 2 — Moderate Cardio (3–4×/week):</b> 30–40 min cycling, swimming, elliptical at 65–70% max HR",
               "<b>Priority 3 — HIIT (max 2×/week):</b> 20 min sessions maximum; avoid during luteal phase; counterproductive if overdone",
               "<b>Fasted cardio:</b> Effective (20% more fat oxidized fasted) — but not mandatory; adherence > perfect protocol"]:
        items.append(bl(x, s))

    items += sh("8. TRAINING WITH YOUR MENSTRUAL CYCLE", TK, s, "🌙")
    cycle=[["Phase","Days","Best Training","Adjust Diet","Key Notes"],
           ["Menstrual","1–5","Light movement; yoga; walking","Normal calories; prioritize iron-rich foods","Energy often low; don't skip training entirely — movement helps cramps"],
           ["Follicular","6–13","Heavy strength training; HIIT; PRs","Normal to slight surplus carbs","Rising estrogen = peak strength and pain tolerance; best time for max effort"],
           ["Ovulatory","14","Absolute maximum performance day","Normal","Peak power output; set new personal records; joints slightly looser (injury awareness)"],
           ["Luteal","15–28","Moderate intensity; more rest; reduce HIIT","Increase calories by 100–200 kcal; complex carbs","Progesterone dominates; fatigue, cravings increase; body temperature elevated"]]
    items.append(tbl(cycle[0],[r for r in cycle[1:]],TK,[(W-72)*f for f in [0.14,0.09,0.22,0.20,0.35]]))

    items += sh("9. EVIDENCE-BASED SUPPLEMENT STACK FOR WOMEN", TK, s, "💊")
    supp=[["Supplement","Dose","Evidence for Women"],
          ["Iron (if deficient)","18–27 mg/day (with 500mg Vitamin C)","Menstrual iron loss; deficiency causes fatigue, poor recovery, reduced VO2 max"],
          ["Magnesium Glycinate","300–400 mg nightly","Reduces PMS severity 40% in trials; improves sleep quality; muscle recovery"],
          ["Omega-3 (EPA+DHA)","2–3 g/day","Reduces menstrual pain (prostaglandin inhibition); improves body composition; anti-inflammatory"],
          ["Vitamin D3 + K2","3000 IU D3 + 100 mcg K2","Bone density; immune; testosterone production (even in women)"],
          ["Ashwagandha (KSM-66)","300 mg twice daily","Reduces cortisol 20–30%; improves thyroid T4→T3 conversion; reduces stress eating"],
          ["Creatine Monohydrate","3–5 g/day","Often overlooked for women — multiple studies show 5–15% strength gain; improves brain health; no fat gain"],
          ["Collagen Peptides","10–15 g/day","Joint integrity; skin elasticity; connective tissue — important for high-volume training"]]
    items.append(tbl(supp[0],[r for r in supp[1:]],TK,[(W-72)*f for f in [0.22,0.16,0.62]]))

    items += sh("10–11. ANAVAR & PRIMOBOLAN FOR WOMEN (ADVANCED)", TK, s, "⚡")
    items.append(wb("These compounds are controlled substances in many jurisdictions. This information is provided for educational purposes only. Consult a physician. Women are significantly more sensitive to anabolic compounds — virilization (voice deepening, clitoral enlargement, body hair) can be PERMANENT.", TK, s))
    items.append(Paragraph("<b>Anavar (Oxandrolone) — Most Female-Friendly Anabolic:</b>", s["SSH"]))
    anavar=[["Parameter","Conservative","Moderate","Aggressive"],
            ["Dose","2.5–5 mg/day","5–10 mg/day","10–15 mg/day"],
            ["Duration","6 weeks","6–8 weeks","8 weeks MAX"],
            ["Virilization Risk","Very low","Low","Moderate"],
            ["Expected Results","Lean maintenance + strength","5–8 lbs lean mass; hardness","10+ lbs lean mass; significant virilization risk"],
            ["PCT","None required","None typically","None — but monitor hormones"]]
    items.append(tbl(anavar[0],[r for r in anavar[1:]],TK,[(W-72)*f for f in [0.24,0.26,0.26,0.24]]))
    items.append(Paragraph("<b>Primobolan (Methenolone Acetate) for Women:</b>", s["SSH"]))
    for x in ["Dose: 25–75 mg/week injectable OR 25–50 mg/day oral acetate form",
               "Duration: 8–12 weeks — excellent lean mass quality with minimal virilization",
               "Often considered the 'queen of women's compounds' — very low androgenic activity",
               "Stop immediately at first sign of voice changes, clitoral sensitivity changes, or excess body hair growth"]:
        items.append(bl(x, s))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 12 — INDIAN BODYBUILDER'S DIET BIBLE
# ════════════════════════════════════════════════════════════
def pdf_indian(path):
    TK="indian"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["THE INDIAN BODYBUILDER'S","COMPLETE NUTRITION BIBLE"],
                   "High-Protein Indian Foods · Meal Plans for Every Goal · Budget Guide · Restaurant Strategies",
                   "Build muscle and lose fat with traditional Indian cuisine — no imported foods needed",
                   TK, s, badges=["INDIAN FOODS ONLY","3 MEAL PLANS","BUDGET GUIDE","RESTAURANT TIPS"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Top 30 High-Protein Indian Foods Ranked","2.  Indian Foods Macronutrient Reference Table",
               "3.  Bulking Meal Plan — 3000–3500 kcal/day","4.  Cutting Meal Plan — 1600–2000 kcal/day",
               "5.  Maintenance & Recomp Plan — 2200–2600 kcal/day","6.  Pre-Workout Meals (Indian)",
               "7.  Post-Workout Meals (Indian)","8.  Budget-Friendly Protein Sources",
               "9.  Eating Out — Indian Restaurant Strategy","10. Festival & Social Event Survival Guide",
               "11. Supplement Stack for Indian Athletes","12. Common Myths About Indian Food & Fitness"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. TOP 30 HIGH-PROTEIN INDIAN FOODS", TK, s, "🏆")
    foods=[["Rank","Food","Serving","Protein","Calories","Cost/Serving"],
           ["1","Chicken Breast (skinless)","100g","31g","165 kcal","₹15–20"],
           ["2","Paneer (low-fat homemade)","100g","18–22g","260 kcal","₹20–25"],
           ["3","Eggs (whole)","1 large","6g","70 kcal","₹6–8"],
           ["4","Moong Dal (cooked)","1 cup (200g)","14g","212 kcal","₹8–12"],
           ["5","Chana Dal (cooked)","1 cup","15g","270 kcal","₹8–12"],
           ["6","Rajma / Kidney Beans","1 cup (cooked)","15g","225 kcal","₹12–15"],
           ["7","Soya Chunks (dried)","50g dry","26g","170 kcal","₹10–15"],
           ["8","Greek Yogurt / Hung Curd","200g","12–16g","130 kcal","₹25–35"],
           ["9","Tuna (canned in water)","100g","25g","116 kcal","₹40–60"],
           ["10","Rohu / Katla Fish","100g cooked","22g","97 kcal","₹25–40"],
           ["11","Sattu (roasted chickpea flour)","50g","12g","180 kcal","₹10–15"],
           ["12","Quinoa (cooked)","1 cup (185g)","8g","222 kcal","₹50–70"],
           ["13","Cow's Milk (full fat)","300ml","9g","186 kcal","₹15–20"],
           ["14","Whey Protein (local brand)","1 scoop (30g)","22–25g","120 kcal","₹50–80"],
           ["15","Chickpeas / Kabuli Chana","1 cup cooked","15g","269 kcal","₹12–18"]]
    items.append(tbl(foods[0],[r for r in foods[1:]],TK,[(W-72)*f for f in [0.07,0.24,0.15,0.12,0.14,0.13]]))

    items += sh("2. MACRONUTRIENT REFERENCE TABLE", TK, s, "📊")
    macro_ref=[["Food (100g unless noted)","Calories","Protein","Carbs","Fats","Fiber"],
               ["Cooked White Rice","130","2.7g","28g","0.3g","0.4g"],
               ["Whole Wheat Roti (1 medium)","71","2.5g","13g","1g","1.2g"],
               ["Oats (dry)","389","17g","66g","7g","10g"],
               ["Sweet Potato (cooked)","86","1.6g","20g","0.1g","3g"],
               ["Banana (medium)","89","1.1g","23g","0.3g","2.6g"],
               ["Broccoli (100g)","34","2.8g","7g","0.4g","2.6g"],
               ["Spinach (raw 100g)","23","2.9g","3.6g","0.4g","2.2g"],
               ["Almonds (30g)","174","6g","6g","15g","3g"],
               ["Peanut Butter (1 tbsp)","94","4g","3g","8g","1g"],
               ["Ghee (1 tsp/5g)","45","0","0","5g","0"],
               ["Coconut Oil (1 tbsp)","120","0","0","14g","0"]]
    items.append(tbl(macro_ref[0],[r for r in macro_ref[1:]],TK,[(W-72)*f for f in [0.32,0.12,0.12,0.12,0.12,0.10]]))
    items.append(PageBreak())

    items += sh("3. BULKING MEAL PLAN — 3000–3500 KCAL/DAY", TK, s, "💪")
    items.append(Paragraph("Target macros: 180–220g protein · 350–400g carbs · 80–100g fats", s["B"]))
    bulk=[["Meal","Time","Menu","~Protein","~Kcal"],
          ["Breakfast","7:00 AM","5 whole eggs scrambled with 50g paneer + 2 multigrain rotis + 1 banana + masala chai (full fat milk)","35g","620"],
          ["Mid-Morning","10:00 AM","50g soya chunks (cooked in minimal oil) + 1 cup brown rice + 100g curd + 1 fruit","25g","500"],
          ["Pre-Workout","12:30 PM","3 rotis + 150g chicken/paneer curry + salad","35g","580"],
          ["Post-Workout","3:30 PM","1 scoop whey protein + 1 banana + 10 almonds","30g","320"],
          ["Dinner","7:00 PM","200g dal (any) + 3 rotis + 100g paneer sabzi + vegetables","35g","680"],
          ["Before Bed","9:30 PM","200g full-fat curd + 10g chia seeds + handful of mixed nuts","15g","300"],
          ["TOTAL","","","175–200g","3000–3500"]]
    items.append(tbl(bulk[0],[r for r in bulk[1:]],TK,[(W-72)*f for f in [0.15,0.12,0.44,0.13,0.10]]))

    items += sh("4. CUTTING MEAL PLAN — 1600–2000 KCAL/DAY", TK, s, "🔥")
    items.append(Paragraph("Target macros: 160–180g protein · 120–150g carbs · 40–55g fats", s["B"]))
    cut=[["Meal","Time","Menu","~Protein","~Kcal"],
         ["Breakfast","7:00 AM","3 egg whites + 1 whole egg scrambled + ½ cup oats with water + green tea","30g","320"],
         ["Mid-Morning","10:30 AM","1 cup moong dal soup + 100g cucumber + 1 cup green tea","12g","180"],
         ["Lunch","1:00 PM","150g grilled chicken/paneer + 1 roti + large salad (cucumber, tomato, onion, lemon)","40g","380"],
         ["Snack","4:30 PM","200g low-fat curd + 1 tsp jeera + 10 almonds","14g","200"],
         ["Dinner","7:30 PM","200g dal (thin) + 2 rotis + steamed mixed vegetables + salad","28g","450"],
         ["TOTAL","","","124–150g","1600–1800"]]
    items.append(tbl(cut[0],[r for r in cut[1:]],TK,[(W-72)*f for f in [0.15,0.12,0.44,0.13,0.10]]))

    items += sh("5. RECOMP PLAN — 2200–2600 KCAL/DAY", TK, s, "⚖")
    items.append(Paragraph("Recomposition (building muscle and losing fat simultaneously) requires eating near TDEE with high protein and strategic carb timing:", s["B"]))
    recomp=[["Meal","Menu","Notes"],
            ["Breakfast","4 whole eggs + 2 rotis + 100g vegetables + chai","High protein start"],
            ["Post-Workout","50g whey/sattu + 1 banana + 5 almonds","Fast carbs + protein within 45 min"],
            ["Lunch","175g dal/legumes + 2 rotis + 100g paneer + salad","Largest meal; most carbs"],
            ["Snack","150g Greek yogurt + mixed seeds","Protein + healthy fats"],
            ["Dinner","200g fish or chicken + 1 roti + vegetables + salad","Protein dominant; reduce carbs at night"]]
    items.append(tbl(recomp[0],[r for r in recomp[1:]],TK,[(W-72)*f for f in [0.16,0.50,0.34]]))

    items += sh("6–7. PRE & POST WORKOUT MEALS", TK, s, "⏱")
    items.append(Paragraph("<b>Pre-Workout Meals (2–3 hours before training):</b>", s["SSH"]))
    pre=[["Option","Protein","Carbs","Preparation Time"],
         ["3 rotis + dal + curd","20–25g","45–55g","Cook ahead; reliable classic"],
         ["Oats porridge + boiled egg (2) + banana","22g","60g","15 min prep; easy"],
         ["Sattu drink (50g sattu + lemon + salt + water) + 3 almonds","14g","25g","5 min; great for busy mornings"],
         ["Brown rice (1 cup) + paneer (100g) + vegetables","25g","45g","Meal-prep friendly"]]
    items.append(tbl(pre[0],[r for r in pre[1:]],TK,[(W-72)*f for f in [0.36,0.14,0.14,0.36]]))
    items.append(Paragraph("<b>Post-Workout Meals (within 45–60 min of training):</b>", s["SSH"]))
    post=[["Option","Protein","Carbs","Why"],
          ["Whey protein + banana + 10 almonds","28g","30g","Fastest; optimal amino acid profile for muscle protein synthesis"],
          ["Poha (cooked) + 2 boiled eggs","18g","40g","Complete meal; traditional Indian; fast carbs from poha"],
          ["Sattu lassi (50g sattu + curd + banana)","18g","45g","Budget-friendly whole food option; high in fiber and minerals"],
          ["Paneer bhurji + 2 rotis","30g","28g","High protein; great if training before lunch or dinner"]]
    items.append(tbl(post[0],[r for r in post[1:]],TK,[(W-72)*f for f in [0.30,0.12,0.12,0.46]]))

    items += sh("8–12. BUDGET · RESTAURANTS · FESTIVALS · SUPPLEMENTS · MYTHS", TK, s, "📋")
    items.append(Paragraph("<b>Budget-Friendly Protein Sources (ranked by protein-per-rupee):</b>", s["SSH"]))
    budget=[["Rank","Food","Protein per ₹10","Notes"],
            ["1","Eggs","~8g","Best value in India; complete protein"],
            ["2","Moong/Chana Dal","~12g","Dried pulse; incredible value; high fibre"],
            ["3","Soya Chunks","~18g (dry weight basis)","Best plant protein per rupee in India"],
            ["4","Sattu","~14g","Underused superfood; complete amino profile"],
            ["5","Paneer (homemade)","~9g","Make from full-fat milk — 50% cheaper than store-bought"],
            ["6","Tuna (canned)","~6g","Great value if on sale; complete protein"]]
    items.append(tbl(budget[0],[r for r in budget[1:]],TK,[(W-72)*f for f in [0.08,0.22,0.22,0.48]]))
    items.append(Paragraph("<b>Restaurant Ordering Strategy:</b>", s["SSH"]))
    for x in ["Ask for <b>less oil/ghee</b> in sabzi — most restaurants use 3–5× the home cooking amount",
               "Choose <b>grilled/tandoor options</b> over fried: tandoori chicken vs butter chicken saves 200+ kcal",
               "<b>Dal over paneer</b> dishes when protein-focused: dal provides better protein-to-calorie ratio",
               "Skip biryani; choose <b>brown rice or 2 rotis</b> instead; avoid paratha (loaded with ghee)",
               "Order <b>raita</b> (curd-based) instead of heavy gravies; ask for salad before meal",
               "At weddings/buffets: <b>protein-first strategy</b> — fill plate with dal, paneer, chicken before touching rice/bread"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Festival Survival Guide:</b>", s["SSH"]))
    for x in ["<b>Diwali/Eid/Christmas:</b> Eat normally all day; at event, protein-first then 1–2 portions of festive food. Guilt-free enjoyment in moderation",
               "<b>Holi/Navratri:</b> Stock up on fruit, nuts, and dairy alternatives if fasting is cultural practice",
               "<b>Ramadan fasting:</b> Sehri (pre-dawn) should be high-protein + complex carbs; Iftar should start with dates + water then protein-rich meal before carbs"]:
        items.append(bl(x, s))
    myths=[["Myth","Reality"],
           ["Dal makes you fat","Dal is one of the best weight-loss foods — high protein, high fibre, low fat. Problem is the ghee tadka, not the dal itself"],
           ["Ghee is unhealthy","Pure cow ghee contains CLA, butyric acid, and fat-soluble vitamins. 1–2 tsp/day is beneficial, not harmful"],
           ["Rice/roti cause weight gain","No single food causes weight gain — total caloric surplus does. White rice has lower fibre than brown but is not 'bad'"],
           ["Indian food can't build muscle","India produces world-class athletes on dal-rice-sabzi diets. Total protein intake matters, not the source"],
           ["Need expensive protein supplements","Soya chunks, eggs, and dal provide complete protein at a fraction of whey protein cost"]]
    items.append(Paragraph("<b>Common Myths Debunked:</b>", s["SSH"]))
    items.append(tbl(myths[0],[r for r in myths[1:]],TK,[(W-72)*f for f in [0.30,0.70]]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 13 — PRE/INTRA/POST WORKOUT OPTIMIZATION
# ════════════════════════════════════════════════════════════
def pdf_preworkout(path):
    TK="preworkout"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["PRE · INTRA · POST","WORKOUT OPTIMIZATION","COMPLETE SUPPLEMENT GUIDE"],
                   "Every Ingredient Analyzed · DIY Formulas · Intra-Workout Fuel · Recovery Stack",
                   "Stop wasting money on proprietary blends — understand what actually works",
                   TK, s, badges=["INGREDIENT SCIENCE","DIY FORMULAS","INTRA-WORKOUT","RECOVERY STACK"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Pre-Workout Science — What Actually Works","2.  The Stimulant Layer — Caffeine, Dynamine, TeaCrine",
               "3.  The Pump Layer — L-Citrulline, Arginine, Norvaline","4.  The Performance Layer — Beta-Alanine, Creatine, Betaine",
               "5.  The Focus Layer — Alpha-GPC, Tyrosine, Huperzine A","6.  DIY Pre-Workout Formula Guide",
               "7.  Intra-Workout Nutrition — What to Consume During Training",
               "8.  Post-Workout — Protein Synthesis Window (Myth vs Reality)",
               "9.  The Anabolic Window — Timing & Protocol","10. Post-Workout Supplement Stack",
               "11. Pre-Workout Timing & Tolerance Management","12. What to Avoid — Useless Ingredients"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. PRE-WORKOUT SCIENCE", TK, s, "🔬")
    items.append(Paragraph("The pre-workout supplement market is a ₹5,000 crore industry globally, yet most products contain proprietary blends with clinically ineffective doses behind exotic names. This guide cuts through the marketing to show you <b>exactly which ingredients work, at what doses, and why</b>.", s["BJ"]))
    items.append(rn("A 2021 systematic review (Martinez et al., Journal of the International Society of Sports Nutrition) analyzed 44 commercially available pre-workout products. Finding: 75% were under-dosed for key active ingredients relative to clinically validated doses. The average product contained ingredients at 40% of the evidence-based dose.", TK, s))
    eff=[["Evidence Level","Ingredients","Benefit"],
         ["Grade A (Very Strong)","Caffeine, Creatine, Citrulline, Beta-Alanine","Primary drivers of pre-workout performance"],
         ["Grade B (Good)","Betaine, Alpha-GPC, Tyrosine, Theanine","Meaningful secondary contributors"],
         ["Grade C (Moderate)","Beet Root Extract, Norvaline, Taurine","Modest benefits; worth including at correct dose"],
         ["Grade D (Weak/Inconclusive)","BCAAs pre-workout, Glutamine, Vitamin B12","Limited evidence for acute pre-workout benefit"],
         ["Grade F (No Evidence)","'Proprietary blends', fairy-dusted exotics, most herbals at under-studied doses","Marketing only"]]
    items.append(tbl(eff[0],[r for r in eff[1:]],TK,[(W-72)*f for f in [0.22,0.36,0.42]]))

    items += sh("2. THE STIMULANT LAYER", TK, s, "⚡")
    items.append(Paragraph("<b>Caffeine Anhydrous — The Gold Standard Stimulant:</b>", s["SSH"]))
    items.append(Paragraph("Caffeine is the most researched ergogenic aid in sports nutrition history. It works via adenosine receptor antagonism — blocking the sleep-inducing signal in your brain. This increases adrenaline, dopamine, and acetylcholine simultaneously.", s["BJ"]))
    for x in ["<b>Optimal dose:</b> 3–6 mg/kg body weight. 70kg athlete: 210–420 mg",
               "<b>Timing:</b> 30–45 min before training (peak plasma: 45–60 min)",
               "<b>Tolerance management:</b> Cycle caffeine — take 2 days off per week to prevent receptor downregulation",
               "<b>Benefits:</b> 10–15% increase in strength output; significant endurance improvement; pain perception reduction; improved focus and motivation",
               "<b>Caution:</b> Half-life 5–6 hours; avoid after 2 PM if bedtime is 10 PM"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Dynamine (Methylliberine) + TeaCrine (Theacrine):</b>", s["SSH"]))
    for x in ["Dynamine: Faster onset than caffeine (15 min); dopaminergic; pairs well with caffeine",
               "TeaCrine: Same mechanism as caffeine but zero tolerance development over time",
               "Effective stack: Caffeine 200mg + Dynamine 100mg + TeaCrine 50mg — fast onset + sustained effect"]:
        items.append(bl(x, s))

    items += sh("3–4. THE PUMP & PERFORMANCE LAYERS", TK, s, "💉")
    pump=[["Ingredient","Clinical Dose","Mechanism","Effect"],
          ["L-Citrulline","6–10 g (not citrulline malate)","Converts to arginine in kidneys → nitric oxide (NO) production → vasodilation","Best pump ingredient; superior to arginine due to better oral bioavailability"],
          ["Agmatine Sulfate","500 mg–1 g","NOS inhibitor → amplifies NO signaling; also reduces pain perception","Synergistic with citrulline; unique pain-reducing benefit"],
          ["Norvaline","100–200 mg","Arginase enzyme inhibitor — prevents breakdown of arginine into urea; prolongs NO effect","Modest addition; dose-dependent benefit"],
          ["HydroMax Glycerol","2–3 g","Hyperhydrates muscle cells; draws water into muscle → skin-splitting pump; anti-dehydration","Excellent for appearance and performance in hot conditions"]]
    items.append(tbl(pump[0],[r for r in pump[1:]],TK,[(W-72)*f for f in [0.18,0.14,0.38,0.30]]))
    perf=[["Ingredient","Clinical Dose","Mechanism","Expected Benefit"],
          ["Beta-Alanine","3.2–6.4 g","Combines with histidine → carnosine in muscle → buffers hydrogen ions (acid) → delays fatigue","~3% endurance increase; more reps in 8–20 rep range. Causes tingles (paraesthesia) — normal, harmless"],
          ["Creatine Monohydrate","3–5 g (maintenance) or 20g/day × 5 days (loading)","Increases phosphocreatine stores → faster ATP regeneration → more power and strength","3–8% strength increase; 1–3 kg lean mass over 4 weeks; one of the most proven supplements ever"],
          ["Betaine Anhydrous","2.5 g","Osmolyte — improves cellular hydration similar to creatine; may increase GH and IGF-1","~4% strength; 2% power output increase; 1.3 kg lean mass in some trials"]]
    items.append(tbl(perf[0],[r for r in perf[1:]],TK,[(W-72)*f for f in [0.20,0.16,0.38,0.26]]))

    items += sh("5–6. FOCUS LAYER & DIY FORMULA", TK, s, "🧠")
    focus=[["Ingredient","Dose","Mechanism","Best For"],
           ["Alpha-GPC","300–600 mg","Acetylcholine precursor — enhances mind-muscle connection; increases GH output acutely","Mind-muscle connection; neurological focus"],
           ["L-Tyrosine","500–2000 mg","Dopamine and noradrenaline precursor; maintains cognitive performance under stress/fatigue","Focus under high-stress training; stimulant augmentation"],
           ["L-Theanine","100–200 mg (with caffeine)","GABAergic modulation; reduces caffeine jitteriness; improves 'calm focus'","Pairs with caffeine 2:1 ratio; reduces anxiety without reducing stimulation"],
           ["Huperzine A","50–200 mcg","Acetylcholinesterase inhibitor — prevents breakdown of acetylcholine; long half-life","Occasional use only (every 2–3 days) — accumulates; avoid daily"]]
    items.append(tbl(focus[0],[r for r in focus[1:]],TK,[(W-72)*f for f in [0.16,0.13,0.38,0.33]]))
    items.append(Paragraph("<b>DIY Pre-Workout Formula (per serving):</b>", s["SSH"]))
    diy=[["Ingredient","Amount","Cost/Serving"],
         ["Caffeine Anhydrous","200 mg","₹0.50"],
         ["L-Citrulline","6000 mg","₹8–12"],
         ["Beta-Alanine","3200 mg","₹4–6"],
         ["Creatine Monohydrate","5000 mg","₹3–5"],
         ["Alpha-GPC 50%","300 mg","₹6–10"],
         ["L-Theanine","200 mg","₹2–4"],
         ["Betaine Anhydrous","2500 mg","₹5–8"],
         ["Agmatine Sulfate","500 mg","₹3–5"],
         ["TOTAL","~17.7g powder","₹30–50 (vs ₹200–500 for commercial)"]]
    items.append(tbl(diy[0],[r for r in diy[1:]],TK,[(W-72)*f for f in [0.40,0.25,0.35]]))

    items += sh("7–8. INTRA-WORKOUT & POST-WORKOUT", TK, s, "⏱")
    items.append(Paragraph("<b>Intra-Workout Nutrition (for sessions >60 minutes):</b>", s["SSH"]))
    intra=[["Component","Amount","Source","Purpose"],
           ["Fast Carbohydrates","20–40 g per hour","Dextrose, Cyclic Dextrin, banana, dates","Maintains muscle glycogen; prevents cortisol spike; sustains performance in 2nd hour"],
           ["Essential Amino Acids (EAAs)","6–10 g","EAA supplement or 20g whey (smaller sip)","Prevents muscle protein breakdown; stimulates synthesis during training"],
           ["Electrolytes","Full spectrum","Sports drink / electrolyte powder / salt + potassium","Prevents hyponatremia; maintains muscle contraction; crucial in Indian heat"],
           ["Water","500–800 mL per hour","Plain water","Prevents dehydration-induced strength loss (2% dehydration = 10% strength loss)"]]
    items.append(tbl(intra[0],[r for r in intra[1:]],TK,[(W-72)*f for f in [0.22,0.14,0.22,0.42]]))
    items.append(Paragraph("<b>The Anabolic Window — Myth vs Reality:</b>", s["SSH"]))
    items.append(rn("Aragon & Schoenfeld (2013, JISSN) meta-analysis: the 'anabolic window' of 30–45 minutes post-workout is largely a myth for athletes who consumed a pre-workout meal. Muscle protein synthesis is elevated for 24–48 hours post-training — total daily protein intake matters far more than timing.", TK, s))
    for x in ["<b>If fasted before training:</b> Post-workout meal is critical — consume protein + carbs within 30 min",
               "<b>If fed before training:</b> Post-workout meal within 2–3 hours is sufficient",
               "<b>Always prioritize:</b> Total daily protein (1.5–2g/lb) over meal timing"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Post-Workout Supplement Stack:</b>", s["SSH"]))
    post=[["Supplement","Dose","Timing","Evidence"],
          ["Whey Protein Isolate","25–40 g","Within 1 hr post-workout","Strong — fastest digesting complete protein; leucine content drives MPS"],
          ["Creatine Monohydrate","5 g","Post-workout (slightly better than pre)","Strong — marginally superior post-workout absorption in one meta-analysis"],
          ["Fast Carbohydrates","40–80 g","Post-workout with protein","Strong — restores glycogen; insulin spike aids creatine uptake"],
          ["Tart Cherry Extract","480 mg","Post-workout","Moderate — reduces muscle soreness and inflammation significantly"]]
    items.append(tbl(post[0],[r for r in post[1:]],TK,[(W-72)*f for f in [0.22,0.14,0.20,0.44]]))
    items.append(Spacer(1,8)); items.append(Paragraph("Knowledge of ingredient mechanisms eliminates expensive marketing decisions. Build your stack on science, not branding.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")

# ════════════════════════════════════════════════════════════
# PDF 14 — NATURAL TESTOSTERONE OPTIMIZATION
# ════════════════════════════════════════════════════════════
def pdf_natural_t(path):
    TK="natural_t"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["NATURAL TESTOSTERONE","OPTIMIZATION","COMPLETE PROTOCOL"],
                   "Diet · Training · Sleep · Supplements · Lifestyle — Maximize Your Natural Hormones",
                   "Evidence-based strategies to double your natural T without drugs or injections",
                   TK, s, badges=["100% NATURAL","DIET PROTOCOLS","SUPPLEMENT SCIENCE","LIFESTYLE GUIDE"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Testosterone Physiology — How T is Made","2.  Dietary Strategies That Boost Testosterone",
               "3.  The Testosterone-Killing Foods to Avoid","4.  Training for Maximum Testosterone Response",
               "5.  Sleep — The Most Powerful Testosterone Booster","6.  Stress & Cortisol — The T-Killer",
               "7.  Evidence-Based Supplement Stack","8.  Micronutrients Critical for T Production",
               "9.  Lifestyle Optimization Protocol","10. Reading Your Blood Work",
               "11. Natural T Stack — Daily Protocol","12. When Natural Optimization Isn't Enough (TRT Consideration)"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. TESTOSTERONE PHYSIOLOGY", TK, s, "🔬")
    items.append(Paragraph("Testosterone is synthesized from cholesterol through a multi-step enzymatic process called <b>steroidogenesis</b>. Understanding this pathway reveals exactly which dietary, lifestyle, and supplementation interventions can optimize natural production.", s["BJ"]))
    items.append(Paragraph("<b>The Production Pathway:</b>", s["SSH"]))
    for x in ["<b>Cholesterol</b> is taken up by Leydig cells in the testes → converted to Pregnenolone by CYP11A1 enzyme",
               "Pregnenolone → DHEA → Androstenedione → <b>Testosterone</b>",
               "Testosterone can → DHT (via 5-alpha reductase) OR → Estradiol (via aromatase)",
               "HPT axis controls output: hypothalamus → GnRH → pituitary → LH → Leydig cells → Testosterone",
               "<b>Critical implication:</b> Cholesterol is NOT the enemy — it is the raw material for testosterone. Low-fat diets suppress T production"]:
        items.append(bl(x, s))
    items.append(rn("Hamalainen et al. (1984, Hormone Research): Healthy men who changed from high-fat diet (40% fat) to low-fat diet (25% fat) for 6 weeks showed a 12% reduction in total testosterone and 9% reduction in free testosterone. Fat intake directly correlates with T production.", TK, s))

    items += sh("2. DIETARY STRATEGIES THAT BOOST TESTOSTERONE", TK, s, "🍽")
    diet=[["Strategy","Evidence","Implementation"],
          ["Eat adequate fats (30–35% of calories)","Very Strong — fat provides cholesterol and fat-soluble vitamins needed for T production","Include eggs, whole milk, olive oil, avocado, nuts, and fatty fish daily"],
          ["Saturated fat (moderate amounts)","Strong — saturated fat positively correlates with T in multiple studies","Full-fat dairy, red meat 2–3×/week, coconut oil in cooking"],
          ["Monounsaturated fats","Strong — strongly correlated with LH pulse frequency","Olive oil (extra virgin), avocado, almonds — daily consumption"],
          ["Avoid severe caloric restriction","Very Strong — deficit >25% of TDEE suppresses T by 20–40%","Never eat below 1600 kcal for men; diet breaks every 8–12 weeks"],
          ["Adequate zinc from food","Very Strong — zinc is essential cofactor for testosterone-producing enzymes","Pumpkin seeds, beef, oysters, eggs, legumes daily"],
          ["Adequate carbohydrates","Moderate — low carb diets can reduce T via cortisol elevation","Don't go below 100g carbs if testosterone optimization is priority"]]
    items.append(tbl(diet[0],[r for r in diet[1:]],TK,[(W-72)*f for f in [0.25,0.22,0.53]]))

    items += sh("3. FOODS THAT LOWER TESTOSTERONE", TK, s, "⚠")
    items.append(wb("These foods, when consumed in excess, have documented evidence of reducing testosterone or increasing estrogen in men. Moderation is key — none need to be fully eliminated, but overconsumption is harmful.", TK, s))
    bad_foods=[["Food/Substance","Effect on T","Mechanism","Safe Threshold"],
               ["Alcohol (ethanol)","↓ T significantly","Direct Leydig cell toxin; increases cortisol; zinc depleter","<2 standard drinks/day; zero is optimal"],
               ["Soy products (high dose)","↓ T mildly","Phytoestrogens (isoflavones) — weak estrogen activity","<3 servings/day is generally safe for most men"],
               ["Flaxseed (high dose)","↓ T mildly (evidence mixed)","Lignans (phytoestrogens) + reduces DHT via 5-AR inhibition","1–2 tbsp/day acceptable"],
               ["Trans fats","↓ T strongly","Disrupts cell membrane function in Leydig cells; increases inflammation","Zero — eliminate completely"],
               ["Excess processed sugar","↓ T acutely after consumption","Insulin spike suppresses T for 1–2 hours post-consumption","Limit refined sugar; avoid chronic high sugar intake"],
               ["BPA / Plastics","↓ T (environmental)","Xenoestrogen — activates estrogen receptors; documented Leydig cell toxin","Avoid plastic water bottles; use glass or stainless steel"]]
    items.append(tbl(bad_foods[0],[r for r in bad_foods[1:]],TK,[(W-72)*f for f in [0.20,0.12,0.36,0.32]]))

    items += sh("4–5. TRAINING & SLEEP FOR TESTOSTERONE", TK, s, "🏋")
    items.append(Paragraph("<b>Training Protocol for Maximum Testosterone Response:</b>", s["SSH"]))
    for x in ["<b>Compound movements are essential:</b> Squat, deadlift, bench press, OHP, rows — recruit maximum muscle mass → maximum T response. Isolation exercises produce minimal hormonal response",
               "<b>Heavy loads produce higher T response:</b> Training at 85% 1RM produces greater acute T spike than 60% 1RM when volume is equated",
               "<b>Volume sweet spot:</b> 3–5 sets of compound movements. Beyond this, cortisol rise exceeds T benefit",
               "<b>Session length:</b> 45–75 min. Beyond 90 min, cortisol elevates sharply and T:cortisol ratio inverts (catabolic state)",
               "<b>Rest between sets:</b> 2–3 min for compound, heavy sets — allows T response to peak fully before next set",
               "<b>Frequency:</b> Training 4–5 days/week maintains persistently elevated T baseline vs 1–2 days/week"]:
        items.append(bl(x, s))
    items.append(rn("Kraemer & Ratamess (2005, Endocrine Reviews): Acute post-exercise testosterone elevation is most pronounced after high-volume, multi-joint exercises with short rest intervals at moderate-high loads. A single heavy squat session elevates T for 15–30 min post-workout.", TK, s))
    items.append(Paragraph("<b>Sleep — The Most Underrated Testosterone Booster:</b>", s["SSH"]))
    items.append(Paragraph("75% of daily testosterone release occurs during sleep, primarily during REM and slow-wave sleep cycles. Sleep deprivation is one of the most potent testosterone suppressors:", s["B"]))
    sleep=[["Sleep Duration","T Level Effect","Cortisol Effect","Practical Impact"],
           ["<5 hours","↓ T by 10–15%","↑ Cortisol +21%","Impaired muscle recovery; fat accumulation; mood disruption"],
           ["5–6 hours","↓ T by 5–10%","↑ Cortisol +10%","Suboptimal; common in busy schedules; chronic damage"],
           ["7–8 hours","Optimal T release","Normal cortisol","Sweet spot for most people"],
           ["9+ hours","Slight T benefit","Low cortisol","Beneficial during heavy training or recovery phases"]]
    items.append(tbl(sleep[0],[r for r in sleep[1:]],TK,[(W-72)*f for f in [0.18,0.20,0.20,0.42]]))

    items += sh("6–8. CORTISOL · SUPPLEMENTS · MICRONUTRIENTS", TK, s, "🌿")
    items.append(Paragraph("<b>Cortisol & Stress Management:</b>", s["SSH"]))
    for x in ["Cortisol is testosterone's primary antagonist — they share steroidogenic precursors (both come from pregnenolone)",
               "High chronic cortisol → pregnenolone preferentially shunted to cortisol → less substrate for testosterone",
               "Interventions: Meditation (reduces cortisol 14–31%), cold water therapy, yoga, nature exposure, social connection",
               "Avoid: overtraining, chronic sleep deprivation, extreme caloric restriction simultaneously with training"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Evidence-Based Supplement Stack:</b>", s["SSH"]))
    supp=[["Supplement","Dose","Evidence","Effect on Testosterone"],
          ["Ashwagandha (KSM-66)","600 mg/day (2 × 300 mg)","Very Strong — 6 RCTs","↑ T by 10–22% in studies; ↓ cortisol 25–30%; improves sperm quality"],
          ["Vitamin D3","3000–5000 IU/day","Strong — deficiency common; strongly linked to T","Correcting deficiency: ↑ T by 20–25% in deficient men"],
          ["Zinc (bisglycinate)","25–40 mg/day","Very Strong","Cofactor for T synthesis; ↑ T in deficient men significantly; preserves T during exercise"],
          ["Magnesium (glycinate)","300–500 mg nightly","Strong","Reduces SHBG; improves T:SHBG ratio; improves sleep quality (indirectly boosts T)"],
          ["Boron","10 mg/day","Moderate","↓ SHBG 9%; ↑ Free T 25%; ↑ DHT in clinical study"],
          ["Fenugreek Extract","500–600 mg/day","Moderate","Inhibits 5-alpha reductase and aromatase; maintains T; ↑ libido in trials"],
          ["Tongkat Ali (LJ100)","200 mg/day","Moderate","↑ T by 10–37% in aging men; reduces SHBG; improves energy"],
          ["D-Aspartic Acid (DAA)","3 g/day","Weak-Moderate (fading)","Stimulates LH → T in some studies; inconsistent results; may be better for already-deficient"]]
    items.append(tbl(supp[0],[r for r in supp[1:]],TK,[(W-72)*f for f in [0.22,0.14,0.14,0.50]]))

    items += sh("9–12. LIFESTYLE · BLOOD WORK · DAILY PROTOCOL", TK, s, "📋")
    items.append(Paragraph("<b>Daily Natural T Optimization Protocol:</b>", s["SSH"]))
    protocol=[["Time","Action","T-Boosting Effect"],
              ["Morning (7–8 AM)","10–20 min sunlight exposure (no sunscreen on skin)","Vitamin D synthesis; circadian cortisol calibration; mood-boosting"],
              ["Morning","Cold shower (2 min final cold blast)","Noradrenaline spike; testosterone-supportive; brown fat activation"],
              ["Training","Compound-heavy workout 45–70 min","Acute T spike; long-term receptor sensitivity improvement"],
              ["Post-Workout","Zinc + Vitamin D3 supplement","Replenish exercise-depleted zinc; synergize with T production"],
              ["Evening","Ashwagandha + Magnesium before bed","Cortisol reduction; sleep quality improvement; T synthesis overnight"],
              ["9–10 PM","Lights dim, screen-off or blue light glasses","Cortisol reduction; melatonin onset (precursor to T pathway)"],
              ["10–11 PM","Sleep (7–9 hours target)","Primary T synthesis window — 75% of daily T released during sleep"]]
    items.append(tbl(protocol[0],[r for r in protocol[1:]],TK,[(W-72)*f for f in [0.16,0.34,0.50]]))
    items.append(Paragraph("<b>Blood Work Targets for Optimal Natural Testosterone:</b>", s["SSH"]))
    bw=[["Biomarker","Low-Normal","Optimal","Action if Below Optimal"],
        ["Total Testosterone","300–400 ng/dL","700–1000 ng/dL","Full natural protocol; consider TRT evaluation below 400"],
        ["Free Testosterone","5–9 pg/mL","15–25 pg/mL","Reduce SHBG; optimize D3 and zinc; check thyroid"],
        ["SHBG","20–60 nmol/L","20–35 nmol/L","Reduce alcohol; optimize thyroid; adequate dietary fat"],
        ["LH","1–5 mIU/mL","3–7 mIU/mL","Low LH with low T = pituitary issue; consult endocrinologist"],
        ["Estradiol (E2)","10–20 pg/mL","20–35 pg/mL","High E2: reduce body fat; use DIM; limit alcohol"],
        ["Vitamin D","20–30 ng/mL","50–80 ng/mL","Supplement D3 3000–5000 IU/day + K2 100mcg"]]
    items.append(tbl(bw[0],[r for r in bw[1:]],TK,[(W-72)*f for f in [0.22,0.14,0.14,0.50]]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# PDF 15 — RECOVERY, SLEEP & CNS RESTORATION
# ════════════════════════════════════════════════════════════
def pdf_recovery(path):
    TK="recovery"; doc=new_doc(path); s=mk(TK); items=[]
    items += cover(["RECOVERY, SLEEP &","CNS RESTORATION","COMPLETE PROTOCOL"],
                   "Sleep Science · Active Recovery · Cold & Heat Therapy · Recovery Peptides · Deload Strategy",
                   "The most underrated performance multiplier — master recovery and double your gains",
                   TK, s, badges=["SLEEP SCIENCE","COLD THERAPY","RECOVERY PEPTIDES","DELOAD STRATEGY"])
    items += sh("TABLE OF CONTENTS", TK, s, "📋")
    for x in ["1.  Why Recovery Determines Your Results","2.  The Science of Muscle Repair",
               "3.  Sleep Architecture — Deep Sleep & Hormones","4.  Sleep Optimization Protocol",
               "5.  Sleep Supplement Stack — Evidence-Based","6.  Active Recovery Methods",
               "7.  Cold Therapy — Ice Baths & Cold Showers","8.  Heat Therapy — Sauna Protocols",
               "9.  CNS Fatigue vs Local Muscle Fatigue","10. Deload Strategy — When & How",
               "11. Recovery Peptides — BPC-157, TB-500, DSIP","12. HRV Monitoring & Training Readiness"]:
        items.append(Paragraph(x, s["TOC"]))
    items.append(PageBreak())

    items += sh("1. WHY RECOVERY DETERMINES YOUR RESULTS", TK, s, "🔬")
    items.append(Paragraph("Training creates the <b>stimulus</b> for adaptation — recovery creates the <b>adaptation</b>. Every physiological response you seek from training (muscle growth, strength increase, fat loss, improved conditioning) occurs <i>during recovery</i>, not during the workout itself.", s["BJ"]))
    items.append(rn("A 2019 systematic review in Sports Medicine demonstrated that athletes who prioritized sleep optimization (targeting 9 hours during training blocks) showed 20% greater strength gains and 40% lower injury rates compared to sleep-restricted athletes (6 hours) following identical training programs.", TK, s))
    recovery_comp=[["Recovery Component","Contribution to Total Adaptation","Most Critical For"],
                   ["Sleep (7–9+ hours)","~50–60%","GH release; protein synthesis; neural regeneration; testosterone production"],
                   ["Nutrition quality & timing","~20–25%","Muscle protein synthesis; glycogen resynthesis; anti-inflammatory"],
                   ["Active recovery & mobility","~10–15%","Clearance of metabolic waste; reduced DOMS; maintained movement quality"],
                   ["Stress management","~10–15%","Cortisol control; hormonal balance; immune function"],
                   ["Cold/Heat therapy","~5–10%","Inflammation management; blood flow; psychological recovery"]]
    items.append(tbl(recovery_comp[0],[r for r in recovery_comp[1:]],TK,[(W-72)*f for f in [0.25,0.24,0.51]]))

    items += sh("2–3. MUSCLE REPAIR & SLEEP ARCHITECTURE", TK, s, "💤")
    items.append(Paragraph("<b>The Muscle Repair Timeline:</b>", s["SSH"]))
    repair=[["Timeframe","Process","What This Means Practically"],
            ["0–2 hours post-training","Inflammatory phase: cytokines recruit satellite cells and macrophages to damaged fibers","Prioritize protein + carbs; begin active cooling or stretching"],
            ["2–24 hours","Satellite cell activation: muscle stem cells proliferate and fuse to repair micro-tears","Protein synthesis peaks; adequate amino acids (especially leucine) are critical"],
            ["24–48 hours","Protein synthesis peak: maximum anabolic state if nutrition and sleep are optimized","This is why training frequency ≤2× per muscle per week works for most"],
            ["48–72 hours","Remodeling: collagen cross-linking, myofibril reorganization, strength restoration","When soreness resolves; ready to train again; connective tissue still remodeling"]]
    items.append(tbl(repair[0],[r for r in repair[1:]],TK,[(W-72)*f for f in [0.18,0.37,0.45]]))
    items.append(Paragraph("<b>Sleep Architecture & Hormones:</b>", s["SSH"]))
    sleep_arch=[["Sleep Stage","Cycle Position","Duration","Hormones Released","Function"],
                ["N1 (Light Sleep)","Entry point","5–10 min","Minimal","Transition; temperature drops"],
                ["N2 (Light-Moderate)","After N1","20–25 min","Some melatonin","Heart rate slows; brain waves slow; most of night spent here"],
                ["N3 (Deep/Slow-Wave)","After N2 in early cycles","20–40 min","GH pulse (largest daily)","PRIMARY GROWTH AND REPAIR PHASE — most critical for athletes"],
                ["REM Sleep","Occurs more in later cycles","20–45 min","Testosterone (primary release)","Neural regeneration; memory consolidation; skill learning; T production"]]
    items.append(tbl(sleep_arch[0],[r for r in sleep_arch[1:]],TK,[(W-72)*f for f in [0.16,0.14,0.12,0.20,0.38]]))

    items += sh("4. SLEEP OPTIMIZATION PROTOCOL", TK, s, "🌙")
    items.append(Paragraph("Sleep optimization is not just about duration — <b>sleep quality and architecture</b> determine hormone output. An 8-hour night with poor deep sleep is less restorative than a 7-hour night with optimal deep sleep.", s["BJ"]))
    items.append(Paragraph("<b>Environmental Optimization:</b>", s["SSH"]))
    for x in ["<b>Temperature:</b> 65–68°F (18–20°C) — core body temperature must drop 1–2°C to initiate sleep. Cold room = faster sleep onset and more deep sleep",
               "<b>Complete darkness:</b> Even light through eyelids suppresses melatonin by 50%. Use blackout curtains or eye mask",
               "<b>Silence or white noise:</b> Sudden sounds disrupt sleep architecture without waking you. Use earplugs or white noise machine",
               "<b>No screens 60–90 min before bed:</b> Blue light (480nm wavelength) suppresses melatonin production by 3 hours if exposure is >30 min"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Behavioral Optimization:</b>", s["SSH"]))
    for x in ["Consistent sleep and wake times (±30 min on weekends) — anchors circadian rhythm",
               "No caffeine after 1–2 PM (6-hour half-life; affects sleep architecture even if you fall asleep)",
               "Alcohol disrupts REM sleep and suppresses GH release — even 1–2 drinks reduce sleep quality by 24%",
               "Exercise timing: Intense training <2 hours before bed elevates core temperature and cortisol — impairs sleep onset",
               "Cold shower or warm bath 60 min before bed accelerates core cooling → faster sleep onset"]:
        items.append(bl(x, s))

    items += sh("5. SLEEP SUPPLEMENT STACK", TK, s, "💊")
    sleep_supp=[["Supplement","Dose","Mechanism","Evidence"],
                ["Magnesium Glycinate","300–500 mg","GABA receptor modulation; muscle relaxation; lowers cortisol","Strong — significantly improves sleep onset and deep sleep duration"],
                ["Apigenin (Chamomile extract)","50 mg","GABA-A receptor partial agonist — mild anxiolytic without tolerance","Moderate — non-habit-forming mild sleep aid"],
                ["L-Theanine","200–400 mg","Increases GABA and serotonin; reduces anxiety; enhances sleep quality without causing drowsiness","Strong — excellent for high-stress athletes; improves sleep quality without morning grogginess"],
                ["Ashwagandha (KSM-66)","300–600 mg nightly","Reduces cortisol 20–30%; improves sleep quality by modulating HPA axis","Strong — doubles deep sleep duration in one RCT"],
                ["Melatonin","0.5–3 mg","Sleep onset signal — circadian rhythm regulator. Effective for shift workers and time zone adjustment","Strong for sleep onset; NOT a sleep maintenance supplement; use lowest effective dose"],
                ["DSIP (Peptide)","100–200 mcg SC","Delta sleep-inducing peptide — promotes deep slow-wave sleep directly","Moderate — significantly increases deep sleep; subcutaneous injection required"],
                ["Glycine","3 g","Lowers core body temperature via vasodilation; improves deep sleep quality","Moderate — 1.5°C core temp reduction; improves next-day performance"]]
    items.append(tbl(sleep_supp[0],[r for r in sleep_supp[1:]],TK,[(W-72)*f for f in [0.20,0.12,0.40,0.28]]))

    items += sh("6–8. ACTIVE RECOVERY · COLD THERAPY · SAUNA", TK, s, "❄")
    items.append(Paragraph("<b>Active Recovery Methods:</b>", s["SSH"]))
    active=[["Method","Intensity","Duration","Best Timing","Benefit"],
            ["Light walking","Very light (40–50% HR)","20–40 min","Same day or next day after training","Increases blood flow; removes lactate; reduces DOMS by 40%"],
            ["Yoga / Stretching","Passive","20–30 min","Evening; rest days","Reduces muscle tension; improves mobility; parasympathetic activation"],
            ["Foam rolling (SMR)","Moderate pressure","10–15 min","Pre-workout + post-workout","Reduces perceived soreness; improves range of motion"],
            ["Swimming (gentle)","Light","20–30 min","Day after heavy lifting","Full-body blood flow; hydrostatic pressure reduces swelling; zero joint loading"],
            ["Massage","Passive","30–60 min","24–48 hrs post-training","Reduces inflammation markers; improves sleep quality night-of"]]
    items.append(tbl(active[0],[r for r in active[1:]],TK,[(W-72)*f for f in [0.18,0.12,0.11,0.20,0.39]]))
    items.append(Paragraph("<b>Cold Water Immersion (Ice Bath) Protocol:</b>", s["SSH"]))
    cold=[["Protocol","Temperature","Duration","Recovery Benefit","Caution"],
          ["Post-training ice bath","10–15°C (50–59°F)","10–15 min","Reduces acute inflammation; numbs soreness; vasoconstriction","May blunt hypertrophy adaptations — avoid immediately post-strength training"],
          ["Cold shower (daily)","Cold blast final 2 min","2 min cold blast","Noradrenaline spike; dopamine +250%; mental toughness; anti-inflammatory","Generally safe; excellent mental benefits even without physical immersion"],
          ["Contrast therapy","Hot 3 min / Cold 1 min × 3–4 cycles","~15–20 min total","Vascular pump — alternating vasodilation/constriction removes waste","Best for team sport athletes; post-game recovery"]]
    items.append(tbl(cold[0],[r for r in cold[1:]],TK,[(W-72)*f for f in [0.20,0.14,0.12,0.32,0.22]]))
    items.append(Paragraph("<b>Sauna Protocol — Heat Therapy:</b>", s["SSH"]))
    for x in ["<b>Traditional Sauna (80–100°C):</b> 15–20 min sessions, 2–4×/week. 2+ hours after training — significant GH release (up to 16× baseline in one study at 2× 15 min sessions with 30 min cool-down between)",
               "<b>Benefits:</b> Increases heat shock proteins (HSP — prevent muscle protein degradation); improves cardiovascular adaptations; reduces all-cause mortality by 40% with 4×/week sauna use (Kuopio cohort study)",
               "<b>Infrared sauna (45–55°C):</b> Can be used closer to bedtime; deeper tissue penetration; detoxification benefits",
               "<b>Hydration:</b> Drink 500mL per 15 min in sauna. Add electrolytes post-sauna"]:
        items.append(bl(x, s))

    items += sh("9–12. CNS FATIGUE · DELOADS · PEPTIDES · HRV", TK, s, "📊")
    items.append(Paragraph("<b>CNS Fatigue vs Local Muscle Fatigue:</b>", s["SSH"]))
    cns=[["Type","Cause","Signs","Recovery Time","Strategy"],
         ["Local Muscle Fatigue","Metabolite accumulation, micro-tears, glycogen depletion","Soreness in specific muscle; reduced strength only in trained muscles","24–72 hours","Protein, sleep, light movement"],
         ["CNS Fatigue","High neural demand from heavy compound lifts, high frequency","Whole-body lethargy; reduced motivation; poor coordination; ALL lifts feel heavy","3–7 days","Deload; sleep; reduce volume"]]
    items.append(tbl(cns[0],[r for r in cns[1:]],TK,[(W-72)*f for f in [0.18,0.22,0.22,0.14,0.24]]))
    items.append(Paragraph("<b>Deload Protocol — When & How:</b>", s["SSH"]))
    for x in ["<b>Scheduled deload:</b> Every 4–6 weeks of hard training; reduce all sets by 50%; maintain exercise selection and load",
               "<b>Reactive deload:</b> When performance drops 3+ consecutive sessions, sleep quality deteriorates, motivation is very low",
               "<b>Deload week approach:</b> 3 full-body sessions; 2–3 sets per exercise; same weight; no intensity techniques; prioritize sleep + nutrition",
               "<b>What NOT to do on deload:</b> Zero training (detraining begins after 7+ days); extreme diet changes; added cardio (defeats purpose)"]:
        items.append(bl(x, s))
    items.append(Paragraph("<b>Heart Rate Variability (HRV) — Training Readiness Monitor:</b>", s["SSH"]))
    items.append(Paragraph("HRV measures the variation between heartbeats — higher variation indicates a well-recovered, parasympathetically dominant state (recovered and ready). Lower HRV indicates sympathetic dominance (stressed, fatigued, or sick). Track HRV every morning using apps (Elite HRV, HRV4Training, Whoop).", s["BJ"]))
    hrv=[["HRV Status","Training Recommendation","Nutrition Focus","Lifestyle"],
         ["Green (above baseline)","Full planned training; progressive overload; can add volume","Normal calories; carb timing around training","All good — maintain routine"],
         ["Yellow (near baseline)","Moderate training; avoid PR attempts; technical focus","Prioritize protein; adequate carbs","Investigate sleep quality; check stressors"],
         ["Red (below baseline)","Active recovery only; no intense training","Increase calories slightly; recovery nutrition","Rest; sleep early; address stress; assess illness"]]
    items.append(tbl(hrv[0],[r for r in hrv[1:]],TK,[(W-72)*f for f in [0.20,0.28,0.22,0.30]]))
    items.append(Spacer(1,8))
    items.append(Paragraph("Most athletes train too much and recover too little. The athlete who masters recovery outperforms the athlete who simply trains harder.", s["DIS"]))
    doc.build(items, onFirstPage=make_bg(TK,True), onLaterPages=make_bg(TK,False))
    print(f"  ✓  {path}")


# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    OUT = "/home/user/royal-fitness-club/generated_pdfs"
    os.makedirs(OUT, exist_ok=True)
    print("Generating 15 Elite Fitness Guide Series PDFs...\n")

    pdf_cutting(   f"{OUT}/01_Advanced_Cutting_Cycle_12Weeks.pdf")
    pdf_bulking(   f"{OUT}/02_Advanced_Bulking_Cycle_with_Peptides.pdf")
    pdf_beginner(  f"{OUT}/03_Beginner_Steroid_Cycle_Full_Guide.pdf")
    pdf_keto(      f"{OUT}/04_30Day_Keto_Indian_Vegetarian_Plan.pdf")
    pdf_female(    f"{OUT}/05_Female_Vegetarian_Weight_Loss_Plan.pdf")
    pdf_peptides(  f"{OUT}/06_Complete_Peptide_Protocol_Bible.pdf")
    pdf_sarms(     f"{OUT}/07_SARMs_Complete_Scientific_Handbook.pdf")
    pdf_trt(       f"{OUT}/08_TRT_Hormone_Optimization_Guide.pdf")
    pdf_hypertrophy(f"{OUT}/09_Science_of_Muscle_Hypertrophy.pdf")
    pdf_fatloss(   f"{OUT}/10_Ultimate_Fat_Loss_Masterclass.pdf")
    pdf_women_fit( f"{OUT}/11_Womens_Complete_Body_Transformation.pdf")
    pdf_indian(    f"{OUT}/12_Indian_Bodybuilder_Nutrition_Bible.pdf")
    pdf_preworkout(f"{OUT}/13_PreWorkout_Optimization_Guide.pdf")
    pdf_natural_t( f"{OUT}/14_Natural_Testosterone_Optimization.pdf")
    pdf_recovery(  f"{OUT}/15_Recovery_Sleep_CNS_Restoration.pdf")

    print("\n✅  All 15 PDFs generated successfully!")
    total = 0
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".pdf"):
            sz = os.path.getsize(f"{OUT}/{f}") // 1024
            total += sz
            print(f"  {f}  ({sz} KB)")
    print(f"\n  Total size: {total} KB")
