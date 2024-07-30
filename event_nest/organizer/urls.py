from authentication.auth_serializers import CustomTokenRefreshSerializer
from authentication.auth_serializers import CustomTokenObtainPairSerializer
from authentication.views import login_organizer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.urls import re_path
from django.urls import path, include
from .views import (
    EventNestRegisterView, EventView,
    UpdateProfileView, MarkAttendanceView,
    UploadMediaFilesView, GetEventView,
    RegisteredAttendeeView,
)


urlpatterns = [
    #  JWT
    path('api/token/', TokenObtainPairView.as_view(
        serializer_class=CustomTokenObtainPairSerializer
        ),
         name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(
        serializer_class=CustomTokenRefreshSerializer
        ),
        name='token_refresh'),

    #  Organizer
    path('api/register/',
         EventNestRegisterView.as_view(),
         name="eventnest-register-view"),
    path('api/event/<int:pk>/',
         GetEventView.as_view(),
         name="get-event-view"),
    path('api/<int:pk>/',
         EventView.as_view(),
         name="event-view-with-id"),
    path('api/events/',
         EventView.as_view(),
         name="event-view"),
    path('api/profile/',
         UpdateProfileView.as_view(),
         name="update-profile-view"),
    path('api/attendance/<int:pk>/',
         MarkAttendanceView.as_view(),
         name="mark-attendance-view"),
    path('api/uploadfile/<int:pk>/',
         UploadMediaFilesView.as_view(),
         name="upload-media-files-view"),
    path('api/get_attendees/<int:pk>/',
         RegisteredAttendeeView.as_view(),
         name="registered-attendee-view"),

    #  oauth2
    path('social/', include('social_django.urls', namespace='social')),
    re_path(r'^oauth2/', include('drf_social_oauth2.urls', namespace='drf')),
    #  path('google-login/', google_login, name='google_login')
    path('api/auth2/', login_organizer),
]
