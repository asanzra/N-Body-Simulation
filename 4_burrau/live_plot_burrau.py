import numpy as np
import matplotlib.pyplot as plt
#To darken colors in live plot
import matplotlib.colors as mcolors
#Abstracted functions for clarity and modularisation
from static_plot_burrau import ax_plot_step

#!!-------------------------------------------!!-------------------------------------------------!!
########THIS FILE ADDS A BIT OF FUNCTIONALITY TO LIVE_PLOT_TOOLS.PY FOR THIS SPECIAL CASE########
#!!-------------------------------------------!!-------------------------------------------------!!

def live_plots(body_count, plot_step, top_view,
               t,x,y,z):
    fig2 = plt.figure()
    ax_update = fig2.add_subplot(111, projection='3d')

    # Plot positions
    legend=[]
    #Here markers are used for latest position, and line for previous ones.
    markers=[]
    lines=[]
    #Obtained from matplotlib internal default colours: mpl.rcParams['axes.prop_cycle']
    colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    #Function to darken markers for visibility over lines
    def darken_color(hex_color, factor=0.85):
        rgb_color = mcolors.hex2color(hex_color)
        darkened_rgb = [max(0, c * factor) for c in rgb_color]
        darkened_hex = mcolors.rgb2hex(darkened_rgb)
        return darkened_hex
    dark_colours = [darken_color(colour) for colour in colours]
    for body in range(body_count):
        print(f"Plotting initial positions for body with index {body}...")
        marker = ax_plot_step(ax_update, plot_step, x[body][0], y[body][0], z=z[body][0], colour=dark_colours[body], marker='.')
        markers.append(marker[0])

        line = ax_plot_step(ax_update, plot_step, x[body][0], y[body][0], z=z[body][0], colour=colours[body], linewidth=0.5)
        lines.append(line[0])

        legend.append(f"Past body {body}")
        legend.append(f"Current body {body}")
    
    print("Doing legend and titles...")
    ax_update.legend(legend)
    ax_update.set_xlabel("x")
    ax_update.set_ylabel("y")
    if not top_view:
        ax_update.set_zlabel("z")
    ax_update.set_xlim([np.min(x), np.max(x)])
    ax_update.set_ylim([np.min(y), np.max(x)])
    if not top_view:
        ax_update.set_zlim([np.min(z)-1e-12, np.maz(z)+1e-12])
    if top_view:
        ax_update.view_init(elev=90, azim=-90, roll=0)
        ax_update.zaxis.line.set_lw(0.)
        ax_update.set_zticks([])
        ax_update.spines['left'].set_position(('data', -0.5))

    plt.show(block=False)
    plt.pause(1)

    #Loop to plot each time
    for time_i in range(0, len(t), int(len(t)/1000)):
        ax_update.cla()
        for body, marker in enumerate(markers):
            start_line_time = time_i - plot_step*2000
            if start_line_time < 0: #This variable sets time window for trailing line.
                start_line_time = 0
            lines[body] = ax_plot_step(ax_update, plot_step, x[body][start_line_time:time_i], y[body][start_line_time:time_i], z=z[body][start_line_time:time_i], colour=colours[body], linewidth=0.5)
            marker = ax_plot_step(ax_update, plot_step, x[body][time_i], y[body][time_i], z=z[body][time_i], colour=dark_colours[body], marker='*')
        ax_update.legend(legend)
        ax_update.set_xlabel("x")
        ax_update.set_ylabel("y")
        ax_update.set_title(f"Time : {round(t[time_i],2)}")
        fig2.canvas.draw()
        fig2.canvas.flush_events()
        plt.draw()
        plt.pause(0.001)
    plt.show(block=False)