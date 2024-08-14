#Based on https://gist.github.com/homerjed/985be9737b07eb72196c004d92ae72f0

import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def wireframe(ax, origin, size, visible=True):
    Z = size * np.array([[0,+1,0], [+1,+1,0], 
                         [+1,0,0], [0,0,0], 
                         [0,+1,+1], [+1,+1,+1], 
                         [+1,0,+1], [0,0,+1]]) + origin
    verts = [[Z[0],Z[1],Z[2],Z[3]],
             [Z[4],Z[5],Z[6],Z[7]],
             [Z[0],Z[1],Z[5],Z[4]],
             [Z[2],Z[3],Z[7],Z[6]], 
             [Z[1],Z[2],Z[6],Z[5]],
             [Z[4],Z[7],Z[3],Z[0]]] # return verts
    return ax.add_collection3d(Poly3DCollection(verts, 
                                         facecolors=(0,0,0,0),
                                         linewidths=1, 
                                         edgecolors='blueviolet',
                                         visible=visible))

class WireframeHolder:
    def __init__(self, ax, UNIVERSE_SIZE):
        self.ax = ax
        self.UNIVERSE_SIZE = UNIVERSE_SIZE
        self.wireframe_list = []

    def add_wireframe(self, body_position, size, visible=True):
        real_uni_size = size * self.UNIVERSE_SIZE
        coordinates_of_node = (body_position//real_uni_size) * real_uni_size
        self.wireframe_list.append(wireframe(self.ax, origin=coordinates_of_node, size=real_uni_size, visible=visible))

    def set_wireframes_visibility(self, visibility):
        for wireframei in self.wireframe_list:
            wireframei.set(visible=visibility)

    def reset_list(self):
        for wireframei in self.wireframe_list:
            wireframei.remove()
        self.wireframe_list.clear()