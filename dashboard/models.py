from datetime import datetime

from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField

from users.models import MongoUser
from events.models import MongoEvent


class MongoNotification(Document): 
    user = ReferenceField(MongoUser) 
    message = StringField() 
    type = StringField(choices=["cancelled", "postponed", "deleted"]) 
    event = ReferenceField(MongoEvent) 
    created_at = DateTimeField(default=datetime.utcnow) 
    is_read = BooleanField(default=False)
