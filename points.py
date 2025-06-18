from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import random
import math

# Parametry
page_w, page_h = A4
margin = 10 * mm
max_dots = 25
dot_radius = 0.5 * mm   # 2 mm średnicy
num_pages = 10

def generate_pseudorandom_points(n, width, height, margin):
    # liczba komórek w każdym kierunku
    cells = math.ceil(math.sqrt(max_dots))
    cell_w = (width - 2 * margin) / cells
    cell_h = (height - 2 * margin) / cells

    # wszystkie możliwe indeksy komórek
    all_cells = [(i, j) for i in range(cells) for j in range(cells)]
    chosen = random.sample(all_cells, n)

    pts = []
    for i, j in chosen:
        x0 = margin + i * cell_w
        y0 = margin + j * cell_h
        x = random.uniform(x0, x0 + cell_w)
        y = random.uniform(y0, y0 + cell_h)
        pts.append((x, y))
    return pts

# Generacja PDF
c = canvas.Canvas("points.pdf", pagesize=A4)

for _ in range(num_pages):
    n = random.randint(10, 20)
    points = generate_pseudorandom_points(n, page_w, page_h, margin)

    for x, y in points:
        c.setFillColorRGB(0, 0, 0)
        c.circle(x, y, dot_radius, fill=1, stroke=0)

    c.showPage()

c.save()
print("Gotowe: punkty_trening_linii_pseudolosowe.pdf")
