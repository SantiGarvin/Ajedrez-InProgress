import cv2
import subprocess

class Webcam:
    def __init__(self, url):
        self.url = url
        self.cap = None

    def open_camera(self):
        # Establecer la conexión ADB con el dispositivo móvil
        adb_command = "adb forward tcp:4747 tcp:4747"
        subprocess.call(adb_command.split())

        # Inicializar el objeto de captura de video con la URL de la cámara del dispositivo móvil
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            print("No se pudo abrir la cámara")
            return False
        return True

    def get_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                print("No se pudo leer el frame")
                return None
        else:
            print("La cámara no está abierta")
            return None

    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None
