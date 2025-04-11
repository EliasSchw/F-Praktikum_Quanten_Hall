from Preprocessing import getDatenreihe
import DataPlotter as plotter
import matplotlib.pyplot as plt
from macroswriter import writeLatexMacro, writeLatexCSname
import numpy as np




def plotWithVerticalLines():
    V1 = getDatenreihe('Gate_1_5V')
    V2 = getDatenreihe('Gate_1V')
    V3 = getDatenreihe('1.4K')
    
    plt.plot(V1['B'], V1['rho_xy'], label=r'$\rho_\text{xy,1.5V}$')
    
    plt.plot(V2['B'], V2['rho_xy'], label=r'$\rho_\text{xy,1V}$')
    
    plt.plot(V3['B'], V3['rho_xy'], label=r'$\rho_\text{xy,-0.25V}$')
    
    plt.axvline()
        
    plotter.fancyGraph()
    plotter.save_and_open(filename='differentGateVoltagesQHE')
    