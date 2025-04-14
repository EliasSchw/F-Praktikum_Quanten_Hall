from ChargeCarrierDensity import getN1
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import DataPlotter as dp
from macroswriter import writeLatexMacro

Gates = ['-1.5', '-1', '-0.25', '1', '1.5', '-2']
# Datenbasis
Data = ['Gate_minus_1_5V', 'Gate_minus_1V', '1.4K_switched', 'Gate_1V', 'Gate_1_5V', 'Gate_minus_2V']
def writeN1Macros(nTable, nErrorTable, temperatures):
    """
    Schreibt die Makros für n1-Werte in die Datei macros.tex.
    """
    for i in range(len(temperatures)-1):
        macro_name = f"n_{temperatures[i+1].replace('.', '').replace('K', '')}"  
        writeLatexMacro(macro_name, nTable[i+1], unit=r"\text{m}^{-2}", error=nErrorTable[i],
                        filepath="Paper/Latex/macros.tex")
    writeLatexMacro('n-15', nTable[0]*-1,unit=r"\text{m}^{-2}", error=nErrorTable[0],
                        filepath="Paper/Latex/macros.tex")
# Daten extrahieren
nTable, nErrorTable, BTable, rhoXYTable, slopeTable, rhoXXTable = getN1(Data)

writeN1Macros(nTable, nErrorTable, Gates)
# Plot für rhoXY und rhoXX
plt.figure(figsize=(10, 6))
plt.plot(BTable[0], rhoXYTable[0]/1000, label=r"$\rho_{XY}$", color="blue")
plt.plot(BTable[0], rhoXXTable[0]/1000, label=r"$\rho_{XX}$", color="red")
plt.xlabel(r"$B$ (T)")
plt.ylabel(r"$\rho$ ($k\Omega$)")
plt.title('Gate Voltage = -1.5V')
plt.legend()
dp.fancyGraph()
plt.show()