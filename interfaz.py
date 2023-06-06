import json

import PySimpleGUI as sg
import cv2

import principal
from gestos import GestoClass
from reconocimiento import ReconocimientoVideo
from strategy import CapturarPantallaStrategyAccion
from PIL import Image
import datetime
from datosDB import DATADB

import hashlib
from selenium.webdriver.support.wait import WebDriverWait
from msal import ConfidentialClientApplication, PublicClientApplication
import app_config
import webbrowser
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class Interfaz:
    sg.theme('DarkAmber')
    sg.set_options(font='bold')
    __accion = CapturarPantallaStrategyAccion()
    __reconocimiento = ReconocimientoVideo(__accion)
    llave_gesto = None
    menssaje = None
    file = DATADB()
    font = ("Arial", 20)
    username = ''
    password = ''
    # PROGRESS BAR

    sg.set_options(font='bold')

    def interfaz_home(self, parent_window=None):
        def cargar_layout():
            return [

                [sg.Text(self.menssaje, key="txtCombo", font=self.font)],
                [sg.Text('Seleccione el gesto para la captura:', key="txtCombo")],
                [(sg.Button(image_source=gesto.img_referencia, button_color='white',
                            key='btnGesto-' + gesto.nombre_gesto), sg.Text(gesto.nombre_gesto))
                 for gesto in self.__reconocimiento.gestos_],

                [sg.Text('Agregar nuevo gesto', key="txtAdd"),
                 sg.Button(image_source='recursos/manoAdd.png', image_size=(50, 50),
                           button_color=("white", "#E7C829"),
                           key="btnAddWindow")],
                [sg.Text(key='gestoSeleccionado', text_color='white')],
                [sg.Text(key='errorGesto', text_color='red')],
                [sg.Text("Seleccione una carpeta para guardar: ")],
                [sg.In(enable_events=True, key='File_Path'), sg.FolderBrowse('Buscar')],
                [sg.Text(key='errorFolder', text_color='red')],
                [sg.Button('Ok', size=(7, 1)), sg.Button('Cancel', size=(7, 1))],

                [sg.Button('Cerrar Sesion', size=(16, 1))],
            ]

        if parent_window:
            parent_window.close()
        result = self.file.obtener_session_activa()
        if not result:
            exit()
        self.menssaje = 'Hola ' + str(result[1])
        self.__reconocimiento.gestos_ = []
        self.__reconocimiento.cargar_gestos_predeterminados()
        # Create the Window
        window = sg.Window('Reconocimiento de gestos', cargar_layout(), resizable=True)
        # Event Loop to process "events" and get the "values" of the inputs
        self.llave_gesto = None
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                window.close()
                break
            elif event == "Cerrar Sesion":
                self.file.cerrar_session()
                # break
                window.close()
                self.login()
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
        dedos_seleccionar_data = ['THUMB', 'INDEX', 'MIDDLE', 'RING', 'PINKY']

        def cargar_layout():
            return [
                [sg.Text('Seleccione los dedos para el nuevo gesto:', key="txtCombo")],
                [sg.Checkbox(dedoscheckbox, default=True, key=dedoscheckbox) for dedoscheckbox in dedos_seleccionar],
                [sg.Button('Seleccionar todos'), sg.Button('Desmarcar todos')],
                [sg.Text('Seleccione un nombre para el gesto:', font='bold'), sg.InputText(key='txtNombreGestoNuevo')],

                [sg.Button('Guardar', size=(7, 1)), sg.Button('Cancelar', size=(7, 1))],
            ]

        if parent_window:
            parent_window.close()

        result = self.file.obtener_session_activa()
        # Create the Window
        window = sg.Window('Reconocimiento de gestos', cargar_layout(), resizable=True)
        # Event Loop to process "events" and get the "values" of the inputs
        self.llave_gesto = None
        while True:
            event, values = window.read()
            if event == 'Guardar':
                nombre = values['txtNombreGestoNuevo']
                image = r"./recursos/gestoPersonalizado.png"
                Pulgar = int(values['Pulgar'])
                Indice = int(values['Indice'])
                Medio = int(values['Medio'])
                Anular = int(values['Anular'])
                Meñique = int(values['Meñique'])
                reg = self.file.guardar_gesto(nombre, image, result[0], Pulgar, Indice, Medio, Anular, Meñique)
                __accion = CapturarPantallaStrategyAccion()
                self.__reconocimiento = ReconocimientoVideo(__accion)
                self.interfaz_home(window)

            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                window.close()
                break
            if event == 'Cancelar':
                self.interfaz_home(window)
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
        self.interfaz_home()

    def login(self):
        global username, password
        sg.theme("DarkAmber")
        layout = [[sg.Text("Inicie sesion para Comenzar", size=(30, 1), font=55)],
                  [sg.Text("Usuario", size=(15, 1), font=16), sg.InputText(key='-usrnm-', font=16, pad=5)],
                  [sg.Text("Contraseña", size=(15, 1), font=16), sg.InputText(key='-pwd-', pad=5, password_char='*', font=16)],
                  [sg.Button('Iniciar'), sg.Button('Cancelar'), sg.Button('Registrarse')],
                  [sg.Button('Iniciar sesion con Microsoft', size=(26, 1), pad=5, key='-inimicrosoft-')]]

        window = sg.Window("Reconocedor de gestos", layout)

        while True:
            event, values = window.read()
            if event == "Cancelar" or event == sg.WIN_CLOSED:
                break
            elif event == "-inimicrosoft-":
                SCOPES = ['User.Read']
                client = ConfidentialClientApplication(client_id=app_config.CLIENT_ID,
                                                       client_credential=app_config.CLIENT_SECRET)
                authori_url = client.get_authorization_request_url(SCOPES)
                # print(authori_url)
                driver = webdriver.Chrome()
                driver.get(authori_url)
                wait = WebDriverWait(driver, 60)
                element = wait.until(EC.url_contains("?code="))
                strUrl = driver.current_url
                ide = strUrl.index('code=') + 5
                authcode = strUrl[ide:]
                accestoken = client.acquire_token_by_authorization_code(code=authcode, scopes=SCOPES)
                data1 = accestoken['id_token_claims']['name']
                userna = accestoken['id_token_claims']['preferred_username']
                file = DATADB()
                result = file.obtener_usuario_by_user(userna)
                if not result:
                    file.insert_user_token(data1, userna, authcode)
                    result = file.obtener_usuario_by_user(userna)
                    file.insert_session(result[0])
                else:
                    file.insert_session(result[0])
                driver.close()
                window.close()
                self.interfaz_home()
            elif event == "Iniciar":
                user = values['-usrnm-']
                pasw = values['-pwd-']
                paswmd5 = hashlib.md5(pasw.encode())
                pswd = paswmd5.hexdigest()
                file = DATADB()
                result = file.login(user, pswd)
                if not result:
                    sg.popup("Usuario no encontrado!")
                else:
                    userini = result[1]
                    # sg.popup("Bienvenido "+userini,auto_close_duration=5000)
                    file = DATADB()
                    resultsession = file.obterner_session_valida(result[0])
                    if not resultsession:
                        file = DATADB()
                        result = file.insert_session(result[0])
                window.close()
                self.interfaz_home()
            elif event == "Registrarse":
                global username, password
                sg.theme('DarkAmber')
                layout = [[sg.Text("Registrate", font=55, justification='c')],
                          [sg.Text("Nombre Completo", size=(15, 1)), sg.InputText(key='-email-', font=16)],
                          [sg.Text("Crear Usuario", size=(15, 1)), sg.InputText(key='-username-', font=16)],
                          [sg.Text("Crear Password", size=(15, 1)),
                           sg.InputText(key='-password-', font=16, password_char='*')],
                          [sg.Text(key='errorCrearUser', text_color='red')],
                          [sg.Button("Completar"), sg.Button("Cancel")]]

                windowreg = sg.Window("Sign Up", layout)

                while True:
                    event, values = windowreg.read()
                    if event == 'Cancel' or event == sg.WIN_CLOSED:
                        windowreg.finalize()
                        break
                    else:
                        if event == "Completar":
                            nombre = values['-email-']
                            password = values['-password-']
                            username = values['-username-']
                            passmd5 = hashlib.md5(password.encode())
                            pswr = passmd5.hexdigest()
                            file = DATADB()
                            result = file.obtener_usuario_by_user(username)
                            if not result:
                                file = DATADB()
                                file.insert_user(nombre, username, pswr)
                                sg.popup("Usuario registrado correctamente!")
                                windowreg.finalize()
                                break
                            else:
                                sg.popup_error("Usuario existe", font=16)
                                continue
                windowreg.close()
