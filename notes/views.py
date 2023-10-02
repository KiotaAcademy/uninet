import requests


from rest_framework import viewsets, status, authentication, permissions, serializers, mixins, response
from rest_framework.response import Response
from rest_framework.decorators import action, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q, QuerySet
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
        It calls the perform_create method for custom creation logic.

        It handles validation errors resulting during document upload
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

        This method is called by the create method. 

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

    def delete(self, request, *args, **kwargs):
        """
        Delete a document instance.

        This method handles the deletion of a document instance. It checks whether the user making the request is the same
        user who uploaded the document. If not, it returns a response with a forbidden error. Otherwise, it calls the
        perform_delete method for custom deletion logic.

        Args:
            request: The HTTP request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response indicating success or error.
        """
        instance = self.get_object()
        if instance.uploaded_by == request.user:
            return self.perform_delete(instance)
        else:
            return Response(
                {"error": "You do not have permission to delete this document."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def perform_delete(self, instance):
        """
        Perform the deletion of a document instance.

        This method is responsible for performing the actual deletion of the document instance.

        Args:
            instance: The document instance to be deleted.

        Returns:
            Response: The response indicating success or error.
        """
        instance.delete()
        return Response({"message": "Document deleted successfully."}, status=status.HTTP_204_NO_CONTENT)  

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
    """
    A viewset for managing topics.

    Provides CRUD operations for topics, along with additional actions like updating and deleting topics.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        """
        Return the serializer context with the current request.
        """
        return {'request': self.request}
    
    @action(detail=False, methods=['post'])
    def create_topic(self, request):
        """
        Create a new topic along with an optional document.
        If a document file is not present in the request, a document_title for an existing document should be provided.
        
        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        # Create topic data
        topic_data = {
            'name': request.data.get('name'),  # Assuming 'name' is a required field for topics
            'start_page': request.data.get('start_page', None),
            'end_page': request.data.get('end_page', None),
        }

        if 'uploaded_document' in request.data:
            # Prepare the data for document creation
            document_data = {
                'document': request.data['uploaded_document']
            }

            # Call the create_document method to upload the document
            document = self.create_document(request, document_data)
            # Check if the document was created successfully
            if document:
                topic_data['document'] = document.id
            else:
                # If there was an error during document creation, return an error response
                return Response({'error': 'Document creation failed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif 'uploaded_document' not in request.data and 'document_title' not in request.data:
            return Response({'error': 'A document or title for an existing document has to be provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            document_title = request.data.get('document_title', None)
            if document_title:
                existing_document = Document.objects.filter(title=document_title).first()
                if existing_document:
                    topic_data['document'] = existing_document.id
                else:
                    return Response({'not found': 'Document with this title does not exist'}, status=status.HTTP_404_NOT_FOUND)

        existing_topic = Topic.objects.filter(name=topic_data['name'], document=topic_data['document']).first()
        if existing_topic:
            raise ValidationError({'name': 'A topic with the same name already exists for the provided document.'})
        # Create the topic
        serializer = TopicSerializer(data=topic_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def create_document(self, request, document_data):
        """
        Create a new document or retrieve an existing document based on the provided data.

        Args:
            request: The HTTP request object.
            document_data: Data for creating the document.

        Returns:
            Document or None: The created or existing Document object, or None if creation fails.
        """
        # Check if a document title is provided in the request
        document_title = request.data.get('document_title', None)
        if document_title:
            existing_document = Document.objects.filter(title=document_title).first()
            if existing_document:
                return existing_document  # Return the existing document
            else:
                document_data['title'] = document_title
        
        try:
            # Create an instance of the DocumentSerializer and call save to create the document
            serializer = DocumentSerializer(data=document_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return serializer.instance
            
        except Exception as e:
            # Check if existing_document_title is in the error and use it to search the database for that document
            if 'existing_document_title' in str(e):
                existing_document_title = e.detail['existing_document_title']
                existing_document = Document.objects.filter(title=existing_document_title).first()
                if existing_document:
                    return existing_document  
            return None 

    
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a topic by its ID or name.

        Args:
            request: The HTTP request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response containing the retrieved topic data.
            
        Raises:
            Http404: If the topic is not found.
        """
    
        lookup_field = self.lookup_field
        lookup_value = self.kwargs[lookup_field]

        try:
            # Check if the lookup value is numeric (likely an ID)
            int(lookup_value)
            topic = self.get_object()
        except ValueError:
            # If it's not numeric, consider it a topic name
            topics = Topic.objects.filter(name=lookup_value)
            if not topics.exists():
                raise Http404("Topic not found.")
            topic = topics

        serializer = self.get_serializer(topic, many=isinstance(topic, QuerySet))
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_topic(self, request):
        """
        Update a topic.

        Args:
            request: The HTTP request.

        Returns:
            Response: The response containing the updated topic data or error details.
        """
        # Parse query parameters to get topic name and document title
        topic_name = request.query_params.get('topic_name', '')
        document_title = request.query_params.get('document_title', '')

        # Query the database to find the topic
        try:
            topic = Topic.objects.get(name__iexact=topic_name, document__title__iexact=document_title)
        except Topic.DoesNotExist:
            return Response({'error': 'Topic not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the topic instance with JSON data from the request
        serializer = TopicSerializer(topic, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'])
    def delete_topic(self, request):
        """
        Delete a topic.

        Args:
            request: The HTTP request.

        Returns:
            Response: The response indicating success or error.
        """
        # Parse query parameters to get topic name and document title
        topic_name = request.query_params.get('topic_name', '')
        document_title = request.query_params.get('document_title', '')

        # Query the database to find the topic
        try:
            topic = Topic.objects.get(name__iexact=topic_name, document__title__iexact=document_title)
        except Topic.DoesNotExist:
            return Response({'error': 'Topic not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the topic instance
        topic.delete()
        return Response({'message': 'Topic deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class LectureViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    @action(detail=False, methods=['post'])
    def create_lecture(self, request):
        """
        Create a new lecture.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The response containing the created lecture data or error details.
        """
        serializer = LectureSerializer(data=request.data, context={'request': request})
    
        if serializer.is_valid():
            # Save the lecture without validating students for now
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['put'])
    def update_lecture(self, request):
        # Extract the lecture ID from the request data or query parameters
        lecture_id = request.data.get('id') or request.query_params.get('id')
        if not lecture_id:
            return Response({'error': 'Lecture ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the lecture instance to be updated
            lecture = Lecture.objects.get(pk=lecture_id)
        except Lecture.DoesNotExist:
            return Response({'error': 'Lecture not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a serializer instance for the lecture and update it with the request data
        serializer = LectureSerializer(lecture, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    @action(detail=False, methods=['delete'])
    def delete_lecture(self, request):
        # Extract the lecture ID from the request data or query parameters
        lecture_id = request.data.get('id') or request.query_params.get('id')
        if not lecture_id:
            return Response({'error': 'Lecture ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the lecture instance to be deleted
            lecture = Lecture.objects.get(pk=lecture_id)
        except Lecture.DoesNotExist:
            return Response({'error': 'Lecture not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the lecture instance
        lecture.delete()
        return Response({'message': 'Lecture deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

