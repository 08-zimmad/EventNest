def save_profile(backend, user, response, *args, **kwargs):
    # Example custom logic to save user profile
    if backend.name == 'google-oauth2':
        user.first_name = response.get('given_name')
        user.last_name = response.get('family_name')
    user.save()


def get_email(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.email=response.get('email')
    user.save()