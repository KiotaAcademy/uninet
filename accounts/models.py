from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    A custom manager for the CustomUser model.
    """

    def create_superuser(self, email, username, first_name, password, **other_fields):
        """
        Creates a superuser with the provided parameters.

        Args:
            email (str): The email address of the superuser.
            username (str): The username of the superuser.
            first_name (str): The first name of the superuser.
            password (str): The password of the superuser.
            **other_fields (dict): Additional fields for the superuser.

        Raises:
            ValueError: If the is_staff or is_superuser fields are not set to True.

        Returns:
            CustomUser: The created superuser instance.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        """
        Creates a regular user with the provided parameters.

        Args:
            email (str): The email address of the user.
            username (str): The username of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            password (str): The password of the user.
            **other_fields (dict): Additional fields for the user.

        Raises:
            ValueError: If the email address is not provided.

        Returns:
            CustomUser: The created user instance.
        """
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that extends the AbstractBaseUser and PermissionsMixin.
    """

    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        """
        Returns the string representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username


class UserProfile(models.Model):
    """
    A model representing additional profile information for each user.
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='accounts/avatars/', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    location = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)

    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    def __str__(self):
        """
        Returns the string representation of the user profile.

        Returns:
            str: The username of the associated user.
        """
        return self.user.username
