from firebase_admin import auth
from app import app, spec
from flask import request, jsonify
from flask_pydantic_spec import (Response, Request)
from json import loads
from app.controllers.utils import get_user_type

from app.models.user_model import User


def delete_all_users():
    users = User.objects()
    for user in users:
        user.delete()


@app.post('/user')
def add_or_replace_user():
    """
    - ADD/Replace user to bd.
    """
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
