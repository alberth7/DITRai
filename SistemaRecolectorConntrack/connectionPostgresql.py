import psycopg2

class ConnectionPostgresql(object):

    _dbName = str
    _userDB = str
    _passwordDB = str
    _hostDB = str
    _portDB = str

    def __init__(self):
        self._dbName = 'networktraffic'
        self._userDB = 'postgres'
        self._passwordDB = 'pwd'
        self._hostDB = '10.0.0.20'
        self._portDB = '5432'

    def __int__(self, dbName, userDB, passwordDB, hostDB, portDB):
        self._dbName = dbName
        self._userDB = userDB
        self._passwordDB = passwordDB
        self._hostDB = hostDB
        self._portDB = portDB

    def beginConnection(self):
        try:
           conn = psycopg2.connect(
                database=self._dbName,
                user=self._userDB,
                password=self._passwordDB,
                host=self._hostDB,
                port=self._portDB
            )
           print(">> conexion exitosa con postgresql")
        except (Exception, psycopg2.DatabaseError) as error:
            print(">> Error de conexion con PostgresSQL: ", error)
        return conn
