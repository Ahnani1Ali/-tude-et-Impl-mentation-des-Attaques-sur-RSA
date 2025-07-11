# Étude et Implémentation d'Attaques sur RSA

Ce projet présente une étude approfondie et des implémentations en Python de plusieurs attaques connues contre le système cryptographique RSA. Il s’inscrit dans le cadre du cours **Cryptanalyse et Sécurité des Systèmes** (ISMIN 1A - EI24).

## 📄 Objectif du projet

L’objectif est double :
1. **Comprendre les fondements mathématiques** du chiffrement RSA, des réseaux euclidiens et des approximations rationnelles.
2. **Mettre en œuvre des attaques pratiques**, notamment :
   - l’**attaque de Wiener** (petite clé privée `d`),
   - l’**attaque de Coppersmith** (petites racines modulo N).

Toutes les méthodes sont présentées dans le rapport `Etude des attaques sur RSA.pdf`.

---

## Contenu du projet

- `rsa.py` : Génération de clés RSA, chiffrement et déchiffrement.
- `wiener_attack.py` : Implémentation complète de l’attaque de Wiener par fractions continues.
- `LLL.py` : Réduction de bases par l'algorithme de Lenstra–Lenstra–Lovász.
- `coppersmith.py` : Construction de bases pour l'attaque de Coppersmith et exploitation via LLL.
- `Etude des attaques sur RSA.pdf` : Rapport théorique illustrant les fondements et les résultats.

---

## Résultats obtenus

-  **Wiener** : l’attaque retrouve efficacement la clé privée lorsque \( d < n^{0.25} \). Testée avec succès sur des clés vulnérables générées dans le script.
-  **Coppersmith** : base construite et réduite par LLL, les racines trouvées sont pertinentes si les conditions sur \( X, d, h \) sont respectées. Implémentation validée structurellement mais nécessite une adaptation à des cas réels pour exploitation complète.

---

##  Principaux outils mathématiques

- Exponentiation modulaire, PGCD étendu
- Réseaux euclidiens et base réduite (LLL)
- Approximation par fractions continues
- Polynômes et manipulation via `numpy.polynomial`

---

##  Références

- Wiener, M. J. (1990). *Cryptanalysis of short RSA secret exponents*. IEEE.
- Coppersmith, D. (1996). *Finding a small root of a univariate modular equation*. EUROCRYPT.
- Rapport complet : [`Etude des attaques sur RSA.pdf`](Etude%20des%20attaques%20sur%20RSA.pdf)

---

## Exécution

```bash
# Exemple : tester l'attaque de Wiener
python wiener_attack.py

# Exemple : tester la réduction LLL sur une base pour Coppersmith
python coppersmith.py
