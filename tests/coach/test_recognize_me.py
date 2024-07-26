class TestRecognizeMe:
    def test_recognize_me(self, test_client, UserDBFactory, CreateAudioFile, login):
        user = UserDBFactory()

        audio_file = CreateAudioFile
        audio_file.name = 'test_audio.mp3'

        login_header = login(user)

        files = {
            'audio_file': (audio_file.name, audio_file, 'audio/mpeg')
        }

        response = test_client.post(f'/coach/recognize-me', files=files, headers=login_header)
        
        assert response.status_code == 200
        assert response.json()['status'] is True
        