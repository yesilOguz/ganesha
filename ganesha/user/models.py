from ganesha.core.GaneshaBaseModel import GaneshaBaseModel, ObjectIdPydanticAnnotation
from bson import ObjectId
from typing import Annotated, Optional


class UserDBModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    password: str
    country: str
    city: str


class UserRegisterModel(GaneshaBaseModel):
    full_name: str
    email: str
    password: str
    country: str
    city: str


class UserLoginModel(GaneshaBaseModel):
    email: str
    password: str


class UserResponseModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    country: str
    city: str


class UserUpdateModel(GaneshaBaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


class UserUpdateResponseModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    country: str
    city: str


class UserGetResponseModel(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    full_name: str
    email: str
    country: str
    city: str
