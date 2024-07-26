from ganesha.auth.models import AuthResponse


class TestUserRegister:
    def test_user_register(self, test_client, UserRegisterFactory):
        user_register = UserRegisterFactory()

        response = test_client.post('/user/register', json=user_register.to_json())

        assert response.status_code == 201

        registered_user = AuthResponse.from_mongo(response.json())

        assert registered_user.user.email == user_register.email
        assert registered_user.tokens.access_token is not None

    def test_user_register_if_email_is_registered(self, test_client, UserDBFactory, UserRegisterFactory):
        user = UserDBFactory()
        user_register = UserRegisterFactory(email=user.email)

        response = test_client.post('/user/register', json=user_register.to_json())

        assert response.status_code == 400

    def test_user_register_if_some_fields_missing(self, test_client, UserRegisterFactory):
        user_register = UserRegisterFactory()
        user_register.email = None

        response = test_client.post('/user/register', json=user_register.to_json())

        assert response.status_code == 422

    def test_user_register_if_email_format_is_not_valid(self, test_client, UserRegisterFactory):
        user_register = UserRegisterFactory(email='example')

        response = test_client.post('/user/register', json=user_register.to_json())

        assert response.status_code == 400
