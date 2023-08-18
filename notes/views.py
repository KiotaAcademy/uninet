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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        category_names = self.request.data.get('categories', '').split(',')  # Split comma-separated string
        # Remove empty strings and strip whitespace
        category_names = [name.strip() for name in category_names if name.strip()]
        # Create or retrieve Category instances based on the provided names
        categories = []
        for name in category_names:
            name_lower = name.lower()  # Convert to lowercase for case-insensitive comparison
            category, created = Category.objects.get_or_create(name__iexact=name_lower)
            if created:
                category.name = name  # Set the actual case-sensitive name
                category.save()
            categories.append(category)
            
        serializer.save(uploaded_by=self.request.user, categories=categories)

    
    @action(detail=True, methods=['get'])
    def download_document_by_id(self, request, pk=None):
        document = get_object_or_404(Document, pk=pk)
        response = FileResponse(document.document.open('rb'), as_attachment=True)
        return response
    
    @action(detail=False, methods=['get'])
    def download_document_by_title(self, request, title=None):
        document = get_object_or_404(Document, title=title)
        response = FileResponse(document.document.open('rb'), as_attachment=True)
        return response
    
    @action(detail=False, methods=['get'])
    def document_urls(self, request):
        queryset = Document.objects.all()

        ids = self.request.query_params.get('ids')  # Get comma-separated IDs from query parameters
        titles = self.request.query_params.get('titles')  # Get comma-separated titles from query parameters

        if ids:
            ids_list = ids.split(',')
            queryset = queryset.filter(pk__in=ids_list)
        if titles:
            titles_list = titles.split(',')
            title_queries = Q()  # Initialize an empty query
            for title in titles_list:
                title_queries |= Q(title__iexact=title.strip())  # Case-insensitive match
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
