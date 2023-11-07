from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Institution, School, Department, Course, Unit
from .serializers import InstitutionSerializer, SchoolSerializer, DepartmentSerializer, CourseSerializer, UnitSerializer

class ObjectViewMixin:
    """
    A mixin for viewsets to provide object lookup and authorization checks.
    """
    def lookup_object(self, request, queryset, id_param='id', name_param='name'):
        """
        Retrieve an object by either its primary key or name using the given queryset.
        Use the 'id' parameter for the PK or 'name' for the name.
        """
        id_param_value = request.query_params.get(id_param)
        name_param_value = request.query_params.get(name_param)

        if id_param_value:
            obj = get_object_or_404(queryset, pk=id_param_value)
        elif name_param_value:
            obj = get_object_or_404(queryset, name=name_param_value)
        else:
            return Response({'error': f'You must provide either the {id_param} or {name_param} parameter for the lookup.'}, status=status.HTTP_400_BAD_REQUEST)

        return obj

    def check_authorization(self, obj, user, user_field='admins'):
        """
        Check if the user is authorized to perform actions on the object.
        The user must be an object-level admin to perform these actions.
        """
        if user_field not in obj._meta.fields:
            return Response({'error': f'Invalid field name {user_field} for object-level admins.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user not in getattr(obj, user_field).all():
            return Response({'error': f'You are not authorized to perform this action on this object. Only object-level admins can do this.'}, status=status.HTTP_403_FORBIDDEN)

        return None


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
        self.check_authorization(institution, request.user)

        serializer = self.get_serializer(institution)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_institution(self, request):
        institution = self.lookup_object(request, self.queryset)
        self.check_authorization(institution, request.user)

        serializer = self.get_serializer(institution, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def delete_institution(self, request):
        institution = self.lookup_object(request, self.queryset)
        self.check_authorization(institution, request.user)

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
