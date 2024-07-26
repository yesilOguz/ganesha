from datetime import timedelta
import os

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from ganesha.auth.models import AuthResponse, AuthTokens, RefreshResponse
from ganesha.collections import get_collection, Collections
from ganesha.user.models import UserResponseModel, UserDBModel

SECRET = os.getenv("SECRET")
access_security = JwtAccessBearer(secret_key=SECRET, auto_error=True, access_expires_delta=timedelta(weeks=1))
refresh_security = JwtRefreshBearer(secret_key=SECRET, auto_error=True)


def auth_user(user: UserDBModel):
    subject = {'id': str(user.id), 'role': user.role}

    authed_user_collection = get_collection(Collections.USER_COLLECTION).find_one({'_id': user.id})
    authed_user = UserResponseModel.from_mongo(authed_user_collection)

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    tokens = AuthTokens(access_token=access_token, refresh_token=refresh_token)
    return AuthResponse(user=authed_user, tokens=tokens)


def refresh(subject):
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return RefreshResponse(access_token=access_token, refresh_token=refresh_token)
