from Preprocessing import getDatenreihe
import DataPlotter as plotter
import matplotlib.pyplot as plt
from macroswriter import writeLatexMacro, writeLatexCSname
import numpy as np




def plot_15_1_025_v_Treppe():
    V1 = getDatenreihe('Gate_1_5V')
    V2 = getDatenreihe('Gate_1V')
    V3 = getDatenreihe('1.4K')
    
    plt.plot(V1['B'], V1['rho_xy'], label=r'$\rho_\text{xy,1.5V}$')
    plt.plot(V1['B'], 5*np.array(V1['rho_xx']), label=r'$5\rho_\text{xx,1.5V}$')
    
    plt.plot(V2['B'], V2['rho_xy'], label=r'$\rho_\text{xy,1V}$')
    plt.plot(V2['B'], 5*np.array(V2['rho_xx']), label=r'$5\rho_\text{xx,1V}$')
    
    plt.plot(V3['B'], V3['rho_xy'], label=r'$\rho_\text{xy,-0.25V}$')
    plt.plot(V3['B'], 5*np.array(V3['rho_xx']), label=r'$5\rho_\text{xx,-0.25V}$')    
    
    plotter.fancyGraph()
    plotter.save_and_open(filename='differentGateVoltagesQHE')
    
    
def testPlot():
    B = np.array(getDatenreihe('1.4K')['B'])
    rho_xx = np.array(getDatenreihe('Gate_1_5V')['rho_xx'])

        #invertiere B
    B_inv = 1/B
        
    #sortiere B für interpolation
    sorted_indices = np.argsort(B_inv)
    B_inv2 = B_inv[sorted_indices]
    rho_xx_inv = rho_xx[sorted_indices]
    
    Binverse = np.linspace(0.05, 50, 3000)
    rho_xx_interpolated = np.interp(Binverse, B_inv, rho_xx_inv)
    
    
    plt.plot(B_inv, rho_xx, label=r'$\rho_\text{xx,1.5V}$')
    plt.xlim(0.14,0.18)
    plt.ylim(0,10)
    plotter.fancyGraph()
    plotter.save_and_open(filename='foo')
    
    
testPlot()



