import PySimpleGUI as sg
import cv2
from reconocimiento import ReconocimientoVideo
from strategy import CapturarPantallaStrategyAccion
from PIL import Image
#from principal import Principal
import datetime
from datosDB import DATADB

class Interfaz:

    sg.theme('DarkAmber')
    __accion = CapturarPantallaStrategyAccion()
    __reconocimiento = ReconocimientoVideo(__accion)
    llave_gesto = None
    menssaje=None
    file = DATADB()
    font = ("Arial", 20)
    def principal(self):
        def cargar_layout():
            return [
                [sg.Text(self.menssaje, key="txtCombo", font=self.font)],
                [sg.Text('Seleccione el gesto para la captura:', key="txtCombo")],
                [
                    sg.Button(image_source=gesto.img_referencia, button_color='white',
                              key='btnGesto-' + gesto.nombre_gesto)
                    for gesto in self.__reconocimiento.gestos_
                ],

                [sg.Text(key='gestoSeleccionado', text_color='white')],
                [sg.Text(key='errorGesto', text_color='red')],
                [sg.Text("Seleccione una carpeta para guardar: ")],
                [sg.In(enable_events=True, key='File_Path'), sg.FolderBrowse('Buscar')],
                [sg.Text(key='errorFolder', text_color='red')],
                [sg.Button('Ok',size=(10, 2)), sg.Button('Cancel',size=(10, 2))],
                [sg.Text('Agregar nuevo gesto', key="txtAdd"),
                 sg.Button(image_source='recursos/plus.png', image_size=(50, 50), button_color=("white", "#E7C829"),
                           key="btnAddWindow")],
                [sg.Button('Cerrar Sesion',size=(10, 2))],
            ]

        result = self.file.obtener_session_activa()
        if not result:
            exit()
        self.menssaje = 'Hola '+str(result[1])
        # Create the Window
        window = sg.Window('Reconocimiento de gestos', cargar_layout(), resizable=True, size=(900, 600))
        # Event Loop to process "events" and get the "values" of the inputs
        self.llave_gesto = None
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                window.close()
                break
            elif event == "Cerrar":
                self.file.cerrar_session()
                #break
                window.close()
                principal = Principal()
                principal.login()
            if '-' in event:
                gesto_seleccionado = event.split("-")
                if gesto_seleccionado[0].startswith('btnGesto'):
                    self.llave_gesto = gesto_seleccionado[0] + "-" + gesto_seleccionado[1]
            if event == self.llave_gesto:
                [
                    window[f'btnGesto-{gesto.nombre_gesto}'].update(button_color='white')
                    for gesto in self.__reconocimiento.gestos_
                ]
                window[self.llave_gesto].update(button_color='#E7C829')


            elif event == 'File_Path':
                self.__reconocimiento.cambiar_ruta_guardado_captura(values["File_Path"])

            elif event == "btnAddWindow":
                self.nuevo_gesto(window)

            elif values['File_Path'] == "":
                window['errorFolder'].update('Por favor seleccione una ubicacion para guardar el archivo')

            elif event == "Ok" and self.llave_gesto is not None and values['File_Path'] != '':
                self.__reconocimiento.cambiar_valor_gesto(self.llave_gesto.split('-')[1])
                self.abrir_recon(window)


        window.close()

    def nuevo_gesto(self, parent_window=None):
        dedos_seleccionar = ['Pulgar', 'Indice', 'Medio', 'Anular', 'Meñique']

        def cargar_layout():
            return [
                [sg.Text('Seleccione los dedos para el nuevo gesto:', key="txtCombo")],
                [sg.Checkbox(dedoscheckbox, default=True, key=dedoscheckbox) for dedoscheckbox in dedos_seleccionar],
                [sg.Button('Seleccionar todos'), sg.Button('Desmarcar todos')],
                [sg.Text('Sube una imagen de guia para el gesto'), sg.Input(),
                 sg.FileBrowse(file_types=(("png files", "*.png"),))],
                [sg.Image(size=(50, 50), key='image')],
                [sg.Button('Ok'), sg.Button('Cancel')]
            ]

        # Create the Window
        window = sg.Window('Reconocimiento de gestos', cargar_layout(), resizable=True)
        # Event Loop to process "events" and get the "values" of the inputs
        self.llave_gesto = None
        while True:
            event, values = window.read()
            if event == 'Ok':
                if values[0] and values[0].endswith('.png'):
                    try:
                        # Open the image and convert it to 50x50 pixels
                        image = Image.open(values[0])
                        image = image.resize((50, 50))
                        # Save the image to a temporary file
                        temp_file = 'temp.png'
                        image.save(temp_file)
                        # Update the image element with the resized image
                        sg_image = sg.Image(temp_file, size=(50, 50))
                        window['image'].update(temp_file)
                    except Exception as e:
                        sg.popup_error(str(e))
                else:
                    sg.popup_error('Please select a PNG image')

            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break

            if event == self.llave_gesto:
                [
                    window[f'btnGesto-{gesto.nombre_gesto}'].update(button_color='white')
                    for gesto in self.__reconocimiento.gestos_
                ]
                window[self.llave_gesto].update(button_color='#E7C829')

            elif event == 'Seleccionar todos':
                for dedoscheckbox in dedos_seleccionar:
                    window[dedoscheckbox].update(True)

            elif event == 'Desmarcar todos':
                for dedoscheckbox in dedos_seleccionar:
                    window[dedoscheckbox].update(False)



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
