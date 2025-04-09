def writeLatexMacro(macro_name:str, value:float, unit:str=None, error:float=None, digitsIfNoError:int = 4, filepath='Paper/Latex/macros.tex'):
    """
    Writes or overrides LaTeX macros in the specified file.
    Rounds the value and error to the same order of magnitude (two digits of the error) and writes them in scientific notation.
    """
    
    if error:
        if error > value:
            raise ValueError("Error cannot be larger than the value.")  
        
        value_order = int(f"{value:.1e}".split('e')[1])
        error_order = int(f"{error:.1e}".split('e')[1])
        error *= 10**-value_order
        value *= 10**-value_order
        valueStr = f"{value:.{value_order - error_order+1}f}"
        errorStr = f"{error:.{value_order - error_order+1}f}"

        macro_content = f"\\newcommand{{\\{macro_name}}}{{\\left({valueStr} \\pm {errorStr}"
    else:
        value_order = int(f"{value:.1e}".split('e')[1])
        value *= 10**-value_order
        valueStr = f"{value:.{digitsIfNoError-1}f}"

        macro_content = f"\\newcommand{{\\{macro_name}}}{{\\left({valueStr}"
    if not value_order == 0:
        macro_content += f"\\right) \\cdot 10^{{{value_order}}}"
    if unit:
        macro_content += f"\\,\\text{{{unit}}}"
    macro_content += '}' + f"\n"
    
    macro_content = macro_content.replace("_","")


    # Read the existing file content
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Remove existing macro with the same name
    lines = [line for line in lines if not line.strip().startswith(f"\\newcommand{{\\{macro_name.replace('_','')}}}")] 

    # Append the new macro
    lines.append(macro_content)

    # Write back to the file
    with open(filepath, 'w') as file:
        file.writelines(lines)





