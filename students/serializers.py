from rest_framework import serializers
from .models import Student
from accounts.serializers import UserProfileSerializer  

from base.shared_across_apps.serializers import GenericRelatedField
from base.shared_across_apps.mixins import ObjectLookupMixin

from institutions.models import Institution, Department, Course, Unit

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    user = serializers.ReadOnlyField(source='user.username')
    profile = UserProfileSerializer(source='user.profile', read_only=True)

    institution = GenericRelatedField(queryset=Institution.objects.all(), field="name")
    
    school= serializers.StringRelatedField(source='course.department.school.name', read_only=True)
    department = serializers.StringRelatedField(source='course.department.name', read_only=True)
    
    course = GenericRelatedField(queryset=Course.objects.none(), field="name")    
    
    def get_courses_queryset(self):
        # Check if there is a request
        request = self.context.get('request', None)
        if not request:  # Can happen when the serializer is used outside of a view
            return Course.objects.none()
        
        # If there is a request, check if the institution is present in the query parameters
        institution_name = request.data.get('institution', None)
        if institution_name:
            return Course.objects.filter(department__school__institution__name__iexact=institution_name)
        else:  # GET request or institution not provided
            return Course.objects.none()

    def get_fields(self):
        fields = super().get_fields()
        course_queryset = self.get_courses_queryset()
        fields['course'] = GenericRelatedField(queryset=course_queryset, field="name")
        return fields