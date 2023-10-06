from django.db import models
from django.contrib.auth import get_user_model

from notes.models import Document, Lecture

User = get_user_model()

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    # Add any additional fields specific to students here, for example:
    # student_id = models.CharField(max_length=10, unique=True)
    # program = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

