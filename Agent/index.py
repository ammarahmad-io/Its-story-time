from fastapi import FastAPI,Depends
import uvicorn
from schemas.db_user_schemas import User_signup_schema,User_login_schema
from utils.util_functions import get_db
from sqlalchemy.orm import Session
from db.database_models import Users
from utils.util_functions import jwt_encoder
from db.bearer import get_current_user
from utils.nodes import graph
from schemas.state import State
from Prompts.system import STORY_SYSTEM_PROMT


app = FastAPI()

@app.get('/get_users')
def signup(db:Session = Depends(get_db)):
    users = db.query(Users).all()
    return users

@app.post('/signup')
def signup(user:User_signup_schema,db:Session = Depends(get_db)):
    db.add(Users(**user.model_dump()))
    db.commit()
    return {'hello','user added'}

@app.post('/login')
def login(user:User_login_schema,db:Session= Depends(get_db)):
    user = db.query(Users).filter(Users.email == user.email).first()
    if user:
        return jwt_encoder(user.email)
    return 'User not found'

@app.post('/generate_story')
def generate_story(prompt:str,user: dict = Depends(get_current_user)):
    updated_state = graph.invoke(State(messages=[
    {'role':'system','content':STORY_SYSTEM_PROMT},
    {'role':'user','content':prompt}
    ]))
    state = {
        'page_content':updated_state.get('page_content'),
        'page_image_prompts':updated_state.get('page_image_prompts'),
        'page_image_url':updated_state.get('page_image_url')
    }
    return state

if __name__ =='__main__':
    uvicorn.run('index:app',port=8000,reload=True)


'My daughter Maya, age 7, mood brave. She is scared of the dark.'

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYW1tYXJAZXhhbXBsZS5jb20ifQ.yxrKRnGA81dtDkUFzOp_D5FcMHkFhJxf-xBqEk9r_dk"
}






# print(updated_state.get('page_content'))
# print('\n',updated_state.get('page_image_prompts'))
# print('\n',updated_state.get('page_image_url'))
# # state_content = [msg.content for msg in updated_state.get('messages') if isinstance(msg,AIMessage)]
# # print(state_content)