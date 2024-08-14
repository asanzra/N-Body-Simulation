import numpy as np
import matplotlib.pyplot as plt

#Abstracted functions for clarity and modularisation
from odes import ode_solve
from universe_variables import SOLVE_IVP
from csv_io import receive_csv_input, save_output_csv
from static_plot_trappist import static_plots
from live_plot_tools import live_plots

#Main function. Must be run from _impl (implementation) scripts.
def main(input_masses, x, vx, y, vy, z, vz, t, method=SOLVE_IVP, plot_step=1, livePlot=False, regPlot=True, regPlot_coordToTime="x", output_file="_output.csv", output_graph="_output.png", bodies_names=None, top_view=True, input_file=None, initial_positions_in_legend=True, regPlot_energyToTime=True, regPlot_3Dplot=True):
    """
    This function calculates and plots the N-body problem for the given initial conditions.

    Parameters
    ----------
    input_masses: N-size array.
        Masses of the N bodies in kg.
    x : N-size array.
        Initial x position of each body in m.
    vx : N-size array.
        Initial x velocity of each body in m/s.
    y : N-size array.
        Initial y position of each body in m.
    vy : N-size array.
        Initial y velocity of each body in m/s.
    z : N-size array.
        Initial z position of each body in m.
    vz : N-size array.
        Initial z velocity of each body in m/s.
    method : string
        Either SOLVE_IVP (import SOLVE_IVP from general) or ODEINT (import ODEINT from general).
    plot_step : int
        How many time steps can be skipped between drawn points.
    livePlot : bool
        Whether to draw an animated plot of the simulation or not.
    regPlot : bool
        Whether to draw a regular plot of the simulation or not.
    regPlot_coordToTime : string (only working for "x"/None.)
        What coordinate to plot separately.
    output_file : string
        Output .csv to save the result data.
    output_graph : string. 
        Output image file to save the result data.
    bodies_names : N-size array of strings
        The name of each body in order.
    top_view : bool
        Whether to make the 3d plot top-down and hide z-axis ticks and label.
    input_file : string
        Path to previously calculated solutions in a .csv. This will not create a solution and instead take that one.
    regPlot_energyToTime : bool
        Whether or not to include energy plot.
    regPlot_3Dplot : bool
        Whether or not to include 3D position plot.
    """
    
    plot_step = int(plot_step) #How often to plot time points, speeds up plots.
    global body_count, masses #Sets this global variables.
    masses = input_masses
    body_count = len(masses)

    if input_file:
        t, x, vx, y, vy, z, vz = receive_csv_input(input_file, body_count)
    else:
        print("Solving ODE...")
        initial_vars = np.array([x,vx,y,vy,z,vz]).flatten()
        # Sets variables used by other functions
        [x,vx,y,vy,z,vz]=ode_solve(method, initial_vars, t, body_count, masses, 
                                   rtol=1e-12, atol=1e-12)

    #Saves obtained data to output file csv.
    if output_file:
        save_output_csv(t, x, vx, y, vy, z, vz, output_file)

    if regPlot:
        static_plots(regPlot_3Dplot, regPlot_coordToTime, regPlot_energyToTime,
                 initial_positions_in_legend, top_view, output_graph,
                 body_count, bodies_names, plot_step,
                 t, x, vx, y, vy, z, vz, masses)
       

    #Shows an animation of the evolution of the system.
    if livePlot:
        live_plots(body_count, plot_step,t,x,y,z)
        
    plt.show()

if __name__ == "__main__":
    raise Exception("This program is meant to be run from an implementation one: 'impl_*.py' ")

