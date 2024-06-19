import cv2
import numpy as np
import subprocess

def abrir_camara_movil(url):
    # Establecer la conexión ADB con el dispositivo móvil
    adb_command = "adb forward tcp:4747 tcp:4747"
    subprocess.call(adb_command.split())

    # Inicializar el objeto de captura de video con la URL de la cámara del dispositivo móvil
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return None
    return cap

def detectar_marcadores_aruco(cap, diccionario, parametros):
    cv2.namedWindow('Detección de Marcadores ArUco')  # Crear una única ventana al principio
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los marcadores ArUco en el frame
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)

        # Si se detectan marcadores, dibujarlos en el frame
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Mostrar el frame
        cv2.imshow('Detección de Marcadores ArUco', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    url = "http://localhost:4747/video"

    # Configurar el diccionario ArUco y los parámetros del detector
    diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    
    # Configurar manualmente los parámetros del detector
    parametros = cv2.aruco.DetectorParameters()

    cap = abrir_camara_movil(url)
    if cap:
        detectar_marcadores_aruco(cap, diccionario, parametros)

if __name__ == "__main__":
    main()
