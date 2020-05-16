import random
from .functions import modPow

#Source: https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/

def test(d, p):
  a = 2 + random.randint(1, p-4)
  x = modPow(a, d, p)

  if x == 1 or x == p-1:
    return True

  while (d != p-1):
    x = (x*x) % p
    d*=2
    if (x == 1):
      return False
    if (x == p-1):
      return True
  return False


def millerRabin(p, k):
  if (p <= 1 or p == 4):
    return False
  if (p <= 3):
    return True
  
  d = p-1
  while (d % 2 == 0):
    d//=2
  
  for i in range(k):
    if not test(d, p):
      return False
  return True