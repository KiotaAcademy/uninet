from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Lecturer
from .serializers import LecturerSerializer

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
