import glob
from pathlib import Path
import random

from ganesha.character.routes import main_path


class TestGetModelCameraSettings:
    def test_get_model_camera_settings(self, test_client, UserDBFactory, CameraSettingsDBFactory, login):
        user = UserDBFactory()

        model_list = glob.glob(f'{main_path}*.glb')
        models = [Path(e).stem for e in model_list]

        if len(models) == 0:
            assert True
        else:
            random_model = random.choice(models)
            settings = CameraSettingsDBFactory(object_name=random_model)
    
            login_header = login(user)
            response = test_client.get(f'/character/get-model-camera-settings/{random_model}', headers=login_header)

            assert response.status_code == 200

    def test_get_model_camera_settings_if_model_is_not_exist(self, test_client, UserDBFactory, login):
        user = UserDBFactory()

        login_header = login(user)
        response = test_client.get('/character/get-model-camera-settings/{model-with-this-name-is-not-exist', headers=login_header)

        assert response.status_code == 404
