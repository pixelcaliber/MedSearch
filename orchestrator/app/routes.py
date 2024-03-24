import io
import mimetypes
import os

import psycopg2
import requests
from flask import jsonify, render_template, request, send_file

from app.logger_utils import logger

# from search_module import search_similar_xrays
from app.utils import PgConnection

UPLOAD_FOLDER = "app/static/uploads"

SEARCH_SERVICE_URL = "http://localhost:5001/search"


def setup_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/search", methods=["POST"])
    def search():
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded."})

        image_file = request.files["image"]

        if not image_file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            return jsonify({"error": "Invalid image format."}), 400

        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)

        try:
            files = {"image": open(image_path, "rb")}
            data = {
                "filename": image_file.filename,
            }

            response = requests.post(SEARCH_SERVICE_URL, files=files, data=data)

            if response.status_code == 200:
                similar_image_indices = response.json()
                logger.info(f"response: {similar_image_indices}")
                res = jsonify(similar_image_indices)
                logger.info(res)
                return render_template("search.html", results=similar_image_indices)

        except Exception as e:
            return jsonify({"error": f"An error occurred during search: {str(e)}"})

    @app.route("/images/<filename>")
    def get_image(filename):
        try:
            conn = psycopg2.connect(
                host=PgConnection.HOST,
                port=PgConnection.PORT,
                database=PgConnection.DB,
                user=PgConnection.USER,
                password=PgConnection.USER_PASSWORD,
            )
            cursor = conn.cursor()
            db_query = "SELECT image_data FROM images WHERE name = '{}'".format(
                filename,
            )
            cursor.execute(query=db_query)
            image_data = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            file_extension = filename.split(".")[-1]
            mimetype = mimetypes.guess_type("dummy." + file_extension)[0]

            return send_file(io.BytesIO(image_data), mimetype=mimetype)
        except (Exception, psycopg2.Error) as error:
            print("Error fetching image:", error)
