from django.db import models
from django.contrib.auth import get_user_model

from institutions.models import Institution
from base.shared_across_apps.mixins import AdminsModelMixin

User = get_user_model()

class ClubSociety(AdminsModelMixin, models.Model):
    name = models.CharField(max_length=200)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    
    avatar = models.ImageField(upload_to='clubs_societies/avatars/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)

    members = models.ManyToManyField(User, related_name='clubs_societies', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_clubs_societies', null=True)

    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    class Meta:
        unique_together = ['name', 'institution']
    
    def __str__(self):
        return self.name

