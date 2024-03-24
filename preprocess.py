import os
from functools import lru_cache

import cv2
import faiss
import numpy as np
import psycopg2
from pymilvus import MilvusClient, connections
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img

import logger_utils
from database import create_collection_if_not_exists, drop_collection
from fine_tune_model import feature_extractor_model
from utils import Constants, Database, MilvusConnection, PgConnection

logger = logger_utils.logger

# create connection with milvus
connections.connect(
    host=MilvusConnection.HOST,
    port=MilvusConnection.PORT,
    user=MilvusConnection.USER,
    password=MilvusConnection.USER_PASSWORD,
)

# initialize user client
client = MilvusClient(
    uri=MilvusConnection.URI,
    token=MilvusConnection.TOKEN,
    db_name=Database.DATABASE_NAME,
)

conn = psycopg2.connect(
    host=PgConnection.HOST,
    port=PgConnection.PORT,
    database=PgConnection.DB,
    user=PgConnection.USER,
    password=PgConnection.USER_PASSWORD,
)
cursor = conn.cursor()


@lru_cache(maxsize=1000)
def preprocess_image(img_path, filename=None):
    with open(img_path, "rb") as f:
        image_data = f.read()
    if filename is not None:
        try:
            db_query = "INSERT INTO images (name, image_data) VALUES ('{}', {})".format(
                filename, psycopg2.Binary(image_data)
            )
            cursor.execute(query=db_query)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error storing image:", error)

    image = load_img(img_path, target_size=(224, 224))
    image = img_to_array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = preprocess_input(image)
    return image


def preprocess():
    try:
        create_collection_if_not_exists(
            client=client, collection_name=Database.COLLECTION
        )
        data = []
        for idx, filename in enumerate(os.listdir(Constants.dataset_path)):
            if filename.endswith(".jpeg"):
                image_path = os.path.join(Constants.dataset_path, filename)
                preprocessed_image = preprocess_image(image_path, filename)
                # image_filename_dict[idx] = filename

                image = np.expand_dims(preprocessed_image, axis=0)
                feature = feature_extractor_model.predict(image).flatten()
                feature = feature.flatten()[:2048]

                record = {
                    "id": idx,
                    "image_vector": feature.tolist(),
                    "filename": filename,
                }
                data.append(record)

        logger.info(f"total files processed: {len(data)}")

        # The code below belongs to the Faiss implementation..
        # scaler = StandardScaler()
        # image_features = scaler.fit_transform(image_features)
        # d = image_features[0].shape[0]
        # index = faiss.IndexFlatL2(d)
        # index.add(image_features)
        # index = faiss.write_index("xray_index.faiss")

        results = client.insert(collection_name=Database.COLLECTION, data=data)
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(
            field_name="image_vector", metric_type="COSINE", index_name="vector_index"
        )
        client.create_index(
            collection_name=Database.COLLECTION, index_params=index_params
        )
        print("Image vectors generated and stored in Milvus!")
    except Exception as e:
        raise e
    finally:
        if conn:
            cursor.close()
            conn.close()
