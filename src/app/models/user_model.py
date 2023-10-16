from enum import Enum, IntEnum
from mongoengine import Document, StringField, EnumField, ListField
from app.models.comment_model import Comment


class User_Type(Enum):
    Student = 'Student'
    Teacher = 'Teacher'


class Tag(IntEnum):
    SOFTWARE_ENGINEERING = 0
    EDUCATIONAL_INFORMATICS = 1
    ARTIFICIAL_INTELLIGENCE = 2
    DISTRIBUTED_SYSTEMS = 3
    INFORMATION_SYSTEMS = 4


class User(Document):
    firebase_uid = StringField(required=True)
    type = EnumField(User_Type, required=True)
    avatar_url = StringField(required=True)
    email = StringField(required=True)
    name = StringField(required=True)
    tags = ListField(EnumField(Tag))

    def __init__(self, firebase_uid, type, avatar_url, email, name, tags, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.firebase_uid = firebase_uid
        self.type = type
        self.avatar_url = avatar_url
        self.email = email
        self.name = name
        self.tags = tags
