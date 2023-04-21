import pandas as pd

from Data.ConnectionPostgresql import ConnectionPostgresql


def limpiezaDeDatos():
    try:
        connectionPostgresql = ConnectionPostgresql()
        connection = connectionPostgresql.beginConnection()
        cursor = connection.cursor()

        query1 = "DELETE FROM estadodeconexiones WHERE originalsrc_layer3  LIKE '%.1' OR originalsrc_layer3  LIKE '255.255.255.255' OR originalsrc_layer3  LIKE '192.168%' OR originalsrc_layer3  LIKE '0.%' OR originaldst_layer3 LIKE '10.%' OR originaldst_layer3 LIKE '192.168.%' OR originaldst_layer3 LIKE '8.%' "
        cursor.execute(query1)
        connection.commit()

        query2 = "DROP TABLE IF EXISTS estadodeconexiones_clean"
        cursor.execute(query2)
        connection.commit()
        #Creamos una tabla con las columnas mas relevantes y adicionamos una columna de frecuencia
        #query3 = "CREATE TABLE estadodeconexiones_clean as ( SELECT originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalpackets, originalbytes, replyprotoum_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, estado, timeout, use, '0' AS bad_traffic, to_char(datetime, 'DD/MM/YY HH:MI:SS') as datetime, count(to_char(datetime, 'HH:MI:SS')) as frecuencia FROM public.estadodeconexiones group by originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalpackets, originalbytes, replyprotoum_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, estado, timeout, use, to_char(datetime, 'DD/MM/YY HH:MI:SS') )"
        #query3 = "CREATE TABLE estadodeconexiones_clean as ( SELECT originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalpackets, originalbytes, replyprotoum_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, estado, timeout, use, '0' AS bad_traffic, to_char(datetime, 'DD/MM/YY HH:MI:SS') as datetime, count(to_char(datetime, 'HH:MI:SS')) as frecuencia FROM public.test_cel_bad4 where originaldst_layer3 = '185.151.204.13' or originaldst_layer3 = '193.34.76.44' group by originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalpackets, originalbytes, replyprotoum_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, estado, timeout, use, to_char(datetime, 'DD/MM/YY HH:MI:SS') )"
        query3 = "CREATE TABLE estadodeconexiones_clean as ( SELECT originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalpackets, originalbytes, replyprotoum_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, estado, timeout, use, '0' AS bad_traffic, to_char(datetime, 'DD/MM/YY HH:MI:SS') as datetime, '1' as frecuencia FROM public.test_cel_bad4 limit 5 )"
        cursor.execute(query3)
        connection.commit()

        cursor.close()
        connection.close()
    except ConnectionPostgresql.Error as e:
        print("Error >>> en la percepcion 2: limpieza de datos", e)


def obtenerDataCSV():
    try:
        print("p2>> obteniendo datos de la base de datos y guardando en csv")
        connectionPostgresql = ConnectionPostgresql()
        connection = connectionPostgresql.beginConnection()
        cursor = connection.cursor()

        '''Obtenemos los datos limpios'''
        query = " SELECT * FROM estadodeconexiones_clean  "
        cursor.execute(query)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows)

        if cursor.rowcount > 1:
            df.columns = ['originalsrc_layer3','originaldst_layer3','originalprotoum_layer4','originalprotoname_layer4',
                          'originalpackets','originalbytes','replyprotoum_layer4','replysport_layer4','replydport_layer4',
                          'replypackets','replybytes','estado','timeout','use','bad_traffic','datetime','frecuencia']

        df.to_csv(r'data.csv', index=False)
        cursor.close()
    except (Exception, connectionPostgresql) as error:
        print("Error >>> percepcion 2: Obteniendo los datos de estado de conexiones en la base de datos. ", error)

class B_PeticionDeTabla_A_DB(ConnectionPostgresql):

    def __init__(self):
        super(B_PeticionDeTabla_A_DB, self).__init__()

    def obtenerTraficoOfDB(self):
        print("Percepcion 2: Obtener tabla estado de conexiones de db..................")
        limpiezaDeDatos()
        obtenerDataCSV()
        print("Percepcion 2: Obtener tabla estado de conexiones de db..................OK")


