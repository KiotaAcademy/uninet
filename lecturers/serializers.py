from rest_framework import serializers
from .models import Lecturer

class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = '__all__'

    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username
