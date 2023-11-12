from flask import Flask
from flask_cors import CORS

from config import config

# Routes
from routes import RatingRoutes, MovieRoutes, LinkRoutes, AuthRoutes, UserRoutes
from routes import RecommendationRoute

app = Flask(__name__)

CORS(app)


if __name__ == "__main__":
    app.config.from_object(config["development"])

    # Blueprints
    app.register_blueprint(AuthRoutes.main, url_prefix="/auth")
    app.register_blueprint(RatingRoutes.main, url_prefix="/api/ratings")
    app.register_blueprint(MovieRoutes.main, url_prefix="/api/movies")
    app.register_blueprint(LinkRoutes.main, url_prefix="/api/links")
    app.register_blueprint(UserRoutes.main, url_prefix="/api/users")
    app.register_blueprint(RecommendationRoute.main, url_prefix="/api/recommendations")

    app.run()
