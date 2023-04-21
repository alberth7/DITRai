import sqlite3
from Data.PathFiles import PathFiles


'''
           id INTEGER PRIMARY KEY,
           chatId : ide de chat de telegram
           telegramToken : token del bot
           monitorSystem : tiempo en minutos de la frecuencia del monitoreo del sstema
           frecuencyGetTableTrafict: tiempo en segundos, frecuencia de peticion al router
           timeFrecuencyGetTableTrafict: tiempo en segundos, tiempo de ejcucion de las peticiones al router
'''

def createDB():
    try:
        conexon = sqlite3.connect(PathFiles.dbRoute)
        cursor = conexon.cursor()
        query = '''CREATE TABLE setting (
           id INTEGER PRIMARY KEY,
           chatId TEXT NOT NULL,
           telegramToken TEXT NOT NULL,
           monitorSystem INTEGER NOT NULL,
           frecuencyGetTableTrafict INTEGER NOT NULL,
           timeFrecuencyGetTableTrafict INTEGER NOT NULL,
           beginEnd INTEGER NOT NULL
        );'''
        cursor.execute(query)
    except Exception as ex:
        print(ex)

def createTableRouter():
    try:
        conexon = sqlite3.connect(PathFiles.dbRoute)
        cursor = conexon.cursor()
        query = '''CREATE TABLE router (
           id INTEGER PRIMARY KEY,
           host TEXT NOT NULL,
           user TEXT NOT NULL,
           password TEXT NOT NULL,
           port INTEGER NOT NULL,
           sshPath TEXT NOT NULL
        );'''
        cursor.execute(query)
    except Exception as ex:
        print(ex)

def createTableConnectionDB():
    try:
        conexon = sqlite3.connect(PathFiles.dbRoute)
        cursor = conexon.cursor()
        query = '''CREATE TABLE connection_DB(
           id INTEGER PRIMARY KEY,
           dbName TEXT NOT NULL,
           userDB TEXT NOT NULL,
           passwordDB TEXT NOT NULL,
           hostDB TEXT NOT NULL,
           portDB INTEGER NOT NULL
        );'''
        cursor.execute(query)
    except Exception as ex:
        print(ex)

def createTableConnectionML():
    try:
        conexon = sqlite3.connect(PathFiles.dbRoute)
        cursor = conexon.cursor()
        query = '''CREATE TABLE api_ML(
           id INTEGER PRIMARY KEY,
           model_1 TEXT NOT NULL,
           model_2 TEXT NOT NULL
        );'''
        cursor.execute(query)
    except Exception as ex:
        print(ex)


def getDatadb():
    try:
        conexon = sqlite3.connect(PathFiles.dbRoute)
        cursor = conexon.cursor()
        query = "SELECT * FROM setting"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        # Mostrar los resultados
        for row in rows:
            print(row)

        # Cerrar la conexión
        conexon.close()

    except Exception as ex:
        print(ex)


def insertDataDB():
    try:
        connexion = sqlite3.connect(PathFiles.dbRoute)
        cursor = connexion.cursor()
        query = '''
        INSERT INTO setting (chatId, telegramToken, monitorSystem, frecuencyGetTableTrafict, timeFrecuencyGetTableTrafict, beginEnd)
        VALUES ('-931358388', '5705085619:AAF-Nd7M34OUpmV2Tl4baMB0fRo_5F8U_9M', 15, 5, 180, 0);
        '''
        cursor.execute(query)
        connexion.commit()
        connexion.close()
    except Exception as ex:
        print(ex)

#createDB()
#insertDataDB()
#getDatadb()
#createTableConnectionDB()
#createTableConnectionML()
#createTableRouter()


