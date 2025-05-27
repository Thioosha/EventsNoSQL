from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField, EmbeddedDocument, EmbeddedDocumentListField
from users.models import MongoUser
from events.models import MongoEvent


class NotificationParticipant(EmbeddedDocument):
    user_id = ReferenceField(MongoUser, required=True)
    read = BooleanField(default=False)
    read_at = DateTimeField(null=True)

class MongoNotification(Document):
    event = ReferenceField(MongoEvent, required=True)
    type = StringField(choices=["cancelled", "postponed", "deleted"], required=True)
    message = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    participants = EmbeddedDocumentListField(NotificationParticipant)
    
    meta = {
        'indexes': [
            'event',
            {'fields': ['created_at'], 'name': 'created_at_desc'},
            {'fields': ['participants.user_id', 'participants.read'], 'name': 'participant_read_status'}
        ]
    }

