from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from ChargeCarrierDensity import slicingWithPandas
from scipy import constants as const

def arcsch(x):
    return np.arcsinh(1 / x)

# Funktion für den Fit
def fit_function(B, c1, c2):
    return c1 / (1 + c2 * B**2)

# Datenreihen definieren
Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']
farben = ['blue', 'green', 'orange', 'purple']

# Daten vorbereiten
sigmaXXTable = []
BTable = []
for datenreihe in Datenreihen:
    I, B, rhoXY, rhoXX = slicingWithPandas(datenreihe)
    sigmaXX = rhoXX / (rhoXX**2 + rhoXY**2)  
    sigmaXXTable.append(sigmaXX)  
    BTable.append(B)

# Figuren vorbereiten
plt.figure(figsize=(10, 6))  # Differenzplot
for idx, datenreihe in enumerate(Datenreihen):
    B = BTable[idx]
    sigmaXX = sigmaXXTable[idx]

    # Filter für 1 <= B <= 3
    mask = (B >= 0.5) & (B <= 2)
    B_filtered = B[mask]
    sigmaXX_filtered = sigmaXX[mask]

    # Curve Fit durchführen
    popt, pcov = curve_fit(fit_function, B_filtered, sigmaXX_filtered, p0=[1e-5, 1e-1])
    c1, c2 = popt
    c1_err, c2_err = np.sqrt(np.diag(pcov))
    print(f"Fit-Parameter für '{datenreihe}':")
    print(f"c1 = {c1:.3e} ± {c1_err:.3e}")
    print(f"c2 = {c2:.3e} ± {c2_err:.3e}")

    # Berechnung der Fit-Werte & Differenz
    sigmaXX_fit = fit_function(B_filtered, c1, c2)
    difference = sigmaXX_filtered - sigmaXX_fit

    # Plot der Differenz (alle in eine Figur)
    plt.scatter(B_filtered, difference, label=f"{datenreihe}", color=farben[idx], s=10)

# Styling für Differenzplot
plt.axhline(0, color="black", linestyle="--", linewidth=1)
plt.xlabel("$B$ (T)")
plt.ylabel("Differenz $\\sigma_{XX} - \\text{Fit}$ (S)")
plt.title("Differenz zwischen Daten und Fit für alle Temperaturen")
plt.legend()
plt.grid()
plt.tight_layout()
#plt.show()

# Neue Figur für Daten + Fits
plt.figure(figsize=(10, 6))
for idx, datenreihe in enumerate(Datenreihen):
    B = BTable[idx]
    sigmaXX = sigmaXXTable[idx]

    # Filter für 1 <= B <= 3
    mask = (B >= 0.5) & (B <= 2)
    B_filtered = B[mask]
    sigmaXX_filtered = sigmaXX[mask]

    # Curve Fit wiederholen (optional: speichern und wiederverwenden)
    popt, _ = curve_fit(fit_function, B_filtered, sigmaXX_filtered, p0=[1e-5, 1e-1])
    c1, c2 = popt

    # Plot der Datenpunkte
    plt.scatter(B_filtered, sigmaXX_filtered, label=f"{datenreihe} Daten", color=farben[idx], s=3, alpha=0.2)

    # Fit-Kurve
    B_fit = np.linspace(0.5, 2, 500)
    sigmaXX_fit = fit_function(B_fit, c1, c2)
    plt.plot(B_fit, sigmaXX_fit, label=f"{datenreihe} Fit", color=farben[idx] )

# Styling für Daten + Fit-Plot
plt.xlabel("$B$ (T)")
plt.ylabel("$\\sigma_{XX}$ (S)")
plt.title("Ursprüngliche Daten und Fit-Funktionen für alle Temperaturen")
plt.legend()
plt.grid()
plt.tight_layout()
#plt.show()

# abgelesene values:
BPeak = 1.05
BPeakFehler = 0.01

Amplitudes = np.array([1.55, 1.90, 2.21, 2.45])*10**-6
q = np.array([Amplitudes[2]/Amplitudes[0], Amplitudes[3]/Amplitudes[1]]) #0: 3K/1.5K, 1: 4.2K/2.1K

cyclotronElectron0 = (const.hbar*const.e*BPeak)/(const.m_e*np.pi**2*const.k*1.5)*arcsch(q[0])
cyclotronElectron1 = (const.hbar*const.e*BPeak)/(const.m_e*np.pi**2*const.k*2.1)*arcsch(q[1])
print(cyclotronElectron0)
print(cyclotronElectron1)
