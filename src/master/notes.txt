""" from flask import Flask """
import sys
sys.path.insert(0, '../')
import random
import functools
from utils import functions


_PRIME = 41
print("p: ", _PRIME)
_RINT = functools.partial(random.SystemRandom().randint, 0)
"""
Generacion de llaves
g = generador
alpha = llave privada 1<alpha<=p-1
u = g**alpha
"""

def evalAT(poly, x, prime):
    accum = 0
    for index, coeff in enumerate(reversed(poly[1:len(poly)])):
        xterm = functions.modPow(x, len(poly)-(index+1), prime)
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
    print("F(X)="+stracc)

def shamir(s,t,alpha, prime=_PRIME):
    poly = [t]
    poly[0] = alpha
    poly[1:t] = [_RINT(prime - 1) for i in range(1,t)]
    puntos = [(i, evalAT(poly, i, prime)) for i in range(1, s + 1)]
    print("--------------------------------------------------------------------------------------------------------------------")
    print("Coeficientes:", poly)
    print("--------------------------------------------------------------------------------------------------------------------")
    polyToString(poly)
    print("--------------------------------------------------------------------------------------------------------------------")
    print("Puntos: ",puntos)

    return puntos

#pido s(cuantos clientes quiero tener), t(cuantos se necesitan minimo para desencriptar)
s=6
t=3
alpha = 13
print("Shares: ", s, " - Minimun: ", t, " - Secret: ", alpha)
puntos = shamir(s,t,alpha)

#iniciar array de slaves?
"""
para i= 1: i<s: i++
    Slave slave = new Slave(puntos[i], p,g,u)
fin para
"""

#pedir mensaje a encryptar
#encryptar con llave publica

#recibir el mensaje crifrado

#enviar el mensaje crifrado a TODOS los slaves

#esperar el mensaje de regreso de los slaves, esperar a por lo menos t de ellos
#unir partes

#mostrar mensaje desencriptado