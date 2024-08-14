import matplotlib.pyplot as plt
#Progress bar
from tqdm import tqdm

#Abstracted functions for clarity and modularisation
from universals_8_9 import UNIVERSE_SIZE, G
from node_8_9 import place_node_inside_node

#Multiprocessing
from multiprocessing import Process
#Number of subprocesses for multiprocessing
#NOT FASTER THAN SINGLE CORE. Recommendation:1
process_size = 1

#Calculate the potential energy of the system
def potential_energy(bodies_nodes, G):
    sum_i = 0
    for i, body_i in enumerate(bodies_nodes[1:]):
        sum_j = 0
        for body_j in bodies_nodes[i+2:]:
            r=body_i.rij(body_j)
            if abs(r) <= 1e-16 :
                raise Exception(f"Overlapping position for bodies. i={i}")
            sum_j += body_j.mass / r
        sum_i += sum_j * body_i.mass
    return -G * sum_i

# Calculates the total acceleration generated on the body by the node contents.
def calculate_total_grav_acc(body, node, theta):
    if node.children is None: #If node is a leaf of the tree.
        return body.grav_acc(node)
    
    elif node.size < node.rij(body)/UNIVERSE_SIZE * theta: #If the distance is far enough, center of mass approximation.
        return body.grav_acc(node)
    else: #If body and node are too near, the acceleration provided by each child is summed up.
        acceleration = 0
        for child in node.children:
            if child is None:
                continue
            acceleration += calculate_total_grav_acc(body, child, theta)
    return acceleration

def work_on_ode_steps(bodies_nodes_left, root_node, G, theta, dt, bodies_nodes, draw_real_time_plot):
    while len(bodies_nodes_left) > 0:
        len(bodies_nodes_left)
        body = bodies_nodes_left.pop(0)

        acceleration = G * calculate_total_grav_acc(body, root_node, theta)
            
        v = body.v
        r = body.r

        #2nd order Runge-Kutta
        vh = v+ dt/2*acceleration
        r += dt*vh
        v += dt*acceleration

        for coord in r:
            if coord >= 0.9 * UNIVERSE_SIZE or coord < 0.1 * UNIVERSE_SIZE:
                print(f"Body exited universe, at position: {body.r[0], body.r[1], body.r[2]}")
                if body in bodies_nodes:
                    bodies_nodes.pop(bodies_nodes.index(body))
                    if draw_real_time_plot:
                        body.plot_point.set(color='r', marker='*', markersize=20.)
                        plt.pause(0.1)
                print(f"{len(bodies_nodes)} bodies left")
                if len(bodies_nodes) == 0:
                    print("EMPTY UNIVERSE")
                    exit()

def ode_step(bodies_nodes, root_node, theta, G, dt, draw_real_time_plot):
    bodies_nodes_left = bodies_nodes.copy()
    if process_size > 1:
        processes = []
        for i in range(process_size):
            p = Process(target=work_on_ode_steps, args=(bodies_nodes_left, root_node, G, theta,
                                                         dt, bodies_nodes, draw_real_time_plot))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
    else:
        work_on_ode_steps(bodies_nodes_left, root_node, G, theta, dt, bodies_nodes, draw_real_time_plot)

#Calculate and save the result for all time
def perform_time_steps(t, draw_tree_fill, draw_real_time_plot, wireframeHolder, 
                       bodies_nodes, historic_positions, historic_energy, theta, plot_t_step):
    print("Calculating time steps...")
    with tqdm(total=100, unit="‰") as pbar:
        state=[t[0], (t[-1]-t[0])/100]
               
        for i, ti in enumerate(t):
            #print(f"Time index: {i}/{len}")
            if draw_tree_fill:
                wireframeHolder.reset_list()
            #Progress bar
            [last_t, dt_pbar] = state
            n = int((ti - last_t)/dt_pbar)
            pbar.update(n)
            # this we need to take into account that n is a rounded number.
            state[0] = last_t + dt_pbar * n

            if i == 0:
                #In the first iteration we just stablish the initial variables, no dt available to change r or v.
                #Save energies and positions
                for j, body_node in enumerate(bodies_nodes):
                    historic_energy[i]+=1/2*body_node.mass*(body_node.v[0]**2+body_node.v[1]**2+body_node.v[2]**2)
                    historic_positions[i][j]=body_node.r
                historic_energy[i]+=potential_energy(bodies_nodes, G)
                continue

            dt = ti - t[i-1]
            #Rebuild oct tree
            root_node = None
            for body_node in bodies_nodes:
                body_node.restore()
                root_node = place_node_inside_node(body_node, root_node, bodies_nodes, historic_positions, wireframeHolder, draw_tree_fill)
            #Calculate forces
            ode_step(bodies_nodes, root_node, theta, G, dt, draw_real_time_plot)

            if draw_real_time_plot and i % plot_t_step == 0:
                #print(f"Step {i} out of {len(t)}")
                for body in bodies_nodes:
                    body.plot_point.set_data(body.r[0], body.r[1])
                    body.plot_point.set_3d_properties(body.r[2])
                plt.pause(0.01)
            
            if i % plot_t_step == 0:
                hist_index = int(i/plot_t_step)
                historic_energy[hist_index]+=potential_energy(bodies_nodes, G)
                for j, body_node in enumerate(bodies_nodes):
                    #Save energies and positions
                    historic_positions[hist_index][j]=body_node.r
                    historic_energy[hist_index]+=1/2*body_node.mass*(body_node.v[0]**2+body_node.v[1]**2+body_node.v[2]**2)