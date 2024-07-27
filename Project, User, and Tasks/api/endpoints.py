from fastapi import FastAPI, HTTPException, APIRouter, Request, Query, Body, UploadFile, File
from pydantic import EmailStr, BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID, uuid4
from fastapi.responses import JSONResponse
import logging
app = FastAPI()

projects_db = []
users_db = []
tasks_db = []
comments_db = []
history_db = []
actions_db = []
access_db = []
columns_db = []

router = APIRouter()

class User(BaseModel):
    id: UUID
    full_name: str
    public_name: str
    initials: str
    email: EmailStr
    status: str
    last_active: datetime

    class Config:
        orm_mode = True


class UserCreateRequest(BaseModel):
    full_name: str
    public_name: str
    initials: str
    email: EmailStr
    status: str

class UserInviteRequest(BaseModel):
    email: EmailStr
    projectId: int

class UserInviteResponse(BaseModel):
    status: str
    message: str
DEFAULT_ROLES = ["TaskAdmin", "ProjectAdmin"]

class UserRole(BaseModel):
    user_id: UUID
    roles: List[str]

    class Config:
        orm_mode = True

class UserRoleUpdateRequest(BaseModel):
    roles: List[str]

    @classmethod
    def validate_roles(cls, roles):
        for role in roles:
            if role not in DEFAULT_ROLES:
                raise ValueError(f"Invalid role: {role}. Allowed roles are {DEFAULT_ROLES}.")
        return roles

class UserRoleResponse(BaseModel):
    status: str
    data: UserRole


class UserListResponse(BaseModel):
    status: str
    data: List[User]

class UpdateLastActiveRequest(BaseModel):
    last_active: datetime

class UpdateLastActiveResponse(BaseModel):
    status: str
    msg: str

class Comment(BaseModel):
    id: UUID
    timestamp: datetime
    user_id: UUID
    initials: str
    comment: str

    class Config:
        orm_mode = True

class History(BaseModel):
    id: UUID
    timestamp: datetime
    user_id: UUID
    initials: str
    event: str

    class Config:
        orm_mode = True

class Attachment(BaseModel):
    id: UUID
    timestamp: datetime
    file_name: str

    class Config:
        orm_mode = True

class LinkedIssue(BaseModel):
    id: UUID
    timestamp: datetime
    link_id: UUID

    class Config:
        orm_mode = True

class Action(BaseModel):
    id: UUID
    action_type: str
    attachments: List[Attachment] = []
    linked_issues: List[LinkedIssue] = []

    class Config:
        orm_mode = True


class Activity(BaseModel):
    comments: List[Comment] = []
    history: List[History] = []
    actions: List[Action] = []

    class Config:
        orm_mode = True

class Task(BaseModel):
    id: UUID
    name: str
    description: str
    total_order_id: str
    assignee: UUID
    reporter: UUID
    priority: str
    start_date: datetime
    due_date: datetime
    status_id: str
    activity: Activity

    class Config:
        orm_mode = True


class TaskCreateRequest(BaseModel):
    name: str
    description: str
    total_order_id: str
    assignee: UUID
    reporter: UUID
    priority: str
    start_date: datetime
    due_date: datetime
    status_id: str

class TaskUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    total_order_id: Optional[str]
    assignee: Optional[UUID]
    reporter: Optional[UUID]
    priority: Optional[str]
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    status_id: Optional[str]
    column_id: Optional[str]

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

# Add global exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)},
    )


# Create User
@app.post("/user", response_model=User)
def create_user(request: UserCreateRequest):
    new_user = User(
        id=uuid4(),
        full_name=request.full_name,
        public_name=request.public_name,
        initials=request.initials,
        email=request.email,
        status=request.status,
        last_active=datetime.now()
    )
    users_db.append(new_user)
    return new_user

# Invite User
@app.post("/invitations", response_model=UserInviteResponse)
def invite_user(request: UserInviteRequest):
    # Here you would normally add code to handle the invitation logic, e.g., sending an email
    if request.email and request.projectId:  # Mock logic to check if user exists
        return UserInviteResponse(status="success", message="User invited successfully to the board.")
    else:
        return UserInviteResponse(status="error", message="User with the provided email not found.")

# List User Table
@app.get("/users", response_model=UserListResponse)
def list_users():
    return UserListResponse(status="success", data=users_db)

# Update Last Active Time
@app.patch("/users/{UserId}", response_model=UpdateLastActiveResponse)
def update_last_active(UserId: UUID, request: UpdateLastActiveRequest):
    for user in users_db:
        if user.id == UserId:
            user.last_active = request.last_active
            return UpdateLastActiveResponse(status="success", msg="Last active time updated successfully.")
    raise HTTPException(status_code=404, detail="User not found")

# Get User Detailed Name Card
@app.get("/user", response_model=User)
def get_user_detail(userId: UUID):
    for user in users_db:
        if user.id == userId:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Update user role
@router.put("/API/v1/access", response_model=UserRoleResponse)
def update_user_role(request: UserRoleUpdateRequest, user_id: UUID = Query(...)):
    for role in access_db:
        if role.user_id == user_id:
            role.roles = request.roles
            return UserRoleResponse(status="success", data=role)
    # 如果用户角色不存在，则创建一个新角色记录
    new_role = UserRole(user_id=user_id, roles=request.roles)
    access_db.append(new_role)
    return UserRoleResponse(status="success", data=new_role)

# Get User Role
@router.get("/API/v1/access", response_model=UserRoleResponse)
def get_user_role(user_id: UUID = Query(...)):
    for role in access_db:
        if role.user_id == user_id:
            return UserRoleResponse(status="success", data=role)
    raise HTTPException(status_code=404, detail="User role not found")

# Delete User Role
@router.delete("/API/v1/access", response_model=UserRoleResponse)
def delete_user_role(user_id: UUID = Query(...)):
    for role in access_db:
        if role.user_id == user_id:
            access_db.remove(role)
            return UserRoleResponse(status="success", data=role)
    raise HTTPException(status_code=404, detail="User role not found")


# Create Task
@router.post("/task", response_model=Task)
def create_task(request: TaskCreateRequest):
    new_task = Task(
        id=uuid4(),
        name=request.name,
        description=request.description,
        total_order_id=request.total_order_id,
        assignee=request.assignee,
        reporter=request.reporter,
        priority=request.priority,
        start_date=request.start_date,
        due_date=request.due_date,
        status_id=request.status_id,
        column_id=request.column_id,
        activity=Activity()
    )
    tasks_db.append(new_task)
    return new_task

# Get Task
@router.get("/API/v1/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update Task
@router.put("/API/v1/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, request: TaskUpdateRequest):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in request.dict(exclude_unset=True).items():
        setattr(task, key, value)
    return task

# Delete Task
@router.delete("/API/v1/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db.remove(task)
    return task

# 获取任务链接
@router.get("/API/v1/tasks/{task_id}/link", response_model=Dict[str, str])
def get_task_link(task_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    link = f"https://localhost:8080/tasks/view/{task_id}"
    return {"status": "success", "link": link}

# 获取任务详细信息
@router.get("/API/v1/tasks/{task_id}/details", response_model=Task)
def get_task_details(task_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/API/v1/tasks/{task_id}/details", response_model=Dict[str, str])
def update_task_details(task_id: UUID, request: TaskUpdateRequest):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in request.dict(exclude_unset=True).items():
        setattr(task, key, value)
    return {"status": "success", "msg": "Task updated successfully."}

@router.get("/API/v1/tasks/{task_id}/comments/{comment_id}", response_model=Comment)
def get_task_comment(task_id: UUID, comment_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    comment = next((c for c in task.activity.comments if c.id == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.post("/API/v1/tasks/{task_id}/comments", response_model=Dict[str, str])
def add_task_comment(task_id: UUID, request: Comment):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    new_comment = Comment(
        id=uuid4(),
        timestamp=datetime.now(),
        user_id=request.user_id,
        initials=request.initials,
        comment=request.comment
    )
    task.activity.comments.append(new_comment)
    return {"status": "success", "msg": "Comment added successfully.", "comment": new_comment}

@router.delete("/API/v1/tasks/{task_id}/comments", response_model=Dict[str, str])
def delete_task_comment(task_id: UUID, comment_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    comment = next((c for c in task.activity.comments if c.id == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    task.activity.comments.remove(comment)
    return {"status": "success", "msg": "Comment deleted successfully."}

@router.get("/API/v1/tasks/{task_id}/history", response_model=Dict[str, List[History]])
def get_task_history(task_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "history": task.activity.history}

@router.post("/API/v1/tasks/{task_id}/attachments", response_model=Dict[str, str])
def add_task_attachment(task_id: UUID, file: UploadFile = File(...)):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    attachment_id = uuid4()
    attachment_url = f"https://localhost:8080/path/to/file/{file.filename}"
    # 这里可以添加实际文件保存逻辑
    return {
        "status": "success",
        "msg": "File attached successfully.",
        "attached_file": {
            "task_id": task_id,
            "file_id": attachment_id,
            "filename": file.filename,
            "url": attachment_url
        }
    }

@router.delete("/API/v1/tasks/{task_id}/attachments", response_model=Dict[str, str])
def delete_task_attachment(task_id: UUID, file_id: UUID):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # 这里可以添加实际文件删除逻辑
    return {"status": "success", "msg": "File deleted successfully."}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)