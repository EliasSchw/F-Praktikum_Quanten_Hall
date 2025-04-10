from Preprocessing import getDatenreihe
import matplotlib.pyplot as plt
import numpy as np
from macroswriter import writeLatexMacro
import pandas as pd
from scipy.stats import linregress
from scipy import constants as const

Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']

def slicingWithPandas(Datenreihen):
    df = pd.DataFrame.from_dict(getDatenreihe(Datenreihen))
    I = df.iloc[:, 0]
    B = df.iloc[:, 1]
    rhoXY = df.iloc[:, 2]
    rhoXX = df.iloc[:, 3]
    return I, B, rhoXY, rhoXX

def calculateSlope(B, rhoXY):
    mask = (B <= 1) & (B >= 0) 
    B_cuttet = B[mask]
    rhoXY_cuttet = rhoXY[mask]
    linReg = linregress(B_cuttet, rhoXY_cuttet)
    slope = linReg[0]
    nError = linReg[4]
    n = 1 / (slope * const.e)
    return n, nError, slope

def getN1(Datenreihen):
    nTable = []
    nErrorTable = []
    slopeTable = []
    BTable = []
    rhoXYTable = []
    for i in Datenreihen:
        I, B, rhoXY, rhoXX = slicingWithPandas(i)
        n, nError, slope = calculateSlope(B, rhoXY)
        slopeTable.append(slope)
        nTable.append(n)
        nErrorTable.append(nError)
        BTable.append(B)
        rhoXYTable.append(rhoXY)
        #print(nTable)
        #print(nErrorTable)
    return nTable, nErrorTable, BTable, rhoXYTable, slopeTable

def allLinFitsPlotting(Datenreihen):
    plt.figure(figsize=(10, 8))
    for idx, datenreihe in enumerate(Datenreihen):
        I, B, rhoXY, rhoXX = slicingWithPandas(datenreihe)
        n, nError, slope = calculateSlope(B, rhoXY)
        plt.scatter(B, rhoXY, label=f"{datenreihe} Daten", s=1)
        B_fit = np.linspace(min(B), max(B), 100) 
        rhoXY_fit = slope * B_fit  
        plt.plot(B_fit, rhoXY_fit, label=f"{datenreihe} linear fit")
    plt.xlabel("$B$ (T)")
    plt.ylabel("$\\rho_{xy}$ ($\\Omega$)")
    plt.title("Alle Kurven mit linearem Fit")
    plt.legend()
    plt.grid()
    plt.show()


def calculate_mean_n_and_error(n2, Bn2_by_temperature, Bn2Error, temperatures):
    """
    Berechnet den Mittelwert von n und den zugehörigen Fehler für jede Temperatur.

    Args:
        n2 (np.array): Array mit den berechneten n-Werten.
        Bn2_by_temperature (np.array): Transponiertes Array von Bn2, gruppiert nach Temperatur.
        Bn2Error (np.array): Array mit den Fehlern von Bn2.
        temperatures (list): Liste der Temperaturwerte.

    Returns:
        None: Gibt die Ergebnisse direkt aus.
    """
    # Fehler in n berechnen
    n2_error = n2 * (Bn2Error.T / Bn2_by_temperature)  # Relativer Fehler von Bn2 auf n übertragen

    # Mittelwerte und Fehler berechnen
    mean_n_by_temperature = np.mean(n2, axis=1)
    mean_n_error_by_temperature = np.sqrt(np.sum((Bn2Error.T / Bn2_by_temperature)**2, axis=1)) * mean_n_by_temperature

    # Ergebnisse ausgeben
    for idx, temp in enumerate(temperatures):
        print(f"Temperatur: {temp}")
        print(f"  Mittelwert von n: {mean_n_by_temperature[idx]:.3e} ± {mean_n_error_by_temperature[idx]:.3e}")


def calculate_mean_n_and_error_to_macros(n2, Bn2_by_temperature, Bn2Error, temperatures, macro_prefix="n", filepath="Paper/Latex/macros.tex"):
    """
    Berechnet den Mittelwert von n und den zugehörigen Fehler für jede Temperatur und schreibt sie in LaTeX-Makros.

    Args:
        n2 (np.array): Array mit den berechneten n-Werten.
        Bn2_by_temperature (np.array): Transponiertes Array von Bn2, gruppiert nach Temperatur.
        Bn2Error (np.array): Array mit den Fehlern von Bn2.
        temperatures (list): Liste der Temperaturwerte.
        macro_prefix (str): Präfix für die LaTeX-Makronamen.
        filepath (str): Pfad zur LaTeX-Makrodatei.

    Returns:
        None
    """
    # Fehler in n berechnen
    n2_error = n2 * (Bn2Error.T / Bn2_by_temperature)  # Relativer Fehler von Bn2 auf n übertragen

    # Mittelwerte und Fehler berechnen
    mean_n_by_temperature = np.mean(n2, axis=1)
    mean_n_error_by_temperature = np.sqrt(np.sum((Bn2Error.T / Bn2_by_temperature)**2, axis=1)) * mean_n_by_temperature

    # Ergebnisse ausgeben und in LaTeX-Makros schreiben
    for idx, temp in enumerate(temperatures):
        print(f"Temperatur: {temp}")
        print(f"  Mittelwert von n: {mean_n_by_temperature[idx]:.3e} ± {mean_n_error_by_temperature[idx]:.3e}")
        
        # Schreibe die Werte in die LaTeX-Makros
        macro_name = f"{macro_prefix}_{temp.replace('.', '').replace('K', '')}"  # Erzeuge Makronamen
        writeLatexMacro(macro_name, mean_n_by_temperature[idx], unit="cm^{-2}", error=mean_n_error_by_temperature[idx], filepath=filepath)


nu = np.array([[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]])  
Bn2 = np.array([[8.2, 8.1, 7.9, 7.8],  
                [4.4, 4.4, 4.4, 4.4],  
                [3.01, 3.01, 3.01, 3.01],  
                [2.25, 2.26, 2.26, 2.26]])  

temperatures = ['4.2K', '3K', '2.1K', '1.4K']
Bn2_by_temperature = Bn2.T 
n2 = (nu.T * Bn2_by_temperature * const.e) / const.h
Bn2Error = np.array([[0.1, 0.1, 0.1, 0.1],  
                     [0.01, 0.01, 0.01, 0.01],  
                     [0.05, 0.05, 0.05, 0.05],  
                     [0.01, 0.01, 0.01, 0.01]])
calculate_mean_n_and_error(n2, Bn2_by_temperature, Bn2Error, temperatures)



