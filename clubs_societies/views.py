from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import ClubSociety
from .serializers import ClubSocietySerializer

class ClubSocietyViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing club and society profiles.

    Provides CRUD operations for club/society profiles.
    """
    queryset = ClubSociety.objects.all()
    serializer_class = ClubSocietySerializer
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
        club = serializer.instance
        club.members.add(self.request.user)