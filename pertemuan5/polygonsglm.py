import turtle
import math

def draw_line(x1, y1, x2, y2, steps=10):
    """Menggambar garis dari (x1,y1) ke (x2,y2) dengan titik-titik"""
    points = []
    
    for i in range(steps + 1):
        t = i / steps
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        points.append((x, y))
    
    return points

def draw_pentagon(vertices, steps=10):
    """Menggambar segi lima dari daftar vertices dengan titik-titik"""
    all_points = []
    
    # Menggambar 5 sisi segi lima
    for i in range(5):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % 5]
        
        # Menambahkan titik-titik sepanjang garis
        all_points.extend(draw_line(x1, y1, x2, y2, steps))
    
    return all_points

def generate_pentagon_vertices(radius=100):
    """Menghasilkan koordinat vertices untuk segi lima beraturan"""
    vertices = []
    
    # Segi lima beraturan memiliki sudut 72 derajat antar titik
    for i in range(5):
        angle = math.radians(90 + i * 72)  # Mulai dari atas (90 derajat)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, y))
    
    return vertices

def draw_points(points):
    """Menggambar titik-titik pada koordinat yang diberikan"""
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    
    for x, y in points:
        turtle.goto(x, y)
        turtle.dot(5, "black")
    
    turtle.done()

# Setup window
turtle.title("Segi Lima Titik dengan Turtle")
turtle.setup(width=600, height=600)

# Generate vertices untuk segi lima beraturan
vertices = generate_pentagon_vertices(radius=100)

# Menggambar segi lima dengan titik-titik
points = draw_pentagon(vertices, steps=15)

# Menggambar semua titik
draw_points(points)