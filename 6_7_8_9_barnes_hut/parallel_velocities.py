import numpy as np
import matplotlib.pyplot as plt

def remove_parallel_component_of_velocities(r, v):
    N=len(r)
    for body in range(1, N):
        r_sun_body=-(r[body]-r[0])
        r_sun_body_mod_sqr = (r_sun_body[0]**2+r_sun_body[1]**2+r_sun_body[2]**2)
        velocity_tangent_to_sun = np.dot(v[body], r_sun_body) * r_sun_body / r_sun_body_mod_sqr
        velocity_parallel_to_sun = v[body]-velocity_tangent_to_sun
        v[body] = velocity_parallel_to_sun

if __name__=="__main__":
    ax = plt.figure().add_subplot(projection='3d')

    N=20
    UNIVERSE_SIZE=1

    r=np.random.rand(N,3)
    r = 3*(2*np.arctan(np.exp(r))-0.75*r) -5
    for ri in r:
            if(np.random.rand(1)) >= 0.5:
                ri[0] *= -1
            if(np.random.rand(1)) >= 0.5:
                ri[1] *= -1
            if(np.random.rand(1)) >= 0.5:
                ri[2] *= -1
    #Now we move back out of negative numbers
    r+=0.5

    v = np.random.rand(N,3)*2e2-1e2

    r[0] = np.array([0.5,0.5,0.5])
    v[0] = np.array([0,0,0])

    remove_parallel_component_of_velocities(r,v)

    r*=UNIVERSE_SIZE

    for body in range(0, N):
        markersize = 4
        marker='.'
        if body == 0:
            markersize = 8
            marker='*'
        ax.plot(r[body,0],r[body,1],r[body,2],marker,markersize=markersize)
        ax.quiver(X=r[body,0],Y=r[body,1],Z=r[body,2],U=v[body,0],V=v[body,1],W=v[body,2], length=0.1, normalize=True)
        r_sun_body=-(r[body]-r[0])
        r_sun_body_mod_sqr = (r_sun_body[0]**2+r_sun_body[1]**2+r_sun_body[2]**2)
        velocity_tangent_to_sun = np.dot(v[body], r_sun_body) * r_sun_body / r_sun_body_mod_sqr
        ax.quiver(X=r[body,0],Y=r[body,1],Z=r[body,2],U=velocity_tangent_to_sun[0],V=velocity_tangent_to_sun[1],W=velocity_tangent_to_sun[2], color='r')

    ax.set_xlim([0, UNIVERSE_SIZE])
    ax.set_ylim([0, UNIVERSE_SIZE])
    ax.set_zlim([0, UNIVERSE_SIZE])

    plt.show()