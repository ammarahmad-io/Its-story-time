from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import Depends
from sqlalchemy.orm import Session
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.util_functions import get_db,jwt_decoder
from db.database_models import Users

security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session= Depends(get_db)):
    token = credentials.credentials
    decoded = jwt_decoder(token)
    email = decoded.get('user_id')

    if email:
        try:
            user = db.query(Users).filter(Users.email == email).first()
            return user
        except Exception as e:
            return e

    return 'Token expired or fake email credentials'