import random

# ALGORITHMES D’ARITHMÉTIQUE USUELS

# Calcule m^e mod n (exponentiation rapide)
def mod_exp(m, e, n):
    result = 1
    base = m % n
    while e > 0:
        if e % 2 == 1:
            result = (result * base) % n
        base = (base * base) % n
        e //= 2
    return result

# Calcule le r = pgcd(a, b) ainsi que des entiers u et v tels que au + bv = r
def euclide_etendu(a, b):
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, b
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1,
            u2 - q * v2,
            u3 - q * v3,
            v1, v2, v3
        )
    return u3, u1, u2

# GÉNÉRATION DE NOMBRES PREMIERS

# Test de témoin
def test_temoin(a, n):
    k = 0
    d = n - 1
    while d % 2 == 0:
        k += 1
        d //= 2
    x = mod_exp(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(k - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False

# Test de Miller–Rabin
def miller_rabin(n, k):
    if n < 3:
        return n == 2
    if n % 2 == 0:
        return False
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not test_temoin(a, n):
            return False
    return True
# Générateur de nombres premiers
def generate_prime(bits, k=100):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1)) | 1
        if miller_rabin(n, k):
            return n

# Génère deux nombres premiers distincts
def generate_primes(bits=1024):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
    return p, q

# GÉNÉRATION CLÉS RSA
class RSA:

    def __init__(self):
        self.generate_keys()

    # Clé publique : (e, n)
    # Clé privée : d
    def generate_keys(self, bits=1024):
        p, q = generate_primes(bits)
        self.n = p * q
        phi_n = (p - 1) * (q - 1)
        while True:
            e = random.randint(2, phi_n)
            r, u, v = euclide_etendu(e, phi_n)
            if r == 1:
                self.e = e
                self.d = u % phi_n
                break

    # ENCODAGE D’UN MESSAGE
    def encode(self, m):
        return mod_exp(m, self.e, self.n)

    # DÉCODAGE D’UN MESSAGE
    def decode(self, c):
        return mod_exp(c, self.d, self.n)


if __name__ == "__main__":
    rsa = RSA()
    print("Clé publique n : ", rsa.n)
    print("Clé publique e : ", rsa.e)
    print("Clé privée d : ", rsa.d)
    print("\n")

    # Premières décimales de pi
    m = 314159265358979323846264338327950288419716939937510
    print("Message : ", m)
    print("\n")

    c = rsa.encode(m)
    print("Message codé : ", c)
    print("\n")
    m2 = rsa.decode(c)
    print('Message décodé : ', m2)

