from flask import Flask
from app.extensions import db,migrate,jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.users.user_controller import users
from app.controllers.companies.company_controller import companies
from app.controllers.books.book_controller import books
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

#application factory function
def create_app():
    
    #app instance
    app = Flask(__name__,static_url_path='/static')
  
    app.config.from_object('config.Config')

    SWAGGER_URL = '/api/docs'  
    API_URL = '/static/docs.json' 
    
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
   

   # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={  
        'app_name': "Test application"
    },

   )

    CORS(app) 



     #Importing and registering models

    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book
    


    #registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(companies)
    app.register_blueprint(books)

    app.register_blueprint(swaggerui_blueprint)




    @app.route("/")
    def home():
        return "Authors API Project setup 1"
    
  
    
    

    return app

