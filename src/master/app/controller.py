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

  #Calculate pair (x, c1^y) from slaves for every encrypted pairs
  shamirValues = currentShamir.getValues()
  partialDecrypt = []
  for pair in pairs:
    slaveX = []
    slaveC1Y = []
    for i in range(shamirValues["t"]):
      body = { "c1": pair["c1"] }
      r = requests.post("http://elgamal_shamir_slave_{}:5001/return".format(i+1), json=body)
      
      response = r.json()
      print(response)
      slaveX.append(response["partialDecrypt"]["x"])
      slaveC1Y.append(response["partialDecrypt"]["c1y"])
    partialDecrypt.append({ "x": slaveX, "c1y": slaveC1Y, "c2": pair["c2"] })

  #Decrypt encrypted message
  decryptedMessage = []
  lambdas = currentShamir.lagrangeInterpolation(partialDecrypt[0]["x"])
  for pair in partialDecrypt:
    decryptPair = { "lambda": lambdas, "c1y": pair["c1y"], "c2": pair["c2"] }
    plainText = currentGamal.decrypt(decryptPair)
    decryptedMessage.append(plainText)

  return jsonify({ "decryptedMessage": decryptedMessage })