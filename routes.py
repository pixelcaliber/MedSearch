import io
import mimetypes
import os

import psycopg2
from flask import jsonify, render_template, request, send_file

import logger_utils
from preprocess import preprocess
from search_module import search_similar_xrays
from utils import PgConnection

logger = logger_utils.logger


def setup_routes(app):

    @app.route("/")
    def index():
        preprocess()
        return render_template("index.html")

    @app.route("/search", methods=["POST"])
    def search():
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded."})

        image_file = request.files["image"]

        if not image_file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            return jsonify({"error": "Invalid image format."})

        image_path = os.path.join("uploads", image_file.filename)
        image_file.save(image_path)

        try:
            similar_image_indices = search_similar_xrays(image_path)
            res = jsonify(similar_image_indices)
            # return res
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
