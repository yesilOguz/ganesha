class TestChatWithGanesha:
    def test_chat_with_ganesha(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        test_text = 'hi ganesha! how are you today?'
        model_name = 'man'
        login_header = login(user)

        response = test_client.get(f'/coach/chat/{model_name}/{test_text}', headers=login_header)

        assert response.status_code == 200

    def test_chat_with_ganesha_if_there_is_no_model_with_that_name(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        test_text = 'hi ganesha! how are you today?'
        model_name = 'there_is_no_model_with_that_name'
        login_header = login(user)

        response = test_client.get(f'/coach/chat/{model_name}/{test_text}', headers=login_header)

        assert response.status_code == 200
