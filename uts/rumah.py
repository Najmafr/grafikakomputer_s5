from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# =====================
# BANGUN DASAR 2D
# =====================
def persegi(x, y, w, h):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

def segitiga(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

# =====================
# JENDELA & PINTU
# =====================
def jendela(x, y):
    glColor3f(0.12, 0.20, 0.30)
    persegi(x, y, 40, 60)

def pintu(x, y):
    glColor3f(0.30, 0.18, 0.10)
    persegi(x, y, 50, 90)

# =====================
# POHON 2D
# =====================
def pohon(x, y):
    glColor3f(0.35, 0.22, 0.12)
    persegi(x + 20, y, 20, 60)

    glColor3f(0.08, 0.30, 0.10)
    glBegin(GL_POLYGON)
    for i in range(360):
        glVertex2f(
            x + 30 + 35 * __import__("math").cos(i),
            y + 90 + 35 * __import__("math").sin(i)
        )
    glEnd()

# =====================
# GARASI & MOBIL 2D
# =====================
def mobil(x, y):
    glColor3f(0.15, 0.15, 0.18)
    persegi(x, y, 90, 25)
    persegi(x + 15, y + 25, 60, 20)

def garasi(x, y):
    glColor3f(0.45, 0.45, 0.47)
    persegi(x, y, 120, 80)

    glColor3f(0.25, 0.25, 0.27)
    persegi(x + 15, y, 90, 50)

    mobil(x + 15, y + 5)

# =====================
# RUMAH 2D (2 LANTAI)
# =====================
def rumah():
    # LANTAI 1
    glColor3f(0.55, 0.55, 0.53)
    persegi(300, 150, 300, 150)

    pintu(425, 150)
    jendela(330, 210)
    jendela(520, 210)

    # LANTAI 2
    glColor3f(0.48, 0.48, 0.46)
    persegi(350, 300, 200, 120)

    jendela(370, 340)
    jendela(470, 340)

    # ATAP SEGITIGA
    glColor3f(0.25, 0.15, 0.12)
    segitiga(340, 420, 560, 420, 450, 500)

# =====================
# TAMAN
# =====================
def taman():
    glColor3f(0.10, 0.35, 0.12)
    persegi(0, 0, 900, 150)

# =====================
# DISPLAY
# =====================
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    taman()
    rumah()

    garasi(650, 150)

    pohon(100, 150)
    pohon(180, 150)
    pohon(760, 150)

    glFlush()

# =====================
# INIT 2D
# =====================
def init():
    glClearColor(0.18, 0.22, 0.30, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 900, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)

# =====================
# MAIN
# =====================
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(900, 600)
glutCreateWindow(b"Rumah 2D - OpenGL")
init()
glutDisplayFunc(display)
glutMainLoop()
