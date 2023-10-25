from rest_framework import serializers
from .models import ClubSociety
from accounts.serializers import UserProfileSerializer
from institutions.models import Institution
from django.contrib.auth import get_user_model

User = get_user_model()

class GenericRelatedField(serializers.RelatedField):
    """
    A generic serializer field for handling related models, either by primary key or a specified field.
    This field can handle various related models and allows querying by primary key or a specific field.

    Parameters:
        - `field`: The name of the field to use for the query.
    """

    def __init__(self, field, **kwargs):
        """
        Initialize the GenericRelatedField.

        Args:
            field (str): The name of the field to use for the query.
        """
        self.field = field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        """
        Convert the external representation (e.g., primary key or field value) to an internal value (the object itself).

        Args:
            data: The external representation to convert.

        Returns:
            object: The internal representation of the related object.
        """
        # Check if the data is an integer (expected primary key)
        if isinstance(data, int):
            return self.queryset.get(pk=data)

        # Treat it as the field and retrieve the object
        filter_kwargs = {f'{self.field}__iexact': data}
        try:
            return self.queryset.get(**filter_kwargs)
        except self.queryset.model.DoesNotExist:
            raise serializers.ValidationError(f"{self.queryset.model.__name__} does not exist")

    def to_representation(self, obj):
        """
        Convert the object to its external representation (e.g., the field value).

        Args:
            obj: The internal representation of the related object.

        Returns:
            str: The external representation of the related object.
        """
        return getattr(obj, self.field)

class ClubSocietySerializer(serializers.ModelSerializer):
    """
    Serializer for the ClubSociety model.

    This serializer is designed to work with ClubSociety models. It uses the GenericRelatedField
    for handling related fields like 'institution', 'members', and 'created_by'.
    """

    institution = GenericRelatedField(queryset=Institution.objects.all(), field="name")
    members = GenericRelatedField(queryset=User.objects.all(), field="username", many=True)
    created_by = serializers.StringRelatedField(source='created_by.username')

    class Meta:
        model = ClubSociety
        fields = '__all__'
