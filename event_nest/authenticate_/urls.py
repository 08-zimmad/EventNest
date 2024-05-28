from django.urls import path
from .views import OrganizerLogin, SignUpView

urlpatterns = [
    path("token/",OrganizerLogin.as_view()),
    path('signup/', SignUpView.as_view(), name='signup')
]

