from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Institution, School, Department, Course, Unit
from lecturers.serializers import LecturerSerializer
from clubs_societies.serializers import ClubSocietySerializer
from clubs_societies.models import ClubSociety

from base.shared_across_apps.serializers import GenericRelatedField
from base.shared_across_apps.mixins import AdminsSerializerMixin
from base.shared_across_apps.mixins import ObjectLookupMixin

from django.db.models import Prefetch
from django.contrib.auth import get_user_model
User = get_user_model()

class UnitSerializer(ObjectLookupMixin, serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
    
    course = serializers.StringRelatedField(source='course.name', read_only=True)
    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)
    department = serializers.StringRelatedField(source='course.department.name', read_only=True)
    school = serializers.StringRelatedField(source='course.department.school.name', read_only=True)
    institution = serializers.StringRelatedField(source='course.department.school.institution.name', read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        provided_course = request.query_params.get('course', None)
        provided_department = request.query_params.get('department', None)
        provided_school = request.query_params.get('school', None)
        provided_institution = request.query_params.get('institution', None)
        
        if not (provided_course and provided_department and provided_school and provided_institution):
            raise ValidationError("Provide 'course', 'department', 'school', 'institution' in the query parameters.")
            
        course = self.lookup_object(request=self.context['request'],
                                    queryset=Course.objects.all(),
                                    name_param='course',
                                    filters={'department__school__institution__name': provided_institution,
                                             'department__school__name': provided_school,
                                             'department__name': provided_department})[0]
        
        authorized = self.check_authorization(course.department, user)
        if not authorized:
            raise ValidationError(f"You are not an admin in Department of '{course.department.name}'. Only department admins can create units.")

        validated_data['course'] = course
        instance = super().create(validated_data)
        return instance


class CourseSerializer(ObjectLookupMixin, serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)
    department = serializers.StringRelatedField(source='department.name', read_only=True)
    school = serializers.StringRelatedField(source='department.school.name', read_only=True)
    institution = serializers.StringRelatedField(source='department.school.institution.name', read_only=True)

    def create(self, validated_data):
        # logic to check if the user is a department level admin
        user = self.context['request'].user
        provided_department = self.context['request'].query_params.get('department', None)
        provided_school = self.context['request'].query_params.get('school', None)
        provided_institution = self.context['request'].query_params.get('institution', None)

        if provided_department:
            if not (provided_school and provided_institution):
                raise ValidationError("Provide 'school', 'institution', and 'department' in the query parameters.")
            department = self.lookup_object(request=self.context['request'],
                                           queryset=Department.objects.all(),
                                           name_param='department',
                                           filters={'school__institution__name': provided_institution,
                                                    'school__name': provided_school})[0]
            authorized = self.check_authorization(department, user)
            if authorized:
                validated_data['department'] = department
            else:
                raise ValidationError(f"You are not an admin in Department of '{department.name}'. Only department admins can create courses.")
        
        else:
            departments = Department.objects.filter(admins=user)

            if departments.exists():
                department = departments.first()
                validated_data['department'] = department
            else:
                # If the user is not a department level admin, raise a validation error
                raise ValidationError("You are not a department level admin in any department. Only department level admins can create courses within a department.")

        instance = super().create(validated_data)
        return instance
    

class DepartmentSerializer(ObjectLookupMixin, AdminsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    courses = CourseSerializer(many=True, read_only=True)
    head = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    secretary = GenericRelatedField(queryset=User.objects.all(), field="username", required=False)
    created_by = serializers.StringRelatedField(source='created_by.username', read_only=True)
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)
    school = serializers.StringRelatedField(source='school.name', read_only=True)
    institution = serializers.StringRelatedField(source='school.institution.name', read_only=True)

    # Use the following line only if you intend to provide the school in the request data.
    # The 'school' field is automatically filled based on the institution the user is an admin of.
    # school = GenericRelatedField(queryset=School.objects.all(), field="name", required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        default_admins = ['head', 'secretary', 'created_by']
        # Determine the school based on the user's admin role
        provided_school = self.context['request'].query_params.get('school', None)
        provided_institution = self.context['request'].query_params.get('institution', None)
        if provided_school:
            if not provided_institution:
                raise ValidationError(f"Provide both 'institution' and 'school' in the query parameters.")
            school = self.lookup_object(request=self.context['request'], 
                                        queryset=School.objects.all(),
                                        name_param='school',
                                        filters={'institution__name': provided_institution})[0]
            authorized = self.check_authorization(school, user)
            if authorized:
                validated_data['school'] = school
            else:
                raise ValidationError(f"You are not an admin in School of '{school.name}'. Only school admins can create departments.")
        
        else:
            schools = School.objects.filter(admins=user)

            if schools.exists():
                school = schools.first()
                validated_data['school'] = school
            else:
                # If the user is not a school level admin, raise a validation error
                raise ValidationError("You are not a school level admin in any school. Only school level admins can create departments within a school.")
            
        instance = super().create(validated_data)
        return self.add_admins_to_instance(instance, validated_data, default_admins)

        
    def update(self, instance, validated_data):
        default_admin_fields = ['head', 'secretary'] # exclude created_by as its admin status should not be updated 
        instance = self.update_admins_for_instance(instance, validated_data, default_admin_fields)

        # Update the instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Include the serialized representation of lecturers
        lecturers = LecturerSerializer(instance.lecturers.all(), many=True).data
        representation['lecturers'] = lecturers

        return representation
    

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


