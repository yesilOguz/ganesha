class TestUpdateUser:
    def test_update_user(self, test_client, UserDBFactory, UserUpdateFactory, login):
        new_full_name = 'test'

        user = UserDBFactory()
        user_update = UserUpdateFactory(full_name=new_full_name)

        login_header = login(user)
        response = test_client.post('/user/update', json=user_update.to_json(), headers=login_header)

        assert response.status_code == 201
        assert response.json()['id'] == str(user.id)
        assert response.json()['full_name'] == new_full_name

    def test_update_user_if_some_fields_are_None(self, test_client, UserDBFactory, UserUpdateFactory, login):
        user = UserDBFactory()
        user_update = UserUpdateFactory(full_name=None, email=None)

        login_header = login(user)
        response = test_client.post('/user/update', json=user_update.to_json(), headers=login_header)

        assert response.status_code == 201
        assert response.json()['id'] == str(user.id)
        assert response.json()['full_name'] == user.full_name

    def test_update_users_email_with_exist_one(self, test_client, UserDBFactory, UserUpdateFactory, login):
        user = UserDBFactory()
        exist_user = UserDBFactory()
        user_update = UserUpdateFactory(email=exist_user.email)

        login_header = login(user)
        response = test_client.post('/user/update', json=user_update.to_json(), headers=login_header)

        assert response.status_code == 400
        assert user.email != exist_user.email
