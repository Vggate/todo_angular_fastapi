import os


import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


from todo_app.todo_api import todo_api
from base.models import Base
from base.database import engine
import config


# Set system timezone to UTC
os.environ['TZ'] = 'UTC'
root_router = APIRouter()

root_router.include_router(todo_api)


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(root_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run():
    uvicorn.run(app, host=config.server_interface, port=config.server_port)

if __name__ == "__main__":
    run()
