from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

rotY = 0

# =====================
# BANGUN DASAR
# =====================
def balok(p, t, l):
    glBegin(GL_QUADS)
    # Depan
    glVertex3f(-p, 0, l); glVertex3f(p, 0, l)
    glVertex3f(p, t, l);  glVertex3f(-p, t, l)
    # Belakang
    glVertex3f(-p, 0, -l); glVertex3f(p, 0, -l)
    glVertex3f(p, t, -l);  glVertex3f(-p, t, -l)
    # Kiri
    glVertex3f(-p, 0, -l); glVertex3f(-p, 0, l)
    glVertex3f(-p, t, l);  glVertex3f(-p, t, -l)
    # Kanan
    glVertex3f(p, 0, -l); glVertex3f(p, 0, l)
    glVertex3f(p, t, l);  glVertex3f(p, t, -l)
    # Atas
    glVertex3f(-p, t, l); glVertex3f(p, t, l)
    glVertex3f(p, t, -l); glVertex3f(-p, t, -l)
    # Bawah
    glVertex3f(-p, 0, l); glVertex3f(p, 0, l)
    glVertex3f(p, 0, -l); glVertex3f(-p, 0, -l)
    glEnd()

# =====================
# ATAP SEGITIGA RAPI
# =====================
def atap_pelana(p, l, tinggi):
    # Depan & Belakang
    glBegin(GL_TRIANGLES)
    # Depan
    glVertex3f(-p, 0, l)
    glVertex3f(p, 0, l)
    glVertex3f(0, tinggi, l)
    # Belakang
    glVertex3f(-p, 0, -l)
    glVertex3f(p, 0, -l)
    glVertex3f(0, tinggi, -l)
    glEnd()

    # Sisi kiri & kanan
    glBegin(GL_QUADS)
    # Kiri
    glVertex3f(-p, 0, l)
    glVertex3f(0, tinggi, l)
    glVertex3f(0, tinggi, -l)
    glVertex3f(-p, 0, -l)
    # Kanan
    glVertex3f(p, 0, l)
    glVertex3f(0, tinggi, l)
    glVertex3f(0, tinggi, -l)
    glVertex3f(p, 0, -l)
    glEnd()

# =====================
# JENDELA
# =====================
def jendela(x, y, z):
    glColor3f(0.12, 0.20, 0.30)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(0.9, 1.4, 0.05)
    glutSolidCube(1)
    glPopMatrix()

# =====================
# PINTU
# =====================
def pintu():
    glColor3f(0.30, 0.18, 0.10)
    glPushMatrix()
    glTranslatef(0, 1.2, 3.05)
    glScalef(1.4, 2.5, 0.12)
    glutSolidCube(1)
    glPopMatrix()

# =====================
# GARASI & MOBIL
# =====================
def mobil(x, z):
    glColor3f(0.15, 0.15, 0.18)
    glPushMatrix()
    glTranslatef(x, 0.4, z)
    glScalef(2, 0.5, 1)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.05, 0.05, 0.05)
    for dx in (-0.8, 0.8):
        for dz in (-0.5, 0.5):
            glPushMatrix()
            glTranslatef(x + dx, 0.15, z + dz)
            glutSolidTorus(0.05, 0.18, 12, 12)
            glPopMatrix()

def garasi():
    glColor3f(0.35, 0.35, 0.37)
    glPushMatrix()
    glTranslatef(6.5, 0, -1.5)
    balok(2.2, 2.2, 3)
    glPopMatrix()

    glColor3f(0.20, 0.20, 0.22)
    glPushMatrix()
    glTranslatef(6.5, 1, 1.6)
    glScalef(3.5, 1.6, 0.1)
    glutSolidCube(1)
    glPopMatrix()

    mobil(6.5, -1.5)

# =====================
# POHON
# =====================
def pohon(x, z):
    glColor3f(0.30, 0.20, 0.12)
    glPushMatrix()
    glTranslatef(x, 1.5, z)
    glScalef(0.6, 3, 0.6)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.08, 0.30, 0.10)
    for i in range(3):
        glPushMatrix()
        glTranslatef(x, 3 + i * 0.6, z)
        glutSolidSphere(1.4 - i * 0.3, 20, 20)
        glPopMatrix()

# =====================
# RUMAH (LANTAI 1 & 2)
# =====================
def rumah():
    # LANTAI 1
    glColor3f(0.55, 0.55, 0.53)
    balok(4.5, 3, 3)

    pintu()
    for x in (-2, 0, 2):
        jendela(x, 1.5, 3.01)

    # LANTAI 2 (DIPERJELAS)
    glColor3f(0.48, 0.48, 0.46)
    glPushMatrix()
    glTranslatef(0, 3.0, 0)
    balok(3.5, 2.2, 2.4)
    glPopMatrix()

    for x in (-1.5, 0, 1.5):
        jendela(x, 4.1, 2.41)

    # ATAP DI ATAS LANTAI 2
    glColor3f(0.25, 0.15, 0.12)
    glPushMatrix()
    glTranslatef(0, 5.2, 0)
    atap_pelana(3.8, 2.6, 1.8)
    glPopMatrix()

# =====================
# TAMAN
# =====================
def taman():
    glColor3f(0.10, 0.35, 0.12)
    glPushMatrix()
    glTranslatef(0, -0.8, 0)
    glScalef(30, 0.1, 30)
    glutSolidCube(1)
    glPopMatrix()

# =====================
# DISPLAY
# =====================
def display():
    global rotY
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(18, 6, 18, 0, 2, 0, 0, 1, 0)
    glRotatef(rotY, 0, 1, 0)

    taman()
    rumah()
    garasi()

    pohon(-10, -6)
    pohon(-10, 6)
    pohon(10, -6)
    pohon(10, 6)

    glutSwapBuffers()

# =====================
# KEYBOARD
# =====================
def keyboard(key, x, y):
    global rotY
    if key == b'a': rotY -= 5
    if key == b'd': rotY += 5
    if key == b'\x1b': sys.exit(0)
    glutPostRedisplay()

# =====================
# INIT
# =====================
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.18, 0.22, 0.30, 1)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.5, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glLightfv(GL_LIGHT0, GL_POSITION, [15, 20, 15, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])

# =====================
# MAIN
# =====================
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1400, 900)
glutCreateWindow(b"Rumah 2 ")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
