from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK 
import validators
from app.models.companies import    Company
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity


#company blueprint
companies = Blueprint('companies', __name__,url_prefix='/api/v1/companies')


#creating companies
@companies.route('/create',methods=['POST'])
@jwt_required()
def createCompany():

    #storing request values
    data = request.json
    origin = data.get('origin')
    description = data.get('description')
    user_id = get_jwt_identity()
    name = data.get('name')


    #validations of the incoming request

    if not name or not origin or not description :
        return jsonify({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    
    
    if Company.query.filter_by(name=name).first() is not None:
        return jsonify({"error":"Company name already in use"}),HTTP_409_CONFLICT
 
    try:

       #creating a new company
       new_company = Company(name=name,origin=origin,description=description,user_id=user_id)
       db.session.add(new_company)
       db.session.commit()


       return jsonify({
           'message':name + " has been created successfully ",
           'user':{
               'id':new_company.id,
               "name":new_company.name,
               "origin":new_company.origin,
               "description": new_company.description,

           }
       }),HTTP_201_CREATED

    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR

    
    

