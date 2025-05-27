from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from bson import ObjectId
from .models import MongoEvent, NotificationParticipant  # adapte si le nom est différent
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from bson import ObjectId
from .models import MongoEvent
from events.forms import MongoEventForm
from django.utils import timezone as dj_timezone  # Pour `now()`, `is_naive()`, etc.
from datetime import datetime, timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect

from events.models import MongoEvent
from users.models import MongoUser
from reservations.models import MongoReservation  # deferred import to avoid circular reference
from dashboard.models import MongoNotification  # deferred import to avoid circular reference

from reservations.models import MongoReservation
from bson import ObjectId
from django.contrib import messages


def dashboard_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    current_user = MongoUser.objects(id=ObjectId(user_id)).first()
    now = datetime.utcnow()

    # Récupérer les notifications de l'utilisateur
    notifications = MongoNotification.objects(
        participants__user_id=ObjectId(user_id)
    ).order_by('-created_at')
    
    # Préparer les notifications avec leur statut de lecture
    user_notifications = []
    unread_count = 0
    for notification in notifications:
        participant = next((p for p in notification.participants if str(p.user_id.id) == user_id), None)
        if participant:
            if not participant.read:
                unread_count += 1
            user_notifications.append({
                'notification': notification,
                'is_read': participant.read,
                'read_at': participant.read_at
            })
    print(unread_count)
    if current_user.account_type == "organizer": 
        section = request.GET.get("section", "events")
    else:
        section = request.GET.get("section", "reservations")

    context = {
        "account_type": current_user.account_type,
        "notifications": user_notifications,
        "unread_notifications_count": unread_count,
        "section": section,
        "now": now
    }


    if current_user.account_type == "organizer":
        # Récupérer les événements créés par l'organisateur
        my_events = MongoEvent.objects(created_by=ObjectId(user_id)).order_by('-start_datetime')
        
        # Séparer les événements en passés et à venir
        context["upcoming_events"] = [
            event for event in my_events
            if event.start_datetime > now
        ]
        context["past_events"] = [
            event for event in my_events
            if event.start_datetime <= now
        ]
        
        print(f"Événements à venir: {len(context['upcoming_events'])}")
        print(f"Événements passés: {len(context['past_events'])}")
        
        # Récupérer les réservations où l'organisateur est participant
        organizer_reservations = list(MongoReservation.objects(
            user=ObjectId(user_id)  # Chercher les réservations où l'utilisateur est participant
        ).order_by('-created_at')) 
        
        for r in organizer_reservations:
            if hasattr(r, 'event'):
                if hasattr(r.event, 'organizer'):
                    print("Host:", r.event.organizer)
                elif hasattr(r.event, 'created_by'):
                    print("Host:", r.event.created_by)
        
        # Séparer les réservations en passées et à venir
        context["upcoming_reservations"] = [
            r for r in organizer_reservations
            if r.event.start_datetime > now
        ]
        context["past_reservations"] = [
            r for r in organizer_reservations
            if r.event.start_datetime <= now
        ]

        # Calculer les statistiques des réservations
        total_reservations = len(organizer_reservations)
        confirmed_reservations = len([r for r in organizer_reservations if r.status == "confirmed"])
        paid_reservations = len([r for r in organizer_reservations if r.payment_status == "paid"])
        total_adults = sum(r.adults for r in organizer_reservations)
        total_children = sum(r.children for r in organizer_reservations)
        
        context["reservation_stats"] = {
            "total": total_reservations,
            "confirmed": confirmed_reservations,
            "paid": paid_reservations,
        }
        
          
        return render(request, "dashboard/dashboard.html", {**context, 'color_on_scroll': 30})

    elif current_user.account_type == "participant":
        # Récupérer toutes les réservations de l'utilisateur avec un seul appel à la base de données
        user_reservations = list(MongoReservation.objects(
            user=ObjectId(user_id)
        ).order_by('-created_at'))
        

        # Séparer les réservations en passées et à venir
        context["upcoming_reservations"] = [
            r for r in user_reservations
            if r.event.start_datetime > now
        ]
        context["past_reservations"] = [
            r for r in user_reservations
            if r.event.start_datetime <= now
        ]

        # Calculer les statistiques des réservations
        total_reservations = len(user_reservations)
        confirmed_reservations = len([r for r in user_reservations if r.status == "confirmed"])
        paid_reservations = len([r for r in user_reservations if r.payment_status == "paid"])
        total_adults = sum(r.adults for r in user_reservations)
        total_children = sum(r.children for r in user_reservations)
        
        context["reservation_stats"] = {
            "total": total_reservations,
            "confirmed": confirmed_reservations,
            "paid": paid_reservations,
            "total_adults": total_adults,
            "total_children": total_children
        }
        
        print(f"Réservations à venir: {len(context['upcoming_reservations'])}")
        print(f"Réservations passées: {len(context['past_reservations'])}")
        print(f"Statistiques des réservations: {context['reservation_stats']}")
        
        return render(request, "dashboard/dashboard_participant.html", {**context, 'color_on_scroll': 30})

    return redirect("login")


def event_detail_view(request, event_id):
    try:
        # Récupérer l'événement
        event = MongoEvent.objects.get(id=event_id)
        
        # Récupérer toutes les réservations pour cet événement
        reservations = MongoReservation.objects.filter(event=event).order_by('-created_at')
        
        # Calculer les statistiques
        total_adults = sum(reservation.adults for reservation in reservations)
        total_children = sum(reservation.children for reservation in reservations)
        
        context = {
            'event': event,
            'reservations': reservations,
            'total_adults': total_adults,
            'total_children': total_children,
        }
        
        return render(request, 'dashboard/detail_admin_event.html', {**context, 'color_on_scroll': 30})
        
    except MongoEvent.DoesNotExist:
        return redirect('dashboard')
    except Exception as e:
      return redirect('dashboard')
    
def reservation_event_detail(request, event_id):
    try:
        event = MongoEvent.objects.get(id=event_id)
    except MongoEvent.DoesNotExist:
        raise Http404("Event not found 🚫")

    ticket_url = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = MongoUser.objects.get(id=user_id)
            reservation = MongoReservation.objects.filter(user=user, event=event, status="confirmed").first()
            if reservation and reservation.ticket:
                ticket_url = reservation.ticket
        except MongoUser.DoesNotExist:
            pass

    # Handle reservation-related errors from query string
    error = request.GET.get('error')
    if error == 'expired':
        messages.error(request, "La réservation a expiré. Veuillez réessayer.")
    elif error == 'already_reserved':
        messages.warning(request, "Vous avez déjà une réservation pour cet événement ⚠️")
    elif error == 'not_enough_slots':
        messages.error(request, "Nombre de places insuffisant pour cette réservation ⚠️")

    return render(request, 'dashboard/reservation_event_detail.html', {
        'event': event,
        'ticket': ticket_url,
        'color_on_scroll': 30,
    })



def annuler_reservation(request, event_id):
    if request.method != "POST":
        raise Http404("Méthode non autorisée")

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    try:
        user = MongoUser.objects.get(id=user_id)
    except MongoUser.DoesNotExist:
        raise Http404("Utilisateur introuvable")

    try:
        event = MongoEvent.objects.get(id=ObjectId(event_id))
    except MongoEvent.DoesNotExist:
        raise Http404("Événement introuvable")

    # Vérifier si l'événement est passé
    event_end = event.end_datetime
    if dj_timezone.is_naive(event_end):
        event_end = dj_timezone.make_aware(event_end, timezone.utc)

    if event_end < dj_timezone.now():
        messages.error(request, "Vous ne pouvez pas annuler une réservation pour un événement passé.")
        return redirect(request.META.get("HTTP_REFERER", "dashboard"))

    # Trouver et supprimer la réservation
    reservation = MongoReservation.objects.filter(user=user, event=event).first()
    if reservation:
        # Créer une notification pour l'organisateur
        if event.created_by:
            organizer_notification = MongoNotification(
                event=event,
                type="cancelled",
                message=f"Le participant {user.full_name} a annulé sa réservation pour l'événement '{event.title}'",
                participants=[NotificationParticipant(user_id=event.created_by)]
            )
            organizer_notification.save()

        # Créer une notification pour l'utilisateur qui annule
        notify_users(event, "cancelled")  # Crée une notification pour tous les participants
        
        reservation.delete()
    else:
        return redirect('dashboard')

    # Mettre à jour les participants
    user_object_id = ObjectId(user.id)
    if user_object_id in event.participants:
        event.participants.remove(user_object_id)
        event.available_slots += 1
        event.save()

    return redirect('dashboard')


    event_end = event.end_datetime
    if dj_timezone.is_naive(event_end):
        event_end = dj_timezone.make_aware(event_end, timezone.utc)

    if event_end < dj_timezone.now():
        messages.error(request, "Vous ne pouvez pas annuler une réservation pour un événement passé.")
        return redirect(request.META.get("HTTP_REFERER", "dashboard"))



    # Trouver et supprimer la réservation
    reservation = MongoReservation.objects.filter(user=user, event=event).first()
    if reservation:
        reservation.delete()
    else:
        return redirect('dashboard')

    # Mettre à jour les participants
    user_object_id = ObjectId(user.id)
    if user_object_id in event.participants:
        event.participants.remove(user_object_id)
        event.available_slots += 1
        event.save()

    return redirect('dashboard')



def modifier_event(request, event_id):
    try:
        event = MongoEvent.objects.get(id=ObjectId(event_id))
    except MongoEvent.DoesNotExist:
        messages.error(request, "Événement introuvable.")
        return redirect("dashboard")

    if request.method == "POST":
        form = MongoEventForm(request.POST, request.FILES)
        if form.is_valid():
            # Sauvegarder les anciennes données pour la notification
            old_data = {
                'title': event.title,
                'start_datetime': event.start_datetime,
                'end_datetime': event.end_datetime,
                'location': event.location,
                'total_slots': event.total_slots,
                'price': event.price,
                'category': event.category
            }
            
            # Mise à jour des champs
            event.title = form.cleaned_data['title']
            event.description = form.cleaned_data['description']
            event.location = form.cleaned_data['location']
            event.start_datetime = form.cleaned_data['start_datetime']
            event.end_datetime = form.cleaned_data['end_datetime']
            event.image = form.cleaned_data['image']
            event.total_slots = form.cleaned_data['total_slots']
            event.available_slots = form.cleaned_data['available_slots']
            event.price = form.cleaned_data['price']
            event.category = form.cleaned_data['category']

            event.save()  # Sauvegarde dans MongoDB

            # Vérifier si des changements importants ont été faits
            changes = {
                'title': old_data['title'] != event.title,
                'dates': old_data['start_datetime'] != event.start_datetime or old_data['end_datetime'] != event.end_datetime,
                'location': old_data['location'] != event.location,
                'slots': old_data['total_slots'] != event.total_slots,
                'price': old_data['price'] != event.price,
                'category': old_data['category'] != event.category
            }

            # Si au moins un changement important a été fait
            if any(changes.values()):
                notify_users(event, "postponed")

            messages.success(request, "L'événement a été modifié avec succès.")
            return redirect("dashboard")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        # Pré-remplissage du formulaire avec les données existantes
        initial_data = {
            'title': event.title,
            'description': event.description,
            'location': event.location,
            'start_datetime': event.start_datetime.strftime('%Y-%m-%dT%H:%M') if event.start_datetime else '',
            'end_datetime': event.end_datetime.strftime('%Y-%m-%dT%H:%M') if event.end_datetime else '',
            'total_slots': event.total_slots,
            'available_slots': event.available_slots,
            'price': event.price,
            'category': event.category,
        }
        form = MongoEventForm(initial=initial_data)

    return render(request, "dashboard/edit_event.html", {"form": form, "event": event, 'color_on_scroll': 30})

def supprimer_event(request, event_id):
    try:
        event = MongoEvent.objects.get(id=ObjectId(event_id))
        
        # Créer une notification pour tous les participants avant la suppression
        notify_users(event, "deleted")
        
        event.delete()
        messages.success(request, "L'événement a été supprimé avec succès.")
    except Exception as e:
        return redirect("dashboard")  # redirige vers la page d'accueil ou de gestion
    return redirect("dashboard")  # redirige vers la page d'accueil ou de gestion


def notifications_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # ou gérer l'absence d'authentification

    current_user = MongoUser.objects(id=ObjectId(user_id)).first()
    notifications = MongoNotification.objects(user=current_user).order_by('-created_at')
    return render(request, "notifications.html", {"notifications": notifications, 'color_on_scroll': 30})



def notify_users(event, type):
    # Récupérer tous les participants confirmés
    reservations = MongoReservation.objects.filter(event=event, status="confirmed")
    if not reservations:
        return
    
    # Créer le message
    message = {
        "cancelled": f"L'événement '{event.title}' a été annulé.",
        "postponed": f"L'événement '{event.title}' a été modifié.",
        "deleted": f"L'événement '{event.title}' a été supprimé."
    }[type]

    # Créer la notification
    notification = MongoNotification(
        event=event,
        type=type,
        message=message,
        participants=[]
    )

    # Ajouter tous les participants
    for reservation in reservations:
        participant = NotificationParticipant(
            user_id=reservation.user,
            read=False,
            read_at=None
        )
        notification.participants.append(participant)

    notification.save()

def mark_notification_read(request, notification_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    notification = MongoNotification.objects(id=notification_id).first()
    if notification:
        participant = next((p for p in notification.participants if str(p.user_id.id) == user_id), None)
        if participant:
            participant.read = True
            participant.read_at = datetime.utcnow()
            notification.save()
            messages.success(request, "Notification marquée comme lue")
    return redirect('dashboard')