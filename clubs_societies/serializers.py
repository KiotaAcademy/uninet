from rest_framework import serializers
from .models import ClubSociety
from accounts.serializers import UserProfileSerializer

class ClubSocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubSociety
        fields = '__all__'

    members_names = serializers.StringRelatedField(many=True, source='members', read_only=True)
    user_profile = UserProfileSerializer(source='members.profile', read_only=True)
