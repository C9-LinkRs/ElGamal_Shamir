import random
import functools
from functions import modPow

_PRIME = 41
_RINT = functools.partial(random.SystemRandom().randint, 0)


def evalAT(poly, x, prime):
    accum = 0
    for index, coeff in enumerate(reversed(poly[1:len(poly)])):
        xterm = modPow(x, len(poly)-(index+1), prime)
        #print(x,"**",len(poly)-(index+1),"=",xterm)
        #print("coeff:",coeff)
        accum += (coeff*xterm)%prime
        #print("accum:",accum)
    
    accum = (accum+poly[0])%prime
    return accum

def polyToString(poly):
    stracc = ""
    for index, coeff in enumerate(reversed(poly[1:len(poly)])):
        stracccterm = str(coeff)+"*"+"(x**"+str(len(poly)-(index+1))+")+"
        stracc += stracccterm 
        #term = coeff*(x**poly.length-index)
    stracc += str(poly[0])
    print(stracc)

prime = _PRIME
t = 3
s = 6
secret = 1000
poly = [t]
poly[0] = secret
poly[1:t] = [_RINT(prime - 1) for i in range(1,t)]
poly = [13,25,28]
puntos = [(i, evalAT(poly, i, prime)) for i in range(1, s + 1)]
print("--------------------------------------------------------------------------------------------------------------------")
polyToString(poly)
print("--------------------------------------------------------------------------------------------------------------------")
print(poly)
print("--------------------------------------------------------------------------------------------------------------------")
print(puntos)