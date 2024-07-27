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


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    lead = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_issue = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    public_name = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    total_order_id = models.IntegerField()
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_tasks')
    priority = models.CharField(max_length=50,
                                choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    status_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def key(self):
        # 提取项目名称中每个单词的首字母并大写
        project_initials = ''.join([word[0].upper() for word in self.project.name.split()])
        return project_initials

    def __str__(self):
        return self.name

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    initials = models.CharField(max_length=10, blank=True)
    comment = models.TextField()

    def save(self, *args, **kwargs):
        if self.user and not self.initials:
            self.initials = ''.join([name[0].upper() for name in self.user.get_full_name().split()])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.user} on {self.task}"

    class History(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
        timestamp = models.DateTimeField(auto_now_add=True)
        user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        initials = models.CharField(max_length=10, blank=True)
        event = models.CharField(max_length=200)
        details = models.TextField(null=True, blank=True)

        def save(self, *args, **kwargs):
            if self.user and not self.initials:
                self.initials = ''.join([name[0].upper() for name in self.user.get_full_name().split()])
            super().save(*args, **kwargs)

        def __str__(self):
            return f"History for {self.task}"

    class Action(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='actions')
        timestamp = models.DateTimeField(auto_now_add=True)
        action_type = models.CharField(max_length=50,
                                       choices=[('link_issue', 'Link Issue'), ('attached_file', 'Attached File')])
        details = models.JSONField()

        def __str__(self):
            return f"Action {self.action_type} on {self.task}"


