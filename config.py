from datetime import timedelta

class Config:
     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flask_authors_db'
     JWT_SECRET_KEY = "authors" 
     JWT_EXPIRATION_DELTA = timedelta(minutes=10)
#name,hw old is he, for how lng,,how did u meet him,where he  stays,does he know luganda,u need to learn 
     #some lunyakore 