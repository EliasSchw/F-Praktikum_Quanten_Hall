from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from ChargeCarrierDensity import slicingWithPandas

# Funktion für den Fit
def fit_function(B, c1, c2):
    return c1 / (1 + c2 * B**2)

# Datenreihen definieren
Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']

# Daten vorbereiten
sigmaXXTable = []
BTable = []
for datenreihe in Datenreihen:
    I, B, rhoXY, rhoXX = slicingWithPandas(datenreihe)
    sigmaXX = rhoXX / (rhoXX**2 + rhoXY**2)  
    sigmaXXTable.append(sigmaXX)  
    BTable.append(B)

# Beispiel: Fit für die Datenreihe '4.2K'
BVierK = BTable[0]
sigmaXXVierK = sigmaXXTable[0]

# Filter für 1 <= B < 2
mask = (BVierK >= 1) & (BVierK < 2)
B_filtered = BVierK[mask]
sigmaXX_filtered = sigmaXXVierK[mask]

# Curve Fit durchführen
popt, pcov = curve_fit(fit_function, B_filtered, sigmaXX_filtered, p0=[1e-5, 1e-1])
c1, c2 = popt
c1_err, c2_err = np.sqrt(np.diag(pcov))
print(f"Fit-Parameter für '4.2K':")
print(f"c1 = {c1:.3e} ± {c1_err:.3e}")
print(f"c2 = {c2:.3e} ± {c2_err:.3e}")

# Berechnung der Differenz (Daten - Fit)
sigmaXX_fit = fit_function(B_filtered, c1, c2)
difference = sigmaXX_filtered - sigmaXX_fit

# Plot der Differenz
plt.scatter(B_filtered, difference, label="Differenz (Daten - Fit)", color="blue", s=10)
plt.axhline(0, color="red", linestyle="--", label="Null-Linie")
plt.xlabel("$B$ (T)")
plt.ylabel("Differenz $\\sigma_{XX} - \\text{Fit}$ (S)")
plt.title("Differenz zwischen Daten und Fit für 4.2K")
plt.legend()
plt.grid()
plt.show()