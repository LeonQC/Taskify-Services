from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import EmailStr, BaseModel
from typing import List
from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI()

users_db = []

router = APIRouter()

class User(BaseModel):
    id: UUID
    full_name: str
    public_name: str
    initials: str
    email: EmailStr
    status: str
    last_active: datetime

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

class UserListResponse(BaseModel):
    status: str
    data: List[User]

class UpdateLastActiveRequest(BaseModel):
    last_active: datetime

class UpdateLastActiveResponse(BaseModel):
    status: str
    msg: str

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

