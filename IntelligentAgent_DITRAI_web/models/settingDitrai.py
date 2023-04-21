from main import db

class SettingDitrai(db.Model):
    __tablename__="setting"
    id:int=db.Column(db.Integer,primary_key=True)
    chatId:str=db.Column(db.String(50))
    telegramToken:str=db.Column(db.String(300))
    monitorSystem:str=db.Column(db.Integer)
    frecuencyGetTableTrafict:str=db.Column(db.Integer)
    timeFrecuencyGetTableTrafict:str=db.Column(db.Integer)
    beginEnd:str=db.Column(db.Integer)
    

    def __init__(self,chatId,telegramToken,monitorSystem, frecuencyGetTableTrafict, timeFrecuencyGetTableTrafict, beginEnd):
        self.chatId = chatId
        self.telegramToken = telegramToken
        self.monitorSystem = monitorSystem
        self.frecuencyGetTableTrafict = frecuencyGetTableTrafict
        self.timeFrecuencyGetTableTrafict = timeFrecuencyGetTableTrafict
        self.beginEnd = beginEnd


        