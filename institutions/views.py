from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

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
        serializer = self.get_serializer(institution, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_institution(self, request):
        institution = self.lookup_object(request, self.queryset)[0]
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
        institution = self.lookup_object(request, self.queryset)[0]
        authorized = self.check_authorization(institution, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to DELETE this institution. Only institution-level admins can DELETE.'}, status=status.HTTP_403_FORBIDDEN)

        institution.delete()
        return Response({'message': 'Institution deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class SchoolViewSet(ObjectViewMixin, viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['GET'])
    def retrieve_school(self, request):
        institution_name = request.query_params.get('institution', None)
        schools = self.lookup_object(request, self.queryset, filters={'institution__name': institution_name})
        serializer = self.get_serializer(schools, many=True)            
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_school(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)

        school = self.lookup_object(request, self.queryset, filters={'institution__name': institution_name})[0]
        authorized = self.check_authorization(school, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to update this school. Only school-level admins can update.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def delete_school(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)

        school = self.lookup_object(request, self.queryset, filters={'institution__name': institution_name})[0]
        authorized = self.check_authorization(school, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to DELETE this school. Only school-level admins can DELETE.'}, status=status.HTTP_403_FORBIDDEN)

        school.delete()
        return Response({'message': 'School deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class DepartmentViewSet(ObjectViewMixin, viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['GET'])
    def retrieve_department(self, request):
        institution_name = request.query_params.get('institution', None)
        departments = self.lookup_object(request, self.queryset, filters={'school__institution__name': institution_name})
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['PUT'])
    def update_department(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)

        department = self.lookup_object(request, self.queryset, filters={'school__institution__name': institution_name})[0]
        authorized = self.check_authorization(department, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to update this school. Only school-level admins can update.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def delete_department(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)

        department = self.lookup_object(request, self.queryset, filters={'school__institution__name': institution_name})[0]
        authorized = self.check_authorization(department, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to DELETE this department. Only department-level admins can DELETE.'}, status=status.HTTP_403_FORBIDDEN)

        department.delete()
        return Response({'message': 'Department deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CourseViewSet(ObjectViewMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def retrieve_course(self, request):
        institution_name = request.query_params.get('institution', None)
        courses = self.lookup_object(request, self.queryset, filters={'department__school__institution__name': institution_name})
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['PUT'])
    def update_course(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)
        
        course = self.lookup_object(request, self.queryset, filters={'department__school__institution__name': institution_name})[0]
        # If you have authorization checks, perform them here
        department = course.department
        authorized = self.check_authorization(department, request.user)
        if not authorized:
            return Response({'error': 'You are not authorized to update this course. Only Department-level admins can update.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['DELETE'])
    def delete_course(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)
        
        course = self.lookup_object(request, self.queryset, filters={'department__school__institution__name': institution_name})[0]
        # If you have authorization checks, perform them here
        department = course.department
        authorized = self.check_authorization(department, request.user)
        if not authorized:
            return Response({'error': 'You are not authorized to DELETE this course. Only Department-level admins can delete.'}, status=status.HTTP_403_FORBIDDEN)

        course.delete()
        return Response({'message': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class UnitViewSet(ObjectViewMixin, viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def retrieve_unit(self, request):
         # Extract query parameters
        institution_name = request.query_params.get('institution', None)
        course_name = request.query_params.get('course', None)

        # Look up the unit based on the provided parameters
        units = self.lookup_object(
            request,
            self.queryset,
            filters={
                'course__department__school__institution__name': institution_name,
                'course__name': course_name
            }
        )
        

        serializer = self.get_serializer(units, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['PUT'])
    def update_unit(self, request):
        institution_name = request.query_params.get('institution', None)
        course_name = request.query_params.get('course', None)
        if not institution_name or not course_name:
            return Response({'error': 'You must provide the institution, course and name of the unit in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)

        unit = self.lookup_object(
            request,
            self.queryset,
            filters={
                'course__department__school__institution__name': institution_name,
                'course__name': course_name
            }
        )[0]

        department = unit.course.department
        authorized = self.check_authorization(department, request.user)
        if not authorized:
            return Response({'error': 'You are not authorized to update this unit. Only Department-level admins can update.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['DELETE'])
    def delete_unit(self, request):
        institution_name = request.query_params.get('institution', None)
        course_name = request.query_params.get('course', None)
        
        if not institution_name or not course_name:
            return Response({'error': 'You must provide the institution, course and name of the unit in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)
        
        unit = self.lookup_object(
            request,
            self.queryset,
            filters={
                'course__department__school__institution__name': institution_name,
                'course__name': course_name
            }
        )[0]

        department = unit.course.department
        authorized = self.check_authorization(department, request.user)
        if not authorized:
            return Response({'error': 'You are not authorized to delete this unit. Only Department-level admins can delete.'}, status=status.HTTP_403_FORBIDDEN)

        unit.delete()
        return Response({'message': 'Unit deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



