from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import EmailStr, BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI()

projects_db = []

router = APIRouter()

class Project(BaseModel):
    id: UUID
    name: str
    key: str
    type: str
    lead: UUID
    created_at: datetime
    updated_at: datetime
    last_updated_issue: Optional[str] = None

class ProjectCreateRequest(BaseModel):
    name: str
    key: str
    type: str
    lead: UUID

class ProjectInviteRequest(BaseModel):
    email: EmailStr
    project_id: UUID

class ProjectInviteResponse(BaseModel):
    status: str
    message: str

class ProjectListResponse(BaseModel):
    status: str
    data: List[Project]

class UpdateProjectRequest(BaseModel):
    id: UUID
    name: Optional[str] = None
    key: Optional[str] = None
    type: Optional[str] = None
    lead: Optional[UUID] = None

class UpdateProjectResponse(BaseModel):
    status: str
    msg: str

class UpdateLastIssueRequest(BaseModel):
    lastUpdatedIssue: str

class UpdateLastIssueResponse(BaseModel):
    status: str
    message: str

class ProjectDetailResponse(BaseModel):
    success: bool
    projects: Project

class DeleteProjectResponse(BaseModel):
    status: str
    msg: str

@app.post("/API/v1/projects", response_model=Project)
def create_project(request: ProjectCreateRequest):
    new_project = Project(
        id=uuid4(),
        name=request.name,
        key=request.key,
        type=request.type,
        lead=request.lead,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    projects_db.append(new_project)
    return new_project

@app.post("/API/v1/projects/invitations", response_model=ProjectInviteResponse)
def invite_user_to_project(request: ProjectInviteRequest):
    if request.email and request.project_id:
        return ProjectInviteResponse(status="success", message="User invited successfully to the project.")
    else:
        return ProjectInviteResponse(status="error", message="Project with the provided ID not found.")

@app.get("/API/v1/projects", response_model=ProjectListResponse)
def list_projects():
    return ProjectListResponse(status="success", data=projects_db)

@app.put("/API/v1/projects", response_model=UpdateProjectResponse)
def update_project(request: UpdateProjectRequest):
    for project in projects_db:
        if project.id == request.id:
            if request.name:
                project.name = request.name
            if request.key:
                project.key = request.key
            if request.type:
                project.type = request.type
            if request.lead:
                project.lead = request.lead
            project.updated_at = datetime.now()
            return UpdateProjectResponse(status="success", msg=f"Project with ID '{request.id}' updated successfully.")
    raise HTTPException(status_code=404, detail="Project not found")

@app.patch("/API/v1/projects/{project_id}/lastIssueUpdates", response_model=UpdateLastIssueResponse)
def update_last_issue(project_id: UUID, request: UpdateLastIssueRequest):
    for project in projects_db:
        if project.id == project_id:
            project.last_updated_issue = request.lastUpdatedIssue
            project.updated_at = datetime.now()
            return UpdateLastIssueResponse(status="success", message=f"Last updated issue for project with ID '{project_id}' updated successfully.")
    raise HTTPException(status_code=404, detail="Project not found")

@app.get("/API/v1/projects/{project_id}", response_model=ProjectDetailResponse)
def get_project_detail(project_id: UUID):
    for project in projects_db:
        if project.id == project_id:
            return ProjectDetailResponse(success=True, projects=project)
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/API/v1/projects", response_model=DeleteProjectResponse)
def delete_project(project_id: UUID):
    for project in projects_db:
        if project.id == project_id:
            projects_db.remove(project)
            return DeleteProjectResponse(status="success", msg="Project deleted successfully")
    raise HTTPException(status_code=404, detail="Project not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)