from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Lecturer, Lecture

from accounts.serializers import UserProfileSerializer

from base.shared_across_apps.serializers import GenericRelatedField
from base.shared_across_apps.mixins import ObjectLookupMixin

from institutions.models import Institution, Department, Unit

from notes.models import Document

from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()

class LectureSerializer(ObjectLookupMixin, serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

    lecturer = serializers.ReadOnlyField(source='lecturer.user.username')
    unit = serializers.StringRelatedField(source='unit.name', read_only=True)
    course = serializers.StringRelatedField(source='unit.course.name', read_only=True)
    department = serializers.StringRelatedField(source='unit.course.department.name', read_only=True)
    school = serializers.StringRelatedField(source='unit.course.department.school.name', read_only=True)
    institution = serializers.StringRelatedField(source='unit.course.department.school.institution.name', read_only=True)
    documents = GenericRelatedField(queryset=Document.objects.all(), field="title", many=True)

    def get_document_urls(self, instance):
        document_urls = []
        for document in instance.documents.all():
            document_download_url_by_id = reverse('download-document-by-id', args=[document.pk])
            document_download_url_by_title = reverse('download-document-by-title', args=[document.title])
            document_urls.append({
                'title': document.title,
                'download_url_by_id': self.context['request'].build_absolute_uri(document_download_url_by_id),
                'download_url_by_title': self.context['request'].build_absolute_uri(document_download_url_by_title),
            })
        return document_urls

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['document_urls'] = self.get_document_urls(instance)
        return data
    
    def create(self, validated_data):
        lecturer = validated_data['lecturer']
        request = self.context.get('request')
        provided_department = request.query_params.get('department', None)
        provided_unit = request.query_params.get('unit', None)

        if not provided_unit:
            raise serializers.ValidationError("Provide 'unit' in the query parameters.")

        lecturer_departments = lecturer.departments.all()
        if provided_department not in lecturer_departments.values_list('name', flat=True):
            raise ValidationError(f"You are not a lecturer in the department '{provided_department}'")
        
        department = lecturer_departments.get(name=provided_department)
        # Use the department to look up the unit
        unit = self.lookup_object(
            request=request,
            queryset=Unit.objects.all(),
            name_param='unit',
            filters={'course__department': department}
        )[0]

        # Add the unit to the validated data before creating the Lecture instance
        validated_data['unit'] = unit
        try:
            # Try to create the Lecture instance
            lecture = super().create(validated_data)
        except IntegrityError as e:
            # Handle the case where the lecture already exists
            existing_lecture = Lecture.objects.get(
                lecturer=lecturer,
                unit=unit,
                name=validated_data['name'],
                date=validated_data['date']
            )
            # If needed, you can update the existing lecture here
            # existing_lecture.description = validated_data['description']
            # existing_lecture.save()

            # Return a meaningful error message or take other appropriate action
            raise serializers.ValidationError("Lecture already exists.")

        return lecture

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

    lectures = LectureSerializer(many=True, read_only=True)

    # initially set the queryset to None. the queryset will be updated dynamically based on the institution
    departments = GenericRelatedField(queryset=Department.objects.none(), field="name", many=True)
    remove_departments = GenericRelatedField(queryset=Department.objects.none(), field="name", many=True, required=False)
    
    def get_departments_queryset(self):
        # check if there is a request
        request = self.context.get('request', None)
        if not request: # can happen when the lecturer serializer is used within other serializers eg institutions/serializers.py/DepartmentSerializer
            return Department.objects.none()
        # if there is a request
        # Check if institution is present in the query parameters
        institution_name = request.data.get('institution', None)
        if institution_name:
            q = Department.objects.filter(school__institution__name__iexact=institution_name)
            return q
        else: # get request
            return Department.objects.none()

    def get_fields(self):
        fields = super().get_fields()
        q = self.get_departments_queryset() 
        fields['departments'] = GenericRelatedField(queryset=q, field="name", many=True)
        fields['remove_departments'] = GenericRelatedField(queryset=q, field="name", many=True, required=False)
        return fields
    
    def update(self, instance, validated_data):
        # Handle removal of departments
        remove_departments = set(validated_data.pop('remove_departments', []))
        instance.departments.remove(*remove_departments)

        # Handle addition of departments
        new_departments = set(validated_data.pop('departments', []))
        instance.departments.add(*new_departments)

        instance.save()

        return instance
