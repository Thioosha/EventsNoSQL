from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime, timedelta
from users.models import MongoUser
from events.models import MongoEvent # Changement ici
from datetime import datetime

from mongoengine import ValidationError

# class MongoReservation(Document):
#     user = ReferenceField(MongoUser, required=True)
#     event = ReferenceField(MongoEvent, required=True)  # updated Event model
#     status = StringField(
#         choices=["pending", "confirmed", "cancelled"],
#         default="pending"
#     )
#     created_at = DateTimeField(default=lambda: datetime.now())
#     expires_at = DateTimeField(default=lambda: datetime.now() + timedelta(minutes=30), null=True)
#     confirmed_at = DateTimeField(null=True)
#     payment_status = StringField(
#         choices=["paid", "unpaid", "failed"],
#         default="unpaid"
#     )
#     payment_method = StringField(null=True)

#     meta = {
#         'indexes': [
#             'user',
#             'event',
#             {'fields': ['-created_at'], 'name': 'created_at_desc'},
#             {
#                 'fields': ['expires_at'],
#                 'expireAfterSeconds': 0  # TTL kicks in right when expires_at is reached
#             }
#         ]
#     }
#     def save(self, *args, **kwargs):
#         # On create only
#         if not self.pk:
#             # Check available slots
#             if self.event.available_slots <= 0:
#                 raise ValidationError("Aucun slot dispo pour cet event 🚫")
        
#         super().save(*args, **kwargs)

from mongoengine import IntField

class MongoReservation(Document):
    user = ReferenceField(MongoUser, required=True)
    event = ReferenceField(MongoEvent, required=True)
    status = StringField(
        choices=["pending", "confirmed", "cancelled"],
        default="pending"
    )
    adults = IntField(min_value=1, default=1)  # Nombre d'adultes (1 par défaut)
    children = IntField(min_value=0, default=0)  # Nombre d'enfants (0 par défaut)
    created_at = DateTimeField(default=lambda: datetime.now())
    expires_at = DateTimeField(default=lambda: datetime.now() + timedelta(minutes=30), null=True)
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

