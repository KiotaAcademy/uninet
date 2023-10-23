from rest_framework import serializers
from .models import Lecturer
from accounts.serializers import UserProfileSerializer  


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = '__all__'

    user_name = serializers.ReadOnlyField(source='user.username')
    user_profile = UserProfileSerializer(source='user.profile', read_only=True)
    department_names = serializers.StringRelatedField(many=True, source='departments')