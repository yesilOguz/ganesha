import glob
from ganesha.character.routes import main_path as model_main_path


class TestGetModelList:
    def test_get_model_list(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        login_header = login(user)
        response = test_client.get('/character/get-model-list', headers=login_header)

        model_name_list = glob.glob(f'{model_main_path}*.glb')

        print(model_name_list)

        assert response.status_code == 200
        assert len(response.json()['characters']) == len(model_name_list)
