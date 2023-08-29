from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, TopicViewSet, LectureViewSet, CategoryViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'lectures', LectureViewSet)
router.register(r'categories', CategoryViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('categories/delete_by_name/<str:name>/', CategoryViewSet.as_view({'delete': 'delete_by_name'}), name='delete-category-by-name'),

    path('documents/<int:pk>/download_document_by_id/', DocumentViewSet.as_view({'get': 'download_document_by_id'}), name='download-document-by-id'),
    path('documents/<str:title>/download_document_by_title/', DocumentViewSet.as_view({'get': 'download_document_by_title'}), name='download-document-by-title'),


    ]
