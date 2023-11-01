from datetime import datetime
from firebase_admin import auth
from app import app, spec
from flask import request, jsonify
from flask_pydantic_spec import (Response, Request)
from json import loads
from app.utils import get_user_type
from app.models.comment_model import Comment

from app.models.tcc_model import TCC, User_Type


@app.before_request
def verify_firebase_auth():
    try:
        # Extract Firebase UID from the Authorization heade
        firebase_uid = request.headers.get('Authorization')
        print("FIREBASE UID", firebase_uid)

        # Verify the Firebase UID
        user = auth.get_user(firebase_uid)

        request.user = user

    except Exception as e:
        return jsonify({"error": "Authentication failed."}), 401


@app.post('/tcc')
# @spec.validate(body=Request(TCC_DTO), resp=Response(HTTP_201=TCC_DTO))
def add_tcc():
    """
    - ADD tcc to bd.
    """
    user = getattr(request, 'user', None)
    print("USER ID", user.uid)
    authorId = user.uid
    title = request.json.get('title')
    body = request.json.get('body')
    type = get_user_type(user.email)
    comments = []

    tcc = TCC.objects(title=title)

    if tcc:
        return jsonify({'message': 'TCC já existe.'}), 400

    tcc = TCC(authorId=authorId,
              title=title, body=body, type=type, comments=comments)

    tcc.save()

    resp = tcc.to_mongo().to_dict()
    resp.pop('_id')

    return jsonify(resp), 201


@app.get('/tcc/title/<title>')
# @spec.validate(resp=Response(HTTP_200=TCC_DTO))
def get_tcc_by_title(title):
    """
    - GET tcc by title.
    """
    print("title", title)
    try:
        tcc = TCC.objects.get(title=title)
        resp = tcc.to_mongo().to_dict()
        resp.pop('_id')

        return jsonify(resp), 200

    except:
        return jsonify({'message': 'TCC not found'}), 404


@app.get('/tcc')
# @spec.validate(resp=Response(HTTP_200=TCC_list_DTO))
def list_tcc_by_type():
    """
    - GET all tccs filtered by type.
    """
    user = getattr(request, 'user', None)
    user_type = get_user_type(user.email)

    if user_type == User_Type.Teacher:
        tccs = TCC.objects(type=User_Type.Student)
        print("FAZENDO GET DE TCCs DE ALUNOS")
    elif user_type == User_Type.Student:
        tccs = TCC.objects(type=User_Type.Teacher)
        print("FAZENDO GET DE TCCs DE PROFESSORES")
    else:
        return jsonify({'message': 'Por favor, logue com um email acadêmico'}), 401

    if tccs == None:
        return jsonify([])

    json_data = loads(tccs.to_json())
    print('json_data \n', json_data)

    return jsonify(json_data * 10), 200


@app.get('/tcc/author/<authorId>')
def list_tcc_by_author(authorId):
    """
    - GET all tccs filtered by author.
    """
    user = getattr(request, 'user', None)
    user_type = get_user_type(user.email)

    tccs = TCC.objects(authorId=authorId)

    if tccs == None:
        return jsonify([])

    json_data = loads(tccs.to_json())

    print('json_data \n', json_data)
    json_data = [tcc for tcc in json_data if (
        tcc["type"] != user_type.value or tcc["authorId"] == user.uid)]

    return jsonify(json_data), 200


@app.delete('/tcc/title/<title>')
def delete_tcc_by_title(title):
    """
    - DELETE tcc by title.
    """
    # title = request.args.get('title')
    tcc = TCC.objects(title=title).first()

    if tcc == None:
        return jsonify({'message': 'TCC not found'}), 404

    tcc.delete()

    return jsonify({'message': 'TCC deleted'}), 200


@app.post('/tcc/comment')
def add_comment():
    """
    - ADD comment to tcc.
    """
    user = getattr(request, 'user', None)
    authorName = user.display_name
    authorEmail = user.email
    authorAvatar = user.photo_url
    title = request.json.get('title')
    text = request.json.get('text')
    timestamp = datetime.now()

    tcc = TCC.objects(title=title).first()

    if tcc == None:
        return jsonify({'message': 'TCC not found'}), 404

    tcc.comments.append(
        Comment(authorName=authorName, authorEmail=authorEmail,
                authorAvatarUrl=authorAvatar, text=text, timestamp=timestamp)
    )
    tcc.save()

    resp = tcc.to_mongo().to_dict()
    resp.pop('_id')

    return jsonify(resp), 201


@app.get('/tcc/all')
def list_all_tccs():
    """
    - GET all tccs.
    """
    tccs = TCC.objects().all()
    json_data = loads(tccs.to_json())
    print('json_data \n', json_data)

    return jsonify(json_data), 200


@app.get('/delete_all_tccs')
def delete_all_posts():
    """
    - DELETE all tccs.
    """
    tccs = TCC.objects().all()
    tccs.delete()
    return jsonify({'message': 'All tccs deleted'}), 200
