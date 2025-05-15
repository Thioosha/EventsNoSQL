from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from datetime import datetime, timedelta

@receiver(post_save, sender=Reservation)
def check_reservation_expiry(sender, instance, **kwargs):
    if instance.status == 'pending' and instance.expires_at <= datetime.now():
        instance.cancel()  # Appel à la méthode du modèle