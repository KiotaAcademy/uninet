from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentProfileViewSet

router = DefaultRouter()
router.register(r'student-profiles', StudentProfileViewSet)

urlpatterns = [
    # Add other URL patterns as needed
    path('', include(router.urls)),
    path('student-profiles/<int:pk>/student-documents/', StudentProfileViewSet.as_view({'get': 'student_documents'}), name='student-documents'),
    # path('student-profiles/<int:pk>/attended-lectures/', StudentProfileViewSet.as_view({'get': 'attended_lectures'}), name='attended-lectures'),

]
