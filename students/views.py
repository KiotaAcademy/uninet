from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.urls import reverse

from .models import StudentProfile
from .serializers import StudentProfileSerializer

from notes.models import Document, Lecture 
from notes.serializers import DocumentSerializer, CategorySerializer, LectureSerializer

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    @action(detail=True, methods=['GET'])
    def student_documents(self, request, pk=None):
        student_profile = self.get_object()
        student_documents = Document.objects.filter(uploaded_by=student_profile.user)

        # Create a list of download links for the student's documents
        download_links = []
        for document in student_documents:
            category_data = CategorySerializer(document.categories.all(), many=True).data
            download_links.append({
                'document_title': document.title,
                'document_download_url': request.build_absolute_uri(
                    reverse('download-document-by-id', args=[document.pk])
                ),
                'document_author': document.author,
                'document_categories': category_data,
                'document_created_at': document.created_at,

            })

        return Response(download_links)
    

    
