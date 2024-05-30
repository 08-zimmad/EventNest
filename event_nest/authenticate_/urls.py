from django.urls import path, include
from .views import OrganizerRegisterView, OrganizerLoginView

urlpatterns = [
    path('api/organizer/register/', OrganizerRegisterView.as_view(), name='organizer_register'),
    path('api/organizer/login/', OrganizerLoginView.as_view(), name='organizer_login'),
    path('accounts/', include('allauth.urls')),
]
