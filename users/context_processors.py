from .models import MongoUser

def current_user(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = MongoUser.objects.get(id=user_id)
        except MongoUser.DoesNotExist:
            pass
    return {'user': user}
