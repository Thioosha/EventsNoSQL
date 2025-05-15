from django.shortcuts import render,redirect

# Create your views here.
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')
    # You can add more context if you want, sexy
    return render(request, 'dashboard/dashboard.html')