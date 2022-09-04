import PySimpleGUI as sg


class Interfaz:
    sg.theme('DarkAmber')

    def __init__(self):
        self.layout = None

    def __cargar_layout(self):
        self.layout = [
            [sg.Text('Seleccione el gesto para la captura:')],
            [sg.Combo(['HighFive', 'spiderman', 'V'], default_value='Seleccione un gesto', size=(19, 1))],
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
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            elif event == 'File_Path':
                direccion = values["File_Path"]
                print(values['File_Path'])
            print('You entered ', values[0], values["File_Path"])
        window.close()
