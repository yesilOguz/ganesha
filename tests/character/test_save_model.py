import json
from io import BytesIO

from faker import Faker
from faker_file.providers.txt_file import TxtFileProvider

from ganesha.character.routes import main_path
from ganesha.user.roles import UserRole
import os

Faker.seed(3)
faker = Faker()
faker.add_provider(TxtFileProvider)


class TestSaveModel:
    def test_save_model(self, test_client, UserDBFactory, CameraSettingsFactory, login):
        user = UserDBFactory(role=UserRole.ADMIN_USER)

        test_model_name = 'test_model.txt'
        fake_file_content = faker.txt_file()
        fake_file = BytesIO(fake_file_content.encode('utf-8'))
        fake_file.name = test_model_name

        settings = CameraSettingsFactory(test_model_name)

        camera_settings_json = json.dumps(settings.to_json())
        data = {
            'camera_settings': camera_settings_json
        }
        files = {
            'object_file': (test_model_name, fake_file, 'text/plain')
        }

        login_header = login(user)
        response = test_client.post('/character/save-model', data=data, files=files, headers=login_header)

        assert response.status_code == 201

        os.remove(f'{main_path}{test_model_name}.glb')

    def test_save_model_if_user_is_not_admin(self, test_client, UserDBFactory, CameraSettingsFactory, login):
        user = UserDBFactory(role=UserRole.END_USER)

        test_model_name = 'test_model.txt'
        fake_file_content = faker.txt_file()
        fake_file = BytesIO(fake_file_content.encode('utf-8'))
        fake_file.name = test_model_name

        settings = CameraSettingsFactory(test_model_name)

        camera_settings_json = json.dumps(settings.to_json())
        data = {
            'camera_settings': camera_settings_json
        }
        files = {
            'object_file': (test_model_name, fake_file, 'text/plain')
        }

        login_header = login(user)
        response = test_client.post('/character/save-model', data=data, files=files, headers=login_header)

        assert response.status_code == 403
