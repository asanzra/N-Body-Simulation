import numpy as np
import matplotlib.pyplot as plt
from universe_variables import AU
#Abstracted functions for clarity and modularisation
from static_plot_tools import ax_plot_step

#!!--------------------###--------------------!!--------------------###--------------------------!!
##########THIS FILE IS THE EXACT SAME AS THE OTHERS WITH THE SAME NAME IN OTHER FOLDERS##########
#!!--------------------###--------------------!!--------------------###--------------------------!!

def live_plots(body_count, plot_step, live_plot_t_step,
               t,x,y,z, bodies_names):
    fig2 = plt.figure()
    ax_update = fig2.add_subplot(111, projection='3d')

    # Plot positions
    if not bodies_names:
        legend=[] #Create a generic legend
    lines=[]
    #Obtained from matplotlib internal default colours: mpl.rcParams['axes.prop_cycle']
    colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    for body in range(body_count):
        print(f"Plotting initial positions for body with index {body}...")
        line = ax_plot_step(ax_update, plot_step, x[body][0]/AU, y[body][0]/AU, z=z[body][0]/AU, colour=colours[body], marker='.')
        lines.append(line[0])
        if not bodies_names:
            legend.append(f"Planet {body}")
    
    print("Doing legend and titles...")
    if bodies_names:
        ax_update.legend(bodies_names)
    else:
        ax_update.legend(legend)
    ax_update.set_xlabel("x (AU)")
    ax_update.set_ylabel("y (AU)")
    ax_update.set_zlabel("z (AU)")
    ax_update.set_xlim([np.min(x)/AU, np.max(x)/AU])
    ax_update.set_ylim([np.min(y)/AU, np.max(y)/AU])
    ax_update.set_zlim([np.min(z)-1e-12, np.max(z)+1e-12])

    plt.show(block=False)

    #Loop to plot each time
    for time_i in range(0, len(t), live_plot_t_step):
        ax_update.cla()
        for body, line in enumerate(lines):
            line = ax_plot_step(ax_update, plot_step, x[body][time_i]/AU, y[body][time_i]/AU, z=z[body][time_i]/AU, colour=colours[body], marker='*')
        if bodies_names:
            ax_update.legend(bodies_names)
        else:
            ax_update.legend(legend)
        ax_update.set_xlabel("x (AU)")
        ax_update.set_ylabel("y (AU)")
        ax_update.set_xlim([np.min(x)/AU, np.max(x)/AU])
        ax_update.set_ylim([np.min(y)/AU, np.max(y)/AU])
        ax_update.set_zlim([np.min(z)-1e-12, np.max(z)+1e-12])
        fig2.canvas.draw()
        fig2.canvas.flush_events()
        plt.draw()
        plt.pause(0.01)
    plt.show(block=False)