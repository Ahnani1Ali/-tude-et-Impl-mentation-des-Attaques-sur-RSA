from fractions import Fraction
import math

# Algorithme pour obtenir les fractions continues de e/n
def continued_fraction(e, n):
    cf = []
    while n:
        q = e // n
        cf.append(q)
        e, n = n, e - q * n
    return cf

# Renvoie les convergents de la fraction continue
def convergents(cf):
    convs = []
    for i in range(1, len(cf) + 1):
        frac = Fraction(0)
        for x in reversed(cf[:i]):
            frac = 1 / frac if frac else 0
            frac += x
        convs.append((frac.numerator, frac.denominator))
    return convs

# Tente de résoudre une équation quadratique : x^2 - a x + b = 0
def is_perfect_square(x):
    s = math.isqrt(x)
    return s * s == x

# Teste si un couple (k,d) peut être la bonne clé privée
def is_valid_d(e, n, k, d):
    if k == 0:
        return False
    # phi = (ed - 1)/k doit être entier
    if (e * d - 1) % k != 0:
        return False
    phi = (e * d - 1) // k
    # Trouver racines de x^2 - (n - phi + 1)x + n = 0
    s = n - phi + 1
    discrim = s * s - 4 * n
    if discrim < 0 or not is_perfect_square(discrim):
        return False
    return True

# Attaque de Wiener
def wiener_attack(e, n):
    cf = continued_fraction(e, n)
    convs = convergents(cf)
    for k, d in convs:
        if d == 0:
            continue
        if is_valid_d(e, n, k, d):
            return d
    return None

# Exemple vulnérable à Wiener : petit d
def generate_vulnerable_rsa():
    p = 26513
    q = 32321
    n = p * q
    phi = (p - 1) * (q - 1)
    d = 947  # petit d < n^0.25
    e = pow(d, -1, phi)
    return e, d, n

if __name__ == "__main__":
    e, d_real, n = generate_vulnerable_rsa()
    print(f"Clé publique : (n={n}, e={e})")
    print(f"Clé privée réelle : d = {d_real}")

    d_found = wiener_attack(e, n)
    if d_found:
        print(f"[✔] d trouvé par l’attaque de Wiener : {d_found}")
    else:
        print("[✘] Aucune clé trouvée (pas vulnérable à Wiener).")
