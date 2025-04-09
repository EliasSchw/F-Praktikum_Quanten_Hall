from Leseratte import einlesen
import DataPlotter as plotter
import matplotlib.pyplot as plt
from macroswriter import writeLatexMacro
import numpy as np


'''
Tasks:

switched korrigieren
Strom ausrechnen
Magnetfeld ausrechnen
zerschneiden $ Drift korrigieren
'''

R_für_Strom = 4.982*10**3
FactorFürsMagnetfel = 0.9
formfaktor = 6

zeitoffset = 4
switchFaktorAlpha = 1 #noch zu ändern


filepath_4_2K = r'RawData/1 0.dat'
filepath_3K = r'RawData/18_23V2_970K_end_18_30V_2_970K 1.dat'
filepath_2_1K = r'RawData/43_6V2_08K_end_44_8V_2_100K 3.dat'
filepath_1_4K = r'RawData/133V1_520K_end_133_1V1_520K 4.dat'
filepath_1_4K_switched = r'RawData/LI_swiched_153_3V1_470K_end_135_1V1_520K 5.dat'
filepath_Gate_minus_1_5V = r'RawData/Gate_--1_49904V_LI_swiched_151_6V1_470K_end_133_3V1_520K 9.dat'
filepath_Gate_minus_1V = r'RawData/Gate_-0_9992V_LI_swiched_133_9V1_520K_end_133_5V1_520K 8.dat'
filepath_Gate_1V = r'RawData/Gate_1V_LI_swiched_152_3V1_520K_end_134_0V1_520K 7.dat'
filepath_Gate_1_5V = r'RawData/Gate_1_5V_LI_swiched_135_5V1_520K_end_134_7V1_520K 6.dat'
# im Array: filepath, cut_rampup_anfang (Zeit), cut_rampup_ende, cut_rampdown_anfang, cut_rampdown_ende, temp, temp_fehler, U_gate, switched:boolean
Messungen_dict = {'4.2K': {'path': filepath_4_2K, 'switched': False, 'temp': 3.99, 'temp_fehler': 0.031, 'U_gate': -0.25},                 
                    '3K' : {'path': filepath_3K, 'temp': 2.97, 'temp_fehler': 0.0, 'U_gate': -0.25, 'switched': False},
                    '2.1K' : {'path': filepath_2_1K, 'temp': 2.11, 'temp_fehler': 0.01, 'U_gate': -0.25, 'switched': False},
                    '1.4K' : {'path': filepath_1_4K, 'temp': 1.52, 'temp_fehler': 0.0, 'U_gate': -0.25, 'switched': False},
                    '1.4K_switched' : {'path': filepath_1_4K_switched, 'temp': 1.495, 'temp_fehler': 0.025, 'U_gate': -0.25, 'switched': True},
                    'Gate_minus_1_5V' : {'path': filepath_Gate_minus_1_5V, 'temp': 1.495, 'temp_fehler': 0.025, 'U_gate': -1.5, 'switched': True},
                    'Gate_minus_1V' : {'path': filepath_Gate_minus_1V, 'temp': 1.52, 'temp_fehler': 0.0, 'U_gate': -1.0, 'switched': True},
                    'Gate_1V' : {'path': filepath_Gate_1V, 'temp': 1.495, 'temp_fehler': 0.025, 'U_gate': 1.0, 'switched': True},
                    'Gate_1_5V' : {'path': filepath_Gate_1_5V, 'temp': 1.52, 'temp_fehler': 0.0, 'U_gate': 1.5, 'switched': True}
                    }
                    
                    
                    
                  

def getDatenreihe(nameMessung:str):
    return preprocessing(Messungen_dict[nameMessung])


def zeitUmstellung(raw_data):
    U_xy_versch = []
    U_xx_versch = []
    U_I_versch = []
    U_B_versch  = []
    for i, _ in enumerate(raw_data['time']):
        if i >= zeitoffset*10:                   #*10 wegen o.1s zeitschritten
            U_xy_versch.append(raw_data['U_xy'][int(i)])
            U_xx_versch.append(raw_data['U_xx'][int(i)])
            U_I_versch.append(raw_data['U_I'][int(i)])
            U_B_versch.append(raw_data['U_B'][int(i-zeitoffset*10)]) 
        
    raw_data['U_xy'] = U_xy_versch
    raw_data['U_xx'] = U_xx_versch
    raw_data['U_I'] = U_I_versch
    raw_data['U_B'] = U_B_versch
    return raw_data
    

def preprocessing(Messung):
    raw_data = zeitUmstellung(einlesen(Messung['path']))
    if Messung['switched']:
        raw_data['U_xy'], raw_data['U_I'] =  raw_data['U_I'], raw_data['U_xy'] 


    processedData = {}
    processedData['I'] = [U_I/R_für_Strom for U_I in raw_data['U_I']]
    processedData['B'] = [U_B*FactorFürsMagnetfel for U_B in raw_data['U_B']]
    processedData['rho_xy'] = [U_xy/I for U_xy, I in zip(raw_data['U_xy'], processedData['I'])]
    processedData['rho_xx'] = [U_xx/formfaktor for U_xx in raw_data['U_xx']]
    return processedData

def plotHall():
    data = getDatenreihe('4.2K')
    colors = np.linspace(0, 1, len(data['B']))
    scatter = plt.scatter(data['B'], data['rho_xy'], c=colors, cmap='viridis')
    plt.colorbar(scatter, label='Color Gradient')
    plt.show()
    

