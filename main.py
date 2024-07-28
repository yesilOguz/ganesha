import os

from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from ganesha.core.mongo_database import MONGO

from ganesha.user.routes import router as user_router
from ganesha.coach.routes import router as coach_router
from ganesha.character.routes import router as character_router
from ganesha.health.routes import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MONGO.check_connection():
        MONGO.reconnect()

    app.database = MONGO.get_db()

    yield

    MONGO.shut_down_db()


router = APIRouter()
app = FastAPI(lifespan=lifespan, docs_url=None)

app.mount('/static', StaticFiles(directory='web-page'), name='static')


@router.post('/', response_description='Hello', status_code=status.HTTP_200_OK, response_model=dict)
def main_path():
    return {'Ganesha': 'Key ?'}


@router.get('/', response_description='Hello', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def main_path():
    html_file_path = os.path.join("web-page", "index.html")
    with open(html_file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(user_router, prefix='/user')
app.include_router(coach_router, prefix='/coach')
app.include_router(character_router, prefix='/character')
app.include_router(health_router, prefix='/health')
