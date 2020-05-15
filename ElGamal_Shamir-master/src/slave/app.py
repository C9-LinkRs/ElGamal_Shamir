""" from flask import Flask """

class Slave:
    punto = (0,0)
    p = 0
    g = 0
    u = 0

    def __init__(self, pu, p, g, u):
        self.punto = pu
        self.p = p
        self.g = g
        self.u = u

    def decrypt(self, cipher):
        return (self.punto[0],cipher[0]**self.punto[1])


obj = Slave((1,1),41,5,(5**3)%41)
cipher = (2,5)
mensaje = obj.decrypt(cipher)
print("Punto:", obj.punto, " - p: ", obj.p, " - g: ", obj.g, " - u: ", obj.u)
print("Desencriptar: ", cipher)
print(mensaje)