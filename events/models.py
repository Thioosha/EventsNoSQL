from mongoengine import Document, StringField, DateTimeField, ReferenceField, IntField, FloatField, ListField
from datetime import datetime, timezone
from users.models import MongoUser  # adjust if needed

CATEGORY_CHOICES = [
    "Musique", "Art", "Conférence", "Sport", "Atelier", "Formation", "Technologie",
    "Rencontre", "Mode", "Santé", "Voyage", "Cinéma", "Théâtre", "Danse", "Gaming",
    "Littérature", "Religion", "Cuisine", "Networking", "Autre"
]

class MongoEvent(Document):
    title = StringField(required=True)
    description = StringField()
    location = StringField()
    start_datetime = DateTimeField(required=True)
    end_datetime = DateTimeField(required=True)

    available_slots = IntField(required=True)
    total_slots = IntField(required=True)

    image_url = StringField(default="https://dummyimage.com/900x400/dee2e6/6c757d.jpg") 

    created_by = ReferenceField(MongoUser, required=True)
    participants = ListField(ReferenceField(MongoUser), default=list)
    price = FloatField(default=0.0)

    category = StringField(choices=CATEGORY_CHOICES)

    status = StringField(
        choices=["active", "cancelled", "postponed", "archived"],
        default="active"
    )

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"{self.title} ({self.start_datetime.strftime('%d/%m/%Y')})"

