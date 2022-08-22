import cv2
import mediapipe as mp
from aux_functions import plt_meth


class DeteccionGestos:

    def __init__(self):
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
        self.manos_videos = self.mp_manos.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_dibujo = mp.solutions.drawing_utils

    def detectar_puntos_manos(self, imagen, mano, dibujo=True, display=True):
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