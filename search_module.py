import numpy as np
from pymilvus import DataType, MilvusClient, connections

import logger_utils
from fine_tune_model import feature_extractor_model, model
from preprocess import preprocess_image
from utils import Constants, Database, MilvusConnection

logger = logger_utils.logger
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
