import sqlite3
from Data.PathFiles import PathFiles


class VariablesConfiguracion(object):
    _chatId = str
    _telegramToken = str
    _monitorSystem = int
    _frecuencyGetTableTrafict = int
    _timeFrecuencyGetTableTrafict = int
    _beginEnd = int
    def __init__(self):
        try:
            conexon = sqlite3.connect(PathFiles.dbRoute)
            cursor = conexon.cursor()
            query = "SELECT id, chatId, telegramToken, monitorSystem, frecuencyGetTableTrafict, timeFrecuencyGetTableTrafict, beginEnd FROM setting"
            cursor.execute(query)
            rows = cursor.fetchall()
            # Mostrar los resultados
            for row in rows:
                self._chatId = row[1]
                self._telegramToken = row[2]
                self._monitorSystem = row[3]
                self._frecuencyGetTableTrafict = row[4]
                self._timeFrecuencyGetTableTrafict = row[5]

            # Cerrar la conexión
            conexon.close()
            #self._monitorSystem = 4
            #self._frecuencyGetTableTrafict = 2
            #self._timeFrecuencyGetTableTrafict = 240
        except Exception as ex:
            print(ex)

    def getDatadb(self):
        try:
            conexon = sqlite3.connect(PathFiles.dbRoute)
            cursor = conexon.cursor()
            query = "SELECT * FROM setting"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Mostrar los resultados
            for row in rows:
                print(row)

            # Cerrar la conexión
            conexon.close()

        except Exception as ex:
            print(ex)




