import json
from flask import Blueprint, jsonify, request

main_blueprint = Blueprint('Slave', __name__)

#Shamir pair to save
shamirPair = []

@main_blueprint.route("/")
def index():
  return jsonify({ "message": "Slave server's up!" }), 200


@main_blueprint.route("/init", methods=["POST"])
def initSlave():
  global shamirPair

  params = request.get_json()
  shamirPair = params["key"]
  return jsonify({ "received": shamirPair }), 200


@main_blueprint.route("/return")
def returnKey():
  global shamirPair

  return jsonify({ "shamirPair": shamirPair })