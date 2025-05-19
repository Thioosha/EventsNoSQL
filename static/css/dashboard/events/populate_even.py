from datetime import datetime, timedelta
from events.models import MongoEvent
from mongoengine import connect

connect(
    db='events_db',
    host='mongodb+srv://groupe9:groupe%409@cluster0.y8zgs6y.mongodb.net/',
    alias='default')

EVENTS_DATA = [
    {
        "title": "Concert Jazz",
        "description": "Soirée musicale",
        
        
    },
    {
        "title": "Conférence Tech",
        "description": "Nouvelles technologies"
        
    }
]

for event_data in EVENTS_DATA:
    MongoEvent(**event_data).save()

print(f"✅ {len(EVENTS_DATA)} événements créés")