from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.http import Http404

from .models import Lecturer, Lecture
from .serializers import LecturerSerializer, LectureSerializer

from base.shared_across_apps.mixins import ObjectLookupMixin

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if a lecturer with the same user already exists
        user = self.request.user
        existing_lecturer = Lecturer.objects.filter(user=user).first()

        if existing_lecturer:
            # If an existing lecturer is found, return it
            serializer.instance = existing_lecturer
            return

        # Create a new lecturer if one doesn't already exist
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def retrieve_lecturer(self, request):
        username = request.query_params.get('username', None)
        if username:
            lecturer = Lecturer.objects.filter(user__username=username).first()
            
            if lecturer:
                serializer = self.get_serializer(lecturer)
                return Response(serializer.data)
            else:
                return Response({"detail": "Lecturer status not found."}, status=404)
        else:
            return Response({"detail": "Username parameter is required."}, status=400)
    
    @action(detail=False, methods=['PUT'])
    def update_lecturer(self, request):
        # Ensure that the user can only update their own lecturer instance
        lecturer = Lecturer.objects.filter(user=request.user).first()
        if not lecturer:
            raise Http404("Lecturer not found.")
        request.data['institution'] = lecturer.institution.name
        serializer = self.get_serializer(lecturer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['DELETE'])
    def delete_lecturer(self, request):
        # Ensure that the user can only delete their own lecturer instance
        lecturer = Lecturer.objects.filter(user=request.user).first()
        if not lecturer:
            raise Http404("Lecturer not found.")
        
        lecturer.delete()
        return Response({"detail": "Lecturer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class LectureViewSet(ObjectLookupMixin, viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if a lecturer with the same user already exists
        user = self.request.user
        existing_lecturer = Lecturer.objects.filter(user=user).first()
        
        if not existing_lecturer:
            return Response({"detail": "Only lecturers can create lectures."}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(lecturer=existing_lecturer)
    
    @action(detail=False, methods=['GET'])
    def retrieve_lecture(self, request):
        # Extract query parameters
        name = request.query_params.get('name', None)
        unit_name = request.query_params.get('unit', None)
        department_name = request.query_params.get('department', None)
        date = request.query_params.get('date', None)

        # Look up the lecture based on the provided parameters
        lectures = self.lookup_object(
            request=request,
            queryset=self.queryset,
            filters={
                'name': name,
                'unit__name': unit_name,
                'unit__course__department__name': department_name,
                'date': date
            }
        )

        serializer = self.get_serializer(lectures, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_lecture(self, request):
        # Check if the user is a lecturer
        lecturer = Lecturer.objects.filter(user=request.user).first()
        if not lecturer:
            return Response({"detail": "Only lecturers can update lectures."}, status=status.HTTP_403_FORBIDDEN)

        # Extract query parameters
        name = request.data.get('name', None)
        unit_name = request.data.get('unit', None)
        department_name = request.data.get('department', None)
        date = request.data.get('date', None)

        # Look up the lecture based on the provided parameters and lecturer
        lectures = self.lookup_object(
            request=request,
            queryset=self.queryset.filter(lecturer=lecturer),
            filters={
                'name': name,
                'unit__name': unit_name,
                'unit__course__department__name': department_name,
                'date': date
            }
        )

        # Ensure there is only one lecture matching the criteria
        if len(lectures) != 1:
            return Response({"detail": "Invalid or multiple lectures match the criteria."}, status=status.HTTP_400_BAD_REQUEST)

        lecture = lectures[0]
        serializer = self.get_serializer(lecture, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['DELETE'])
    def delete_lecture(self, request):
        # Check if the user is a lecturer
        lecturer = Lecturer.objects.filter(user=request.user).first()
        if not lecturer:
            return Response({"detail": "Only lecturers can delete lectures."}, status=status.HTTP_403_FORBIDDEN)

        # Extract query parameters
        name = request.data.get('name', None)
        unit_name = request.data.get('unit', None)
        department_name = request.data.get('department', None)
        date = request.data.get('date', None)

        # Look up the lecture based on the provided parameters and lecturer
        lectures = self.lookup_object(
            request=request,
            queryset=self.queryset.filter(lecturer=lecturer),
            filters={
                'name': name,
                'unit__name': unit_name,
                'unit__course__department__name': department_name,
                'date': date
            }
        )

        # Ensure there is only one lecture matching the criteria
        if len(lectures) != 1:
            return Response({"detail": "Invalid or multiple lectures match the criteria."}, status=status.HTTP_400_BAD_REQUEST)

        lecture = lectures[0]
        lecture.delete()

        return Response({"detail": "Lecture deleted successfully."}, status=status.HTTP_204_NO_CONTENT)