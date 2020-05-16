from flask import Blueprint, jsonify, request
from ..libs import Shamir

main_blueprint = Blueprint('Slave', __name__)

@main_blueprint.route("/")
def index():
  return jsonify({ "message": "Slave server's up!" }), 200

@main_blueprint.route("/init", methods=["POST"])
def initSlave():
  params = request.get_json()
  gamalKey = params["key"]
  return jsonify({ "received": gamalKey }), 200