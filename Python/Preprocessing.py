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


filepath_erste_Messung = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\1 0.dat'
filepath_switched = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\LI_swiched_153_3V1_470K_end_135_1V1_520K 5.dat'


# im Array: filepath, cut_rampup_anfang (Zeit), cut_rampup_ende, cut_rampdown_anfang, cut_rampdown_ende, temp, temp_fehler, U_gate, switched:boolean
Messungen_dict = {'erste Messung': {'path': filepath_erste_Messung, 'switched': False,
                            'cut_rampup_anfang': 5.42, 'cut_rampup_ende':441, 'cut_rampdown_anfang':459, 'cut_rampdown_ende':896},
                  
                    'switchedTestMessung' : {'path': filepath_switched}}


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

    '''plt.plot(B_up, rho_xy_up, 'o', markersize=0.1, color='red', label='up')
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







#preprocessing(Messungen_dict['erste Messung'])



