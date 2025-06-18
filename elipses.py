import random
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# --- Parametry Konfiguracyjne ---

# Parametry strony i marginesów
PAGE_W, PAGE_H = A4
MARGIN = 5 * mm
NUM_PAGES = 10

# Minimalny odstęp między krawędziami dwóch elips
SHAPE_PADDING = 10 * mm

# Parametry kropek
DOT_RADIUS = 0.4 * mm
MIN_POINTS_PER_SHAPE = 20
MAX_POINTS_PER_SHAPE = 40

# Parametry elipsy
MIN_SEMI_AXIS = 15 * mm
MAX_SEMI_AXIS = 60 * mm
MIN_OVALNESS = 0.2

# Parametry logiki wypełniania strony i detekcji kolizji
MAX_PLACEMENT_ATTEMPTS_PER_SHAPE = 200
MAX_CONSECUTIVE_FAILS = 100
# Liczba punktów na obrysie używana do precyzyjnego sprawdzania kolizji
COLLISION_TEST_POINTS = 36


def is_point_in_ellipse(px, py, ellipse_def):
    """
    Sprawdza, czy punkt (px, py) znajduje się wewnątrz elipsy.
    Elipsa jest zdefiniowana przez słownik `ellipse_def`.
    Test uwzględnia padding, wirtualnie powiększając elipsę.
    """
    a = ellipse_def['a'] + SHAPE_PADDING / 2
    b = ellipse_def['b'] + SHAPE_PADDING / 2
    cx = ellipse_def['cx']
    cy = ellipse_def['cy']
    angle = ellipse_def['angle']

    # Przesuń punkt tak, jakby elipsa była w centrum układu współrzędnych
    translated_x = px - cx
    translated_y = py - cy

    # Obróć punkt w przeciwnym kierunku niż elipsa
    cos_a = math.cos(-angle)
    sin_a = math.sin(-angle)
    local_x = translated_x * cos_a - translated_y * sin_a
    local_y = translated_x * sin_a + translated_y * cos_a

    # Sprawdź standardowe równanie elipsy
    return (local_x / a) ** 2 + (local_y / b) ** 2 <= 1


def check_analytical_collision(ellipse1_def, ellipse2_def):
    """
    Sprawdza kolizję między dwoma elipsami zdefiniowanymi matematycznie.
    Testuje, czy punkty z obrysu jednej elipsy wchodzą w obszar drugiej.
    """
    # Test 1: Czy punkty z elipsy 1 są wewnątrz elipsy 2?
    for i in range(COLLISION_TEST_POINTS):
        theta = 2 * math.pi * i / COLLISION_TEST_POINTS
        # Oblicz punkt na obrysie elipsy 1
        x0 = ellipse1_def['a'] * math.cos(theta)
        y0 = ellipse1_def['b'] * math.sin(theta)
        # Obróć i przesuń ten punkt
        cos1 = math.cos(ellipse1_def['angle'])
        sin1 = math.sin(ellipse1_def['angle'])
        px = x0 * cos1 - y0 * sin1 + ellipse1_def['cx']
        py = x0 * sin1 + y0 * cos1 + ellipse1_def['cy']

        if is_point_in_ellipse(px, py, ellipse2_def):
            return True

    # Test 2: Czy punkty z elipsy 2 są wewnątrz elipsy 1?
    for i in range(COLLISION_TEST_POINTS):
        theta = 2 * math.pi * i / COLLISION_TEST_POINTS
        x0 = ellipse2_def['a'] * math.cos(theta)
        y0 = ellipse2_def['b'] * math.sin(theta)
        cos2 = math.cos(ellipse2_def['angle'])
        sin2 = math.sin(ellipse2_def['angle'])
        px = x0 * cos2 - y0 * sin2 + ellipse2_def['cx']
        py = x0 * sin2 + y0 * cos2 + ellipse2_def['cy']

        if is_point_in_ellipse(px, py, ellipse1_def):
            return True

    return False


def generate_shapes_for_page():
    """
    Generuje kształty, wypełniając stronę z użyciem precyzyjnej, analitycznej detekcji kolizji.
    """
    placed_shapes_definitions = []
    consecutive_failures = 0

    while True:
        shape_placed_successfully = False
        for _ in range(MAX_PLACEMENT_ATTEMPTS_PER_SHAPE):
            # 1. Losowe parametry elipsy
            major_axis = random.uniform(MIN_SEMI_AXIS, MAX_SEMI_AXIS)
            ovalness = random.uniform(MIN_OVALNESS, 1.0)
            minor_axis = major_axis * ovalness
            angle_rad = random.uniform(0, math.pi)

            # Wstępne, szybkie sprawdzenie za pomocą prostokątnego bounding boxa
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            half_width = abs(major_axis * cos_a) + abs(minor_axis * sin_a)
            half_height = abs(major_axis * sin_a) + abs(minor_axis * cos_a)

            if (2 * half_width > PAGE_W - 2 * MARGIN) or (2 * half_height > PAGE_H - 2 * MARGIN):
                continue

            cx = random.uniform(MARGIN + half_width, PAGE_W - MARGIN - half_width)
            cy = random.uniform(MARGIN + half_height, PAGE_H - MARGIN - half_height)

            # Stwórz pełną definicję matematyczną nowej elipsy
            current_ellipse_def = {'cx': cx, 'cy': cy, 'a': major_axis, 'b': minor_axis, 'angle': angle_rad}

            # Precyzyjne sprawdzenie kolizji z każdą istniejącą elipsą
            has_collision = any(check_analytical_collision(current_ellipse_def, existing_def) for existing_def in
                                placed_shapes_definitions)

            if not has_collision:
                placed_shapes_definitions.append(current_ellipse_def)
                shape_placed_successfully = True
                break

        if shape_placed_successfully:
            consecutive_failures = 0
            print(f"   -> Umieszczono {len(placed_shapes_definitions)} obiektów.")
        else:
            consecutive_failures += 1

        if consecutive_failures >= MAX_CONSECUTIVE_FAILS:
            print(f"   -> Strona uznana za pełną. Umieszczono {len(placed_shapes_definitions)} obiektów.")
            break

    # Na koniec, wygeneruj listy punktów do narysowania na podstawie zapisanych definicji
    final_points_to_draw = []
    for shape_def in placed_shapes_definitions:
        points = []
        size_ratio = (shape_def['a'] - MIN_SEMI_AXIS) / (MAX_SEMI_AXIS - MIN_SEMI_AXIS)
        num_points = int(MIN_POINTS_PER_SHAPE + size_ratio * (MAX_POINTS_PER_SHAPE - MIN_POINTS_PER_SHAPE))

        cos_a = math.cos(shape_def['angle'])
        sin_a = math.sin(shape_def['angle'])

        for i in range(num_points):
            theta = 2 * math.pi * i / num_points
            x0 = shape_def['a'] * math.cos(theta)
            y0 = shape_def['b'] * math.sin(theta)
            px = x0 * cos_a - y0 * sin_a + shape_def['cx']
            py = x0 * sin_a + y0 * cos_a + shape_def['cy']
            points.append((px, py))
        final_points_to_draw.append(points)

    return final_points_to_draw


def create_pdf(filename="elipses.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    print(f"📄 Rozpoczynam generowanie pliku '{filename}' (może to potrwać dłużej)...")

    for i in range(NUM_PAGES):
        print(f"   -> Tworzenie strony {i + 1}/{NUM_PAGES}...")
        shapes = generate_shapes_for_page()

        c.setFillColorRGB(0, 0, 0)
        for shape_points in shapes:
            for x, y in shape_points:
                c.circle(x, y, DOT_RADIUS, fill=1, stroke=0)
        c.showPage()

    c.save()
    print(f"✅ Gotowe! Zapisano plik '{filename}'.")


if __name__ == "__main__":
    create_pdf()
