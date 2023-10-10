from mongoengine import EmbeddedDocument, StringField, DateTimeField


class Comment(EmbeddedDocument):
    authorName = StringField(required=True)
    authorEmail = StringField(required=True)
    authorAvatarUrl = StringField(required=True)
    text = StringField(required=True)
    timestamp = DateTimeField(required=True)

    def __init__(self, authorName, authorEmail, authorAvatarUrl, text, timestamp, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        self.authorName = authorName
        self.authorEmail = authorEmail
        self.authorAvatarUrl = authorAvatarUrl
        self.text = text
        self.timestamp = timestamp
