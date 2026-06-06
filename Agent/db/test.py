from fastapi import FastAPI,Depends
import uvicorn
from database_models import base
from database import engine,session
from database_models import Users
from schemas import Users_schema
from sqlalchemy.orm import Session

app = FastAPI()
base.metadata.create_all(bind=engine)

def get_db():
    db = session() 

    try: 
        yield db
    finally:
        db.close()

@app.post('/post')
def post(user:Users_schema, db : Session= Depends(get_db)):
    db.add(Users(**user))
