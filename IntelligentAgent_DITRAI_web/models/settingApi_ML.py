from main import db

class SettingApi_ML(db.Model):
    __tablename__="api_ML"
    id:int=db.Column(db.Integer,primary_key=True)
    model_1:str=db.Column(db.String(300))
    model_2:str=db.Column(db.String(300))
    

    def __init__(self, model_1, model_2):
        self.model_1 = model_1
        self.model_2 = model_2


        