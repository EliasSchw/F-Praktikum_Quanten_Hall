from Preprocessing import getDatenreihe
import matplotlib as plt
import numpy as np
from macroswriter import writeLatexMacro


def average(data_set, AnfangEnde):
    BanfangStufe, BendeStufe = AnfangEnde
    indices = [i for i, t in enumerate(data_set["B"]) if BanfangStufe < t < BendeStufe]
    chopped_rho_xy = [data_set['rho_xy'][i] for i in indices]    
    return np.average(chopped_rho_xy) 
    

HallPlateaus = {'4.2K':[[8,10],[4.1,5.1],[2.8,3.1],[2.2,2.35],[1.77,1.86]]}


def writePlateauMacros(HallPlateaus, data_set):
    for name, plateauList in HallPlateaus.items():
        for i in range(len(plateauList)):
            writeLatexMacro(f'PlateauNr{i+1}{name.replace(' ','').replace('_','')}', average(data_set, HallPlateaus[name][i]),
                            r'$\Omega$')

writePlateauMacros(HallPlateaus, getDatenreihe('4.2K'))

def findAlpha():
    R_k1 = average(getDatenreihe('1.4K'),[8,10])
    R_k2 = average(getDatenreihe('1.4K_switched'),[8,10])
    return(np.sqrt(R_k2/R_k1))
    

print(findAlpha())
    
    



