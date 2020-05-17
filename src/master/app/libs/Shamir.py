import random 
from math import ceil 
from ..utils.functions import egcd
from ..utils.functions import mod_inverse


class Shamir:
  def __init__(self, t, n, secret, fieldSize):
      # t = minimum number of shares to reconstruct the secret
      self.t = t
      # n = number of parts the secret will be divided
      self.n = n
      # secret = the private key obtained with ElGamal
      self.secret = secret
      # fieldSize = the size of the field which we will be working
      self.fieldSize = fieldSize

  def lagrangeInterpolation(self, shares): 
      # Calculate Lambdas using Lagrange interpolation.  
      # Lambda is an array of shares being combined 
      sums = 0
      for j in range(len(shares["x"])): 
          xj = shares["x"][j]
          yj = shares["y"][j]
          
          num = 1
          den = 1
          prod = 1

          for i in range(len(shares["x"])): 
              xi = shares["x"][i]

              if (i != j):
                num = (num * ((-xi) % self.fieldSize) ) % self.fieldSize
                den = (den * ((xj - xi) % self.fieldSize)) % self.fieldSize
          prod = (num * mod_inverse(den, self.fieldSize)) % self.fieldSize
          sums = (self.fieldSize + sums + (yj * prod)) % self.fieldSize
      return sums

  def generatePool(self):
      # Generate pool to obtain t random shares
      # The pool is used to reconstruct the Polynomial and then reconstruct the Secret
      pool = random.sample(self.shares, self.t)
      self.pool = pool
      return pool

  def generateShares(self): 
      # Randomly generate a coefficient 
      # array for a polynomial with degree t-1 whose constant (alpha) = secret
      #coeff = [random.randrange(0, self.fieldSize) for _ in range(self.t-1)] 
      coeff = [111, 58]
      coeff.append(self.secret) 

      # Split secret using Shamir's Secret Sharing into n shares with threshold t
      cfs = coeff
      print("shamir coeff {}".format(cfs))
      shares = [] 
      for i in range(1,self.n+1):
          r = i
          #r = random.randrange(1, self.fieldSize) 
          # Evaluates a polynomial in x with coeff being the coefficient list 
          shares.append([r, sum([((r**(len(cfs)-i-1))%self.fieldSize * cfs[i])%self.fieldSize for i in range(len(cfs))]) % self.fieldSize ]) 
      self.shares = shares
      return shares 

  def getValues(self):
    return {
      "t": self.t,
      "n": self.n,
      "secret": self.secret,
      "fieldSize": self.fieldSize
    }
  
  def deletePrivateKey(self):
    self.secret = "hidden"
