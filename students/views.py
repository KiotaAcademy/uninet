from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.urls import reverse
from django.http import Http404

from .models import Student
from .serializers import StudentSerializer

from notes.models import Document 
from notes.serializers import DocumentSerializer, CategorySerializer

from base.shared_across_apps.mixins import ObjectLookupMixin

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if a lecturer with the same user already exists
        user = self.request.user
        existing_student = Student.objects.filter(user=user).first()

        if existing_student:
            # If an existing lecturer is found, return it
            serializer.instance = existing_student
            return

        # Create a new student if one doesn't already exist
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def retrieve_student(self, request):
        username = request.query_params.get('username', None)
        if username:
            student = Student.objects.filter(user__username=username).first()

            if student:
                serializer = self.get_serializer(student)
                return Response(serializer.data)
            else:
                return Response({"detail": f"No student status found for the user '{username}'."}, status=404)
        else:
            return Response({"detail": "Username parameter is required."}, status=400)

    @action(detail=False, methods=['PUT'])
    def update_student(self, request):
        # Ensure that the user can only update their own student instance
        student = Student.objects.filter(user=request.user).first()
        if not student:
            raise Http404("Student not found.")
        
        request.data['institution'] = student.institution.name
        serializer = self.get_serializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=False, methods=['DELETE'])
    def delete_student(self, request):
        # Ensure that the user can only delete their own student instance
        student = Student.objects.filter(user=request.user).first()
        if not student:
            raise Http404("Student not found.")
        
        student.delete()
        return Response({"detail": "Student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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
    

    @action(detail=True, methods=['GET'])
    def attended_lectures(self, request, pk=None):
        pass
