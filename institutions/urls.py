from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutionViewSet, SchoolViewSet, DepartmentViewSet, CourseViewSet, UnitViewSet

router = DefaultRouter()
router.register(r'institution', InstitutionViewSet)
router.register(r'school', SchoolViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'course', CourseViewSet)
router.register(r'unit', UnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
