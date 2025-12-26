import turtle
import math

def draw_petal(radius, angle):
    """Menggambar satu kelopak bunga mawar"""
    turtle.circle(radius, angle)
    turtle.left(180 - angle)
    turtle.circle(radius, angle)
    turtle.left(180 - angle)

def draw_rose():
    """Menggambar bunga mawar lengkap"""
    turtle.speed(0)
    turtle.pensize(2)
    
    # Menggambar kelopak bunga (8 kelopak)
    turtle.color("red", "pink")
    turtle.begin_fill()
    
    for _ in range(8):
        draw_petal(100, 60)
        turtle.left(45)
    
    turtle.end_fill()
    
    # Menggambar lingkaran tengah
    turtle.penup()
    turtle.goto(0, -20)
    turtle.pendown()
    turtle.color("yellow", "gold")
    turtle.begin_fill()
    turtle.circle(20)
    turtle.end_fill()
    
    # Menggambar batang
    turtle.penup()
    turtle.goto(0, -20)
    turtle.pendown()
    turtle.color("green")
    turtle.pensize(5)
    turtle.right(90)
    turtle.forward(200)
    
    # Menggambar daun kiri
    turtle.pensize(2)
    turtle.left(45)
    turtle.color("green", "lightgreen")
    turtle.begin_fill()
    turtle.circle(50, 90)
    turtle.left(90)
    turtle.circle(50, 90)
    turtle.end_fill()
    
    # Kembali ke batang
    turtle.penup()
    turtle.goto(0, -120)
    turtle.setheading(-90)
    turtle.pendown()
    
    # Menggambar daun kanan
    turtle.right(45)
    turtle.color("green", "lightgreen")
    turtle.begin_fill()
    turtle.circle(-50, 90)
    turtle.right(90)
    turtle.circle(-50, 90)
    turtle.end_fill()
    
    turtle.hideturtle()
    turtle.done()

# Setup window
turtle.title("Menggambar Mawar")
turtle.setup(width=800, height=800)
turtle.bgcolor("white")

# Posisi awal
turtle.penup()
turtle.goto(0, 0)
turtle.pendown()

# Menggambar mawar
draw_rose()