from datetime import datetime
from django.shortcuts import render,redirect

from events.models import MongoEvent
from users.models import MongoUser
from reservations.models import MongoReservation  # deferred import to avoid circular reference
from dashboard.models import MongoNotification  # deferred import to avoid circular reference

from reservations.models import MongoReservation
# Create your views here.
from bson import ObjectId


user1 = {
    "_id": "68270af8c262482bd643b66d",
    "username": "codiallo",
    "email": "codaillo@ept.sn",
    "password": "Cod1508",
    "full_name": "Cheikh Oumar DIALLO",
    "reservations": [],
    "created_events": [],
    "notifications": [],
    "account_type": "organizer"
}

user2 = {
    "_id": "68275f587eee979e0e4e62b5",
    "username": "cod",
    "email": "cod@cod.sn",
    "password": "Cod1508",
    "full_name": "Cheikh DIALLO",
    "reservations": [],
    "created_events": [],
    "notifications": [],
    "account_type": "participant"
}

my_events = [
  {
    "title": "Atelier de Peinture",
    "description": "Un atelier créatif pour apprendre les bases de la peinture à l'huile.",
    "location": "Maison des Associations, Paris",
    "start_datetime": "2026-06-10T14:00:00",
    "end_datetime": "2026-06-10T17:00:00",
    "available_slots": 20,
    "created_by": "68270af8c262482bd643b66d",
    "is_paid": True,
    "price": 35.00,
    "category": "Art",
    "status": "completed",
    "created_at": "2024-05-17T10:30:00"
  },
  {
    "title": "Conférence sur l'IA",
    "description": "Découvrez les dernières avancées en intelligence artificielle avec des experts du domaine.",
    "location": "Université Lyon 1",
    "start_datetime": "2024-12-01T09:00:00",
    "end_datetime": "2024-12-01T17:00:00",
    "available_slots": 100,
    "created_by": "68270af8c262482bd643b66d",
    "is_paid": False,
    "price": 0.0,
    "category": "Technologie",
    "status": "active",
    "created_at": "2024-05-10T08:00:00"
  },
  {
    "title": "Cours de Yoga",
    "description": "Séance de yoga pour débutants, apportez votre tapis !",
    "location": "Parc Montsouris, Paris",
    "start_datetime": "2024-05-15T08:00:00",
    "end_datetime": "2024-05-15T09:30:00",
    "available_slots": 15,
    "created_by": "68270af8c262482bd643b66d",
    "is_paid": True,
    "price": 25.00,
    "category": "Bien-être",
    "status": "completed",
    "created_at": "2024-04-15T12:45:00"
  },
  {
    "title": "Soirée jeux de société",
    "description": "Venez découvrir et jouer à une sélection de jeux de société modernes.",
    "location": "Café Ludique, Nantes",
    "start_datetime": "2024-11-20T18:00:00",
    "end_datetime": "2024-11-20T22:00:00",
    "available_slots": 30,
    "created_by": "68270af8c262482bd643b66d",
    "is_paid": False,
    "price": 0.0,
    "category": "Loisir",
    "status": "active",
    "created_at": "2024-05-12T14:20:00"
  },
  {
    "title": "Atelier de cuisine végétarienne",
    "description": "Apprenez à préparer des plats végétariens délicieux et sains.",
    "location": "Cuisine Communautaire, Lille",
    "start_datetime": "2025-06-25T11:00:00",
    "end_datetime": "2025-06-25T14:00:00",
    "available_slots": 12,
    "created_by": "68270af8c262482bd643b66d",
    "is_paid": True,
    "price": 0.00,
    "category": "Cuisine",
    "status": "active",
    "created_at": "2025-05-14T09:10:00"
  },
  {
    "title": "Festival de Musique",
    "description": "Un festival de musique en plein air avec des artistes locaux et internationaux.",
    "location": "Parc de la Tête d'Or, Lyon",
    "start_datetime": "2025-07-15T14:00:00",
    "end_datetime": "2025-07-15T23:00:00",
    "available_slots": 500,
    "created_by": "68270af8c262482bd643b66d",
    "is_paid": True,
    "price": 45.00,
    "category": "Musique",
    "status": "active",
    "created_at": "2024-05-20T10:00:00"
  }
]

reservations = [
  {
    "user": "68275f587eee979e0e4e62b5",
    "event": "event1_id", 
    "status": "confirmed",
    "created_at": "2024-05-18T10:00:00",
    "confirmed_at": "2024-05-18T10:30:00",
    "payment_status": "paid",
    "payment_method": "carte"
  },
  {
    "user": "68275f587eee979e0e4e62b5",
    "event": "event2_id", 
    "status": "pending",
    "created_at": "2024-05-18T10:01:00",
    "confirmed_at": None,
    "payment_status": "unpaid",
    "payment_method": "carte"
  },
  {
    "user": "68275f587eee979e0e4e62b5",
    "event": "event3_id", 
    "status": "completed",
    "created_at": "2024-05-01T10:02:00",
    "confirmed_at": "2024-05-01T10:30:00",
    "payment_status": "paid",
    "payment_method": "carte"
  },
  {
    "user": "68275f587eee979e0e4e62b5",
    "event": "event4_id", 
    "status": "completed",
    "created_at": "2024-04-15T10:03:00",
    "confirmed_at": "2024-04-15T10:30:00",
    "payment_status": "paid",
    "payment_method": "gratuit"
  },
  {
    "user": "98765af8c262482bd643c99a",
    "event": "event5_id", 
    "status": "pending",
    "created_at": "2025-05-18T10:04:00",
    "confirmed_at": None,
    "payment_status": "unpaid",
    "payment_method": "gratuit"
  },
  {
    "user": "68275f587eee979e0e4e62b5",
    "event": "event6_id",
    "status": "confirmed",
    "created_at": "2024-05-20T11:00:00",
    "confirmed_at": "2024-05-20T11:30:00",
    "payment_status": "paid",
    "payment_method": "carte"
  }
]


# def dashboard_view(request):
#     from bson import ObjectId

#     # user_id = request.session.get('user_id')
#     # if not user_id:
#     #     return redirect('login')

#     # current_user = MongoUser.objects(id=ObjectId(user_id)).first()
#     now = datetime.utcnow()

#     # my_events = MongoEvent.objects(created_by=current_user)
#     user_id = "68270af8c262482bd643b66d"

#     filtered_events = [event for event in my_events if event["created_by"] == user_id]

#     # reservations = MongoReservation.objects(user=current_user, status="confirmed").select_related()
#     upcoming_reservations = [r for r in reservations if r.event.start_datetime > now]
#     past_reservations = [r for r in reservations if r.event.start_datetime <= now]

#     section = request.GET.get("section")

#     context = {
#         "my_events": my_events,
#         "upcoming_reservations": upcoming_reservations,
#         "past_reservations": past_reservations,
#         "section": section
#     }

#     return render(request, "dashboard/dashboard.html", context)



def get_current_user():
    return user1  # ou user2 pour tester

def dashboard_view(request):
    now = datetime.utcnow()
    current_user = get_current_user()
    user_id = current_user["_id"]
    account_type = current_user["account_type"]
    section = request.GET.get("section", "events")

    print(f"User ID: {user_id}")
    print(f"Account Type: {account_type}")
    print(f"Section: {section}")

    context = {
        "account_type": account_type,
        "section": section,
        "now": now
    }

    if account_type == "organizer":
        # Convertir les dates en objets datetime pour la comparaison
        for event in my_events:
            if isinstance(event["start_datetime"], str):
                event["start_datetime"] = datetime.fromisoformat(event["start_datetime"])
            if isinstance(event["end_datetime"], str):
                event["end_datetime"] = datetime.fromisoformat(event["end_datetime"])
        
        # Filtrer les événements de l'organisateur
        organizer_events = [event for event in my_events if event["created_by"] == user_id]
        
        # Séparer les événements en passés et à venir
        context["upcoming_events"] = [
            event for event in organizer_events
            if event["start_datetime"] > now
        ]
        context["past_events"] = [
            event for event in organizer_events
            if event["start_datetime"] <= now
        ]
        
        print(f"Événements à venir: {len(context['upcoming_events'])}")
        print(f"Événements passés: {len(context['past_events'])}")
        
        # Récupérer les réservations pour les événements de l'organisateur
        event_ids = [f"event{i+1}_id" for i in range(len(organizer_events))]
        
        # Filtrer les réservations pour les événements de l'organisateur
        organizer_reservations = [r for r in reservations if r["event"] in event_ids]
        
        # Associer les données d'événement à chaque réservation
        for r in organizer_reservations:
            try:
                event_index = int(r["event"].replace("event", "").replace("_id", "")) - 1
                r["event_data"] = my_events[event_index].copy()
                
                # Convertir les dates seulement si elles sont des chaînes
                if isinstance(r["event_data"]["start_datetime"], str):
                    r["event_data"]["start_datetime"] = datetime.fromisoformat(r["event_data"]["start_datetime"])
                if isinstance(r["event_data"]["end_datetime"], str):
                    r["event_data"]["end_datetime"] = datetime.fromisoformat(r["event_data"]["end_datetime"])
                
                print(f"Réservation associée à l'événement: {r['event_data']['title']}")
            except Exception as e:
                print(f"Erreur lors de l'association de l'événement: {e}")
                r["event_data"] = None

        # Séparer les réservations en passées et à venir
        context["upcoming_reservations"] = [
            r for r in organizer_reservations
            if r["event_data"] and r["event_data"]["start_datetime"] > now
        ]
        context["past_reservations"] = [
            r for r in organizer_reservations
            if r["event_data"] and r["event_data"]["start_datetime"] <= now
        ]
        
        print(f"Réservations à venir: {len(context['upcoming_reservations'])}")
        print(f"Réservations passées: {len(context['past_reservations'])}")
        
        return render(request, "dashboard/dashboard.html", context)

    elif account_type == "participant":
        # Filtrer les réservations de l'utilisateur
        user_reservations = [r for r in reservations if r["user"] == user_id]
        print(f"Nombre de réservations trouvées: {len(user_reservations)}")
        
        # Associer les données d'événement à chaque réservation
        for r in user_reservations:
            try:
                event_index = int(r["event"].replace("event", "").replace("_id", "")) - 1
                r["event_data"] = my_events[event_index].copy()
                
                # Convertir les dates seulement si elles sont des chaînes
                if isinstance(r["event_data"]["start_datetime"], str):
                    r["event_data"]["start_datetime"] = datetime.fromisoformat(r["event_data"]["start_datetime"])
                if isinstance(r["event_data"]["end_datetime"], str):
                    r["event_data"]["end_datetime"] = datetime.fromisoformat(r["event_data"]["end_datetime"])
                
                print(f"Réservation associée à l'événement: {r['event_data']['title']}")
            except Exception as e:
                print(f"Erreur lors de l'association de l'événement: {e}")
                r["event_data"] = None

        # Séparer les réservations en passées et à venir
        context["upcoming_reservations"] = [
            r for r in user_reservations
            if r["event_data"] and r["event_data"]["start_datetime"] > now
        ]
        context["past_reservations"] = [
            r for r in user_reservations
            if r["event_data"] and r["event_data"]["start_datetime"] <= now
        ]
        
        print(f"Réservations à venir: {len(context['upcoming_reservations'])}")
        print(f"Réservations passées: {len(context['past_reservations'])}")
        
        return render(request, "dashboard/dashboard_participant.html", context)

    return redirect("login")


def notifications_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # ou gérer l'absence d'authentification

    current_user = MongoUser.objects(id=ObjectId(user_id)).first()
    notifications = MongoNotification.objects(user=current_user).order_by('-created_at')
    return render(request, "notifications.html", {"notifications": notifications})


def mark_notification_read(request, notification_id):
    from dashboard.models import Notification  # deferred import
    notif = MongoNotification.objects(id=notification_id).first()
    if notif:
        notif.is_read = True
        notif.save()
    return redirect('notifications')


def notify_users(event, type):
    users = MongoReservation.objects(event=event, status="confirmed").distinct('user')
    message = {
        "cancelled": f"L'événement '{event.title}' a été annulé.",
        "postponed": f"L'événement '{event.title}' a été reporté.",
        "deleted": f"L'événement '{event.title}' a été supprimé.",
    }[type]

    for user in users:
        MongoNotification(user=user, message=message, type=type, event=event).save()