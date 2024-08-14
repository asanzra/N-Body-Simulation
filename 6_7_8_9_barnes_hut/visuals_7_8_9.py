import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#To draw octrees
from wireframeHolder import WireframeHolder

#Abstracted functions for clarity and modularisation
from universals_8_9 import UNIVERSE_SIZE, YEAR, AU

def plot_init_r__set_wireframes(bodies_nodes, draw_tree_fill, draw_real_time_plot):
    fig3 = plt.figure(figsize=(8, 6),constrained_layout=True)
    ax3 = fig3.add_subplot(projection='3d')
    for body in bodies_nodes:
        point, =ax3.plot(body.r[0], body.r[1], body.r[2], 'k.', markersize='2')
        body.plot_point = point
    if draw_tree_fill:
        wireframeHolder = WireframeHolder(ax3, UNIVERSE_SIZE)
    else: 
        wireframeHolder = None
    ax3.set_xlim([0, UNIVERSE_SIZE])
    ax3.set_ylim([0, UNIVERSE_SIZE])
    ax3.set_zlim([0, UNIVERSE_SIZE])
    print("Showing initial points...")
    plt.show(block=(not draw_real_time_plot))
    if draw_real_time_plot:
        plt.pause(1)

    return wireframeHolder

def plot_final_visuals(plot_t, historic_energy, historic_positions, body_count, legend=None):
    #Plot energies
    print("Plotting energies...")
    fig = plt.figure(figsize=(8, 6),constrained_layout=True)
    gs = gridspec.GridSpec(2, 1, height_ratios=[2,1], width_ratios=[1])
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(plot_t/YEAR, historic_energy/historic_energy[0]-1.)
    ax2.set_xlabel("t (years)")
    ax2.set_ylabel("Energy difference")
    plt.show(block=False)

    #Plot of X against time
    print("Plotting X against time...")
    ax = fig.add_subplot(gs[0])
    for body in range(body_count):
        ax.plot(plot_t/YEAR, historic_positions[:,body,0]/AU)
    ax.set_xlabel("t (years)")
    ax.set_ylabel("x (AU)")
    if legend:
        ax.legend(legend)
    fig.set_tight_layout(True)
    plt.show(block=True)