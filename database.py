from pymilvus import DataType, MilvusClient, Role, connections, db, utility

import logger_utils
from utils import Constants, Database, Fields, MilvusConnection

logger = logger_utils.logger

connections.connect(
    host=MilvusConnection.HOST,
    port=MilvusConnection.PORT,
    user=MilvusConnection.USER,
    password=MilvusConnection.USER_PASSWORD,
)

role = Role(MilvusConnection.ROLE_NAME, using="default")


def create_role():
    role.create()


def create_user():
    utility.create_user(
        MilvusConnection.USER, MilvusConnection.USER_PASSWORD, using="default"
    )


def list_users():
    users = utility.list_usernames(using="default")
    print(f"users: {users}")


def grant_role():
    role.grant(
        "Collection",
        "*",
        MilvusConnection.PRIVILEGE_INSERT,
        db_name=Database.DATABASE_NAME,
    )
    print(role.list_grants())
    role = utility.list_user(MilvusConnection.USER, True, using="default")
    print(f"role: {role}")


def create_database():
    database = db.create_database(Database.DATABASE_NAME)
    print(db.list_database())


def create_collection_if_not_exists(client, collection_name):
    # Check if collection exists
    if client.has_collection(collection_name):
        print(f"Collection '{collection_name}' already exists.")
        return

    # Create collection if it doesn't exist
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )

    schema.add_field(field_name=Fields.ID, datatype=DataType.INT64, is_primary=True)
    schema.add_field(
        field_name=Fields.NAME, datatype=DataType.FLOAT_VECTOR, dim=Constants.DIM
    )
    schema.add_field(
        field_name=Fields.FILENAME, datatype=DataType.VARCHAR, max_length=1024
    )

    print(f"Creating collection '{collection_name}'...")
    client.create_collection(
        collection_name=collection_name, schema=schema, dimension=Constants.DIM
    )
    print(f"Collection '{collection_name}' created successfully.")


def drop_collection(client):
    client.drop_collection(collection_name=Database.COLLECTION)
