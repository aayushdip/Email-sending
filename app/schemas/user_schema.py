from pydantic import BaseModel


class UserCreate(BaseModel):
    fullname: str
    email: str
    password: str


class UserInDB(BaseModel):
    hashed_password: str

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id: int
    email: str
    fullname: str
    is_active: bool

    class Config:
        orm_mode = True
