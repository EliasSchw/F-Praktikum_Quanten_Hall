from ChargeCarrierDensity import getN1
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import DataPlotter as dp

# Datenbasis
Data = ['Gate_minus_1_5V', 'Gate_minus_1V', '1.4K_switched', 'Gate_1V', 'Gate_1_5V']

# Daten extrahieren
nTable, nErrorTable, BTable, rhoXYTable, slopeTable, rhoXXTable = getN1(Data)

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