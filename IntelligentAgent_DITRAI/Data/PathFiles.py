from pathlib import Path

class PathFiles:

    pathRoot = '/home/michael/Documents/thesis/DITRai_private/'

    apiModel_1 = 'http://177.222.49.52:8081/predict'
    apiModel_2 = 'http://177.222.49.52:8082/predict'
    api_geoip_1 = 'http://177.222.49.52:8083/'
    api_geoip_2 = 'https://api.ip2location.io/?key=06FB985059AEACBE0C067EF43FD9B4AB&ip='

    '''
    Data del tabla estado de conexiones
    '''
    data_csv = Path(pathRoot + 'IntelligentAgent_DITRAI/data.csv')
    data_json = Path(pathRoot + 'IntelligentAgent_DITRAI/BusinessLogic/Files/data.json')
    '''
    Json respuesta de los modelos
    '''
    res_m1 = Path(pathRoot + "IntelligentAgent_DITRAI/BusinessLogic/Files/res_m1.json")
    res_m2 = Path(pathRoot + "IntelligentAgent_DITRAI/BusinessLogic/Files/res_m2.json")

    '''
    union del data.json con la respuesta  res_m1.json de los modelos 
    en un solo archivo json 
    '''
    resApi_m1 = Path(pathRoot + "IntelligentAgent_DITRAI/BusinessLogic/Files/resApi_m1.json")
    resApi_m2 = Path(pathRoot + "IntelligentAgent_DITRAI/BusinessLogic/Files/resApi_m2.json")

    resultadoFinal = Path(pathRoot + "IntelligentAgent_DITRAI/BusinessLogic/Files/resultadoFinal.json")

    firewallUser = Path(pathRoot + "IntelligentAgent_DITRAI/BusinessLogic/Files/firewall.user")

    #db
    dbRoute = Path(pathRoot + "IntelligentAgent_DITRAI/database/database.db")

    def __init__(self):
        super(PathFiles, self).__init__()