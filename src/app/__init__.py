from config.config import (
    DB,
    DB_HOST,
    DB_PORT,
    DB_USERNAME,
    DB_PASSWORD,
    MONGO_URI
)
from flask_pydantic_spec import FlaskPydanticSpec
from mongoengine import connect
from flask import Flask

import os
import firebase_admin
from firebase_admin import credentials

# Initialize the SDK with your service account credentials
key_path = os.path.join(os.path.dirname(__file__), '../../serviceAccountKey.json')
print(key_path)
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

app = Flask(__name__)
spec = FlaskPydanticSpec('mongo-crud')
spec.register(app)


connect(
    db=DB,
    host=DB_HOST,
    port=int(DB_PORT),
    username=DB_USERNAME,
    password=DB_PASSWORD
)

from app.controllers import tcc_controller, user_controller
