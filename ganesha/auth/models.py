from ganesha.core.GaneshaBaseModel import GaneshaBaseModel
from ganesha.user.models import UserResponseModel


class AuthTokens(GaneshaBaseModel):
    access_token: str
    refresh_token: str


class AuthResponse(GaneshaBaseModel):
    user: UserResponseModel
    tokens: AuthTokens


class RefreshResponse(GaneshaBaseModel):
    access_token: str
    refresh_token: str
