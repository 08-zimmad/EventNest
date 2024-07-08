from django.shortcuts import redirect
# from django.contrib.auth import login
from social_django.utils import psa

@psa('social:complete')
def custom_login(request, backend, role):
    request.session['role'] = role
    return redirect('social:begin', backend=backend)

def login_organizer(request):
    return custom_login(request, backend='google-oauth2', role='organizer')

def login_attendee(request):
    return custom_login(request, backend='google-oauth2', role='attendee')
