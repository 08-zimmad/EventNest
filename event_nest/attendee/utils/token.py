from rest_framework_simplejwt.tokens import RefreshToken

def get_access_token(user):
    token = RefreshToken.for_user(user)
    return {
        "access": str(token.access_token),
    }
