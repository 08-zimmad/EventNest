from django.urls import path, include, re_path
from authentication.auth_serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer
    )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )

from .views import (
    EventView,
    FetchAllEventsViews,
    UpdateProfileView,
    GiveRating,
    AttendeeRegistrationView
    )
from authentication.views import login_attendee

urlpatterns = [
    # attendee routes
    path('api/register/',
         AttendeeRegistrationView.as_view(),
         name="attendee-signup-view"
         ),
    path('api/<int:pk>/',
         EventView.as_view(),
         name="events-attendee-registration"
         ),
    path('api/get_all/',
         FetchAllEventsViews.as_view(),
         name="get-all-events-available-view"
         ),
    path('api/profile/',
         UpdateProfileView.as_view(),
         name="attendee-profile-view"
         ),
    path('api/rate/<int:pk>/',
         GiveRating.as_view(),
         name="rating-view"
         ),

    # JWT routes
    path('api/token/',
         TokenObtainPairView.as_view(
             serializer_class=CustomTokenObtainPairSerializer
             ),
         name='token_obtain_pair'
         ),
    path('api/token/refresh',
         TokenRefreshView.as_view(
             serializer_class=CustomTokenRefreshSerializer
             ),
         name='token_refresh'
         ),
     
     #  oauth2
    path('social/', include('social_django.urls', namespace='social')),
    re_path(r'^oauth2/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/auth2/', login_attendee),
]
