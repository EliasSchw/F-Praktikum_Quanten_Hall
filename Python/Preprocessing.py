from Leseratte import einlesen
import DataPlotter as plotter
import matplotlib.pyplot as plt
from macroswriter import writeLatexMacro, writeLatexCSname
import numpy as np
from scipy.interpolate import interp1d
from numpy import array



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

zeitoffset = 3.8
alpha = 1.0103310857773136 #switchkorrektur

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
                    
                    
def writeTempMacros():
    for name in ['4.2K', '3K', '2.1K', '1.4K']:
        writeLatexCSname(f'tempFor{name}', Messungen_dict[name]['temp'], 'K', np.max([Messungen_dict[name]['temp_fehler'], 0.01 * Messungen_dict[name]['temp']]))
                  

def getDatenreihe(nameMessung:str):
    '''
    returns a dic with 'B', 'I', 'rho_xx', 'rho_xy' 
    '''
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
    processedData['rho_xx'] = [U_xx/(I*formfaktor) for U_xx, I in zip(raw_data['U_xx'],processedData['I'])]
    #alpha Korrektur
    if Messung['switched']:
        processedData['rho_xy'] = [rho_xy / alpha for rho_xy in processedData['rho_xy']]
    else:
        processedData['rho_xy'] = [rho_xy * alpha for rho_xy in processedData['rho_xy']]
    
    processedData = interpoliereFürLukas(processedData)
    processedData['U_gate'] = Messung['U_gate']
    return processedData

def plotHall():
    data = getDatenreihe('Gate_minus_1_5V')
    colors = np.linspace(0, 1, len(data['B']))
    plt.scatter(data['B'], data['rho_xy'], label=r'$\rho_\text{xy}$')
    plt.scatter(data['B'], data['rho_xx'], label=r'$\rho_\text{xx}$')
    
    plt.xlabel('B/T')
    plt.ylabel(r'$\rho$')
    plotter.fancyGraph()
    plotter.save_and_open()
    
def plotrhoFürKaputteKurve():
    data1 = getDatenreihe('Gate_minus_1V')
    data2 = getDatenreihe('Gate_minus_1_5V')

    plt.plot(data1['B'], np.array(data1['rho_xy'])/1000, label=r'$\rho_\text{xy, 1V}$', color='red')
    plt.plot(data1['B'], np.array(data1['rho_xx'])/1000, label=r'$\rho_\text{xx, 1V}$', color ='red', linestyle='--')
    
    plt.plot(data2['B'], np.array(data2['rho_xy'])/1000, label=r'$\rho_\text{xy, 1.5V}$', color='blue')
    plt.plot(data2['B'], np.array(data2['rho_xx'])/1000, label=r'$\rho_\text{xx, 1.5V}$', color ='blue', linestyle='--')
    
    
    
    plt.xlabel(r'$B\,/\,T$')
    plt.ylabel(r'$\rho\,/\,k\Omega$')
    plotter.fancyGraph()
    plotter.save_and_open(filename='kaputteKurvenGateV')
    
def plotBeispielBildVomAnfang():
    data1 = getDatenreihe('1.4K')
    B = np.array(data1['B'])
    rho_xx = np.array(data1['rho_xx'])
    rho_xy =np.array(data1['rho_xy'])

    plt.plot(B, 5*rho_xx/1000, label=r'$5 \cdot \rho_\text{xx}$')
    plt.plot(B, rho_xy/1000, label=r'$\rho_\text{xy}$')
        
    plt.xlabel(r'$B\,/\,T$')
    plt.ylabel(r'$\rho\,/\,k\Omega$')
    plotter.fancyGraph()
    plotter.save_and_open(filename='BeispielBildVomAnfang')
    
def plotBeatingPattern():
    data1 = getDatenreihe('Gate_1_5V')
    B = np.array(data1['B'])
    rho_xx = np.array(data1['rho_xx'])

    plt.plot(B, rho_xx)
    plt.xlim(1,4)
    plt.ylim(0,100)
        
    plt.xlabel(r'$B\,/\,T$')
    plt.ylabel(r'$\rho\,/\,k\Omega$')
    plotter.fancyGraph()
    plotter.save_and_open(filename='beatingPattern')

    
def plotHalls():
    data1 = getDatenreihe('4.2K')    
    data2 = getDatenreihe('3K')
    data3 = getDatenreihe('2.1K')
    data4 = getDatenreihe('1.4K')
    
    # Get the first half of data1 array
    data1_half ={}
    data1_half2 ={}
    half_index = len(data1['B']) // 2
    data1_half['B'] = data1['B'][:half_index]
    data1_half['rho_xy'] = data1['rho_xy'][:half_index]
    # Get the second half of data2 array
    data1_half2['B'] = data1['B'][half_index:]
    data1_half2['rho_xy'] = data1['rho_xy'][half_index:]

    plt.figure()
    plt.plot(data1_half['B'], data1_half['rho_xy'], label='4.2K')
    plt.plot(data1_half2['B'], data1_half2['rho_xy'], label='second half')
    
    #plt.plot(data2['B'], data2['rho_xy'], label='3K')
    #plt.plot(data3['B'], data3['rho_xy'], label='2.1K')
    #plt.plot(data4['B'], data4['rho_xy'], label='1.4K')
    plt.legend()
    plt.xlabel('Magnetic Field B')
    plt.ylabel('Hall Resistivity ρ_xy')
    plt.title('Hall Resistivity vs Magnetic Field')
    #plt.show()

def interpoliereFürLukas(data):
    max_index = np.argmax(data['B'])
    data_first_half = {
        'B': data['B'][:max_index + 1],
        'rho_xy': data['rho_xy'][:max_index + 1],
        'rho_xx': data['rho_xx'][:max_index + 1],
        'I': data['I'][:max_index + 1]
    }
    data_second_half = {
        'B': data['B'][max_index:],
        'rho_xy': data['rho_xy'][max_index:],
        'rho_xx': data['rho_xx'][max_index:],
        'I': data['I'][max_index:]
    }
    
    # Define equally spaced B values for interpolation
    B_interp = np.linspace(min(data['B']), max(data['B']), num=20000)
    # Interpolate rho_xy, rho_xx, and I using np.interp
    data_first_half = {
        'B': B_interp,
        'rho_xy': np.interp(B_interp, data_first_half['B'], data_first_half['rho_xy']),
        'rho_xx': np.interp(B_interp, data_first_half['B'], data_first_half['rho_xx']),
        'I': np.interp(B_interp, data_first_half['B'], data_first_half['I'])
    }
    
    #sortiere für interpolation
    sorted_indices = np.argsort(data_second_half['B'])
    data_second_half = {
        'B': np.array(data_second_half['B'])[sorted_indices],
        'rho_xy': np.array(data_second_half['rho_xy'])[sorted_indices],
        'rho_xx': np.array(data_second_half['rho_xx'])[sorted_indices],
       'I': np.array(data_second_half['I'])[sorted_indices],
    }
    
    data_second_half = {
        'B': B_interp,
        'rho_xy': np.interp(B_interp, data_second_half['B'], data_second_half['rho_xy']),
        'rho_xx': np.interp(B_interp, data_second_half['B'], data_second_half['rho_xx']),
       'I': np.interp(B_interp, data_second_half['B'], data_second_half['I'])
    }
    
    averaged = {
        'B': np.array(B_interp),
        'rho_xy': np.array([(a+b)/2 for a, b in zip(data_first_half['rho_xy'], data_second_half['rho_xy'])]),
        'rho_xx': [(a+b)/2 for a, b in zip(data_first_half['rho_xx'], data_second_half['rho_xx'])],
       'I': [(a+b)/2 for a, b in zip(data_first_half['I'], data_second_half['I'])]
    }
    return averaged


plotBeispielBildVomAnfang()
#plotBeatingPattern()
#plotrhoFürKaputteKurve()
#plotHall()   
#getDatenreihe('3K')
#writeTempMacros()