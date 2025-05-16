from mongoengine import Document, StringField, ReferenceField, DateTimeField
from users.models import MongoUser
from events.models import MongoEvent # Changement ici
from datetime import datetime

from mongoengine import ValidationError

class MongoReservation(Document):
    user = ReferenceField(MongoUser, required=True)
    event = ReferenceField(MongoEvent, required=True)  # updated Event model
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

    def save(self, *args, **kwargs):
        # On create only
        if not self.pk:
            # Check available slots
            if self.event.available_slots <= 0:
                raise ValidationError("Aucun slot dispo pour cet event 😤")
            # Decrease slot
            self.event.available_slots -= 1
            self.event.save()
        
        super().save(*args, **kwargs)
