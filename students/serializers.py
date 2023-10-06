from rest_framework import serializers
from .models import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    # Add a SerializerMethodField to include the username
    #username = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = '__all__'

    username = serializers.ReadOnlyField(source='user.username')
