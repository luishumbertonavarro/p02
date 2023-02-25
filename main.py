from interfaz import Interfaz
from principal import Principal
from datosDB import DATADB
import msal
#system("clear")
if __name__ == '__main__':

    file = DATADB()
    result = file.obtener_session_activa()

    if result is None:
        principal = Principal()
        principal.login()

    else:
        interfaz = Interfaz()
        interfaz.principal()


