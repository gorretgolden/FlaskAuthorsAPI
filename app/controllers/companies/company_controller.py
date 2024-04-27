from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN,HTTP_404_NOT_FOUND,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK 
import validators
from app.models.companies import  Company
from app.models.users import    User
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
           'company':{
               'id':new_company.id,
               "name":new_company.name,
               "origin":new_company.origin,
               "description": new_company.description,

           }
       }),HTTP_201_CREATED

    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR


#get all companies
@companies.get('/')
@jwt_required()
def getAllCompanies():

    try:

        all_companies = Company.query.all()

        companies_data = []

        for company in all_companies:
            company_info ={
                'id':company.id,
                'name':company.name,
                'description':company.description,
                'origin':company.origin,
                'user':{
                    'first_name':company.user.first_name,
                    'last_name':company.user.last_name,
                    'username':company.user.get_full_name(),
                    'email':company.user.email,
                    'contact':company.user.contact,
                    'type':company.user.user_type,
                    'biography':company.user.biography,
                    'created_at':company.user.created_at

                },
                'created_at':company.created_at

            }
            companies_data.append(company_info)


        return jsonify({

            "message":"All companies retrieved successfully",
            "total_companies": len(companies_data),
            "companies": companies_data

        }), HTTP_200_OK



    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


    
    
#get company by id
@companies.get('/company/<int:id>')
@jwt_required()
def getCompany(id):

    try:

        company = Company.query.filter_by(id=id).first()

        if not company:
           return jsonify({"error":"Company not found"}),HTTP_404_NOT_FOUND

    
        return jsonify({

            "message":"Company details retrieved successfully",

            "company": {
                    'id':company.id,
                    'name':company.name,
                    'description':company.description,
                    'origin':company.origin,
                   'user':{
                    'first_name':company.user.first_name,
                    'last_name':company.user.last_name,
                    'username':company.user.get_full_name(),
                    'email':company.user.email,
                    'contact':company.user.contact,
                    'type':company.user.user_type,
                    'biography':company.user.biography,
                    'created_at':company.user.created_at

                },
                'created_at':company.created_at
            }

        }), HTTP_200_OK



    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR



#update company details
@companies.route('/edit/<int:id>',methods=['PUT','PATCH'])
@jwt_required()
def updateCompanyDetails(id):

    try:
       current_user = get_jwt_identity()
       loggedInUser = User.query.filter_by(id=current_user).first()

       #get company by id
       company = Company.query.filter_by(id=id).first() 

       if not company:
           return jsonify({"error":"Company not found"}),HTTP_404_NOT_FOUND
       
       elif loggedInUser.user_type!='admin' and company.user_id!=current_user:
           return jsonify({"error": "You are not authorized to update the company details"}),HTTP_403_FORBIDDEN
       
       else:
            #store request data

            name = request.get_json().get('name',company.name)
            origin = request.get_json().get('origin',company.origin)
            description = request.get_json().get('description',company.description)
           
            
            if name != company.name and Company.query.filter_by(name=name).first():
                return jsonify({
                    "error":"Contact  already in use"
                }),HTTP_409_CONFLICT
            
            

            company.name = name
            company.origin = origin
            company.description = description

            db.session.commit()


            return jsonify({
               'message':name + "'s details have been successfully updated " ,
               'company':{
                      'id':company.id,
                    'name':company.name,
                    'description':company.description,
                    'origin':company.origin,
                   'user':{
                    'first_name':company.user.first_name,
                    'last_name':company.user.last_name,
                    'username':company.user.get_full_name(),
                    'email':company.user.email,
                    'contact':company.user.contact,
                    'type':company.user.user_type,
                    'biography':company.user.biography,
                    'created_at':company.user.created_at

                },
                'created_at':company.created_at
          
              }
            })
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
