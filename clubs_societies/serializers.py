from rest_framework import serializers
from .models import ClubSociety
from accounts.serializers import UserProfileSerializer
from institutions.models import Institution
from django.contrib.auth import get_user_model
from base.shared_across_apps.serializers import GenericRelatedField

User = get_user_model()

class ClubSocietySerializer(serializers.ModelSerializer):
    """
    Serializer for the ClubSociety model.

    This serializer is designed to work with ClubSociety models. It uses the GenericRelatedField
    for handling related fields like 'institution', 'members', and 'created_by'.
    """

    institution = GenericRelatedField(queryset=Institution.objects.all(), field="name")
    members = GenericRelatedField(queryset=User.objects.all(), field="username", many=True)
    created_by = serializers.StringRelatedField(source='created_by.username')

    class Meta:
        model = ClubSociety
        fields = '__all__'
