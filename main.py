import os

from flask import Flask
from pymilvus import connections

import logger_utils
from routes import setup_routes
from utils import Database, MilvusConnection

app = Flask(__name__)
logger = logger_utils.logger

if __name__ == "__main__":
    connections.connect(
        host=MilvusConnection.HOST,
        port=MilvusConnection.PORT,
        user=MilvusConnection.USER,
        password=MilvusConnection.USER_PASSWORD,
    )
    setup_routes(app)
    app.run(debug=True)
