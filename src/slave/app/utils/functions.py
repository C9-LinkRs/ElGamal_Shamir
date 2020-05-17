#Euclideant Greatest Common Divisor 
def GCD(a, b):
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

#Extended Greatest Common Divisor 2.0
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

#Moduled Inverse
def mod_inverse(k, prime):
    k = k % prime
    if k < 0:
        r = egcd(prime, -k)[2]
    else:
        r = egcd(prime, k)[2]
    return (prime + r) % prime