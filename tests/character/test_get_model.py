import glob
from pathlib import Path

from ganesha.character.routes import main_path
import random


class TestGetModel:
    def test_get_model(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        model_list = glob.glob(f'{main_path}*.glb')
        models = [Path(e).stem for e in model_list]

        if len(models) == 0:
            assert True
        else:
            random_model = random.choice(models)

            login_header = login(user)
            response = test_client.get(f'/character/get-model/{random_model}', headers=login_header)

            assert response.status_code == 200

    def test_get_model_if_there_is_no_model_with_that_name(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        login_header = login(user)
        response = test_client.get(f'/character/get-model/there-is-no-model-with-this-name', headers=login_header)

        assert response.status_code == 404
