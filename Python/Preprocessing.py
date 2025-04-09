from Leseratte import einlesen
import DataPlotter as plotter
import matplotlib.pyplot as plt
from macroswriter import writeLatexMacro

'''
Tasks:

switched korrigieren
Strom ausrechnen
Magnetfeld ausrechnen
zerschneiden $ Drift korrigieren
'''

R_für_Strom = 4.982*10**3
FactorFürsMagnetfeldWsl1 = 0.9
formfaktor = 6

filepath_erste_Messung = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\1 0.dat'
filepath_switched = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\LI_swiched_153_3V1_470K_end_135_1V1_520K 5.dat'


# im Array: filepath, cut_rampup_anfang (Zeit), cut_rampup_ende, cut_rampdown_anfang, cut_rampdown_ende, temp, temp_fehler, U_gate
Raw_Data_direc = {'erste Messung': {'path': filepath_erste_Messung},
                       'switched' : {'path': filepath_switched}}


def getDatenreihe(name:str):
    return preprocessing(einlesen(Raw_Data_direc[name]['path']))


def cutter(data:list, t_anfang, t_ende):
    return [data for data in data if t_anfang < data["time"]<t_ende]
    


def preprocessing(raw_data):
    I_up = [U_I/R_für_Strom for U_I in raw_data['U_I']]
    B_up = [raw_data['U_B']*FactorFürsMagnetfeldWsl1]
    U_xy = raw_data['U_Hall']
    U_xx = raw_data['U_xx']/6 
    
    
    
    return








