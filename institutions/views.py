from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Institution, School, Department, Course, Unit
from .serializers import InstitutionSerializer, SchoolSerializer, DepartmentSerializer, CourseSerializer, UnitSerializer

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def retrieve_institution(self, request):
        """
        Retrieve an institution by either its primary key or name.
        Use the 'id' parameter for the PK or 'name' for the name.
        """
        id_param = request.query_params.get('id')
        name_param = request.query_params.get('name')

        if id_param:
            institution = self.queryset.filter(pk=id_param).first()
        elif name_param:
            institution = self.queryset.filter(name=name_param).first()
        else:
            return Response({'error': 'You must provide either the id or name parameter for the lookup.'}, status=400)

        if institution:
            serializer = self.get_serializer(institution)
            return Response(serializer.data)
        else:
            return Response({'error': 'Institution not found.'}, status=404)
        

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
