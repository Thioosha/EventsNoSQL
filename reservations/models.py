from mongoengine import Document, StringField, ReferenceField, DateTimeField
from users.models import MongoUser
from events.models import MongoEvent  # Changement ici
from datetime import datetime

class MongoReservation(Document):
    user = ReferenceField(MongoUser, required=True)
    event = ReferenceField(MongoEvent, required=True)  # Changement ici
    status = StringField(
        choices=["pending", "confirmed", "cancelled"],
        default="pending"
    )
    created_at = DateTimeField(default=lambda: datetime.now())
    confirmed_at = DateTimeField(null=True)
    payment_status = StringField(
        choices=["paid", "unpaid", "failed"],
        default="unpaid"
    )
    payment_method = StringField(null=True)

    meta = {
        'indexes': [
            'user',
            'event',
            {'fields': ['-created_at'], 'name': 'created_at_desc'}
        ]
    }