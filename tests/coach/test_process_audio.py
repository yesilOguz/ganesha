from io import BytesIO


class TestProcessAudio:
    def test_process_audio(self, test_client, UserDBFactory, CreateAudioFile, login):
        user = UserDBFactory()

        audio_file = CreateAudioFile
        audio_file.name = 'test_audio.mp3'

        login_header = login(user)

        files = {
            'audio_file': (audio_file.name, audio_file, 'audio/mpeg')
        }

        response = test_client.post('/coach/process-audio', files=files, headers=login_header)

        assert response.status_code == 200
        assert response.json()['response_from_coach'] != ''
