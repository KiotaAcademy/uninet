from typing import List

from rest_framework.response import Response
from rest_framework import status

from django.db import models
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminsModelMixin(models.Model):
    """
    A mixin to manage administrators for a model instance.

    This mixin includes an 'admins' field that is a ManyToMany relationship with User,
    allowing the association of multiple administrators to a model instance.

    Methods:
        - add_admins: Add one or more administrators to the 'admins' field.

    Meta:
        abstract (bool): Indicates that this is an abstract model and should not be instantiated.
    """
    
    admins = models.ManyToManyField(User, related_name="admin_%(class)ss", blank=True)

    def add_admins_from_specified_fields(self, *user_fields):
        """
        Add users from specified fields to the 'admins' field.

        Args:
            *user_fields: Variable number of fields containing User instances to be added as admins.
            
        Usage:
            instance.add_admins('field1','chancellor', 'field3', ...)
            instance.add_admins(*default_admins)
                
                default_admins (List[str]): List of default admin fields to add to the instance.
                default_admins = ['head', 'secretary', 'created_by']

        This method iterates through the specified fields, retrieves the User instance from each field,
        and adds it to the 'admins' field if it is not already present.
        """
        for field in user_fields:
            user = getattr(self, field, None)
            if user and user not in self.admins.all():
                self.admins.add(user)

    class Meta:
        abstract = True

class AdminsSerializerMixin:
    """
    A mixin with utility methods for handling admins in serializers.
    """

    @staticmethod
    def add_admins_to_instance(instance: Model, validated_data: dict, default_admins: List[str]) -> Model:
        """
        Add default and provided admin users to the created instance.
        Used in the create method of the serializer.

        Args:
            instance (Model): The instance to which admins are added.
            validated_data (dict): The validated data dictionary from the serializer.
            default_admins (List[str]): List of default admin fields to add to the instance.

        Returns:
            Model: The instance with combined admin fields.
        """
        provided_admins = validated_data.pop('admins', [])
        instance.add_admins_from_specified_fields(*default_admins)
        instance.admins.add(*provided_admins)
        return instance

    @staticmethod
    def merge_admins(existing_admins: List, new_admins: List) -> List:
        """
        Merge existing and new admin users while ensuring no duplicates.

        Args:
            existing_admins (List): List of existing admin users.
            new_admins (List): List of new admin users.

        Returns:
            List: Merged list of admin users.
        """
        return list(set(existing_admins) | set(new_admins))

    @staticmethod
    def update_admins_for_instance(instance: Model, validated_data: dict, default_admin_fields: List[str]) -> Model:
        """
        Update admin users for the given instance based on the provided validated data.
        Used in the update method of the serializer.

        Args:
            instance (Model): The instance for which admins are updated.
            validated_data (dict): The validated data dictionary from the serializer.
            default_admin_fields (List[str]): List of default admin fields for the associated model.

        Returns:
            Model: The updated instance.
        """
        old_default_admins = {getattr(instance, field) for field in default_admin_fields}
        remove_admins = set(validated_data.pop('remove_admins', [])) - old_default_admins
        
        instance.admins.remove(*remove_admins)
        
        new_admins = validated_data.pop('admins', [])
        merged_admins = AdminsSerializerMixin.merge_admins(instance.admins.all(), new_admins)
        instance.admins.set(merged_admins)
        
        # check if any default admins have changed users and update the admins list for the instance accordingly
        for field in default_admin_fields:
            new_user = validated_data.get(field, getattr(instance, field))
            if new_user != getattr(instance, field):
                instance.admins.remove(getattr(instance, field))
                instance.admins.add(new_user)
        return instance


class ObjectViewMixin:
    """
    A mixin for viewsets to provide object lookup and authorization checks.
    """
    def lookup_object(self, request, queryset, id_param='id', name_param='name'):
        """
        Retrieve an object by either its primary key or name using the given queryset.
        Use the 'id' parameter for the PK or 'name' for the name.
        """
        id_param_value = request.query_params.get(id_param)
        name_param_value = request.query_params.get(name_param)

        if id_param_value:
            obj = get_object_or_404(queryset, pk=id_param_value)
        elif name_param_value:
            obj = get_object_or_404(queryset, name=name_param_value)
        else:
            return Response({'error': f'You must provide either the {id_param} or {name_param} parameter for the lookup.'}, status=status.HTTP_400_BAD_REQUEST)

        return obj

    def check_authorization(self, obj, user, authorized_users_field='admins'):
        """
        Check if the user is authorized to perform actions on the object.
        The user must be an object-level admin to perform these actions.
        """
        if user not in getattr(obj, authorized_users_field).all():
            return False  # Return False when the user is not authorized

        return True  # Return True when the user is authorized
