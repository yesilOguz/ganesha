import pytest
from faker import Faker
from fastapi.testclient import TestClient

from ganesha.auth.login_utilities import auth_user
from ganesha.auth.models import AuthResponse
from ganesha.collections import get_collection, Collections
from ganesha.core.mongo_database import MONGO
from ganesha.user.models import UserDBModel, UserRegisterModel
from ganesha.user.roles import UserRole
from main import app

Faker.seed(3)
faker = Faker()


@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as client:
        yield client
        MONGO.drop_database()


@pytest.fixture()
def GetHeaderFromAuthUser():
    def _func(authed_user: AuthResponse):
        access_token = authed_user.tokens.access_token
        return {'Authorization': f'Bearer {access_token}'}

    return _func


@pytest.fixture()
def GetRefreshHeaderFromAuthUser():
    def _func(authed_user: AuthResponse):
        refresh_token = authed_user.tokens.refresh_token

        return {'Authorization': f'Bearer {refresh_token}'}

    return _func


@pytest.fixture()
def login(GetHeaderFromAuthUser):
    def _func(user: UserDBModel):
        authed_user = auth_user(user)
        return GetHeaderFromAuthUser(authed_user)

    return _func


@pytest.fixture()
def UserDBFactory():
    def _func(full_name=faker.name(), email=None, password=faker.password(),
              country=faker.country(), city=faker.city(), role=UserRole.END_USER):
        if email is None:
            email = faker.email()
        register_model = UserRegisterModel(full_name=full_name, email=email, password=password,
                                           country=country, city=city, role=role)

        inserted = get_collection(Collections.USER_COLLECTION).insert_one(register_model.to_mongo())
        inserted_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'_id': inserted.inserted_id})
        inserted_user = UserDBModel.from_mongo(inserted_user_collection)

        return inserted_user

    return _func


