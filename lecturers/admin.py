from django.contrib import admin
from .models import Lecturer, Lecture
# Register your models here.
admin.site.register([Lecturer, Lecture])