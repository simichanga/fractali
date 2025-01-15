import numpy as np
import matplotlib.pyplot as plt

def newton_raphson_basins(x_min, x_max, y_min, y_max, resolution, max_iter, tol):
    """
    Reprezintă bazinul de atracție pentru o funcție folosind metoda Newton-Raphson.
    
    :param x_min: Limita inferioară pentru axa x
    :param x_max: Limita superioară pentru axa x
    :param y_min: Limita inferioară pentru axa y
    :param y_max: Limita superioară pentru axa y
    :param resolution: Rezoluția imaginii (număr de puncte per axă)
    :param max_iter: Numărul maxim de iterații permise
    :param tol: Toleranța pentru convergență
    :return: Harta bazinelor de atracție (imagine)
    """
    # Definirea funcției polinomiale și a derivatelor
    def func(z):
        return z**3 - 1  # Polinomul z^3 - 1 (rădăcinile sunt 1, ω, ω^2)

    def derivative(z):
        return 3 * z**2

    # Configurarea grid-ului complex
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y  # Plane complex

    # Inițializăm matricea pentru rezultate
    roots = []
    convergence = np.zeros(Z.shape, dtype=int)

    # Iterăm pentru fiecare punct din grilă
    for i in range(max_iter):
        Z_prev = Z
        Z = Z - func(Z) / derivative(Z)  # Newton-Raphson update

        # Calculăm eroarea
        delta = np.abs(Z - Z_prev)

        # Identificăm rădăcinile
        for root_idx, root in enumerate(roots):
            mask = np.abs(Z - root) < tol
            convergence[mask] = root_idx + 1
            Z[mask] = root

        # Adăugăm noile rădăcini găsite
        mask_new_root = (delta < tol) & (convergence == 0)
        new_roots = Z[mask_new_root]
        if len(new_roots) > 0:
            for new_root in new_roots:
                if all(np.abs(new_root - r) > tol for r in roots):
                    roots.append(new_root)

    return convergence, X, Y, roots

# Configurarea parametrilor
x_min, x_max = -2, 2
y_min, y_max = -2, 2
resolution = 500
max_iter = 50
tol = 1e-6

# Generarea bazinelor de atracție
convergence, X, Y, roots = newton_raphson_basins(x_min, x_max, y_min, y_max, resolution, max_iter, tol)

# Afișarea graficului
plt.figure(figsize=(8, 8))
plt.imshow(convergence, extent=(x_min, x_max, y_min, y_max), cmap="viridis", origin="lower")
plt.colorbar(label="Bazinul de atracție (Index rădăcină)")
plt.title("Bazele de Atracție pentru z^3 - 1")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.grid(False)
plt.show()
