import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from universe_variables import G

#!!-------------------------------------------!!-------------------------------------------------!!
###########THIS FILE ONLY CHANGES UNITS AND LINEWIDTHS COMPARED TO STATIC_PLOT_TOOLS.PY###########
#!!-------------------------------------------!!-------------------------------------------------!!

#Plots the variables given, but only every "plot_step" points.
def ax_plot_step(axis, plot_step, x, y, z = None, colour = None, marker=None, linewidth=1.5):
    if not isinstance(x, np.ndarray):
        x = np.array([x])
    if not isinstance(y, np.ndarray):
        y = np.array([y])
    x = x[0::plot_step]
    y = y[0::plot_step]
    if z is not None:
        if not isinstance(z, np.ndarray):
            z = np.array([z])
        z = z[0::plot_step]
        if colour is not None and marker is not None:
            return axis.plot(x, y, z, color=colour, marker=marker, linestyle='', linewidth=linewidth)
        return axis.plot(x, y, z)
    if colour is not None and marker is not None:
            return axis.plot(x, y, color=colour, marker=marker, linewidth=linewidth)
    return axis.plot(x, y)

# Calculate and plot energies. Read print statements.
def Energies(t, x, vx, y, vy, z, vz, masses, ax_energy, body_count):
    print("Calculating kinetic energies")
    k = np.zeros(len(t))
    for time_i in range (len(t)):
        for body in range(body_count):
            v_sqr=vx[body][time_i]**2+vy[body][time_i]**2+vz[body][time_i]**2
            k[time_i]+=0.5*v_sqr*masses[body]
    
    print("Calculating potential energy")
    u = np.ones(len(t))
    for time_i in range (len(t)):
        sum_i = 0
        for body_i in range(1,body_count):
            sum_j = 0
            for body_j in range(body_i):
                r=np.sqrt(
                    (x[body_i][time_i]-x[body_j][time_i])**2+
                    (y[body_i][time_i]-y[body_j][time_i])**2+
                    (z[body_i][time_i]-z[body_j][time_i])**2
                    )
                if abs(r) <= 1e-6 :
                    raise Exception(f"Overlapping position for body {body_i} and body {body_j} at time {t[time_i]/(3872.)} time units. Distance: {str(abs(r)/1e-2)} length units.")
                sum_j += masses[body_j] / r
            sum_i += sum_j * masses[body_i]
        ui = -G * sum_i

        u[time_i]=ui

    print("Calculating total energies")
    e = np.zeros(len(t))
    for i in range (len(t)):
        e[i] = u[i] + k[i]

    # Plot energies
    print("Plotting e to t...")
    ax_plot_step(ax_energy, 1, t, (e-e[0])/e[0])
    
    print("Doing legend and titles...")
    ax_energy.set_xlabel("t")
    ax_energy.set_ylabel("Energy difference")

#Can print 3 plots in same figure, depending on first 3 variables (bools):
    #1. regPlot_3Dplot: A 3D plot of all positions along all time
    #2. regPlot_coordToTime: A 2D plot of one coordinate against all time
    #3. regPlot_energyToTime: A 2D plot of energy against all time
def static_plots(regPlot_3Dplot, regPlot_coordToTime, regPlot_energyToTime,
                 initial_positions_in_legend, top_view, output_graph,
                 body_count, bodies_names, plot_step,
                 t, x, vx, y, vy, z, vz, masses):
    # Create a figure and a 1x1 - 3x1 grid specification, depending on what is asked by user.
    fig = plt.figure(figsize=(8, 6),constrained_layout=True)
    axis_count = 0
    if regPlot_3Dplot:
        axis_count+=1
    if regPlot_coordToTime:
        axis_count += 1
    if regPlot_energyToTime:
        axis_count += 1
    # Create a grid of n axis where the biggest one's size is n times bigger than the others
    height_ratios=[1 for _ in range(axis_count)]
    height_ratios[0]=axis_count
    gs = gridspec.GridSpec(axis_count, 1, height_ratios=height_ratios, width_ratios=[1])

    #Create subplot for each asked for plot item.
    plot_index = 0
    if regPlot_3Dplot:
        ax_pos = fig.add_subplot(gs[plot_index], projection='3d')
        plot_index+=1
    if regPlot_coordToTime:
        ax_coord_to_t = plt.subplot(gs[plot_index])
        plot_index+=1
    if regPlot_energyToTime:
        ax_energy = plt.subplot(gs[plot_index])

    plt.show(block=False)

    #Plots 3D positions across all time
    if regPlot_3Dplot:
        #A set of names and colours is set, one for each planet.
        legend_ax_pos=[]
        colours=[]
        for body in range(body_count):
            if bodies_names:
                body_name = bodies_names[body]
            else:
                body_name = f"body {body}"
            print(f"Plotting positions for {body_name}...")
            colours.append(ax_plot_step(ax_pos, plot_step, x[body], y[body], z[body])[0]._color)
            legend_ax_pos.append(body_name.capitalize())

        #Plots the actual positions.
        print("Plotting initial positions...")
        for body in range(body_count):
            if bodies_names:
                body_name = bodies_names[body]
            else:
                body_name = f"body {body}"
            ax_pos.scatter(x[body][0], y[body][0], z[body][0], marker='*', color=colours[body])
            if initial_positions_in_legend:
                legend_ax_pos.append(f"Initial position for {body_name}")
        
        print("Doing axis labels...")
        ax_pos.set_xlabel("x")
        ax_pos.set_ylabel("y")
        if not top_view:
            ax_pos.set_zlabel("z")
        # Sets the needed "camera" position for a top view and removes the visuals of z-axis.
        if top_view:
            ax_pos.view_init(elev=90, azim=-90, roll=0)
            ax_pos.zaxis.line.set_lw(0.)
            ax_pos.set_zticks([])
            ax_pos.spines['left'].set_position(('data', -0.5))

        plt.pause(0.001)

    # Plot a coordinate or velocity to t
    if regPlot_coordToTime:
        if regPlot_coordToTime in ["x","vx","y","vy","z","vz"]:
            #Obtains the variable related to that coordinate. x for "x", vx for "vx", etc.
            coord = locals()[regPlot_coordToTime]
        else:
            raise Exception(f"Trying to plot invalid coordinate: {regPlot_coordToTime}, inputted in main")
        
        #Creates the legend for the plot
        legend_regPlot_coordToTime=[]
        for body in range(body_count):
            print(f"Plotting {regPlot_coordToTime} to time for body with index {body}...")
            ax_plot_step(ax_coord_to_t, plot_step, t, coord[body])
            if bodies_names:
                legend_regPlot_coordToTime.append(bodies_names[body])
            else:
                legend_regPlot_coordToTime.append(f"Planet {body}")

        print("Doing titles...")
        ax_coord_to_t.set_xlabel("t")
        ax_coord_to_t.set_ylabel(f"{regPlot_coordToTime}")

        plt.pause(0.001)

    # Calculate and plot energies
    if regPlot_energyToTime:
        t_e = t[0::plot_step]
        e_size = len(t_e)
        x_e = np.zeros((body_count, e_size))
        vx_e = np.zeros((body_count, e_size))
        y_e = np.zeros((body_count, e_size))
        vy_e = np.zeros((body_count, e_size))
        z_e = np.zeros((body_count, e_size))
        vz_e = np.zeros((body_count, e_size))

        #Slices variables to only calculate the energies that will be plotted.
        for body in range(body_count):
            x_e[body] = x[body][0::plot_step]
            vx_e[body] = vx[body][0::plot_step]
            y_e[body] = y[body][0::plot_step]
            vy_e[body] = vy[body][0::plot_step]
            z_e[body] = z[body][0::plot_step]
            vz_e[body] = vz[body][0::plot_step]
        Energies(t_e, x_e, vx_e, y_e, vy_e, z_e, vz_e, masses, ax_energy, body_count)
        
        plt.pause(0.001)

    # Adjust layout for better spacing
    plt.tight_layout()

    # The legends must be set after tight_layout to not break it with large legends.
    print("Doing legends")
    if regPlot_3Dplot:
        ax_pos.legend(legend_ax_pos)
    if regPlot_coordToTime:
        ax_coord_to_t.legend(legend_regPlot_coordToTime)

    if output_graph:
        print("Saving file to png...")
        plt.savefig(output_graph)

    print("Showing regular plot...")
    plt.show(block=False)