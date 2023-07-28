# accounts/middleware.py

from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.http import JsonResponse


class TokenExpirationMiddleware:
    def __init__(self, get_response):
        """
        Initialize the TokenExpirationMiddleware.

        Args:
            get_response (function): The callable that represents the next middleware or view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and perform token expiration checks.

        If the request contains an Authorization header with a token, this middleware will check if the token has expired.
        If the token has expired, it will be deleted and an error response will be returned.
        If the token is still valid, its expiration time will be updated to extend its validity.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response from the view or the error response if the token has expired.
        """
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token_key = auth_header.split(' ')[1]  # Extract the token from the Authorization header
            try:
                token = Token.objects.get(key=token_key)

                if token.created < timezone.now() - timezone.timedelta(days=7):
                    token.delete()  # Token has expired, delete it
                    response_data = {'message': 'Token has expired. Please log in again.'}
                    return JsonResponse(response_data, status=401)
                else:
                    # Update token's created time to extend its expiration
                    token.created = timezone.now()
                    token.save()

            except Token.DoesNotExist:
                print('Token.DoesNotExist')
                response_data = {
                    'message': 'Invalid token'
                }
                return JsonResponse(response_data, status=401)

        response = self.get_response(request)
        return response
