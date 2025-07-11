import numpy as np

class Basis:
    # Les constructeurs de cet objet sont : une matrice représentant la base, 
    # une matrice contenant les mu_{i,j} et un vecteur contenant les B_i
    def __init__(self, basis):
        self.basis = basis
        self.gram_schmidt()

    # Calcule, pour une base, les coefficients de Gram–Schmidt
    def gram_schmidt(self):
        basis = self.basis
        n = len(basis)
        m = len(basis[0])
        orthogonal_basis = np.copy(basis)

        # Matrices contenant les coefficients de Gram–Schmidt
        mu = np.zeros((n, m))
        B = np.zeros(n)
        B[0] = np.dot(basis[0], basis[0])

        for i in range(1, n):
            for j in range(i):
                mu[i, j] = np.dot(basis[i], orthogonal_basis[j]) / np.dot(orthogonal_basis[j], orthogonal_basis[j])
                orthogonal_basis[i] -= mu[i, j] * orthogonal_basis[j]
            B[i] = np.dot(orthogonal_basis[i], orthogonal_basis[i])

        self.mu = mu
        self.B = B

    # Échange b_k et b_{k-1} et calcule les nouveaux coefficients de Gram–Schmidt
    def lovasz(self, self_, k):
        m = self_.basis
        mu0 = self_.mu
        B = self_.B

        m[[k, k - 1]] = m[[k - 1, k]]  # Échange b_k et b_{k-1}
        mu0[[k, k - 1]] = mu0[[k - 1, k]]
        B[k], B[k - 1] = B[k - 1], B[k]

        mu0[k, k - 1] = mu0[k, k - 1] * B[k] / B[k - 1]
        for i in range(k + 1, len(m)):
            tmp = self_.mu[i, k]
            self_.mu[i, k] = self_.mu[i, k - 1]
            self_.mu[i, k - 1] = tmp - mu0[k, k - 1] * self_.mu[i, k]

        # Actualisation des coefficients de Gram–Schmidt
        for i in range(k + 1, len(m)):
            for j in range(k - 1, k + 1):
                self_.mu[i, j] = self_.mu[i, j] - round(self_.mu[i, k]) * self_.mu[k, j]
        self_.mu[k, k - 1] = 0

        return max(k - 1, 1)

    # Opère la transformation b_k ← b_k − [mu_{k,k−1}]b_{k−1} et actualise les coefficients de Gram–Schmidt
    def taille(self, self_, k):
        if abs(self_.mu[k, k - 1]) > 0.5 + 10**(-12):
                # Le + 10^(-12) permet de résoudre un dysfonctionnement dans le cas d’égalité
            self_.basis[k] = self_.basis[k] - round(self_.mu[k, k - 1]) * self_.basis[k - 1]

        # Actualisation des coefficients de Gram–Schmidt
            for j in range(k - 1):
                self_.mu[k, j] = self_.mu[k, j] - round(self_.mu[k, k - 1]) * self_.mu[k - 1, j]
            self_.mu[k, k - 1] = self_.mu[k, k - 1] - round(self_.mu[k, k - 1])

    # Applique l’algorithme LLL à la base
    def lll(self):
        n = len(self.basis)
        self.gram_schmidt()
        k = 1
        while k < n:
            if self.taille(self, k) > self.B[k] + self.mu[k, k - 1] * self.B[k - 1]:
                k = self.lovasz(self, k)
                continue
            for l in range(k - 1, -1, -1):
                self.taille(self, k)
            k += 1

if __name__ == "__main__":
    a = np.array([[1.7, 2.5], [9.5, 46.0]])
    b = Basis(a)
    print("Base d’entrée :\n", b.basis)

    b.lll()
    print("Base réduite :\n", b.basis)

    a = np.array([[1., 1., 1., 0., 2.], [3., 5., 6., 0., 1.]])
    b = Basis(a)
    print("Base d’entrée :\n", b.basis)

    b.lll()
    print("Base réduite :\n", b.basis)

