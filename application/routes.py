from flask import request, jsonify, abort
import hashlib
from application import app, db, config
import sys
import json
import datetime
import jwt
from functools import wraps
from bson import ObjectId


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        secret = json.dumps(config.JWT_SECRET_KEY, indent=4, sort_keys=True, default=str)
        auth = request.headers.get('Authorization', None)
        
        if auth is not None:
            parts = auth.split(" ")
            
            if parts[0].lower() != 'bearer':
                return jsonify({
                    "success": False,
                    'code': 'invalid_header',
                    'message': 'Authorization header must start with "Bearer".'
                }, 401)

            elif len(parts) == 1:
                return jsonify({
                    "success": False,
                    'code': 'invalid_header',
                    'message': 'Token not found.'
                }, 401)

            elif len(parts) > 2:
                return jsonify({
                    "success": False,
                    'code': 'invalid_header',
                    'description': 'Authorization header must be bearer token.'
                }, 401)
                
            token = parts[1]
            
            try:
                jwt.decode(token, secret, algorithms=['HS256'])
            except:
                return jsonify({"success": False, "message": "Unauthorized access"}), 401
            
            return f(*args, **kwargs)
        else:
            return jsonify({"success": False, "message": "unauthorized access"}), 401
        
    return decorator


@app.route('/register', methods=['POST'])
def register_user():
    try:
        body = request.get_json()

        body['password'] = hashlib.sha256(body["password"].encode("utf-8")).hexdigest()
        existing_user = db.user_collection.find_one({"email": body['email']})
        body['created'] = datetime.datetime.now()

        if existing_user is None:
            db.user_collection.insert_one(body)

            return jsonify({
                "success": True,
                "message": "User created successfully."
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": "User already exists"
            }), 409
    except:
        abort(400)


@app.route('/login', methods=['POST'])
def user_login():
    try:
        body = request.get_json()
        time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        secret = json.dumps(config.JWT_SECRET_KEY, indent=4,
                            sort_keys=True, default=str)

        find_db_user = db.user_collection.find_one({"email": body['email']})

        if find_db_user is not None:
            encrypt_password = hashlib.sha256(
                body['password'].encode("utf-8")).hexdigest()
            if encrypt_password == find_db_user['password']:
                access_token = jwt.encode(
                    {
                        "user": {
                            # "id": find_db_user['_id'],
                            "email": find_db_user['email'],
                            "first_name": find_db_user['first_name'],
                            "last_name": find_db_user['last_name'],
                        },
                        "exp": time
                    },
                    secret,
                    algorithm='HS256'
                )

                del find_db_user['password']

                return jsonify({
                    "success": True,
                    "message": "User login successfully",
                    "token": access_token
                }), 200

        return jsonify({
            "success": False,
            "message": "The username or password is incorrect"
        }), 401
    except:
        abort(400)


@app.route('/template', methods=['POST'])
@token_required
def create_template():
    try:
        body = request.get_json()
        body['created'] = datetime.datetime.now()
        
        db.template_collection.insert_one(body)
        
        return jsonify({
            "success": True,
            "message": "Template created successfully."
        }), 201
    except: 
        abort(400)
        
        
@app.route('/template', methods=['GET'])
@token_required
def templates():
    try:
        templates = []
        responses = db.template_collection.find().sort("_id", -1)
        
        for res in responses:
            res["_id"] = str(res["_id"])
            templates.append(res)
            
        return jsonify({
            "success": True,
            "statusCode": 200,
            "data": templates
        }), 200
    except:
        abort(400)
        
        
@app.route('/template/<template_id>', methods=['GET'])
@token_required
def single_template(template_id):
    try:
        template = db.template_collection.find_one({"_id": ObjectId(template_id)})
        print(template)
        if template is not None:
            template["_id"] = str(template["_id"])
                
        return jsonify({
            "success": True,
            "statusCode": 200,
            "data": template
        }), 200
    except:
        abort(400)
        
        
@app.route('/template/<template_id>', methods=['PUT'])
@token_required
def update_template(template_id):
    try:
        body = request.get_json()
        template = {}
        response = db.template_collection.update_one({"_id": ObjectId(template_id)}, { "$set": body})
        
        if response:
            template = db.template_collection.find_one({"_id": ObjectId(template_id)})
            if template is not None:
                template["_id"] = str(template["_id"])
                
        return jsonify({
            "success": True,
            "statusCode": 200,
            "data": template,
            "message": "Template updated successfully",
        }), 200
    except:
        abort(400)
        

@app.route('/template/<template_id>', methods=['DELETE'])
@token_required
def delete_template(template_id):
    try:
        response = db.template_collection.delete_one({"_id": ObjectId(template_id)})
        
        if response:
                
            return jsonify({
                "success": True,
                "statusCode": 200,
                "message": "Template deleted successfully",
            }), 200
    except:
        abort(404)