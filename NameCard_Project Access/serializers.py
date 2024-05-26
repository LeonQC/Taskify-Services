from rest_framework import serializers
from .models import UserDetailedNameCard, ProjectAccess

class UserDetailedNameCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailedNameCard
        fields = ['id', 'full_name', 'public_name', 'initials', 'email', 'status', 'last_active']

class ProjectAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccess
        fields = ['user', 'roles']
