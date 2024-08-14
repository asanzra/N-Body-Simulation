import numpy as np
from universe_variables import SOLVE_IVP, ODEINT, G
from scipy.integrate import solve_ivp, odeint
#Used for progress bar
from tqdm import tqdm
#Abstracted functions for clarity and modularisation
from get_variables import get_ode_variables, get_solve_ivp_variables

#!!--------------------###--------------------!!--------------------###--------------------------!!
##########THIS FILE IS THE EXACT SAME AS THE OTHERS WITH THE SAME NAME IN OTHER FOLDERS##########
#!!--------------------###--------------------!!--------------------###--------------------------!!

#This function defines de ODE for the solvers.
# vars fed into ODE : x1,x2,...,vx1,vx2,...,y1,y2,...,vy1,vy2,...,z1,z2,...,vz1,vz2,...
def odes(arg1, arg2, method, pbar, state, body_count, masses, G):
    #Obtains vars from arguments. For some reason these functions use different order.
    if method == ODEINT:
        vars = arg1
        t = arg2
    elif method == SOLVE_IVP:
        t = arg1
        vars = arg2
    else:
        "ODE received wrong method"

    #Updates progress bar based on percentage of time steps completed
    [last_t, dt_pbar] = state
    n = int((t - last_t)/dt_pbar)
    pbar.update(n)
    state[0] = last_t + dt_pbar * n

    vars = list(vars)
    sep = len(vars)/6 #Argument type separation. 0 to sep is x, sep to 2*sep is vx, etc.

    #Check for correct inputs
    if sep != int(sep):
        raise Exception(f"Expected a multiple of 6 for args, got: {len(vars)}")
    if sep != body_count:
        raise Exception(f"Expected a multiple of body count({body_count}) for args, got: {len(vars)}")
    sep = int(sep)

    #Obtain variables from provided arguments
    x = vars[0*sep:1*sep]
    dxdt = vars[1*sep:2*sep]
    y = vars[2*sep:3*sep]
    dydt = vars[3*sep:4*sep]
    z = vars[4*sep:5*sep]
    dzdt = vars[5*sep:6*sep]

    #We will hold these in vectors to benefit from vector operations when they are faster.
    dvxdt = np.zeros(body_count)
    dvydt = np.zeros(body_count)
    dvzdt = np.zeros(body_count)
    dvdt = np.array([dvxdt, dvydt, dvzdt])

    for i in range(body_count):
        xi = x[i]
        yi = y[i]
        zi = z[i]
        ri = np.array([xi, yi, zi])
        # For n >= j > i to avoid repetition of expensive sqrt operations
        for j in range(i, body_count):
            if i == j:
                continue
            xj = x[j]
            yj = y[j]
            zj = z[j]
            rj = np.array([xj, yj, zj])
            #Distance vector and magnitude cubed.
            rij = ri-rj
            rijmod_cubed = (np.sqrt(rij[0]**2+rij[1]**2+rij[2]**2))**3.
            # Set 3d velocities for both bodies
            for coordinate in range(3):
                dvdt[coordinate][i] += masses[j] / rijmod_cubed * -rij[coordinate]
                dvdt[coordinate][j] += masses[i] / rijmod_cubed * rij[coordinate]
    dvdt = dvdt * G
    dvxdt = dvdt[0]
    dvydt = dvdt[1]
    # We return the derivatives
    return np.array([dxdt,dvxdt,dydt,dvydt,dzdt,dvzdt]).flatten()


#This function feeds the initial variable to the selected solver, with the appropiate parameters.
def ode_solve(method, initial_vars, t, body_count, masses, rtol=1.49012e-8, atol=1.49012e-8):

    state = [t[0], (t[-1]-t[0])/100] #Defines the state of the progress bar
    
    if method==ODEINT:
        #Starts a progress bar to show progress
        with tqdm(total=100, unit="‰") as pbar:
            vars = odeint(odes, initial_vars, t, args=(method,pbar,state,body_count,masses,G),
                      rtol=rtol, atol=atol,)
        time_size = len(t)

        #Gets all variables
        x, vx, y, vy, z, vz = get_ode_variables(body_count, time_size, vars)

    elif method==SOLVE_IVP:
        t_span = (t[0],t[-1])
        #Starts a progress bar to show progress
        with tqdm(total=100, unit="‰") as pbar:
            vars = solve_ivp(odes, t_span, initial_vars, t_eval=t, args=(method,pbar,state,body_count,masses,G), 
                            method='LSODA', dense_output=True,
                            rtol=rtol, atol=atol)
            
        #Gets all variables
        vars = vars.y
        x, vx, y, vy, z, vz = get_solve_ivp_variables(body_count, vars)
    else:
        "ODE solve received wrong method"
    return np.array([x, vx, y, vy, z, vz])