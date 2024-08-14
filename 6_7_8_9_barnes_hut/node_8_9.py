import numpy as np
import matplotlib.pyplot as plt
#Abstracted functions for clarity and modularisation
from universals_8_9 import UNIVERSE_SIZE

#!!-------------------------------------------!!-------------------------------------------------!!
#############This file expands node_7 with 3d wireframe visuals, but is very similar#############
#!!-------------------------------------------!!-------------------------------------------------!!

class node:
    #Initializes the object, setting its variables
    def __init__(self, mass, r, v):
        self.mass = mass #Mass contained in this node (either sum of children or of the body contained here if external node)
        self.r = r #Absolute position of center of mass if internal node, or body itself if external (external empty nodes are None).
            #Positions are normalised (0 to 1), where 0 is included and 1 excluded.
        self.depth = None #Depth n as defined in last variable.
        self.v = v #Velocity of this node, not on internal nodes!!
        self.size = None #Length of one of the sides of the cube. Has to be 1/n, where n is an integer. For the root node, n=1, their children have n=2, etc.
        self.children = None #When children are created, these are always 8. A subdivision of this cube of space in 8 equal sub-cubes.
            #Children indexing where each can be in left(x0)/right(x1), front(y0)/back(y1) and bottom(z0)/top(z1) goes in this order:
            #0:x0y0z0, 1:x1y0z0, 2:x0y1z0, 3:x1y1z0, 4:x0y0z1, 5:x1y0z1, 6:x0y1z1, 7:x1y1z1. Left to right, front to back, then bottom to top.
        self.relative_r = None #Position inside its parents cube. The origin is the bottom, left front corner. 
            #Relative positions are also normalised (0 to 1), where 0 is included and 1 excluded.
        self.plot_point = None #Graphical point in axis represetning this body
    
    #Restores a node to be in the root node level
    def restore(self):
        self.size = 1.
        self.depth = 1
        #Create a copy of the array
        self.relative_r = np.array([self.r[0], self.r[1], self.r[2]])/UNIVERSE_SIZE

    #The node where this body is has been subvidived. Thus, this node must find a place in the subvidided space.
    #This function changes the node's variables as that change implies, and returns its index as a 'newborn child'
    def get_my_child_index__moving_me_to_deeper_node(self):
        relative_r = self.relative_r
        #It will become a children and must follow the order rules above. Left is 0 included to 0.5 excluded, same for y and z.
        left = relative_r[0] < 0.5
        front = relative_r[1] < 0.5
        bottom = relative_r[2] < 0.5
        child_index = (not left) + (not front) * 2 + (not bottom) * 4
        #The subdivision doubles relative position by halving node size. ...
        relative_r *= 2.
        self.size /= 2.
        self.depth *= 2
        #... but the right/back/top ones need to be substracted their origin offset.
        for i, coord in enumerate(relative_r):
            if coord >= 1.:
                relative_r[i] -= 1.
        return child_index
    
    #Modulus distance from self to node j
    def rij(self, j):
        i = self
        rij = i.r-j.r
        rijmod = np.sqrt(rij[0]**2+rij[1]**2+rij[2]**2)
        if rijmod > 1e35:
            raise Exception(f"Positions very far away. ri: {i.r}, rj: {j.r}. rij={rij}")
        return rijmod
    
    #Force j makes on self(i)
    def grav_acc(self, j):
        i = self
        if i == j:
            return 0.
        rijmod_cubed = i.rij(j)**3.
        if abs(rijmod_cubed) < 1e-10:
            raise Exception(f"Close prox at distance: {rijmod_cubed}")
        return (j.r - i.r) * j.mass / rijmod_cubed
    
    #Make a copy of the current node
    def make_copy(self):
        new_node = node(self.mass, self.r, self.v)
        new_node.r = self.r
        new_node.mass = self.mass
        new_node.v = self.v
        new_node.size = self.size
        new_node.relative_r = self.relative_r
        return new_node


# Tries to place a body in a place, checking if the place is free.
# The place_node must be set to the return or this function, as this
# function fills and updates it.
        
# This function is used
        #1.In the main loop to update the root node.
        #2.Recursively inside this function to update any internal nodes.
def place_node_inside_node(body_node, place_node, bodies_nodes, historic_positions, wireframeHolder, draw_tree_fill):
    if draw_tree_fill:
        body_node.plot_point.set(color='g', marker='*', markersize=7.)
        wireframe_pause_time=0.001
        plt.pause(wireframe_pause_time)
    if place_node is None: #This node is free, use it! Example: First placed node (in empty root).
        new_node_in_place = body_node
    else: #Place node occupied. Could be internal or external (leaf)
        if place_node.children is None and place_node.size > 10e-27:
            if draw_tree_fill:
                place_node.plot_point.set(color='r', marker='*', markersize=7.)
                plt.pause(wireframe_pause_time)
            #Place node was an external node (occupied by another body!).
            
            evicted_body = place_node #The body that was here gets "evicted"
            internal_node = evicted_body.make_copy() #We create a parent internal node for the two bodies
            #Now we have two bodies to place as children, and we must update internal_node' center of mass and total mass.
            internal_node.children  = np.array([None]*8)
            internal_node.children_rectangles = np.array([None]*8)
            evicted_body_new_place = evicted_body.get_my_child_index__moving_me_to_deeper_node()
            internal_node.children[evicted_body_new_place] = evicted_body
            if draw_tree_fill:
                wireframeHolder.add_wireframe(body_position=evicted_body.r, size=evicted_body.size, visible=True)
                evicted_body.plot_point.set(color='b', marker='.', markersize=5.)
                plt.pause(wireframe_pause_time)
        else: 
            #Place node was an internal node, at least with 1 child. It remains in its place.
            internal_node = place_node
        
        #Now we still have to place body_node inside the internal_node
        #First we update the mass and centre or mass of the internal node
        total_mass = body_node.mass + internal_node.mass
        internal_node_alone_mass = (internal_node.mass).copy()
        internal_node.r = (internal_node.r*internal_node_alone_mass+body_node.r*body_node.mass)/total_mass
        internal_node.mass = total_mass

        if place_node.size < 10e-27:
            #Then we fuse the bodies, to prevent inifite oct tree divisions
            print(f"Fusing two bodies, depth of place node in tree: {place_node.depth}, of body node: {body_node.depth}. Their distance is: {place_node.rij(body_node)}")
            if body_node in bodies_nodes and body_node.children is None:
                momentum_body = body_node.v * body_node.mass
                momentum_place = place_node.v * internal_node_alone_mass
                place_node.v = momentum_body + momentum_place / internal_node.mass
                index = bodies_nodes.index(body_node)
                bodies_nodes.pop(index)
                historic_positions = np.delete(historic_positions, index, 1)
                print(f"{len(bodies_nodes)} bodies left")
            return place_node

        #Now we place the new node inside its destined child place
        body_new_place = body_node.get_my_child_index__moving_me_to_deeper_node()
        internal_node.children[body_new_place] = place_node_inside_node(body_node, internal_node.children[body_new_place],
                                                                        bodies_nodes, historic_positions, wireframeHolder,
                                                                        draw_tree_fill)
        if draw_tree_fill:
            wireframeHolder.add_wireframe(body_position=body_node.r, size=body_node.size, visible=True)
            body_node.plot_point.set(color='b', marker='.', markersize=5.)
            plt.pause(wireframe_pause_time)
        #internal_node.children_rectangles[body_new_place].draw()
        #We do this recursively because:
            #1. If that child spot is free it will be simply occupied.
            #2. If that child spot is occupied (for example by evicted child or bc place_node was internal),
                #it will be handled correctly.

        new_node_in_place = internal_node
    return new_node_in_place