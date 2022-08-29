import os

import cv2
import mediapipe as mp
from matplotlib import pyplot as plt


class Reconocimiento:

    def __init__(self):
        self.flipped_image = None
        self.imagen = None
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
        self.manos_videos = self.mp_manos.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_dibujo = mp.solutions.drawing_utils

    def cargar_imagen(self, imagen_path):
        if not isinstance(imagen_path, str):
            raise ValueError('imagen_path debe ser un string')
        if not os.path.exists(imagen_path):
            raise FileNotFoundError('El path no es una ruta valida')
        self.imagen = cv2.imread(imagen_path)
        self.flipped_image = cv2.flip(self.imagen, 1)

    def detectar_puntos_manos(self, dibujar=True, display=True):
        if not self.flipped_image or not self.imagen:
            raise Exception('Primero debe ejecutar el metodo cargar_imagen')
        imagen_salida = self.flipped_image.copy()
        imgRGB = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
        results = self.manos.process(imgRGB)
        if results.multi_hand_landmarks and dibujar:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_dibujo.draw_landmarks(
                    imagen_salida,
                    hand_landmarks,
                    self.mp_manos.HAND_CONNECTIONS,
                    self.mp_dibujo.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                    self.mp_dibujo.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )
        if display:
            self.mostrar_imagen(imagen=self.flipped_image, imagen_salida=imagen_salida)
        else:
            return imagen_salida, results

    def mostrar_imagen(self, **kwargs):
        def plot_image(*args):
            plt.figure(figsize=[15, 15])
            plt.subplot(121)
            plt.imshow(args[1][:, :, ::-1])
            plt.title(f"Imagen {args[0]}")
            plt.axis('off')
        [plot_image(key, value) for key, value in kwargs.items()]

    def contar_dedos(self, results, dibujo=True, display=True):
        if not self.flipped_image or not self.imagen:
            raise Exception('Primero debe ejecutar el metodo cargar_imagen')
        altura, ancho, _ = self.imagen.shape
        imagen_salida = self.imagen.copy()
        count = {'RIGHT': 0, 'LEFT': 0}
        punta_dedos_ids = [
            self.mp_manos.HandLandmark.INDEX_FINGER_TIP, self.mp_manos.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_manos.HandLandmark.RING_FINGER_TIP, self.mp_manos.HandLandmark.PINKY_TIP
        ]

        estado_dedos = {
            'PULGAR_DERECHO': False, 'INDICE_DERECHO': False, 'MEDIO_DERECHO': False, 'ANULAR_DERECHO': False,
            'MENIQUE_DERCHO': False, 'PULGAR_IZQUIERDO': False, 'INDICE_IZQUIERDO': False,
            'MEDIO_IZQUIERDO': False, 'ANULAR_IZQUIERDO': False, 'MENIQUE_IZQUIERDO': False
        }

        for index_mano, mano_info in enumerate(results.multi_handedness):

            etiqueta_mano = mano_info.classification[0].label
            etiqueta_marcas = results.multi_hand_landmarks[index_mano]

            for punta_indice in punta_dedos_ids:
                nombre_dedo = punta_indice.name.split("_")[0]
                if (etiqueta_marcas.landmark[punta_indice].y < etiqueta_marcas.landmark[punta_indice - 2].y):
                    estado_dedos[etiqueta_mano.upper() + "_" + nombre_dedo] = True
                    count[etiqueta_mano.upper()] += 1

            pulgar_punta_x = etiqueta_marcas.landmark[self.mp_manos.HandLandmark.THUMB_TIP].x
            pulgar_mcp_x = etiqueta_marcas.landmark[self.mp_manos.HandLandmark.THUMB_TIP - 2].x

            if (etiqueta_mano == 'Right' and (pulgar_punta_x < pulgar_mcp_x)) or \
                    (etiqueta_mano == 'Left' and (pulgar_punta_x > pulgar_mcp_x)):
                estado_dedos[etiqueta_mano.upper() + "_THUMB"] = True
                count[etiqueta_mano.upper()] += 1
        if dibujo:
            cv2.putText(
                imagen_salida, "Dedos totales: ", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 255), 2
            )
            cv2.putText(
                imagen_salida, str(sum(count.values())), (ancho // 2 - 150, 240), cv2.FONT_HERSHEY_SIMPLEX, 8.9,
                (20, 255, 155), 10, 10
            )

        if display:
            self.mostrar_imagen(imagen_salida=imagen_salida)
        else:
            return imagen_salida, estado_dedos, count

    def reconocimiento_gestos(self, estados_dedos, contador, dibujo=True, display=True):
        if not self.flipped_image or not self.imagen:
            raise Exception('Primero debe ejecutar el metodo cargar_imagen')
        imagen_salida = self.imagen.copy()
        etiqueta_manos = ['RIGHT', 'LEFT']
        gestos_manos = {'RIGHT': "UNKNOWN", 'LEFT': "UNKOWN"}
        for hand_index, etiqueta_manos in enumerate(etiqueta_manos):
            color = (0, 0, 255)
            if contador[etiqueta_manos] == 2 and estados_dedos[etiqueta_manos + '_MIDDLE'] and \
                    estados_dedos[etiqueta_manos + '_INDEX']:
                gestos_manos[etiqueta_manos] = "V SIGN"
                color = (0, 255, 0)
            elif contador[etiqueta_manos] == 3 and estados_dedos[etiqueta_manos + '_THUMB'] and \
                    estados_dedos[etiqueta_manos + '_INDEX'] and estados_dedos[etiqueta_manos + '_PINKY']:
                gestos_manos[etiqueta_manos] = "SPIDERMAN SIGN"

            if contador[etiqueta_manos] == 5:
                gestos_manos[etiqueta_manos] = "HIGH-FIVE SIGN"
                color = (0, 255, 0)

            if dibujo:
                cv2.putText(
                    imagen_salida, etiqueta_manos + ': ' + gestos_manos[etiqueta_manos],
                    (10, (hand_index + 1) * 60), cv2.FONT_HERSHEY_PLAIN, 4, color, 5
                )

        if display:
            self.mostrar_imagen(imagen_salida=imagen_salida)
        else:
            return imagen_salida, gestos_manos

    def Reconocimiento_imagen(self, imagen_path: str):
        if not imagen_path:
            return
        self.cargar_imagen(imagen_path)
        _, results = self.detectar_puntos_manos(display=False)
        if results.multi_hand_landmarks:
            output_image, fingers_statuses, contador = self.contar_dedos(results, dibujo=False, display=False)
            self.reconocimiento_gestos(fingers_statuses, contador)
