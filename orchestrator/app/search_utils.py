import os
from functools import lru_cache

import psycopg2
import requests
from flask import jsonify, render_template

from app.logger_utils import logger
from app.utils import PgConnection

conn = psycopg2.connect(
    host=PgConnection.HOST,
    port=PgConnection.PORT,
    database=PgConnection.DB,
    user=PgConnection.USER,
    password=PgConnection.USER_PASSWORD,
)
cursor = conn.cursor()

SEARCH_SERVICE_URL = "http://localhost:5003/search"


@lru_cache(maxsize=1000)
def search_similar_xrays(image_path):
    try:
        data = {
            "image_path": image_path,
        }

        response = requests.post(SEARCH_SERVICE_URL, data=data)

        if response.status_code == 200:
            similar_image_indices = response.json()
            res = jsonify(similar_image_indices)
            logger.info(res)
            return render_template("search.html", results=similar_image_indices)

    except Exception as e:
        return jsonify({"error": f"An error occurred during search: {str(e)}"})
