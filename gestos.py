class GestoClass:
    dedos = []

    def __init__(
            self, nombre_gesto, dedos
    ):
        self.nombre_gesto = nombre_gesto
        self.dedos = dedos
        self.dedos.sort()

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


