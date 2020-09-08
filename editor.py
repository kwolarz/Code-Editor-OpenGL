from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

characters = []
characters.append([])


w,h= 800, 600
row = 0
column = 0

def arrowHandler(key, x, y):
    if key == GLUT_KEY_UP:
        print('góra')
    elif key == GLUT_KEY_DOWN:
        print('dół')
    elif key == GLUT_KEY_LEFT:
        print('lewo')
    elif key == GLUT_KEY_RIGHT:
        print('prawo')

    return None

def handler(key, x, y):
    global row, column
    print(characters)
    if key == b'\x7f':
        characters[row].pop()
        print(characters)
    elif key==b'\r':
        row += 1
        characters.append([])
        
    else:
        characters[row].append(key.decode('UTF-8'))
    return None

def glut_print(x, y, font, text, r, g, b):
    blending = False 
    if glIsEnabled(GL_BLEND):
        blending = True

    #glEnable(GL_BLEND)
    glColor3f(r, g, b)
    glWindowPos2f(x, y)
    for ch in text :
        glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

    if not blending :
        glDisable(GL_BLEND) 

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for i in range(row + 1):
        glut_print(5, (h-15) - (15 * i), GLUT_BITMAP_HELVETICA_10, str(i), 0.1 , 0.3 , 1.0)

    for charRow in range(row+1):
        for pos, char in enumerate(characters[charRow]):
            if characters[charRow][pos-1] == 'i' and characters[charRow][pos] == 'f':
                glut_print(20 + 10*pos, h - (15 * (charRow + 0)), GLUT_BITMAP_9_BY_15, char, 0.1 , 0.1 , 1.0)
                
            else:
                glut_print(20 + 10*pos, (h - 15) - (15 * (charRow)), GLUT_BITMAP_9_BY_15, char, 1.0 , 1.0 , 1.0)

    glut_print(20 + 10*len(characters[row]), (h - 15) - (15 * (row)), GLUT_BITMAP_HELVETICA_18, "|", 0.5 , 0.5 , 0.5)

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w, h)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutKeyboardFunc(handler)
glutSpecialFunc(arrowHandler)
glutMainLoop()