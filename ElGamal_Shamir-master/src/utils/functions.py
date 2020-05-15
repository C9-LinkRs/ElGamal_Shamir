#Extended Greatest Common Divisor 
def EGCD(a, b):
  while b != 0:
    c = a%b
    a = b
    b = c
  return a

#Fast modular exponentiation in O(log y)  
def modPow(x, y, p) : 
  res = 1
  x = x % p  
    
  if (x == 0) : 
      return 0

  while (y > 0) :  
    if ((y & 1) == 1) : 
      res = (res * x) % p 
    y = y >> 1
    x = (x * x) % p 
        
  return res