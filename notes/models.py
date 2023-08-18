from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse

from rest_framework.exceptions import ValidationError


User = get_user_model()

class Category(models.Model):
    """
    Model representing categories for notes.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    """
    Model representing individual notes.
    """
    title = models.CharField(max_length=200, blank=True)
    document = models.FileField(upload_to='notes/documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # User who uploaded the notes
    author = models.CharField(max_length=200, blank=True)  # Author name (optional)
    categories = models.ManyToManyField(Category)  

    def __str__(self):
        return self.title

# Signal to set default title for Note based on the filename
@receiver(pre_save, sender=Document)
def set_default_document_title(sender, instance, *args, **kwargs):
    if not instance.title:
        # Set default title based on the filename
        filename = instance.document.name
        instance.title = filename.split('.')[0]  # Use the filename without extension

    # Check if a document with the same title already exists
    existing_document = Document.objects.filter(title=instance.title).exclude(pk=instance.pk).first()
    if existing_document:
        
        if existing_document.uploaded_by == instance.uploaded_by:
            raise ValidationError({'title': 'You have already uploaded a document with the same title.',
                                   })
        else:
            raise ValidationError({
                'title': f"A document with the same title was uploaded by {existing_document.uploaded_by.username}.",
            })



class Topic(models.Model):
    """
    Model representing individual topics discussed during a lecture.
    """
    name = models.CharField(max_length=200)
    start_page = models.PositiveIntegerField(blank=True)
    end_page = models.PositiveIntegerField(blank=True)
    notes = models.ManyToManyField(Document)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    """
    Model representing various lectures that have taken place.
    """
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
    students = models.ManyToManyField(User, related_name='lectures_attended')
    lecturer_comments = models.TextField(blank=True)

    def __str__(self):
        return f"Lecture: {self.id} - {self.lecturer}"
