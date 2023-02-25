import PySimpleGUI as sg
import msal
import app_config
import webbrowser
import requests

username = ''
password = ''
#PROGRESS BAR
msc_base64='iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAMAAAC5zwKfAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAFBUExURWxIPlBbOc5OKXGdEt5PJnepCt1PJnapC9lPJ3WlDapMMWSCIsZNK26XFTBkfAuX2Aad4gib3xaHuw2U0uirCdWfEfOxBvWzBe2uCJJ1Kk1GRHFIPXtJO3pJO3dJPGBHQU1UPlRiNVRjNFVkNFJeOEhKRNZOKOVPJeVPJeBPJrJML2aIHnirCXmvB3qvB3SjDu9QI8FNLGyTF363Au5QI2yTGH23An23AupQJLxNLWqPGnyzBJBKN1txLDdbaxSLwg6Szg+RzhCPyiB6o76QGeKnDOWpC+WpC9uiD31oMStriQae5AKj7QKj7QOh6vu3Av24Av24Av64Ave0BKF/JCltjASf5/m1A6WBIqWBIwSg5/m1A6aBIi5ngQia3fGxBph5J0FMUlhRP/NQIn+7APJQIn+6AAGk7/+5AQGk8P///zvg0CgAAABjdFJOUwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAg8REREHCBQUFBIDmsfFvjg9xMnLoflFS/r2Svf47UNJ8BYZBDA+PTsRDjc5OisDDLf39Onn8/L2swoMv7wKCsG+CgqQiwgBAZN5mZgAAAABYktHRGolYpUOAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5wIOExQMZPIjngAAARhJREFUWMPtzNciggEYBuCv8TfRoKU9aKedQot20d4RZd3/DTh29Mbx91zAQ+dWmx1yOEnkcnsgr++CrJf+ABQMiSXhSBSKXfnI5t9h8YRUSKb2WMxL9sDuHUonZPJM9gPaRz0ccsghhxxyyCGHHHL4r1DI5A4LHcF4GrrOK5SFm1wWSUXc5AwlsPytSn1XyEDJsItILJVBCtXRsVopyBFBIqITjRbT6U/PDEYTZrZQsVSuQNV7veGhVocazRa1O90e9FjVGWtP/QEyHI1pMv3EehWtqd7/wmbzP4SDQ8IFhxxyyCGHHHLIIYcc/g6X3zjslrWmxvCAcLWmzfNyCnVKGnNzNINWL1t63UywdvHE0hrPF8h6+/YDzT/YmYyxV9UAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMDItMTRUMTk6MTk6NTQrMDA6MDCJaX9kAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTAyLTE0VDE5OjE5OjU0KzAwOjAw+DTH2AAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyMy0wMi0xNFQxOToyMDoxMiswMDowMC1MkAwAAAAASUVORK5CYII='


def progress_bar():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Creating your account...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()


def create_account():
    global username, password
    sg.theme('DarkAmber')
    layout = [[sg.Text("Sign Up", size =(15, 1), font=40, justification='c')],
             [sg.Text("E-mail", size =(15, 1),font=16), sg.InputText(key='-email-', font=16)],
             [sg.Text("Re-enter E-mail", size =(15, 1), font=16), sg.InputText(key='-remail-', font=16)],
             [sg.Text("Create Username", size =(15, 1), font=16), sg.InputText(key='-username-', font=16)],
             [sg.Text("Create Password", size =(15, 1), font=16), sg.InputText(key='-password-', font=16, password_char='*')],
             [sg.Button("Submit"), sg.Button("Cancel")]]

    window = sg.Window("Sign Up", layout)

    while True:
        event,values = window.read()
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
create_account()

def _retrieve_data_from_function(token, table):
    token = _get_token_from_cache(app_config.DELEGATED_PERMISSONS)
    print(graph_data)

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
    global username,password
    sg.theme("DarkAmber")
    layout = [[sg.Text("Inicie sesion para Comenzar", size =(30, 1), font=55)],
            [sg.Text("Usuario", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Contraseña", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.Text("Iniciar con tu cuenta de Microsoft:", size=(30, 1), font=55)],
            [sg.Button('m',image_data=msc_base64)]]

    window = sg.Window("Reconocedor de gestos", layout)

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
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

            #result = app2.acquire_token_for_client(scopes=app_config.APPLICATION_PERMISSIONS)
            #token = result['access_token']
            result = app2.acquire_token_for_client(scopes=app_config.APPLICATION_PERMISSIONS)
            token = result['access_token']
            if token:
                print(token)
                row = _retrieve_data_from_function(token, None)
            #si es correcto iniciamos
            #interfaz = Interfaz()
            #interfaz.principal()
        else:
            if event == "Ok":
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                    sg.popup("Welcome!")
                    break
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                    sg.popup("Invalid login. Try again")

    window.close()
login()