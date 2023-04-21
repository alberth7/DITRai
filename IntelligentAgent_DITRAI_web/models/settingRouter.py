from main import db

class SettingRouter(db.Model):
    __tablename__="router"
    id:int=db.Column(db.Integer,primary_key=True)
    host:str=db.Column(db.String(50))
    user:str=db.Column(db.String(50))
    password:str=db.Column(db.String(300))
    port:str=db.Column(db.Integer)
    sshPath:str=db.Column(db.String(300))

    def __init__(self, host, user, password, port, sshPath):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.sshPath = sshPath



