from django.urls import path, include
from .views import OrganizerRegisterView, EventView, google_login
from .serializer import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_social_oauth2.views import ConvertTokenView
from django.urls import re_path
urlpatterns = [
        # JWT
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(serializer_class=CustomTokenRefreshSerializer), name='token_refresh'),


    #Organizer
    path('api/organizer/register/', OrganizerRegisterView.as_view(), name='organizer_register'),
    path('api/organizer/<int:event_id>/',EventView.as_view()),
    path('api/organizer/',EventView.as_view()),


    #oauth2
    path('social/', include('social_django.urls', namespace='social')),
    re_path(r'^oauth2/', include('drf_social_oauth2.urls', namespace='drf')),
    path('google-login/', google_login, name='google_login')
]



