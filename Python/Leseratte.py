import pandas as pd

def einlesen(file_path:str):
   
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the index of the line ending with 'Uxx(V)'
    start_index = next(i for i, line in enumerate(lines) if line.strip().endswith('Uxx(V)')) + 1

    # Read the data starting from the line after 'Uxx(V)'
    data = pd.read_csv(file_path, delimiter='	', header=None, skiprows=start_index)

    # Convert the DataFrame to a dictionary
    data_dict = data.to_dict(orient='list')
    # Set the names of the elements of the list
    names = ['time', 'U_B', 'U_xy', 'U_I', 'U_xx']
    data_dict = {names[i]: [float(value.replace(',', '.')) for value in values] for i, values in enumerate(data_dict.values())}

    # Print the dictionary to verify the content
    return(data_dict)