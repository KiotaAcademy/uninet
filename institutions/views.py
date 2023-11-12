from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Institution, School, Department, Course, Unit
from .serializers import InstitutionSerializer, SchoolSerializer, DepartmentSerializer, CourseSerializer, UnitSerializer
from base.shared_across_apps.mixins import ObjectViewMixin

class InstitutionViewSet(ObjectViewMixin, viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['GET'])
    def retrieve_institution(self, request):
        institution = self.lookup_object(request, self.queryset)
        serializer = self.get_serializer(institution)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_institution(self, request):
        institution = self.lookup_object(request, self.queryset)
        authorized = self.check_authorization(institution, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to update this institution. Only institution-level admins can update.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(institution, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def delete_institution(self, request):
        institution = self.lookup_object(request, self.queryset)
        authorized = self.check_authorization(institution, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to DELETE this institution. Only institution-level admins can DELETE.'}, status=status.HTTP_403_FORBIDDEN)

        institution.delete()
        return Response({'message': 'Institution deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
