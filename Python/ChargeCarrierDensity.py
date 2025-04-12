from Preprocessing import getDatenreihe
import matplotlib.pyplot as plt
import numpy as np
from macroswriter import writeLatexMacro
import pandas as pd
from scipy.stats import linregress
from scipy import constants as const
from macroswriter import writeLatexCSname
import DataPlotter as plotter

Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']
def slicingWithPandas(Datenreihen):
    df = pd.DataFrame.from_dict(getDatenreihe(Datenreihen))
    I = df.iloc[:, 3]
    B = df.iloc[:, 0]
    rhoXY = df.iloc[:, 1]
    rhoXX = df.iloc[:, 2]
    return I, B, rhoXY, rhoXX


def calculateSlope(B, rhoXY):
    mask = (B <= 1) 
    B_cuttet = B[mask]
    rhoXY_cuttet = rhoXY[mask]
    linReg = linregress(B_cuttet, rhoXY_cuttet)
    slope = linReg[0]
    nError = (linReg[4] / (const.e * slope**2))/10**15
    n = (1 / (slope * const.e))/10**15
    return n, nError, slope

def getN1(Datenreihen):
    nTable = []
    nErrorTable = []
    slopeTable = []
    BTable = []
    rhoXYTable = []
    rhoXXTable = []
    for i in Datenreihen:
        I, B, rhoXY, rhoXX = slicingWithPandas(i)
        n, nError, slope = calculateSlope(B, rhoXY)
        slopeTable.append(slope)
        nTable.append(n)
        nErrorTable.append(nError)
        BTable.append(B)
        rhoXYTable.append(rhoXY)
        rhoXXTable.append(rhoXX)
    return nTable, nErrorTable, BTable, rhoXYTable, slopeTable, rhoXXTable

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

def calculate_mean_n_and_error(nu, Bn2, Bn2Error, temperatures, scale_factor=10**15):
    e = const.e
    h = const.h

    n2 = (nu * Bn2 * e) / h
    n2_error = ((nu * e) / h) * (Bn2Error / Bn2)
    
    # Mittelwert und Fehler über Spalten berechnen
    mean_n_by_temperature = np.mean(n2, axis=0)  # Mittelwert über Spalten
    mean_n_error_by_temperature = np.sqrt(np.sum(n2_error**2, axis=0)) / np.sqrt(n2.shape[0])  # Fehler über Spalten
    
    # Skalierung anwenden
    mean_n_by_temperature /= scale_factor
    mean_n_error_by_temperature /= scale_factor

    #print("Berechnete Mittelwerte und Fehler für n:")
    #for idx, temp in enumerate(temperatures):
        #print(f"  Temperatur: {temp}")
        #print(f"    Mittelwert von n: {mean_n_by_temperature[idx]:.3e} ± {mean_n_error_by_temperature[idx]:.3e}")

    return mean_n_by_temperature, mean_n_error_by_temperature

def writeCSMacros(mean_n_by_temperature, mean_n_error_by_temperature, temperatures):
    """
    Schreibt die Makros für n2-Werte in die Datei macros.tex mit der Methode writeCSMacros.
    """
    for i in range(len(temperatures)):
        macro_name = f"nEins_{temperatures[i]}"
        writeLatexCSname(macro_name, value=nTable[i], error = nErrorTable[i], noBrackets=True, )

def writeCSMacrosForN2(mean_n_by_temperature, mean_n_error_by_temperature, temperatures):
    """
    Schreibt die Makros für N2-Werte in die Datei macros.tex mit der Methode writeCSMacros.
    """
    for i in range(len(temperatures)):
        macro_name = f"nZwei_{temperatures[i]}"
        writeLatexCSname(macro_name, value = mean_n_by_temperature[i], error = mean_n_error_by_temperature[i], noBrackets=True)

# --- Datenbasis ---

temperatures = ['4.2K', '3K', '2.1K', '1.4K']

nu = np.array([[1, 1, 1, 1],
               [2, 2, 2, 2],
               [3, 3, 3, 3],
               [4, 4, 4, 4]])

Bn2 = np.array([[8.2, 8.1, 7.9, 7.8],  
                [4.4, 4.4, 4.4, 4.4],  
                [3.01, 3.01, 3.01, 3.01],  
                [2.25, 2.26, 2.26, 2.26]])

Bn2Error = np.array([[0.1, 0.1, 0.1, 0.1],  
                     [0.07, 0.07, 0.07, 0.07],  
                     [0.05, 0.05, 0.05, 0.05],  
                     [0.01, 0.01, 0.01, 0.01]])



#Elias

def plot_ns():
    gates=['1.4K', 'Gate_minus_1_5V', 'Gate_minus_1V', 'Gate_1V', 'Gate_1_5V']
    #gates=['1.4K',  'Gate_1V', 'Gate_1_5V']

    nTable, nErrorTable, BTable, rhoXYTable, slopeTable, rhoXXTable = getN1(gates)
    datenreihen = [getDatenreihe(name) for name in gates]
    plt.scatter([datenreihe['U_gate'] for datenreihe in datenreihen], nTable)
    plt.xlabel(r'$U_\text{gate}\,/\,V$')
    plt.ylabel(r'$n / 10^{15}\,m^2$')
    plt.gca().invert_xaxis()
    
    # Perform linear fit
    U_gate = np.array([datenreihe['U_gate'] for datenreihe in datenreihen])
    nTable = np.array(nTable)
    slope, intercept, _, _, _ = linregress(U_gate, nTable)

    # Generate fit line
    U_gate_fit = np.linspace(-2, max(U_gate), 100)
    n_fit = slope * U_gate_fit + intercept

    # Plot the fit line
    plt.plot(U_gate_fit, n_fit, label=f'Linear Fit: $n = {slope:.2e} U_{{gate}} + {intercept:.2e}$', color='red')
    plt.legend()
    plotter.fancyGraph()  
    plotter.save_and_open()


plot_ns()





# --- Berechnung ---

mean_n_by_temperature, mean_n_error_by_temperature = calculate_mean_n_and_error(nu, Bn2, Bn2Error, temperatures)

nTable, nErrorTable, BTable, rhoXYTable, slopeTable, rhoXXTable = getN1(temperatures)

# Makros schreiben mit writeCSMacros
writeCSMacros(mean_n_by_temperature, mean_n_error_by_temperature, temperatures)

# --- Makros schreiben mit writeCSMacros für N2 ---
writeCSMacrosForN2(mean_n_by_temperature, mean_n_error_by_temperature, temperatures)


