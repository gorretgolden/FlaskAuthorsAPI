from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK 
import validators
from app.models.users import User
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity


#users blueprint
users = Blueprint('users', __name__,url_prefix='/api/v1/users')


#Getting all users from the database
@users.get('/')
@jwt_required()
def getAllUsers():

    try:

        all_users = User.query.all()

        users_data = []

        for user in all_users:
            user_info ={
                'id':user.id,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'username':user.get_full_name(),
                'email':user.email,
                'contact':user.contact,
                'type':user.user_type,
                'created_at':user.created_at

            }
            users_data.append(user_info)


        return jsonify({

            "message":"All users retrieved successfully",
            "total_users": len(users_data),
            "users": users_data

        }), HTTP_200_OK



    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR



#Get all authors endpoint
@users.get('/authors')
@jwt_required()
def getAllAuthors():

    try:

        all_authors = User.query.filter_by(user_type='author').all()

        authors_data = []

        for author  in all_authors:
            author_info ={
                'id':author.id,
                'first_name':author.first_name,
                'last_name':author.last_name,
                'name':author.get_full_name(),
                'email':author.email,
                'contact':author.contact,
                'biography':author.biography,
                'created_at':author.created_at,
                'companies': [],
                'books':[]

            }

            if  hasattr(author,'books'):
                author_info['books'] = [ { 'id': book.id, 'title':book.title,'price':book.price,'genre':book.id, "price_unit":book.price_unit,'description':book.description,'publicaation':book.publication_date,'image':book.image,'created_at':book.created_at} for book in author.books]
          
          
            if hasattr(author,'companies'):
                author_info['companies'] = [{'id':company.id,'name':company.name,'origin':company.origin} for company in author.companies]
            
            authors_data.append(author_info)


        return jsonify({

            "message":"All authors retrieved successfully",
            "total": len(authors_data),
            "authors": authors_data

        }), HTTP_200_OK



    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR




#Get a user by id
@users.get('/user/<int:id>')
@jwt_required()
def getUser(id):

    try:

        user = User.query.filter_by(id=id).first()

        books = []
        companies = []

    

        if  hasattr(user,'books'):
                books = [ { 'id': book.id, 'title':book.title,'price':book.price,'genre':book.id, "price_unit":book.price_unit,'description':book.description,'publicaation':book.publication_date,'image':book.image,'created_at':book.created_at} for book in user.books]
          
          
        if hasattr(user,'companies'):
                companies = [{'id':company.id,'name':company.name,'origin':company.origin} for company in user.companies]
            
        


        return jsonify({

            "message":"User details retrieved successfully",

            "user": {
                   'id':user.id,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'username':user.get_full_name(),
                'email':user.email,
                'contact':user.contact,
                'type':user.user_type,
                'biography':user.biography,
                'created_at':user.created_at,
                'companies':companies,
                'books':books
                 
            }

        }), HTTP_200_OK



    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


   







    


