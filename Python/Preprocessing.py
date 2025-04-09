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

#magnetfeldGeschwindigkeitAmpsprosek = 0.213
#FeldkonstangeMagnet = 0.095815 #T/A
#Zeitoffset = 1.5
#MagFeldOffset = Zeitoffset*magnetfeldGeschwindigkeitAmpsprosek*FeldkonstangeMagnet

zeitoffset = 1.5


filepath_erste_Messung = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\1 0.dat'
filepath_switched = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\LI_swiched_153_3V1_470K_end_135_1V1_520K 5.dat'


# im Array: filepath, cut_rampup_anfang (Zeit), cut_rampup_ende, cut_rampdown_anfang, cut_rampdown_ende, temp, temp_fehler, U_gate, switched:boolean
Messungen_dict = {'erste Messung': {'path': filepath_erste_Messung, 
                            'cut_rampup_anfang': 8, 'cut_rampup_ende':350, 'cut_rampdown_anfang':550, 'cut_rampdown_ende':900,
                            'Offset_up':69, 'Offset_down':69},
                  
                    'switched' : {'path': filepath_switched}}


def getDatenreihe(nameMessung:str):
    return preprocessing(Messungen_dict[nameMessung])


def cutter(data, t_anfang, t_ende):
    time_indices = [i for i, t in enumerate(data["time"]) if t_anfang < t < t_ende]
    chopped_data = {key: [values[i] for i in time_indices] for key, values in data.items()}
    return chopped_data

def zeitVerschieben(raw_data):
    
    verschoben_U_B = []
    for i, _ in enumerate(raw_data['time']):
        if i >= zeitoffset*10:                   #*10 wegen o.1s zeitschritten
            verschoben_U_B.append(raw_data['U_B'][int(i-zeitoffset*10)])
        
    
    raw_data['U_B'] = verschoben_U_B
    return raw_data
    


def preprocessing(Messung):
    raw_data = zeitVerschieben(einlesen(Messung['path']))

    data_up = cutter(raw_data, Messung['cut_rampup_anfang'], Messung['cut_rampup_ende'])
    data_down = cutter(raw_data, Messung['cut_rampdown_anfang'], Messung['cut_rampdown_ende'])
    
    
    
    I_up = [U_I/R_für_Strom for U_I in data_up['U_I']]
    I_down = [U_I/R_für_Strom for U_I in data_down['U_I']]

    B_up = [U_B*FactorFürsMagnetfel - Messung['Offset_up'] for U_B in data_up['U_B']]
    B_down = [U_B*FactorFürsMagnetfel + Messung['Offset_down'] for U_B in data_down['U_B']]

    rho_xy_up = [U_Hall/I for U_Hall, I in zip(data_up['U_Hall'], I_up)]
    rho_xy_down = [U_Hall/I for U_Hall, I in zip(data_down['U_Hall'], I_down)]

    rho_xx_up = [U_xx/formfaktor for U_xx in data_up['U_xx']]
    rho_xx_down = [U_xx/formfaktor for U_xx in data_down['U_xx']]


    processedData = {}
    processedData['I'] = I_up + I_down
    processedData['B'] = B_up + B_down
    processedData['rho_xy'] = rho_xy_up + rho_xy_down
    processedData['rho_xx'] = rho_xx_up + rho_xx_down
    
    return processedData


#data = einlesen(Messungen_dict['erste Messung']['path'])
#plt.plot(data['time'], data['U_Hall'])

datenreihe = preprocessing(Messungen_dict['erste Messung'])
plt.plot(datenreihe['B'], datenreihe['rho_xy'])
plt.show()








