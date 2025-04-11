from Preprocessing import getDatenreihe
import DataPlotter as plotter
import matplotlib.pyplot as plt
from macroswriter import writeLatexMacro, writeLatexCSname
import numpy as np
from scipy import constants as const
 



def plotWithVerticalLines():
    V1 = getDatenreihe('Gate_1_5V')
    V2 = getDatenreihe('Gate_1V')
    V3 = getDatenreihe('1.4K')
    
    #plt.plot(V1['B'], V1['rho_xy']/1000, label=r'$\rho_\text{xy,1.5V}$')
    
    #plt.plot(V2['B'], V2['rho_xy']/1000, label=r'$\rho_\text{xy,1V}$')
    
    plt.plot(V3['B'], V3['rho_xy']/1000, label=r'$\rho_\text{xy,-0.25V}$')
    
    #plt.legend()
    plt.axhline(const.h/const.e**2/(4/3)/1000, color='black', linestyle='--', label=r'$\nu=4/3$')
    plt.axhline(const.h/const.e**2/(5/3)/1000, color='black', linestyle='--', label=r'$\nu=5/3$')
    
    plt.text(8, (const.h/const.e**2/(4/3)+1000)/1000, r'$\nu=4/3$', color='black', va='center', ha='left')
    plt.text(8, (const.h/const.e**2/(5/3)+1000)/1000, r'$\nu=5/3$', color='black', va='center', ha='left')
    
    plt.ylabel(r'$\rho_\text{xy}\,/\, k\Omega$')
    plt.xlabel('B / T')
    
    plotter.fancyGraph()
    plotter.save_and_open(filename='FQHE')


plotWithVerticalLines()
    