from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from ChargeCarrierDensity import slicingWithPandas
from scipy import constants as const
from macroswriter import writeLatexMacro

# Funktion für den Fit
def fit_function(B, c1, c2):
    return c1 / (1 + c2 * B**2)

# Funktion zur Datenvorbereitung
def prepare_data(Datenreihen):
    sigmaXXTable = []
    BTable = []
    for datenreihe in Datenreihen:
        I, B, rhoXY, rhoXX = slicingWithPandas(datenreihe)
        sigmaXX = rhoXX / (rhoXX**2 + rhoXY**2)
        sigmaXXTable.append(sigmaXX)
        BTable.append(B)
    return sigmaXXTable, BTable

# Funktion zur Durchführung des Fits
def perform_fit(B, sigmaXX, B_min=0.5, B_max=2):
    mask = (B >= B_min) & (B <= B_max)
    B_filtered = B[mask]
    sigmaXX_filtered = sigmaXX[mask]
    popt, pcov = curve_fit(fit_function, B_filtered, sigmaXX_filtered, p0=[1e-5, 1e-1])
    return popt, pcov, B_filtered, sigmaXX_filtered

# Funktion zum Plotten der Differenzen
def plot_differences(Datenreihen, BTable, sigmaXXTable, farben):
    plt.figure(figsize=(10, 6))
    for idx, datenreihe in enumerate(Datenreihen):
        B = BTable[idx]
        sigmaXX = sigmaXXTable[idx]
        popt, _, B_filtered, sigmaXX_filtered = perform_fit(B, sigmaXX)
        sigmaXX_fit = fit_function(B_filtered, *popt)
        difference = sigmaXX_filtered - sigmaXX_fit
        plt.scatter(B_filtered, difference, label=f"{datenreihe}", color=farben[idx], s=10)
    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("$B$ (T)")
    plt.ylabel("Differenz $\\sigma_{XX} - \\text{Fit}$ (S)")
    plt.title("Differenz zwischen Daten und Fit für alle Temperaturen")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Funktion zum Plotten der Daten und Fits
def plot_data_and_fits(Datenreihen, BTable, sigmaXXTable, farben):
    plt.figure(figsize=(10, 6))
    for idx, datenreihe in enumerate(Datenreihen):
        B = BTable[idx]
        sigmaXX = sigmaXXTable[idx]
        popt, _, B_filtered, sigmaXX_filtered = perform_fit(B, sigmaXX)
        plt.scatter(B_filtered, sigmaXX_filtered, label=f"{datenreihe} Daten", color=farben[idx], s=3, alpha=0.2)
        B_fit = np.linspace(0.5, 2, 500)
        sigmaXX_fit = fit_function(B_fit, *popt)
        plt.plot(B_fit, sigmaXX_fit, label=f"{datenreihe} Fit", color=farben[idx])
    plt.xlabel("$B$ (T)")
    plt.ylabel("$\\sigma_{XX}$ (S)")
    plt.title("Ursprüngliche Daten und Fit-Funktionen für alle Temperaturen")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Funktion zur Berechnung der Zyklotronmasse
def calculate_cyclotron_mass(BPeak, BPeakFehler, Amplitudes, AmplitudesFehler):
    q = np.array([Amplitudes[2] / Amplitudes[0], Amplitudes[3] / Amplitudes[1]])
    qError = np.array([q[0]*np.sqrt((AmplitudesFehler[2]/Amplitudes[2])**2+(AmplitudesFehler[0]/Amplitudes[0])**2), q[1]*np.sqrt((AmplitudesFehler[3]/Amplitudes[3])**2+(AmplitudesFehler[1]/Amplitudes[1])**2)])  
    cyclotronElectron15 = (const.hbar * const.e * BPeak) / (const.m_e * np.pi**2 * const.k * 1.5) * arcsch(q[0])
    cyclotronElectron21 = (const.hbar * const.e * BPeak) / (const.m_e * np.pi**2 * const.k * 2.1) * arcsch(q[1])
    a15 = (const.hbar * const.e) / (const.m_e * np.pi**2 * const.k * 1.5)
    a21 = (const.hbar * const.e) / (const.m_e * np.pi**2 * const.k * 2.1)
    cyclotron15Error = np.sqrt((a15*arcsch(q[0])*BPeakFehler)**2+(a15*BPeak*(1/(np.sqrt(q[0]**2+1))*qError[0]))**2)*const.m_e
    cyclotron21Error = np.sqrt((a21*arcsch(q[1])*BPeakFehler)**2+(a21*BPeak*(1/(np.sqrt(q[1]**2+1))*qError[1]))**2)*const.m_e
    cyclotron15 = cyclotronElectron15 * const.m_e
    cyclotron21 = cyclotronElectron21 * const.m_e
    return cyclotron15, cyclotron21, cyclotron15Error, cyclotron21Error

# Funktion zur Berechnung von arcsinh
def arcsch(x):
    return np.arcsinh(1 / x)

# Hauptfunktion
def main():
    Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']
    farben = ['blue', 'green', 'orange', 'purple']

    # Daten vorbereiten
    sigmaXXTable, BTable = prepare_data(Datenreihen)

    # Plot der Differenzen
    #plot_differences(Datenreihen, BTable, sigmaXXTable, farben)

    # Plot der Daten und Fits
    #plot_data_and_fits(Datenreihen, BTable, sigmaXXTable, farben)

    # Zyklotronmasse berechnen
    BPeak = 1.05
    BPeakFehler = 0.01
    Amplitudes = np.array([1.55, 1.90, 2.21, 2.45]) * 10**-6
    AmplitudesFehler = Amplitudes * 0.1
    cyclotron15, cyclotron21, cyclotron15Error, cyclotron21Error = calculate_cyclotron_mass(BPeak, BPeakFehler, Amplitudes, AmplitudesFehler)

    # Makros für die Zyklotronmasse schreiben
    writeLatexMacro("cyclotronMass_1_5K", cyclotron15, r"\text{kg}", cyclotron15Error)
    writeLatexMacro("cyclotronMass_2_1K", cyclotron21, r"\text{kg}", cyclotron21Error)

    # Ergebnisse ausgeben
    print(f"Zyklotronmasse bei 1.5K: {cyclotron15:.3e} ± {cyclotron15Error:.3e} kg")
    print(f"Zyklotronmasse bei 2.1K: {cyclotron21:.3e} ± {cyclotron21Error:.3e} kg")

# Skript ausführen
if __name__ == "__main__":
    main()


