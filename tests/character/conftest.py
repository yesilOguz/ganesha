import pytest

from ganesha.character.models import CharacterGetCameraSettings, CameraOrbitSettings, CameraTargetSettings
from ganesha.collections import Collections, get_collection

from faker import Faker
from faker_file.providers.txt_file import TxtFileProvider

from ganesha.character.routes import main_path

Faker.seed(3)
faker = Faker()
faker.add_provider(TxtFileProvider)


@pytest.fixture()
def CameraSettingsDBFactory():
    def _func(object_name: str):
        camera_orbit = CameraOrbitSettings()
        camera_target = CameraTargetSettings(x=0, y=0, z=0)

        settings = CharacterGetCameraSettings(object_name=object_name,
                                              camera_target=camera_target,
                                              camera_orbit=camera_orbit)

        get_collection(Collections.CAMERA_SETTINGS_COLLECTION).insert_one(settings.to_mongo())
        return settings
    return _func


@pytest.fixture()
def CameraSettingsFactory():
    def _func(object_name: str):
        camera_orbit = CameraOrbitSettings()
        camera_target = CameraTargetSettings(x=0, y=0, z=0)

        settings = CharacterGetCameraSettings(object_name=object_name,
                                              camera_target=camera_target,
                                              camera_orbit=camera_orbit)
        return settings
    return _func


@pytest.fixture()
def CharacterDBFactory(CameraSettingsDBFactory):
    def _func(object_name: str):
        fake_file_content = faker.txt_file()
        settings = CameraSettingsDBFactory(object_name)

        path = f'{main_path}{object_name}.glb'
        with open(path, 'wb+') as f:
            f.write(fake_file_content.encode('utf-8'))

        return object_name

    return _func



