from flask import Flask

from app.routes import setup_routes

app = Flask(__name__, template_folder="app/templates")
app.config.from_pyfile("config.py")

setup_routes(app)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
