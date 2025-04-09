from Leseratte import einlesen
import DataPlotter as plotter
import matplotlib.pyplot as plt
from macroswriter import writeLatexMacro

R_für_Strom = 4.982*10**3


filepath = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\1 0.dat'
filepath = r'C:\Users\schwa\OneDrive\EliasOneDrive\Uni\7. Semester\F-Praktikum\F-Praktikum\Quanten-Hall\F-Praktikum_Quanten_Hall\RawData\ersteTestDaten\LI_swiched_153_3V1_470K_end_135_1V1_520K 5.dat'

def U_Hall_plotten(U_I, U_Hall, U_B):
    
    plt.plot(U_B, [U_Hall*R_für_Strom/U_I for U_Hall, U_I in zip(U_Hall,U_I)], '.', linewidth=0.9)
    
    plt.xlabel(r'$U_B$')
    plt.ylabel(r'$U_{Hall}/I= \rho _{xy}$')
    
    #plotter.fancyGraph()
    plotter.save(open=True)


def U_xx_plotten(U_I, U_xx, U_B):
    
    plt.plot(U_B, [U_Hall/U_I for U_Hall, U_I in zip(U_xx,U_I)], '.', linewidth=0.9)
    
    plotter.fancyGraph()
    plotter.save(open=True)



data = einlesen(file_path=filepath)
#print(data['U_I'])
U_Hall_plotten(data['U_Hall'], data['U_I'], data['U_B'])


#writeLatexMacro('test', 17,'Hz')