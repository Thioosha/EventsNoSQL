from django.shortcuts import render, redirect
from users.models import MongoUser


# Create your views here

def user_events(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')
    user = MongoUser.objects.get(id=user_id)
    if user.account_type != 'participant':
        return redirect('creer_event') 
    return render(request, 'events/user_events.html')

def create_event(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')
    user = MongoUser.objects.get(id=user_id)
    if user.account_type != 'organizer':
        return redirect('user_events')
    return render(request, 'events/creer_event.html')