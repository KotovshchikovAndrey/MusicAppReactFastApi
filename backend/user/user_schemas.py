from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserAuthSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    id: int
    refresh_token: str
    user_id: int

    class Config:
        orm_mode = True
    
