import PySimpleGUI as sg

from reconocimiento import ReconocimientoVideo


class Interfaz:
    sg.theme('DarkAmber')

    def __init__(self):
        self.layout = None

    def __cargar_layout(self):
        self.layout = [
            [sg.Text('Seleccione el gesto para la captura:')],
            [sg.Combo(['HighFive', 'spiderman', 'V'], default_value=0, size=(19, 1), key='gesto')],
            [sg.Text("Seleccione una carpeta para guardar: ")],
            [sg.In(enable_events=True, key='File_Path'), sg.FolderBrowse()],
            [sg.Button('Ok'), sg.Button('Cancel')]
        ]
    
    def generar_ventana(self):
        self.__cargar_layout()
        # Create the Window
        window = sg.Window('Reconocimiento de gestos', self.layout, resizable=True)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                video = ReconocimientoVideo()
                if values['gesto'] == 'HighFive':
                    video.reconocer('HIGH-FIVE SIGN')
                elif values['gesto'] == 'spiderman':
                    video.reconocer('SPIDERMAN SIGN')
                else:
                    video.reconocer()
            elif event == 'File_Path':
                if not values['File_Path'] == '':
                    video.cambiar_ruta_guardado_captura(values["File_Path"])
        window.close()
