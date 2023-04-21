import xml.etree.ElementTree as ET
import datetime
import psycopg2

from .TraficoTCP_UDP import TraficoTCP_UDP
from Data.ConnectionPostgresql import ConnectionPostgresql


def getMacAddressOfIp(ip):
    '''
    Se adicionara el mac de las respectivas ip al objeto traficoTCP_UDP
    '''
    # Insetar mac
    listIp = []
    listMac = []
    with open('BusinessLogic/Files/dhcp.txt', 'r') as file:
        data = file.readlines()
    for raw_line in data:
        if raw_line.strip() != "":
            split_line = raw_line.strip().split(" ")
            listMac.append(split_line[1])
            listIp.append(split_line[2])
    macAddress = ""
    if ip in listIp:
        macAddress = listMac[listIp.index(ip)]

    return macAddress


def accionGuardarTabla_en_DB(traficoTCP_UDP):
    print("Accion 1: Guardar tabla estado de conexiones en la db ........")

    try:
        connectionPostgresql = ConnectionPostgresql()
        connection = connectionPostgresql.beginConnection()
        cursor = connection.cursor()
        postgres_insert_query = "INSERT INTO public.estadodeconexiones( macAddress, originaldirection, originalprotoum_layer3, originalprotoname_layer3, originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalsport_layer4, originaldport_layer4, originalpackets, originalbytes, replydirection, replyprotoum_layer3, replyprotoname_layer3, replysrc_layer3, replydst_layer3, replyprotoum_layer4, replyprotoname_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, independentdirection, estado, timeout, mark, use, id_pakage,assured, unreplied, datetime) " \
                                " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
        record_to_insert = (
            traficoTCP_UDP.macAddress,
            traficoTCP_UDP.originalDirection,
            # layer 3
            traficoTCP_UDP.originalProtoum_Layer3,
            traficoTCP_UDP.originalProtoname_Layer3,
            traficoTCP_UDP.originalSRC_Layer3,
            traficoTCP_UDP.originalDST_Layer3,
            # layer 4
            traficoTCP_UDP.originalProtoum_Layer4,
            traficoTCP_UDP.originalProtoname_Layer4,
            traficoTCP_UDP.originalSPORT_Layer4,
            traficoTCP_UDP.originalDPORT_Layer4,
            # counters
            traficoTCP_UDP.originalPackets,
            traficoTCP_UDP.originalBytes,

            ## direction = "reply"
            traficoTCP_UDP.replyDirection,
            # layer 3
            traficoTCP_UDP.replyProtoum_Layer3,
            traficoTCP_UDP.replyProtoname_Layer3,
            traficoTCP_UDP.replySRC_Layer3,
            traficoTCP_UDP.replyDST_Layer3,
            # layer 4
            traficoTCP_UDP.replyProtoum_Layer4,
            traficoTCP_UDP.replyProtoname_Layer4,
            traficoTCP_UDP.replySPORT_Layer4,
            traficoTCP_UDP.replyDPORT_Layer4,
            # counters
            traficoTCP_UDP.replyPackets,
            traficoTCP_UDP.replyBytes,

            ## direction="independent"
            traficoTCP_UDP.independentDirection,
            traficoTCP_UDP.state,
            traficoTCP_UDP.timeout,
            traficoTCP_UDP.mark,
            traficoTCP_UDP.use,
            traficoTCP_UDP.id,
            traficoTCP_UDP.assured,
            traficoTCP_UDP.unreplied,
            traficoTCP_UDP.date
        )
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        connection.close()
        print("Accion 1: Guardar tabla estado de conexiones en la db ........OK")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error >> Accion 1: procesador de resultados: error al subir conntrack a la base de datos.", error)





class A_GuardarTablaEnDB(ConnectionPostgresql):

    def __init__(self):
        super(A_GuardarTablaEnDB, self).__init__()

    def procesadorXML_a_Objeto(self):
        try:
            # fecha y hora
            now = datetime.datetime.now()
            # Leemos el conntrack.xml y despues guardamos en la base de datos postgresql
            traficoTCP_UDP = TraficoTCP_UDP()
            tree = ET.parse('BusinessLogic/Files/conntrack.xml')
            root = tree.getroot()

            for flow in root:
                print("Rol 1: Guardar tabla estado de conexiones en la db ........")
                for meta in flow:
                    if str(meta.get('direction')) == 'original':
                        traficoTCP_UDP.originalDirection = str(meta.get('direction'))
                        for layer in meta:
                            # Layer 3
                            # print(str(layer.tag))
                            if str(layer.tag) == "layer3":
                                traficoTCP_UDP.originalProtoum_Layer3 = layer.get('protonum')
                                traficoTCP_UDP.originalProtoname_Layer3 = layer.get('protoname')
                                if layer.find('src') is not None: traficoTCP_UDP.originalSRC_Layer3 = layer.find(
                                    'src').text
                                if layer.find('dst') is not None: traficoTCP_UDP.originalDST_Layer3 = layer.find(
                                    'dst').text
                            # Layer 4
                            elif str(layer.tag) == "layer4":
                                traficoTCP_UDP.originalProtoum_Layer4 = layer.get('protonum')
                                traficoTCP_UDP.originalProtoname_Layer4 = layer.get('protoname')
                                if layer.find('sport') is not None: traficoTCP_UDP.originalSPORT_Layer4 = layer.find(
                                    'sport').text
                                if layer.find('dport') is not None: traficoTCP_UDP.originalDPORT_Layer4 = layer.find(
                                    'dport').text
                            # Counters
                            elif str(layer.tag) == "counters":
                                traficoTCP_UDP.originalPackets = layer.find('packets').text
                                traficoTCP_UDP.originalBytes = layer.find('bytes').text

                    elif str(meta.get('direction')) == 'reply':
                        traficoTCP_UDP.replyDirection = meta.get('direction')
                        for layer in meta:
                            # Layer 3
                            if str(layer.tag) == "layer3":
                                traficoTCP_UDP.replyProtoum_Layer3 = layer.get('protonum')
                                traficoTCP_UDP.replyProtoname_Layer3 = layer.get('protoname')
                                if layer.find('src') is not None: traficoTCP_UDP.replySRC_Layer3 = layer.find(
                                    'src').text
                                if layer.find('dst') is not None: traficoTCP_UDP.replyDST_Layer3 = layer.find(
                                    'dst').text

                            # Layer 4
                            elif str(layer.tag) == "layer4":
                                traficoTCP_UDP.replyProtoum_Layer4 = layer.get('protonum')
                                traficoTCP_UDP.replyProtoname_Layer4 = layer.get('protoname')
                                if layer.find('sport') is not None: traficoTCP_UDP.replySPORT_Layer4 = layer.find(
                                    'sport').text
                                if layer.find('dport') is not None: traficoTCP_UDP.replyDPORT_Layer4 = layer.find(
                                    'dport').text

                            # Counters
                            elif str(layer.tag) == "counters":
                                if layer.find('packets') is not None: traficoTCP_UDP.replyPackets = layer.find(
                                    'packets').text
                                if layer.find('bytes') is not None: traficoTCP_UDP.replyBytes = layer.find('bytes').text

                    elif str(meta.get('direction')) == 'independent':
                        # inicializamios por defecto el valor 0
                        traficoTCP_UDP.assured = "0"
                        traficoTCP_UDP.unreplied = "0"
                        traficoTCP_UDP.independentDirection = meta.get('direction')
                        if meta.find('state') is not None: traficoTCP_UDP.state = meta.find('state').text
                        if meta.find('timeout') is not None: traficoTCP_UDP.timeout = meta.find('timeout').text
                        if meta.find('mark') is not None: traficoTCP_UDP.mark = meta.find('mark').text
                        if meta.find('use') is not None: traficoTCP_UDP.use = meta.find('use').text
                        if meta.find('id') is not None: traficoTCP_UDP.id = meta.find('id').text
                        if meta.find('assured') is not None: traficoTCP_UDP.assured = "1"
                        if meta.find('unreplied') is not None: traficoTCP_UDP.unreplied = "1"

                traficoTCP_UDP.macAddress = getMacAddressOfIp(traficoTCP_UDP.originalSRC_Layer3)
                traficoTCP_UDP.date = str(now)
                # print(vars(traficoTCP_UDP))
                print("Rol 1: Guardar tabla estado de conexiones en la db ........ OK")
                accionGuardarTabla_en_DB(traficoTCP_UDP)
        except Exception as e:
            print(e)







