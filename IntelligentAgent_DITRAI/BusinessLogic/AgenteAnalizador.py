import schedule
import time
from Data.ConnectionRouter import ConnectionRouter
from Data.VariablesConfiguracion import VariablesConfiguracion
from Data.ConnectionPostgresql import ConnectionPostgresql

from .Percepcion.A_PeticionTablaConexcionesAlRouter import A_PeticionTablaConexcionesAlRouter
from .Percepcion.B_PeticionDeTabla_A_DB import B_PeticionDeTabla_A_DB
from .Percepcion.C_Peticion_ip_sospechosas import C_Peticion_ip_sospechosas


from .Rol_Accion.A_GuardarTablaEnDB import A_GuardarTablaEnDB
from .Rol_Accion.B_Guardar_conexiones_sospechosas import B_Guardar_conexiones_sospechosas
from .Rol_Accion.C_Enviar_regla_iptable import C_Enviar_regla_iptable


def mesageLog(param):
    message = '''
    ************************************************************
    >>>>>>>>>>>>>>>>>        {}       <<<<<<<<<<<<<<<<<<<<<
    ************************************************************
    '''
    print(message.format(param))


def backupTablaEstadoConexiones():
    connectionPostgresql = ConnectionPostgresql()
    connection = connectionPostgresql.beginConnection()
    cursor = connection.cursor()

    query ='''
     INSERT INTO estadodeconexiones_bk
        SELECT macaddress, originaldirection, originalprotoum_layer3, originalprotoname_layer3, originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalsport_layer4, originaldport_layer4, originalpackets, originalbytes, replydirection, replyprotoum_layer3, replyprotoname_layer3, replysrc_layer3, replydst_layer3, replyprotoum_layer4, replyprotoname_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, independentdirection, estado, timeout, mark, use, id_pakage, assured, unreplied, datetime
        FROM estadodeconexiones '''

    cursor.execute(query)
    connection.commit()
    cursor.close()

def eliminarDatosTablaEstadoConexiones():
    connectionPostgresql = ConnectionPostgresql()
    connection = connectionPostgresql.beginConnection()
    cursor = connection.cursor()

    query = "DELETE FROM estadodeconexiones"
    cursor.execute(query)
    connection.commit()

    query = "DELETE FROM estadodeconexiones_clean"
    cursor.execute(query)
    connection.commit()

    cursor.close()


class AgenteAnalizador(ConnectionRouter):

    def __init__(self):
        super(AgenteAnalizador, self).__init__()

    def objetivoSolicitar(self):
        mesageLog("Objeto Solicitar")

        pathVar = VariablesConfiguracion()
        frecSeg = pathVar._frecuencyGetTableTrafict
        frecMin = pathVar._timeFrecuencyGetTableTrafict
        start_time = time.time()

        while time.time() - start_time < frecMin:
            percepcionPedirEstdoConexion = A_PeticionTablaConexcionesAlRouter()
            rol_accion_guardarTablaEnDB= A_GuardarTablaEnDB()
            #percepcion 1
            percepcionPedirEstdoConexion.ObtenerTablaEstadoConexionToRouter()
            #rol y accion 2
            rol_accion_guardarTablaEnDB.procesadorXML_a_Objeto()
            time.sleep(frecSeg)

    def objetivoDetectar(self):
        mesageLog("Objeto Detectar")

        percepcionPeticionDeTabaAdb = B_PeticionDeTabla_A_DB()
        rolAccionGuardarConexionesSospechosas = B_Guardar_conexiones_sospechosas()
        #percepcion 2
        percepcionPeticionDeTabaAdb.obtenerTraficoOfDB()
        #rol 2
        rolAccionGuardarConexionesSospechosas.procesadorDetecta()
        #rol 3
        rolAccionGuardarConexionesSospechosas.procesadorResultados()
        #accion 2
        rolAccionGuardarConexionesSospechosas.a_guardarConexionesSospechosas()

    def objetivoBloquear(self):
        mesageLog("Objeto Bloquear")

        percepcionReglasIptable = C_Peticion_ip_sospechosas()
        #Percepcion 3
        list = percepcionReglasIptable.SolicitarIpSospechosas()

        rolAccinoEnviarReglaIptable = C_Enviar_regla_iptable()
        #rol 4
        rolAccinoEnviarReglaIptable.procesadorGenerarReglas(list)
        #accion 3
        rolAccinoEnviarReglaIptable.EnviarReglas()

    def actualizarTablas(self):
        mesageLog("Actulizando tablas")
        '''
        - Guardar los datos de la tabla estadodeconexiones en otra tabla historica
        - Eliminar datos de la tabla estadodeconexiones
        '''
        backupTablaEstadoConexiones()
        eliminarDatosTablaEstadoConexiones()





