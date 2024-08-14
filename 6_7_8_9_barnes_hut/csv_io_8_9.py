import numpy as np
# To save and load from csv
import pandas as pd
#Used for progress bar
from tqdm import tqdm

#!!-------------------------------------------!!-------------------------------------------------!!
##############################This file is very similar to csv_io.py##############################
#!!-------------------------------------------!!-------------------------------------------------!!

def receive_csv_input(input_file, body_count):
    print("Importing solutions from .csv...")
    df = pd.read_csv(input_file)
    t = np.array(df['t'])
    historic_energy = df["e"]
    historic_positions = np.zeros((len(t), body_count, 3))

    #Starts a progress bar to show importing progress
    with tqdm(total=100, unit="‰") as pbar:
        state=[0, body_count/100]
        #Get all column headers and eliminate used ones
        column_list = df.columns.values.tolist()
        column_list.pop(column_list.index("t"))
        column_list.pop(column_list.index("e"))
        for i in range(body_count):
            if len(column_list)==0: #When no data left to extract
                break
            historic_positions[:,i,0] = df[f"x{i}"]
            historic_positions[:,i,1] = df[f"y{i}"]
            historic_positions[:,i,2] = df[f"z{i}"]

            #Eliminate from available columns. 
            #This is needed because bodies may escape
            column_list.pop(column_list.index(f"x{i}"))
            column_list.pop(column_list.index(f"y{i}"))
            column_list.pop(column_list.index(f"z{i}"))

            #Updates progress bar
            [last_i, di_pbar] = state
            n = int((i - last_i)/di_pbar)
            pbar.update(n)
            state[0] = last_i + di_pbar * n
    pbar.update(100)
    return t, historic_energy, historic_positions
    

def save_output_csv(plot_t, historic_positions, historic_energy, body_count, output_file):
    print("Preparing results to save in .csv...")
    df = pd.DataFrame()
    df['t']=plot_t
    df["e"] = historic_energy
    
    for i in range(body_count):
        df[f"x{i}"] = historic_positions[:,i,0]
        df[f"y{i}"] = historic_positions[:,i,1]
        df[f"z{i}"] = historic_positions[:,i,2]

    print("Creating and filling the .csv file...")
    df.to_csv(output_file, index=False)