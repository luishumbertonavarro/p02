from interfaz import Interfaz
import datetime
from principal import Principal
import app_config
import conexion as conn
import msal
db = conn.DB()
#system("clear")
if __name__ == '__main__':
    # consulta session activa
    current_time = datetime.datetime.now()
    day = '0'+str(current_time.day) if (current_time.day < 10) else str(current_time.day)
    moth = '0' + str(current_time.month) if (current_time.month < 10) else str(current_time.month)
    fechahoy = day+'/'+moth+'/'+str(current_time.year)
    sql = "SELECT u.* FROM session s INNER JOIN usuario u on u.id = s.iduser WHERE s.valido = 1 AND s.fecha_session = '"+fechahoy+"'"
    #parametros = (fechahoy,)
    result = db.ejecutar_consulta(sql).fetchone()



    if result is None:
        principal = Principal()
        principal.login()
    else:
        interfaz = Interfaz()
        interfaz.principal()


