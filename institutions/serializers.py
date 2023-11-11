from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db.models import Model

from typing import List

from .models import Institution, School, Department, Course, Unit
from lecturers.serializers import LecturerSerializer
from base.general import GenericRelatedField

from django.contrib.auth import get_user_model
User = get_user_model()

# Define a function to add admins to an instance
def add_admins_to_instance(instance, validated_data, default_admins):
    """
    Add default admin fields to provided admin fields for the given instance.

    Args:
        instance: The instance to which admins are added.
        validated_data: The validated data dictionary from the serializer.
        default_admins: List of default admin fields to add to the instance.

    Returns:
        The instance with combined admin fields.

    Example:
    To add default admin fields 'admin1' and 'admin2' to provided admins,
    call: add_admins_to_instance(instance, validated_data, ['admin1', 'admin2'])
    """
    provided_admins = validated_data.pop('admins', [])
    instance = instance.create(validated_data)
    instance.add_admins(*default_admins)
    instance.admins.add(*provided_admins)
    return instance

def merge_admins(existing_admins, new_admins):
    """
    Merge existing and new admin users while ensuring no duplicates.
    """
    return list(set(existing_admins) | set(new_admins))

def update_admins_for_instance(instance: Model, validated_data: dict, default_admin_fields: List[str]):
    """
    Update admin users for the given instance based on the provided validated data.

    Args:
        instance: The instance for which admins are updated.
        validated_data: The validated data dictionary from the serializer.
        admin_fields: List of admin fields to update.

    Returns:
        The updated instance.

    Example:
    To update admins for fields 'chancellor', 'vice_chancellor', 'created_by',
    call: update_admins_for_instance(instance, validated_data, ['chancellor', 'vice_chancellor', 'created_by'])
    """
    # Get the default admins from the instance
    old_default_admins = {getattr(instance, field) for field in default_admin_fields}

    # Get the users in the 'remove_admins' list excluding the old default admins
    remove_admins = set(validated_data.pop('remove_admins', [])) - old_default_admins

    # Handle 'admins' removal
    instance.admins.remove(*remove_admins)

    # Handle updating 'admins' separately to avoid overwriting existing admins
    new_admins = validated_data.pop('admins', [])
    # Merge existing admins and new admins while ensuring no duplicates
    merged_admins = merge_admins(instance.admins.all(), new_admins)
    instance.admins.set(merged_admins)

    # Check if the default admin users are changed and update 'admins' accordingly
    for field in default_admin_fields:
        new_user = validated_data.get(field, getattr(instance, field))
        if new_user != getattr(instance, field):
            instance.admins.remove(getattr(instance, field))
            instance.admins.add(new_user)

    return instance



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
    head = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    secretary = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)
    school = GenericRelatedField(queryset=School.objects.all(), field="name", required=False)

    def create(self, validated_data):
        default_admins = ['head', 'secretary', 'created_by']
        # Determine the school based on the user's admin role
        user = self.context['request'].user
        schools = School.objects.filter(admins=user)

        if schools.exists():
            school = schools.first()
            validated_data['school'] = school
            return add_admins_to_instance(super(), validated_data, default_admins)

        # If the user is not a school level admin, raise a validation error
        raise ValidationError("You are not a school level admin in any school. Only school level admins can create departments within a school.")


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
    
    departments = DepartmentSerializer(many=True, read_only=True)
    institution = GenericRelatedField(queryset=Institution.objects.all(), field="name", required=False)
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
            return add_admins_to_instance(super(), validated_data, default_admins)
        
        # If the user is not an admin in any institution, raise a validation error
        raise ValidationError("You are not an institution level admin in any institution. Only institution level admins can create schools within an institution.")



class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
    
    # schools = SchoolSerializer(many=True, read_only=True)  # Include related schools
    chancellor = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    vice_chancellor = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)
    remove_admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)

    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)

    def create(self, validated_data):
        default_admins = ['chancellor', 'vice_chancellor', 'created_by']
        return add_admins_to_instance(super(), validated_data, default_admins)
    
    def update(self, instance, validated_data):
        default_admin_fields = ['chancellor', 'vice_chancellor', 'created_by']
        instance = update_admins_for_instance(instance, validated_data, default_admin_fields)

        # Update the instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


