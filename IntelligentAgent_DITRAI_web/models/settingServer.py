from main import db

class SettingServer(db.Model):
    __tablename__="connection_DB"
    id:int=db.Column(db.Integer,primary_key=True)
    dbName:str=db.Column(db.String(250))
    userDB:str=db.Column(db.String(250))
    passwordDB:str=db.Column(db.String(250))
    hostDB:str=db.Column(db.String(250))
    portDB:str=db.Column(db.Integer)

    def __init__(self, dbName, userDB, passwordDB, hostDB, portDB):
        self.dbName = dbName
        self.userDB = userDB
        self.passwordDB = passwordDB
        self.hostDB = hostDB
        self.portDB = portDB


