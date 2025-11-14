from clerk_backend_api import Clerk
from rest_framework.authentication import BaseAuthentication, exceptions
from clerk_backend_api.security.types import AuthenticateRequestOptions
from django.contrib.auth import get_user_model
import environ
from django.conf import settings

class ClerkAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_headers: str = request.headers.get("Authorization")
        if not auth_headers or not auth_headers.startswith("Bearer"):
            return None
        
        token = auth_headers.split(" ")[1]
        clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
        
        opts = AuthenticateRequestOptions(
            authorized_parties=[settings.CLERK_FRONTEND_API_URL,'http://localhost:5173'],
        )
        
        try:
            request_state = clerk.authenticate_request(request, opts)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid token') from e
        
        if not request_state.is_signed_in:
            raise exceptions.AuthenticationFailed('User not signed in')

        payload = request_state.payload  # dict of user info from Clerk

        # Here you can get the user id from payload
        clerk_user_id = payload.get('sub')  # e.g., “usr_xxx”
        if clerk_user_id is None:
            raise exceptions.AuthenticationFailed('Invalid payload')
        
        User = get_user_model()
        try :
            user = User.objects.get(clerk_id=clerk_user_id)
        except User.DoesNotExist:
            return exceptions.AuthenticationFailed("User not found in local database")
        
        return (user, None)
        
        