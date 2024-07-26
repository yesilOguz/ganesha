from fastapi import APIRouter, status, Security
from fastapi_jwt import JwtAuthorizationCredentials
from ganesha.auth.login_utilities import access_security
from ganesha.models import StatusResponse

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def check_server_health():
    return StatusResponse(status=True)


@router.get('/check-key', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def check_key_health(credentials: JwtAuthorizationCredentials = Security(access_security)):
    return StatusResponse(status=True)
