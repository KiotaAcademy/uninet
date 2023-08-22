from rest_framework import viewsets, status, authentication, permissions, serializers, mixins, response
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.urls import reverse
from django.conf import settings


from .models import Category, Document, Topic, Lecture
from .serializers import CategorySerializer, DocumentSerializer, TopicSerializer, LectureSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Custom action to handle bulk creation of categories
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True) # many=True: This parameter specifies that the data you're passing is a list of items
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return Response(serializer.data)

    # Custom method to perform the bulk creation
    def perform_bulk_create(self, serializer):
        serializer.save()
    
    # Custom action to delete a category by name
    @action(detail=False, methods=['delete'])
    def delete_by_name(self, request, name):
        try:
            category = Category.objects.get(Q(name__iexact=name)) #case-insensitive lookup for the category name.
            category_name = category.name  # Store the category name before deleting
            category.delete()
            return Response({'message': f"Category '{category_name}' has been successfully deleted."}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'message': f"Category '{name}' not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        category_names = request.data.get('category_names', [])
        deleted_categories = []

        for name in category_names:
            try:
                category = Category.objects.get(Q(name__iexact=name))
                category.delete()
                deleted_categories.append(name)
            except Category.DoesNotExist:
                pass

        return Response({'message': f'Categories {", ".join(deleted_categories)} have been successfully deleted'}, status=status.HTTP_200_OK)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing documents.

    Provides CRUD operations for documents along with additional actions like downloading and retrieving URLs.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        """
        Create a new document instance.

        This method handles the creation of a new document instance. 
        It calls the perform_create method for custom creation logic.
        ir handles validation errors resulting during document upload
        This validation error is raised by the presave signal which sets default title based on the filename if no title is provided.

        Args:
            request: The HTTP request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response containing the created document details or error details.

        Raises:
            ValidationError: If a validation error occurs during document creation.
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            if 'existing_document_title' in e.detail:
                existing_document_title = e.detail['existing_document_title']
                existing_document = Document.objects.get(title=existing_document_title)
                document_download_url_by_id = reverse('download-document-by-id', args=[existing_document.pk])
                document_download_url_by_title = reverse('download-document-by-title', args=[existing_document.title])
                response_data = {
                    'title_error': str(e.detail['title']),
                    'existing_document_download_url_by_id': request.build_absolute_uri(document_download_url_by_id),
                    'existing_document_download_url_by_title': request.build_absolute_uri(document_download_url_by_title),
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise e
            
    def perform_create(self, serializer):
        """
        Perform the creation of a document instance.

        This method is responsible for creating a new document instance, associating categories, and setting the
        uploaded user.

        Args:
            serializer: The serializer for document creation.

        Returns:
            None
        """
        category_names = self.request.data.get('categories', '').split(',')
        category_names = [name.strip() for name in category_names if name.strip()]
        categories = []
        for name in category_names:
            name_lower = name.lower()
            category, created = Category.objects.get_or_create(name__iexact=name_lower)
            if created:
                category.name = name
                category.save()
            categories.append(category)
                
        serializer.save(uploaded_by=self.request.user, categories=categories)
      

    @action(detail=True, methods=['get'])
    def download_document_by_id(self, request, pk=None):
        """
        Download a document by its ID.

        Args:
            request: The HTTP request.
            pk: The primary key of the document.

        Returns:
            FileResponse: The file response for downloading the document.
        """
        document = get_object_or_404(Document, pk=pk)
        response = FileResponse(document.document.open('rb'), as_attachment=True)
        return response
    
    @action(detail=False, methods=['get'])
    def download_document_by_title(self, request, title=None):
        """
        Download a document by its title.

        Args:
            request: The HTTP request.
            title: The title of the document.

        Returns:
            FileResponse: The file response for downloading the document.
        """
        document = get_object_or_404(Document, title=title)
        response = FileResponse(document.document.open('rb'), as_attachment=True)
        return response
    
    @action(detail=False, methods=['get'])
    def document_urls(self, request):
        """
        Retrieve URLs for documents.

        This method retrieves URLs for documents based on the provided IDs and titles in query parameters.

        Args:
            request: The HTTP request.

        Returns:
            Response: The response containing document URLs.
        """
        queryset = Document.objects.all()

        ids = self.request.query_params.get('ids')
        titles = self.request.query_params.get('titles')

        if ids:
            ids_list = ids.split(',')
            queryset = queryset.filter(pk__in=ids_list)
        if titles:
            titles_list = titles.split(',')
            title_queries = Q()
            for title in titles_list:
                title_queries |= Q(title__iexact=title.strip())
            queryset = queryset.filter(title_queries)

        document_urls = []
        for document in queryset:
            document_url = reverse('document-detail', args=[document.pk])
            document_download_url_by_id = reverse('download-document-by-id', args=[document.pk])
            document_download_url_by_title = reverse('download-document-by-title', args=[document.title])

            document_urls.append({
                'title': document.title,
                'url': document_url,
                'download_url_by_id': request.build_absolute_uri(document_download_url_by_id),
                'download_url_by_title': request.build_absolute_uri(document_download_url_by_title),
            })

        return Response(document_urls)

    
    

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer



class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
