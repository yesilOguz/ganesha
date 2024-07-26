import json

from google.generativeai import ChatSession
import google.generativeai as genai
import os


class Gemini:
    def __init__(self):
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest',
                                           system_instruction="""You are a personal life coach.
                                            And your name is Ganesha.
                                            your task is to monitor my life through sounds,
                                            comment on my life and help me improve my life. 
                                            In cases other than life coaching,
                                            you will respond by saying "this is not within my knowledge.".""")

    def get_chat(self, user_id: str):
        file_name = f'{user_id}-history.json'
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                return self.model.start_chat(history=json.load(file))

        return self.model.start_chat(history=[])

    def save_chat(self, user_id: str, chat: ChatSession):
        file_name = f'{user_id}-history.json'
        with open(file_name, 'w') as f:
            json.dump(chat.history, f)

    def list_models(self):
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)

        return models

    def audio_file_prompt(self, chat: ChatSession, text_prompt: str, file_path: str, file_name: str | None = None):
        if file_name is None:
            file_name = file_path

        audio_file = genai.upload_file(path=file_path,
                                       display_name=file_name,
                                       mime_type='audio/mp4')

        response = chat.send_message([audio_file, text_prompt])
        return response

    def text_prompt(self, chat: ChatSession, text_prompt: str):
        response = chat.send_message([text_prompt])
        return response


GEMINI = Gemini()
MODEL = GEMINI.model
