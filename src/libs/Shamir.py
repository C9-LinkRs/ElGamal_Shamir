import random 
from math import ceil 
from decimal import *


class Shamir:
  pass
  
  def __init__(self, t, n, secret, fieldSize):
      # t = minimum number of shares to reconstruct the secret
      self.t = t
      # n = number of parts the secret will be divided
      self.n = n
      # secret = the private key obtained with ElGamal
      self.secret = secret
      # fieldSize = the size of the field which we will be working
      self.fieldSize = fieldSize

  def reconstructSecret(self, shares): 
      # Combines shares using Lagranges interpolation.  
      # Shares is an array of shares being combined 
      sums, prod_arr = 0, [] 

      for j in range(len(shares)): 
          xj, yj = shares[j][0],shares[j][1] 
          prod = Decimal(1) 

          for i in range(len(shares)): 
              xi = shares[i][0] 
              if i != j: prod *= Decimal(Decimal(xi)/(xi-xj)) 

          prod *= yj 
          sums += Decimal(prod) 
      self.reconstructedSecret = int(round(Decimal(sums),0)) 
      return int(round(Decimal(sums),0)) 

  def generatePool(self):
      # Generate pool to obtain t random shares
      # The pool is used to reconstruct the Polynomial and then reconstruct the Secret
      pool = random.sample(self.shares, self.t)
      self.pool = pool
      return pool

  def generateShares(self): 
      # Randomly generate a coefficient 
      # array for a polynomial with degree t-1 whose constant (alpha) = secret
      coeff = [random.randrange(0, self.fieldSize) for _ in range(self.t-1)] 
      coeff.append(self.secret) 

      # Split secret using Shamir's Secret Sharing into n shares with threshold t
      cfs = coeff
      shares = [] 
      for i in range(1,self.n+1): 
          r = random.randrange(1, self.fieldSize) 
          # Evaluates a polynomial in x with coeff being the coefficient list 
          shares.append([r, sum([r**(len(cfs)-i-1) * cfs[i] for i in range(len(cfs))])]) 
      self.shares = shares
      return shares 
