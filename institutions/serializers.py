from rest_framework import serializers

from .models import Institution, School, Department, Course, Unit
from lecturers.serializers import LecturerSerializer
from base.general import GenericRelatedField

from django.contrib.auth import get_user_model
User = get_user_model()

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    department_name = serializers.ReadOnlyField(source='department.name')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
    courses = CourseSerializer(many=True, read_only=True)
    lecturers = LecturerSerializer(many=True, read_only=True)

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
    
    departments = DepartmentSerializer(many=True, read_only=True)


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
    
    schools = SchoolSerializer(many=True, read_only=True)  # Include related schools
    chancellor = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    vice_chancellor = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)
    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)

    def create(self, validated_data):
        # Retrieve and merge provided admins with chancellor, vice-chancellor, and created_by
        provided_admins = validated_data.pop('admins', [])
        instance = super().create(validated_data)
        instance.add_admins('chancellor', 'vice_chancellor', 'created_by')
        instance.admins.add(*provided_admins)
        return instance


