"""Make the PDF of Fig. 2 from figures/Fig2_nationalnetworks.pptx as a fully vector figure.

PowerPoint exports the two network pictures of the slide (Gephi PDFs wrapped in EMF) as their low-resolution bitmap
previews (about 80 dpi). This script builds the PDF directly instead, with the layout of the slide:

- the two Gephi network PDFs are placed with the positions and crops of the slide pictures (vector);
- the country labels of the Gephi PDFs (Helvetica, not embedded) are redrawn in embedded Arial with the same size,
  colour and centre;
- the panel letters, the in-degree legend (circles, lines and values) are drawn as vectors with embedded Arial.

Usage (from the code folder):
    python make_Fig2_pdf.py [input.pptx] [output.pdf]
Defaults: ../figures/Fig2_nationalnetworks.pptx and ../figures/Fig2_nationalnetworks.pdf

Requires PyMuPDF (pip install pymupdf) and the Arial fonts; set ARIAL_FONT and ARIAL_BOLD_FONT to the .ttf files
if they are not found in the usual system folders.
"""
import os
import re
import sys
import zipfile

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PPTX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figures', 'Fig2_nationalnetworks.pptx')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'figures', 'Fig2_nationalnetworks.pdf')


def find_font(env, names):
    """the first existing font file: the environment variable, then the usual macOS, Windows and Linux folders"""
    folders = ['/System/Library/Fonts/Supplemental', '/Library/Fonts', 'C:/Windows/Fonts',
               '/usr/share/fonts/truetype/msttcorefonts', '/usr/share/fonts/TTF']
    candidates = [os.environ.get(env)] + [os.path.join(d, n) for d in folders for n in names]
    for f in candidates:
        if f and os.path.exists(f):
            return f
    sys.exit(f'Arial font not found: set {env} to the path of {names[0]}')


FONT = {False: find_font('ARIAL_FONT', ['Arial.ttf', 'arial.ttf']),
        True: find_font('ARIAL_BOLD_FONT', ['Arial Bold.ttf', 'arialbd.ttf', 'Arial_Bold.ttf'])}
fonts = {bold: pymupdf.Font(fontfile=f) for bold, f in FONT.items()}

z = zipfile.ZipFile(PPTX)
slide = z.read('ppt/slides/slide1.xml').decode()
pres = z.read('ppt/presentation.xml').decode()
rels = dict(re.findall(r'Id="(\w+)"[^>]*Target="../media/([^"]+)"', z.read('ppt/slides/_rels/slide1.xml.rels').decode()))


def pt(emu):
    """EMU to points"""
    return int(emu) / 12700


W, H = [pt(v) for v in re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', pres).groups()]


def emf_pdf(name):
    """the Gephi PDF inside an EMF picture of the slide, with its country labels redrawn in embedded Arial"""
    b = z.read('ppt/media/' + name)
    i, e = b.find(b'%PDF'), b.rfind(b'%%EOF')
    if i < 0:
        sys.exit(f'{name} does not contain a PDF: insert the Gephi PDF in PowerPoint as a picture')
    src = pymupdf.open('pdf', b[i:e + 5])
    p = src[0]
    spans = [sp for bl in p.get_text('dict')['blocks'] for l in bl.get('lines', []) for sp in l['spans']
             if sp['text'].strip()]
    # remove only the text; the network drawing (nodes, edges) is kept
    for sp in spans:
        p.add_redact_annot(pymupdf.Rect(sp['bbox']))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                       text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    p.insert_font(fontname='arial', fontfile=FONT[False])
    for sp in spans:
        t, sz, c = sp['text'].strip(), sp['size'], sp['color']
        colour = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
        centre = (sp['bbox'][0] + sp['bbox'][2]) / 2
        x = centre - fonts[False].text_length(t, sz) / 2
        p.insert_text((x, sp['origin'][1]), t, fontsize=sz, fontname='arial', color=colour)
    return src


doc = pymupdf.open()
page = doc.new_page(width=W, height=H)
for bold, f in FONT.items():
    page.insert_font(fontname='arialb' if bold else 'arial', fontfile=f)

for m in re.finditer(r'<p:(sp|pic|cxnSp)>.*?</p:\1>', slide, re.S):
    kind, b = m.group(1), m.group(0)
    x, y, cx, cy = [pt(v) for v in re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"', b).groups()]
    r = pymupdf.Rect(x, y, x + cx, y + cy)
    if kind == 'pic':
        src = emf_pdf(rels[re.search(r'r:embed="(\w+)"', b).group(1)])
        P = src[0].rect
        crop = re.search(r'<a:srcRect l="(-?\d+)" t="(-?\d+)" r="(-?\d+)" b="(-?\d+)"', b)
        l, t, rr, bb = [int(v) / 1e5 for v in crop.groups()] if crop else (0, 0, 0, 0)
        clip = pymupdf.Rect(l * P.width, t * P.height, (1 - rr) * P.width, (1 - bb) * P.height)
        page.show_pdf_page(r, src, 0, clip=clip, keep_proportion=False)
    elif 'prst="ellipse"' in b:
        page.draw_oval(r, color=(0, 0, 0), width=pt(re.search(r'<a:ln w="(\d+)"', b).group(1)))
    elif kind == 'cxnSp':
        page.draw_line(r.tl, (r.x1, r.y0), color=(0, 0, 0), width=pt(re.search(r'<a:ln w="(\d+)"', b).group(1)))
    else:
        t = ''.join(re.findall(r'<a:t>([^<]*)', b))
        if not t:
            continue
        sz = int(re.search(r'sz="(\d+)"', b).group(1)) / 100
        bold = ' b="1"' in b
        align = re.search(r'algn="(\w+)"', b)
        align = align.group(1) if align else 'l'
        tw = fonts[bold].text_length(t, sz)
        tx = {'l': r.x0, 'ctr': (r.x0 + r.x1 - tw) / 2, 'r': r.x1 - tw}[align]
        # the text boxes are vertically centred: centre the cap height (Arial: 0.716 em)
        ty = (r.y0 + r.y1) / 2 + 0.716 * sz / 2
        page.insert_text((tx, ty), t, fontsize=sz, fontname='arialb' if bold else 'arial')

doc.subset_fonts()
doc.set_metadata({'title': 'Fig. 2: international networks of national citation preferences',
                  'creator': 'make_Fig2_pdf.py from ' + os.path.basename(PPTX)})
doc.save(OUT, garbage=4, deflate=True)
print('saved', os.path.normpath(OUT), f'({W / 72 * 25.4:.1f} x {H / 72 * 25.4:.1f} mm)')
