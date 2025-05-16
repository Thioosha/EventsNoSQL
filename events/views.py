from django.shortcuts import render, redirect
from users.models import MongoUser


# Create your views here

# def user_events(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('register')
    
#     user = MongoUser.objects.get(id=user_id)
    
#     if user.account_type != 'participant':
#         return redirect('creer_event') 
    
#     return render(request, 'events/user_events.html', {
#         'color_on_scroll': 30
#     })

# def user_events(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('register')
    
#     user = MongoUser.objects.get(id=user_id)
    
#     if user.account_type != 'participant':
#         return redirect('creer_event')
    
#     events = MongoEvent.objects(status__nin=["cancelled", "archived"]).order_by('start_datetime')
#     main_event = events.first()
#     other_events = events[1:] if events.count() > 1 else []
    
#     return render(request, 'events/user_events.html', {
#         'color_on_scroll': 30,
#         'main_event': main_event,
#         'other_events': other_events
#     })

def user_events(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')
    
    user = MongoUser.objects.get(id=user_id)

    if user.account_type != 'participant':
        return redirect('creer_event') 

    events = MongoEvent.objects(status__nin=["cancelled", "archived"]).order_by('start_datetime')
    main_event = events.first()
    other_events = events[1:] if events.count() > 1 else []

    return render(request, 'events/user_events.html', {
        'main_event': main_event,
        'other_events': other_events,
        'color_on_scroll': 30
    })

# def user_event_detail(request, event_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('register')

#     user = MongoUser.objects.get(id=user_id)

#     try:
#         event = MongoEvent.objects.get(id=event_id)
#     except MongoEvent.DoesNotExist:
#         return render(request,  'events/user_events.html')
    
#     return render(request, 'events/user_event_detail.html', {
#         'event': event,
#         'user': user,
#         'color_on_scroll': 30
#     })

from django.shortcuts import render, get_object_or_404
from .models import MongoEvent

from django.shortcuts import render
from django.http import Http404
from .models import MongoEvent

def user_event_detail(request, event_id):
    try:
        event = MongoEvent.objects.get(id=event_id)
    except MongoEvent.DoesNotExist:
        raise Http404("Event not found...")

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
    'color_on_scroll': 30,  # change this to any value you want for this page
})




