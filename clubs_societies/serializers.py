from rest_framework import serializers
from .models import ClubSociety
from accounts.serializers import UserProfileSerializer
from institutions.models import Institution
from django.contrib.auth import get_user_model

from base.shared_across_apps.serializers import GenericRelatedField
from base.shared_across_apps.mixins import AdminsSerializerMixin

User = get_user_model()

class ClubSocietySerializer(AdminsSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for the ClubSociety model.

    This serializer is designed to work with ClubSociety models. It uses the GenericRelatedField
    for handling related fields like 'institution', 'members', and 'created_by'.
    """
    class Meta:
        model = ClubSociety
        fields = '__all__'

    institution = GenericRelatedField(queryset=Institution.objects.all(), field="name")
    members = GenericRelatedField(queryset=User.objects.all(), field="username", many=True, required=False)
    remove_members = GenericRelatedField(queryset=User.objects.all(), field="username", many=True, required=False)

    created_by = serializers.StringRelatedField(source='created_by.username')
    
    admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)
    remove_admins = GenericRelatedField(queryset=User.objects.all(), field="username", required=False, many=True)

    def create(self, validated_data):
        default_admins = ['created_by']

        # Add admins to members before creating
        admins = validated_data.get('admins', [])
        members = validated_data.get('members', [])
        members.extend(admins)
        validated_data['members'] = members

        instance = super().create(validated_data)
        return self.add_admins_to_instance(instance, validated_data, default_admins)
    
    def update(self, instance, validated_data):
        default_admin_fields = []
        # Check if the user who created the club is in remove_members
        created_by = instance.created_by.username
        if created_by in validated_data.get('remove_members', []):
            # If yes, do not remove them from members and do not touch admin status
            validated_data['remove_members'].remove(created_by)
        else:
            # If no, proceed with removing members and updating admin status
            removed_members = validated_data.get('remove_members', [])
            instance.members.remove(*removed_members)

            # Update remove_admins with the removed members
            validated_data.setdefault('remove_admins', []).extend(removed_members)

        instance = self.update_admins_for_instance(instance, validated_data, default_admin_fields)

        # Always add admins to members
        instance.members.add(*instance.admins.all())

        # Update the instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance