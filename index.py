import cv2
import mediapipe as mp
import numpy as np
from encontra_coordenadas import encontra_coordenadas_maos
from utils.dedos_levantados import dedos_levantados

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (255, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (0, 0, 255)
AZUL_CLARO = (255, 255, 0)

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils
maos = mp_maos.Hands()

resolucao_x = 1280
resolucao_y = 720
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucao_y)

img_quadro = np.ones((resolucao_y, resolucao_x, 3), np.uint8)*255
cor_pincel = (255, 0, 0)
espessura_pincel = 7
x_quadro, y_quadro = 0, 0

while True:
    sucesso, img = camera.read()
    img = cv2.flip(img, 1)

    img, todas_maos = encontra_coordenadas_maos(img, maos, mp_desenho, mp_maos)

    if len(todas_maos) == 2:
        info_dedos_mao1 = dedos_levantados(todas_maos[0])
        info_dedos_mao2 = dedos_levantados(todas_maos[1])

        indicador_x, indicador_y, indicador_z = todas_maos[0]['coordenadas'][8]

        if sum(info_dedos_mao2) == 1:
            cor_pincel = AZUL
        elif sum(info_dedos_mao2) == 2:
            cor_pincel = VERDE
        elif sum(info_dedos_mao2) == 3:
            cor_pincel = VERMELHO
        elif sum(info_dedos_mao2) == 4:
            cor_pincel = BRANCO
        else:
            img_quadro = np.ones((resolucao_y, resolucao_x, 3), np.uint8)*255
     

        espessura_pincel = int(abs(indicador_z))//3+5

        cv2.circle(img, (indicador_x, indicador_y),
                   espessura_pincel, cor_pincel, cv2.FILLED)

        if info_dedos_mao1 == [1, 0, 0, 0]:
            if x_quadro == 0 and y_quadro == 0:
                x_quadro, y_quadro = indicador_x, indicador_y

            cv2.line(img_quadro, (x_quadro, y_quadro),
                     (indicador_x, indicador_y), cor_pincel, espessura_pincel)

            x_quadro, y_quadro = indicador_x, indicador_y
        else:
            x_quadro, y_quadro = 0, 0

        #print(cv2.addW(img, 1, img_quadro, 0.2, 0))
        # img = cv2.addWeighted(img, 1, img_quadro, 0.2, 0)

    cv2.imshow("Imagem", img)
    cv2.imshow('Quadro', img_quadro)
    tecla = cv2.waitKey(1)
    if tecla == 27:
        break


cv2.imwrite('quadro.png', img_quadro)
