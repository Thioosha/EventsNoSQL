from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect
from .forms import AccountTypeForm, RegisterForm
from mongoengine.errors import NotUniqueError
from .models import MongoUser

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
                    password=form.cleaned_data['password'],
                    full_name=form.cleaned_data['full_name'],
                    account_type=account_type,
                    reservations=[],
                    created_events=[],
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

def login_view(request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        context['email'] = email

        try:
            user = MongoUser.objects.get(email=email, password=password)
            request.session['user_id'] = str(user.id)
            return redirect('home')
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
    return render(request, 'users/settings.html')
