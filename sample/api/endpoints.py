# endpoints.py
import random
import string
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from django.db import transaction
from fastapi.responses import RedirectResponse

# from api.models import Project

# from .schemas import ProjectResponse

router = APIRouter()
app = FastAPI()

# client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = client.mydatabase



class ProjectItem(BaseModel):
      name: str
      key: str
      type: str
      lead: str  # Assuming lead is a string identifier like an ObjectId
# #
#  class ProjectResponse(Project):
#      id: ObjectId

# @app.get("/projects")
# async def create_project():
#      return {"message": "project information here" }

    # result = await db.projects.insert_one(new_project)
    # if result.inserted_id:
    #     return ProjectResponse(**new_project)
    # raise HTTPException(status_code=500, detail="Project creation failed")
#     project_id = str(ObjectId())
#     projects_db[project_id] = project.dict()
#     return {
#         "success": True,
#         "msg": "Project created successfully.",
#         "project": {**projects_db[project_id], "id": project_id}
#     }
#
# @app.get("/project/id/" )
# #response_model=ProjectResponse
# def get_project():
#     # if not project_id:
#     #     raise HTTPException(status_code=400, detail="Project ID is required")
#     return {"project_id": "unique id here"}
#     if project_id not in projects_db:
#         raise HTTPException(status_code=404, detail="Project not found")
#     return projects_db[project_id]
#
# @app.put("/API/v1/project/id/{project_id}", response_model=ProjectResponse)
# def update_project(project_id: str, project: Project):
#     if project_id not in projects_db:
#         raise HTTPException(status_code=404, detail="Project not found")
#     projects_db[project_id].update(project.dict())
#     return {
#         "success": True,
#         "msg": "Project updated successfully.",
#         "project": {**projects_db[project_id], "id": project_id}
#     }
#
# @app.delete("/API/v1/project/id/{project_id}", response_model=Dict[str, bool])
# def delete_project(project_id: str):
#     if project_id not in projects_db:
#         raise HTTPException(status_code=404, detail="Project not found")
#     del projects_db[project_id]
#     return {"success": True}

@app.get("/test")
async def read_test():
    return {"message": "This is a test endpoint"}

#project management

@app.get("/projects")
async def view_project():
    return {"message": "project information here"}

@app.post("/projects")
async def create_project():
    return {"message": "Project created successfully"}

@app.delete("/projects")
async def delete_project():
    return {"message": "project successful deleted"}

@app.put("/projects")
async def update_project():
    return {"message": "Project with ID 'x' updated successfully"}

@app.patch("/projects")
async def project_last_issued_update():
    return {"message": "Last updated issue for project with ID 'id' updated successfully"}



# @app.post("/project")
# def create_project(item: ProjectItem):
# #     short_urls = shortener.encode(item.url, item.title)
#      return {
# #         "real_url": short_urls["real_url"],
# #         "display_url": short_urls["display_url"],
# #         "title": item.title
#            "name": "Project Name",
# 		   "key": "Project Initials",
# 		   "type": "Team-managed business",
# 		   "lead": "UserID"
#        }

# redirect
@app.get("/{short_key}")
def redirect_url(short_key: str):
    mapping = None#URLMapping.objects.filter(short_url=short_key).first()
    if mapping:
        return RedirectResponse(url=mapping.long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
