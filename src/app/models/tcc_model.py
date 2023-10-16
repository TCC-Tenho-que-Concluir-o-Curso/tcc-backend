from mongoengine import Document, StringField, EnumField, EmbeddedDocumentListField
from enum import Enum

from app.models.comment_model import Comment
from app.models.user_model import User_Type


class TCC(Document):
    authorId = StringField(required=True)
    title = StringField(required=True)
    body = StringField(required=True)
    type = EnumField(User_Type, required=True)
    comments = EmbeddedDocumentListField(Comment)

    def __init__(self, authorId, title, body, type, comments, *args, **kwargs):
        super(TCC, self).__init__(*args, **kwargs)
        self.authorId = authorId
        self.title = title
        self.body = body
        self.type = type
        self.comments = comments
