import os

from fastapi import FastAPI, Query
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import EmailStr, BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI()

# 加载环境变量
load_dotenv()

#如果用本地数据库做示例
projects_db = []
tasks_db = []
columns_db = []
history_db = []
current_order_id = 0  # global variable, used to keep track of the task order number. 全局变量，用于追踪任务顺序编号

# # 连接到MongoDB
# MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# client = AsyncIOMotorClient(MONGO_DB_URL)
# db = client.get_database("project")

router = APIRouter()


# Project management
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


# Task board management

#Columns

class Column(BaseModel):
    id: UUID
    name: str
    order: int  # 用于表示列的顺序
    tasks: List[UUID]  # 存储关联的任务ID列表

class Comment(BaseModel):
    id: UUID
    timestamp: datetime
    user_id: UUID
    initials: str
    comment: str

class History(BaseModel):
    id: UUID
    timestamp: datetime
    user_id: UUID
    initials: str
    event: str

class Action(BaseModel):
    id: UUID
    timestamp: datetime
    action_type: str
    details: dict

class Activity(BaseModel):
    comments: List[Comment]
    history: List[History]
    actions: List[Action]


class Task(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    total_order_id: int
    assignee: Optional[UUID] = None
    reporter: Optional[UUID] = None
    priority: str
    start_date: datetime
    due_date: datetime
    status_id: str
    created_at: datetime
    updated_at: datetime
    activity: Activity
    key: Optional[str] = None

class UpdateTaskRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    assignee: Optional[UUID] = None
    reporter: Optional[UUID] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status_id: Optional[str] = None

class UpdateTaskResponse(BaseModel):
    status: str
    msg: str
    task: Optional[Task] = None

class DeleteTaskResponse(BaseModel):
    status: str
    msg: str

class TaskLinkResponse(BaseModel):
    status: str
    link: str

class User(BaseModel):
    id: UUID
    full_name: str
    public_name: str
    initials: str
    email: EmailStr
    status: str
    last_active: datetime

    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    task_id: UUID
    history: List[dict]

# healthy check
@app.get("/health")
async def health_check():
    try:
        # 尝试从数据库获取数据
        await db.command("ping")
        return {"status": "success", "message": "Connected to MongoDB"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# project management

#for db test
# @app.post("/API/v1/projects", response_model=Project)
# async def create_project(request: ProjectCreateRequest):
#     project = {
#         "name": request.name,
#         "key": request.key,
#         "type": request.type,
#         "lead": request.lead,
#         "created_at": datetime.now(),
#         "updated_at": datetime.now(),
#     }
#     result = await db.projects.insert_one(project)
#     project["_id"] = str(result.inserted_id)
#     project["id"] = project["_id"]
#     return project


# project management

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
            return UpdateLastIssueResponse(status="success",
                                           message=f"Last updated issue for project with ID '{project_id}' updated successfully.")
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


class DeleteColumnResponse(BaseModel):
    status: str
    msg: str

# Task board management
#Columns
@app.post("/API/v1/columns", response_model=Column)
def create_column(name: str, order: int):
    new_column = Column(
        id=uuid4(),  # 生成新的唯一ID
        name=name,
        order=order,
        tasks=[]
    )
    columns_db.append(new_column)
    return new_column


@app.delete("/API/v1/columns/{column_id}", response_model=DeleteColumnResponse)
def delete_column(column_id: UUID, new_column_id: UUID):
    # 确保新列存在
    new_column = next((col for col in columns_db if col.id == new_column_id), None)
    if not new_column:
        raise HTTPException(status_code=404, detail="New column not found")

    # 找到并删除目标列
    column = next((col for col in columns_db if col.id == column_id), None)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    # 将任务转移到新列
    new_column.tasks.extend(column.tasks)

    # 删除列
    columns_db.remove(column)
    return DeleteColumnResponse(status="success", msg="Column deleted and tasks moved successfully")


@app.patch("/API/v1/columns/{column_id}", response_model=Column)
def rename_column(column_id: UUID, new_name: str):
    column = next((col for col in columns_db if col.id == column_id), None)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    column.name = new_name
    return column

@app.patch("/API/v1/columns/{column_id}/order", response_model=Column)
def update_column_order(column_id: UUID, new_order: int):
    column = next((col for col in columns_db if col.id == column_id), None)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    # 更新列的顺序
    column.order = new_order
    # 这里可以加入更多逻辑来重新排列其他列的顺序
    return column


# Tasks
#任务创建 (Create Task),获取任务 (Get Task),更新任务 (Update Task),删除任务 (Delete Task)
@app.post("/API/v1/tasks", response_model=Task)
def create_task(request: Task):
    global current_order_id
    current_order_id += 1  # 增加任务顺序编号
    new_task = Task(
        id=uuid4(),
        name=request.name,
        description=request.description,
        total_order_id=current_order_id,  # 赋值顺序编号
        assignee=request.assignee,
        reporter=request.reporter,
        priority=request.priority,
        start_date=request.start_date,
        due_date=request.due_date,
        status_id=request.status_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    projects_db.append(new_task)
    return new_task


@app.get("/API/v1/tasks", response_model=List[Task])
def list_tasks():
    return projects_db


@app.put("/API/v1/task/{task_id}", response_model=Task)
def update_task(task_id: UUID, update_task: UpdateTaskRequest):
    for task in tasks_db:
        if task.id == task_id:
            task.name = update_task.name or task.name
            task.description = update_task.description or task.description
            task.assignee = update_task.assignee or task.assignee
            task.reporter = update_task.reporter or task.reporter
            task.priority = update_task.priority or task.priority
            task.start_date = update_task.start_date or task.start_date
            task.due_date = update_task.due_date or task.due_date
            task.status_id = update_task.status_id or task.status_id
            task.updated_at = datetime.now()
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/API/v1/task/{task_id}", response_model=DeleteTaskResponse)
def delete_task(task_id: UUID):
    global tasks_db
    tasks_db = [task for task in tasks_db if task.id != task_id]
    return {"status": "success", "msg": "Task deleted successfully"}

# 获取任务详情
@app.get("/API/v1/tasks/{task_id}", response_model=Task)
def get_task_detail(task_id: UUID):
    for task in projects_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

#获取任务的 Assignee
@app.get("/API/v1/tasks/{task_id}/assignee", response_model=UUID)
def get_task_assignee(task_id: UUID):
    for task in tasks_db:
        if task.id == task_id:
            return task.assignee
    raise HTTPException(status_code=404, detail="Task not found")

#更新任务的状态栏 (Move Task to Another Column)
@app.patch("/API/v1/columns/{column_id}/tasks/{task_id}", response_model=Task)
def move_task_to_column(column_id: UUID, task_id: UUID):
    # 查找任务
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 查找目标列
    new_column = next((col for col in columns_db if col.id == column_id), None)
    if not new_column:
        raise HTTPException(status_code=404, detail="Column not found")

    # 从原列中移除任务
    for column in columns_db:
        if task_id in column.tasks:
            column.tasks.remove(task_id)

    # 添加任务到新列
    new_column.tasks.append(task_id)

    # 更新任务的 status_id
    task.status_id = str(column_id)
    task.updated_at = datetime.now()

    return task


# 删除任务卡片操作 Task card delete
@app.delete("/API/v1/tasks/{task_id}/actions", response_model=DeleteTaskResponse)
def delete_task_actions(task_id: UUID):
    # 逻辑代码来删除任务的操作
    return {"status": "success", "msg": "Task deleted successfully"}

#获取任务链接
@app.get("/API/v1/tasks/{task_id}/link", response_model=TaskLinkResponse)
def get_task_link(task_id: UUID):
    # 逻辑代码来生成任务链接
    link = f"https://localhost:8080/tasks/view/{task_id}"
    return TaskLinkResponse(status="success", link=link)

#get key and order of the task
@app.get("/API/v1/columns/{column_id}/tasks/{task_id}/key", response_model=dict)
def get_task_key(column_id: UUID, task_id: UUID):
    # 查找任务
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 生成 key：项目名称的首字母 + 任务的顺序编号
    project_initials = ''.join([word[0].upper() for word in task.project.name.split()])
    key = f"{project_initials}-{task.total_order_id}"

    return {"key": key}


# 获取任务链接 copy link
@app.get("/API/v1/tasks/{task_id}/link", response_model=TaskLinkResponse)
def get_task_link(task_id: UUID):
    link = f"https://localhost:8080/tasks/view/{task_id}"
    return TaskLinkResponse(status="success", link=link)

#search task
@app.get("/API/v1/tasks/search", response_model=List[dict])
def search_tasks(text: str = Query(..., description="Text to search in task names and descriptions")):
    matching_tasks = []
    for task in tasks_db:
        if (text.lower() in task["name"].lower()) or (text.lower() in task["description"].lower()):
            matching_tasks.append(task)
    if not matching_tasks:
        raise HTTPException(status_code=404, detail="No matching tasks found")
    return matching_tasks

# need improve Task 筛选 (Task Filter)
@app.get("/API/v1/tasks/filter", response_model=List[Task])
def filter_tasks(
        id: Optional[str] = Query(None, description="Task ID"),
        priority: Optional[str] = Query(None, description="Task priority"),
        assignee: Optional[str] = Query(None, description="Assignee ID"),
        reporter: Optional[str] = Query(None, description="Reporter ID"),
        status_id: Optional[str] = Query(None, description="Status ID")
):
    filtered_tasks = []

    for task in tasks_db:
        if id:
            try:
                if str(task.id) == id:
                    filtered_tasks.append(task)
                    continue
            except ValueError:
                raise HTTPException(status_code=422, detail=f"Invalid UUID format for id: {id}")
        if priority and task.priority == priority:
            filtered_tasks.append(task)
            continue
        if assignee:
            try:
                if str(task.assignee) == assignee:
                    filtered_tasks.append(task)
                    continue
            except ValueError:
                raise HTTPException(status_code=422, detail=f"Invalid UUID format for assignee: {assignee}")
        if reporter:
            try:
                if str(task.reporter) == reporter:
                    filtered_tasks.append(task)
                    continue
            except ValueError:
                raise HTTPException(status_code=422, detail=f"Invalid UUID format for reporter: {reporter}")
        if status_id and task.status_id == status_id:
            filtered_tasks.append(task)
            continue

    return filtered_tasks

# History api
@app.get("/API/v1/tasks/{task_id}/history", response_model=HistoryResponse)
def get_task_history(task_id: UUID):
    task = next((t for t in tasks_db if t['id'] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_history = [h for h in history_db if h['task_id'] == task_id]

    return {"task_id": task_id, "history": task_history}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
