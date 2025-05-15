from django.db import models

from mongoengine import Document, StringField, EmailField, ListField

class MongoUser(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    full_name = StringField(required=True)
    reservations = ListField()
    created_events = ListField()
    notifications = ListField()
    account_type = StringField(choices=['organizer', 'participant'], required=True)
