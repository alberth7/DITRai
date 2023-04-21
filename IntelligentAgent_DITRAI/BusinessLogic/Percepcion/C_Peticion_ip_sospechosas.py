import psycopg2
from Data.PathFiles import PathFiles
from Data.ConnectionPostgresql import ConnectionPostgresql

class C_Peticion_ip_sospechosas():
    def __init__(self):
        super(C_Peticion_ip_sospechosas, self).__init__()

    def SolicitarIpSospechosas(self):
        print("Percepcion 3: Solicitar ip sospechosas.............")
        results_list = []
        path = PathFiles()
        reglas = path.resultadoFinal
        connectionPostgresql = ConnectionPostgresql()
        conn = connectionPostgresql.beginConnection()
        try:
            print("Obteniedo Ip's")
            cur = conn.cursor()
            query = "SELECT DISTINCT originaldst_layer3 FROM resultado_final"
            # ejecucion query
            cur.execute(query)
            # Obtener resultados y guardarlos en una lista
            results = cur.fetchall()
            # print(results)
            results_list = [list(row) for row in results]
            conn.commit()
            conn.close()
            print("Percepcion 3: Solicitar ip sospechosas............. OK")
            return results_list
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error >>> Percepcion 3: Error al obetener ip sospechosas la query:", error)

