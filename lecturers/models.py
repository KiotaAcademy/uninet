from django.db import models
from django.contrib.auth import get_user_model
from institutions.models import Institution, School, Department, Course, Unit

User = get_user_model()

class Lecturer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    departments = models.ManyToManyField(Department, related_name='lecturers')

    def __str__(self):
        return self.user.username

class Lecture(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.title} - {self.date}"