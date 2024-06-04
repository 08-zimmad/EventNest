from django.urls import path, include
from .views import OrganizerRegisterView, OrganizerLoginView, EventView
from .serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
urlpatterns = [
    path('api/organizer/register/', OrganizerRegisterView.as_view(), name='organizer_register'),
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('accounts/', include('allauth.urls')),
    path('api/organizer/<int:event_id>/',EventView.as_view()),
    path('api/organizer/',EventView.as_view())
]
