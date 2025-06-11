from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime, timedelta
from users.models import MongoUser
from events.models import MongoEvent
from datetime import datetime
from mongoengine import ValidationError
from mongoengine import IntField


class MongoReservation(Document):
    user = ReferenceField(MongoUser, required=True)
    event = ReferenceField(MongoEvent, required=True)
    status = StringField(
        choices=["pending", "confirmed", "cancelled"],
        default="pending"
    )
    adults = IntField(min_value=1, default=1)
    children = IntField(min_value=0, default=0)
    created_at = DateTimeField(default=lambda: datetime.now())
    expires_at = DateTimeField(default=lambda: datetime.now() + timedelta(minutes=30), null=True)
    confirmed_at = DateTimeField(null=True)
    payment_status = StringField(
        choices=["paid", "unpaid", "failed"],
        default="unpaid"
    )
    payment_method = StringField(null=True)

    #  QR Code Ticket Image Path
    ticket = StringField(null=True)

    meta = {
        'indexes': [
            'user',
            'event',
            {'fields': ['-created_at'], 'name': 'created_at_desc'},
            {
                'fields': ['expires_at'],
                'expireAfterSeconds': 0
            }
        ]
    }

    def save(self, *args, **kwargs):
        if not self.pk:
            total_requested = self.adults + self.children
            if self.event.available_slots < total_requested:
                raise ValidationError("Pas assez de places disponibles pour ta demande.")
        
        super().save(*args, **kwargs)
