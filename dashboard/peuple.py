from dashboard.models import MongoNotification
from users.models import MongoUser
from events.models import MongoEvent
from datetime import datetime
from mongoengine import connect


connect(
    db="events_db",
    host="mongodb+srv://groupe9:groupe%409@cluster0.y8zgs6y.mongodb.net/events_db?retryWrites=true&w=majority"
)

print("Connexion à la base de données établie.")

user = MongoUser.objects.first()
print(f"Utilisateur récupéré : {user}")

event = MongoEvent.objects.first()
print(f"Événement récupéré : {event}")

if user is None:
    print("Erreur : aucun utilisateur trouvé.")
if event is None:
    print("Erreur : aucun événement trouvé.")

notif = MongoNotification(
    user=user,
    message="Test",
    type="cancelled",
    event=event
)

notif.save()
print(f"Notification créée avec id : {notif.id}")
