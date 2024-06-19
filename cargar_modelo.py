import cv2
import numpy as np
import pyassimp
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Variables globales
window = 0
model = None
width, height = 640, 480

def initGL(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_model():
    global model
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)

    glBegin(GL_TRIANGLES)
    for mesh in model.meshes:
        for face in mesh.faces:
            for index in face:
                vertex = mesh.vertices[index]
                glVertex3f(vertex[0], vertex[1], vertex[2])
    glEnd()

    glutSwapBuffers()

def load_model(path):
    global model
    model = pyassimp.load(path)
    if not model:
        print("Error: could not load model")
        exit(1)

def main():
    global window
    load_model('chessboard.fbx')

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("OpenGL Model Viewer")
    glutDisplayFunc(draw_model)
    glutIdleFunc(draw_model)
    initGL(width, height)
    glutMainLoop()

if __name__ == "__main__":
    main()
