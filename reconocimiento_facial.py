import os
import pathlib
import cv2
import numpy as np
import cuia

h, w, _ = oscars.shape
detector = cv2.FaceDetectorYN.create("dnn/face_detection_yunet_2023mar.onnx", config="", input_size=(w,h),  score_threshold=0.7)
ret, caras = detector.detect(oscars)
imagen = oscars.copy()
if ret:
    for cara in caras:
        c = cara.astype(int)
        cv2.rectangle(imagen, (c[0],c[1]), (c[0]+c[2],c[1]+c[3]), (0,255,0), 3)
        cv2.circle(imagen, (c[4],c[5]), 10, (255,0,0), -1)
        cv2.circle(imagen, (c[6],c[7]), 10, (255,0,0), -1)
        cv2.circle(imagen, (c[8],c[9]), 10, (0,0,255), -1)
        cv2.line(imagen, (c[10],c[11]), (c[12],c[13]), (255,255,0), 10)
        cv2.putText(imagen, str(round(100*cara[14])), (c[0],c[1]+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
cuia.plot(imagen)

famosos = []
lista = os.listdir("media/Famosos/")
for f in lista:
    nombre = pathlib.Path(f).stem    
    img = cv2.imread(f'media/Famosos/{f}')
    h, w, _ = img.shape
    detector.setInputSize((w,h))
    ret, caranueva = detector.detect(img)
    if ret:
        caracrop = fr.alignCrop(img, caranueva[0]) # Solo tomo la primera cara encontrada
        codcara = fr.feature(caracrop)
        famosos.append((nombre, codcara))

imagen = oscars.copy()
for cara in caras:
    c = cara.astype(int)
    caracrop = fr.alignCrop(oscars, cara)
    codcara = fr.feature(caracrop)
    maximo = -999
    nombre = "Desconocido"
    for i in range(len(famosos)):
        semejanza = fr.match(famosos[i][1], codcara, cv2.FaceRecognizerSF_FR_COSINE)
        if semejanza > maximo:
            maximo = semejanza
            nombre = famosos[i][0]
    if maximo < 0.4: # Si la semejanza es muy baja pongo recuadro rojo e indico la mejor coincidencia
        cv2.rectangle(imagen, (c[0],c[1]), (c[0]+c[2],c[1]+c[3]), (0, 0, 255), 3)
        cv2.putText(imagen, nombre+"?", (c[0],c[1]+25), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA)
    else: # Si la mejor coincidencia es buena entonces recuadro verde y nombre en grande
        cv2.rectangle(imagen, (c[0],c[1]), (c[0]+c[2],c[1]+c[3]), (0, 255, 0), 3)
        cv2.putText(imagen, nombre, (c[0],c[1]+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        
cuia.plot(imagen) 