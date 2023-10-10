from mongoengine import Document, StringField, EnumField, EmbeddedDocumentListField
from app.models.tcc_model import User_Type
from app.models.comment_model import Comment


class User(Document):
    firebase_uid = StringField(required=True)
    type = EnumField(User_Type, required=True)
    avatar_url = StringField(required=True)
    email = StringField(required=True)
    name = StringField(required=True)

    def __init__(self, firebase_uid, type, avatar_url, email, name, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.firebase_uid = firebase_uid
        self.type = type
        self.avatar_url = avatar_url
        self.email = email
        self.name = name
