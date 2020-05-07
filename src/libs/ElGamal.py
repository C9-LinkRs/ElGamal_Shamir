import random
from utils.functions import modPow
from utils.millerRabin import millerRabin

"""
Python class for ElGamal implementation

PS: If you instantiate the class with no params, you have to generate prime p and generator g
"""

class ElGamal:

  #Instantiate class only with prime q
  def __init__(self, q):
    self.p = 2 * q + 1
  
  #Instantiate class with prime q and generator g
  def __init__(self, q, g):
    self.p = 2 * q + 1
    self.g = g

  #Find a proper prime p of numBits bits using Miller-Rabin test with factor of accuracy k
  def findPrime(self, numBits, k):
    while True:
      q = random.randint(2**(numBits - 2), 2**(numBits - 1))
      while q % 2 == 0:
        q = random.randint(2**(numBits - 2), 2**(numBits - 1))
      
      while not millerRabin(q, k):
        q = random.randint(2**(numBits - 2), 2**(numBits - 1))
        while q % 2 == 0:
          q = random.randint(2**(numBits - 2), 2**(numBits - 1))
      
      p = 2 * q + 1
      if millerRabin(p, k):
        self.p = p
        break
  
  #Finding the smallest primitive root for prime p using Lagrange's Theorem
  def findGenerator(self):
    if self.p == 2:
      return 1
    
    primeFactor1 = 2
    primeFactor2 = (self.p - 1)//2

    while True:
      g = random.randint(2, self.p - 2)
      if modPow(g, (self.p - 1)//primeFactor1) != 1 and modPow(g, (self.p - 1)//primeFactor2) != 1:
        self.g = g
        break

  def generatePrivateKey(self):
    self.x = random.randint(2, (self.p - 1)//2)
    return x

  def generatePublicKey(self):
    self.findGenerator()
    self.y = modPow(self.g, self.x, self.p)
    return {
      "p": self.p,
      "g": self.g,
      "y": self.y
    }
  
  def getKeys(self):
    return {
      "public": {
        "p": self.p,
        "g": self.g,
        "y": self.y
      },
      "private": x
    }
  
  def encrypt(self, plainText):
    asciiText = ord(plainText)
    k = random.randint(2, self.p - 2)
    c1 = modPow(self.g, k, self.p)
    c2 = (asciiText * modPow(self.y, k, self.p)) % self.p
    return {
      "c1": c1,
      "c2": c2
    }
