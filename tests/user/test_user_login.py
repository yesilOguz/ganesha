class TestUserLogin:
    def test_user_login(self, test_client, UserDBFactory, UserLoginFactory):
        user = UserDBFactory()
        user_login = UserLoginFactory(email=user.email, password=user.password)

        response = test_client.post('/user/login', json=user_login.to_json())

        assert response.status_code == 200
        assert response.json()['user']['id'] == str(user.id)

    def test_user_login_if_email_doesnt_match_with_email_pattern(self, test_client, UserDBFactory, UserLoginFactory):
        user = UserDBFactory()
        user_login = UserLoginFactory(email='invalid_email', password=user.password)

        response = test_client.post('/user/login', json=user_login.to_json())

        assert response.status_code == 400

    def test_user_login_if_password_is_wrong(self, test_client, UserDBFactory, UserLoginFactory):
        user = UserDBFactory()
        user_login = UserLoginFactory(email='mail@mail.com', password=user.password)

        response = test_client.post('/user/login', json=user_login.to_json())

        assert response.status_code == 403
