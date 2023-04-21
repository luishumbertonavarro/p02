from interfaz import Interfaz
from datosDB import DATADB
import msal
from principal import Principal
#system("clear")
if __name__ == '__main__':

    file = DATADB()
    result = file.obtener_session_activa()
    interfaz = Interfaz()

    if result is None:
        interfaz.login()
    else:
        interfaz.interfaz_home()


