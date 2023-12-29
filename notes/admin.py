from django.contrib import admin
from .models import Category, Document, Topic

# Register your models here.
admin.site.register([Category, Document, Topic])
