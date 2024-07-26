from bson import ObjectId


class TestGetUser:
    def test_get_user(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        login_headers = login(user)
        response = test_client.get(f'/user/get-user/{user.id}', headers=login_headers)

        assert response.status_code == 200
        assert response.json()['id'] == str(user.id)

    def test_get_user_if_user_is_not_exist(self, test_client, UserDBFactory, login):
        user = UserDBFactory()
        user_id = ObjectId()

        login_header = login(user)
        response = test_client.get(f'/user/get-user/{user_id}', headers=login_header)

        assert response.status_code == 404
