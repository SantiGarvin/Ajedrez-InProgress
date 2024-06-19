import cv2
import numpy as np
import cuia
import camara

def proyeccion(puntos, rvec, tvec, cameraMatrix, distCoeffs):
    if isinstance(puntos, list):
        return(proyeccion(np.array(puntos, dtype=np.float32), rvec, tvec, cameraMatrix, distCoeffs))
    if isinstance(puntos, np.ndarray):
        if puntos.ndim == 1 and puntos.size == 3:
            res, _ = cv2.projectPoints(puntos.astype(np.float32), rvec, tvec, cameraMatrix, distCoeffs)
            return(res[0][0].astype(int))
        if puntos.ndim > 1:
            aux = proyeccion(puntos[0], rvec, tvec, cameraMatrix, distCoeffs)
            aux = np.expand_dims(aux, axis=0)
            for p in puntos[1:]:
                aux = np.append(aux, [proyeccion(p, rvec, tvec, cameraMatrix, distCoeffs)], axis=0)
            return(np.array(aux))

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
detector = cv2.aruco.ArucoDetector(diccionario)

cam = 0
bk = cuia.bestBackend(cam)
ar = cuia.myVideo(cam, bk)

def ajedrez_ar(frame):
    tam = 0.05  # Tamaño (en metros) del lado del marcador
    bboxs, ids, _ = detector.detectMarkers(frame)
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(bboxs, tam, camara.cameraMatrix, camara.distCoeffs)
    if rvecs is not None:
        for i in range(len(rvecs)):
            # Dibujar el tablero de ajedrez virtual
            tablero = np.zeros((800, 800, 4), dtype=np.uint8)
            tablero[:] = (128, 128, 128, 255)
            for j in range(8):
                for k in range(8):
                    if (j + k) % 2 == 0:
                        tablero[j*100:(j+1)*100, k*100:(k+1)*100] = (255, 255, 255, 255)
            
            # Proyectar el tablero de ajedrez virtual sobre el marcador
            origen = np.array([[0, 0], [800, 0], [800, 800], [0, 800]])
            destino = proyeccion(np.array([[-tam/2, -tam/2, 0], [tam/2, -tam/2, 0], [tam/2, tam/2, 0], [-tam/2, tam/2, 0]]), rvecs[i], tvecs[i], camara.cameraMatrix, camara.distCoeffs)
            M = cv2.getPerspectiveTransform(np.float32(origen), np.float32(destino))
            hframe, wframe, _ = frame.shape
            warp = cv2.warpPerspective(tablero, M, dsize=(wframe, hframe))
            frame = cuia.alphaBlending(warp, frame)
    
    return frame

ar.process = ajedrez_ar
ar.play("Ajedrez AR", key=ord(' '))
ar.release()