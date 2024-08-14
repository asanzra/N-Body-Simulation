import numpy as np
import matplotlib.pyplot as plt
#In order to draw rectangles
import matplotlib.patches as patches

class node:
    #Initializes the object, setting its variables
    def __init__(self, mass, x, vx, y, vy, z, vz):
        self.mass = mass #Mass contained in this node (either sum of children or of the body contained here if external node)
        self.r = np.array([x, y, z]) #Absolute position of center of mass if internal node, or body itself if external (external empty nodes are None).
            #Positions are normalised (0 to 1), where 0 is included and 1 excluded.
        self.v = np.array([vx, vy, vz]) #Velocity of this node, not on internal nodes!!
        self.size = None #Length of one of the sides of the cube. Has to be 1/n, where n is an integer. For the root node, n=1, their children have n=2, etc.
        self.children = None #When children are created, these are always 8. A subdivision of this cube of space in 8 equal sub-cubes.
            #Children indexing where each can be in left(x0)/right(x1), front(y0)/back(y1) and bottom(z0)/top(z1) goes in this order:
            #0:x0y0z0, 1:x1y0z0, 2:x0y1z0, 3:x1y1z0, 4:x0y0z1, 5:x1y0z1, 6:x0y1z1, 7:x1y1z1. Left to right, front to back, then bottom to top.
        self.relative_r = None #Position inside its parents cube. The origin is the bottom, left front corner. 
            #Relative positions are also normalised (0 to 1), where 0 is included and 1 excluded.
        self.children_rectangles = None
        self.point = None
    
    #Restores a node to be in the root node level
    def restore(self):
        self.size = 1.
        #Create a copy of the array
        self.relative_r = np.array([self.r[0], self.r[1], self.r[2]])

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
        #... but the right/back/top ones need to be substracted their origin offset.
        for i, coord in enumerate(relative_r):
            if coord >= 1.:
                relative_r[i] -= 1.
        return child_index
    
    #Make a copy of the current node
    def make_copy(self):
        new_node = node(self.mass, self.r[0], self.v[0], self.r[1], self.v[1], self.v[2], self.r[2])
        new_node.r = self.r
        new_node.mass = self.mass
        new_node.v = self.v
        new_node.size = self.size
        new_node.relative_r = self.relative_r
        return new_node
    
    #Draws rhe quadrants of the children
    def draw_children(self, ax):
        size = self.size
        #Left front bottom corner of node
        coordinates_of_node = (self.r//size) * size

        children_size = size / 2.
        for x in range(2):
            for y in range(2):
                offset = np.array([x, y, 0])*children_size
                rectangle = patches.Rectangle((coordinates_of_node + offset), children_size, children_size, linewidth=1, edgecolor='k', facecolor='none')
                self.children_rectangles[x+2*y] = rectangle
                ax.add_patch(rectangle)



# Tries to place a body in a place, checking if the place is free.
# The place_node must be set to the return or this function, as this
# function fills and updates it.
        
# This function is used
        #1.In the main loop to update the root node.
        #2.Recursively inside this function to update any internal nodes.
def place_node_inside_node(body_node, place_node, ax):
    body_node.point.set(color='b',marker="*", markersize=7.)
    plt.pause(0.2)
    if place_node is None: #This node is free, use it! Example: First placed node (in empty root).
        new_node_in_place = body_node
    else: #Place node occupied. Could be internal or external (leaf)
        if place_node.children is None:
            #Place node was an external node (occupied by another body!).

            evicted_body = place_node #The body that was here gets "evicted"
            evicted_body.point.set(color='r',marker="*", markersize=7.)
            plt.pause(0.1)
            internal_node = evicted_body.make_copy() #We create a parent internal node for the two bodies
            #Now we have two bodies to place as children, and we must update internal_node' center of mass and total mass.
            internal_node.children  = np.array([None]*8)
            internal_node.children_rectangles = np.array([None]*8)
            #We created the children and we draw their quads
            internal_node.draw_children(ax)
            evicted_body_new_place = evicted_body.get_my_child_index__moving_me_to_deeper_node()
            internal_node.children[evicted_body_new_place] = evicted_body
            evicted_body.point.set(color='g',marker=".", markersize=5.5)
            plt.pause(0.1)
        else: 
            #Place node was an internal node, at least with 1 child. It remains in its place.
            internal_node = place_node
        
        #Now we still have to place body_node inside the internal_node
        #First we update the mass and centre or mass of the internal node
        total_mass = body_node.mass + internal_node.mass
        internal_node.r = (internal_node.r*internal_node.mass+body_node.r*body_node.mass)/total_mass
        internal_node.mass = total_mass

        #Now we place the new node inside its destined child place
        body_new_place = body_node.get_my_child_index__moving_me_to_deeper_node()
        internal_node.children[body_new_place] = place_node_inside_node(body_node, internal_node.children[body_new_place], ax)
        #internal_node.children_rectangles[body_new_place].draw()
        #We do this recursively because:
            #1. If that child spot is free it will be simply occupied.
            #2. If that child spot is occupied (for example by evicted child or bc place_node was internal),
                #it will be handled correctly.

        new_node_in_place = internal_node
    body_node.point.set(color='g',marker=".", markersize=5.5)
    plt.pause(0.2)
    return new_node_in_place