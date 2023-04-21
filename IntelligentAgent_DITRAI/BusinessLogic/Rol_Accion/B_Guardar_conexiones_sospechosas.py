import csv
import json
import requests
import pandas as pd
import psycopg2
import subprocess

from Data.PathFiles import PathFiles
from Data.ConnectionPostgresql import ConnectionPostgresql
def prepararDatasParaAPI(data_csv, data_json):
    pathData_csv = data_csv

    with open(pathData_csv) as csv_file:
        # Read CSV data
        csv_reader = csv.DictReader(csv_file)
        # Convert to JSON
        json_data = json.dumps([row for row in csv_reader])

    # Print JSON data
    #print(json_data)

    pathData_json = data_json

    parsed = json.loads(json_data)

    with open(pathData_json, 'w', encoding='utf-8') as json_file_handler:
        json_file_handler.write('{' + '\n')
        json_file_handler.write('"instances":' + '\n')
        json_file_handler.write(json.dumps(parsed, indent=4, sort_keys=True))
        json_file_handler.write('\n' + '}')
    print("Preparacion de datos finalizada")


def analizarModeloAI(apiModel, data_json, resApi, res):
    # Define los datos que se enviarán como JSON
    dataLimpiaJson = data_json
    resAPI = resApi
    res = res
    # Lee el archivo JSON
    with open(dataLimpiaJson, 'r') as f:
        data_json = json.load(f)
    # Convierte los datos a un objeto JSON
    json_data = json.dumps(data_json)
    # Define las cabeceras HTTP para indicar que se está enviando JSON
    headers = {'Content-type': 'application/json'}
    # Envía la solicitud HTTP POST a la API REST con los datos JSON y las cabeceras
    response = requests.post(apiModel, data=json_data, headers=headers)
    # Guardamos la respuesta en una archvivo txt
    with open(resAPI, 'w') as f:
        json.dump(response.json(), f)

    data1 = data_json
    data2 = response.json()


    # Al archivo data_json adicionamos un atributo prediccions donde se encuentra toda la prediccion del modelo
    for i, instance in enumerate(data1["instances"]):
        instance["predictions"] = data2["predictions"][i]
    # Convertir el objeto Python combinado a JSON
    json_result = json.dumps(data1)
    # Guardando resultado
    with open(res, 'w') as f:
        f.write(json_result)

    #Obteniedo ubicacion de las ip
    with open(res, 'r') as f:
        json_data = json.load(f)

    result = subprocess.run(['curl', 'ifconfig.co/'], stdout=subprocess.PIPE)
    what_is_my_ip = result.stdout.decode()
    print(what_is_my_ip)

    pathFile = PathFiles()
    api_geoip_1 = pathFile.api_geoip_1
    api_geoip_2 = pathFile.api_geoip_2

    for instance in json_data["instances"]:
        ip = instance["originaldst_layer3"]
        # url = f"https://api.iplocation.net/?ip={ip}"
        ip_location = {"country": " ", "stateprov": " ", "stateprovCode": " ", "city": " ", "latitude": " ",
                       "longitude": " ", "continent": " ", "timezone": " ", "accuracyRadius": 0, "asn": 0,
                       "asnOrganization": " ", "asnNetwork": " "}
        instance["ip_location"] = ip_location

        #url = f"http://localhost:8090/{ip}"
        url = api_geoip_1 + ip
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            ip_location = response.json()
            #print(ip_location)
            if "country" in ip_location:
                instance["ip_location"]["country"] = str(ip_location["country"])
            if "stateprov" in ip_location:
                instance["ip_location"]["stateprov"] = str(ip_location["stateprov"])
            if "stateprovCode" in ip_location:
                instance["ip_location"]["stateprovCode"] = str(ip_location["stateprovCode"])
            if "city" in ip_location:
                instance["ip_location"]["city"] = str(ip_location["city"])
            if "latitude" in ip_location:
                instance["ip_location"]["latitude"] = str(ip_location["latitude"])
            if "longitude" in ip_location:
                instance["ip_location"]["longitude"] = str(ip_location["longitude"])
            if "continent" in ip_location:
                instance["ip_location"]["continent"] = str(ip_location["continent"])
            if "timezone" in ip_location:
                instance["ip_location"]["timezone"] = str(ip_location["timezone"])
            if "accuracyRadius" in ip_location:
                instance["ip_location"]["accuracyRadius"] = str(ip_location["accuracyRadius"])
            if "asn" in ip_location:
                instance["ip_location"]["asn"] = str(ip_location["asn"])
            if "asnOrganization" in ip_location:
                instance["ip_location"]["asnOrganization"] = str(ip_location["asnOrganization"])
            if "asnNetwork" in ip_location:
                instance["ip_location"]["asnNetwork"] = str(ip_location["asnNetwork"])
        else:
            what_is_my_ip = what_is_my_ip.replace("\n", "")
            #url = f"http://localhost:8090/{what_is_my_ip}"
            #url = f"http://177.222.49.52:8083/{what_is_my_ip}"
            url = api_geoip_1 + ip
            response = requests.get(url)
            if response.status_code == 200:
                ip_location = response.json()
                instance["ip_location"]["asnOrganization"] = 'Private IP Address LAN'
                instance["ip_location"]["asnNetwork"] = 'LAN'
            else:
                print('Ip no encontrada, buscando en la api iplocation')
                # url = f"https://api.iplocation.net/?ip={ip}"
                #url = f"https://api.ip2location.io/?key=06FB985059AEACBE0C067EF43FD9B4AB&ip={ip}"
                url = api_geoip_2 + ip
                response = requests.get(url)
                if response.status_code == 200:
                    ip_location = response.json()
                    instance["ip_location"]["country"] = str(ip_location["country_code"])
                    instance["ip_location"]["city"] = str(ip_location["city_name"])
                    instance["ip_location"]["latitude"] = str(ip_location["latitude"])
                    instance["ip_location"]["longitude"] = str(ip_location["longitude"])
                    instance["ip_location"]["timezone"] = str(ip_location["time_zone"])
                    instance["ip_location"]["asn"] = str(ip_location["asn"])

    #print(json.dumps(json_data))
    print("Latitud y longitud de la ip encontradas.")
    with open(res, 'w') as f:
        f.write(json.dumps(json_data))
def guardandoBackupResultado_M1(res_m1):
    resultM1 = res_m1
    connectionPostgresql = ConnectionPostgresql()
    conn = connectionPostgresql.beginConnection()

    # Cargar archivo JSON
    with open(resultM1, 'r') as f:
        data = json.load(f)
    ipBackList = []

    try:
        cur = conn.cursor()
        # Iterar a través de las instancias
        for instance in data['instances']:
            bad_traffic = str(instance["bad_traffic"])
            estado = str(instance["estado"])
            frecuencia = str(instance["frecuencia"])
            originalbytes = str(instance["originalbytes"])
            originaldst_layer3 = str(instance["originaldst_layer3"])
            originalpackets = str(instance["originalpackets"])
            originalprotoname_layer4 = str(instance["originalprotoname_layer4"])
            originalprotoum_layer4 = str(instance["originalprotoum_layer4"])
            originalsrc_layer3 = str(instance["originalsrc_layer3"])
            replybytes = str(instance["replybytes"])
            replydport_layer4 = str(instance["replydport_layer4"])
            replypackets = str(instance["replypackets"])
            replyprotoum_layer4 = str(instance["replyprotoum_layer4"])
            replysport_layer4 = str(instance["replysport_layer4"])
            timeout = str(instance["timeout"])
            use = str(instance["use"])
            datetime = str(instance["datetime"])
            scores = instance['predictions']['scores']
            predicction_0 = str(scores[0])
            predicction_1 = str(scores[1])
            country = str(instance['ip_location']["country"])
            stateprov = str(instance['ip_location']["stateprov"])
            stateprovCode = str(instance['ip_location']["stateprovCode"])
            city = str(instance['ip_location']["city"])
            latitude = str(instance['ip_location']["latitude"])
            longitude = str(instance['ip_location']["longitude"])
            continent = str(instance['ip_location']["continent"])
            timezone = str(instance['ip_location']["timezone"])
            accuracyRadius = str(instance['ip_location']["accuracyRadius"])
            asn = str(instance['ip_location']["asn"])
            asnOrganization = str(instance['ip_location']["asnOrganization"])
            asnNetwork = str(instance['ip_location']["asnNetwork"])

            query = "INSERT INTO resultado_m1 (bad_traffic, estado, frecuencia, originalbytes, originaldst_layer3, originalpackets, originalprotoname_layer4, originalprotoum_layer4, originalsrc_layer3, replybytes, replydport_layer4, replypackets, replyprotoum_layer4, replysport_layer4, timeout, use, datetime, predictions, predicction_0, predicction_1, country, stateprov, stateprovcode, city, latitude, longitude, continent, timezone, accuracyradius, asn, asnorganization, asnnetwork)" \
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "

            record_to_insert = (bad_traffic, estado, frecuencia, originalbytes, originaldst_layer3, originalpackets, originalprotoname_layer4, originalprotoum_layer4, originalsrc_layer3, replybytes, replydport_layer4, replypackets, replyprotoum_layer4, replysport_layer4, timeout, use, datetime, scores, predicction_0, predicction_1, country, stateprov, stateprovCode, city, latitude, longitude, continent, timezone, accuracyRadius, asn, asnOrganization, asnNetwork)

            cur.execute(query, record_to_insert)
            conn.commit()
        print("OK >>> Se subieron los datos del modelo 1, exitosamente!!!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error >> En el rol detecta:  al ejecutar la query subida de modelo 1:", error)

def guardandoBackupResultado_M2(res_m2):
    resultM1 =  res_m2
    connectionPostgresql = ConnectionPostgresql()
    conn = connectionPostgresql.beginConnection()

    # Cargar archivo JSON
    with open(resultM1, 'r') as f:
        data = json.load(f)
    ipBackList = []

    try:
        print("subiendo resultado de modelo 2 a la base de datos>>>>")
        cur = conn.cursor()
        # Iterar a través de las instancias
        for instance in data['instances']:
            bad_traffic = str(instance["bad_traffic"])
            estado = str(instance["estado"])
            frecuencia = str(instance["frecuencia"])
            originalbytes = str(instance["originalbytes"])
            originaldst_layer3 = str(instance["originaldst_layer3"])
            originalpackets = str(instance["originalpackets"])
            originalprotoname_layer4 = str(instance["originalprotoname_layer4"])
            originalprotoum_layer4 = str(instance["originalprotoum_layer4"])
            originalsrc_layer3 = str(instance["originalsrc_layer3"])
            replybytes = str(instance["replybytes"])
            replydport_layer4 = str(instance["replydport_layer4"])
            replypackets = str(instance["replypackets"])
            replyprotoum_layer4 = str(instance["replyprotoum_layer4"])
            replysport_layer4 = str(instance["replysport_layer4"])
            timeout = str(instance["timeout"])
            use = str(instance["use"])
            datetime = str(instance["datetime"])
            scores = instance['predictions']['scores']
            predicction_0 = str(scores[0])
            predicction_1 = str(scores[1])
            country = str(instance['ip_location']["country"])
            stateprov = str(instance['ip_location']["stateprov"])
            stateprovCode = str(instance['ip_location']["stateprovCode"])
            city = str(instance['ip_location']["city"])
            latitude = str(instance['ip_location']["latitude"])
            longitude = str(instance['ip_location']["longitude"])
            continent = str(instance['ip_location']["continent"])
            timezone = str(instance['ip_location']["timezone"])
            accuracyRadius = str(instance['ip_location']["accuracyRadius"])
            asn = str(instance['ip_location']["asn"])
            asnOrganization = str(instance['ip_location']["asnOrganization"])
            asnNetwork = str(instance['ip_location']["asnNetwork"])

            query = "INSERT INTO resultado_m2(bad_traffic, estado, frecuencia, originalbytes, originaldst_layer3, originalpackets, originalprotoname_layer4, originalprotoum_layer4, originalsrc_layer3, replybytes, replydport_layer4, replypackets, replyprotoum_layer4, replysport_layer4, timeout, use, datetime, predictions, predicction_0, predicction_1, country, stateprov, stateprovcode, city, latitude, longitude, continent, timezone, accuracyradius, asn, asnorganization, asnnetwork)" \
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "

            record_to_insert = (bad_traffic, estado, frecuencia, originalbytes, originaldst_layer3, originalpackets, originalprotoname_layer4, originalprotoum_layer4, originalsrc_layer3, replybytes, replydport_layer4, replypackets, replyprotoum_layer4, replysport_layer4, timeout, use, datetime, scores, predicction_0, predicction_1, country, stateprov, stateprovCode, city, latitude, longitude, continent, timezone, accuracyRadius, asn, asnOrganization, asnNetwork)

            cur.execute(query, record_to_insert)
            conn.commit()
        print("OK >>> Se subieron los datos del modelo 2, exitosamente!!!")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error >>> al ejecutar la query subida de modelo 2 :", error)

def analizarModel_1(apiModel_1, data_json, resApi_m1, res_m1):
    analizarModeloAI(apiModel_1, data_json, resApi_m1, res_m1)
    guardandoBackupResultado_M1(res_m1)

def analizarModel_2(apiModel_2, data_json, resApi_m2, res_m2):
    analizarModeloAI(apiModel_2, data_json, resApi_m2, res_m2)
    guardandoBackupResultado_M2(res_m2)

def combinacionDeResultados(res_m1, res_m2, resultadoFinal):
    data1 = res_m1
    data2 = res_m2
    resultadoFinal = resultadoFinal

    with open(data1, 'r') as f:
        json1 = json.load(f)

    with open(data2, 'r') as f:
        json2 = json.load(f)

    # Unir los dos JSON
    json1["instances"].extend(json2["instances"])

    # Convertir a JSON
    resultado = json.dumps(json1)

    # Imprimir el resultado
    #print(resultado)

    with open(resultadoFinal, 'w') as f:
        f.write(resultado)


'''
<<<<<< MAIN >>>>>>

'''
class B_Guardar_conexiones_sospechosas(PathFiles,ConnectionPostgresql):

    def __init__(self ):
        pass
    def procesadorDetecta(self):
        print("Rol 2: Procesador detecta ........")
        path = PathFiles()
        prepararDatasParaAPI(path.data_csv, path.data_json)

        analizarModel_1(path.apiModel_1, path.data_json, path.resApi_m1, path.res_m1)
        analizarModel_2(path.apiModel_2, path.data_json, path.resApi_m2, path.res_m2)

        combinacionDeResultados(path.res_m1, path.res_m2, path.resultadoFinal)
        print("Rol 2: Procesador detecta .............OK")

    def procesadorResultados(self):
        print("Rol 2: Procesador resultados ........")
        #Generar estadisticas de la tabla estadodeconexiones
        connectionPostgresql = ConnectionPostgresql()
        conn = connectionPostgresql.beginConnection()
        try:
            cur = conn.cursor()
            query = "SELECT  predicction_1, originalsrc_layer3, originaldst_layer3, country, latitude, longitude, asnorganization " \
                    "FROM public.resultado_m1 " \
                    "WHERE CAST(predicction_1 AS DECIMAL) > 0.90 " \
                    "UNION " \
                    "SELECT  predicction_1, originalsrc_layer3, originaldst_layer3, country, latitude, longitude, asnorganization " \
                    "FROM public.resultado_m2 " \
                    "WHERE CAST(predicction_1 AS DECIMAL) > 0.90 "
            # ejecucion query
            cur.execute(query)
            # Obtener resultados y guardarlos en una lista
            results = cur.fetchall()

            for result in results:
                predicction_1 = result[0]
                originalsrc_layer3 = result[1]
                originaldst_layer3 = result[2]
                country = result[3]
                latitude = result[4]
                longitude = result[5]
                asnorganization = result[6]

                query = "INSERT INTO resultado_final (predicction_1, originalsrc_layer3, originaldst_layer3, country, latitude, longitude, asnorganization) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                cur.execute(query, (
                predicction_1, originalsrc_layer3, originaldst_layer3, country, latitude, longitude, asnorganization))

            query = "DELETE FROM resultado_final a " \
                    "USING resultado_final b " \
                    "WHERE a.id > b.id " \
                    "AND a.originaldst_layer3 = b.originaldst_layer3 "
            cur.execute(query)

            print("OK >>> Se finalizo la generacion de los resultados para el grafico 1 del mapa")
            conn.commit()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error >>> Rol 3 al ejecutar la query:", error)
        print("Rol 3: Procesador resultados ........")

    def a_guardarConexionesSospechosas(self):
        print("Accion 2: Guardar conexiones sospechosas en la base de datos .............")
        path = PathFiles()
        resultados = path.resultadoFinal

        connectionPostgresql = ConnectionPostgresql()
        conn = connectionPostgresql.beginConnection()

        # Cargar archivo JSON
        with open(resultados, 'r') as f:
            data = json.load(f)
        ipBackList = []

        try:
            cur = conn.cursor()
            for ip in ipBackList:
                query = "SELECT  resultado_final (ip) VALUES ('{}');".format(ip)
                # print(query)
                cur.execute(query)
                conn.commit()
            print("Accion 2: Guardar conexiones sospechosas en la base de datos .............OK")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error >> Accion 2: Guardar conexiones sospechosas en la base de datos.",error)

        # print(ipBackList)
        try:
            cur = conn.cursor()
            for ip in ipBackList:
                query = "INSERT INTO iptablesrulesa7 (ip) VALUES ('{}');".format(ip)
                # print(query)
                cur.execute(query)
                conn.commit()
            print("Accion 2: Guardar conexiones sospechosas en la base de datos .............OK")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error >> Accion 2: Guardar conexiones sospechosas en la base de datos.",error)





