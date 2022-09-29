import PySimpleGUI as sg
import cv2
from reconocimiento import ReconocimientoVideo
from strategy import CapturarPantallaStrategyAccion


class Interfaz:
    sg.theme('DarkAmber')
    __accion = CapturarPantallaStrategyAccion()
    __reconocimiento = ReconocimientoVideo(__accion)
    llave_gesto = ''

    def principal(self):
        def cargar_layout():
            return [
                [sg.Text('Seleccione el gesto para la captura:', key="txtCombo")],
                [
                    sg.Button(image_source=gesto.img_referencia, button_color='white', key='btnGesto-' + gesto.nombre_gesto)
                    for gesto in self.__reconocimiento.gestos_
                ],
                [sg.Text(key='gestoSeleccionado', text_color='white')],
                [
                    sg.Combo(
                        ['PALMA_ABIERTA', 'SPIDERMAN', 'PAZ'], default_value='Seleccione un gesto', size=(19, 1),
                        key='gesto', readonly=True, enable_events=True
                    ),
                    sg.Image(filename='', size=(20, 20), key='gestoImg')
                ],
                [sg.Text(key='errorCombo', text_color='red')],
                [sg.Text("Seleccione una carpeta para guardar: ")],
                [sg.In(enable_events=True, key='File_Path'), sg.FolderBrowse('Buscar')],
                [sg.Text(key='errorFolder', text_color='red')],
                [sg.Button('Ok'), sg.Button('Cancel')]
            ]

        # Create the Window
        window = sg.Window('Reconocimiento de gestos', cargar_layout(), resizable=True)
        # Event Loop to process "events" and get the "values" of the inputs

        while True:
            event, values = window.read()
            gesto_seleccionado = event.split("-")
            if gesto_seleccionado[0].startswith('btnGesto'):
                self.llave_gesto = gesto_seleccionado[0] + "-" + gesto_seleccionado[1]
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            elif event == self.llave_gesto:
                # CREAR UN FOR QUE RECORRA EL OBJ Y CONCATENAR A BTNGESTO CON EL NOMBRE
                [
                    window[f'btnGesto-{gesto.nombre_gesto}'].update(button_color='white')
                    for gesto in self.__reconocimiento.gestos_
                ]
                window[self.llave_gesto].update(button_color='red')
                window['gestoSeleccionado'].update(
                    'Seleccionaste el gesto ' + gesto_seleccionado[1] + ' para la captura de pantalla'
                )
            elif event == 'gesto':
                for gesto in self.__reconocimiento.gestos_:
                    if gesto.nombre_gesto == values['gesto']:
                        window['gestoImg'].update(filename=gesto.img_referencia, size=(50, 50))
                        break
            elif event == 'File_Path':
                self.__reconocimiento.cambiar_ruta_guardado_captura(values["File_Path"])
            elif values['gesto'] == "Seleccione un gesto":
                window['errorCombo'].update('Por favor seleccione un gesto')
            elif values['File_Path'] == "":
                window['errorFolder'].update('Por favor seleccione una ubicacion para guardar el archivo')
            elif values['File_Path'] != "" and event == "Ok" and values['gesto'] != "Seleccione un gesto":
                self.__reconocimiento.cambiar_valor_gesto(gesto_seleccionado[1])
                self.abrir_recon(window)
        window.close()

    def abrir_recon(self, parent_window=None):

        def cargar_layout():
            return [
                [sg.Text('', size=(40, 1), justification='center', font='Helvetica 20')],
                [sg.Image(filename='', key='image')],
                [sg.Button('Cerrar', size=(10, 1), font='Helvetica 14')]
            ]

        if parent_window:
            parent_window.close()

        sg.theme('DarkAmber')
        window = sg.Window('Gestos', cargar_layout(), resizable=True)
        self.__reconocimiento.configurar_camera_video()
        timer = 0
        while self.__reconocimiento.camera_video.isOpened():
            self.__reconocimiento.reconocer()
            if timer % 30 == 0:
                if self.__reconocimiento.filter_on:
                    self.__reconocimiento.accion_estrategia.realizar_accion(direccion=self.__reconocimiento.direccion)
                    self.__reconocimiento.filter_on = False
            event, values = window.read(timeout=20)
            if event == sg.WIN_CLOSED or event == 'Cerrar':  # if user closes window or clicks cancel
                break
            imgbytes = cv2.imencode('.png', self.__reconocimiento.output_image)[1].tobytes()
            window['image'].update(data=imgbytes)
            timer += 1
        self.__reconocimiento.cerrar_ventanas()
        window.close()
        self.principal()
