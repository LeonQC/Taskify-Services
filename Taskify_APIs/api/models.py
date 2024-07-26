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

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    lead = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_issue = models.TextField(null=True, blank=True)  # 新增字段


    def __str__(self):
        return self.name


