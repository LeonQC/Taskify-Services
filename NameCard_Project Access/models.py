from django.db import models

class UserDetailedNameCard(models.Model):
    full_name = models.CharField(max_length=100)
    public_name = models.CharField(max_length=50)
    initials = models.CharField(max_length=10)
    email = models.EmailField()
    status = models.CharField(max_length=20)
    last_active = models.DateTimeField()

class ProjectAccess(models.Model):
    user = models.ForeignKey(UserDetailedNameCard, on_delete=models.CASCADE)
    roles = models.JSONField(default=list)

