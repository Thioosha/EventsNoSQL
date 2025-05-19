from mongoengine import Document, StringField, DateTimeField, ReferenceField, IntField, FloatField, ListField
from datetime import datetime, timezone
from users.models import MongoUser  # adjust if needed

CATEGORY_CHOICES = [
    "Musique", "Art", "Conférence", "Sport", "Atelier", "Formation", "Technologie",
    "Rencontre", "Mode", "Santé", "Voyage", "Cinéma", "Théâtre", "Danse", "Gaming",
    "Littérature", "Religion", "Cuisine", "Networking", "Autre"
]

class MongoEvent(Document):
    title = StringField(default="")
    description = StringField(default="")
    location = StringField(default="")
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()
    available_slots = IntField(default=0)
    total_slots = IntField(default=0)
    image_url = StringField(default="https://dummyimage.com/900x400/dee2e6/6c757d.jpg")
    created_by = ReferenceField('MongoUser', required=False)
    participants = ListField(ReferenceField('MongoUser'), default=list)
    price = FloatField(default=0.0)
    category = StringField(default="Autre")
    status = StringField(default="active")
    created_at = DateTimeField()
    
    def _str_(self):
        return f"{self.title} ({self.start_datetime.strftime('%d/%m/%Y') if self.start_datetime else 'No Date'})"

