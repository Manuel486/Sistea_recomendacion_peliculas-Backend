from flask import Blueprint, jsonify, request

# Entities
from models.entities.Link import Link

# Models
from models.LinkModel import LinkModel

main = Blueprint("link_blueprint", __name__)


@main.route("/")
def get_links():
    try:
        links = LinkModel.get_links()
        return jsonify(links)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
