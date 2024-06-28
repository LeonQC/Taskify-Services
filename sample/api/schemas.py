# # schemas.py
#
# from pydantic import BaseModel
#
# class ProjectCreate(BaseModel):
#     name: str
#     key: str
#     type: str
#     lead: str
#
# class ProjectUpdate(BaseModel):
#     name: str = None
#     key: str = None
#     type: str = None
#     lead: str = None
#
# class LastIssueUpdate(BaseModel):
#     lastUpdatedIssue: str
#
# class ProjectResponse(BaseModel):
#     id: str
#     name: str
#     key: str
#     type: str
#     lead: str
#
# class ProjectListResponse(BaseModel):
#     success: bool
#     projects: list[ProjectResponse]
#
