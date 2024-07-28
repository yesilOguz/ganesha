import datetime
import math
import random

import pytest
from bson import ObjectId
from faker import Faker

from ganesha.collections import get_collection, Collections
from ganesha.user.models import UserRegisterModel, UserLoginModel, UserUpdateModel, UserOTPCreateModel, UserOTPModel, \
    UserRenewPassword
from ganesha.user.otp_types import OTP_TYPES

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


@pytest.fixture()
def OtpDBFactory():
    def generate_otp_code():
        OTP_COLLECTION = get_collection(Collections.OTP_COLLECTION)

        digits = "0123456789"
        otp = ''

        for i in range(6):
            otp += digits[math.floor(random.random() * 10)]

        check_otp_code_for_existence_collection = OTP_COLLECTION.find_one({'otp_code': otp})
        check_otp_code_for_existence = UserOTPModel.from_mongo(check_otp_code_for_existence_collection)

        if check_otp_code_for_existence:
            if check_otp_code_for_existence.end_time < datetime.datetime.now():
                OTP_COLLECTION.find_one_and_delete({'otp_code': otp})
            else:
                return generate_otp_code()

        return otp

    def _func(user_id: ObjectId, email: str):
        OTP_COLLECTION = get_collection(Collections.OTP_COLLECTION)

        now = datetime.datetime.now()
        OTP_CODE_EXPIRES_IN = datetime.timedelta(minutes=5)

        generated_code = generate_otp_code()
        new_otp = UserOTPCreateModel(requested_by=user_id,
                                     created_time=now,
                                     end_time=now + OTP_CODE_EXPIRES_IN,
                                     otp_code=generated_code,
                                     otp_type=OTP_TYPES.PASSWORD_RESET)

        OTP_COLLECTION.insert_one(new_otp.to_mongo())
        return new_otp

    return _func


@pytest.fixture()
def RenewPasswordFactory():
    def _func(password: str = faker.password()):
        return UserRenewPassword(password=password)
    return _func
