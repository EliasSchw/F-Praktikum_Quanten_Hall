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
                    
                    
                    
                    
                    


#zur präzisen bestimmung der cutoffs
def plotBNachZeitZurCutoffBestimmung(Messung):
    data=einlesen(Messung['path'])
    plt.plot(data['time'], data['U_B'])
    plt.axvline(Messung['cut_rampup_anfang'], label='up_anfang', color='red')
    plt.axvline(Messung['cut_rampup_ende'], label='up_ende', color='green')    
    plt.axvline(Messung['cut_rampdown_anfang'], label='down_anfang', color='purple')
    plt.axvline(Messung['cut_rampdown_ende'], label='down_ende', color='orange')
    plotter.fancyGraph()
    plt.show()    


def getDatenreihe(nameMessung:str):
    return preprocessing(Messungen_dict[nameMessung])


def cutter(data_sets, t_anfang, t_ende):
    time_indices = [i for i, t in enumerate(data_sets["time"]) if t_anfang < t < t_ende]
    chopped_data = {key: [values[i] for i in time_indices] for key, values in data_sets.items()}
    return chopped_data


def zeitUmstellung(raw_data):
    U_xy_versch = []
    U_xx_versch = []
    U_I_versch = []
    for i, _ in enumerate(raw_data['time']):
        if i >= zeitoffset*10:                   #*10 wegen o.1s zeitschritten
            U_xy_versch.append(raw_data['U_xy'][int(i)])
            U_xx_versch.append(raw_data['U_xx'][int(i)])
            U_I_versch.append(raw_data['U_I'][int(i)])
        
    raw_data['U_xy'] = U_xy_versch
    raw_data['U_xx'] = U_xx_versch
    raw_data['U_I'] = U_I_versch
    return raw_data
    

def preprocessing(Messung):
    raw_data = zeitUmstellung(einlesen(Messung['path']))
    if Messung['switched']:
        raw_data['U_xy'], raw_data['U_I'] =  raw_data['U_I'], raw_data['U_xy'] 
        

    data_up = cutter(raw_data, Messung['cut_rampup_anfang'], Messung['cut_rampup_ende'])
    data_down = cutter(raw_data, Messung['cut_rampdown_anfang'], Messung['cut_rampdown_ende'])
    
    I_up = [U_I/R_für_Strom for U_I in data_up['U_I']]
    I_down = [U_I/R_für_Strom for U_I in data_down['U_I']]

    B_up = [U_B*FactorFürsMagnetfel for U_B in data_up['U_B']]
    B_down = [U_B*FactorFürsMagnetfel for U_B in data_down['U_B']]

    rho_xy_up = [U_xy/I for U_xy, I in zip(data_up['U_xy'], I_up)]
    rho_xy_down = [U_xy/I for U_xy, I in zip(data_down['U_xy'], I_down)]

    rho_xx_up = [U_xx/formfaktor for U_xx in data_up['U_xx']]
    rho_xx_down = [U_xx/formfaktor for U_xx in data_down['U_xx']]
    '''
    plt.plot(B_up, rho_xy_up, 'o', markersize=0.1, color='red', label='up')
    plt.plot(B_down, rho_xy_down, 'o', markersize=0.1, color='blue', label='down')
    plt.legend()
    plotter.fancyGraph()
    plotter.save_and_open(open=True)    
    ''' 
    processedData = {}
    processedData['I'] = I_up + I_down
    processedData['B'] = B_up + B_down
    processedData['rho_xy'] = rho_xy_up + rho_xy_down
    processedData['rho_xx'] = rho_xx_up + rho_xx_down
    return processedData







#preprocessing(Messungen_dict['4.2K'])
#plotBNachZeitZurCutoffBestimmung(Messungen_dict['3K'])


