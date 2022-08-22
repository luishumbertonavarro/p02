from abc import ABC, abstractmethod

import cv2
import time
import datetime
import pyautogui
import tkinter as tk
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
import os
import pyvirtualcam
from numpy.ma import count


def plt_meth(imagen_salida, imagen=None):
    """
    Esta funcion bvlalbalbabla
    :param
        -imagen_salida(ImageBuffer): resultado
        -image(ImageBuffer): imagen en bruto
    """

    plt.figure(figsize=[15, 15])
    plt.subplot(121)
    if imagen:
        plt.imshow(imagen[:, :, ::-1])
        plt.title("Imagen Original")

    plt.axis('off')
    plt.subplot(122)
    plt.imshow(imagen_salida[:, :, ::-1])
    plt.title("Salida")
    plt.axis('off')


class Abstracta(ABC):

    @abstractmethod
    def metodo_uno(self):
        pass


class DeteccionGestos(Abstracta):
    def __init__(self):
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
        self.manos_videos = self.mp_manos.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_dibujo = mp.solutions.drawing_utils

    def detectarPuntosManos(self, imagen, mano, dibujo=True, display=True):
        def draw(hand_landmarks):
            if hand_landmarks is None:
                return
            landmark_drawing = self.mp_dibujo.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
            connection_drawing = self.mp_dibujo.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
            self.mp_dibujo.draw_landmarks(
                imagen_salida, landmark_list=hand_landmarks, connections=self.mp_manos.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_drawing,
                connection_drawing_spec=connection_drawing
            )

        if imagen is None:
            return
        imagen_salida = imagen.copy()
        imgRGB = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        results = mano.process(imgRGB)
        if results.multi_hand_landmarks and dibujo:
            for hand_landmarks in results.multi_hand_landmarks:
                draw(hand_landmarks)
        if display:
            plt_meth(imagen_salida, imagen)
        else:
            return imagen_salida, results

    def contarDedos(self, imagen, results, dibujo=True, display=True):
        altura, ancho, _ = imagen.shape
        if imagen is None:
            return
        imagen_salida = imagen.copy()
        count = {'RIGHT': 0, 'LEFT': 0}
        punta_dedos_ids = [self.mp_manos.HandLandmark.INDEX_FINGER_TIP, self.mp_manos.HandLandmark.MIDDLE_FINGER_TIP,
                           self.mp_manos.HandLandmark.RING_FINGER_TIP, self.mp_manos.HandLandmark.PINKY_TIP]

        estado_dedos = {'PULGAR_DERECHO': False, 'INDICE_DERECHO': False, 'MEDIO_DERECHO': False,
                        'ANULAR_DERECHO': False,
                        'MENIQUE_DERCHO': False, 'PULGAR_IZQUIERDO': False, 'INDICE_IZQUIERDO': False,
                        'MEDIO_IZQUIERDO': False,
                        'ANULAR_IZQUIERDO': False, 'MENIQUE_IZQUIERDO': False}

        for index_mano, mano_info in enumerate(results.multi_handedness):

            etiqueta_mano = mano_info.classification[0].label
            etiqueta_marcas = results.multi_hand_landmarks[index_mano]

            for punta_indice in punta_dedos_ids:

                nombre_dedo = punta_indice.name.split("_")[0]

                if etiqueta_marcas.landmark[punta_indice].y < etiqueta_marcas.landmark[punta_indice - 2].y:
                    estado_dedos[etiqueta_mano.upper() + "_" + nombre_dedo] = True

                    count[etiqueta_mano.upper()] += 1

            pulgar_punta_x = etiqueta_marcas.landmark[self.mp_manos.HandLandmark.THUMB_TIP].x
            pulgar_mcp_x = etiqueta_marcas.landmark[self.mp_manos.HandLandmark.THUMB_TIP - 2].x

            if (etiqueta_mano == 'Right' and (pulgar_punta_x < pulgar_mcp_x)) or (
                    etiqueta_mano == 'Left' and (pulgar_punta_x > pulgar_mcp_x)):
                estado_dedos[etiqueta_mano.upper() + "_THUMB"] = True
                count[etiqueta_mano.upper()] += 1

        if dibujo:
            cv2.putText(imagen_salida, "Dedos totales: ", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 255), 2)
            cv2.putText(imagen_salida, str(sum(count.values())), (ancho // 2 - 150, 240), cv2.FONT_HERSHEY_SIMPLEX, 8.9,
                        (20, 255, 155), 10, 10)

        if display:
            plt_meth(imagen_salida)

        else:
            return imagen_salida, estado_dedos, count


class OperacionesBasicas(DeteccionGestos):
    def __init__(self):
        DeteccionGestos.__init__(self)

    def check_cam_by_index(self, i):
        print('entro')
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def check_multiple(self):
        try:
            for i in range(-1, 5):
                print(f'checking camera #{i}')
                self.check_cam_by_index(i)
        except Exception as e:
            print(e)

    def lista(self):
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return print(arr)

    def reconocimiento_gestos(self, image, estados_dedos, contador, dibujo=True, display=True):
        if image is None:
            return
        imagen_salida = image.copy()
        etiqueta_manos = ['RIGHT', 'LEFT']
        gestos_manos = {'RIGHT': "UNKNOWN", 'LEFT': "UNKNOWN"}

        for hand_index, etiqueta_manos in enumerate(etiqueta_manos):
            color = (0, 0, 255)

            if contador[etiqueta_manos] == 2 and estados_dedos[etiqueta_manos + '_MIDDLE'] and estados_dedos[etiqueta_manos + '_INDEX']:
                gestos_manos[etiqueta_manos] = "V SIGN"
                color = (0, 255, 0)
            elif contador[etiqueta_manos] == 3 and estados_dedos[etiqueta_manos + '_THUMB'] and estados_dedos[etiqueta_manos + '_INDEX'] and estados_dedos[etiqueta_manos + '_PINKY']:
                gestos_manos[etiqueta_manos] = "SPIDERMAN SIGN"

            if contador[etiqueta_manos] == 5:
                gestos_manos[etiqueta_manos] = "HIGH-FIVE SIGN"
                color = (0, 255, 0)
            if dibujo:
                cv2.putText(imagen_salida, etiqueta_manos + ': ' + gestos_manos[etiqueta_manos],
                            (10, (hand_index + 1) * 60),
                            cv2.FONT_HERSHEY_PLAIN, 4, color, 5)
        if display:
            plt_meth(imagen_salida)

        else:
            return imagen_salida, gestos_manos


a = OperacionesBasicas()
a.check_multiple()
