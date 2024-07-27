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
from django.contrib.auth.models import User
import uuid

from api.endpoints import Attachment, LinkedIssue, Comment, History, Action, Activity


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    lead = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_issue = models.TextField(null=True, blank=True)  # 新增字段

    class User(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        full_name = models.CharField(max_length=100)
        public_name = models.CharField(max_length=100)
        initials = models.CharField(max_length=10)
        email = models.EmailField(unique=True)
        status = models.CharField(max_length=50)
        last_active = models.DateTimeField(auto_now=True)

    class Comment(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        timestamp = models.DateTimeField(auto_now_add=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        initials = models.CharField(max_length=10)
        comment = models.TextField()

    class History(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        timestamp = models.DateTimeField(auto_now_add=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        initials = models.CharField(max_length=10)
        event = models.CharField(max_length=200)

    class Attachment(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        timestamp = models.DateTimeField(auto_now_add=True)
        file_name = models.CharField(max_length=255)

    class LinkedIssue(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        timestamp = models.DateTimeField(auto_now_add=True)
        link_id = models.UUIDField()

    class Action(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        action_type = models.CharField(max_length=50)
        attachments = models.ManyToManyField(Attachment, related_name='actions', blank=True)
        linked_issues = models.ManyToManyField(LinkedIssue, related_name='actions', blank=True)

    class Activity(models.Model):
        comments = models.ManyToManyField(Comment, related_name='activities', blank=True)
        history = models.ManyToManyField(History, related_name='activities', blank=True)
        actions = models.ManyToManyField(Action, related_name='activities', blank=True)

    class Task(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        name = models.CharField(max_length=255)
        description = models.TextField()
        total_order_id = models.CharField(max_length=100)
        assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True)
        reporter = models.ForeignKey(User, related_name='reported_tasks', on_delete=models.SET_NULL, null=True)
        priority = models.CharField(max_length=50)
        start_date = models.DateTimeField()
        due_date = models.DateTimeField()
        status_id = models.CharField(max_length=50)
        activity = models.OneToOneField(Activity, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


