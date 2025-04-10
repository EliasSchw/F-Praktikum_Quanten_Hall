from Preprocessing import getDatenreihe
import matplotlib.pyplot as plt
import numpy as np
import macroswriter as marco


def average(data_set, AnfangEnde):
    BanfangStufe, BendeStufe = AnfangEnde
    indices = [i for i, t in enumerate(data_set["B"]) if BanfangStufe < t < BendeStufe]
    chopped_rho_xy = [data_set['rho_xy'][i] for i in indices]    
    return np.average(chopped_rho_xy) 
    

HallPlateaus = [[8,10],[4.1,4.75],[2.9,3.1],[2.2,2.3],[1.77,1.86]]


def writePlateauMacros(HallPlateaus, data_sets):
    for name in ('4.2K', '3K', '2.1K', '1.4K'):
        for i in range(len(HallPlateaus)):
            marco.writeLatexCSname(f'PlateauNr{i+1}{name.replace(' ','').replace('_','')}', 10**-4*average(data_sets[name], HallPlateaus[i]),
                            r'', noBrackets=True)
            marco.writeLatexCSname(f'PlateauMalNuNr{i+1}{name.replace(' ','').replace('_','')}', 10**-4*(i+1)*average(data_sets[name], HallPlateaus[i]),
                            r'', noBrackets=True)


def findAlpha():
    R_k1 = average(getDatenreihe('1.4K'),[8,10])
    R_k2 = average(getDatenreihe('1.4K_switched'),[8,10])
    return(np.sqrt(R_k2/R_k1))
    

writePlateauMacros(HallPlateaus, {'4.2K':getDatenreihe('4.2K'),'3K': getDatenreihe('3K'),'2.1K': getDatenreihe('2.1K'), '1.4K':getDatenreihe('1.4K')})
#print(findAlpha())
    
    



