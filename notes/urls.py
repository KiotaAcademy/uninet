from django.urls import path, include
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

]
