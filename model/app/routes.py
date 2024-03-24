from app.preprocess import preprocess


def setup_routes(app):

    @app.route("/")
    def index():
        preprocess()
        return "Preprocessing complete!"
