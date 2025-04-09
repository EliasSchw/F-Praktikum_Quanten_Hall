from Preprocessing import getDatenreihe
import matplotlib as plt
import numpy as np
from macroswriter import writeLatexMacro


def average(data, AnfangEnde):
    BanfangStufe, BendeStufe = AnfangEnde
    indices = [i for i, t in enumerate(data["B"]) if BanfangStufe < t < BendeStufe]
    chopped_rho_xy = [data['rho_xy'][i] for i in indices]    
    print(np.average(chopped_rho_xy))
    

HallPlateaus = {'erste Messung':[[8,10],[4.1,5.1],[2.8,3.1],[2.2,2.35],[1.77,1.86]]}


def writePlateauMacros(HallPlateaus, data_sets):
    for name, plateauList in HallPlateaus:
        for i in len(plateauList):
            writeLatexMacro(f'PlateauNr{i}{name.replace(' ','').replace('_','')}', average(data_sets[name]['B'], HallPlateaus[name][i]))

writePlateauMacros(HallPlateaus)