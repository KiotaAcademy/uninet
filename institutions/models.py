from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminsModelMixin(models.Model):
    """
    A mixin to manage administrators for a model instance.

    This mixin includes an 'admins' field that is a ManyToMany relationship with User,
    allowing the association of multiple administrators to a model instance.

    Methods:
        - add_admins: Add one or more administrators to the 'admins' field.

    Meta:
        abstract (bool): Indicates that this is an abstract model and should not be instantiated.
    """
    
    admins = models.ManyToManyField(User, related_name="admin_%(class)ss", blank=True)

    def add_admins_from_specified_fields(self, *user_fields):
        """
        Add users from specified fields to the 'admins' field.

        Args:
            *user_fields: Variable number of fields containing User instances to be added as admins.
            
        Usage:
            instance.add_admins('field1','chancellor', 'field3', ...)
            instance.add_admins(*default_admins)
                
                default_admins (List[str]): List of default admin fields to add to the instance.
                default_admins = ['head', 'secretary', 'created_by']

        This method iterates through the specified fields, retrieves the User instance from each field,
        and adds it to the 'admins' field if it is not already present.
        """
        for field in user_fields:
            user = getattr(self, field, None)
            if user and user not in self.admins.all():
                self.admins.add(user)

    class Meta:
        abstract = True

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

    def __str__(self):
        return self.name

# Model for units offered for a course
class Unit(models.Model):
    name = models.CharField(max_length=200)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")

    def __str__(self):
        return self.name
