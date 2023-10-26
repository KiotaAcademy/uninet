from rest_framework import serializers

class GenericRelatedField(serializers.RelatedField):
    """
    A serializer field designed for handling related models, allowing the use of either the primary key or a specified field's string representation in the request.
    
    This field can accommodate various related models and offers the flexibility to query based on either the primary key or the string representation of a specified field.

    Args:
        field (str): The name of the field to use for the query.
        queryset (QuerySet): A set of objects to query, typically obtained using the model's manager (e.g., queryset=ModelName.objects.all()).
        many (bool, optional): Indicates whether the field represents a collection of objects (default is False).

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