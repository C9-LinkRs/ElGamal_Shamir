import json
import requests
from flask import Flask, jsonify
import app.controller as controller
from app.libs.ElGamal import ElGamal
from app.libs.Shamir import Shamir

"""
  FOR EDUCATIONAL AND TESTING PURPOSE, CURRENT PRIVATE KEY IS NOT DELETED FROM
  OBJECT INSTANCES UNTIL SHAMIR RECONSTRUCTION FUNCTION IS CALLED
"""

#Init Flask server
app = Flask(__name__)
app.register_blueprint(controller.main_blueprint)

#Init ElGamal values
currentGamal = ElGamal()
currentGamal.findPrime(50, 5)
currentGamal.findGenerator()
currentGamal.generatePrivateKey()
currentGamal.generatePublicKey()
elGamal_values = currentGamal.getKeys()

#Setting master controller class variable 'currentGamal' current ElGamal object instance
controller.currentGamal = currentGamal

#Init Shamir secret sharing
t = 3 #Minimum keys to use to reconstruct
n = 6 #Number of slaves
secret = elGamal_values["private"]
fieldSize = elGamal_values["public"]["p"]
currentShamir = Shamir(t, n, secret, fieldSize)
sharesSecret = currentShamir.generateShares()

#Send share pair to slaves
for i in range(n):
  body = { "pair": { "x": sharesSecret[i][0], "y": sharesSecret[i][1] }, "p": elGamal_values["public"]["p"] }
  r = requests.post("http://elgamal_shamir_slave_{}:5001/init".format(i+1), json=body)

#Setting master controller class variable 'currentShamir' current Shamir object instance
controller.currentShamir = currentShamir

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5001, debug=False)