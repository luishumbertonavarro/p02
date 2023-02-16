import os

from PIL import Image


class GestoClass:
    dedos = []

    def __init__(
            self, nombre_gesto, dedos, img
    ):
        self.nombre_gesto = nombre_gesto
        self.dedos = dedos
        self.dedos.sort()
        try:
            picture = Image.open(img)
            path = os.path.join(os.getcwd(), 'images')
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join(path, f'{nombre_gesto}.png')
            picture.save(path)
            self.img_referencia = path
        except Exception as e:
            print(e)

    def gesto_hecho(self, dedos_detectados, gestos_manos):
        mano_izquierda = [
            dedo.split('_')[1] for dedo, value in dedos_detectados.items() if dedo.startswith('LEFT_') and value
        ]
        mano_izquierda.sort()
        if self.dedos == mano_izquierda:
            gestos_manos['LEFT'] = self.nombre_gesto

        mano_derecha = [
            dedo.split('_')[1] for dedo, value in dedos_detectados.items() if dedo.startswith('RIGHT_') and value
        ]
        mano_derecha.sort()
        if self.dedos == mano_derecha:
            gestos_manos['RIGHT'] = self.nombre_gesto

    def __str__(self):
        return self.nombre_gesto

