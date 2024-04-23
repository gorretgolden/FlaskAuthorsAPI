from app.extensions import db
from datetime import datetime


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    origin = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text(),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    user = db.relationship('User',backref='companies')
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())


    def __init__(self,name,origin,description,user_id):
        super(Company, self).__init__()
        self.name = name
        self.origin = origin
        self.description = description
        self.user_id = user_id

      
    def __repr__(self):
        return  f"{self.name} {self.origin}"
        

