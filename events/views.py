from django.shortcuts import render, redirect
from users.models import MongoUser


# Create your views here

CATEGORY_CHOICES = [
    "Musique", "Art", "Conférence", "Sport", "Atelier", "Formation", "Technologie",
    "Rencontre", "Mode", "Santé", "Voyage", "Cinéma", "Théâtre", "Danse", "Gaming",
    "Littérature", "Religion", "Cuisine", "Networking", "Autre"
]

def user_events(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = MongoUser.objects.get(id=user_id)

    events = MongoEvent.objects(status__nin=["cancelled", "archived"])

    # --- Filtrage ---
    category = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category:
        events = events.filter(category=category)
    if price_min:
        events = events.filter(price__gte=float(price_min))
    if price_max:
        events = events.filter(price__lte=float(price_max))
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            events = events.filter(start_datetime__gte=start)
        except:
            pass
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            events = events.filter(end_datetime__lte=end)
        except:
            pass

    events = events.order_by('start_datetime')

    main_event = events.first()
    carousel_events = events[1:6] if events.count() > 1 else []
    remaining_events = events[6:] if events.count() > 6 else []

    return render(request, 'events/user_events.html', {
        'main_event': main_event,
        'carousel_events': carousel_events,
        'remaining_events': remaining_events,
        'color_on_scroll': 30,
        'categories': CATEGORY_CHOICES,  # pour la liste déroulante
        'filters': {
            'category': category,
            'price_min': price_min,
            'price_max': price_max,
            'start_date': start_date,
            'end_date': end_date,
        }
    })



# def user_events(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('register')

#     user = MongoUser.objects.get(id=user_id)

#     events = MongoEvent.objects(status__nin=["cancelled", "archived"]).order_by('start_datetime')

#     main_event = events.first()
#     carousel_events = events[1:6] if events.count() > 1 else []
#     remaining_events = events[6:] if events.count() > 6 else []
    

#     return render(request, 'events/user_events.html', {
#         'main_event': main_event,
#         'carousel_events': carousel_events,
#         'remaining_events': remaining_events,
#         'color_on_scroll': 30
#     })

from django.shortcuts import render, get_object_or_404
from .models import MongoEvent

from django.shortcuts import render
from django.http import Http404
from .models import MongoEvent

from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from mongoengine import ValidationError
from events.models import MongoEvent
from reservations.models import MongoReservation
from users.models import MongoUser

from django.contrib import messages

def user_event_detail(request, event_id):
    try:
        event = MongoEvent.objects.get(id=event_id)
    except MongoEvent.DoesNotExist:
        raise Http404("Event not found 🚫")

    # Check for reservation errors sent via GET
    error = request.GET.get('error')
    if error == 'expired':
        messages.error(request, "La réservation a expiré. Veuillez réessayer.")
    elif error == 'already_reserved':
        messages.warning(request, "Vous avez déjà une réservation pour cet événement ⚠️")
    elif error == 'not_enough_slots':
        messages.error(request, "Nombre de places insuffisant pour cette réservation ⚠️")

    return render(request, 'events/user_event_detail.html', {
        'event': event,
        'color_on_scroll': 30,
    })






from django.shortcuts import render, redirect
from .forms import MongoEventForm
from .models import MongoEvent
from users.models import MongoUser
from datetime import datetime, timezone

import requests
import base64

IMGBB_API_KEY = "71106fa24c9850b035d087a4513b07d2"  #https://api.imgbb.com/

def upload_image_to_imgbb(image_file):
    image_data = base64.b64encode(image_file.read()).decode("utf-8")
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
        "image": image_data,
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()["data"]["url"]
    else:
        return None
    
def create_event(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = MongoUser.objects.get(id=user_id)

    if user.account_type != 'organizer':
        return redirect('user_events')

    if request.method == 'POST':
        form = MongoEventForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES.get("image")
            image_url = upload_image_to_imgbb(image) if image else None

            data = form.cleaned_data
            event = MongoEvent(
                title=data['title'],
                description=data.get('description'),
                location=data['location'],
                start_datetime=data['start_datetime'],
                end_datetime=data['end_datetime'],
                available_slots=data['available_slots'],
                image_url=image_url,
                created_by=user,
                price=data['price'],
                category=data['category'],
                status="active",
                created_at=datetime.now(timezone.utc),
            )
            event.total_slots = data['total_slots']
            event.save()
            return redirect('dashboard')
    else:
        form = MongoEventForm()

    return render(request, 'events/creer_event.html', {
    'form': form,
    'color_on_scroll': 30,
})




