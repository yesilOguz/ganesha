from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Security, Body
from fastapi_jwt import JwtAuthorizationCredentials

from ganesha.auth.models import AuthResponse, RefreshResponse
from ganesha.core.validator import validate_object_id

from ganesha.auth.login_utilities import access_security, refresh_security, refresh
from ganesha.models import StatusResponse
from ganesha.auth.login_utilities import auth_user
from ganesha.user.models import UserLoginModel, UserDBModel, UserRegisterModel, \
    UserUpdateResponseModel, UserUpdateModel, UserGetResponseModel
from ganesha.collections import get_collection, Collections

router = APIRouter()


@router.post('/login', status_code=status.HTTP_200_OK, response_model=AuthResponse)
def login_user(user: UserLoginModel = Body(...)):
    get_db_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'email': user.email,
                                                                                   'password': user.password})
    get_db_user = UserDBModel.from_mongo(get_db_user_collection)

    if not get_db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='email or password is wrong')

    return auth_user(get_db_user)


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
def register_user(user: UserRegisterModel = Body(...)):
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


@router.get('/get-user/{user_id_param}', status_code=status.HTTP_200_OK, response_model=UserGetResponseModel)
@validate_object_id('user_id_param')
def get_user(user_id_param: str,
             credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(user_id_param)
    wanted_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'_id': user_id})
    wanted_user = UserGetResponseModel.from_mongo(wanted_user_collection)

    if not wanted_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='there is no user with this id')

    return wanted_user


@router.get('/delete-user/{user_id_param}', status_code=status.HTTP_200_OK, response_model=StatusResponse)
@validate_object_id('user_id_param')
def delete_user(user_id_param: str,
                credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(user_id_param)
    get_collection(Collections.USER_COLLECTION).find_one_and_delete({'_id': user_id})

    return StatusResponse(status=True)
