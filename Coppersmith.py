import numpy as np
from numpy.polynomial import Polynomial
from LLL import Basis
from rsa import RSA

# Opère la transformation polynôme → vecteur exposée dans le dossier
def poly_to_vect(poly, X, xlen=1):
    d = poly.degree()
    vect = np.zeros((X * xlen))
    for i in range(d + 1):
        vect[i] = poly.coef[i] * X ** i
    return vect

# Opère la transformation vecteur → polynôme exposée dans le dossier
def vect_to_poly(vect, X):
    n = len(vect)
    poly = Polynomial([0])
    for i in range(n):
        monomial = Polynomial([0] * i + [1])
        poly += (vect[i] / (X ** i)) * monomial
    return poly

# Construit la base de vecteurs pour la méthode de la section 4.1
def poly_to_basis1(poly, X, k, d, a, b):
    s = np.zeros((k + 1, d + 4))
    for i in range(k):
        monomial = Polynomial([0] * i + [1])
        G = (Polynomial([b]) ** (k - 1 - i)) * monomial
        vect = poly_to_vect(G * poly, X, xlen=d+4)
        s[i] = vect
    s[k] = poly_to_vect((Polynomial([b]) ** k) * a, X, xlen=d+4)
    return Basis(s)

# Construit la base de vecteurs pour la méthode de Coppersmith
def poly_to_basis2(poly, X, k, d):
    s = np.zeros((k + 1, d + 4))
    for i in range(k):
        monomial = Polynomial([0] * i + [1])
        vect = poly_to_vect(poly * monomial, X, xlen=d+4)
        s[i] = vect
    s[k] = poly_to_vect(Polynomial([1]), X, xlen=d+4)
    return Basis(s)

# Exemple d’utilisation
poly = Polynomial([-222, 5000, 10, 1])
print(poly)

X = 10**3
k = 4
d = 3
a = 1000
b = 11

base1 = poly_to_basis1(poly, X, k, d, a, b)
print('Base 1 :\n', base1.basis)
p1 = vect_to_poly(base1.basis[0], X)
print(p1)
print(p1.roots())

base2 = poly_to_basis2(poly, X, k, d)
print('Base 2 :\n', base2.basis)
p2 = vect_to_poly(base2.basis[0], X)
print(p2)
print(p2.roots())
