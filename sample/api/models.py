#models.py
# from django.db import models
#
# class Project(models.Model):
#       name = models.CharField(max_length=255, unique=True)
#       key = models.CharField(max_length=10, unique=True)
#       type = models.CharField(max_length=255, blank=True, null=True)
#       lead = models.CharField(max_length=255, blank=True, null=True)
#       created_at = models.DateTimeField(auto_now_add=True)
#
#       def __str__(self):
#           return self.name
#

# # models.py
#
# from pydantic import BaseModel, Field
# from bson import ObjectId
#
# class Project(BaseModel):
#     id: ObjectId = Field(..., alias="_id")
#     name: str
#     key: str
#     type: str
#     lead: ObjectId
#
#     class Config:
#         arbitrary_types_allowed = True  # 允许处理未知类型，如 ObjectId
