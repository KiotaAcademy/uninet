from rest_framework import viewsets
from .models import Lecturer
from .serializers import LecturerSerializer

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer

    # You can add any additional custom views or actions for the Lecturer model here if needed.
