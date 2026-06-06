from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class User_signup_schema(BaseModel):
    fullname: str
    email: EmailStr
    password : str
    token : Optional[str] 
    role : Optional[str]

class User_login_schema(BaseModel):
    email: EmailStr
    password : str