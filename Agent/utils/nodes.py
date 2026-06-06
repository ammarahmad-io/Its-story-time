from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
import json
from openai import OpenAI
import os
import sys
from decouple import config

# Ensure the Agent/.env file is loaded even when the app is started from outside the Agent folder.
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.state import State
from langchain_groq import ChatGroq



api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise RuntimeError('GROQ_API_KEY must be set in the environment or Agent/.env before creating ChatGroq')

llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key)
client = OpenAI(
    api_key=config('AGNES_API_KEY'),
    base_url='https://apihub.agnes-ai.com/v1'
)

def story_bot(state):
    print(f'Iside story_chatbot')
    response = llm.invoke(state.get('messages'))
    parsed = json.loads(response.content)
    return {'page_content':parsed.get('pages_content'),'page_image_prompts':parsed.get('page_image_prompts')}



def images_bot(state:State):
    image_prompts = state.get('page_image_prompts')
    images_url = []
    for prompt in image_prompts:
        response = client.images.generate(
            model='agnes-image-2.1-flash',
            prompt=prompt,
            size='1024x1024',
            n=1
        )
        image_data = response.data[0]
        images_url.append(image_data.url)
    return {'page_image_url':images_url}

graph_builder = StateGraph(State)
graph_builder.add_node('story_bot',story_bot)
graph_builder.add_node('images_bot',images_bot)

graph_builder.add_edge(START,'story_bot')
graph_builder.add_edge('story_bot','images_bot')
graph_builder.add_edge('images_bot',END)
graph = graph_builder.compile()
