from mongoengine import connect
from reservations.models import MongoReservation
from users.models import MongoUser
from events.models import MongoEvent

# Remplacez par vos informations de connexion MongoDB Atlas
username = 'absa'
password = 'hasher'
db_name = 'events_db'


# Connexion à MongoDB
connect(
    db='events_db',
    host='mongodb+srv://groupe9:groupe%409@cluster0.y8zgs6y.mongodb.net/'
)

try:
    # Récupération des documents existants
    user = MongoUser.objects.get(username='thio')
    event = MongoEvent.objects.get(title="Concert Jazz")
    
    # Création de la réservation avec tous les champs requis
    reservation = MongoReservation(
        user=user,
        event=event,
        status='pending',
       
    )
    
    reservation.save()
    print(f"✅ Réservation créée avec ID: {reservation.id}")

except Exception as e:
    print(f"❌ Erreur lors de la création: {str(e)}")
    print("Vérifiez que:")
    print("- Tous les champs requis sont fournis")
    print("- Les documents référencés existent bien")
    print("- La connexion à MongoDB est active")