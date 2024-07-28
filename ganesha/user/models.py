from ganesha.core.GaneshaBaseModel import GaneshaBaseModel, ObjectIdPydanticAnnotation
from bson import ObjectId
from typing import Annotated, Optional

from ganesha.user.otp_types import OTP_TYPES
from ganesha.user.roles import UserRole

import datetime


class UserDBModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    password: str
    recognized_user: bool = False
    role: UserRole = UserRole.END_USER.value


class UserRegisterModel(GaneshaBaseModel):
    full_name: str
    email: str
    password: str
    role: UserRole = UserRole.END_USER.value


class UserLoginModel(GaneshaBaseModel):
    email: str
    password: str


class UserResponseModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    recognized_user: bool = False
    role: UserRole = UserRole.END_USER.value


class UserUpdateModel(GaneshaBaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None


class UserUpdateResponseModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    recognized_user: bool = False


class UserGetResponseModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    recognized_user: bool = False
    role: UserRole = UserRole.END_USER.value


class UserRenewPassword(GaneshaBaseModel):
    password: str


class UserOTPModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    requested_by: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    created_time: datetime.datetime
    end_time: datetime.datetime
    otp_code: str
    otp_type: OTP_TYPES


class UserOTPCreateModel(GaneshaBaseModel):
    requested_by: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    created_time: datetime.datetime
    end_time: datetime.datetime
    otp_code: str
    otp_type: OTP_TYPES


