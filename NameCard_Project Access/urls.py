from django.urls import path
from .views import UserDetailedNameCardlView, ProjectAccessView

urlpatterns = [
    path('API/v1/Users', UserDetailedNameCardlView.as_view(), name='user-detail'),
    path('API/v1/accesses', ProjectAccessView.as_view(), name='access-view'),
]
