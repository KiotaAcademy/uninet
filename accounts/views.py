# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


from accounts.serializers import UserSerializer, UserProfileSerializer
from accounts.models import CustomUser as User
from accounts.models import UserProfile

class GlobalFunctions:
    @staticmethod
    def generate_email_verification_token(user):
        """
        Generates a unique email verification token for the user.

        Args:
            user (User): The user for whom the token is generated.

        Returns:
            str: The generated email verification token.
        """
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verification_token = f"{uid}_{token}"

        return verification_token

    @staticmethod
    def send_verification_email(request, email, verification_token, username):
        """
        Sends a verification email to the user.

        Args:
            request (HttpRequest): The current request.
            email (str): The email address of the user.
            verification_token (str): The verification token.
            username (str): The username of the user.
        """
        current_site = get_current_site(request)
        verification_url = reverse('verify-email')
        absolute_url = f"http://{current_site.domain}{verification_url}?token={verification_token}"
        subject = 'Verify Your Email'
        message = f'Hello {username},\n\nClick the following link to verify your email: {absolute_url}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        email = EmailMessage(subject, message, from_email, to_email)
        email.send()

    @staticmethod
    def generate_token(user):
        """
        Generates a token for the user.

        Args:
            user (User): The user for whom the token is generated.

        Returns:
            str: The generated token.
        """
        token, created = Token.objects.get_or_create(user=user)
        return token.key


class UserRegistrationView(APIView):
    def post(self, request):
        """
        Handles the registration of a new user.

        Args:
            request (HttpRequest): The current request.

        Returns:
            Response: The response containing the registration status.
        """
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # Create a user profile
            UserProfile.objects.create(user=user)

            verification_token = GlobalFunctions.generate_email_verification_token(user)
            GlobalFunctions.send_verification_email(request, user.email, verification_token, user.username)

            response_data = {
                'message': f'A verification email has been sent to {user.email} for the user {user.username}.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class VerifyEmailView(APIView):
    def get(self, request):
        """
        Verifies the user's email address.

        Args:
            request (HttpRequest): The current request.

        Returns:
            Response: The response containing the verification status and token.
        """
        token = request.GET.get('token')

        try:
            uidb64, token = token.split('_', 1)
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.email_verified = True
                user.is_active = True
                user.save()

                token = GlobalFunctions.generate_token(user)

                return Response({
                    'message': 'Email verification successful.',
                    'token': token
                }, status=status.HTTP_200_OK)

            else:
                return Response({'message': 'Invalid verification token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except TypeError:
            return Response({'message': 'Invalid verification token: TypeError.'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({'message': 'Invalid verification token: ValueError.'}, status=status.HTTP_400_BAD_REQUEST)

        except OverflowError:
            return Response({'message': 'Invalid verification token: OverflowError.'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        """
        Handles user authentication and token generation.

        Args:
            request (HttpRequest): The current request.

        Returns:
            Response: The response containing the authentication status and token.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        token = GlobalFunctions.generate_token(user)

        serializer = UserSerializer(user)
        data = {
            'token': token,
            'user': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    def post(self, request):
        """
        Logs out the user by deleting the authentication token.

        Args:
            request (HttpRequest): The current request.

        Returns:
            Response: The response indicating the logout status.
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                token.delete()
                return Response({'message': 'Logged out successfully.'}, status=status.HTTP_204_NO_CONTENT)
            except Token.DoesNotExist:
                return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No token provided.'}, status=status.HTTP_400_BAD_REQUEST)


    
class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retrieves the user's profile.

        Args:
            request (HttpRequest): The current request.

        Returns:
            Response: The response containing the user's profile data.
        """
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
        
    def put(self, request):
        """
        Updates the user's profile.

        Args:
            request (HttpRequest): The current request.

        Returns:
            Response: The response containing the updated profile data or error messages.
        """
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDeleteView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        Deletes the user's account.

        Args:
            request (HttpRequest): The current request.

        Returns:
            Response: The response indicating the account deletion status.
        """
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
        user.delete()
        return Response({'message': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
