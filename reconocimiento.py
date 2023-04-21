import datetime
import os
from abc import ABC, abstractmethod
import cv2
import mediapipe as mp
from matplotlib import pyplot as plt

from gestos import GestoClass
from enums import GestosEnum, DEDOSENUM
from strategy import AccionEstrategia
from datosDB import DATADB


class ReconocimientoI(ABC):
    file = DATADB()

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
    gestos_ = []

    def __init__(self, accion_estrategia: AccionEstrategia):
        self.gestos_ = []
        super().__init__()
        self.accion_estrategia = accion_estrategia
        self.filter_on = None
        self.camera_video = None
        self.contador = 0
        self.direccion = 'c:/Users/' + self.usuarioWindows + '/desktop/Capturas/'
        self.num_of_frames = 5
        self.captured_image = None
        self.input_frame = None
        self.output_image = None
        self.gesto = GestosEnum.PALMA_ABIERTA.value
        self.cargar_gestos_predeterminados()
        if not os.path.exists(self.direccion):
            os.makedirs(self.direccion)

    def crear_gesto(self, nuevo_gesto: GestoClass):

        self.gestos_.append(nuevo_gesto)

    def cambiar_valor_gesto(self, nuevo_gesto: str):
        self.gesto = nuevo_gesto

    def cargar_gestos_predeterminados(self):
        peace_sign = GestoClass(
            'PAZ',
            [DEDOSENUM.INDEX.value, DEDOSENUM.MIDDLE.value],
            r"./recursos/PAZ.png"
        )
        spiderman_sign = GestoClass(
            'SPIDERMAN',
            [DEDOSENUM.PINKY.value, DEDOSENUM.INDEX.value, DEDOSENUM.THUMB.value],
            r"./recursos/SPIDERMAN.png"
        )
        palma_abierta = GestoClass(
            'PALMA_ABIERTA',
            [DEDOSENUM.PINKY.value, DEDOSENUM.INDEX.value, DEDOSENUM.THUMB.value, DEDOSENUM.RING.value,
             DEDOSENUM.MIDDLE.value],
            r"./recursos/PALMA_ABIERTA.png"
        )

        self.gestos_.append(spiderman_sign)
        self.gestos_.append(peace_sign)
        self.gestos_.append(palma_abierta)

        user = self.file.obtener_session_activa()
        if user:
            result = self.file.obtener_gestos(user[0])
            migesto = None
            for gesto in result:
                migesto = GestoClass(
                    gesto[1],
                    self.obtener_dedos_data(gesto[4],gesto[5],gesto[6],gesto[7],gesto[8]),
                    gesto[2]
                )
                self.gestos_.append(migesto)
        print("")

    def obtener_dedos_data(self,t,i,m,r,p):
        dedos = []
        if t:
            dedos.append('THUMB')
        if i:
            dedos.append('INDEX')
        if m:
            dedos.append('MIDDLE')
        if r:
            dedos.append('RING')
        if p:
            dedos.append('PINKY')
        return dedos

    def crear_carpeta_por_hora(self):
        tiempo_actual = datetime.datetime.now()
        ruta = f'clase del {tiempo_actual.day} de {tiempo_actual.month} de {tiempo_actual.year} hora {tiempo_actual.hour}/'
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
                    landmark_drawing_spec=self.mp_dibujo.DrawingSpec(
                        color=(255, 255, 255), thickness=2, circle_radius=2
                    ),
                    connection_drawing_spec=self.mp_dibujo.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )
        if display:
            self.mostrar_imagen(imagen=self.input_frame, imagen_salida=self.output_image)
        else:
            return results

    def contar_dedos(self, results, dibujo=False, display=True):
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

            if (etiqueta_mano == 'Right' and (pulgar_punta_x < pulgar_mcp_x)) or \
                    (etiqueta_mano == 'Left' and (pulgar_punta_x > pulgar_mcp_x)):
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

        gestos_manos = {'RIGHT': "UNKNOWN", 'LEFT': "UNKNOWN"}

        for gesto_obj in self.gestos_:
            gesto_obj.gesto_hecho(estados_dedos, gestos_manos)

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
        self.camera_video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.camera_video.set(3, 1280)
        self.camera_video.set(4, 720)

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
                self.filter_on = True

    def cerrar_ventanas(self):
        self.camera_video.release()
        cv2.destroyAllWindows()