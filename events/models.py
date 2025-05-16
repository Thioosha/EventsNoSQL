from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField
from datetime import datetime

class MongoEvent(Document):
    title = StringField(required=True)
    description = StringField()
    date = DateTimeField()
    location = StringField()
    organizer = ReferenceField('MongoUser')  # Référence à l'organisateur
    participants = ListField(ReferenceField('MongoUser'))  # Liste des participants
    created_at = DateTimeField(default=datetime)  # Date de création

    def add_participant(self, user):
        if user not in self.participants:
            self.participants.append(user)
            self.save()

    def __str__(self):
        return self.title