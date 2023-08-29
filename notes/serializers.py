from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.urls import reverse

from .models import Category, Document, Topic, Lecture

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
    categories = CategorySerializer(many=True, read_only=True)  # Use CategorySerializer for ManyToMany field
    
    class Meta:
        model = Document
        fields = '__all__'

    

class TopicSerializer(serializers.ModelSerializer):
    """
    Serializer class for Topic model.
    
    Serializes and deserializes Topic model instances.
    """
    document_title = serializers.CharField(write_only=True)
    document_download_url = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        exclude = ('document',)  # Exclude the document field from the serializer

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

    def create(self, validated_data):
        """
        Create a new topic.

        Args:
            validated_data: Validated data for the new topic.

        Returns:
            Topic: The created Topic instance.

        Raises:
            ValidationError: If the associated document does not exist or a topic with the same name already exists.
        """
        # Extract the document title from the validated data
        document_title = validated_data.pop('document_title')
        
        try:
            document = Document.objects.get(title__iexact=document_title)
        except Document.DoesNotExist:
            raise ValidationError({'document_title': 'Document with the provided title does not exist.'})
        
        # Check if a topic with the same name already exists for the same document
        existing_topic = Topic.objects.filter(name=validated_data['name'], document=document).first()
        if existing_topic:
            raise ValidationError({'name': 'A topic with the same name already exists for the provided document.'})
        
        # Create the topic with the retrieved Document instance
        topic = Topic.objects.create(document=document, **validated_data)
        return topic

    
    

class LectureSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    students = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Lecture
        fields = '__all__'
