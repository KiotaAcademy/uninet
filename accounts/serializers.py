# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import CustomUser as User
from accounts.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']  # Add more fields as needed
        extra_kwargs = {
            'password': {'write_only': True}  # Hide password field in response
        }

    def validate(self, data):
        """
        Validate user data.

        This method performs the following checks:
        - Compares the provided password with the confirm_password field to ensure they match.
        - Validates the password using Django's password validation, which checks the following:
            - The password is at least 8 characters long.
            - The password does not contain common sequences or repeated characters.
            - The password is not entirely numeric.
            - The password is not too similar to user attributes (e.g., username, first name, last name, email).

        Args:
            data (dict): The user data to be validated.

        Raises:
            serializers.ValidationError: If the passwords do not match or the password validation fails.

        Returns:
            dict: The validated user data.
        """
        
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError("The passwords do not match.")

        try:
            validate_password(password, user=User(**data))
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data

    def create(self, validated_data):
        """
        Create a new user.

        Args:
            validated_data (dict): The validated user data.

        Returns:
            User: The newly created user.
        """
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'location', 'contact_number', 'website', 'facebook', 'twitter', 'instagram', 'tiktok', 'linkedin', 'youtube']
