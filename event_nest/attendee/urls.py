from django.urls import path
from authentication.auth_serializers import(
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer
    )
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
    )
from .views import(
    EventView,
    FetchAllEventsViews,
    UpdateProfileView,
    GiveRating,AttendeeRegistrationView
    )


urlpatterns = [
    # attendee routes
    path('api/register/', AttendeeRegistrationView.as_view(), name="attendee-signup-view"),
    # path('api/', EventView.as_view(), name="events-view"),
    path('api/<int:pk>/', EventView.as_view(), name="events-attendee-registration"),
    path('api/get_all/', FetchAllEventsViews.as_view(), name="get-all-events-available-view"),
    path('api/profile/', UpdateProfileView.as_view(), name="attendee-profile-view"),
    path('api/rate/<int:pk>/', GiveRating.as_view(), name="rating-view"),

    # JWT routes
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(serializer_class=CustomTokenRefreshSerializer), name='token_refresh'),
]
