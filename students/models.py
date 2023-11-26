from django.db import models
from django.contrib.auth import get_user_model
from institutions.models import Institution, School, Department, Course

User = get_user_model()

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username