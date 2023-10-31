from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminsMixin(models.Model):
    """
    A mixin to add users to the `admins` field based on the specified user fields.
    """
    admins = models.ManyToManyField(User, related_name="admin_%(class)ss", blank=True)

    def add_admins(self, *user_fields):
        for field in user_fields:
            user = getattr(self, field, None)
            if user and user not in self.admins.all():
                self.admins.add(user)

    class Meta:
        abstract = True

# Model for the type of institution (e.g., college, university)
class Institution(AdminsMixin, models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=200, unique=True)
    chancellor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="chancellor_of", null=True, blank=True)
    vice_chancellor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="vice_chancellor_of", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_institutions", null=True)
    #admins = models.ManyToManyField(User, related_name="admin_institutions", blank=True)

    def __str__(self):
        return self.name
    

# Model for a school in the institution (e.g., school of engineering)
class School(models.Model):
    name = models.CharField(max_length=200)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="schools")
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_schools", null=True)

    def __str__(self):
        return self.name
    


# Model for a department under a school (e.g., department of electrical engineering)
class Department(models.Model):
    name = models.CharField(max_length=200)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="departments")
    #created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_departments", null=True)


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
