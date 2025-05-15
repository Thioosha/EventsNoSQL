from datetime import datetime, timedelta
from .models import Reservation

def create_reservation(user, event):
    """Créer une réservation avec expiration automatique"""
    reservation = Reservation(
        user=user,
        event=event,
        expires_at=datetime.now() + timedelta(minutes=30))
    reservation.save()
    return reservation

def confirm_reservation(reservation_id):
    """Confirmer une réservation"""
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.update(status='confirmed', expires_at=None)