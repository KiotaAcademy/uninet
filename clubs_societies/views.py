from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import ClubSociety
from .serializers import ClubSocietySerializer
from base.shared_across_apps.mixins import ObjectViewMixin

class ClubSocietyViewSet(ObjectViewMixin, viewsets.ModelViewSet):
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
    
    @action(detail=False, methods=['GET'])
    def retrieve_club(self, request):
        institution_name = request.query_params.get('institution', None)
        clubs = self.lookup_object(request, self.queryset, filters={'institution__name': institution_name})
        serializer = self.get_serializer(clubs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['PUT'])
    def update_club(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)

        club = self.lookup_object(request, self.queryset, filters={'institution__name': institution_name})[0]
        authorized = self.check_authorization(club, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to update this club. Only club-level admins can update.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(club, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def delete_club(self, request):
        institution_name = request.query_params.get('institution', None)
        if not institution_name:
            return Response({'error': 'You must provide the institution in the query parameters of the request'}, status=status.HTTP_400_BAD_REQUEST)

        club = self.lookup_object(request, self.queryset, filters={'institution__name': institution_name})[0]
        authorized = self.check_authorization(club, request.user)

        if not authorized:
            return Response({'error': 'You are not authorized to DELETE this club. Only club-level admins can DELETE.'}, status=status.HTTP_403_FORBIDDEN)

        club.delete()
        return Response({'message': 'Club deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
