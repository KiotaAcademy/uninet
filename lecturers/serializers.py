from rest_framework import serializers
from .models import Lecturer
from accounts.serializers import UserProfileSerializer
from base.shared_across_apps.serializers import GenericRelatedField
from institutions.models import Institution, Department

from django.contrib.auth import get_user_model
User = get_user_model()

class LecturerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lecturer model.

    This serializer is designed to handle the serialization and deserialization
    of Lecturer model instances. It dynamically sets the queryset for the 'departments'
    field based on the 'institution' provided in the request data.

    Attributes:
        user (serializers.ReadOnlyField): A read-only field to represent the username of the associated user.
        profile (UserProfileSerializer): A serialized representation of the associated user's profile.
        institution (GenericRelatedField): A field to represent the associated institution.
        departments (GenericRelatedField): A field to represent the associated departments, with the queryset set dynamically based on the 'institution' in the request data.

    Methods:
        get_departments_queryset: A method to dynamically set the queryset for 'departments' based on the 'institution' in the request data.
        get_fields: Override of the get_fields method to update the 'departments' field's queryset based on the result of get_departments_queryset.
    """

    class Meta:
        model = Lecturer
        fields = '__all__'

    user = serializers.ReadOnlyField(source='user.username')
    profile = UserProfileSerializer(source='user.profile', read_only=True)
    institution = GenericRelatedField(queryset=Institution.objects.all(), field="name")

    # initially set the queryset to None. the queryset will be updated dynamically based on the institution
    departments = GenericRelatedField(queryset=Department.objects.none(), field="name", many=True)
    
    def get_departments_queryset(self):
        request = self.context.get('request', None)
        if not request: # can happen when the lecturer serializer is used within other serializers eg institutions/serializers.py/DepartmentSerializer
            return Department.objects.none()

        institution_name = self.context['request'].data['institution']
        q = Department.objects.filter(school__institution__name__iexact=institution_name)
        return q

    def get_fields(self):
        fields = super().get_fields()
        q = self.get_departments_queryset() 
        fields['departments'] = GenericRelatedField(queryset=q, field="name", many=True)
        return fields
