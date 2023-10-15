from django.contrib import admin
from .models import Institution, School, Department, Course, Unit

admin.site.register([Institution, School, Department, Course, Unit])