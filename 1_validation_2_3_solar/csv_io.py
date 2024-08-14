import numpy as np
#Used to save and load .csv
import pandas as pd
#Used for progress bar
from tqdm import tqdm

#!!--------------------###--------------------!!--------------------###--------------------------!!
##########THIS FILE IS THE EXACT SAME AS THE OTHERS WITH THE SAME NAME IN OTHER FOLDERS##########
#!!--------------------###--------------------!!--------------------###--------------------------!!

#This function allows the use of previously created csv files with ODE results.
def receive_csv_input(input_file, body_count): 
    print("Importing solutions from .csv...")
    df = pd.read_csv(input_file)
    t = np.array(df['t'])
    
    x = np.array(np.zeros((body_count, len(t))))
    vx = np.array(np.zeros((body_count, len(t))))
    y = np.array(np.zeros((body_count, len(t))))
    vy = np.array(np.zeros((body_count, len(t))))
    z = np.array(np.zeros((body_count, len(t))))
    vz = np.array(np.zeros((body_count, len(t))))
    #Starts a progress bar to show importing progress
    with tqdm(total=100, unit="‰") as pbar:
        state=[0, (len(x))/100]
        for i in range(len(x)):
            x[i] = df[f"x{i}"]
            y[i] = df[f"y{i}"]
            z[i] = df[f"z{i}"]

            vx[i] = df[f"vx{i}"]
            vy[i] = df[f"vy{i}"]
            vz[i] = df[f"vz{i}"]
            #Updates progress bar
            [last_i, di_pbar] = state
            n = int((i - last_i)/di_pbar)
            pbar.update(n)
            state[0] = last_i + di_pbar * n
    pbar.update(100)
    return t, x, vx, y, vy, z, vz

#Saves obtained data to output file csv.
def save_output_csv(t, x, vx, y, vy, z, vz, output_file):
    print("Preparing results to save in .csv...")
    df = pd.DataFrame()
    df['t']=t
    
    for i in range(len(x)):
        df[f"x{i}"] = x[i]
        df[f"y{i}"] = y[i]
        df[f"z{i}"] = z[i]

        df[f"vx{i}"] = vx[i]
        df[f"vy{i}"] = vy[i]
        df[f"vz{i}"] = vz[i]
    print("Creating and filling the .csv file...")
    df.to_csv(output_file, index=False)