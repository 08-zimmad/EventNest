from .models import CustomUserSocialAuth
from organizer.models import EventNestUsers
from social_django.models import UserSocialAuth

def custom_social_user(backend, uid, user=None, *args, **kwargs):
    if user:
        return {'social': None}

    try:
        if backend.name == "google-oauth2":
            social = CustomUserSocialAuth.objects.get(provider=backend.name, uid=uid)
    except (CustomUserSocialAuth.DoesNotExist):
        social = None

    if social:
        user = social.user

    return {'social': social, 'user': user}




def custom_associate_user(backend, uid, user=None, social=None, *args, **kwargs):
    if social:
        return None
    
    if backend.name == 'googe-oauth2':
        if isinstance(user, EventNestUsers):
            CustomUserSocialAuth.objects.get_or_create(provider=backend.name, uid=uid, defaults={'user': user})
    else:
        if isinstance(user, EventNestUsers):
            UserSocialAuth.objects.get_or_create(provider=backend.name, uid=uid, defaults={'user': user})




def custom_load_extra_data(backend, details, response, user=None, social=None, *args, **kwargs):
    if social:
        social.extra_data = response
        social.save()
    return None

