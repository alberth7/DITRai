from flask import Blueprint, render_template,request,redirect,flash, url_for
from models.settingDitrai import SettingDitrai, db
import subprocess
import unittest
import psycopg2
import folium
from flask_table import Table, Col

database=""
user = ""
password = ""
host = ""
port = ""

home=Blueprint("home",__name__,url_prefix="/",template_folder="../templates/home")
pathFileFirewall  = "/home/michael/Documents/thesis/DITRai_private/IntelligentAgent_DITRAI/BusinessLogic/Files/firewall.user"

@home.route("/home", methods=['GET'])
def index():
    settings = SettingDitrai.query.first()     
    return render_template("index.html",settings=settings)

@home.route("/header")
def header():
    return render_template('header.html')

@home.route("/estadisticas")
def estadisticas():
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    try:
        cur = conn.cursor()

        query = "SELECT predicction_1, originaldst_layer3, latitude, longitude, asnorganization " \
                "FROM resultado_final "
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        rint("Error >>> al ejecutar la query:", error)

    # Ejemplo de datos en formato JSON
    #data = [{"predicction_1": "0.99","originaldst_layer3": "10.0.1.60", "latitude": "39.1027", "longitude": "-94.5778",  "asnOrganization": "GOOGLE-CLOUD-PLATFORM"},
    #        {"predicction_1": "0.96","originaldst_layer3": "177.117.65.55","latitude": "38.1027", "longitude": "-99.5778",  "asnOrganization": "Tigo"}]
    
    data = resultados
    print(data)
    # Crear un mapa con la biblioteca folium
    map = folium.Map(location=[10, 10], zoom_start=2)

    # Añadir marcadores al mapa para cada ubicación en el JSON
    for item in data:
        # Extraer las coordenadas y la información del punto
        prediccion = item[0]
        dst = item[1]
        lat = float(item[2])
        lon = float(item[3])
        org = item[4]

        # Crear un marcador y añadirlo al mapa
        marker = folium.Marker(location=[lat, lon], popup="Predicción: "+prediccion + "<br>" +"IP: " + dst + "<br>" + "ASN Organización: " + org, icon=folium.Icon(color='red'))
        marker.add_to(map)

    # Convertir el mapa a HTML y devolverlo
    html_map = map._repr_html_()
    
    ip_list = [tupla[1] for tupla in data]

    return render_template('estadisticas.html', html_map=html_map, datos=ip_list)


@home.route("/estadisticas", methods=['POST'])
def estadisticas_post():
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    try:
        cur = conn.cursor()

        query = "SELECT predicction_1, originaldst_layer3, latitude, longitude, asnorganization " \
                "FROM resultado_final "
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        rint("Error >>> al ejecutar la query:", error)

    # Ejemplo de datos en formato JSON
    #data = [{"predicction_1": "0.99","originaldst_layer3": "10.0.1.60", "latitude": "39.1027", "longitude": "-94.5778",  "asnOrganization": "GOOGLE-CLOUD-PLATFORM"},
    #        {"predicction_1": "0.96","originaldst_layer3": "177.117.65.55","latitude": "38.1027", "longitude": "-99.5778",  "asnOrganization": "Tigo"}]
    
    data = resultados
    print(data)
    # Crear un mapa con la biblioteca folium
    map = folium.Map(location=[10, 10], zoom_start=2)

    # Añadir marcadores al mapa para cada ubicación en el JSON
    for item in data:
        # Extraer las coordenadas y la información del punto
        prediccion = item[0]
        dst = item[1]
        lat = float(item[2])
        lon = float(item[3])
        org = item[4]

        # Crear un marcador y añadirlo al mapa
        marker = folium.Marker(location=[lat, lon], popup="Predicción: "+prediccion + "<br>" +"IP: " + dst + "<br>" + "ASN Organización: " + org, icon=folium.Icon(color='red'))
        marker.add_to(map)

    # Convertir el mapa a HTML y devolverlo
    html_map = map._repr_html_()
    
    ip_list = [tupla[1] for tupla in data]

    item_seleccionado = request.form.get('item_seleccionado')

    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    try:
        cur = conn.cursor()

        query = "SELECT  originalsrc_layer3, originalprotoname_layer4, originalbytes, replybytes, originalpackets, replypackets, replysport_layer4, replydport_layer4, timeout, estado, frecuencia, datetime " \
                "FROM resultado_m1 " \
                "where originaldst_layer3 = '34.117.65.55'"
                #"where originaldst_layer3 = '" + item_seleccionado + "'"
        print(query)
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        print(resultados)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error >>> al ejecutar la query:", error)
    return render_template('estadisticas.html', html_map=html_map, datos=ip_list, table=resultados)



@home.route('/reglas_iptable')
def reglas_iptable():
    data  = pathFileFirewall
    with open(data, 'r') as f:
        datos = f.read()
    return render_template('reglas_iptable.html', datos=datos)

@home.cli.command()
def test():
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


def procesar_json(json_data):
    points = [{"originaldst_layer3": "34.117.65.55","originalsrc_layer3": "10.0.1.60","predicction_1": 0.999885082244873, "latitude": "39.1027", "longitude": "-94.5778", "continent": "NA",  "asnOrganization": "GOOGLE-CLOUD-PLATFORM"}, {"originaldst_layer3": "177.117.65.55","originalsrc_layer3": "10.0.1.60","predicction_1": 0.989885082244873, "latitude": "38.1027", "longitude": "-99.5778", "continent": "NA",  "asnOrganization": "Tigo"} ]
    for item in json_data:
        punto = {}
        punto['lat'] = item['latitude']
        punto['lon'] = item['longitude']
        punto['texto'] = f"Origen: {item['originalsrc_layer3']} \nDestino: {item['originaldst_layer3']} \nOrganización: {item['asnOrganization']}"
        points.append(punto)
    return points

def obtecionDatosMapa():
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    try:
        cur = conn.cursor()

        query = "SELECT predicction_1, originalsrc_layer3, originaldst_layer3, country, latitude, longitude, asnorganization" \
                "FROM resultado_final"
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return resultados
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error >>> al ejecutar la query:", error)


