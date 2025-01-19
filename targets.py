from skimage import draw
import numpy as np
import math


def add_target(x, y, radius, num_rings, data):
    for i, r in zip(range(num_rings), reversed(range(num_rings))):
        ring_size = (r+1) * (radius/num_rings)
        if (i % 2) != 0:
            ring_color = (1, 1, 1)
        else:
            ring_color = (1, 0, 0)
        rr, cc = draw.disk((x, y), radius=ring_size, shape=data.shape)
        data[rr, cc, :] = ring_color
    return data

def get_new_target_data(x_dim, y_dim, min_radius, max_radius, min_rings, max_rings):
    radius = np.random.uniform(min_radius, max_radius)
        
    num_rings = np.random.uniform(min_rings, max_rings)

    min_x = radius
    max_x = x_dim - radius
    min_y = radius
    max_y = y_dim - radius
    x = np.random.uniform(min_x, max_x)
    y = np.random.uniform(min_y, max_y)
    
    return x, y, num_rings, radius

def circle_intersection(x1, y1, r1, x2, y2, r2):
  
    dist_centers = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    radius_sum = r1 + r2
    
    if dist_centers < radius_sum:
        return True
    return False

def create_scene(x_dim = 750, y_dim = 1000, 
                 num_targets=3, min_radius=50, max_radius=100, 
                 min_rings=4, max_rings=6, colors=None):
    """
    Creates multiple new targets of varying radius, number of rings, and color
    
    Parameters:
    num_targets - the number of targets
    min_radius - the minimum radius of a target
    max_radius - the maximum radius of a target
    min_rings - the minimum number of rings on a target
    max_rings - the maximum number of rings on a target
    colors - the colors to use for the targets, must have length equal to num_targets
    """
    if colors:
        assert len(colors) == num_targets, "Number of colors specified must equal number of targets."
    
    scene_arr = np.zeros((x_dim, y_dim, 3)) + 1
    targets = []
    targets_metadata = []
    
    for n in range(num_targets):
        x, y, num_rings, radius = get_new_target_data(x_dim, y_dim, min_radius, max_radius, min_rings, max_rings)
        
        # Check for overlap with existing targets and redo target if it there is overlap        
        while True:
            is_overlapping = False
            
            # Check for overlap with existing targets
            for t in targets_metadata:
                targets_intersect = circle_intersection(t[0], t[1], t[2], x, y, radius)
                if targets_intersect:
                    is_overlapping = True
            
            # If there is overlap, redo the target and check again. If not, break and continue with rest of target creation
            if is_overlapping:
                x, y, num_rings, radius = get_new_target_data(x_dim, y_dim, min_radius, max_radius, min_rings, max_rings)    
            else:
                break
                
        scene_arr = add_target(x, y, radius=radius, num_rings=int(num_rings), data=scene_arr)
        targets_metadata.append((x, y, radius))
        
    return scene_arr, targets_metadata