from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None
    is_active: bool

    class Config:
        from_attributes = True





"""
1. UserCreate
Validates incoming registration data
# When a user registers, they send JSON:
{
    "email": "alice@example.com",
    "password": "secret123",
    "full_name": "Alice Johnson"
}

# Pydantic automatically:
# 1. Validates email format 
# 2. Converts to Python object
# 3. Raises error if invalid



2. UserLogin
Validates login credentials 


3. UserOut
Enforces Response in the exact format defined 

"""