# authentication/social_pipelines.py

from social_core.exceptions import AuthAlreadyAssociated
from .models import CustomUserSocialAuth
from organizer.models import EventNestUsers
def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    try:
        social = CustomUserSocialAuth.objects.get(provider=provider, uid=uid)
    except CustomUserSocialAuth.DoesNotExist:
        social = None

    if social:
        if user and social.user != user:
            raise AuthAlreadyAssociated(backend)
        elif not user:
            user = social.user

    return {
        "social": social,
        "user": user,
        "is_new": user is None,
        "new_association": social is None,
    }

def associate_custom_user(backend, uid, user=None, *args, **kwargs):
    if user:
        if not isinstance(user, EventNestUsers):
            raise ValueError("User must be an instance of EventNestUsers")
        CustomUserSocialAuth.objects.get_or_create(
            user=user,
            provider=backend.name,
            uid=uid,
        )
    return {'user': user}
