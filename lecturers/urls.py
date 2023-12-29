from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LecturerViewSet, LectureViewSet

# Create a router and register the LecturerViewSet
router = DefaultRouter()
router.register(r'lecturer', LecturerViewSet)
router.register(r'lecture', LectureViewSet)


# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
