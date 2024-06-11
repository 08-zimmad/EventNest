from .models import Organizer
from .serializer import OrganizerSerializer
def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':

        serializer=OrganizerSerializer(
            name=response.get("username"),
            email=response.get("email")
                                       )
        if serializer.is_valid():
            serializer.save()
        

