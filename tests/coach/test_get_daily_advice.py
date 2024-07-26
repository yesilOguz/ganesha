class TestGetDailyAdvice:
    def test_get_daily_advice(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        model_name = 'man'
        login_header = login(user)

        response = test_client.get(f'/coach/get-daily/{model_name}', headers=login_header)

        assert response.status_code == 200

    def test_get_daily_advice_if_there_is_no_model_with_that_name(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        model_name = 'there_is_no_model_with_that_name'
        login_header = login(user)

        response = test_client.get(f'/coach/get-daily/{model_name}', headers=login_header)

        assert response.status_code == 200
