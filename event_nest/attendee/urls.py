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
    EventRegistration,
    FetchAllEventsViews,
    UpdateProfileView,
    GiveRating,AttendeeRegistration
    )


urlpatterns = [
    # attendee routes
    path('api/register/', AttendeeRegistration.as_view()),
    path('api/', EventRegistration.as_view()),
    path('api/<int:pk>/', EventRegistration.as_view()),
    path('api/get_all/', FetchAllEventsViews.as_view()),
    path('api/profile/', UpdateProfileView.as_view()),
    path('api/rate/<int:pk>/', GiveRating.as_view()),

    # JWT routes
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(serializer_class=CustomTokenRefreshSerializer), name='token_refresh'),
]
