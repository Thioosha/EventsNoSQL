from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from events.models import MongoEvent
from users.models import MongoUser
from .models import MongoReservation
from mongoengine import ValidationError
from django.contrib import messages


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from .models import MongoReservation
from events.models import MongoEvent
from users.models import MongoUser

from django.shortcuts import redirect, render
from events.models import MongoEvent
from users.models import MongoUser
from .models import MongoReservation
from django.contrib import messages
from datetime import datetime

def create_reservation(request, event_id):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                raise ValidationError("Utilisateur non connecté !")

            user = MongoUser.objects.get(id=user_id)
            event = MongoEvent.objects.get(id=event_id)

            # Check if user already reserved this event
            existing = MongoReservation.objects(event=event, user=user, status="pending").first()
            if existing:
                return redirect(f"{reverse('user_event_detail', args=[str(event_id)])}?error=already_reserved")

            reservation = MongoReservation(
                user=user,
                event=event,
                expires_at=datetime.now() + timedelta(seconds=25)
            )
            reservation.save()
            return redirect('confirm_reservation', reservation_id=str(reservation.id))

        except Exception as e:
            print(f"Error creating reservation: {e}")
            return redirect(f"{reverse('user_event_detail', args=[str(event_id)])}?error=expired")


def confirm_reservation(request, reservation_id):
    try:
        reservation = MongoReservation.objects.get(id=reservation_id)
    except MongoReservation.DoesNotExist:
        messages.error(request, "Cette réservation n'existe pas!")
        return redirect('user_events')

    # Check if TTL expired
    if reservation.expires_at and reservation.expires_at <= datetime.now() and reservation.status == "pending":
        # TTL expired = redirect back to event with error
        event_id = str(reservation.event.id)

        reservation.delete()
        messages.error(request, "Réservation expirée... Veuillez réessayer.")
        return redirect('user_event_detail', event_id=event_id)


    # If the user clicked "Confirmer la réservation" POST
    if request.method == "POST":
        reservation.status = "confirmed"
        reservation.confirmed_at = datetime.now()
        reservation.expires_at = None  # remove TTL
        reservation.payment_status = "paid"
        reservation.payment_method = "PayDunia"
        reservation.save()

        # Add user to event participants
        user = reservation.user
        event = reservation.event
        if user not in event.participants:
            event.participants.append(user)
            event.save()

        # Decrease only when confirmed
        event.available_slots -= 1
        event.save()

        return redirect('validated_reservation')  # route to validated.html

    # Otherwise, GET request shows confirm.html
    return render(request, 'reservations/confirm.html', {
        'reservation': reservation,
        'color_on_scroll': 30,
    })



def validated_reservation(request):
    return render(request, 'reservations/validated.html', {
        'color_on_scroll': 30,
    })
