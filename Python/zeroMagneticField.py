from Preprocessing import getDatenreihe
import matplotlib.pyplot as plt
import numpy as np
from macroswriter import writeLatexCSname
import pandas as pd
from scipy.stats import linregress
from scipy import constants as const
from ChargeCarrierDensity import slicingWithPandas

Datenreihen = ['4.2K', '3K', '2.1K', '1.4K']

def calculateSlope(B, rhoXY):
    mask = (B <= 1.2) & (B >= 0) 
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

def calculate_sigmaXX(Datenreihen):
    """
    Berechnet sigmaXX und dessen Fehler bei B=0 für jede Datenreihe.
    """
    sigmaXXatBzero = []
    sigmaXXErrorAtBzero = []

    for datenreihe in Datenreihen:
        I, B, rhoXY, rhoXX = slicingWithPandas(datenreihe)
        indexNearestToZero = np.argmin(np.abs(B))
        rhoXX_near_zero = rhoXX[indexNearestToZero]
        rhoXX_error = (0.01)*np.sqrt(2) * rhoXX_near_zero  # 1% Fehlerannahme
        sigmaXX_near_zero = 1 / rhoXX_near_zero
        sigmaXX_error = sigmaXX_near_zero * (rhoXX_error / rhoXX_near_zero)  # Gaußsche Fehlerfortpflanzung
        sigmaXXatBzero.append(sigmaXX_near_zero)
        sigmaXXErrorAtBzero.append(sigmaXX_error)

    return sigmaXXatBzero, sigmaXXErrorAtBzero


def calculate_RHall(nTable, nErrorTable, Datenreihen):
    """
    Berechnet RHall und dessen Fehler für jede Datenreihe.
    """
    RHallTable = []
    RHallErrorTable = []

    for i in range(len(Datenreihen)):
        RHall = 1 / (nTable[i] * const.e)
        relative_error = nErrorTable[i] / nTable[i]
        RHallError = RHall * relative_error  # Gaußsche Fehlerfortpflanzung
        RHallTable.append(RHall)
        RHallErrorTable.append(RHallError)

   

    return RHallTable, RHallErrorTable


def calculate_my(RHallTable, RHallErrorTable, sigmaXXatBzero, sigmaXXErrorAtBzero, Datenreihen):
    """
    Berechnet my (Mobilität) und dessen Fehler für jede Datenreihe.
    """
    myTable = []
    myErrorTable = []

    for i in range(len(Datenreihen)):
        my = RHallTable[i] * sigmaXXatBzero[i]
        relative_error_RHall = RHallErrorTable[i] / RHallTable[i]
        relative_error_sigmaXX = sigmaXXErrorAtBzero[i] / sigmaXXatBzero[i]
        relative_error_my = np.sqrt(relative_error_RHall**2 + relative_error_sigmaXX**2)
        myError = my * relative_error_my
        myTable.append(my)
        myErrorTable.append(myError)

    

    return myTable, myErrorTable


# Hauptcode
nTable, nErrorTable, BTable, rhoXYTable, slopeTable = getN1(Datenreihen)

# Berechnung von sigmaXX
sigmaXXatBzero, sigmaXXErrorAtBzero = calculate_sigmaXX(Datenreihen)

# Berechnung von RHall
RHallTable, RHallErrorTable = calculate_RHall(nTable, nErrorTable, Datenreihen)

# Berechnung von my
myTable, myErrorTable = calculate_my(RHallTable, RHallErrorTable, sigmaXXatBzero, sigmaXXErrorAtBzero, Datenreihen)

for i in range(len(Datenreihen)):
 
    writeLatexCSname(f"simaXX_{Datenreihen[i]}", value = sigmaXXatBzero[i]*10**3, error= sigmaXXErrorAtBzero[i]*10**3, noBrackets=True)
    writeLatexCSname(f'RHall_{Datenreihen[i]}', value = RHallTable[i]/10**3, error= RHallErrorTable[i]/10**3, noBrackets=True)
    writeLatexCSname(f'my_{Datenreihen[i]}', value = myTable[i] /10, error= myErrorTable[i]/10, noBrackets=True)




