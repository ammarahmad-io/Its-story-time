from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class Users_schema(BaseModel):
    fullname: str
    email: EmailStr
    password : str
    token : Optional[str] 
    role : Optional[str]