import numpy as np
#Abstracted functions for clarity and modularisation
from universals_8_9 import UNIVERSE_SIZE, G
from parallel_velocities import remove_parallel_component_of_velocities
from node_8_9 import node

def get_starting_variables(N):
    #Masses ranging from 10^23- 10^27
    masses = 10**(np.random.rand(N)*4+23)
    
    #Playing with a graphical calculator to get a nice distribution where there is more in the centre,
    #P(x)=3(sech(x)-0.75) looks like a nice bell. Integrating it, we obtain the conversion from 0 to 1:
    #x=3(2arctg(exp(y))-0.75x+const). The substracting and multiplying cuts the normalised off at +-0.8.
    #It is a good idea to keep distance with margins because some particles will escape.

    r = np.random.rand(N,3)
    r = 3*(2*np.arctan(np.exp(r))-0.75*r) -5

    #The above generates one octant of all space, so we fill the rest by randomly inverting coordinates.
    for ri in r:
        if(np.random.rand(1)) >= 0.5:
            ri[0] *= -1
        if(np.random.rand(1)) >= 0.5:
            ri[1] *= -1
        if(np.random.rand(1)) >= 0.5:
            ri[2] *= -1
    #Now we move back out of negative numbers
    r+=0.5

    #The speeds will just be from 0 to 3 times (in magnitude) that of a circular orbit around center big massive object.
    v = np.random.rand(N,3)

    #Massive central object.
    masses[0] = 1.989e33
    r[0] = np.array([0.5,0.5,0.5])
    v[0] = np.array([0,0,0])

    #Center around middle. No negative values of position used.
    r=r*UNIVERSE_SIZE

    #Ensure no planet has starting velocity towards or away from center, to reach stability faster.
    remove_parallel_component_of_velocities(r,v)

    #Scale velocities by that of regular orbit
    for i, vi in enumerate(v):
        dist = np.sqrt((r[i,0]-0.5)**2+(r[i,1]-0.5)**2+(r[i,2]-0.5)**2)
        vi*=np.sqrt(G*masses[0]/dist)

    bodies_nodes = []
    for i in range(len(masses)):
        bodies_nodes.append(node(masses[i], r[i], v[i]))

    return bodies_nodes