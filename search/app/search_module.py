from functools import lru_cache

import cv2
import numpy as np
from pymilvus import DataType, MilvusClient, connections
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img

from app.fine_tune_model import feature_extractor_model
from app.logger_utils import logger
from app.utils import Constants, Database, MilvusConnection

connections.connect(
    host=MilvusConnection.HOST,
    port=MilvusConnection.PORT,
    user=MilvusConnection.USER,
    password=MilvusConnection.USER_PASSWORD,
)


client = MilvusClient(
    uri=MilvusConnection.URI,
    token=MilvusConnection.TOKEN,
    db_name=Database.DATABASE_NAME,
)


@lru_cache(maxsize=1000)
def preprocess_image(img_path):
    image = load_img(img_path, target_size=(224, 224))
    image = img_to_array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = preprocess_input(image)
    return image


def search_similar_xrays(query_image):
    # index = faiss.read_index("xray_index.faiss")
    logger.info(query_image)
    query_vector = preprocess_image(query_image)
    query_vector = np.expand_dims(query_vector, axis=0)
    query_vector = feature_extractor_model.predict(query_vector).flatten()[
        : Constants.DIM
    ]

    client.load_collection(collection_name=Database.COLLECTION)

    results = client.search(
        collection_name=Database.COLLECTION,
        data=[query_vector.tolist()],
        anns_field="image_vector",
        limit=10,
        search_params={"metric_type": "COSINE", "params": {}},
        output_fields=["filename"],
    )
    logger.info(results[0])
    return results[0]

    # D, I = index.search(np.array([query_vector]), num_neighbors)
    # logger.info(I)
    # similar_image_filenames = [image_filename_dict[index] for index in I[0]]
    # return similar_image_filenames
