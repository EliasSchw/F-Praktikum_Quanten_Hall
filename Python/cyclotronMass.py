from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from ChargeCarrierDensity import slicingWithPandas
from scipy import constants as const
from macroswriter import writeLatexMacro
from DataPlotter import save_and_open
import DataPlotter as dp
fit_B_min = 0.5
fit_B_max = 1.5
plot_B_min = 0.5
plot_B_max = 1.5
x_value = 0.828

# Funktion für den Fit
def fit_function(B, c1, c2):
    return (c1*c2) / (1 + (c2 * B)**2)

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
def perform_fit(B, sigmaXX, B_min=fit_B_min, B_max=fit_B_max):
    mask = (B >= B_min) & (B <= B_max)
    B_filtered = B[mask]
    sigmaXX_filtered = sigmaXX[mask]
    popt, pcov = curve_fit(fit_function, B_filtered, sigmaXX_filtered, p0=[1e-5, 1e-1])
    return popt, pcov, B_filtered, sigmaXX_filtered


# Funktion zum Plotten der Differenzen mit markierten Punkten
def plot_differences_with_points(Datenreihen, BTable, sigmaXXTable, farben, selected_points):
    plt.figure(figsize=(10, 6))
    for idx, datenreihe in enumerate(Datenreihen):
        B = BTable[idx]
        sigmaXX = sigmaXXTable[idx]
        popt, _, B_filtered, sigmaXX_filtered = perform_fit(B, sigmaXX)
        sigmaXX_fit = fit_function(B_filtered, *popt)
        difference = (-sigmaXX_filtered / sigmaXX_fit)+1

        # Plot der Differenzen
        plt.scatter(B_filtered, difference, label=f"dataset ({datenreihe})", color=farben[idx], s=5)

        # Markiere die ausgewählten Punkte in rot
        if idx < len(selected_points):
            selected_B, selected_sigmaXX = selected_points[idx]
            selected_difference = (-selected_sigmaXX / fit_function(np.array([selected_B]), *popt))+1
            plt.scatter(selected_B, selected_difference, color="red", s=25, label=f"read out value ({datenreihe})")

    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("$B / T$", fontsize = 16)
    plt.ylabel("$\sigma_{XX} / \sigma_{fit} +1$ ", fontsize = 16)
    plt.tick_params(axis='both', which='major', labelsize=12, direction = 'in')
    plt.legend(fontsize = 12)
    plt.grid()
    save_and_open(filename='reducedSigma')

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

# Funktion zur Extraktion der Amplitudenwerte
def get_amplitudes_for_x(x_value, BTable, sigmaXXTable, start_index=0):
    """
    Extrahiert die Amplitudenwerte für einen gegebenen x-Wert (B) aus den Daten.
    Beginnt mit der 4.2K-Kurve (start_index=0).
    """
    Amplitudes = []
    selected_points = []  # Speichert die ausgewählten Punkte für das Plotten

    for idx in range(start_index, len(BTable)):
        B = BTable[idx]
        sigmaXX = sigmaXXTable[idx]

        # Finde den Index des nächstgelegenen x-Werts
        closest_index = np.argmin(np.abs(B - x_value))

        # Extrahiere den entsprechenden Amplitudenwert
        amplitude = sigmaXX[closest_index]
        Amplitudes.append(amplitude)

        # Speichere den Punkt für das Plotten
        selected_points.append((B[closest_index], sigmaXX[closest_index]))

    return np.array(Amplitudes), selected_points

# Funktion zum Plotten der Daten und Fits mit markierten Punkten
def plot_data_and_fits_with_points(Datenreihen, BTable, sigmaXXTable, farben):
    plt.figure(figsize=(10, 6))
    for idx, datenreihe in enumerate(Datenreihen):
        B = BTable[idx]
        sigmaXX = sigmaXXTable[idx]
        popt, _, B_filtered, sigmaXX_filtered = perform_fit(B, sigmaXX)

        # Plot der Daten als durchgezogene Linie
        plt.plot(B_filtered, sigmaXX_filtered * 10**5, label=f"data ({datenreihe})", color=farben[idx], linewidth=1.5)

        # Plot des Fits als gestrichelte Linie
        B_fit = np.linspace(plot_B_min, plot_B_max, 1000)
        sigmaXX_fit = fit_function(B_fit, *popt)
        plt.plot(B_fit, sigmaXX_fit * 10**5, label=f"fit ({datenreihe})", color=farben[idx], linestyle="--", linewidth=1.5)

    plt.xlabel(r"$B / T$", fontsize = 16)
    plt.ylabel(r"$\sigma_{\text{xx}} / S$", fontsize = 16)
    plt.xlim(1,1.5)
    plt.ylim(1,3.5)
    plt.legend(fontsize = 12)
    plt.tick_params(axis='both', which='major', labelsize=12, direction = 'in')
    plt.grid()
    plt.tight_layout()
    save_and_open(filename='sigmaWithFit')
# Hauptfunktion
def main():
    Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']
    farben = ['blue', 'green', 'orange', 'purple']

    # Daten vorbereiten
    sigmaXXTable, BTable = prepare_data(Datenreihen)

    # Vorgabe des x-Werts (B-Wert)
    

    # Amplituden für den gegebenen x-Wert extrahieren
    Amplitudes, selected_points = get_amplitudes_for_x(x_value, BTable, sigmaXXTable)

    # Fehler für die Amplituden berechnen (10% der Amplitudenwerte)
    AmplitudesFehler = Amplitudes * 0.1

    # Zyklotronmasse berechnen
    BPeak = x_value
    BPeakFehler = 0.01
    cyclotron15, cyclotron21, cyclotron15Error, cyclotron21Error = calculate_cyclotron_mass(BPeak, BPeakFehler, Amplitudes, AmplitudesFehler)

    # Makros für die Zyklotronmasse schreiben
    writeLatexMacro("cyclotronMass_1_5K", cyclotron15, r"\text{kg}", cyclotron15Error)
    writeLatexMacro("cyclotronMass_2_1K", cyclotron21, r"\text{kg}", cyclotron21Error)

    # Ergebnisse ausgeben
    print(f"Zyklotronmasse bei 1.5K: {(cyclotron15/const.m_e):.3e} ± {(cyclotron15Error/const.m_e):.3e} kg")
    print(f"Zyklotronmasse bei 2.1K: {(cyclotron21/const.m_e):.3e} ± {(cyclotron21Error/const.m_e):.3e} kg")

    # Plot der Differenzen mit markierten Punkten
    plot_differences_with_points(Datenreihen, BTable, sigmaXXTable, farben, selected_points)
    plot_data_and_fits_with_points(Datenreihen, BTable, sigmaXXTable, farben)
# Skript ausführen

if __name__ == "__main__":
    main()


