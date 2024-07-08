import os
from enum import Enum

from ganesha.core.mongo_database import DB


class Collections(Enum):
    USER_COLLECTION = 'user'


def get_collection(collection: Collections):
    APP_MODE = os.getenv("APP_MODE", default='DEV')
    collection_db_name = f'{APP_MODE}_{collection.value}'

    return DB[collection_db_name]


def drop_all_collections():
    for s in Collections:
        DB.drop_collection(get_collection(s))
