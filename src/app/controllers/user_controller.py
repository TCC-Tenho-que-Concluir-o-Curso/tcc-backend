from firebase_admin import auth
from app import app, spec
from flask import request, jsonify
from flask_pydantic_spec import (Response, Request)
from json import loads
from app.controllers.utils import get_user_type

from app.models.user_model import User

# @app.before_request
# def verify_firebase_auth():
#     try:
#         # Extract Firebase UID from the Authorization header
#         # Example: Firebase UID as a Bearer token
#         firebase_uid = request.headers.get('Authorization')
#         print("FIREBASE UID", firebase_uid)

#         # Verify the Firebase UID
#         user = auth.get_user(firebase_uid)

#         # Store the authenticated user in the request context
#         request.user = user
#         # return from middleware

#     except Exception as e:
#         # Authentication failed, return an authentication error
#         return jsonify({"error": "Authentication failed."}), 401


def delete_all_users():
    users = User.objects()
    for user in users:
        user.delete()


@app.post('/user')
def add_or_replace_user():
    """
    - ADD/Replace user to bd.
    """
    # delete_all_users()
    print("FAZENDO LOGIN")
    firebase_uid = request.json.get('firebase_uid')
    avatar_url = request.json.get('avatar_url')
    email = request.json.get('email')
    name = request.json.get('name')
    type = get_user_type(email)

    if type is None:
        return jsonify({'message': 'Use um email acadêmico para logar.'}), 400

    user = User.objects(firebase_uid=firebase_uid).first()

    if user:
        user.update(type=type, avatar_url=avatar_url, email=email,
                    name=name)
        print("User atualizado.")
        return jsonify({'message': 'User atualizado.'}), 200

    user = User(firebase_uid=firebase_uid, type=type, avatar_url=avatar_url,
                email=email, name=name)

    user.save()

    print("User adicionado.")

    resp = user.to_mongo().to_dict()
    resp.pop('_id')

    return jsonify(resp), 201


@app.get('/user/<firebase_uid>')
def get_user_by_firebase_uid(firebase_uid):
    user = User.objects(firebase_uid=firebase_uid).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    resp = user.to_mongo().to_dict()
    resp.pop('_id')

    return resp


@app.get('/user/email/<email>')
def get_user_by_email(email):
    user = User.objects(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    resp = user.to_mongo().to_dict()
    resp.pop('_id')

    return resp
