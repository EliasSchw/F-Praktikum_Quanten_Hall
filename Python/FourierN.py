from Preprocessing import getDatenreihe
import matplotlib.pyplot as plt
import numpy as np
from macroswriter import writeLatexMacro, writeLatexCSname
import DataPlotter as plotter
from scipy.optimize import curve_fit
import scipy.constants as const



def interpolate(data_set, plot=False, label='foo'):
    fitmax = 9
    fitmin = 7.6
    if label=='2.1K':
        fitmax=10.5
        fitmin=6.6
    B = np.array(data_set['B'])  # Convert B to a NumPy array
    rho_xx = np.array(data_set['rho_xx'])
    
    #invertiere B
    B_inv = 1/B
    
    
    #plt.plot(B_inv, rho_xx)
    #plt.show()
    #sortiere B für interpolation
    sorted_indices = np.argsort(B_inv)
    B_inv = B_inv[sorted_indices]
    rho_xx = rho_xx[sorted_indices]
    

    
    #eindeutige B
    #unique_B, unique_indices = np.unique(B_inv, return_index=True)
    #B_inv = B_inv[unique_indices]
    #rho_xx = rho_xx[unique_indices]
        
    Binverse = np.linspace(0.05, 50, 3000)
    rho_xx_interpolated = np.interp(Binverse, B_inv, rho_xx)
    
    #plt.scatter(Binverse, rho_xx_interpolated)
    #plt.show()
    
    # Perform Fourier Transform on rho_xx_interpolated
    fft_result = np.fft.fft(rho_xx_interpolated)/600
    frequencies = np.fft.fftfreq(len(Binverse), d=(Binverse[1] - Binverse[0]))

    
    #plt.scatter(frequencies, np.abs(fft_result))
    ##plt.xlim(0,20)
    #plt.ylim(0,10000)
    #plt.show()
    

    # Define a Gaussian function
    def gaussian(x, a, x0, sigma):
        return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

    # Select the range between 7 and 10
    mask = (frequencies >= fitmin) & (frequencies <= fitmax)
    frequencies_fit = frequencies[mask]
    fft_result_fit = np.abs(fft_result)[mask]

    peakAndError, _ = curve_fit(gaussian, frequencies_fit, fft_result_fit, p0=[max(fft_result_fit), 8.5, 0.8])
    # Plot the Gaussian fit
    x_fit = np.linspace(fitmin,fitmax, 1000)
    y_fit = gaussian(x_fit, *peakAndError)
    plt.plot(x_fit, y_fit, label="Gaussian Fit", color="red", linewidth=3)
    
    if plot:    
        plt.scatter(frequencies, np.abs(fft_result), label=r'FFT of $\rho(1/B)$', s=2, color='black')
        #plt.title("Fourier Transform of rho_xx_interpolated")
        plt.xlabel("Frequency of S.d.H oscillations / T")
        plt.ylabel("Amplitude / arbitrary units")
        plotter.fancyGraph()
        plt.legend()
        plt.xlim(0, 20)
        plt.ylim(0,10)
        plotter.save_and_open(filename=label)
    
    
    # Fit the Gaussian

    
    #print(peakAndError[0])
    n = const.e / const.h * peakAndError[1]
    n_fehler = n * peakAndError[2] / peakAndError[1] /2
    
    return (n, n_fehler)
    
    
def writeFourierMacros():
    for name in ('4.2K', '3K', '2.1K', '1.4K'):
        n_mit_fehler = interpolate(getDatenreihe(name), label=name)
        writeLatexCSname(f'FourierN{name}', n_mit_fehler[0]*10**-15, r'', n_mit_fehler[1]*10**-15, noBrackets=True)



    

interpolate(getDatenreihe('1.4K'),plot=True, label='FourierMitGausFür14K')   
writeFourierMacros()