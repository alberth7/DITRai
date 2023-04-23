import time
import datetime
import xml.etree.ElementTree as ET

from router import Router
from connectionPostgresql import ConnectionPostgresql
from traficoTCP_UDP import  TraficoTCP_UDP
from dataRouterInDB import DataRouterInDB

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.

def getDataOfRouter(hostRouter, userRouter, pwdRouter, portRouter, pathSshRouter):
    '''Obteniendo datos del router en un archivo conntrack.xml'''

    #comandoByRouter = 'conntrack -L -o xml'
    #dataRouter = GetConntrackRouter(hostRouter, userRouter, pwdRouter, portRouter, pathSshRouter)
    #dataRouter.getContrack_XML(comandoByRouter)

    '''Obteniendo la lista de dhcp del router'''
    #comandoByRouter = 'cat /tmp/dhcp.leases'
    #dataRouter = GetDhcpRouter(hostRouter, userRouter, pwdRouter, portRouter, pathSshRouter)
    #dataRouter.getDHCP(comandoByRouter)

def insertTraficcToDataBase(traficoTCP_UDP):
    '''Insertando un objeto trafiico tcp udb a la base de datos postgresql '''

    db = 'networktraffic'
    user_DB = 'postgres'
    password_DB = 'mypwd'
    host_DB = '10.0.0.11'
    port_DB = '5432'

    connectionPostgresql = ConnectionPostgresql(db,user_DB, password_DB,host_DB,port_DB)
    connection = connectionPostgresql.beginConnection()
    #con.autocommit = True
    #con.close()

    cursor = connection.cursor()
    postgres_insert_query = "INSERT INTO public.trafico( originaldirection, originalprotoum_layer3, originalprotoname_layer3, originalsrc_layer3, originaldst_layer3, originalprotoum_layer4, originalprotoname_layer4, originalsport_layer4, originaldport_layer4, originalpackets, originalbytes, replydirection, replyprotoum_layer3, replyprotoname_layer3, replysrc_layer3, replydst_layer3, replyprotoum_layer4, replyprotoname_layer4, replysport_layer4, replydport_layer4, replypackets, replybytes, independentdirection, estado, timeout, mark, use, id_pakage, datetime) " \
                            " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
    record_to_insert = (
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
                        str(traficoTCP_UDP.date)
                        )
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")
    connection.close()

def saveDataInPostgrest():
    '''Leemos el conntrack.xml y despues guardamos en la base de datos postgresql'''

    traficoTCP_UDP = TraficoTCP_UDP()

    #Leendo el archivo xml
    tree = ET.parse('conntrack.xml')
    root = tree.getroot()
    now = datetime.datetime.now()
    for flow in root:
        for meta in flow:
            if str(meta.get('direction')) == 'original':
                traficoTCP_UDP.originalDirection = str(meta.get('direction'))
                for layer in meta:
                    # Layer 3
                    #print(str(layer.tag))
                    if str(layer.tag) == "layer3":
                        traficoTCP_UDP.originalProtoum_Layer3   = layer.get('protonum')
                        traficoTCP_UDP.originalProtoname_Layer3 = layer.get('protoname')
                        if layer.find('src') is not None: traficoTCP_UDP.originalSRC_Layer3       = layer.find('src').text
                        if layer.find('dst') is not None: traficoTCP_UDP.originalDST_Layer3       = layer.find('dst').text
                    # Layer 4
                    elif str(layer.tag) == "layer4":
                        traficoTCP_UDP.originalProtoum_Layer4   = layer.get('protonum')
                        traficoTCP_UDP.originalProtoname_Layer4 = layer.get('protoname')
                        if layer.find('sport') is not None: traficoTCP_UDP.originalSPORT_Layer4     = layer.find('sport').text
                        if layer.find('dport') is not None: traficoTCP_UDP.originalDPORT_Layer4     = layer.find('dport').text
                    # Counters
                    elif str(layer.tag) == "counters":
                        traficoTCP_UDP.originalPackets = layer.find('packets').text
                        traficoTCP_UDP.originalBytes   = layer.find('bytes').text

            elif str(meta.get('direction')) == 'reply':
                traficoTCP_UDP.replyDirection = meta.get('direction')
                for layer in meta:
                    # Layer 3
                    if str(layer.tag) == "layer3":
                        traficoTCP_UDP.replyProtoum_Layer3   = layer.get('protonum')
                        traficoTCP_UDP.replyProtoname_Layer3 = layer.get('protoname')
                        if layer.find('src') is not None: traficoTCP_UDP.replySRC_Layer3       = layer.find('src').text
                        if layer.find('dst') is not None: traficoTCP_UDP.replyDST_Layer3       = layer.find('dst').text

                    # Layer 4
                    elif str(layer.tag) == "layer4":
                        traficoTCP_UDP.replyProtoum_Layer4   = layer.get('protonum')
                        traficoTCP_UDP.replyProtoname_Layer4 = layer.get('protoname')
                        if layer.find('sport') is not None: traficoTCP_UDP.replySPORT_Layer4 = layer.find('sport').text
                        if layer.find('dport') is not None: traficoTCP_UDP.replyDPORT_Layer4 = layer.find('dport').text

                    # Counters
                    elif str(layer.tag) == "counters":
                        if layer.find('packets') is not None: traficoTCP_UDP.replyPackets = layer.find('packets').text
                        if layer.find('bytes') is not None: traficoTCP_UDP.replyBytes   = layer.find('bytes').text

            elif str(meta.get('direction')) == 'independent':
                traficoTCP_UDP.independentDirection = meta.get('direction')
                if meta.find('state') is not None: traficoTCP_UDP.state = meta.find('state').text
                if meta.find('timeout') is not None: traficoTCP_UDP.timeout = meta.find('timeout').text
                if meta.find('mark') is not None: traficoTCP_UDP.mark = meta.find('mark').text
                if meta.find('use') is not None: traficoTCP_UDP.use = meta.find('use').text
                if meta.find('id') is not None: traficoTCP_UDP.id = meta.find('id').text
        traficoTCP_UDP.date = str(now)
        print(vars(traficoTCP_UDP))
        insertTraficcToDataBase(traficoTCP_UDP)

def saveDataInPostgrest2():
    '''Leemos el conntrack.xml y despues guardamos en la base de datos postgresql'''

    traficoTCP_UDP = TraficoTCP_UDP()

    #Leendo el archivo xml
    for x in range(1, 2):
        tree = ET.parse('/media/michael/5FD9-11C0/traffic/conntrack.xml')
        #print(('/media/michael/5FD9-11C0/traffic/conntrack.xml'+ str(x)))
        root = tree.getroot()
        now = datetime.datetime.now()
        for flow in root:
            for meta in flow:
                if str(meta.get('direction')) == 'original':
                    traficoTCP_UDP.originalDirection = str(meta.get('direction'))
                    for layer in meta:
                        # Layer 3
                        # print(str(layer.tag))
                        if str(layer.tag) == "layer3":
                            traficoTCP_UDP.originalProtoum_Layer3 = layer.get('protonum')
                            traficoTCP_UDP.originalProtoname_Layer3 = layer.get('protoname')
                            if layer.find('src') is not None: traficoTCP_UDP.originalSRC_Layer3 = layer.find('src').text
                            if layer.find('dst') is not None: traficoTCP_UDP.originalDST_Layer3 = layer.find('dst').text
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
                            if layer.find('src') is not None: traficoTCP_UDP.replySRC_Layer3 = layer.find('src').text
                            if layer.find('dst') is not None: traficoTCP_UDP.replyDST_Layer3 = layer.find('dst').text

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
                    traficoTCP_UDP.independentDirection = meta.get('direction')
                    if meta.find('state') is not None: traficoTCP_UDP.state = meta.find('state').text
                    if meta.find('timeout') is not None: traficoTCP_UDP.timeout = meta.find('timeout').text
                    if meta.find('mark') is not None: traficoTCP_UDP.mark = meta.find('mark').text
                    if meta.find('use') is not None: traficoTCP_UDP.use = meta.find('use').text
                    if meta.find('id') is not None: traficoTCP_UDP.id = meta.find('id').text
            traficoTCP_UDP.date = str(now)
            print(vars(traficoTCP_UDP))
            insertTraficcToDataBase(traficoTCP_UDP)

if __name__ == '__main__':
    timeSleep = 1
    router = Router()
    dataRouterInDB = DataRouterInDB()
    while True:
        router.getContrack_XML()
        router.getDHCP()
        dataRouterInDB.saveDataInPostgresql()
        time.sleep(timeSleep)
