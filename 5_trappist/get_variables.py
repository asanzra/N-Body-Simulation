import numpy as np

#!!--------------------###--------------------!!--------------------###--------------------------!!
##########THIS FILE IS THE EXACT SAME AS THE OTHERS WITH THE SAME NAME IN OTHER FOLDERS##########
#!!--------------------###--------------------!!--------------------###--------------------------!!

#Gets all variables. This is the fastest method found, although long in code.
def get_ode_variables(body_count, time_size, vars):
    print("Getting x...")
    x = np.array(np.zeros((body_count, time_size)))
    for i, body in enumerate(range(0*body_count, 1*body_count)):
        x[i] = np.array([col[body] for col in vars])

    print("Getting vx...")
    vx = np.array(np.zeros((body_count, time_size)))
    for i, body in enumerate(range(1*body_count, 2*body_count)):
        vx[i] = np.array([col[body] for col in vars])

    print("Getting y...")
    y = np.array(np.zeros((body_count, time_size)))
    for i, body in enumerate(range(2*body_count, 3*body_count)):
        y[i] = np.array([col[body] for col in vars])

    print("Getting vy...")
    vy = np.array(np.zeros((body_count, time_size)))
    for i, body in enumerate(range(3*body_count, 4*body_count)):
        vy[i] = np.array([col[body] for col in vars])

    print("Getting z...")
    z = np.array(np.zeros((body_count, time_size)))
    for i, body in enumerate(range(4*body_count, 5*body_count)):
        z[i] = np.array([col[body] for col in vars])

    print("Getting vz...")
    vz = np.array(np.zeros((body_count, time_size)))
    for i, body in enumerate(range(5*body_count, 6*body_count)):
        vz[i] = np.array([col[body] for col in vars])

    return x, vx, y, vy, z, vz

#Gets all variables. This is the fastest method found, although long in code.
def get_solve_ivp_variables(body_count, vars):
    print("Getting x...")
    x=vars[0*body_count:1*body_count]
    print("Getting vx...")
    vx=vars[1*body_count:2*body_count]
    print("Getting y...")
    y=vars[2*body_count:3*body_count]
    print("Getting vy...")
    vy=vars[3*body_count:4*body_count]
    print("Getting z...")
    z=vars[4*body_count:5*body_count]
    print("Getting vz...")
    vz=vars[5*body_count:6*body_count]
    return x, vx, y, vy, z, vz