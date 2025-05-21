from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect
from .forms import AccountTypeForm, RegisterForm
from mongoengine.errors import NotUniqueError
from .models import MongoUser
from django.contrib.auth.hashers import make_password


def home(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = MongoUser.objects.get(id=user_id)
        except MongoUser.DoesNotExist:
            pass

    return render(request, 'users/home.html', {'user': user})




def account_type_view(request):
    if request.method == 'POST':
        form = AccountTypeForm(request.POST)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            request.session['account_type'] = account_type  # Store temporarily
            return redirect('register')
    else:
        form = AccountTypeForm()
    return render(request, 'users/inscription1.html', {'form': form})


def register_view(request):
    account_type = request.session.get('account_type', 'participant')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = MongoUser(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=make_password(form.cleaned_data['password']),
                    full_name=form.cleaned_data['full_name'],
                    account_type=account_type,
                    reservations=[],
                    notifications=[],
                )
                user.save()

                # Set session
                request.session['user_id'] = str(user.id)
                request.session['username'] = user.username
                request.session['account_type'] = user.account_type

                # Redirect to home
                return redirect('home')
            except NotUniqueError:
                form.add_error('username', "Ce nom d'utilisateur est déjà pris.")
    else:
        form = RegisterForm()
    return render(request, 'users/inscription2.html', {'form': form})

from django.contrib.auth.hashers import check_password

def login_view(request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        context['email'] = email

        try:
            # Just get user by email
            user = MongoUser.objects.get(email=email)

            # Now check the password hash
            if check_password(password, user.password):
                request.session['user_id'] = str(user.id)
                request.session['username'] = user.username
                request.session['account_type'] = user.account_type
                return redirect('home')
            else:
                context['error'] = "Email ou mot de passe incorrect"

        except MongoUser.DoesNotExist:
            context['error'] = "Email ou mot de passe incorrect"

    return render(request, 'users/login.html', context)



def logout_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('login')


from django.contrib.auth.decorators import login_required  # optional

def user_settings_view(request):
    return render(request, 'users/settings.html', {
        'color_on_scroll': 30,
    })




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import MongoUser
import requests, base64

IMGBB_API_KEY = "71106fa24c9850b035d087a4513b07d2"

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


def update_profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = MongoUser.objects.get(id=user_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('pfp')

        if profile_pic:
            image_url = upload_image_to_imgbb(profile_pic)
            if image_url:
                user.pfp = image_url
            else:
                messages.error(request, "Erreur lors de l'upload de l'image.")

        user.full_name = full_name
        user.email = email
        user.save()

        messages.success(request, "Profil mis à jour avec succès!")
        return redirect('settings')

    return redirect('settings')

from django.contrib.auth.hashers import check_password, make_password

def update_password_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = MongoUser.objects.get(id=user_id)
    context = {'user': user}

    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        context['current'] = current
        context['new'] = new
        context['confirm'] = confirm

        errors = {}

        if not check_password(current, user.password):
            errors['current_error'] = "Mot de passe actuel incorrect!"

        if new != confirm:
            errors['confirm_error'] = "Les mots de passe ne correspondent pas."

        if new and len(new) < 6:
            errors['new_error'] = "Le nouveau mot de passe est trop court."

        if errors:
            context.update(errors)
            return render(request, 'users/settings.html', context)

        user.password = make_password(new)
        user.save()
        messages.success(request, "Mot de passe changé avec succès 🔐")
        return redirect('settings')

    return redirect('settings')

