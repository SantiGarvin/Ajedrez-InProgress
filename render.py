import cv2
import numpy as np
import pyassimp
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Webcam import Webcam

# Variables globales
window = 0
scene = None
width, height = 640, 480
webcam = None
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
parameters = cv2.aruco.DetectorParameters_create()

# Matriz de cámara y coeficientes de distorsión (debe calibrarse)
camera_matrix = np.array([[800, 0, width / 2],
                          [0, 800, height / 2],
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((4, 1))  # Asumiendo que no hay distorsión

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

def draw_model(rvec, tvec):
    global scene
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)

    rotM = np.zeros(shape=(3, 3))
    cv2.Rodrigues(rvec, rotM)
    mat = np.array([[rotM[0][0], rotM[0][1], rotM[0][2], tvec[0]],
                    [rotM[1][0], rotM[1][1], rotM[1][2], tvec[1]],
                    [rotM[2][0], rotM[2][1], rotM[2][2], tvec[2]],
                    [0.0, 0.0, 0.0, 1.0]])
    glMultMatrixf(mat.T)

    glBegin(GL_TRIANGLES)
    for mesh in scene.meshes:
        for face in mesh.faces:
            for index in face:
                vertex = mesh.vertices[index]
                glVertex3f(vertex[0], vertex[1], vertex[2])
    glEnd()

    glutSwapBuffers()

def load_model(path):
    global scene
    scene = pyassimp.load(path)
    if not scene:
        print("Error: could not load model")
        exit(1)

def render_loop():
    frame = webcam.get_frame()
    if frame is not None:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = cv2.aruco.detectMarkers(frame_gray, aruco_dict, parameters=parameters)
        if ids is not None:
            for corner, id in zip(corners, ids):
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 0.05, camera_matrix, dist_coeffs)
                if rvec is not None and tvec is not None:
                    draw_model(rvec[0], tvec[0])
        cv2.imshow("Webcam", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        glutLeaveMainLoop()
        webcam.release()
        cv2.destroyAllWindows()
        return

def start_rendering(camera_url):
    global window, webcam
    load_model('chessboard.fbx')

    # Inicializar la cámara
    webcam = Webcam(camera_url)
    if not webcam.open_camera():
        print("No se pudo iniciar la cámara")
        return

    import sys
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("OpenGL Model Viewer with Webcam")
    glutDisplayFunc(render_loop)
    glutIdleFunc(render_loop)
    initGL(width, height)
    glutMainLoop()

if __name__ == "__main__":
    start_rendering("http://127.0.0.1:4747/video")
