import os

from ganesha.character.routes import main_path
from ganesha.user.roles import UserRole


class TestRemoveModel:
    def test_remove_model(self, test_client, UserDBFactory, CharacterDBFactory, login):
        user = UserDBFactory(role=UserRole.ADMIN_USER)

        test_model_name = 'test_model_name'
        CharacterDBFactory(test_model_name)

        login_header = login(user)
        response = test_client.get(f'/character/remove-model/{test_model_name}', headers=login_header)

        assert response.status_code == 200

    def test_remove_model_if_user_not_admin(self, test_client, UserDBFactory, CharacterDBFactory, login):
        user = UserDBFactory(role=UserRole.END_USER)

        test_model_name = 'test_model_name'
        CharacterDBFactory(test_model_name)

        login_header = login(user)
        response = test_client.get(f'/character/remove-model/{test_model_name}', headers=login_header)

        assert response.status_code == 403

        os.remove(f'{main_path}{test_model_name}.glb')
