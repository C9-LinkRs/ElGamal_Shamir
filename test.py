from src.libs.ElGamal import ElGamal

g = ElGamal()
g.findPrime(55, 4)
g.findGenerator()
g.generatePrivateKey()
g.generatePublicKey()

print(g.getKeys())