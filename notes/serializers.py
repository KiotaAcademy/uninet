from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Category, Document, Topic, Lecture

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class for Category model.
    
    Serializes and deserializes Category model instances.
    """
    class Meta:
        model = Category
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer class for Document model.
    
    Serializes and deserializes Document model instances.
    """
    document = serializers.FileField(required=True)
    categories = CategorySerializer(many=True, read_only=True, required=False)  # Use CategorySerializer for ManyToMany field
    
    class Meta:
        model = Document
        fields = '__all__'

    

class TopicSerializer(serializers.ModelSerializer):
    """
    Serializer class for Topic model.
    
    Serializes and deserializes Topic model instances.
    """
    uploaded_document = serializers.FileField(write_only=True, required=False)  # Accept document in the request
    document_title = serializers.CharField(write_only=True, required=False)
    document_download_url = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        # exclude = ('document',)  # Exclude the document field from the serializer
        fields = '__all__'

    def get_document_download_url(self, instance):
        """
        Get the download URL for the associated document.

        Args:
            instance: The Topic instance.

        Returns:
            str: The absolute URL for downloading the associated document.
        """
        # Assuming you have a URL pattern named 'download-document-by-id'
        document_download_url = reverse('download-document-by-id', args=[instance.document.pk])
        return self.context['request'].build_absolute_uri(document_download_url)

    
