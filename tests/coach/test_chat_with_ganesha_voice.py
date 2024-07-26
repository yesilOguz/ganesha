class TestChatWithGaneshaVoice:
    def test_chat_with_ganesha_voice(self, test_client, UserDBFactory, CreateAudioFile, login):
        user = UserDBFactory()

        audio_file = CreateAudioFile
        audio_file.name = 'test_audio.mp3'
        model_name = 'man'

        login_header = login(user)

        files = {
            'audio_file': (audio_file.name, audio_file, 'audio/mpeg')
        }

        response = test_client.post(f'/coach/chat-with-voice/{model_name}', files=files, headers=login_header)

        assert response.status_code == 200

    def test_chat_with_ganesha_voice_if_there_is_no_model_with_that_name(self, test_client, UserDBFactory, CreateAudioFile, login):
        user = UserDBFactory()

        audio_file = CreateAudioFile
        audio_file.name = 'test_audio.mp3'
        model_name = 'there_is_no_model_with_this_name'

        login_header = login(user)

        files = {
            'audio_file': (audio_file.name, audio_file, 'audio/mpeg')
        }

        response = test_client.post(f'/coach/chat-with-voice/{model_name}', files=files, headers=login_header)

        assert response.status_code == 200
        