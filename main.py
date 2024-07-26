from fastapi import APIRouter, status
from fastapi import FastAPI
from faker import Faker
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from ganesha.core.mongo_database import MONGO

from ganesha.user.routes import router as user_router
from ganesha.coach.routes import router as coach_router
from ganesha.character.routes import router as character_router
from ganesha.health.routes import router as health_router

router = APIRouter()
fake = Faker()


@router.get('/', response_description='Hello', status_code=status.HTTP_200_OK, response_model=dict)
def main_path():
    return {'Ganesha': 'Key ?'}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MONGO.check_connection():
        MONGO.reconnect()

    app.database = MONGO.get_db()

    yield

    MONGO.shut_down_db()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

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
