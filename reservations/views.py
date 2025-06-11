from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from events.models import MongoEvent
from users.models import MongoUser
from .models import MongoReservation
from mongoengine import ValidationError
from django.contrib import messages
from django.urls import reverse

import qrcode
import tempfile
import requests
from django.conf import settings

def create_reservation(request, event_id):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                raise ValidationError("Utilisateur non connecté !")

            user = MongoUser.objects.get(id=user_id)
            event = MongoEvent.objects.get(id=event_id)

            # Check if user already reserved this event
            existing = MongoReservation.objects(event=event, user=user, status="confirmed").first()
            if existing:
                return redirect(f"{reverse('user_event_detail', args=[str(event_id)])}?error=already_reserved")

            # Récupérer les champs adults et children depuis le formulaire
            adults = int(request.POST.get('adults', 1))
            children = int(request.POST.get('children', 0))

            total_requested = adults + children
            if event.available_slots < total_requested:
                return redirect(f"{reverse('user_event_detail', args=[str(event_id)])}?error=not_enough_slots")

            reservation = MongoReservation(
                user=user,
                event=event,
                adults=adults,
                children=children,
                expires_at=datetime.now() + timedelta(seconds=25)
            )
            reservation.save()

            return redirect('confirm_reservation', reservation_id=str(reservation.id))

        except Exception as e:
            print(f"Error creating reservation: {e}")
            return redirect(f"{reverse('user_event_detail', args=[str(event_id)])}?error=expired")



IMGBB_API_KEY = "71106fa24c9850b035d087a4513b07d2"

def upload_to_imgbb(image_path):
    with open(image_path, 'rb') as f:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY},
            files={"image": f}
        )
    if response.status_code == 200:
        return response.json()['data']['url']
    return None


def confirm_reservation(request, reservation_id):
    try:
        reservation = MongoReservation.objects.get(id=reservation_id)
    except MongoReservation.DoesNotExist:
        messages.error(request, "Cette réservation n'existe pas!")
        return redirect('user_events')

    if reservation.expires_at and reservation.expires_at <= datetime.now() and reservation.status == "pending":
        event_id = str(reservation.event.id)
        reservation.delete()
        messages.error(request, "Réservation expirée... Veuillez réessayer.")
        return redirect('user_event_detail', event_id=event_id)

    if request.method == "POST":
        total_people = reservation.adults + reservation.children
        event = reservation.event

        if event.available_slots < total_people:
            messages.error(request, "Pas assez de places disponibles pour valider cette réservation.")
            return redirect('user_event_detail', event_id=str(event.id))

        reservation.status = "confirmed"
        reservation.confirmed_at = datetime.now()
        reservation.expires_at = None
        reservation.payment_status = "paid"
        reservation.payment_method = "PayDunia"

        # Generate QR code
        qr_data = (
            f"🎟️ Réservation ID: {reservation.id}\n"
            f"👤 Nom complet: {reservation.user.full_name}\n"
            f"👨‍👩‍👧‍👦 Adultes: {reservation.adults}, Enfants: {reservation.children}\n"
            f"📅 Événement: {reservation.event.title}"
        )
        qr = qrcode.make(qr_data)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            qr.save(tmp_file.name)
            imgbb_url = upload_to_imgbb(tmp_file.name)

        
        if imgbb_url:
            reservation.ticket = imgbb_url

        reservation.save()

        user = reservation.user
        if str(reservation.id) not in [str(rid) for rid in user.reservations]:
            user.reservations.append(reservation.id)
            user.save()

        if user not in event.participants:
            event.participants.append(user)

        event.available_slots -= total_people
        event.save()

        return redirect('validated_reservation')

    return render(request, 'reservations/confirm.html', {
        'reservation': reservation,
        'color_on_scroll': 30,
    })


def validated_reservation(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = MongoUser.objects.get(id=user_id)
        reservation = MongoReservation.objects.filter(user=user, status="confirmed").order_by('-confirmed_at').first()
    except (MongoUser.DoesNotExist, MongoReservation.DoesNotExist):
        reservation = None

    return render(request, 'reservations/validated.html', {
        'color_on_scroll': 30,
        'ticket': reservation.ticket if reservation else None
    })

