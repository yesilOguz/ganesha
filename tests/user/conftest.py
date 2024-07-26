import pytest
from faker import Faker

from ganesha.user.models import UserRegisterModel, UserLoginModel, UserUpdateModel

Faker.seed(3)
faker = Faker()


@pytest.fixture()
def UserRegisterFactory():
    def _func(full_name=faker.name(), email=faker.email(), password=faker.password(),
              country=faker.country(), city=faker.city()):
        register_model = UserRegisterModel(full_name=full_name, email=email, password=password,
                                           country=country, city=city)

        return register_model
    return _func


@pytest.fixture()
def UserLoginFactory():
    def _func(email: str, password: str):
        login_model = UserLoginModel(email=email, password=password)

        return login_model
    return _func


@pytest.fixture()
def UserUpdateFactory():
    def _func(full_name=faker.name(), email=faker.email()):
        update_model = UserUpdateModel(full_name=full_name, email=email)
        return update_model
    return _func
