from flask import Blueprint, jsonify, request

main_blueprint = Blueprint('Master', __name__)

@main_blueprint.route("/")
def index():
  return jsonify({ "message": "Master server's up!" }), 200