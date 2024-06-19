# import cv2

# # Dirección IP y puerto de DroidCam
# ip_address = '10.110.62.4'  # Reemplaza con la dirección IP de tu dispositivo Android
# port = '4747'  # Puerto predeterminado de DroidCam

# # URL del video de DroidCam
# url = f'http://{ip_address}:{port}/video'

# # Inicializar el objeto de captura de video
# cap = cv2.VideoCapture(url)

# while True:
#     # Leer un frame del video
#     ret, frame = cap.read()
    
#     if not ret:
#         break
    
#     # Procesar el frame y aplicar técnicas de realidad aumentada
#     # ...
    
#     # Mostrar el frame procesado
#     cv2.imshow('Realidad Aumentada', frame)
    
#     # Salir del bucle si se presiona la tecla 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Liberar los recursos
# cap.release()
# cv2.destroyAllWindows()

import cv2
import subprocess

# Establecer la conexión ADB con el dispositivo móvil
adb_command = "adb forward tcp:4747 tcp:4747"
subprocess.call(adb_command.split())

# URL del video de la cámara del dispositivo móvil a través de ADB
url = "http://localhost:4747/video"

# Inicializar el objeto de captura de video con la URL de la cámara del dispositivo móvil
cap = cv2.VideoCapture(url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    # Leer un frame del video
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Procesar el frame y aplicar técnicas de realidad aumentada
    # ...
    
    # Mostrar el frame procesado
    cv2.imshow('Realidad Aumentada', frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()