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

from aux_functions import plt_meth
from deteccion_gestos import DeteccionGestos


class Abstracta(ABC):

    @abstractmethod
    def metodo_uno(self):
        pass


class OperacionesBasicas(DeteccionGestos):

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
            [self.check_cam_by_index(i) for i in range(-1, 5)]
        except Exception as e:
            print(e)

    def lista(self):
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            arr.append(index)
            cap.release()
            index += 1
        return arr

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
