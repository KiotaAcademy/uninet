from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutionViewSet, SchoolViewSet, DepartmentViewSet, CourseViewSet, UnitViewSet

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'units', UnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
