#models.py
from django.db import models

# class URLMapping(models.Model):
#     long_url = models.URLField()
#     short_url = models.CharField(max_length=10, unique=True)
#     title = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.short_url

from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    public_name = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


