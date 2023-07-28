from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import UserProfile
from accounts.views import GlobalFunctions
from accounts.serializers import UserSerializer, UserProfileSerializer

User = get_user_model()

# Tests for UserRegistrationView
class UserRegistrationViewTestCase(APITestCase):
    """
    Test case for UserRegistrationView.
    """
    def test_user_registration(self):
        """
        Test user registration with valid data.
        """
        url = reverse('user-registration')
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassbrock',
            'confirm_password': 'testpassbrock'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'A verification email has been sent to test@example.com for the user testuser.')

# Tests for UserAuthenticationView
class UserAuthenticationTestCase(APITestCase):
    """
    Test case for UserAuthenticationView.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass', first_name='Test', last_name='User')

    def test_user_login(self):
        """
        Test user login with valid credentials.
        """
        url = reverse('user-login')
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertIn('token', response.data)

    def test_user_logout(self):
        """
        Test user logout.
        """
        url = reverse('user-logout')

        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        # Generate an authentication token for the user
        token = Token.objects.create(user=self.user)
        
        # Make the request with the Authorization header
        response = self.client.post(url, headers={'Authorization': f'Token {token.key}'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the user token is deleted or invalidated
        self.assertFalse(Token.objects.filter(key=token.key).exists())

        # Add an additional request to verify that the user is no longer authenticated
        response = self.client.get(reverse('user-profile'), headers={'Authorization': f'Token {token.key}'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Tests for VerifyEmailView
class VerifyEmailViewTestCase(APITestCase):
    """
    Test case for VerifyEmailView.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass', first_name='Test', last_name='User')
        self.profile = UserProfile.objects.create(user=self.user)
        self.verification_token = GlobalFunctions.generate_email_verification_token(self.user)

    def test_verify_email(self):
        """
        Test email verification with a valid token.
        """
        url = reverse('verify-email') + f'?token={self.verification_token}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email verification successful.')

        # Assert that the user is now activated or verified
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.is_active)
        self.assertTrue(user.email_verified)

# Tests for UserProfileView
class UserProfileViewTestCase(APITestCase):
    """
    Test case for UserProfileView.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass', first_name='Test', last_name='User')
        self.profile = UserProfile.objects.create(user=self.user)

    def test_get_user_profile(self):
        """
        Test retrieval of user profile.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('user-profile')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "avatar": None,
            "bio": "",
            "location": "",
            "contact_number": "",
            "website": "",
            "facebook": "",
            "twitter": "",
            "instagram": "",
            "tiktok": "",
            "linkedin": "",
            "youtube": ""
        })

    def test_update_user_profile(self):
        """
        Test update of user profile.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('user-profile')
        data = {
            'bio': 'This is a test bio.',
            'location': 'Test City',
            'contact_number': '1234567890'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'This is a test bio.')
        self.assertEqual(response.data['location'], 'Test City')
        self.assertEqual(response.data['contact_number'], '1234567890')



class UserDeleteViewTestCase(APITestCase):
    """
    Test case for UserDeleteView.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        self.profile = UserProfile.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)

    def test_delete_user(self):
        """
        Test deleting the user account.
        """
        url = reverse('user-delete')

        # Set the Authorization header with the user's token
        headers = {'Authorization': f'Token {self.token.key}'}

        # Authenticate the test client with the user's token
        self.client.force_authenticate(user=self.user)

        # Make the DELETE request to delete the user account
        response = self.client.delete(url, headers=headers)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the user and profile are deleted from the database
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())

        # Verify that the token is deleted or invalidated
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

# Optional: Add more test cases to cover edge cases and additional functionality







# Test cases for serializers.py
class UserSerializerTestCase(TestCase):
    """
    Test case for UserSerializer.
    """
    def test_user_serializer_validation(self):
        """
        Test user serializer validation.
        """
        serializer = UserSerializer(data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassbrock',
            'confirm_password': 'testpassbrock'
        })
        self.assertTrue(serializer.is_valid())

    def test_user_serializer_creation(self):
        """
        Test user serializer creation.
        """
        serializer = UserSerializer(data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassbrock',
            'confirm_password': 'testpassbrock'
        })
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        # Add more assertions as needed

class UserProfileSerializerTestCase(TestCase):
    """
    Test case for UserProfileSerializer.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass', first_name='Test', last_name='User')

    def test_user_profile_serializer(self):
        """
        Test user profile serializer.
        """
        profile = UserProfile.objects.create(user=self.user, bio='Test bio', location='Test location')
        serializer = UserProfileSerializer(profile)
        self.assertEqual(serializer.data['bio'], 'Test bio')
        self.assertEqual(serializer.data['location'], 'Test location')
        # Add more assertions as needed






# Test cases for models.py
class CustomUserModelTestCase(TestCase):
    """
    Test case for CustomUser model.
    """
    def test_custom_user_creation(self):
        """
        Test custom user creation.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass', first_name='Test', last_name='User')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        # Add more assertions as needed

class UserProfileModelTestCase(TestCase):
    """
    Test case for UserProfile model.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass', first_name='Test', last_name='User')

    def test_user_profile_creation(self):
        """
        Test user profile creation.
        """
        profile = UserProfile.objects.create(user=self.user, bio='Test bio', location='Test location')
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.location, 'Test location')
        # Add more assertions as needed
