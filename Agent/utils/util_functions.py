import jwt
import os 
from decouple import config
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import session

secret = config('secret')
algorithm = config('algorithm')

def get_db():
    db = session() 
    try: 
        yield db
    finally:
        db.close()

def jwt_encoder(email:str):
    payload = {
        'user_id':email
    }
    token = jwt.encode(payload,secret,algorithm)
    return {'token': token}

def jwt_decoder(token:str):
    return jwt.decode(token,secret,algorithm)

print(jwt_decoder('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYW1tYXJAZXhhbXBsZS5jb20ifQ.yxrKRnGA81dtDkUFzOp_D5FcMHkFhJxf-xBqEk9r_dk'))


# client = OpenAI(
#     api_key='Fe7Ah5wjwIZsqmXb4gKJE71LkvbN1anwhO8cU41dkMaD5giK',
#     base_url='https://apihub.agnes-ai.com/v1'
# )

# response = client.images.generate(
#     model="agnes-image-2.1-flash",
#     prompt="Generate an image of cute 3 years old girl playing with toys",
#     size="1024x1024",
#     n=3
# )

# # Extract image data
# image_data = response.data[0]
# print(image_data.url)  # URL to the generated image