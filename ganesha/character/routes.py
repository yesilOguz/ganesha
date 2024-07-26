import os
from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Security, File, UploadFile, Body, Form
from fastapi.responses import FileResponse

from fastapi_jwt import JwtAuthorizationCredentials

from ganesha.auth.login_utilities import access_security
from ganesha.character.models import CharacterGetModelListResponse, CharacterGetCameraSettingsResponse, \
    CharacterGetCameraSettings
import glob
from pathlib import Path

from ganesha.collections import get_collection, Collections
from ganesha.models import StatusResponse
from ganesha.user.roles import UserRole

router = APIRouter()

main_path = './models/'


def get_model_list():
    model_list = glob.glob(f'{main_path}*.glb')
    models = [Path(e).stem for e in model_list]

    return model_list, models


@router.get('/get-model-list', status_code=status.HTTP_200_OK, response_model=CharacterGetModelListResponse)
def get_models(credentials: JwtAuthorizationCredentials = Security(access_security)):
    _, models = get_model_list()
    return CharacterGetModelListResponse(characters=models)


@router.get('/get-model/{model_name}', status_code=status.HTTP_200_OK, response_class=FileResponse)
def get_model(model_name: str):
    _, models = get_model_list()

    if model_name not in models:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='there is no model with this name')

    return FileResponse(f'{main_path}{model_name}.glb')


@router.get('/get-model-camera-settings/{model_name}', status_code=status.HTTP_200_OK,
            response_model=CharacterGetCameraSettingsResponse)
def get_camera_settings(model_name: str,
                        credentials: JwtAuthorizationCredentials = Security(access_security)):
    camera_settings_collection = get_collection(Collections.CAMERA_SETTINGS_COLLECTION).find_one(
        {'object_name': model_name})

    if not camera_settings_collection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='there is no settings with this model name ( you can use default camera settings )')

    settings = CharacterGetCameraSettingsResponse.from_mongo(camera_settings_collection)
    return settings


@router.post('/save-model', status_code=status.HTTP_201_CREATED, response_model=CharacterGetCameraSettingsResponse)
def save_model(camera_settings: str = Form(...), object_file: UploadFile = File(...),
               credentials: JwtAuthorizationCredentials = Security(access_security)):
    if credentials.subject['role'] == UserRole.END_USER.value:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail='you are not allowed to do this')

    try:
        camera_settings = CharacterGetCameraSettings.parse_raw(camera_settings)
    except Exception:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='camera_settings are not processable')

    _, models = get_model_list()

    if camera_settings.object_name in models:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='model name is already exists')

    with open(f'{main_path}{camera_settings.object_name}.glb', 'wb') as f:
        f.write(object_file.file.read())

    inserted_camera_settings = get_collection(Collections.CAMERA_SETTINGS_COLLECTION).insert_one(
        camera_settings.to_mongo())
    inserted_collection = get_collection(Collections.CAMERA_SETTINGS_COLLECTION).find_one(
        {'_id': inserted_camera_settings.inserted_id})
    inserted = CharacterGetCameraSettings.from_mongo(inserted_collection)

    return inserted


@router.get('/remove-model/{object_name}', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def remove_model(object_name: str,
                 credentials: JwtAuthorizationCredentials = Security(access_security)):
    if credentials.subject['role'] == UserRole.END_USER.value:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail='you are not allowed to do this')

    _, models = get_model_list()

    if object_name not in models:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='there is no model with this name')

    file_path = f'{main_path}{object_name}.glb'
    os.remove(file_path)

    get_collection(Collections.CAMERA_SETTINGS_COLLECTION).find_one_and_delete({'object_name': object_name})

    return StatusResponse(status=True)
