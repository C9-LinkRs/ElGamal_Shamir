import json
from flask import Blueprint, jsonify, request
from .utils.functions import modPow

main_blueprint = Blueprint('Slave', __name__)

#Shamir pair to save
shamirPair = {}
p = -1

@main_blueprint.route("/")
def index():
  return jsonify({ "message": "Slave server's up!", "p":p, "x": shamirPair["x"], "y": shamirPair["y"] }), 200


@main_blueprint.route("/init", methods=["POST"])
def initSlave():
  global shamirPair
  global p

  params = request.get_json()
  shamirPair = params["pair"]
  p = params["p"]
  return jsonify({ "pair": shamirPair, "p": p }), 200


@main_blueprint.route("/return")
def returnKey():
  global shamirPair

  partialDecrypt = { "x": shamirPair["x"], "y": shamirPair["y"] }
  
  return jsonify({ "partialDecrypt": partialDecrypt }), 200