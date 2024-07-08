# from social_django.storage import DjangoUserMixin, BaseDjangoStorage
# from social_core.storage import UserMixin
# from organizer.models import EventNestUsers
# from .models import CustomUserSocialAuth

# class CustomUserMixin(UserMixin):
#     user_model = EventNestUsers

#     def get_social_auth(self, provider, uid):
#         try:
#             return CustomUserSocialAuth.objects.get(provider=provider, uid=uid)
#         except CustomUserSocialAuth.DoesNotExist:
#             return None

# class CustomDjangoStorage(BaseDjangoStorage):
#     user = CustomUserMixin


from social_django.storage import BaseDjangoStorage
from social_core.storage import UserMixin
from .models import CustomUserSocialAuth
from organizer.models import EventNestUsers

class CustomUserMixin(UserMixin):
    user_model = EventNestUsers

    def get_social_auth(self, provider, uid=None):
        try:
            return CustomUserSocialAuth.objects.get(provider=provider, uid=uid)
        except CustomUserSocialAuth.DoesNotExist:
            return None

class CustomDjangoStorage(BaseDjangoStorage):
    user = CustomUserMixin
