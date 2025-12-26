import turtle

def draw_polygon(vertices):
    """Menggambar polygon dari daftar vertices"""
    all_points = []
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        
        # Menggambar garis dengan titik-titik
        all_points.extend(draw_line(x1, y1, x2, y2))
    
    return all_points

def draw_line(x1, y1, x2, y2):
    """Menggambar garis dari (x1,y1) ke (x2,y2) dengan titik-titik"""
    points = []
    steps = 10  # Jumlah titik pada setiap garis
    
    for i in range(steps + 1):
        t = i / steps
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        points.append((x, y))
    
    return points

def draw_points(points):
    """Menggambar titik-titik pada koordinat yang diberikan"""
    turtle.speed(0)
    turtle.penup()
    
    for x, y in points:
        turtle.goto(x, y)
        turtle.dot(5, "black")
    
    turtle.done()

# Setup turtle
turtle.title("Pola Titik Geometris")

# Definisi vertices untuk membentuk pola segitiga/belah ketik
vertices = [(0, 80), (0, 0), (80, 0), (80, 80)]

# Menggambar polygon dan mendapatkan semua titik
points = draw_polygon(vertices)

# Menggambar semua titik
draw_points(points)