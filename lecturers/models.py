from django.db import models
from django.contrib.auth import get_user_model
from institutions.models import Institution, School, Department, Course

User = get_user_model()

class Lecturer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    departments = models.ManyToManyField(Department, related_name='lecturers')

    def __str__(self):
        return self.user.username