import sqlite3
from sqlite3 import Error
import datetime
database = "recursos/bd_proyecto.db"

# The CRUD class contains all the essential querys to create, read, update and delete tables


class DATADB:
    def __init__(self):
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(database)
            return conn
        except Error as e:
            print(e)
    def cerrar_session(self):
        sql = 'UPDATE session SET valido = 0'
        conn = self.create_connection()
        c = conn.cursor()
        result = c.execute(sql, ())
        conn.commit()
        return result
    def obtener_session_activa(self):
         current_time = datetime.datetime.now()
         day = '0' + str(current_time.day) if (current_time.day < 10) else str(current_time.day)
         moth = '0' + str(current_time.month) if (current_time.month < 10) else str(current_time.month)
         fechahoy = day + '/' + moth + '/' + str(current_time.year)
         sql = "SELECT u.* FROM session s INNER JOIN usuario u on u.id = s.iduser WHERE s.valido = 1 AND s.fecha_session = '" + fechahoy + "' ORDER BY s.id DESC "
         conn = self.create_connection()
         c = conn.cursor()
         result = c.execute(sql,())
         conn.commit()
         return result
    def run_query(self, query, parameters = ()):
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query, parameters)
                conn.commit()
            return result
    def obtener_usuario_by_user(self,user):
        sql = 'SELECT * FROM usuario WHERE usuario = "' + user + '"'
        conn = self.create_connection()
        c = conn.cursor()
        result = c.execute(sql, ()).fetchone()
        conn.commit()
        return result
    def insert_user(self, nombre, username, passw):
        sql = 'INSERT INTO usuario ("nombre","usuario","clave","token") VALUES ("' + nombre + '","' + username + '","' + passw + '","") '
        conn = self.create_connection()
        c = conn.cursor()
        result = c.execute(sql, ())
        conn.commit()
        return result
    def insert_session(self, iduser):
        current_time = datetime.datetime.now()
        day = '0' + str(current_time.day) if (current_time.day < 10) else str(current_time.day)
        moth = '0' + str(current_time.month) if (current_time.month < 10) else str(current_time.month)
        fechahoy = day + '/' + moth + '/' + str(current_time.year)
        sql = 'INSERT INTO session("iduser","valido","fecha_session") VALUES (' + str(iduser) + ',1,"' + fechahoy + '")'
        conn = self.create_connection()
        c = conn.cursor()
        result = c.execute(sql, ())
        conn.commit()
        return result
    def obterner_session_valida(self, iduser):
        sql = 'SELECT * FROM session WHERE valido = 1 and iduser = ' + str(iduser)
        conn = self.create_connection()
        c = conn.cursor()
        result = c.execute(sql, ()).fetchone()
        conn.commit()
        return result
    def login(self,user,password):
        sql = 'SELECT * FROM usuario WHERE usuario = "'+user+'" and clave = "'+password+'"'
        conn = self.create_connection()
        c = conn.cursor()
        result = c.execute(sql, ()).fetchone()
        conn.commit()
        return result