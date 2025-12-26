import turtle

def draw_line(x1, y1, x2, y2):
    """Menggambar garis dari (x1,y1) ke (x2,y2) menggunakan algoritma DDA"""
    points = []
    
    dx = x2 - x1
    dy = y2 - y1
    
    # Tentukan jumlah langkah
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    
    if steps == 0:
        return [(x1, y1)]
    
    # Hitung increment untuk x dan y
    x_inc = dx / steps
    y_inc = dy / steps
    
    # Generate titik-titik
    x = x1
    y = y1
    
    for i in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    
    return points

def draw_triangle(vertices):
    """Menggambar segitiga dari 3 titik vertices"""
    all_points = []
    
    # Gambar 3 sisi segitiga
    for i in range(3):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % 3]
        points = draw_line(x1, y1, x2, y2)
        all_points.extend(points)
    
    return all_points

def draw_points(points, scale=3):
    """Menggambar semua titik menggunakan turtle"""
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    
    for x, y in points:
        turtle.goto(x * scale, y * scale)
        turtle.dot(4, "black")
    
    turtle.done()

# Setup window
turtle.title("Algoritma Gambar Segitiga")
turtle.setup(width=600, height=600)

# Definisi 3 titik vertices segitiga
# Segitiga dengan posisi di tengah layar
vertices = [
    (0, 60),      # Titik atas
    (-50, -30),   # Titik kiri bawah
    (50, -30)     # Titik kanan bawah
]

# Gambar segitiga
points = draw_triangle(vertices)

# Hapus duplikat titik
points = list(set(points))

# Tampilkan titik-titik
draw_points(points)