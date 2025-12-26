import turtle
import random

# --- SETUP LAYAR ---
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("SEMANGAT")

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# Warna bunga
colors = ["red", "magenta", "purple", "pink", "orange"]

# --- BUNGA KELOPAK BESAR ---
def bunga_besar(x, y, radius, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    for _ in range(6):                      # 6 kelopak besar
        pen.circle(radius, 60)              # setengah lingkaran memanjang
        pen.left(120)
        pen.circle(radius, 60)
        pen.left(60)
    pen.end_fill()

# --- BATANG ---
def batang(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.width(7)
    pen.color("green")
    pen.setheading(-90)
    pen.forward(180)

# --- DAUN BESAR ---
def daun_besar(x, y, scale=1):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color("green")
    pen.begin_fill()
    pen.left(45)
    pen.circle(40 * scale, 90)
    pen.right(90)
    pen.circle(40 * scale, 90)
    pen.end_fill()
    pen.setheading(0)

# --- GAMBAR SATU BUNGA BESAR ---
posisi = [(-120, 120), (-20, 180), (80, 130)]

for x, y in posisi:
    warna = random.choice(colors)
    bunga_besar(x, y, 60, warna)    # kelopak besar (radius 60)
    batang(x + 5, y - 20)
    daun_besar(x - 10, y - 80, 1.1)
    daun_besar(x + 30, y - 110, 0.9)

# --- TULISAN BAWAH ---
pen.penup()
pen.goto(0, -240)
pen.color("black")
pen.write("SEMANGAT", align="center",
          font=("Comic Sans MS", 34, "bold"))

screen.mainloop()
