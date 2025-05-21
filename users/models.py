from mongoengine import Document, StringField, EmailField, ListField

class MongoUser(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    full_name = StringField(required=True)
    reservations = ListField(default=list)
    notifications = ListField(default=list)
    account_type = StringField(choices=['organizer', 'participant'], required=True)
    pfp = StringField(default="/static/img/users/pfp.png")  # Default local path

