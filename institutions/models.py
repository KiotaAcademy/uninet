from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Model for the type of institution (e.g., college, university)
class Institution(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    chancellor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="chancellor_of", null=True)
    vice_chancellor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="vice_chancellor_of", null=True)

    def __str__(self):
        return self.name

# Model for a school in the institution (e.g., school of engineering)
class School(models.Model):
    name = models.CharField(max_length=200)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="schools")

    def __str__(self):
        return self.name

# Model for a department under a school (e.g., department of electrical engineering)
class Department(models.Model):
    name = models.CharField(max_length=200)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name

# Model for a course offered by the department
class Course(models.Model):
    name = models.CharField(max_length=200)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.name

# Model for units offered for a course
class Unit(models.Model):
    name = models.CharField(max_length=200)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")

    def __str__(self):
        return self.name
