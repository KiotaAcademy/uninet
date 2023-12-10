from django.db import models

from base.shared_across_apps.mixins import AdminsModelMixin

from django.contrib.auth import get_user_model

User = get_user_model()

# Model for the type of institution (e.g., college, university)
class Institution(AdminsModelMixin, models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=200, unique=True)
    chancellor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="chancellor_of", null=True, blank=True)
    vice_chancellor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="vice_chancellor_of", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_institutions", null=True)
    #admins = models.ManyToManyField(User, related_name="admin_institutions", blank=True)

    def __str__(self):
        return self.name
    

class School(AdminsModelMixin, models.Model):
    name = models.CharField(max_length=200)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="school_head")
    secretary = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="school_secretary")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="schools")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_schools", null=True)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'institution')

class Department(AdminsModelMixin, models.Model):
    name = models.CharField(max_length=200)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="department_head")
    secretary = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="department_secretary")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="departments")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_departments", null=True)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'school')


# Model for a course offered by the department
class Course(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_courses", null=True)

    def __str__(self):
        return self.name

# Model for units offered for a course
class Unit(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_units", null=True)

    def __str__(self):
        return self.name
