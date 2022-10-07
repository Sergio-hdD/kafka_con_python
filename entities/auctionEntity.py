from importsAndConfigsApp import db
from datetime import datetime


class AuctionEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user_creator = db.Column(db.Integer)
    id_product = db.Column(db.Integer)
    amount_base = db.Column(db.Integer)
    start_date = db.Column(db.DateTime, default = datetime.now())
    end_date = db.Column(db.DateTime)
    id_user_last_offer = db.Column(db.Integer, nullable = True)
    date_last_offer = db.Column(db.DateTime, nullable = True)
    last_amount_offered = db.Column(db.Integer, nullable = True)

    def __init__(self, data): #constructor, se ejecuta cada vez que se instancia la clase
        self.id_user_creator = data['id_user_creator']
        self.id_product = data['id_product']
        self.amount_base = data['amount_base']
        self.end_date = data['end_date']
        self.id_user_last_offer = data['id_user_last_offer']
        self.date_last_offer = data['date_last_offer']
        self.last_amount_offered = data['last_amount_offered']

    def prepare_table_auction_and_get_db():
        return db


