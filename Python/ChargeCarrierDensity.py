from Preprocessing import getDatenreihe
import matplotlib.pyplot as plt
import numpy as np
from macroswriter import writeLatexMacro
import pandas as pd
from scipy.stats import linregress
from scipy import constants as const

df = pd.DataFrame.from_dict(getDatenreihe('4.2K'))
I = df.iloc[:,0]
B = df.iloc[:,1]
rhoXY = df.iloc[:,2]
rhoXX = df.iloc[:,3]
mask = B <= 1.5
mask = mask >= 0
B_cuttet = B[mask]
rhoXY_cuttet = rhoXY[mask]
linReg = linregress(B_cuttet, rhoXY_cuttet)
slope = linReg[0]
n = 1/ (slope * const.e)
print(n)


