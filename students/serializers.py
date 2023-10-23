from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    user_name = serializers.ReadOnlyField(source='user.username')
    course_name = serializers.ReadOnlyField(source='course.name')
    department_name = serializers.ReadOnlyField(source='course.department.name')
    school_name = serializers.ReadOnlyField(source='course.department.school.name')
    institution_name = serializers.ReadOnlyField(source='course.department.school.institution.name')