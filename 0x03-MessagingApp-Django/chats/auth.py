from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # You can add custom logic here if needed before or after default JWT auth
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            # Optionally, handle exceptions or log them
            raise

class CustomSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        # You can override to customize session authentication behavior
        return super().authenticate(request)
