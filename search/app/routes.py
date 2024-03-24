import os

from flask import jsonify, request

from app import utils
from app.logger_utils import logger
from app.search_module import search_similar_xrays


def setup_routes(app):

    @app.route("/")
    def health():
        return "Search server is running fine!"

    @app.route("/search", methods=["POST"])
    def search():

        if "image" not in request.files:
            return jsonify({"error": "No image Provided."}), 400

        image_file = request.files["image"]

        if not image_file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            return jsonify({"error": "Invalid image format."}), 400

        image_path = os.path.join(utils.Constants.UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)
        try:
            similar_image_indices = search_similar_xrays(image_path)
            res = jsonify(similar_image_indices)
            logger.info(f"res: {res}")
            return res
        except Exception as e:
            return jsonify({"error": f"An error occurred during search: {str(e)}"})
