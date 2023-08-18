from rest_framework import serializers
from .models import Category, Document, Topic, Lecture

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    document = serializers.FileField(required=True)
    categories = CategorySerializer(many=True, read_only=True)  # Use CategorySerializer for ManyToMany field
    
    class Meta:
        model = Document
        fields = '__all__'
    

class TopicSerializer(serializers.ModelSerializer):
    notes = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Topic
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    students = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Lecture
        fields = '__all__'
