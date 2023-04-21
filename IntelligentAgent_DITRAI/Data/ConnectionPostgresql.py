import psycopg2

class ConnectionPostgresql(object):

    _dbName = str
    _userDB = str
    _passwordDB = str
    _hostDB = str
    _portDB = str

    def __init__(self):
        self._dbName = ''
        self._userDB = ''
        self._passwordDB = ''
        self._hostDB = ''
        self._portDB = ''

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




        # Setting auto commit false
        #conn.autocommit = True

    # Creating a cursor object using the cursor() method
    #cursor = conn.cursor()

    # Preparing SQL queries to INSERT a record into the database.
    #cursor.execute(query)
    # Commit your changes in the database
    #conn.commit()

    #print("Records inserted........")

    # Closing the connection
    #conn.close()
