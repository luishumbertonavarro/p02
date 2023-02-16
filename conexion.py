import sqlite3
#Import database
database = "recursos/bd_proyecto.db"
class DB:
    def ejecutar_consulta(self,consulta,parametros = ()):
        with sqlite3.connect(database) as conn:
            self.cursor = conn.cursor()
            result = self.cursor.execute(consulta,parametros)
            conn.commit()
            return result

    def get_connection():
        connection = sqlite3.connect(database)
        return connection

    def close_connection(connection):
        if connection:
            connection.close()