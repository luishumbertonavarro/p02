from abc import ABC, abstractmethod

import cv2
# import time
import datetime
import pyautogui
# import tkinter as tk
import numpy as np
import mediapipe as mp
# import matplotlib.pyplot as plt
import os
# import pyvirtualcam
# from numpy.ma import count
import PySimpleGUI as sg

from reconocimiento import ReconocimientoVideo

if __name__ == '__main__':
    sg.theme('DarkAmber')  # Add a touch of color
    a = ReconocimientoVideo



    def segundo_frame():
        window.close()
        sg.theme('DarkAmber')
        layout_opencv = [[sg.Text('', size=(40, 1), justification='center', font='Helvetica 20')],
                         [sg.Image(filename='', key='image')],
                         [sg.Button('Cerrar', size=(10, 1), font='Helvetica 14'), ]]
        layout_opencv_window = sg.Window('OpenCV con pysimplegui', layout_opencv, resizable=True)
        cap = cv2.VideoCapture(1)
        contador = 0

        recording = True
        while cap.isOpened():
            ok, frame = cap.read()
            filter_on = False
            if not ok:
                continue

            event, values = layout_opencv_window.read(timeout=20)
            if event == sg.WIN_CLOSED or event == 'Cerrar':  # if user closes window or clicks cancel
                break
            if recording:
                ret, frame = cap.read()
                imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                layout_opencv_window['image'].update(data=imgbytes)
                contador = contador + 1
        layout_opencv_window.close()

layout = [[sg.Text('Seleccione el gesto para la captura:')],
          [sg.Combo(['HighFive', 'spiderman', 'V'], default_value='Seleccione un gesto', size=(19, 1))],
          [sg.Text("Seleccione una carpeta para guardar: ")],
          [sg.In(enable_events=True, key='File_Path'),
           sg.FolderBrowse()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Programita', layout, resizable=True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == 'File_Path':
        direccion = values["File_Path"]
        print(values['File_Path'])
    elif values['File_Path'] != "":
        segundo_frame()



    # elif event==
    print('You entered ', values[0], values["File_Path"])

window.close()
"""a = DeteccionGestos()
b = OperacionesBasicas()

mp_manos = mp.solutions.hands

manos = mp_manos.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
manos_videos = mp_manos.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

mp_dibujo = mp.solutions.drawing_utils
camera_video = cv2.VideoCapture(1)
camera_video.set(3, 1280)
camera_video.set(4, 960)
contador = 0
usuarioWindows = os.getenv('username')

direccion = 'c:/Users/' + usuarioWindows + '/desktop/Capturas/'
existe = os.path.exists(direccion)
if not existe:
    os.makedirs(direccion)
cv2.namedWindow('ScreenShot', cv2.WINDOW_NORMAL)
num_of_frames = 5
counter = {'HIGH-FIVE SIGN': 0}
captured_image = None
while camera_video.isOpened():
    contador = contador + 1

    ok, frame = camera_video.read()
    filter_on = False
    if not ok:
        continue
    frame = cv2.flip(frame, 1)
    frame, results = a.detectar_puntos_manos(frame, manos_videos, display=False)
    if results.multi_hand_landmarks:
        frame, estado_dedos, count = a.contar_dedos(frame, results, display=False)

        _, hand_gestures = b.reconocimiento_gestos(frame, estado_dedos, count, dibujo=False, display=False)

        if results.multi_hand_landmarks and any(
                hand_gestures == "HIGH-FIVE SIGN" for hand_gestures in hand_gestures.values()):
            counter['HIGH-FIVE SIGN'] += 1
            if counter['HIGH-FIVE SIGN'] == num_of_frames:
                filter_on = True
                counter['HIGH-FIVE SIGN'] = 0
    cv2.imshow('ScreenShot', frame)
    if filter_on:
        e = str(datetime.datetime.now())
        f = e.replace(":", "")
        g = f.replace(".", "")
        h = g.replace(" ", "")
        pyautogui.screenshot(direccion + h + '.png')

    k = cv2.waitKey(1) & 0xFF
"""
# a = OperacionesBasicas()
# a.check_multiple()
