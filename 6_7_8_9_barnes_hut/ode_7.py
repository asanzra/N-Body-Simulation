from universals_7 import AU, UNIVERSE_SIZE
#Multiprocessing
from multiprocessing import Process
#Number of subprocesses for multiprocessing
#NOT FASTER THAN SINGLE CORE. 
process_size = 1 #NOTE: Highly recommended to be 1 in order to work properly

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

#This function works out the change in position and velocity for one body at a time
def work_on_ode_steps(bodies_nodes_left, root_node, G, theta, dt):
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

#This function calculated the ODE step for all bodies. 
#Assigns different processes to different nodes if process_size > 1
#NOTE: This does not accelerate the performance, given the small task
#each process receives compared to the time it takes to start/end.
#Recommended process_size = 1 in order to work properly
def ode_step(bodies_nodes, root_node, theta, G, dt):
    bodies_nodes_left = bodies_nodes.copy()
    if process_size > 1:
        processes = []
        for i in range(process_size):
            p = Process(target=work_on_ode_steps, args=(bodies_nodes_left, root_node, G, theta, dt))
            #Starts the process, which will, in a loop,
            #pull one body not yet calculated and calculate them
            p.start()
            processes.append(p)

        for p in processes:
            #Here we wait for all process to finish, and this is the 
            #limiting factor.
            p.join()
    else:
        #If multiprocessing disabled, calculate all on main process.
        work_on_ode_steps(bodies_nodes_left, root_node, G, theta, dt)