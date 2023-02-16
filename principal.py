import PySimpleGUI as sg
import conexion as conn
import msal
import app_config
import webbrowser
import datetime
import requests
from interfaz import Interfaz
from flask import Flask, render_template, session, request, redirect, url_for
username = ''
password = ''
#PROGRESS BAR
msc_base64='iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAMAAAC5zwKfAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAFBUExURWxIPlBbOc5OKXGdEt5PJnepCt1PJnapC9lPJ3WlDapMMWSCIsZNK26XFTBkfAuX2Aad4gib3xaHuw2U0uirCdWfEfOxBvWzBe2uCJJ1Kk1GRHFIPXtJO3pJO3dJPGBHQU1UPlRiNVRjNFVkNFJeOEhKRNZOKOVPJeVPJeBPJrJML2aIHnirCXmvB3qvB3SjDu9QI8FNLGyTF363Au5QI2yTGH23An23AupQJLxNLWqPGnyzBJBKN1txLDdbaxSLwg6Szg+RzhCPyiB6o76QGeKnDOWpC+WpC9uiD31oMStriQae5AKj7QKj7QOh6vu3Av24Av24Av64Ave0BKF/JCltjASf5/m1A6WBIqWBIwSg5/m1A6aBIi5ngQia3fGxBph5J0FMUlhRP/NQIn+7APJQIn+6AAGk7/+5AQGk8P///zvg0CgAAABjdFJOUwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAg8REREHCBQUFBIDmsfFvjg9xMnLoflFS/r2Svf47UNJ8BYZBDA+PTsRDjc5OisDDLf39Onn8/L2swoMv7wKCsG+CgqQiwgBAZN5mZgAAAABYktHRGolYpUOAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5wIOExQMZPIjngAAARhJREFUWMPtzNciggEYBuCv8TfRoKU9aKedQot20d4RZd3/DTh29Mbx91zAQ+dWmx1yOEnkcnsgr++CrJf+ABQMiSXhSBSKXfnI5t9h8YRUSKb2WMxL9sDuHUonZPJM9gPaRz0ccsghhxxyyCGHHHL4r1DI5A4LHcF4GrrOK5SFm1wWSUXc5AwlsPytSn1XyEDJsItILJVBCtXRsVopyBFBIqITjRbT6U/PDEYTZrZQsVSuQNV7veGhVocazRa1O90e9FjVGWtP/QEyHI1pMv3EehWtqd7/wmbzP4SDQ8IFhxxyyCGHHHLIIYcc/g6X3zjslrWmxvCAcLWmzfNyCnVKGnNzNINWL1t63UywdvHE0hrPF8h6+/YDzT/YmYyxV9UAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMDItMTRUMTk6MTk6NTQrMDA6MDCJaX9kAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTAyLTE0VDE5OjE5OjU0KzAwOjAw+DTH2AAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyMy0wMi0xNFQxOToyMDoxMiswMDowMC1MkAwAAAAASUVORK5CYII='

db = conn.DB()

class Principal:

    def create_account():
        global username, password
        sg.theme('DarkAmber')
        layout = [[sg.Text("Sign Up", size=(15, 1), font=40, justification='c')],
                  [sg.Text("E-mail", size=(15, 1), font=16), sg.InputText(key='-email-', font=16)],
                  [sg.Text("Re-enter E-mail", size=(15, 1), font=16), sg.InputText(key='-remail-', font=16)],
                  [sg.Text("Create Username", size=(15, 1), font=16), sg.InputText(key='-username-', font=16)],
                  [sg.Text("Create Password", size=(15, 1), font=16),
                   sg.InputText(key='-password-', font=16, password_char='*')],
                  [sg.Button("Submit"), sg.Button("Cancel")]]

        window = sg.Window("Sign Up", layout)

        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            else:
                if event == "Submit":
                    password = values['-password-']
                    username = values['-username-']
                    if values['-email-'] != values['-remail-']:
                        sg.popup_error("Error", font=16)
                        continue
                    elif values['-email-'] == values['-remail-']:
                        progress_bar()
                        break
        window.close()

    #create_account()

    def _retrieve_data_from_function(token, table):
        raph_data = requests.get(  # Use token to call downstream service
            app_config.GRAPH_ENDPOINT,
            headers={'Authorization': 'Bearer ' + token},
        ).json()
        print(raph_data)

    def _get_token_from_cache(scope):
        cache = _load_cache()  # This web app maintains one cache per session
        cca = _build_msal_app(cache=cache)
        accounts = cca.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            result = cca.acquire_token_silent(scope, account=accounts[0])
            _save_cache(cache)
            return result

    def _load_cache():
        cache = msal.SerializableTokenCache()
        if session.get("token_cache"):
            cache.deserialize(session["token_cache"])
        return cache

    def login():
        global username, password
        sg.theme("DarkAmber")
        layout = [[sg.Text("Inicie sesion para Comenzar", size=(30, 1), font=55)],
                  [sg.Text("Usuario", size=(15, 1), font=16), sg.InputText(key='-usrnm-', font=16)],
                  [sg.Text("Contraseña", size=(15, 1), font=16), sg.InputText(key='-pwd-', password_char='*', font=16)],
                  [sg.Button('Iniciar',size=(10, 2)), sg.Button('Cancelar',size=(10, 2))],
                  [sg.Text("Iniciar con:", size=(30, 1), font=55)],
                  [sg.Button('m', image_data=msc_base64)]]

        window = sg.Window("Reconocedor de gestos", layout)

        while True:
            event, values = window.read()
            if event == "Cancelar" or event == sg.WIN_CLOSED:
                break
            elif event == "m":
                SCOPES = ['User.Read']
                app2 = msal.ConfidentialClientApplication(
                    app_config.CLIENT_ID, authority=app_config.AUTHORITY,
                    client_credential=app_config.CLIENT_SECRET
                )
                authorization_url = app2.get_authorization_request_url(SCOPES)
                print(authorization_url)
                webbrowser.open(authorization_url)
                autorization_code = '68a20d07-0850-40d2-8422-14f52299391e'
                access_token = app2.acquire_token_by_authorization_code(code=autorization_code, scopes=SCOPES)

                # result = app2.acquire_token_for_client(scopes=app_config.APPLICATION_PERMISSIONS)
                # token = result['access_token']
                result = app2.acquire_token_for_client(scopes=app_config.APPLICATION_PERMISSIONS)
                token = result['access_token']
                if token:
                    print(token)
                if "access_token" in result:
                    graph_data = requests.get(
                        "https://graph.microsoft.com/v1.0/users",
                        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
                    print("Graph API call result: %s" % json.dumps(graph_data, indent=2))

                    #sql = 'INSERT INTO session("iduser","valido","fecha_session") VALUES (' + str(
                    ##    result[0]) + ',1,"' + fechahoy + '")'
                    #resultsession = db.ejecutar_consulta(sql)
                # si es correcto iniciamos
                # interfaz = Interfaz()
                # interfaz.principal()
            else:
                if event == "Iniciar":
                    user=values['-usrnm-']
                    pasw=values['-pwd-']
                    sql = 'SELECT * FROM usuario WHERE usuario = "'+user+'" and clave = "'+pasw+'"'
                    result = db.ejecutar_consulta(sql).fetchone()
                    if not result:
                        sg.popup("Usuario no encontrado!")
                        break
                    else:
                        userini=result[1]
                        sg.popup("Bienvenido "+userini)
                        sql = 'SELECT * FROM session WHERE iduser = ' + str(result[0])
                        resultsession = db.ejecutar_consulta(sql).fetchone()
                        if not  resultsession:
                            current_time = datetime.datetime.now()
                            day = '0' + str(current_time.day) if (current_time.day < 10) else str(current_time.day)
                            moth = '0' + str(current_time.month) if (current_time.month < 10) else str(current_time.month)
                            fechahoy = day + '/' + moth + '/' + str(current_time.year)
                            sql = 'INSERT INTO session("iduser","valido","fecha_session") VALUES ('+str(result[0])+',1,"'+fechahoy+'")'
                            resultsession = db.ejecutar_consulta(sql)
                        window.close()
                        interfaz = Interfaz()
                        interfaz.principal()

        window.close()

    login()