import json
import requests
from flask import Blueprint, jsonify, request
from .libs.ElGamal import ElGamal

main_blueprint = Blueprint('Master', __name__)
currentGamal = None
currentShamir = None

@main_blueprint.route("/")
def index():
  return jsonify({ 
    "message": "Master server's up!", 
    "ElGamal": currentGamal.getKeys(),
    "Shamir": currentShamir.getValues()
    }), 200


@main_blueprint.route("/encrypt", methods=["POST"])
def encrypt():
  params = request.get_json()
  message = params["message"]
  encryptedMessage = []

  #Encrypt every letter of the message
  for letter in message:
    encryptedMessage.append(currentGamal.encrypt(letter))
  return jsonify({ "encryptedMessage": encryptedMessage })


@main_blueprint.route("/decrypt", methods=["POST"])
def decrypt():
  params = request.get_json()
  pairs = params["encryptedMessage"]

  #Obtain every shamir share pairs
  shamirPairs = []
  shamirValues = currentShamir.getValues()
  for i in range(shamirValues["n"]):
    r = requests.get("http://elgamal_shamir_slave_{}:5001/return".format(i+1))
    
    response = r.json()
    shamirPairs.append(response["shamirPair"])

  decryptedMessage = currentShamir.reconstructSecret(shamirPairs)
  return jsonify({ "decryptedMessage": decryptedMessage })