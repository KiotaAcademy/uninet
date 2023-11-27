from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Institution, School, Department, Course, Unit
from lecturers.serializers import LecturerSerializer
from clubs_societies.serializers import ClubSocietySerializer
from clubs_societies.models import ClubSociety

from base.shared_across_apps.serializers import GenericRelatedField
from base.shared_across_apps.mixins import AdminsSerializerMixin

from django.db.models import Prefetch
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

class DepartmentSerializer(AdminsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    courses = CourseSerializer(many=True, read_only=True)
    lecturers = LecturerSerializer(many=True, read_only=True)
    head = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    secretary = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)
    school = serializers.StringRelatedField(source='school.name', read_only=True)

    # Use the following line only if you intend to provide the school in the request.
    # The 'school' field is automatically filled based on the institution the user is an admin of.
    # school = GenericRelatedField(queryset=School.objects.all(), field="name", required=False)

    def create(self, validated_data):
        default_admins = ['head', 'secretary', 'created_by']
        # Determine the school based on the user's admin role
        user = self.context['request'].user
        schools = School.objects.filter(admins=user)

        if schools.exists():
            school = schools.first()
            validated_data['school'] = school
            instance = super().create(validated_data)
            return self.add_admins_to_instance(instance, validated_data, default_admins)

        # If the user is not a school level admin, raise a validation error
        raise ValidationError("You are not a school level admin in any school. Only school level admins can create departments within a school.")

    def update(self, instance, validated_data):
        default_admin_fields = ['head', 'secretary'] # exclude created_by as its admin status should not be updated 
        instance = self.update_admins_for_instance(instance, validated_data, default_admin_fields)

        # Update the instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class SchoolSerializer(AdminsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

    departments = DepartmentSerializer(many=True, read_only=True)
    institution = serializers.StringRelatedField(source='institution.name', read_only=True)

    # Use the following line only if you intend to provide the institution in the request.
    # The 'institution' field is automatically filled based on the institution the user is an admin of.
    # institution = GenericRelatedField(queryset=Institution.objects.all(), field="name", required=False)
    
    head = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    secretary = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)

    def create(self, validated_data):
        default_admins = ['head', 'secretary', 'created_by']

        # Determine the institution based on the user's admin role
        user = self.context['request'].user
        institutions = Institution.objects.filter(admins=user)
        
        if institutions.exists():
            institution = institutions.first()
            validated_data['institution'] = institution
            instance = super().create(validated_data)
            return self.add_admins_to_instance(instance, validated_data, default_admins)
        
        # If the user is not an admin in any institution, raise a validation error
        raise ValidationError("You are not an institution level admin in any institution. Only institution level admins can create schools within an institution.")

    def update(self, instance, validated_data):
        default_admin_fields = ['head', 'secretary'] # exclude created_by as its admin status should not be updated 
        instance = self.update_admins_for_instance(instance, validated_data, default_admin_fields)

        # Update the instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class InstitutionSerializer(AdminsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
        
    chancellor = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    vice_chancellor = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)
    remove_admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)

    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)

    def create(self, validated_data):
        default_admins = ['chancellor', 'vice_chancellor', 'created_by']
        instance = super().create(validated_data)
        return self.add_admins_to_instance(instance, validated_data, default_admins)
    
    def update(self, instance, validated_data):
        default_admin_fields = ['chancellor', 'vice_chancellor']
        instance = self.update_admins_for_instance(instance, validated_data, default_admin_fields)

        # Update the instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Use prefetch_related to efficiently retrieve related clubs and societies along with their members and admins
        clubs_societies = ClubSociety.objects.filter(institution=instance)
        clubs_societies = clubs_societies.prefetch_related('members', 'admins')
        club_society_serializer = ClubSocietySerializer(clubs_societies, many=True)
        representation['clubs_societies'] = club_society_serializer.data

        return representation


