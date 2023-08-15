from django.contrib import admin
from .models import Category, Document, Topic, Lecture

# Register your models here.
admin.site.register([Category, Document, Topic, Lecture])
