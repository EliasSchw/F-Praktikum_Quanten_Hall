from cyclotronMass import calculate_cyclotron_mass
import matplotlib.pyplot as plt
import numpy as np
from ChargeCarrierDensity import slicingWithPandas
from scipy import constants as const
from scipy.stats import linregress
from Preprocessing import getDatenreihe
import pandas as pd
from macroswriter import writeLatexMacro

BPeak = 1.05
BPeakFehler = 0.01
Amplitudes = np.array([1.55, 1.90, 2.21, 2.45]) * 10**-6
AmplitudesFehler = Amplitudes * 0.1
cyclotron15, cyclotron21, cyclotron15Error, cyclotron21Error  = calculate_cyclotron_mass(BPeak, BPeakFehler, Amplitudes, AmplitudesFehler)
Mc = [cyclotron15, cyclotron21, cyclotron15, cyclotron21]
McError = [cyclotron15Error, cyclotron21Error, cyclotron15Error, cyclotron21Error]
Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']
def slicingWithPandas(Datenreihen):
    df = pd.DataFrame.from_dict(getDatenreihe(Datenreihen))
    I = df.iloc[:, 3]
    B = df.iloc[:, 0]
    rhoXY = df.iloc[:, 1]
    rhoXX = df.iloc[:, 2]
    return I, B, rhoXY, rhoXX

def calculateSlope(B, rhoXY):
    mask = (B <= 1.2) 
    B_cuttet = B[mask]
    rhoXY_cuttet = rhoXY[mask]
    linReg = linregress(B_cuttet, rhoXY_cuttet)
    slope = linReg[0]
    nError = (linReg[4] / (const.e * slope**2))
    n = (1 / (slope * const.e))
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
    return nTable, nErrorTable, BTable, rhoXYTable, slopeTable

nTable, nErrorTable, BTable, rhoXYTable, slopeTable = getN1(Datenreihen)
kTable = []
kErrorTable = []
EFermiTable = []
EFermiFehlerTable = []
vFermiTable = []
vFermiFehlerTable = []

# Berechnung und Speicherung der Ergebnisse in LaTeX-Makros
for i, datenreihe in enumerate(Datenreihen):
    # Berechnung von k und dessen Fehler
    k = np.sqrt(2 * np.pi * nTable[i])
    kError = (np.pi / k) * nErrorTable[i]
    kTable.append(k)
    kErrorTable.append(kError)

    # Berechnung von EFermi und dessen Fehler
    EFermi = (const.hbar**2 * k**2) / (2 * Mc[i]) / const.e
    EFermiTable.append(EFermi)
    EFermiFehler = EFermi * np.sqrt((2 * kError / k)**2 + (McError[i] / Mc[i])**2)
    EFermiFehlerTable.append(EFermiFehler)

    # Berechnung von vFermi und dessen Fehler
    vFermi = np.sqrt((2 * EFermi * const.e) / Mc[i])  # EFermi wird in Joule umgerechnet
    vFermiTable.append(vFermi)
    vFermiFehler = vFermi * 0.5 * np.sqrt(
        (EFermiFehler / EFermi)**2 + (McError[i] / Mc[i])**2
    )
    vFermiFehlerTable.append(vFermiFehler)

    # Schreiben der Ergebnisse in LaTeX-Makros
    writeLatexMacro(f"kFermi_{datenreihe.replace('.', '_')}", k, r"\text{m}^{-1}", kError)
    writeLatexMacro(f"EFermi_{datenreihe.replace('.', '_')}", EFermi, "eV", EFermiFehler)
    writeLatexMacro(f"vFermi_{datenreihe.replace('.', '_')}", vFermi, "m/s", vFermiFehler)

    # Ausgabe der Ergebnisse in der Konsole
    print(f"{datenreihe}:")
    print(f"  k_Fermi = {k:.3e} ± {kError:.3e} m⁻¹")
    print(f"  E_Fermi = {EFermi:.3e} ± {EFermiFehler:.3e} eV")
    print(f"  v_Fermi = {vFermi:.3e} ± {vFermiFehler:.3e} m/s")




