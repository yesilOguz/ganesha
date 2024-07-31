from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Security, Body, UploadFile, File
from fastapi.responses import FileResponse
from fastapi_jwt import JwtAuthorizationCredentials

from ganesha.auth.login_utilities import access_security
from ganesha.coach.models import processAudioModelResponse
from ganesha.collections import get_collection, Collections
from ganesha.models import StatusResponse
from ganesha.core.gemini import GEMINI

from pyt2s.services import stream_elements

import datetime

from ganesha.user.models import UserDBModel

router = APIRouter()


def get_voice(text: str, user_id: str, selected_model: str):
    voice = stream_elements.Voice.Brian.value
    if selected_model == 'man':
        voice = stream_elements.Voice.Brian.value
    elif selected_model == 'batman':
        voice = stream_elements.Voice.Geraint.value
    elif selected_model == 'scout-girl':
        voice = stream_elements.Voice.Mia.value
    elif selected_model == 'real-man':
        voice = stream_elements.Voice.en_GB_Wavenet_B.value
    elif selected_model == 'steve':
        voice = stream_elements.Voice.Matthew.value
    elif selected_model == 'trump':
        voice = stream_elements.Voice.Russell.value

    voice_data = stream_elements.requestTTS(text, voice)
    file_name = f'records/{datetime.datetime.now()} - response-for-{user_id}.mp3'

    with open(file_name, 'wb+') as f:
        f.write(voice_data)

    return file_name


@router.post('/process-audio', status_code=status.HTTP_200_OK, response_model=processAudioModelResponse)
def process_audio_data(audio_file: UploadFile = File(...),
                       credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(credentials.subject['id'])
    chat = GEMINI.get_chat(user_id=user_id)

    audio_format = audio_file.filename.split('.')[-1]
    file_name = f'records/{datetime.datetime.now()} - {user_id}.{audio_format}'

    with open(file_name, 'wb') as f:
        f.write(audio_file.file.read())

    process = GEMINI.audio_file_prompt(chat=chat, text_prompt='', file_path=file_name)
    GEMINI.save_chat(user_id=user_id, chat=chat)

    return processAudioModelResponse(response_from_coach=process.text)


@router.get('/get-daily/{selected_model}', status_code=status.HTTP_200_OK, response_class=FileResponse)
def get_daily_advice(selected_model: str, credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(credentials.subject['id'])
    chat = GEMINI.get_chat(user_id=user_id)

    advice = GEMINI.text_prompt(chat, """Based on all the answers you have sent to me since my last question, I would like you to give me some suggestions for improving my daily life and personal development. Here are the topics I'm curious about:
                                    Daily Recommendations:
                                    What activities can I do to improve or maintain my mood? For example: Meditation, nature walks, spending time with my hobbies.
                                    What are practical advice for managing stress and anxiety?
                                    Social relations:
                                    What steps can I take to improve my interactions with certain people? How can I improve my communication skills? What are your suggestions on empathy?
                                    What are the strategies that will help me establish healthier relationships with my social environment?
                                    General Well-Being:
                                    What general recommendations should I follow for my physical and mental health? For example: Regular exercise, healthy nutrition, adequate sleep.
                                    What do you suggest about resources and activities that will contribute to my personal development?
                                    Friend Relationships:
                                    How can I make my relationships with my friends healthier? What suggestions do you have to help me build supportive and positive relationships?
                                    Please share your analysis and suggestions on these topics, using my conversations recorded throughout the day as a reference. Write them as plain text, spoken text, not as categories. Thanks.""")

    file_name = get_voice(advice.text, str(user_id), selected_model)

    GEMINI.save_chat(user_id=user_id, chat=chat)

    return FileResponse(file_name)


@router.get('/chat/{selected_model}/{text}', status_code=status.HTTP_200_OK, response_class=FileResponse)
def chat_with_ganesha(selected_model: str, text: str,
                      credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(credentials.subject['id'])
    chat = GEMINI.get_chat(user_id=user_id)

    response_from_ganesha = GEMINI.text_prompt(chat, text)

    file_name = get_voice(response_from_ganesha.text, str(user_id), selected_model)
    GEMINI.save_chat(user_id=user_id, chat=chat)
    return FileResponse(file_name)


@router.post('/chat-with-voice/{selected_model}', status_code=status.HTTP_200_OK, response_class=FileResponse)
def chat_with_ganesha_with_voice(selected_model: str, audio_file: UploadFile = File(...),
                                 credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(credentials.subject['id'])
    chat = GEMINI.get_chat(user_id=user_id)

    audio_format = audio_file.filename.split('.')[-1]
    file_name = f'records/{datetime.datetime.now()} - {user_id}-chat-ganesha.{audio_format}'

    with open(file_name, 'wb') as f:
        f.write(audio_file.file.read())

    response_from_ganesha = GEMINI.audio_file_prompt(chat=chat, text_prompt='', file_path=file_name)

    file_name = get_voice(response_from_ganesha.text, str(user_id), selected_model)
    GEMINI.save_chat(user_id=user_id, chat=chat)
    return FileResponse(file_name)


@router.post('/recognize-me', status_code=status.HTTP_200_OK, response_model=StatusResponse)
def recognize_me(audio_file: UploadFile = File(...),
                 credentials: JwtAuthorizationCredentials = Security(access_security)):
    user_id = ObjectId(credentials.subject['id'])
    chat = GEMINI.get_chat(user_id=user_id)

    user_collection = get_collection(Collections.USER_COLLECTION).find_one({'_id': user_id})
    user = UserDBModel.from_mongo(user_collection)

    audio_format = audio_file.filename.split('.')[-1]
    file_name = f'records/{datetime.datetime.now()} - {user_id}-recognize.{audio_format}'

    with open(file_name, 'wb') as f:
        f.write(audio_file.file.read())

    process = GEMINI.audio_file_prompt(chat=chat, text_prompt=f"Hey Ganesha that's my voice and I'm {user.full_name}",
                                       file_path=file_name)

    user.recognized_user = True
    get_collection(Collections.USER_COLLECTION).find_one_and_update(filter={'_id': user.id},
                                                                    update={'$set': user.to_mongo(exclude_unset=False)})

    GEMINI.save_chat(user_id=user_id, chat=chat)

    return StatusResponse(status=True)
