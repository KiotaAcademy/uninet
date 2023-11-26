from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'student', StudentViewSet)

urlpatterns = [
    # Add other URL patterns as needed
    path('', include(router.urls)),
    path('student/<int:pk>/student-documents/', StudentViewSet.as_view({'get': 'student_documents'}), name='student-documents'),
    path('student/<int:pk>/attended-lectures/', StudentViewSet.as_view({'get': 'attended_lectures'}), name='attended-lectures'),

]
