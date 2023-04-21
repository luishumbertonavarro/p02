import PySimpleGUI as sg
import hashlib
from selenium.webdriver.support.wait import WebDriverWait
from datosDB import DATADB
from msal import ConfidentialClientApplication, PublicClientApplication
import app_config
import webbrowser
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

#from interfaz import Interfaz

username = ''
password = ''
#PROGRESS BAR
msc_base64='iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAMAAAC5zwKfAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAFBUExURWxIPlBbOc5OKXGdEt5PJnepCt1PJnapC9lPJ3WlDapMMWSCIsZNK26XFTBkfAuX2Aad4gib3xaHuw2U0uirCdWfEfOxBvWzBe2uCJJ1Kk1GRHFIPXtJO3pJO3dJPGBHQU1UPlRiNVRjNFVkNFJeOEhKRNZOKOVPJeVPJeBPJrJML2aIHnirCXmvB3qvB3SjDu9QI8FNLGyTF363Au5QI2yTGH23An23AupQJLxNLWqPGnyzBJBKN1txLDdbaxSLwg6Szg+RzhCPyiB6o76QGeKnDOWpC+WpC9uiD31oMStriQae5AKj7QKj7QOh6vu3Av24Av24Av64Ave0BKF/JCltjASf5/m1A6WBIqWBIwSg5/m1A6aBIi5ngQia3fGxBph5J0FMUlhRP/NQIn+7APJQIn+6AAGk7/+5AQGk8P///zvg0CgAAABjdFJOUwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAg8REREHCBQUFBIDmsfFvjg9xMnLoflFS/r2Svf47UNJ8BYZBDA+PTsRDjc5OisDDLf39Onn8/L2swoMv7wKCsG+CgqQiwgBAZN5mZgAAAABYktHRGolYpUOAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5wIOExQMZPIjngAAARhJREFUWMPtzNciggEYBuCv8TfRoKU9aKedQot20d4RZd3/DTh29Mbx91zAQ+dWmx1yOEnkcnsgr++CrJf+ABQMiSXhSBSKXfnI5t9h8YRUSKb2WMxL9sDuHUonZPJM9gPaRz0ccsghhxxyyCGHHHL4r1DI5A4LHcF4GrrOK5SFm1wWSUXc5AwlsPytSn1XyEDJsItILJVBCtXRsVopyBFBIqITjRbT6U/PDEYTZrZQsVSuQNV7veGhVocazRa1O90e9FjVGWtP/QEyHI1pMv3EehWtqd7/wmbzP4SDQ8IFhxxyyCGHHHLIIYcc/g6X3zjslrWmxvCAcLWmzfNyCnVKGnNzNINWL1t63UywdvHE0hrPF8h6+/YDzT/YmYyxV9UAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMDItMTRUMTk6MTk6NTQrMDA6MDCJaX9kAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTAyLTE0VDE5OjE5OjU0KzAwOjAw+DTH2AAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyMy0wMi0xNFQxOToyMDoxMiswMDowMC1MkAwAAAAASUVORK5CYII='

sg.set_options(font='bold')


class Principal:

    def login(self):
        global username, password
        sg.theme("DarkAmber")
        layout = [[sg.Text("Inicie sesion para Comenzar", size=(30, 1), font=55)],
                  [sg.Text("Usuario", size=(15, 1), font=16), sg.InputText(key='-usrnm-', font=16)],
                  [sg.Text("Contraseña", size=(15, 1), font=16), sg.InputText(key='-pwd-', password_char='*', font=16)],
                  [sg.Button('Iniciar',size=(10, 2)), sg.Button('Cancelar',size=(10, 2)), sg.Button('Registrarse',size=(10, 2))],
                  [sg.Text("Iniciar con tu cuenta de Microsoft:", size=(30, 1), font=55)],
                  [sg.Button('.', image_data=msc_base64)]]

        window = sg.Window("Reconocedor de gestos", layout)

        while True:
            event, values = window.read()
            if event == "Cancelar" or event == sg.WIN_CLOSED:
                break
            elif event == ".":
                SCOPES = ['User.Read']
                client = ConfidentialClientApplication(client_id=app_config.CLIENT_ID, client_credential=app_config.CLIENT_SECRET)
                authori_url = client.get_authorization_request_url(SCOPES)
                #print(authori_url)
                driver = webdriver.Chrome()
                driver.get(authori_url)
                wait = WebDriverWait(driver, 60)
                element = wait.until(EC.url_contains("?code="))
                strUrl = driver.current_url
                ide = strUrl.index('code=')+5
                authcode = strUrl[ide:]
                accestoken = client.acquire_token_by_authorization_code(code=authcode, scopes=SCOPES)
                data1 = accestoken['id_token_claims']['name']
                userna = accestoken['id_token_claims']['preferred_username']
                file = DATADB()
                result = file.obtener_usuario_by_user(userna)
                if not result:
                    file.insert_user_token(data1,userna,authcode)
                    result = file.obtener_usuario_by_user(userna)
                    file.insert_session(result[0])
                else:
                    file.insert_session(result[0])
                driver.close()
                window.close()
                interfaz = Interfaz()
                interfaz.interfaz_home()
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
                    userini=result[1]
                    sg.popup("Bienvenido "+userini,auto_close_duration=5000)
                    file = DATADB()
                    resultsession = file.obterner_session_valida(result[0])
                    if not  resultsession:
                        file = DATADB()
                        result = file.insert_session(result[0])
                window.close()
                interfaz = Interfaz()
                interfaz.setPrincipalClass(self)
                interfaz.interfaz_home()
            elif event == "Registrarse":
                global username, password
                sg.theme('DarkAmber')
                layout = [[sg.Text("Registrate", font=55, justification='c')],
                          [sg.Text("Nombre Completo", size=(15, 1)), sg.InputText(key='-email-', font=16)],
                          [sg.Text("Crear Usuario", size=(15, 1)), sg.InputText(key='-username-', font=16)],
                          [sg.Text("Crear Password", size=(15, 1)), sg.InputText(key='-password-', font=16, password_char='*')],
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
                                file.insert_user(nombre,username,pswr)
                                sg.popup("Usuario registrado correctamente!")
                                windowreg.finalize()
                                break
                            else:
                                sg.popup_error("Usuario existe", font=16)
                                continue
                windowreg.close()
