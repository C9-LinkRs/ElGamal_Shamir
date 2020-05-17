import json
import random
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

  #Shamir instance values
  shamirValues = currentShamir.getValues()

  #Pick t random slaves servers
  randomServers = random.sample(range(1, shamirValues["n"]), shamirValues["t"])
  
  #Calculate pair (x, c1^y) from slaves for every encrypted pairs
  
  partialDecrypt = []
  for pair in pairs:
    slaveX = []
    slaveY=[]
    for slave in randomServers:
      body = { "c1": pair["c1"] }
      r = requests.get("http://elgamal_shamir_slave_{}:5001/return".format(slave), json=body)
      
      response = r.json()
      
      slaveX.append(response["partialDecrypt"]["x"])
      slaveY.append(response["partialDecrypt"]["y"])
      
    partialDecrypt.append({ "x": slaveX, "y":slaveY, "c1": pair["c1"], "c2": pair["c2"] })
  
  #Decrypt encrypted message
  decryptedMessage = ""
  secret = currentShamir.lagrangeInterpolation(partialDecrypt[0])
  for pair in partialDecrypt:
    decryptPair = { "secret": secret, "c1": pair["c1"], "c2": pair["c2"] }
    plainText = currentGamal.decrypt(decryptPair)
    decryptedMessage+=plainText

  return jsonify({ "decryptedMessage": decryptedMessage, "randomServers": randomServers })