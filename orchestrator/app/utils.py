import os

from dotenv import load_dotenv

load_dotenv()


class MilvusConnection:
    HOST = os.getenv("_HOST")
    PORT = os.getenv("_PORT")
    USER = os.getenv("_USER")
    URI = "http://" + HOST + ":" + PORT
    USER_PASSWORD = os.getenv("_USER_PASSWORD")
    ROLE_NAME = os.getenv("_ROLE_NAME")
    PRIVILEGE_INSERT = os.getenv("_PRIVILEGE_INSERT")
    TOKEN = USER + ":" + USER_PASSWORD


class PgConnection:
    HOST = os.getenv("_PG_HOST")
    PORT = os.getenv("_PG_PORT")
    USER = os.getenv("_PG_USER")
    DB = os.getenv("_PG_DB")
    USER_PASSWORD = os.getenv("_PG_PASSWORD")


class Database:
    DATABASE_NAME = os.getenv("_DATABASE_NAME")
    COLLECTION = "xray_image_vectors"


class Constants:
    dataset_path = "chest_xray/test/PNEUMONIA"
    DIM = 2048


class Fields:
    NAME = "image_vector"
    ID = "id"
    FILENAME = "filename"
