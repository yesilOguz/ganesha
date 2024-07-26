from io import BytesIO

import pytest

from faker import Faker
from faker_file.providers.mp3_file import Mp3FileProvider

Faker.seed(3)
faker = Faker()
faker.add_provider(Mp3FileProvider)


@pytest.fixture()
def CreateAudioFile():
    file_content = faker.mp3_file(raw=True)
    return BytesIO(file_content)

