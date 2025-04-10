import matplotlib.pyplot as plt


def save_and_open(open = True, filename='foo'):
    plt.savefig('.\\Paper\\Images\\'+filename + '.png', dpi=600)
    from PIL import Image
    if open:
        Image.open(".\\Paper\\Images\\"+filename + ".png").show()
    plt.clf()

def fancyGraph():
    plt.grid(True)
    plt.gca().set_axisbelow(True)
    plt.xlabel(plt.gca().get_xlabel(), fontsize=15)
    plt.ylabel(plt.gca().get_ylabel(), fontsize=15)
    plt.tick_params(axis='both', labelsize=14)
    plt.tick_params(axis='both', direction='in', which='both', top=True, right=True)
    plt.tick_params(axis='both', length=6, width=1.2)
    plt.legend(fontsize=16)


def plot_data(data, label=''):
    """
    Plots the data using matplotlib.

    Parameters:
        data (list): The data to plot, assumed to be a list of tuples or a 2D array.
    """
    
    plt.figure(figsize=(10, 6))
    # Extract x and y values from the data
    x_values = [point[0] for point in data]
    y_values = [point[1] for point in data]
    plt.plot(x_values, y_values, '-', linewidth=0.9, label=label)  # Plot as single points
    plt.xlim(left=min(x_values), right=max(x_values))