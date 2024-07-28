import datetime
import math
import re
import random
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Security, Body
from fastapi_jwt import JwtAuthorizationCredentials

from ganesha.auth.login_utilities import access_security, refresh_security, refresh
from ganesha.auth.login_utilities import auth_user
from ganesha.auth.models import AuthResponse, RefreshResponse
from ganesha.collections import get_collection, Collections
from ganesha.core.GaneshaBaseModel import ObjectIdPydanticAnnotation
from ganesha.core.email_service import EmailService
from ganesha.models import StatusResponse
from ganesha.patterns import Patterns
from ganesha.user.models import UserLoginModel, UserDBModel, UserRegisterModel, \
    UserUpdateResponseModel, UserUpdateModel, UserGetResponseModel, UserOTPModel, UserOTPCreateModel, UserRenewPassword
from ganesha.user.otp_types import OTP_TYPES

router = APIRouter()

OTP_CODE_EXPIRES_IN = datetime.timedelta(minutes=5)


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


@router.post('/login', status_code=status.HTTP_200_OK, response_model=AuthResponse)
def login_user(user: UserLoginModel = Body(...)):
    if not re.match(Patterns.EMAIL.value, user.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='email is not correct')

    get_db_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'email': user.email,
                                                                                   'password': user.password})
    get_db_user = UserDBModel.from_mongo(get_db_user_collection)

    if not get_db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='email or password is wrong')

    return auth_user(get_db_user)


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
def register_user(user: UserRegisterModel = Body(...)):
    if not re.match(Patterns.EMAIL.value, user.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='email is not correct')

    check_user_for_email = get_collection(Collections.USER_COLLECTION).find_one({'email': user.email})

    if check_user_for_email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='there is an user with this email.')

    inserted = get_collection(Collections.USER_COLLECTION).insert_one(user.to_mongo())

    get_inserted_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'_id': inserted.inserted_id})
    get_inserted_user = UserDBModel.from_mongo(get_inserted_user_collection)

    return auth_user(get_inserted_user)


@router.get('/refresh-token', status_code=status.HTTP_200_OK, response_model=RefreshResponse)
def refresh_token(credentials: JwtAuthorizationCredentials = Security(refresh_security)):
    return refresh(credentials.subject)


@router.post('/update', status_code=status.HTTP_201_CREATED, response_model=UserUpdateResponseModel)
def update_user(user: UserUpdateModel = Body(...),
                credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(credentials.subject['id'])

    if user.email:
        db_check_user_for_email = get_collection(Collections.USER_COLLECTION).find_one({'email': user.email})

        if db_check_user_for_email:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail='there is an user with this email')

    get_collection(Collections.USER_COLLECTION).find_one_and_update(filter={'_id': user_id},
                                                                    update={'$set': user.to_mongo(exclude_none=True)})

    updated_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'_id': user_id})
    updated_user = UserUpdateResponseModel.from_mongo(updated_user_collection)

    return updated_user


@router.get('/get-user/{user_id}', status_code=status.HTTP_200_OK, response_model=UserGetResponseModel)
def get_user(user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
             credentials: JwtAuthorizationCredentials = Security(access_security)):
    wanted_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'_id': user_id})
    wanted_user = UserGetResponseModel.from_mongo(wanted_user_collection)

    if not wanted_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='there is no user with this id')

    return wanted_user


@router.get('/send-forgot-otp/{email}', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def send_forgot_otp(email: str):
    if not re.match(Patterns.EMAIL.value, email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='email is not correct')

    USER_COLLECTION = get_collection(Collections.USER_COLLECTION)
    OTP_COLLECTION = get_collection(Collections.OTP_COLLECTION)

    check_email_collection = USER_COLLECTION.find_one({'email': email})
    check_email = UserDBModel.from_mongo(check_email_collection)

    if not check_email:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='there is no user with this email')

    now = datetime.datetime.now()

    generated_code = generate_otp_code()
    new_otp = UserOTPCreateModel(requested_by=check_email.id,
                                 created_time=now,
                                 end_time=now + OTP_CODE_EXPIRES_IN,
                                 otp_code=generated_code,
                                 otp_type=OTP_TYPES.PASSWORD_RESET)

    OTP_COLLECTION.insert_one(new_otp.to_mongo())
    try_send_mail = EmailService.send_email(email, EmailService.generate_otp_content(generated_code, new_otp.otp_type))

    return StatusResponse(status=try_send_mail)


@router.get('/check-otp/{email}/{otp_code}', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def check_otp(email: str, otp_code: str):
    if not re.match(Patterns.EMAIL.value, email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='email is not correct')

    USER_COLLECTION = get_collection(Collections.USER_COLLECTION)
    OTP_COLLECTION = get_collection(Collections.OTP_COLLECTION)

    check_email_collection = USER_COLLECTION.find_one({'email': email})
    check_email = UserDBModel.from_mongo(check_email_collection)

    if not check_email:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='there is no user with this email')

    check_otp_correction_collection = OTP_COLLECTION.find_one({'requested_by': check_email.id, 'otp_code': otp_code})
    check_otp_correction = UserOTPModel.from_mongo(check_otp_correction_collection)

    if not check_otp_correction or check_otp_correction.end_time < datetime.datetime.now():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='otp is invalid')

    return StatusResponse(status=True)


@router.post('/renew-password/{email}/{otp_code}', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def renew_password(email: str, otp_code: str, user_renew_password: UserRenewPassword = Body(...)):
    if not re.match(Patterns.EMAIL.value, email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='email is not correct')

    USER_COLLECTION = get_collection(Collections.USER_COLLECTION)
    OTP_COLLECTION = get_collection(Collections.OTP_COLLECTION)

    check_email_collection = USER_COLLECTION.find_one({'email': email})
    check_email = UserDBModel.from_mongo(check_email_collection)

    if not check_email:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='there is no user with this email')

    check_otp_correction_collection = OTP_COLLECTION.find_one({'requested_by': check_email.id, 'otp_code': otp_code})
    check_otp_correction = UserOTPModel.from_mongo(check_otp_correction_collection)

    if not check_otp_correction or check_otp_correction.end_time < datetime.datetime.now():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='otp is invalid')

    check_email.password = user_renew_password.password
    USER_COLLECTION.find_one_and_update(filter={'_id': check_email.id},
                                        update={'$set': check_email.to_mongo()})

    OTP_COLLECTION.find_one_and_delete({'_id': check_otp_correction.id})

    return StatusResponse(status=True)


@router.get('/delete-user/{user_id}', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def delete_user(user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
                credentials: JwtAuthorizationCredentials = Security(access_security)):
    deleted = get_collection(Collections.USER_COLLECTION).find_one_and_delete({'_id': user_id})

    return StatusResponse(status=deleted is not None)
