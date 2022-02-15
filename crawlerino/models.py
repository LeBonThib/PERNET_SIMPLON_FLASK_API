from crawlerino import db

class tablerino(db.Model):
    json_id = db.Column(db.Integer, primary_key=True)
    json_objecterino = db.Column(db.String(50000))
    json_urlerino = db.Column(db.String(50000))