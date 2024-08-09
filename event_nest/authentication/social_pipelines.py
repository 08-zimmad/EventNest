# from social_core.exceptions import (
#     AuthException
# )

# def social_user(backend, uid, user=None, *args, **kwargs):

#     from social_django.models import UserSocialAuth
#     from django.contrib.auth import get_user_model
#     User = get_user_model()
#     social = None
#     try:
#         social = UserSocialAuth.objects.get(provider=backend.name, uid=uid)
#         user = social.user
#     except UserSocialAuth.DoesNotExist:
#         try:
#             user = User.objects.get(email=uid)
#         except User.DoesNotExist:
#             user = None
#     return {'social': social, 'user': user}


# def create_user(strategy, details, backend, user=None, *args, **kwargs):
#     if user:
#         return {'is_new': False}
#     request = strategy.request
#     fields = {
#         'name': details.get('username'),
#         'email': details.get('email'),
#         'role': request.session.get('role')
#     }

#     if not fields['email']:
#         raise AuthException(backend, 'Email is required to create a user account.')

#     user = strategy.create_user(**fields)
#     return {'is_new': True, 'user': user}
