from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK 
import validators
from app.models.users import User
from flask_jwt_extended import jwt_required

#auth blueprint
users = Blueprint('users', __name__,url_prefix='/api/v1/users')


  

@users.route('/', methods=['GET'])
@jwt_required()
def get_all_authors():
    try:
        
        all_users = User.query.all()
     
        users_list = []

     
        for user in all_users:
            user_info = {
               'id': user.id,
               'username': user.get_full_name(),
                'email': user.email,
                'contact': user.contact,
                'user_type': user.user_type,
                'created_at': user.created_at,
                    }
         
            users_list.append(user_info)
        return jsonify({'users': users_list})

    except Exception as e:
        
        return jsonify({'error': str(e)}), 500




   


