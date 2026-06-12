"""Apply dark background overlay to the two flagship PDFs that lack it."""
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas as c_lib
from PyPDF2 import PdfReader, PdfWriter

OUT = '/home/user/royal-fitness-club/generated_pdfs'
W, H = A4

def dark_overlay(num_pages):
    buf = io.BytesIO()
    c = c_lib.Canvas(buf, pagesize=A4)
    for _ in range(num_pages):
        c.setFillColor(colors.HexColor('#020b18'))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.showPage()
    c.save()
    buf.seek(0)
    return buf

def apply(pdf_path):
    reader = PdfReader(pdf_path)
    n = len(reader.pages)
    bg_reader = PdfReader(dark_overlay(n))
    writer = PdfWriter()
    for i in range(n):
        bg = bg_reader.pages[i]
        bg.merge_page(reader.pages[i])
        writer.add_page(bg)
    tmp = pdf_path + '.tmp'
    with open(tmp, 'wb') as f:
        writer.write(f)
    os.replace(tmp, pdf_path)
    print(f'  ✓ {os.path.basename(pdf_path)} — {n} pages with dark background')

targets = [
    '00_Fitness_Mindset_Guidance.pdf',
    '00_Anabolic_Full_Guide.pdf',
]
for t in targets:
    apply(os.path.join(OUT, t))

print('Done.')
