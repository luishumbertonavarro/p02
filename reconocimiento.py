import datetime
import os
from abc import ABC, abstractmethod

import cv2
import mediapipe as mp
import pyautogui
from matplotlib import pyplot as plt

from gestos_enum import GestosEnum


class ReconocimientoI(ABC):

    def __init__(self):
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
        self.manos_videos = self.mp_manos.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_dibujo = mp.solutions.drawing_utils

    @abstractmethod
    def detectar_puntos_manos(self, **kwargs):
        pass

    @abstractmethod
    def contar_dedos(self, **kwargs):
        pass

    @abstractmethod
    def reconocimiento_gestos(self, **kwargs):
        pass

    @abstractmethod
    def reconocer(self, **kwargs):
        pass

    @staticmethod
    def mostrar_imagen(**kwargs):
        def plot_image(*args):
            plt.figure(figsize=[15, 15])
            plt.subplot(121)
            plt.imshow(args[1][:, :, ::-1])
            plt.title(f"Imagen {args[0]}")
            plt.axis('off')

        [plot_image(key, value) for key, value in kwargs.items()]


class ReconocimientoVideo(ReconocimientoI):
    usuarioWindows = os.getenv('username')

    def __init__(self):
        super().__init__()
        self.filter_on = None
        self.camera_video = None
        self.contador = 0
        self.direccion = 'c:/Users/' + self.usuarioWindows + '/desktop/Capturas/'
        self.num_of_frames = 5
        self.counter = {
            GestosEnum.PALMA_ABIERTA.value: 0, GestosEnum.SPIDERMAN.value: 0,  GestosEnum.PAZ.value: 0
        }
        self.captured_image = None
        self.input_frame = None
        self.output_image = None
        self.gesto = GestosEnum.PALMA_ABIERTA.value
        if not os.path.exists(self.direccion):
            os.makedirs(self.direccion)

    def cambiar_valor_gesto(self, nuevo_gesto: GestosEnum):
        self.gesto = nuevo_gesto.value

    def crear_carpeta_por_hora(self):
        tiempo_actual = datetime.datetime.now()
        ruta = f'clase {tiempo_actual.day} de {tiempo_actual.month} del {tiempo_actual.year} hora {tiempo_actual.hour}/'
        carpetas = self.direccion.split('/')
        if carpetas[-2].startswith('clase'):
            self.direccion = self.direccion[:(self.direccion.rindex('/c') + 1)]
            self.direccion += ruta
        else:
            self.direccion += ruta

        if not os.path.exists(self.direccion):
            os.makedirs(self.direccion)

    def cambiar_ruta_guardado_captura(self, new_path):
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        self.direccion = new_path
        if not str(new_path).endswith('/'):
            self.direccion += '/'

    def detectar_puntos_manos(self, dibujo=True, display=True):
        if self.input_frame is None:
            return
        imgRGB = cv2.cvtColor(self.input_frame, cv2.COLOR_BGR2RGB)
        results = self.manos_videos.process(imgRGB)
        if results.multi_hand_landmarks and dibujo:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_dibujo.draw_landmarks(
                    self.output_image,
                    landmark_list=hand_landmarks,
                    connections=self.mp_manos.HAND_CONNECTIONS,
                    landmark_drawing_spec=self.mp_dibujo.DrawingSpec(color=(255, 255, 255), thickness=2,
                                                                     circle_radius=2),
                    connection_drawing_spec=self.mp_dibujo.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )
        if display:
            self.mostrar_imagen(imagen=self.input_frame, imagen_salida=self.output_image)
        else:
            return results

    def contar_dedos(self, results, dibujo=True, display=True):
        if self.output_image is None:
            return

        altura, ancho, _ = self.output_image.shape
        count = {'RIGHT': 0, 'LEFT': 0}

        punta_dedos_ids = [
            self.mp_manos.HandLandmark.INDEX_FINGER_TIP,
            self.mp_manos.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_manos.HandLandmark.RING_FINGER_TIP,
            self.mp_manos.HandLandmark.PINKY_TIP
        ]

        estado_dedos = {
            'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
            'RIGHT_PINKY': False, 'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
            'LEFT_RING': False, 'LEFT_PINKY': False
        }

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
            cv2.putText(
                self.output_image, "Dedos totales: ", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 255), 2
            )
            cv2.putText(
                self.output_image, str(sum(count.values())), (ancho // 2 - 150, 240), cv2.FONT_HERSHEY_SIMPLEX, 8.9,
                (20, 255, 155), 10, 10
            )

        if display:
            self.mostrar_imagen(imagen_salida=self.output_image)
        else:
            return estado_dedos, count

    def reconocimiento_gestos(self, estados_dedos, contador, dibujo=True, display=True):
        if self.output_image is None:
            return

        etiqueta_manos = ['RIGHT', 'LEFT']
        gestos_manos = {'RIGHT': "UNKNOWN", 'LEFT': "UNKOWN"}

        for hand_index, etiqueta_manos in enumerate(etiqueta_manos):
            color = (0, 0, 255)

            if contador[etiqueta_manos] == 2 and estados_dedos[etiqueta_manos + '_MIDDLE'] and estados_dedos[
                etiqueta_manos + '_INDEX']:
                gestos_manos[etiqueta_manos] = GestosEnum.PAZ.value
                color = (0, 255, 0)

            if contador[etiqueta_manos] == 3 and estados_dedos[etiqueta_manos + '_THUMB'] and estados_dedos[
                etiqueta_manos + '_INDEX'] and estados_dedos[etiqueta_manos + '_PINKY']:
                gestos_manos[etiqueta_manos] = GestosEnum.SPIDERMAN.value

            if contador[etiqueta_manos] == 5:
                gestos_manos[etiqueta_manos] = GestosEnum.PALMA_ABIERTA.value
                color = (0, 255, 0)

            if dibujo:
                cv2.putText(
                    self.output_image, etiqueta_manos + ': ' + gestos_manos[etiqueta_manos],
                    (10, (hand_index + 1) * 60), cv2.FONT_HERSHEY_PLAIN, 4, color, 5
                )
        if display:
            self.mostrar_imagen(imagen_salida=self.output_image)
        else:
            return gestos_manos

    def obtener_frame(self):
        ok, frame = self.camera_video.read()
        if ok:
            self.input_frame = cv2.flip(frame, 1)
            self.output_image = self.input_frame.copy()
        return ok

    def configurar_camera_video(self):
        self.camera_video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.camera_video.set(3, 1280)
        self.camera_video.set(4, 960)

    def reconocer(self):
        self.crear_carpeta_por_hora()
        self.contador += 1
        self.filter_on = False

        if not self.obtener_frame():
            return

        results = self.detectar_puntos_manos(display=False)

        if results.multi_hand_landmarks:

            estado_dedos, count = self.contar_dedos(results, display=False)
            hand_gestures = self.reconocimiento_gestos(estado_dedos, count, dibujo=False, display=False)
            if results.multi_hand_landmarks and any(
                    hand_gestures == self.gesto for hand_gestures in hand_gestures.values()
            ):
                self.counter[self.gesto] += 1
                self.filter_on = True

    def capturar_pantalla(self):
        if self.filter_on:
            e = str(datetime.datetime.now())
            f = e.replace(":", "")
            g = f.replace(".", "")
            h = g.replace(" ", "")
            pyautogui.screenshot(self.direccion + h + '.png')
            self.filter_on = False

    def cerrar_ventanas(self):
        self.camera_video.release()
        cv2.destroyAllWindows()
