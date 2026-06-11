#!/usr/bin/env python3
"""Royal Fitness Club — Anabolic Cycle Series  (5 Premium PDFs)"""

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
SERIES = "ROYAL FITNESS CLUB — ANABOLIC SERIES"
OUT    = os.path.join(os.path.dirname(__file__), "generated_pdfs")
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "beginner":  {"bg":"#060F07","accent":"#1B5E20","accent2":"#4CAF50","gold":"#FFCA28","text":"#F0F0F0","muted":"#777777","row_odd":"#0E1A0F","row_even":"#091209","hdr":"#1B5E20","ibg":"#0A1A0B","wbg":"#1A1400"},
    "inter":     {"bg":"#080818","accent":"#1A237E","accent2":"#5C6BC0","gold":"#FFD54F","text":"#F0F0F0","muted":"#777777","row_odd":"#0D0D20","row_even":"#080816","hdr":"#1A237E","ibg":"#080A1C","wbg":"#1A1200"},
    "advanced":  {"bg":"#0B0000","accent":"#B71C1C","accent2":"#EF5350","gold":"#FF8F00","text":"#F0F0F0","muted":"#777777","row_odd":"#1C0808","row_even":"#140404","hdr":"#B71C1C","ibg":"#1A0808","wbg":"#1F1200"},
    "pct":       {"bg":"#030C10","accent":"#00695C","accent2":"#26C6DA","gold":"#64FFDA","text":"#F0F0F0","muted":"#777777","row_odd":"#071218","row_even":"#040D12","hdr":"#00695C","ibg":"#071416","wbg":"#0A1400"},
    "nutrition": {"bg":"#0C0700","accent":"#E65100","accent2":"#FF9800","gold":"#FFD600","text":"#F0F0F0","muted":"#777777","row_odd":"#1A0E00","row_even":"#120900","hdr":"#E65100","ibg":"#180C00","wbg":"#1A1800"},
}

def hx(c):  return colors.HexColor(c)

def make_bg(tk, is_cover=False):
    t = THEMES[tk]
    def bg(canv, doc):
        canv.saveState()
        canv.setFillColor(hx(t["bg"])); canv.rect(0,0,W,H,fill=1,stroke=0)
        if is_cover:
            canv.setFillColor(hx(t["accent"])); canv.rect(0,H-20,W,20,fill=1,stroke=0)
            canv.rect(0,0,W,10,fill=1,stroke=0)
            canv.setFillColor(hx(t["accent2"])); canv.setFillAlpha(0.10)
            canv.rect(0,0,7,H,fill=1,stroke=0); canv.setFillAlpha(1)
            canv.setStrokeColor(hx(t["accent"])); canv.setStrokeAlpha(0.08); canv.setLineWidth(0.8)
            for i in range(0,300,28): canv.line(W-i,0,W,i)
            canv.setStrokeAlpha(1)
            canv.setFont("Helvetica-Bold",7); canv.setFillColor(colors.white)
            canv.drawCentredString(W/2,H-13,SERIES)
        else:
            canv.setFillColor(hx(t["accent"])); canv.rect(0,H-4,W,4,fill=1,stroke=0)
            canv.rect(0,0,W,3,fill=1,stroke=0)
            canv.setStrokeColor(hx(t["accent2"])); canv.setStrokeAlpha(0.10); canv.setLineWidth(0.7)
            canv.line(32,24,32,H-24); canv.setStrokeAlpha(1)
        canv.setFont("Helvetica",7); canv.setFillColor(hx(t["muted"]))
        canv.drawString(36,10,f"{SERIES}  •  Professional Edition")
        canv.drawRightString(W-36,10,f"Page {doc.page}")
        canv.restoreState()
    return bg

def mk(tk):
    t = THEMES[tk]
    def ps(n,**kw): return ParagraphStyle(n,**kw)
    s={}
    s["T1"]  = ps("T1",  fontName="Helvetica-Bold",  fontSize=30,textColor=hx(t["text"]),   alignment=TA_CENTER,leading=36,spaceAfter=4)
    s["T2"]  = ps("T2",  fontName="Helvetica-Bold",  fontSize=22,textColor=hx(t["text"]),   alignment=TA_CENTER,leading=26,spaceAfter=4)
    s["sub"] = ps("sub", fontName="Helvetica",        fontSize=12,textColor=hx(t["accent2"]),alignment=TA_CENTER,leading=16,spaceAfter=3)
    s["tag"] = ps("tag", fontName="Helvetica-Oblique",fontSize=9, textColor=hx(t["muted"]), alignment=TA_CENTER)
    s["SH"]  = ps("SH",  fontName="Helvetica-Bold",  fontSize=12,textColor=hx(t["accent2"]),spaceBefore=12,spaceAfter=3,leading=15)
    s["SSH"] = ps("SSH", fontName="Helvetica-Bold",  fontSize=10,textColor=hx(t["gold"]),   spaceBefore=7, spaceAfter=2,leading=13)
    s["B"]   = ps("B",   fontName="Helvetica",        fontSize=8.8,textColor=hx(t["text"]), spaceBefore=2, spaceAfter=2,leading=13,leftIndent=12)
    s["BJ"]  = ps("BJ",  fontName="Helvetica",        fontSize=8.8,textColor=hx(t["text"]), spaceBefore=2, spaceAfter=2,leading=13,leftIndent=12,alignment=TA_JUSTIFY)
    s["BL"]  = ps("BL",  fontName="Helvetica",        fontSize=8.8,textColor=hx(t["text"]), spaceBefore=1, spaceAfter=1,leading=13,leftIndent=20,bulletIndent=8)
    s["SBL"] = ps("SBL", fontName="Helvetica",        fontSize=8.2,textColor=hx(t["muted"]),spaceBefore=1, spaceAfter=1,leading=12,leftIndent=34,bulletIndent=22)
    s["DIS"] = ps("DIS", fontName="Helvetica-Oblique",fontSize=7.5,textColor=hx(t["muted"]),alignment=TA_CENTER,spaceAfter=3,leading=11)
    s["TOC"] = ps("TOC", fontName="Helvetica",        fontSize=9.5,textColor=hx(t["text"]), spaceBefore=3, spaceAfter=3,leading=13,leftIndent=18)
    s["RN"]  = ps("RN",  fontName="Helvetica-Oblique",fontSize=8, textColor=hx(t["accent2"]),spaceBefore=1,spaceAfter=1,leading=11,leftIndent=10)
    s["CC"]  = ps("CC",  fontName="Helvetica-Bold",   fontSize=9, textColor=hx(t["accent2"]),alignment=TA_CENTER)
    s["CM"]  = ps("CM",  fontName="Helvetica",        fontSize=8, textColor=hx(t["muted"]), alignment=TA_CENTER)
    return s

# ── Helpers ──────────────────────────────────────────────────

def tbl(headers, rows, tk, cw=None, left_align_cols=None):
    t = THEMES[tk]
    hdr_ps  = ParagraphStyle('_th',fontName="Helvetica-Bold",fontSize=7.5,textColor=colors.white,alignment=TA_CENTER,leading=9)
    cell_ps = ParagraphStyle('_td',fontName="Helvetica",fontSize=7.5,textColor=hx(t["text"]),alignment=TA_CENTER,leading=10)
    lcell_ps= ParagraphStyle('_tl',fontName="Helvetica",fontSize=7.5,textColor=hx(t["text"]),alignment=TA_LEFT,leading=10)
    def to_p(text,i,is_hdr=False):
        ps = hdr_ps if is_hdr else (lcell_ps if (left_align_cols and i in left_align_cols) else cell_ps)
        return Paragraph(str(text).replace('\n','<br/>'),ps)
    data=[[to_p(h,i,True) for i,h in enumerate(headers)]]+\
         [[to_p(c,i) for i,c in enumerate(row)] for row in rows]
    tb=Table(data,colWidths=cw,repeatRows=1)
    tb.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),hx(t["hdr"])),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#2A2A2A")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[hx(t["row_odd"]),hx(t["row_even"])]),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ]))
    return tb

def sh(text,tk,s,icon=""):
    label=f"{icon}  {text}" if icon else text
    return [Paragraph(f"<b>{label}</b>",s["SH"]),
            HRFlowable(width="100%",thickness=1.5,color=hx(THEMES[tk]["accent"]),spaceAfter=4,spaceBefore=0)]

def bl(text,s,lv=0):
    return Paragraph(("–" if lv else "•")+"  "+text, s["SBL" if lv else "BL"])

def rn(text,tk,s):
    t=THEMES[tk]
    tb=Table([[Paragraph(f"🔬  <i>{text}</i>",s["RN"])]],colWidths=[W-72])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["ibg"])),
                             ("BOX",(0,0),(-1,-1),0.5,hx(t["accent2"])),
                             ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                             ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return tb

def wb(text,tk,s):
    t=THEMES[tk]
    tb=Table([[Paragraph(f"⚠️  <b>IMPORTANT:</b>  {text}",s["B"])]],colWidths=[W-72])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["wbg"])),
                             ("BOX",(0,0),(-1,-1),0.8,hx(t["gold"])),
                             ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                             ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return tb

def cover(title_lines,subtitle,tagline,tk,s,badges=None,disclaimer=None,edition="Research-Based  •  Professional Edition  •  2024"):
    t=THEMES[tk]; items=[]; items.append(Spacer(1,44*mm))
    if badges:
        bw=(W-80)/len(badges)
        bt=Table([[b for b in badges]],colWidths=[bw]*len(badges))
        bt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hx(t["accent"])),
                                 ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
                                 ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
                                 ("FONTSIZE",(0,0),(-1,-1),6.5),
                                 ("ALIGN",(0,0),(-1,-1),"CENTER"),
                                 ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                 ("TOPPADDING",(0,0),(-1,-1),5),
                                 ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        items+=[bt,Spacer(1,6*mm)]
    for line in title_lines:
        st=s["T1"] if len(line)<26 else s["T2"]
        items.append(Paragraph(line,st))
    items+=[Spacer(1,3*mm),
            HRFlowable(width="55%",thickness=2.5,color=hx(t["accent"]),spaceAfter=5,spaceBefore=3),
            Paragraph(subtitle,s["sub"]),Spacer(1,2*mm),Paragraph(tagline,s["tag"]),Spacer(1,8*mm)]
    ed=Table([[Paragraph(f"<b>{SERIES}</b>",s["CC"]),Paragraph(edition,s["CM"])]],colWidths=[(W-80)*0.56,(W-80)*0.44])
    ed.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#141414")),
                             ("BOX",(0,0),(-1,-1),1,hx(t["accent"])),
                             ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
                             ("LINEAFTER",(0,0),(0,-1),0.5,hx(t["muted"]))]))
    items+=[ed,Spacer(1,65*mm)]
    if disclaimer:
        items.append(Paragraph(disclaimer,s["DIS"]))
    items.append(PageBreak())
    return items

def toc_entry(num,title,s):
    return Paragraph(f"<b>{num:02d}.</b>  {title}",s["TOC"])

def new_doc(path):
    return SimpleDocTemplate(path,pagesize=A4,leftMargin=36,rightMargin=36,topMargin=26,bottomMargin=26)

# ════════════════════════════════════════════════════════════
# PDF 16 — BEGINNER ANABOLIC CYCLE COMPLETE GUIDE
# ════════════════════════════════════════════════════════════
def pdf_beginner():
    TK="beginner"; s=mk(TK)
    path=os.path.join(OUT,"16_Beginner_Anabolic_Cycle_Complete_Guide.pdf")
    doc=new_doc(path)
    DISC="DISCLAIMER: This document is for educational purposes only. Anabolic steroids are controlled substances in many countries. Always consult a licensed physician before starting any hormonal protocol. The authors do not condone illegal use."
    story=[]

    # COVER
    story+=cover(["BEGINNER","ANABOLIC CYCLE","COMPLETE GUIDE"],
                 "Your Safe, Science-Based Entry Into Hormonal Enhancement",
                 "Test-Only Foundation • Injection Protocol • PCT • Blood Work",
                 TK,s,badges=["BEGINNER LEVEL","TEST-E ONLY","10–12 WEEKS","COMPLETE PCT"],
                 disclaimer=DISC,
                 edition="Anabolic Series Vol. 1  •  Beginner Edition  •  2024",
                 )

    # ── PAGE 2: TABLE OF CONTENTS + WHO IS THIS FOR ──
    story+=sh("TABLE OF CONTENTS",TK,s,"📋")
    for num,title in [
        (1,"Introduction & Disclaimer"),(2,"Understanding Testosterone Esters"),
        (3,"First Cycle Protocol — Test-E 10 Weeks"),(4,"Week-by-Week Schedule"),
        (5,"Injection Sites & Technique"),(6,"On-Cycle Support & Estrogen Control"),
        (7,"Side Effects & How to Manage Them"),(8,"Post Cycle Therapy (PCT) Full Protocol"),
        (9,"Blood Work — What to Test & When"),(10,"Nutrition & Training on Cycle"),
    ]:
        story.append(toc_entry(num,title,s))
    story.append(Spacer(1,6*mm))

    story+=sh("1. Introduction & Who Is This Guide For",TK,s,"🎯")
    story.append(Paragraph("This guide is designed for healthy adult males (25+) who have at minimum 3–5 years of serious natural training experience and have maximised their natural genetic potential. A beginner cycle does NOT mean you are new to the gym — it means you are new to anabolic substances.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Criteria","Minimum Requirement"],
        [["Training Age","3–5 years of consistent, structured training"],
         ["Body Fat","Below 15% (ideally 10–12%) before starting"],
         ["Age","Minimum 23–25 years (HPTA fully matured)"],
         ["Natural Max","Close to or at natural genetic potential"],
         ["Knowledge","Understand nutrition, training, and recovery fully"],
         ["Blood Work","Pre-cycle bloods completed and reviewed by physician"],
         ["PCT Meds","Nolvadex/Clomid on hand BEFORE starting"]],
        TK,cw=[90*mm,110*mm],left_align_cols=[0,1]
    ))
    story.append(Spacer(1,4*mm))
    story.append(wb("Never start a cycle without having your PCT medications already purchased and in hand. Never skip blood work.",TK,s))
    story.append(PageBreak())

    # ── PAGE 3: TESTOSTERONE ESTERS ──
    story+=sh("2. Understanding Testosterone Esters",TK,s,"⚗️")
    story.append(Paragraph("Testosterone is available in several ester forms that determine its half-life — how long it stays active in the bloodstream. For beginners, long-estered forms are preferred as they require less frequent injections and produce stable blood levels.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Ester","Half-Life","Injection Freq.","Active Duration","Beginner Use"],
        [["Testosterone Enanthate","4.5 days","2x/week","~14 days","✅ Ideal"],
         ["Testosterone Cypionate","5 days","2x/week","~16 days","✅ Ideal"],
         ["Testosterone Propionate","0.8 days","EOD","~3 days","❌ Too frequent"],
         ["Sustanon 250","Multi-ester","2x/week","~21 days","⚠️ Less stable levels"],
         ["Testosterone Undecanoate","16.5 days","1x/week","~34 days","⚠️ Overdose risk if misdosed"]],
        TK,cw=[45*mm,30*mm,30*mm,35*mm,30*mm]
    ))
    story.append(Spacer(1,4*mm))

    story+=sh("Testosterone Dose-Response Guide",TK,s,"📊")
    story.append(tbl(
        ["Weekly Dose","Expected Effect","Aromatisation Risk","Recommended For"],
        [["200 mg/week","TRT-level, mild lean gains","Low","HRT patients"],
         ["250–300 mg/week","Beginner sweet spot, solid gains","Moderate","First cycle (recommended)"],
         ["400 mg/week","Noticeable muscle growth","Moderate–High","First cycle (aggressive)"],
         ["500 mg/week","Strong anabolic effect","High","2nd cycle onwards"],
         ["600+ mg/week","Diminishing returns, high E2 risk","Very High","Intermediate only"]],
        TK,cw=[35*mm,60*mm,40*mm,45*mm],left_align_cols=[1,3]
    ))
    story.append(Spacer(1,3*mm))
    story.append(rn("Testosterone aromatises (converts) to oestradiol (E2) via the aromatase enzyme. High E2 causes water retention, gynecomastia, and mood issues. Always have an aromatase inhibitor (AI) on hand.",TK,s))
    story.append(PageBreak())

    # ── PAGE 4: CYCLE PROTOCOL ──
    story+=sh("3. First Cycle Protocol — Testosterone Enanthate 10 Weeks",TK,s,"💉")
    story.append(Paragraph("The classic beginner protocol: Test-E only, 300–400 mg/week, 10–12 weeks. This single-compound approach allows you to understand exactly how your body responds to exogenous testosterone before adding complexity.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Compound","Dose","Frequency","Weeks","Purpose"],
        [["Testosterone Enanthate","150–200 mg","2x per week (Mon/Thu)","1–10","Primary anabolic agent"],
         ["Anastrozole (AI)","0.5 mg","Every other day (as needed)","1–10","Oestrogen control"],
         ["Aromasin (alternative AI)","12.5 mg","Every other day (as needed)","1–10","Oestrogen control (preferred)"],
         ["Nolvadex (SERM — PCT)","40/40/20/20 mg","Daily","Weeks 12–15","PCT — restart HPTA"],
         ["Clomid (optional PCT)","50/50/25/25 mg","Daily","Weeks 12–15","Additional HPTA support"]],
        TK,cw=[45*mm,30*mm,45*mm,22*mm,38*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,4*mm))

    story+=sh("4. Week-by-Week Full Schedule",TK,s,"📅")
    story.append(tbl(
        ["Week","Test-E Dose","AI Protocol","Blood Work","Notes"],
        [["1","150 mg ×2","Hold — monitor","—","Start low, assess sides"],
         ["2","150 mg ×2","Hold — monitor","—","Track mood, libido, acne"],
         ["3","200 mg ×2","0.5mg Anastrozole if needed","—","Compound begins fully saturating"],
         ["4","200 mg ×2","Continue if E2 sides present","Optional mid-cycle","Strength gains begin"],
         ["5","200 mg ×2","Consistent AI dose","—","Peak anabolic environment"],
         ["6","200 mg ×2","Consistent AI dose","—","Water retention peaks and stabilises"],
         ["7","200 mg ×2","Consistent AI dose","—","Steady state — solid gains"],
         ["8","200 mg ×2","Consistent AI dose","—","Assess body composition"],
         ["9","200 mg ×2","Taper AI slightly","—","Prepare for cycle end"],
         ["10","200 mg ×2","Last AI dose with last injection","—","Final week — last pin"],
         ["11","—","No AI","End-of-cycle bloods","Clearance period — 2 weeks"],
         ["12","—","No AI","—","PCT Week 1 begins: Nolva 40mg"],
         ["13","—","—","—","PCT Week 2: Nolva 40mg"],
         ["14","—","—","—","PCT Week 3: Nolva 20mg"],
         ["15","—","—","Post-PCT bloods","PCT Week 4: Nolva 20mg — DONE"]],
        TK,cw=[18*mm,28*mm,45*mm,40*mm,49*mm],left_align_cols=[4]
    ))
    story.append(PageBreak())

    # ── PAGE 5: INJECTION TECHNIQUE ──
    story+=sh("5. Injection Protocol — Sites, Technique & Sterility",TK,s,"💉")
    story.append(Paragraph("Proper injection technique is non-negotiable for safety. Infections from improper technique can require hospitalisation. Follow every step meticulously.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Injection Site","Needle Size","Volume Limit","Difficulty","Notes"],
        [["Glute (ventrogluteal)","23G 1.5 inch","3 mL","Easy","Most beginner-friendly, fewest nerves/vessels"],
         ["Glute (dorsogluteal)","23G 1.5 inch","3 mL","Medium","Upper outer quadrant only — nerve risk"],
         ["Vastus lateralis (outer thigh)","23G 1 inch","2 mL","Easy","Good self-injection site"],
         ["Deltoid (shoulder)","25G 1 inch","1 mL","Medium","Small volume only"],
         ["Pectoral","25G 1 inch","1 mL","Difficult","Not recommended for beginners"]],
        TK,cw=[45*mm,28*mm,22*mm,22*mm,53*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Step","Action","Why"],
        [["1","Wash hands thoroughly with soap for 30 seconds","Prevent contamination"],
         ["2","Wipe vial top with fresh alcohol swab","Sterility"],
         ["3","Draw air equal to dose, inject into vial","Prevents vacuum"],
         ["4","Draw out oil + 10–20% extra, remove bubbles","Accurate dosing"],
         ["5","Swap to new injection needle","Blunt drawing needle causes tissue damage"],
         ["6","Wipe injection site with alcohol swab — let dry","Wet alcohol can cause stinging/infection"],
         ["7","Insert needle at 90°, pull back plunger slightly","Confirm not in vein (no blood = safe)"],
         ["8","Inject slowly over 20–30 seconds","Reduces post-injection pain (PIP)"],
         ["9","Remove needle, apply gentle pressure, discard safely","Sterile disposal"]],
        TK,cw=[12*mm,80*mm,68*mm],left_align_cols=[1,2]
    ))
    story.append(Spacer(1,3*mm))
    story.append(wb("NEVER re-use needles. Never inject if you see any cloudiness or particles in the oil. Post-injection pain (PIP) for 1–3 days is normal. Swelling, redness, and fever are signs of infection — seek medical attention immediately.",TK,s))
    story.append(PageBreak())

    # ── PAGE 6: SIDE EFFECTS ──
    story+=sh("6. Side Effects — Identification & Management",TK,s,"⚕️")
    story.append(tbl(
        ["Side Effect","Cause","Symptoms","Prevention / Treatment"],
        [["Gynecomastia","High oestradiol (E2)","Puffy/tender nipples, lump under nipple","AI (Anastrozole/Aromasin). SERM (Nolva) if lump appears"],
         ["Water Retention","High E2, sodium retention","Bloating, puffy face/fingers, high BP","AI management, reduce sodium, increase water"],
         ["Acne","DHT + sebaceous gland activity","Back acne, face acne","Benzoyl peroxide wash, topical retinoids, zinc"],
         ["Hair Loss","DHT sensitivity (genetic)","Temple recession, thinning","Nizoral shampoo, topical minoxidil — if prone"],
         ["Testicular Atrophy","LH/FSH suppression","Reduced testis size","Normal on cycle — reverses with proper PCT"],
         ["High Blood Pressure","Water retention, increased RBC","Headaches, epistaxis","Manage E2, monitor BP weekly, reduce dose"],
         ["Increased RBC/Haematocrit","Testosterone stimulates erythropoiesis","Thick blood, elevated haematocrit","Blood donation, hydration, monitor bloods"],
         ["Mood Swings","E2 fluctuation, hormonal shifts","Irritability, anxiety, aggression","Stable AI dosing, consistent injection schedule"],
         ["Libido Changes","E2 too high or too low","Low libido, ED","Dial in E2 level — sweet spot ~20–30 pg/mL"]],
        TK,cw=[38*mm,32*mm,42*mm,58*mm],left_align_cols=[0,2,3]
    ))
    story.append(PageBreak())

    # ── PAGE 7: BLOOD WORK ──
    story+=sh("7. Blood Work — The Complete Testing Guide",TK,s,"🩸")
    story.append(Paragraph("Blood work is the single most important safety measure for any anabolic cycle. It is non-negotiable. Always test before, during, and after.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Test","Pre-Cycle","Mid-Cycle (Wk 5–6)","End-Cycle (Wk 11)","Post-PCT (Wk 16)","Purpose / Reference Range"],
        [["Total Testosterone","✅","✅","✅","✅","Natural baseline + recovery check"],
         ["Free Testosterone","✅","—","—","✅","Bioavailable T"],
         ["Oestradiol (E2 sensitive)","✅","✅","✅","✅","Target: 20–30 pg/mL on cycle"],
         ["LH / FSH","✅","—","—","✅","Should recover to baseline post-PCT"],
         ["SHBG","✅","—","—","✅","Affects free testosterone"],
         ["Full Blood Count (FBC)","✅","✅","✅","✅","Check haematocrit <54%"],
         ["Lipid Panel (LDL/HDL)","✅","✅","—","✅","Steroids tank HDL"],
         ["Liver Function (AST/ALT)","✅","—","✅","✅","Injectable test — minimal liver stress"],
         ["Kidney Function (eGFR/Creatinine)","✅","—","✅","✅","Baseline function"],
         ["Blood Pressure","✅","Weekly","Weekly","✅","Target: below 130/85 mmHg"],
         ["Glucose / HbA1c","✅","—","—","✅","Insulin sensitivity marker"],
         ["PSA (if 35+)","✅","—","—","✅","Prostate health"]],
        TK,cw=[42*mm,20*mm,24*mm,22*mm,22*mm,40*mm],left_align_cols=[0,5]
    ))
    story.append(Spacer(1,4*mm))
    story+=sh("8. PCT — Full Post Cycle Therapy Protocol",TK,s,"🔄")
    story.append(Paragraph("PCT begins 2 weeks after the last injection of testosterone enanthate (to allow clearance). The goal is to restart natural testosterone production as quickly and completely as possible.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["PCT Week","Nolvadex","Clomid (optional)","Supplements","Goal"],
        [["Week 1 (Wk 12)","40 mg/day","50 mg/day","Zinc 30mg, Vitamin D3 5000IU","Initiate LH/FSH release"],
         ["Week 2 (Wk 13)","40 mg/day","50 mg/day","Continue supplements","Continued HPTA stimulation"],
         ["Week 3 (Wk 14)","20 mg/day","25 mg/day","Add Ashwagandha KSM-66","Taper — natural T rising"],
         ["Week 4 (Wk 15)","20 mg/day","25 mg/day","Continue all supplements","Final taper — assess recovery"],
         ["Week 5+ (optional)","10 mg/day EOD","—","Continue supplements","If recovery slow, extend"],
         ["Blood Work (Wk 16)","Stop all SERMs","—","Continue support supps","Confirm recovery — check LH/FSH/T"]],
        TK,cw=[30*mm,28*mm,30*mm,50*mm,42*mm],left_align_cols=[3,4]
    ))
    story.append(PageBreak())

    # ── PAGE 8: NUTRITION & TRAINING ──
    story+=sh("9. Nutrition on Cycle — Maximising Your Gains",TK,s,"🍗")
    story.append(Paragraph("Anabolic steroids significantly increase nitrogen retention and protein synthesis. Your nutrition must be dialled in to take full advantage of this anabolic environment.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Macro","Bulking (Test 300–400mg)","Cutting (Test 300mg)","Per kg of bodyweight","Notes"],
        [["Protein","220–260 g/day","240–280 g/day","2.2–3.0 g/kg","Higher requirement on cycle — repair demand elevated"],
         ["Carbohydrates","400–600 g/day","150–250 g/day","4–6 g/kg (bulk)","Primary fuel — drives strength and pumps"],
         ["Fats","80–120 g/day","60–80 g/day","0.8–1.2 g/kg","Hormone production, lipid health"],
         ["Total Calories","Surplus +400–600","Deficit -300–400","Body weight dependent","Track weekly weight — aim +0.25–0.5 kg/week"],
         ["Water","4–6 L/day","4–6 L/day","—","Testosterone increases blood viscosity — hydrate"],
         ["Sodium","Moderate","Moderate-Low","—","Excess sodium worsens water retention with high E2"]],
        TK,cw=[28*mm,38*mm,36*mm,36*mm,42*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Training Variable","Natural","On Cycle (Test 300–400mg)","Reason"],
        [["Weekly Volume","10–20 sets/muscle","16–28 sets/muscle","Enhanced recovery capacity"],
         ["Training Frequency","2–3x/muscle/week","3–4x/muscle/week","Faster muscle protein synthesis"],
         ["Intensity","85–90% 1RM max","90–95% 1RM","CNS drive + strength increase"],
         ["Recovery Time","48–72 hrs/muscle","24–36 hrs/muscle","Accelerated recovery"],
         ["Deload","Every 4–6 weeks","Every 6–8 weeks","Reduced recovery need"],
         ["Cardio","2–3x/week","3–4x/week","Offset cardiovascular impact of AAS"]],
        TK,cw=[40*mm,32*mm,42*mm,56*mm],left_align_cols=[0,3]
    ))

    doc.build(story,
              onFirstPage=make_bg(TK,True),
              onLaterPages=make_bg(TK,False))
    print(f"✅  {path}")

# ════════════════════════════════════════════════════════════
# PDF 17 — INTERMEDIATE ANABOLIC CYCLE BLUEPRINT
# ════════════════════════════════════════════════════════════
def pdf_intermediate():
    TK="inter"; s=mk(TK)
    path=os.path.join(OUT,"17_Intermediate_Anabolic_Cycle_Blueprint.pdf")
    doc=new_doc(path)
    DISC="DISCLAIMER: Educational purposes only. Anabolic steroids are controlled in many jurisdictions. Consult a licensed physician. The authors do not condone illegal use of any substance."
    story=[]

    story+=cover(["INTERMEDIATE","ANABOLIC CYCLE","BLUEPRINT"],
                 "Second & Third Cycle Strategies — Stacks, Synergy & Smart Protocols",
                 "Test + Deca  •  Test + Anavar  •  Test + Tren  •  Full Protocols",
                 TK,s,badges=["INTERMEDIATE LEVEL","MULTI-COMPOUND","12–16 WEEKS","ADVANCED PCT"],
                 disclaimer=DISC,edition="Anabolic Series Vol. 2  •  Intermediate Edition  •  2024")

    # PAGE 2: Prerequisites + Stack Options
    story+=sh("Prerequisites for Moving to Intermediate",TK,s,"✅")
    story.append(tbl(
        ["Requirement","Minimum Standard","Why It Matters"],
        [["Completed beginner cycles","At least 1–2 clean beginner test-only cycles","Know how your body responds to testosterone"],
         ["Recovery confirmed","Post-cycle blood work shows normal LH/FSH/T","HPTA must be healthy before next cycle"],
         ["Training age","4–6+ years structured training","Must be able to maximise compound stimuli"],
         ["Knowledge","Understand aromatisation, AI use, PCT fully","Intermediate compounds have more complex profiles"],
         ["Body composition","10–14% body fat pre-cycle","Lower fat = less aromatisation, better results"],
         ["Time off","Minimum time off = cycle length + PCT","'On as long as off' rule — allow HPTA recovery"]],
        TK,cw=[48*mm,60*mm,52*mm],left_align_cols=[0,1,2]
    ))
    story.append(Spacer(1,5*mm))

    story+=sh("Intermediate Stack Options Overview",TK,s,"🧪")
    story.append(tbl(
        ["Stack","Compounds","Goal","Cycle Length","Difficulty","Side Effect Profile"],
        [["Stack A","Test-E + Anavar","Lean bulk / Recomp","10–12 weeks","Low","Mild — low androgenic, no progestin"],
         ["Stack B","Test-E + Deca-Durabolin","Mass & strength","14–16 weeks","Medium","Water retention, Deca dick risk if Test/Deca ratio wrong"],
         ["Stack C","Test-E + Trenbolone Ace","Recomp / Cut","10–12 weeks","High","Night sweats, aggression, tren cough, prolactin issues"],
         ["Stack D","Test-E + Masteron Prop","Hardening / Cut","10–12 weeks","Low–Med","Androgenic — hair loss risk if prone"],
         ["Stack E","Test-E + Primobolan","Lean gains / preserve","12–14 weeks","Low","Very mild — expensive but clean"]],
        TK,cw=[22*mm,40*mm,30*mm,25*mm,22*mm,45*mm],left_align_cols=[1,5]
    ))
    story.append(PageBreak())

    # PAGE 3: Stack A — Test + Anavar
    story+=sh("Stack A — Testosterone Enanthate + Anavar (Lean Bulk / Recomp)",TK,s,"💪")
    story.append(tbl(
        ["Compound","Dose","Frequency","Weeks","Half-Life","Purpose"],
        [["Testosterone Enanthate","400–500 mg","2x/week (Mon/Thu)","1–12","4.5 days","Base anabolic hormone"],
         ["Anavar (Oxandrolone)","40–60 mg","Daily (split AM/PM)","5–12","9 hours","Lean muscle, strength, fat loss"],
         ["Anastrozole","0.5 mg","EOD (as needed for E2)","1–12","—","Oestrogen control"],
         ["TUDCA/UDCA","500 mg","Daily","5–12","—","Liver protection (oral compound)"],
         ["Nolvadex (PCT)","40/40/20/20 mg","Daily","Wks 14–17","—","HPTA restart"]],
        TK,cw=[45*mm,28*mm,32*mm,20*mm,20*mm,35*mm],left_align_cols=[0,5]
    ))
    story.append(Spacer(1,4*mm))

    story+=sh("Stack B — Testosterone Enanthate + Deca-Durabolin (Mass Builder)",TK,s,"🏋️")
    story.append(tbl(
        ["Compound","Dose","Frequency","Weeks","Critical Rule"],
        [["Testosterone Enanthate","500 mg","2x/week","1–16","Test MUST be higher than Deca dose"],
         ["Nandrolone Decanoate (Deca)","300–400 mg","1–2x/week","1–14","Never run Deca without Test as base"],
         ["Anastrozole","0.5 mg","EOD","1–16","Monitor E2 closely — Deca also aromatises mildly"],
         ["Cabergoline","0.25 mg","2x/week","1–16","Controls prolactin — prevents Deca dick"],
         ["Nolvadex (PCT)","40/40/20/20 mg","Daily","Wks 18–21","Wait 3 weeks after last Deca pin to start PCT"]],
        TK,cw=[45*mm,25*mm,28*mm,18*mm,54*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,3*mm))
    story.append(wb("Deca-Durabolin suppresses natural testosterone VERY strongly and has a long half-life (~6 days). If Test:Deca ratio falls below 1:1, 'Deca Dick' (complete erectile dysfunction) is a real risk. Always run Test at 1.5–2x the Deca dose.",TK,s))
    story.append(PageBreak())

    # PAGE 4: Stack C — Trenbolone
    story+=sh("Stack C — Testosterone + Trenbolone Acetate (Advanced Recomp)",TK,s,"🔥")
    story.append(Paragraph("Trenbolone is the most powerful anabolic steroid widely available. It is 5× more anabolic and 5× more androgenic than testosterone, does not aromatise, but raises prolactin and causes significant cardiovascular and CNS side effects. Not for first-time intermediates.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Compound","Dose","Frequency","Weeks","Notes"],
        [["Testosterone Enanthate","200–300 mg","2x/week","1–12","Cruise-level Test to maintain function"],
         ["Trenbolone Acetate","200–300 mg","EOD (every other day)","1–10","Short ester — EOD injections required"],
         ["Aromasin","12.5 mg","EOD","1–12","Preferred AI with Tren — Nolva can worsen prolactin"],
         ["Cabergoline","0.25–0.5 mg","2x/week","1–12","Critical — controls prolactin/progesterone issues"],
         ["Vitamin B6 (P5P)","200 mg","Daily","1–12","Additional prolactin support"],
         ["Nolvadex (PCT)","40/40/20/20 mg","Daily","Wks 14–17","Begin 3 days after last Tren Ace pin"]],
        TK,cw=[45*mm,28*mm,28*mm,18*mm,51*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,4*mm))
    story.append(tbl(
        ["Trenbolone Side Effect","Severity","Management Strategy"],
        [["Night sweats","Very common","Light bedding, temperature control — unavoidable"],
         ["Insomnia","Common","Magnesium glycinate 400mg, melatonin 0.5mg"],
         ["Tren cough","Common","Inject slowly, change injection sites — short-lived"],
         ["Aggression / mood changes","Common","Dose management — never exceed 400mg/wk as beginner"],
         ["Prolactin elevation","Moderate risk","Cabergoline — mandatory on all Tren cycles"],
         ["Cardiovascular strain","Significant","Cardio 3–4x/week, monitor BP and RBC"],
         ["Hair loss acceleration","High (if prone)","Nizoral shampoo — cannot fully prevent on Tren"],
         ["Reduction in aerobic capacity","Common","Tren notably reduces cardio endurance — accept it"]],
        TK,cw=[48*mm,28*mm,84*mm],left_align_cols=[0,2]
    ))
    story.append(PageBreak())

    # PAGE 5: 16-Week Calendar + Injection Schedule
    story+=sh("Full 16-Week Intermediate Cycle Calendar (Test + Deca Example)",TK,s,"📅")
    story.append(tbl(
        ["Week","Test-E","Deca","Anastrozole","Cabergoline","Blood Work / Notes"],
        [["1","250mg Mon+Thu","—","0.5mg EOD if sides","—","Saturation phase — Deca starts Wk 2"],
         ["2","250mg Mon+Thu","200mg Mon","0.5mg EOD","0.25mg Tue+Fri","Deca beginning saturation"],
         ["3","250mg Mon+Thu","200mg Mon","0.5mg EOD","0.25mg Tue+Fri","Monitor for water retention"],
         ["4","250mg Mon+Thu","200mg Mon","Adjust per E2","0.25mg Tue+Fri","Mid-month check-in"],
         ["5","250mg Mon+Thu","200mg Mon","Stable dose","0.25mg Tue+Fri","Strength increasing"],
         ["6","250mg Mon+Thu","200mg Mon","Stable dose","0.25mg Tue+Fri","Mid-cycle bloods — adjust if needed"],
         ["7-10","250mg Mon+Thu","200mg Mon","Continue","0.25mg Tue+Fri","Peak anabolic window"],
         ["11-12","250mg Mon+Thu","200mg Mon","Continue","0.25mg Tue+Fri","Assess body composition"],
         ["13-14","250mg Mon+Thu","200mg Mon","Taper","0.25mg Tue+Fri","Last Deca injection on Wk 14 Thu"],
         ["15-16","250mg Mon+Thu","STOP","Low dose AI","Continue Caber","Clearance window — last Test pin Wk 16"],
         ["17 (PCT Wk 1)","—","—","Stop AI","Stop Caber","End-of-cycle bloods. Start Nolva 40mg"],
         ["18–20 (PCT)","—","—","—","—","Nolva 40/20/20mg. Post-PCT bloods Wk 21"]],
        TK,cw=[20*mm,28*mm,22*mm,28*mm,28*mm,54*mm],left_align_cols=[5]
    ))
    story.append(PageBreak())

    # PAGE 6: Intermediate Nutrition + Supplementation
    story+=sh("Intermediate Cycle Nutrition Protocol",TK,s,"🍽️")
    story.append(tbl(
        ["Nutrition Factor","Bulking Stack (Test+Deca)","Recomp Stack (Test+Tren)","Lean Bulk (Test+Var)"],
        [["Daily Calories","TDEE + 500–700 kcal","TDEE ± 100 kcal","TDEE + 300–400 kcal"],
         ["Protein","2.5–3.0 g/kg bodyweight","3.0–3.5 g/kg bodyweight","2.5–3.0 g/kg bodyweight"],
         ["Carbohydrates","5–7 g/kg (clean sources)","2–4 g/kg (cycle timing)","4–5 g/kg"],
         ["Fats","0.8–1.0 g/kg","0.8–1.0 g/kg","0.8–1.0 g/kg"],
         ["Meal Frequency","4–6 meals/day","4–5 meals/day","4–5 meals/day"],
         ["Pre-workout meal","Carb + protein 60–90 min before","Moderate carb + protein","Moderate carb + protein"],
         ["Post-workout","40–50g protein + 80–100g carbs","50g protein + 60g carbs","40g protein + 70g carbs"],
         ["Sodium management","Moderate — manage water retention","Low — critical for recomp look","Moderate"]],
        TK,cw=[45*mm,47*mm,45*mm,43*mm],left_align_cols=[0]
    ))
    story.append(Spacer(1,4*mm))
    story.append(tbl(
        ["Supplement","Dose","Purpose","Priority"],
        [["Whey Protein (isolate)","2–3 scoops/day","Hit protein targets","Essential"],
         ["Creatine Monohydrate","5g/day","ATP resynthesis, strength","Essential"],
         ["TUDCA / UDCA","500 mg/day","Liver support (if using orals)","Essential with orals"],
         ["Omega-3 Fish Oil","4–6g EPA/DHA daily","Cardiovascular health, HDL support","Essential"],
         ["Vitamin D3 + K2","5000 IU D3 + 100 mcg K2","Hormone synthesis, calcium metabolism","Essential"],
         ["Zinc","30–50 mg/day","Testosterone support, immune","Essential"],
         ["Magnesium Glycinate","400 mg/night","Sleep, muscle function, insulin","Highly recommended"],
         ["CoQ10","200 mg/day","Cardiovascular support, mitochondrial","Recommended on Tren"],
         ["NAC (N-Acetyl Cysteine)","600 mg/day","Liver antioxidant support","Recommended"],
         ["Taurine","3–5 g/day","Prevents back pumps from Anavar","Needed with Anavar"],
         ["Vitamin C","1000 mg/day","Antioxidant, collagen (joint support)","Recommended"]],
        TK,cw=[50*mm,35*mm,60*mm,25*mm],left_align_cols=[0,2]
    ))

    doc.build(story,onFirstPage=make_bg(TK,True),onLaterPages=make_bg(TK,False))
    print(f"✅  {path}")

# ════════════════════════════════════════════════════════════
# PDF 18 — ADVANCED ANABOLIC CYCLE MASTERY
# ════════════════════════════════════════════════════════════
def pdf_advanced():
    TK="advanced"; s=mk(TK)
    path=os.path.join(OUT,"18_Advanced_Anabolic_Cycle_Mastery.pdf")
    doc=new_doc(path)
    DISC="DISCLAIMER: Educational purposes only. This guide discusses advanced pharmacological protocols for academic and harm-reduction purposes only. Consult a licensed physician before any hormonal intervention."
    story=[]

    story+=cover(["ADVANCED","ANABOLIC CYCLE","MASTERY"],
                 "Elite Multi-Compound Strategies, Competition Prep & GH Integration",
                 "Advanced Stacks  •  Competition Protocol  •  Peptide Integration  •  Health Monitoring",
                 TK,s,badges=["ADVANCED LEVEL","MULTI-COMPOUND","16–24 WEEKS","GH + PEPTIDES"],
                 disclaimer=DISC,edition="Anabolic Series Vol. 3  •  Advanced Edition  •  2024")

    # PAGE 2: Advanced Concepts
    story+=sh("Advanced Anabolic Concepts",TK,s,"🧠")
    story.append(tbl(
        ["Concept","Definition","Practical Application"],
        [["Androgen Receptor Upregulation","Increase in AR density with sustained exposure","Blast/cruise allows continuous receptor sensitivity"],
         ["Androgen Receptor Downregulation","Decreased sensitivity with continuous high-dose use","Why 16-week cycles outperform 24-week cycles per mg"],
         ["Synergistic Stacking","Compounds with complementary mechanisms amplify each other","Test + Tren + Mast = DHT-style hardening synergy"],
         ["Progestin Activity","Nandrolone/Tren raise progesterone — interacts with prolactin","Cabergoline management critical — can cause gyno without E2 elevation"],
         ["5α-Reduction","DHT conversion in skin/scalp/prostate","Finasteride blocks 5α-reductase — reduces hair/prostate risk (not with Tren)"],
         ["HPTA Suppression Depth","Higher doses + longer cycles = deeper suppression","Recovery harder after long blasts — TRT bridge sometimes necessary"],
         ["Blast & Cruise","Alternating high-dose cycles with TRT-level maintenance","Avoids repeated PCT — common in competitive bodybuilders"]],
        TK,cw=[45*mm,55*mm,60*mm],left_align_cols=[0,1,2]
    ))
    story.append(PageBreak())

    # PAGE 3: Elite Competition Stack
    story+=sh("Competition Prep Stack — 20-Week Protocol",TK,s,"🏆")
    story.append(Paragraph("This protocol mirrors a competitive bodybuilding prep cycle. It is high-risk, high-reward and requires extensive experience, monitoring, and medical supervision.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Phase","Duration","Compounds","Primary Goal"],
        [["Off-Season Base","Year-round (blast)","Test-E 600mg + Deca 400mg + HGH 2–4 IU","Maximise muscle mass accumulation"],
         ["Early Prep (Wks 1–8)","8 weeks","Test-E 400mg + Tren-E 300mg + Anavar 50mg + HGH 4IU","Begin fat loss while preserving mass"],
         ["Peak Prep (Wks 9–16)","8 weeks","Test-P 200mg + Tren-A 400mg + Mast-P 400mg + Anavar 80mg","Maximum hardness, vascular, fat mobilisation"],
         ["Peak Week (Wks 17–20)","4 weeks","Test-P 100mg + Tren-A 300mg + Mast-P 400mg + Winstrol 50mg","Final conditioning — water manipulation"],
         ["Post Show PCT","6–8 weeks","Nolvadex 40/40/20/20mg + Clomid 50/50/25/25mg","Full HPTA recovery"]],
        TK,cw=[38*mm,22*mm,65*mm,35*mm],left_align_cols=[0,2,3]
    ))
    story.append(Spacer(1,4*mm))
    story.append(tbl(
        ["Compound","Dose","Weeks","Mechanism","Side Effect Focus"],
        [["Testosterone Propionate","100–200 mg","1–20","Anabolic base — short ester for quick removal","Low — base hormone"],
         ["Trenbolone Enanthate","300 mg","1–8","Strong anabolic/androgenic, fat loss","Night sweats, prolactin, CV strain"],
         ["Trenbolone Acetate","300–400 mg","9–20","Switch to short ester for show-week control","Same as above + tren cough"],
         ["Masteron Propionate","300–400 mg","9–20","Anti-oestrogenic, hardening, DHT derivative","Hair loss if genetically prone"],
         ["Anavar","50–80 mg","1–16","Lean mass, strength, minimal water retention","Hepatotoxic — use TUDCA"],
         ["Winstrol","50 mg","17–20","Extreme hardening, SHBG reduction","Joint pain, hepatotoxic, HDL crash"],
         ["HGH (somatropin)","2–4 IU","Year-round","IGF-1 elevation, fat oxidation, recovery","Carpal tunnel, water retention, cost"],
         ["Insulin (Humalog)","4–8 IU post-training","Advanced only","Nutrient partitioning, glycogen","Hypoglycaemia risk — EXTREME caution"]],
        TK,cw=[42*mm,25*mm,18*mm,50*mm,45*mm],left_align_cols=[0,3,4]
    ))
    story.append(Spacer(1,3*mm))
    story.append(wb("Insulin use is extremely dangerous. A miscalculation can cause fatal hypoglycaemia within minutes. This is included for educational awareness ONLY. Never use insulin without direct medical supervision.",TK,s))
    story.append(PageBreak())

    # PAGE 4: Growth Hormone Integration
    story+=sh("Human Growth Hormone (HGH) — Complete Protocol",TK,s,"🧬")
    story.append(tbl(
        ["HGH Protocol","Dose","Timing","Goal","Notes"],
        [["Anti-ageing / Wellness","1–2 IU","AM fasted","Health optimisation, fat loss","Low dose — minimal side effects"],
         ["Bodybuilding (offseason)","2–4 IU","Pre-workout or post-training","Muscle gain + fat loss balance","Split into 2 doses if using 4 IU"],
         ["Aggressive bodybuilding","4–6 IU","2 IU AM + 2–4 IU pre-training","Maximum anabolic effect","High cost, side effect risk rises"],
         ["Competition prep","4–8 IU","AM + post-training","Fat loss + conditioning","Often paired with insulin — extreme risk"],
         ["Peptide alternative (GHRP-2)","100–200 mcg","3x daily, fasted","GH release stimulation","Legal, cheaper, less effective"],
         ["Peptide alternative (CJC-1295)","100 mcg","2x daily","Sustained GH pulse elevation","Stack with GHRP for synergy"]],
        TK,cw=[42*mm,20*mm,35*mm,45*mm,38*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["HGH Side Effect","Threshold","Management"],
        [["Water retention","All doses","Reduces after 4–6 weeks of use"],
         ["Carpal tunnel syndrome","2+ IU/day","Reduce dose, wrist splints, usually reverses on cessation"],
         ["Acromegaly (long-term)","Supraphysiological long-term use","Avoid excessive dose for extended periods"],
         ["Insulin resistance","4+ IU/day","Monitor glucose, use metformin if needed"],
         ["Hypothyroidism","Long-term use","T3/T4 monitoring — may need T3 supplementation"],
         ["Increased IGF-1","Dose-dependent","Acceptable elevation — excessively high IGF-1 has cancer associations"]],
        TK,cw=[50*mm,40*mm,80*mm],left_align_cols=[0,2]
    ))
    story.append(PageBreak())

    # PAGE 5: Advanced Blast & Cruise
    story+=sh("Blast & Cruise Protocol (B&C) — Advanced Continuous Approach",TK,s,"🔄")
    story.append(Paragraph("Blast & Cruise eliminates PCT between cycles. During the 'cruise' phase, the user drops to TRT-level testosterone (100–150mg/week), maintaining hormonal function while allowing partial recovery before the next blast.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Phase","Duration","Compound","Dose","Goal","Health Monitoring"],
        [["BLAST 1","16 weeks","Test-E + Deca + Anavar","500+400+50mg","Mass gain","Bloods at wk 6 + wk 16"],
         ["CRUISE 1","8–12 weeks","Test-E only","100–150 mg/week","Recovery + maintenance","Bloods at wk 4 into cruise"],
         ["BLAST 2","14 weeks","Test-E + Tren-A + Mast-P","400+300+300mg","Recomp / lean mass","Bloods at wk 6"],
         ["CRUISE 2","8 weeks","Test-E only","100–150 mg/week","Recovery","Full hormone panel"],
         ["BLAST 3","12 weeks","Test-P + Tren-A + Mast + Var","200+400+400+60mg","Competition prep","Weekly BP, bloods at wk 6"]],
        TK,cw=[22*mm,22*mm,50*mm,32*mm,28*mm,46*mm],left_align_cols=[2,4,5]
    ))
    story.append(Spacer(1,4*mm))
    story.append(rn("Blast & Cruise is a permanent commitment to exogenous testosterone. Fertility is severely compromised. If you wish to father children, HCG (500 IU 2x/week) throughout all phases is essential to maintain testicular function.",TK,s))
    story.append(Spacer(1,4*mm))

    story+=sh("Advanced Health Monitoring Schedule",TK,s,"🩺")
    story.append(tbl(
        ["Test","Frequency","Critical Thresholds","Action if Exceeded"],
        [["Blood Pressure","Weekly","Systolic >140 / Diastolic >90","Reduce dose, add telmisartan, increase cardio"],
         ["Haematocrit","Every 6 weeks","Above 54%","Blood donation, increase hydration, reduce AAS dose"],
         ["HDL Cholesterol","Every 6 weeks","Below 35 mg/dL","Reduce orals, increase omega-3, add cardio, check statin"],
         ["LDL Cholesterol","Every 6 weeks","Above 160 mg/dL","Diet intervention, reduce orals, consider rosuvastatin"],
         ["Liver Enzymes (AST/ALT)","Every 6 weeks","3× upper normal limit","Stop all orals immediately, use TUDCA, retest in 4 weeks"],
         ["Prolactin","Every 8 weeks on Tren/Deca","Above 30 ng/mL","Cabergoline 0.5mg 2x/week"],
         ["PSA","Every 3–6 months (35+)","Rapidly rising or >4.0 ng/mL","Urologist referral immediately"],
         ["Full Cardiac Echo","Annually","LV wall thickness >13mm","Cardiology referral — LVH risk with long-term AAS"]],
        TK,cw=[42*mm,30*mm,42*mm,56*mm],left_align_cols=[0,3]
    ))
    story.append(PageBreak())

    # PAGE 6: Advanced PCT / Recovery
    story+=sh("Advanced PCT — Recovery After Multi-Compound Cycles",TK,s,"💊")
    story.append(tbl(
        ["Cycle Type","Clearance Wait","PCT Protocol","Duration","Recovery Expectation"],
        [["Test-E only","2 weeks","Nolvadex 40/40/20/20mg","4 weeks","Full in 4–8 weeks"],
         ["Test + Deca","3 weeks (Deca long ester)","Nolva 40/40/20/20 + Clomid 50/50/25/25","6 weeks","8–12 weeks — Deca deeply suppressive"],
         ["Test + Tren-A","3 days (Tren Ace short ester)","Nolva 40/40/20/20 + Cabergoline during PCT","4–6 weeks","6–10 weeks — Tren very suppressive"],
         ["Test + Tren-E","3 weeks","Nolva 40/40/20/20 + Clomid + Caber","6 weeks","10–16 weeks"],
         ["B&C (returning to natural)","3+ weeks from last blast","Nolva 40/40/20/20 + Clomid 50/50/25/25 + HCG 1000 IU EOD × 3 weeks","8–10 weeks","12–24 weeks — may not fully recover"],
         ["Post-competition (full prep)","2–3 weeks","Nolva 40/40/20/20 + Clomid + HCG + DHEA","8+ weeks","16–24 weeks — expect low mood, low T initially"]],
        TK,cw=[38*mm,26*mm,60*mm,22*mm,34*mm],left_align_cols=[0,2,4]
    ))
    story.append(Spacer(1,4*mm))
    story.append(tbl(
        ["PCT Support Supplement","Dose","Role","Duration"],
        [["HCG (pre-PCT only)","1000 IU EOD × 10 days","Directly stimulates Leydig cells — jumpstarts testosterone production","Use BEFORE starting SERM"],
         ["Nolvadex (Tamoxifen)","40→20 mg/day tapering","Blocks oestrogen at pituitary — restores LH/FSH release","4–6 weeks"],
         ["Clomid (Clomiphene)","50→25 mg/day","Competitive E2 blocker — amplifies LH pulse","4–6 weeks"],
         ["Cabergoline","0.25 mg 2x/week","Lowers prolactin post-Deca/Tren — facilitates recovery","During PCT if levels elevated"],
         ["Enclomiphene (modern alternative)","12.5–25 mg/day","Selective isomer of Clomid — fewer side effects, strong LH stimulus","4 weeks"],
         ["Ashwagandha (KSM-66)","600 mg/day","Reduces cortisol, supports natural T recovery","Throughout PCT"],
         ["D-Aspartic Acid","3g/day","Short-term natural LH stimulation","4–8 weeks"],
         ["Zinc + Magnesium (ZMA)","Zinc 30mg + Mag 450mg","Testosterone cofactors — support enzymatic T synthesis","Indefinitely"]],
        TK,cw=[45*mm,28*mm,65*mm,32*mm],left_align_cols=[0,2,3]
    ))

    doc.build(story,onFirstPage=make_bg(TK,True),onLaterPages=make_bg(TK,False))
    print(f"✅  {path}")

# ════════════════════════════════════════════════════════════
# PDF 19 — PCT COMPLETE BIBLE
# ════════════════════════════════════════════════════════════
def pdf_pct():
    TK="pct"; s=mk(TK)
    path=os.path.join(OUT,"19_PCT_Post_Cycle_Therapy_Complete_Bible.pdf")
    doc=new_doc(path)
    DISC="DISCLAIMER: Educational purposes only. This guide discusses pharmacological protocols for harm-reduction. Consult a licensed endocrinologist before using any SERM, hormone, or related compound."
    story=[]

    story+=cover(["POST CYCLE THERAPY","COMPLETE BIBLE"],
                 "The Definitive Guide to HPTA Recovery, SERMs, HCG & Natural T Restoration",
                 "Nolvadex  •  Clomid  •  Enclomiphene  •  HCG  •  Natural Recovery",
                 TK,s,badges=["ALL CYCLE LEVELS","SERM PROTOCOLS","HCG GUIDE","BLOOD WORK"],
                 disclaimer=DISC,edition="Anabolic Series Vol. 4  •  PCT Edition  •  2024")

    story+=sh("Understanding the HPTA — How Testosterone is Regulated",TK,s,"🧠")
    story.append(Paragraph("The Hypothalamic-Pituitary-Testicular Axis (HPTA) is the hormonal feedback system that controls natural testosterone production. Anabolic steroids suppress this axis — PCT is the strategy to restart it.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["HPTA Component","Location","Function","What AAS Does to It"],
        [["Hypothalamus","Brain","Releases GnRH (Gonadotropin-releasing hormone) in pulses","Exogenous androgens suppress GnRH release via negative feedback"],
         ["Anterior Pituitary","Brain","Releases LH + FSH in response to GnRH","LH and FSH drop to near zero on cycle"],
         ["Leydig Cells","Testes","Produce testosterone in response to LH","Atrophy without LH stimulation — reduced testicular size"],
         ["Sertoli Cells","Testes","Produce sperm in response to FSH","Spermatogenesis suppressed — temporary infertility"],
         ["Inhibin B","Testes","Negative feedback on FSH","Levels drop on cycle — FSH suppression compounded"],
         ["Sex Hormone Binding Globulin (SHBG)","Liver","Binds testosterone — regulates free T","AAS lower SHBG — higher free T ratio on cycle, drops post-cycle"]],
        TK,cw=[40*mm,25*mm,55*mm,50*mm],left_align_cols=[0,2,3]
    ))
    story.append(Spacer(1,3*mm))
    story.append(rn("Recovery timeline is NOT linear. LH/FSH often recover within 4–6 weeks but total testosterone can take 3–6 months to fully normalise. Sperm count can take 6–18 months to recover. Pre-cycle fertility testing is strongly advised if having children is a consideration.",TK,s))
    story.append(PageBreak())

    # PAGE 3: SERM Comparison
    story+=sh("SERM Comparison — Nolvadex vs Clomid vs Enclomiphene",TK,s,"💊")
    story.append(tbl(
        ["SERM","Mechanism","Half-Life","LH Stimulation","FSH Stimulation","Side Effects","Dose"],
        [["Nolvadex\n(Tamoxifen)","Competitive E2 antagonist at pituitary and hypothalamus","5–7 days","Moderate","Moderate","Hot flushes, vision issues (rare), nausea","20–40 mg/day"],
         ["Clomid\n(Clomiphene)","Mixed E2 agonist/antagonist — acts primarily at hypothalamus","5–7 days","Strong","Strong","Vision disturbances, emotional blunting, depression","25–50 mg/day"],
         ["Enclomiphene","Pure E2 antagonist isomer of Clomid — no agonist activity","Short","Strong","Strong","Minimal — cleaner than Clomid","12.5–25 mg/day"],
         ["Toremifene","Similar to Nolvadex — also blocks E2 in breast tissue","5 days","Moderate","Moderate","Similar to Nolvadex","60 mg/day"],
         ["Raloxifene","Selective — strong bone/breast E2 blocker","28 hours","Moderate","Low","Hot flushes, rare DVT risk","60 mg/day"]],
        TK,cw=[25*mm,48*mm,22*mm,22*mm,22*mm,32*mm,25*mm],left_align_cols=[0,1,5]
    ))
    story.append(Spacer(1,4*mm))
    story+=sh("SERM Dosing Protocols by Cycle Severity",TK,s,"📋")
    story.append(tbl(
        ["Cycle Type","SERM Choice","Week 1–2","Week 3–4","Week 5–6","Week 7–8 (if needed)"],
        [["Light (Test only, short)","Nolvadex only","40 mg/day","20 mg/day","10 mg/day","—"],
         ["Standard (Test only, 10–12wk)","Nolvadex ± Clomid","Nolva 40 + Clomid 50","Nolva 40 + Clomid 50","Nolva 20 + Clomid 25","Nolva 20"],
         ["Heavy (Test + 2nd compound)","Nolvadex + Clomid","Nolva 40 + Clomid 50","Nolva 40 + Clomid 50","Nolva 20 + Clomid 25","Nolva 20 + Clomid 25"],
         ["Very heavy (Tren/Deca based)","Nolva + Clomid + HCG pre-PCT","HCG first 10 days, then SERMs","Nolva 40 + Clomid 50","Nolva 40 + Clomid 50","Nolva 20 + Clomid 25"],
         ["B&C to natural","Full protocol","HCG 1000IU EOD × 3 weeks","Nolva 40 + Clomid 50","Nolva 40 + Clomid 25","Nolva 20"]],
        TK,cw=[38*mm,38*mm,34*mm,34*mm,34*mm,32*mm],left_align_cols=[0,1]
    ))
    story.append(PageBreak())

    # PAGE 4: HCG Guide
    story+=sh("HCG (Human Chorionic Gonadotropin) — The Complete Guide",TK,s,"🔬")
    story.append(Paragraph("HCG mimics Luteinising Hormone (LH) and directly stimulates Leydig cells to produce testosterone. It prevents testicular atrophy during a cycle and can dramatically accelerate recovery if used correctly.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["HCG Protocol","Timing","Dose","Frequency","Purpose"],
        [["On-cycle maintenance","Throughout entire cycle","250–500 IU","2–3x per week","Prevents testicular atrophy — maintains intratesticular testosterone"],
         ["Pre-PCT blast (Harpenden protocol)","Final 3 weeks before PCT","1000 IU","EOD (every other day)","Restimulates Leydig cells before SERM therapy"],
         ["Pre-PCT high dose","Final 10 days before PCT","1500–2500 IU","EOD","Maximum Leydig cell stimulation — deep suppression cases"],
         ["During PCT (NOT recommended)","Concurrent with SERMs","—","—","HCG suppresses the HPTA at pituitary while SERMs stimulate it — counterproductive"],
         ["Fertility protocol","During or post cycle","500–1000 IU","3x/week","Maintains sperm production — essential if trying to conceive"]],
        TK,cw=[40*mm,33*mm,22*mm,28*mm,57*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,3*mm))
    story.append(wb("HCG raises intratesticular testosterone and oestradiol. Using it during PCT while also using SERMs creates contradictory signals. The gold standard is: HCG blast → wait 3 days → start SERMs.",TK,s))
    story.append(Spacer(1,4*mm))

    story+=sh("Natural Testosterone Recovery Timeline",TK,s,"📈")
    story.append(tbl(
        ["Recovery Phase","Timeframe","LH/FSH Status","Testosterone Level","What to Expect"],
        [["HPTA restart initiation","Weeks 1–4 PCT","LH/FSH rising from near-zero","10–25% of pre-cycle baseline","Fatigue, low mood, libido loss — this is normal"],
         ["Early recovery","Weeks 4–8","LH/FSH reaching 50–70% normal","25–60% of baseline","Energy returning, morning erections resuming"],
         ["Mid recovery","Weeks 8–16","LH/FSH near normal range","60–85% of baseline","Mood stabilising, gym performance partially back"],
         ["Full recovery","Weeks 12–24+","LH/FSH normal","85–100% of baseline","Depends on cycle length, compounds, and individual genetics"],
         ["Extended recovery (severe cases)","6–18 months","Slow but progressive","May take 12+ months","Long cycles, deep suppression, multiple years of blasting"]],
        TK,cw=[38*mm,22*mm,32*mm,32*mm,46*mm],left_align_cols=[0,4]
    ))
    story.append(PageBreak())

    # PAGE 5: Blood Work Guide for PCT
    story+=sh("Post-Cycle Blood Work — The Full Testing Protocol",TK,s,"🩸")
    story.append(tbl(
        ["Test","Pre-Cycle Baseline","End of Cycle","Post-PCT (4 wks after)","Recovery Target"],
        [["Total Testosterone","Record personal baseline","Will be suppressed","Should be rising","Back to or above personal baseline"],
         ["Free Testosterone","Record baseline","Suppressed","Rising","Within normal physiological range"],
         ["LH","Record baseline","Near zero","Rising — should be >2 IU/L","Back to baseline (2–12 IU/L)"],
         ["FSH","Record baseline","Near zero","Rising","Back to baseline (1–12 IU/L)"],
         ["Oestradiol (E2 sensitive)","Record baseline","Elevated on cycle","Normalising","Should mirror T recovery"],
         ["SHBG","Record baseline","Reduced on cycle","Rising","Back toward baseline"],
         ["Prolactin","If Deca/Tren used","Elevated","Should normalise","<15 ng/mL"],
         ["PSA","If 35+ — record baseline","May be elevated","Check if elevated persists","Return to baseline"],
         ["Full blood count","Record haematocrit","Elevated — RBC high","Normalising","Haematocrit <48–50%"],
         ["Lipid panel (HDL/LDL)","Record HDL baseline","HDL crashed","Recovering","HDL should recover within 3–6 months off cycle"],
         ["Sperm count (if fertility concern)","Record pre-cycle","Severely suppressed","Partial recovery","Full recovery: 3–18 months"]],
        TK,cw=[42*mm,30*mm,28*mm,32*mm,48*mm],left_align_cols=[0,4]
    ))
    story.append(Spacer(1,4*mm))
    story+=sh("Signs of Successful PCT Recovery",TK,s,"✅")
    story.append(tbl(
        ["Indicator","Good Sign","Concerning Sign","Action if Concerning"],
        [["Libido","Returns within 4–8 weeks","Still absent after 10+ weeks","Check LH/FSH/T + prolactin"],
         ["Morning erections","Resume within 4–6 weeks","Absent after 8+ weeks","Assess E2, T, prolactin"],
         ["Mood","Gradually stabilises","Persistent depression (12+ weeks)","Rule out low T — possible TRT consult"],
         ["Energy levels","Return to near normal within 6 weeks","Chronically fatigued","Check thyroid, cortisol, iron levels too"],
         ["Gym performance","80–90% of cycle peak within 6–8 weeks","Still significantly weaker","Normal if longer cycle — patience required"],
         ["Blood work","LH/FSH rising, T rising","Flat LH/FSH after 8 weeks PCT","Consider extended SERM protocol or TRT evaluation"]],
        TK,cw=[32*mm,48*mm,45*mm,45*mm],left_align_cols=[1,2,3]
    ))
    story.append(PageBreak())

    # PAGE 6: Full Natural Support Protocol
    story+=sh("Natural Recovery Support Stack — Full Protocol",TK,s,"🌿")
    story.append(tbl(
        ["Supplement","Dose","Evidence Level","Primary Role","Take With"],
        [["Ashwagandha (KSM-66)","600 mg/day","Strong (RCTs)","Reduces cortisol, raises LH/T by 15–20%","Food"],
         ["Tongkat Ali (LJ100)","200 mg/day","Moderate","LH stimulation, free testosterone via SHBG","Morning"],
         ["Zinc (picolinate/bisglycinate)","30–50 mg/day","Strong","Testosterone synthesis cofactor — aromatase inhibitor","Evening (not with calcium)"],
         ["Vitamin D3","5000–10000 IU/day","Strong","Testosterone synthesis, LH signalling","Fat-containing meal, with K2"],
         ["Vitamin K2 (MK-7)","100–200 mcg/day","Moderate","Calcium metabolism, testosterone support","With D3"],
         ["Magnesium Glycinate","400–600 mg/day","Strong","Reduces SHBG, improves sleep, testosterone cofactor","Before bed"],
         ["Boron","10 mg/day","Moderate","Reduces SHBG, raises free testosterone acutely","With meal"],
         ["D-Aspartic Acid","3g/day (4 weeks)","Moderate (short-term)","LH stimulation — short-term T boost","Morning fasted"],
         ["Fadogia Agrestis","600 mg/day","Early (promising)","LH mimetic — increases testosterone in studies","Morning"],
         ["Omega-3 (EPA/DHA)","4g/day","Strong","Anti-inflammatory, reduces SHBG, HDL recovery","With meals"],
         ["B-vitamins complex","2x RDA","Strong","Energy metabolism, hormone synthesis support","Morning with food"],
         ["Pregnenolone","25–50 mg/day","Limited","Precursor to testosterone and DHEA production","Morning"]],
        TK,cw=[42*mm,25*mm,25*mm,55*mm,23*mm],left_align_cols=[0,3]
    ))

    doc.build(story,onFirstPage=make_bg(TK,True),onLaterPages=make_bg(TK,False))
    print(f"✅  {path}")

# ════════════════════════════════════════════════════════════
# PDF 20 — ANABOLIC CYCLE NUTRITION & SUPPLEMENTATION BIBLE
# ════════════════════════════════════════════════════════════
def pdf_nutrition():
    TK="nutrition"; s=mk(TK)
    path=os.path.join(OUT,"20_Anabolic_Cycle_Nutrition_Supplementation_Bible.pdf")
    doc=new_doc(path)
    DISC="DISCLAIMER: Educational purposes only. This guide covers nutritional strategies to support muscle gain and fat loss. All supplementation decisions should be made in consultation with a qualified physician or registered dietitian."
    story=[]

    story+=cover(["ANABOLIC CYCLE","NUTRITION &","SUPPLEMENTATION BIBLE"],
                 "Science-Based Diet, Macro Strategy & Supplement Stack for Every Cycle Phase",
                 "Bulking  •  Cutting  •  Recomp  •  Indian Meal Plans  •  On-Cycle Supplements",
                 TK,s,badges=["ALL CYCLE PHASES","MACROS","INDIAN MEALS","FULL SUPP STACK"],
                 disclaimer=DISC,edition="Anabolic Series Vol. 5  •  Nutrition Edition  •  2024")

    # PAGE 2: Macro Framework
    story+=sh("The Anabolic Macro Framework",TK,s,"📊")
    story.append(Paragraph("On an anabolic cycle, the body's capacity for protein synthesis, glycogen storage, and caloric partitioning is significantly enhanced. Your diet must be structured to maximise these enhanced physiological capabilities.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story.append(tbl(
        ["Phase","Calorie Target","Protein","Carbohydrates","Fats","Water","Key Priority"],
        [["Bulking (high dose AAS)","TDEE + 500–700","2.5–3.5 g/kg","5–8 g/kg","0.8–1.0 g/kg","5–6 L/day","Caloric surplus — progressive overload"],
         ["Lean Bulk (moderate AAS)","TDEE + 300–400","2.5–3.0 g/kg","4–6 g/kg","0.8–1.0 g/kg","4–5 L/day","Quality calories — minimise fat gain"],
         ["Recomp (Test + Tren)","TDEE ± 100","3.0–3.5 g/kg","2–4 g/kg","0.8–1.0 g/kg","5–6 L/day","High protein, carb cycling, training split"],
         ["Cutting (Test only)","TDEE − 300–500","3.0–3.5 g/kg","1.5–3 g/kg","0.7–0.9 g/kg","4–5 L/day","Protect muscle at all costs — protein first"],
         ["Competition prep (peak)","TDEE − 500–800","3.5–4.0 g/kg","1–2 g/kg","0.5–0.7 g/kg","4+ L/day","Extreme deficit — AAS preserves mass"],
         ["PCT (recovery)","TDEE + 100","2.5–3.0 g/kg","4–5 g/kg","1.0–1.2 g/kg","4 L/day","Caloric surplus supports T recovery"]],
        TK,cw=[28*mm,28*mm,22*mm,24*mm,20*mm,18*mm,40*mm],left_align_cols=[0,6]
    ))
    story.append(Spacer(1,4*mm))
    story+=sh("Calorie Calculation — Step by Step",TK,s,"🔢")
    story.append(tbl(
        ["Step","Formula","Example (80kg, 25yr male, 178cm)","Result"],
        [["1. Calculate BMR","BMR = 10×weight + 6.25×height - 5×age + 5","10×80 + 6.25×178 - 5×25 + 5","= 1817 kcal"],
         ["2. Activity Multiplier","Sedentary ×1.2 / Light ×1.375 / Moderate ×1.55 / Very active ×1.725","Training 5–6x/week = ×1.725","TDEE = 3134 kcal"],
         ["3. AAS Adjustment","Add 10–15% to TDEE on cycle (enhanced partitioning)","3134 × 1.12","= 3510 kcal effective TDEE"],
         ["4. Goal Adjustment","Bulk: +500 / Maintain: +0 / Cut: −400","3510 + 500 (bulk)","= 4010 kcal target"],
         ["5. Protein Allocation","2.8 g/kg × 80kg = 224g × 4 kcal","224g protein = 896 kcal","~22% of total"],
         ["6. Fats Allocation","0.9 g/kg × 80kg = 72g × 9 kcal","72g fat = 648 kcal","~16% of total"],
         ["7. Carbohydrates (remainder)","4010 - 896 - 648 = 2466 kcal / 4","2466 ÷ 4 = 616g carbs","~62% of total"]],
        TK,cw=[12*mm,65*mm,65*mm,28*mm],left_align_cols=[1,2]
    ))
    story.append(PageBreak())

    # PAGE 3: Meal Timing
    story+=sh("Nutrient Timing — Maximising the Anabolic Window",TK,s,"⏰")
    story.append(tbl(
        ["Meal Timing","Macros","Food Sources","Reason"],
        [["Wake-up (fasted, 6–7 AM)","30–40g protein, 10–20g carbs","Whey + banana / oats + eggs","Stop overnight catabolism — protein fast"],
         ["Pre-workout (90 min before)","40–50g protein, 60–100g carbs, low fat","Chicken rice, or oats + whey, or whole meal","Glycogen loading — sustained energy"],
         ["Intra-workout (during training)","0g protein, 30–50g fast carbs + EAAs","Gatorade + 10g EAAs / Karbolyn","Blood amino acid peak during training stimulus"],
         ["Post-workout (within 45 min)","50g protein, 70–100g fast carbs","Whey + white rice / potato / fruit","Insulin spike + protein synthesis peak"],
         ["Mid-day meal","30–50g protein, 60–80g carbs","Whole foods — chicken, rice, vegetables","Sustained amino acid availability"],
         ["Evening meal","40–50g protein, 40–60g carbs","Fish / mutton / eggs + rice/roti","Anabolic support — lean protein + moderate carbs"],
         ["Pre-sleep","30–40g slow protein, low carb, medium fat","Casein shake / cottage cheese / paneer + nuts","Overnight muscle protein synthesis"]],
        TK,cw=[35*mm,38*mm,52*mm,45*mm],left_align_cols=[1,2,3]
    ))
    story.append(Spacer(1,4*mm))
    story+=sh("Carb Cycling — Weekly Template for Recomp",TK,s,"🔄")
    story.append(tbl(
        ["Day","Training","Carb Target","Protein","Fat","Total Calories"],
        [["Monday","Heavy compound (Legs/Back)","600–700g","250g","70g","4100–4500 kcal"],
         ["Tuesday","Push / Chest / Shoulders","500–600g","240g","70g","3700–4100 kcal"],
         ["Wednesday","REST / light cardio","150–200g","260g","100g","2600–2900 kcal"],
         ["Thursday","Heavy (Deadlift / Squat)","600–700g","250g","70g","4100–4500 kcal"],
         ["Friday","Pull / Back / Biceps","450–500g","240g","75g","3600–3900 kcal"],
         ["Saturday","Arms / Shoulders / Cardio","300–350g","240g","90g","3100–3400 kcal"],
         ["Sunday","REST / optional LISS","100–150g","260g","110g","2500–2800 kcal"]],
        TK,cw=[25*mm,48*mm,30*mm,25*mm,20*mm,32*mm],left_align_cols=[1]
    ))
    story.append(PageBreak())

    # PAGE 4: Indian Bodybuilder Meal Plans
    story+=sh("Indian Bodybuilder Meal Plans — On Cycle",TK,s,"🍛")
    story.append(Paragraph("High protein, calorie-dense Indian meals that support anabolic cycles. These plans use culturally relevant, affordable, and easy-to-prepare foods available across India.",s["BJ"]))
    story.append(Spacer(1,3*mm))
    story+=sh("Bulking Meal Plan — 4000+ kcal/day (80kg Athlete)",TK,s,"")
    story.append(tbl(
        ["Meal","Foods","Protein","Carbs","Fats","kcal"],
        [["Meal 1 (7 AM)","6 whole eggs scrambled + 4 slices whole wheat bread + 1 banana","38g","60g","30g","650"],
         ["Meal 2 (10 AM)","200g chicken breast + 200g cooked basmati rice + dal (100g)","55g","85g","8g","640"],
         ["Pre-WO (1 PM)","2 scoops whey + 150g oats + 1 tbsp peanut butter","50g","80g","14g","650"],
         ["Intra-WO","Gatorade 500ml + 10g BCAA","2g","30g","0g","130"],
         ["Post-WO (4:30 PM)","2 scoops whey + 4 rotis + 250g curd","52g","80g","10g","630"],
         ["Meal 4 (7 PM)","250g mutton keema + 200g cooked rice + salad","55g","70g","20g","700"],
         ["Meal 5 (9 PM)","200g paneer + 2 rotis + rajma 150g","45g","55g","20g","580"],
         ["Pre-sleep (11 PM)","1 scoop casein + 50g almonds","30g","10g","28g","410"],
         ["DAILY TOTAL","","327g","470g","130g","4390"]],
        TK,cw=[28*mm,70*mm,18*mm,18*mm,18*mm,18*mm],left_align_cols=[1]
    ))
    story.append(Spacer(1,4*mm))
    story+=sh("Cutting Meal Plan — 2600 kcal/day (Deficit)",TK,s,"")
    story.append(tbl(
        ["Meal","Foods","Protein","Carbs","Fats","kcal"],
        [["Meal 1 (7 AM)","5 egg whites + 1 whole egg + spinach omelette + black coffee","26g","3g","8g","190"],
         ["Meal 2 (10 AM)","200g grilled chicken + 100g brown rice + cucumber salad","48g","35g","5g","380"],
         ["Pre-WO (1 PM)","1.5 scoops whey + 1 apple","36g","28g","3g","280"],
         ["Intra-WO","EAAs 10g in water","10g","0g","0g","40"],
         ["Post-WO (4 PM)","1.5 scoops whey + 100g cooked rice","38g","38g","3g","330"],
         ["Meal 4 (7 PM)","200g fish (rohu/basa) + 100g cooked dal + 2 rotis","46g","40g","6g","400"],
         ["Meal 5 (9 PM)","200g low-fat paneer + sauteed vegetables (no oil)","34g","10g","8g","250"],
         ["Pre-sleep (11 PM)","1 scoop casein in water","24g","3g","1g","120"],
         ["DAILY TOTAL","","262g","157g","34g","1990 + cardio allowance"]],
        TK,cw=[28*mm,70*mm,18*mm,18*mm,18*mm,18*mm],left_align_cols=[1]
    ))
    story.append(PageBreak())

    # PAGE 5: Supplement Stack
    story+=sh("Complete On-Cycle Supplement Stack",TK,s,"💊")
    story.append(tbl(
        ["Category","Supplement","Dose","Timing","Purpose","Priority"],
        [["Foundation","Whey Protein (Isolate)","2–3 scoops","Post-WO + morning","Hit protein targets","Essential"],
         ["Foundation","Creatine Monohydrate","5g","Post-WO or AM","ATP, strength, cell hydration","Essential"],
         ["Foundation","Omega-3 Fish Oil","4–6g EPA/DHA","With meals","Heart health, anti-inflammatory, HDL support","Essential"],
         ["Foundation","Vitamin D3 + K2","5000 IU + 100mcg","With fat-containing meal","Testosterone synthesis, immune, bone","Essential"],
         ["Foundation","Zinc Bisglycinate","30mg","Before bed","Test synthesis, aromatase inhibition","Essential"],
         ["Foundation","Magnesium Glycinate","400mg","Before bed","Sleep quality, insulin sensitivity, muscle function","Essential"],
         ["Liver Support","TUDCA / UDCA","500mg","With meal","Liver protection — essential if using oral AAS","Essential if oral"],
         ["Liver Support","NAC (N-Acetyl Cysteine)","600mg","Morning","Glutathione precursor, liver + kidney antioxidant","Recommended"],
         ["Cardiovascular","Coenzyme Q10","200mg","With fat meal","Mitochondrial function, BP, heart muscle","Essential (Tren/Deca)"],
         ["Cardiovascular","Taurine","3–5g","Pre-workout","Reduces back pumps, cardiac support","Needed with Anavar"],
         ["Cardiovascular","Garlic Extract","1200mg","With meals","Lowers LDL, raises HDL, mild BP reduction","Recommended"],
         ["Joint Health","Glucosamine + Chondroitin","1500 + 1200mg","With meal","Cartilage support — rapid strength gains stress joints","Recommended"],
         ["Joint Health","Collagen Peptides","10–15g","Post-WO","Connective tissue repair","Recommended"],
         ["Recovery","Ashwagandha KSM-66","600mg","Evening","Cortisol reduction, better sleep, test support","Recommended"],
         ["Recovery","Melatonin","0.5–1mg","30 min before bed","Sleep onset — disrupted by some AAS (Tren)","As needed"],
         ["Hormonal","Vitamin B6 (P5P form)","100–200mg","Daily","Prolactin control — support with Deca/Tren","Needed with Tren"],
         ["Hormonal","Selenium","200mcg","Morning","Thyroid hormone conversion, antioxidant","Recommended"],
         ["Performance","Citrulline Malate","8–10g","30 min pre-WO","Nitric oxide, pump, performance, blood flow","Recommended"],
         ["Performance","Beta-Alanine","3.2g","Pre-WO","Carnosine buffering, reduces fatigue","Recommended"]],
        TK,cw=[25*mm,40*mm,22*mm,22*mm,50*mm,22*mm],left_align_cols=[0,1,4]
    ))
    story.append(PageBreak())

    # PAGE 6: Foods to eat/avoid + cheat meal guide
    story+=sh("Optimal Food Sources for Anabolic Cycles",TK,s,"🥩")
    story.append(tbl(
        ["Category","Best Sources","Amount/Day","Avoid"],
        [["Animal Protein","Chicken breast, eggs, fish (basa/rohu/salmon), mutton (lean), egg whites","250–400g protein foods","Processed meats, high-fat sausages"],
         ["Plant Protein","Paneer, curd (Greek-style), rajma, chana, moong dal, tofu, soya chunks","As needed to hit targets","Excess soy on cycle (phytoestrogens in very high amounts)"],
         ["Complex Carbs","Basmati/brown rice, oats, sweet potato, whole wheat roti, quinoa","Based on carb target","Refined flour (maida), white bread, biscuits"],
         ["Fast Carbs (post-WO)","White rice, banana, mango, dates, sports drink, white bread","50–100g post-WO only","Fructose-heavy sources (spike triglycerides)"],
         ["Healthy Fats","Eggs (yolk), olive oil, coconut oil (cooking), ghee (moderate), nuts, avocado","60–100g fat target","Trans fats, refined vegetable oils (sunflower/canola excess)"],
         ["Vegetables","Spinach, broccoli, capsicum, bottle gourd, tomato, cucumber, mushrooms","400–600g/day","Deep-fried vegetables, pickles (excess sodium)"],
         ["Hydration","Water, coconut water, green tea, black coffee, lemon water","5–6 L/day","Alcohol (severely impairs testosterone and liver function), sugary drinks"]],
        TK,cw=[32*mm,70*mm,28*mm,40*mm],left_align_cols=[0,1,3]
    ))
    story.append(Spacer(1,3*mm))
    story.append(wb("Alcohol is incompatible with anabolic cycles. It directly inhibits testosterone synthesis, impairs protein synthesis, disrupts sleep, elevates oestrogen, and puts additional strain on a liver already under stress from oral AAS. Eliminate completely.",TK,s))
    story.append(Spacer(1,3*mm))
    story+=sh("Refeeds & Diet Breaks on Extended Cycles",TK,s,"🔄")
    story.append(tbl(
        ["Strategy","When to Use","Protocol","Benefits"],
        [["Refeed day","Weekly during cutting cycles","Raise calories to TDEE + 20%, carbs to 6–8 g/kg, keep fat low","Restore leptin, muscle glycogen, boost training performance"],
         ["Diet break (full)","Every 6–8 weeks on extended cut","Eat at TDEE for 7–14 days","Leptin recovery, hormonal reset, psychological relief"],
         ["Carb loading (pre-competition)","Final 5–7 days before show","Sodium/water manipulation + high carb load after depletion","Peak muscle fullness, glycogen saturation for stage"],
         ["Reverse diet (post-cycle)","After finishing a cut or prep","Increase by 50–75 kcal/week until reaching maintenance","Prevent fat regain, support metabolic recovery"]],
        TK,cw=[30*mm,40*mm,60*mm,50*mm],left_align_cols=[1,2,3]
    ))

    doc.build(story,onFirstPage=make_bg(TK,True),onLaterPages=make_bg(TK,False))
    print(f"✅  {path}")

# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Royal Fitness Club Anabolic Series PDFs...\n")
    pdf_beginner()
    pdf_intermediate()
    pdf_advanced()
    pdf_pct()
    pdf_nutrition()
    print("\n🏆 All 5 PDFs generated successfully!")
    print(f"Location: {OUT}")
