from bson import ObjectId


class TestDeleteUser:
    def test_delete_user(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        login_header = login(user)
        response = test_client.get(f'/user/delete-user/{user.id}', headers=login_header)

        assert response.status_code == 200
        assert response.json()['status'] is True

    def test_delete_user_if_user_is_not_exist(self, test_client, UserDBFactory, login):
        user = UserDBFactory()
        fake_user_id = ObjectId()

        login_header = login(user)
        response = test_client.get(f'/user/delete-user/{fake_user_id}', headers=login_header)

        assert response.status_code == 200
        assert response.json()['status'] is False

