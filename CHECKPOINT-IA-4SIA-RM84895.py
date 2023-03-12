import cv2
import numpy as np
from pynput.keyboard import Key, Controller
import pynput
import time
import random
import os,sys, os.path

keys = [ 
    #Key.up,                                 # UP
    #Key.down,                               # DOWN
    pynput.keyboard.KeyCode.from_char('A'),   # LEFT
    pynput.keyboard.KeyCode.from_char('D'),   # RIGHT
    pynput.keyboard.KeyCode.from_char('S'),  # A
    pynput.keyboard.KeyCode.from_char('W'),  # B
    #Key.enter,                              # START
    #Key.shift_r,                            # SELECT
]

keyboard = Controller()


# Lowers e Uppers do verde e do rosa
verde_lower = (29, 86, 6)
verde_upper = (64, 255, 255)
rosa_lower = (150, 80, 80)
rosa_upper = (180, 255, 255)


capturaVideo = cv2.VideoCapture(1)


while True:
    ret, frame = capturaVideo.read() 

    if not ret:  # ???????
        break 


    bgr2hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 


    mascaraVerde = cv2.inRange(bgr2hsv, verde_lower, verde_upper)
    mascaraRosa = cv2.inRange(bgr2hsv, rosa_lower, rosa_upper)

    # Mascara Final = verde+rosa
    mascaraFinal = cv2.bitwise_or(mascaraVerde, mascaraRosa)


    # Achar Contornos
    contornoVerde, _ = cv2.findContours(mascaraVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornoRosa, _ = cv2.findContours(mascaraRosa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Contorno Verde
    if len(contornoVerde) > 0:
        # Maior area
        contornoMaxVerde = max(contornoVerde, key=cv2.contourArea)
        cv2.drawContours(frame, [contornoMaxVerde], -1, (0, 255, 0), 2)

        # Centro de Massa Verde
        moments = cv2.moments(contornoMaxVerde)
        if moments["m00"] != 0:
            cx_verde = int(moments["m10"] / moments["m00"])
            cy_verde = int(moments["m01"] / moments["m00"])
            cv2.circle(frame, (cx_verde, cy_verde), 5, (0, 255, 0), -1)


    #Contorno Rosa
    if len(contornoRosa) > 0:
        contornoMaxRosa = max(contornoRosa, key=cv2.contourArea)
        cv2.drawContours(frame, [contornoMaxRosa], -1, (255, 0, 255), 2)

        #Centro de Massa Rosa
        moments = cv2.moments(contornoMaxRosa)
        if moments["m00"] != 0:
            cx_rosa = int(moments["m10"] / moments["m00"])
            cy_rosa = int(moments["m01"] / moments["m00"])
            cv2.circle(frame, (cx_rosa, cy_rosa), 5, (255, 0, 255), -1)


    # Linha entre os centros
    if len(contornoVerde) > 0 and len(contornoRosa) > 0:
        cv2.line(frame, (cx_verde, cy_verde), (cx_rosa, cy_rosa), (255, 255, 255), 2)


    #colocar no centro da tela
    altura, largura, _ = frame.shape
    distanciaX = cx_rosa - cx_verde
    distanciaY = cy_rosa - cy_verde
    angulo = str( (np.arctan2(distanciaY, distanciaX) * 180 / np.pi) - 180 )

    fonte = cv2.FONT_HERSHEY_SIMPLEX

    tamanhoAngulo = cv2.getTextSize(angulo, fonte, 1, 2)[0]
    textoAnguloX = int((largura - tamanhoAngulo[0]) / 2)
    textoAnguloY = int((altura - tamanhoAngulo[1]) / 2)

    cv2.putText(frame, angulo, (textoAnguloX, textoAnguloY), fonte, 1, (0, 255, 0), 2)

     

    
    cv2.imshow('frame', frame)


    # Sair com Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capturaVideo.release()
cv2.destroyAllWindows()


