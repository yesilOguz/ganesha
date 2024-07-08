from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Security, Body, UploadFile
from fastapi_jwt import JwtAuthorizationCredentials

from ganesha.auth.login_utilities import access_security
from ganesha.coach.models import process8hrModel, process8hrModelResponse
from ganesha.collections import get_collection, Collections
from ganesha.models import StatusResponse
from ganesha.core.gemini import GEMINI

import datetime

router = APIRouter()


@router.post('/process-8hr', status_code=status.HTTP_200_OK, response_model=process8hrModelResponse)
def process_8hr_data(audio_file: UploadFile, process8hr: process8hrModel = Body(...),
                     credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(credentials.subject['id'])
    chat = GEMINI.get_chat(user_id=user_id)

    audio_format = audio_file.filename.split('.')[-1]
    file_name = f'{datetime.datetime.now()} - {user_id}.{audio_format}'

    with open(file_name, 'wb') as f:
        f.write(audio_file.file.read())

    process = GEMINI.audio_file_prompt(chat=chat, text_prompt='summary', file_path=file_name)
    return process8hrModelResponse(response_from_coach=process.text)
