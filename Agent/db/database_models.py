from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
from typing import Optional

base = declarative_base()

class Users(base):
    __tablename__ = 'Users'

    fullname = Column(String)
    email = Column(String,index=True,primary_key=True)
    password = Column(String)
    token = Column(String,default=None)
    role = Column(String,default=None)