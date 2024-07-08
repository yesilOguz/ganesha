import os
from pymongo import MongoClient


class MONGODB:
    def __init__(self):
        self.APP_MODE = os.getenv("APP_MODE", default='DEV')
        self.HOST = os.getenv("MONGO_HOST")
        self.PORT = os.getenv("MONGO_PORT")
        self.USERNAME = os.getenv("MONGO_USER")
        self.PASSWORD = os.getenv("MONGO_PASS")
        self.DBNAME = os.getenv("MONGO_DB")
        self.MONGO_URL = "mongodb://{}:{}@{}:{}/{}?retryWrites=true&w=majority&authSource=admin".format(self.USERNAME,
                                                                                                        self.PASSWORD,
                                                                                                        self.HOST,
                                                                                                        self.PORT,
                                                                                                        self.DBNAME)

        if self.APP_MODE == 'BETA' or self.APP_MODE == 'PROD' or self.APP_MODE == 'POST_DEPLOY_TEST':
            self.MONGO_URL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(self.USERNAME,
                                                                                            self.PASSWORD,
                                                                                            self.HOST,
                                                                                            self.DBNAME)

        self.mongodb_client = MongoClient(self.MONGO_URL)
        self.db = self.mongodb_client[self.DBNAME]

    def get_db(self):
        return self.db

    def shut_down_db(self):
        self.mongodb_client.close()

    def drop_database(self):
        self.mongodb_client.drop_database(self.DBNAME)

    def check_connection(self):
        try:
            if self.mongodb_client.get_database(self.DBNAME):
                return True
        except:
            return False

    def reconnect(self):
        self.mongodb_client = MongoClient(self.MONGO_URL)
        self.db = self.mongodb_client[self.DBNAME]


MONGO = MONGODB()
MONGO_CLIENT = MONGO.mongodb_client
DB = MONGO.db
