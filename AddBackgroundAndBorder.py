import numpy as np
import os
import matplotlib.pyplot as plt


def add_border(matrix, border_file_path="empty", side=[0,0,0,0], size=[0,0,0,0],border_dark_shade = 2,border_background_shade = 1):
    """
    Use: example:     matrix_with_border = add_border(matrix, "~/path/to/border/file" ,side=[1,1,0,0])
         or:    matrix_with_empty_border = add_border(matrix, side=[1,1,1,1], size=[3,3,2,2]) 
    Pre:  matrix is a binary pattern matrix from Sjonabok. border_file_path is the absolut path to the border txt file
          to add as border to matrix. If border_file_path="empty" an empty border(consisting of zeros) will be added to
          the appropriate sides of matrix.
          side is a list of length 4 and represents in order [top,bottom,left,right] the sides to which to add the border.
          if 0 then no border is added to said side, if 1 the border is added to the side.
          size is a list of length 4 of integers and represents in order [top,bottom,left,right] the size of the empty border
          that is to be added to each side.
    Post: matrix_with_border has added the border provided with the path to top and bottom of matrix.
          matrix_with_empty_border has added an empty boarder(consisting of ones) to all sides of matrix with
          where on the top and bottom the border has length 3 and on the sides the border has size 2.
    """
    if border_file_path=="empty":
        if side[0]:
            matrix = np.vstack((np.ones((size[0],matrix.shape[1])),matrix))
        if side[1]:
            matrix = np.vstack((matrix,np.ones((size[1],matrix.shape[1]))))
        if side[2]:
            matrix = np.hstack((np.ones((matrix.shape[0],size[2])),matrix))
        if side[3]:
            matrix = np.hstack((matrix,np.ones((matrix.shape[0],size[3]))))
        return matrix
    
    #load border
    border_smallest_repeat = np.loadtxt(os.path.expanduser(border_file_path),dtype=int)
    border_smallest_repeat[border_smallest_repeat==1] = border_dark_shade
    border_smallest_repeat[border_smallest_repeat==0] = border_background_shade

    height,length = matrix.shape 
    n,m = border_smallest_repeat.shape
    

    # horizontal border
    if side[0] or side[1]:
        #find length
        whole_multiples = length//m
        border = np.hstack([border_smallest_repeat]*whole_multiples) 
        remaining_border_lenght = length - border.shape[1]
        if remaining_border_lenght > 0:
            border = np.hstack((border,border[:,:remaining_border_lenght]))
        
        #add border to matrix
        if side[0]: #top
            matrix = np.vstack((border,matrix))
        if side[1]: #bottom
            matrix = np.vstack((matrix,border))

        height,length = matrix.shape #update shape

    
    #vertical border
    if side[2] or side[3]:
        #find length
        whole_multiples = height//m
        border = np.vstack([border_smallest_repeat.T]*whole_multiples)
        remaining_border_height = height - border.shape[0]

        if remaining_border_height > 0:
            border = np.vstack((border,border[:remaining_border_height,:]))

        #add vertical border to matrix
        if side[2]: #left
            matrix = np.hstack((border,matrix))
        if side[3]: #right
            matrix = np.hstack((matrix,border))

    return matrix




def find_first_not_background_from_center(matrix, background_color):
    rows, cols = matrix.shape
    center_row, center_col = rows // 2, cols // 2
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    step = 1 
    x, y = center_row, center_col  # search from center

    if matrix[x, y] != background_color:
        return (x, y)

    while step < max(rows, cols):
        for direction in directions:
            for _ in range(step):
                x += direction[0]
                y += direction[1]
                if x < 0 or x >= rows or y < 0 or y >= cols:
                    continue
                if matrix[x, y] != background_color:
                    return (x, y)
        if direction == directions[1] or direction == directions[3]:  # Double the step size after Down and Up directions
            step += 1

    return None  # Return None if no non background color found



def add_background(matrix, background_file_path="empty", matrix_background_color=1, background_starts=[], border=True, border_color=1,background_color_0=1,background_color_1=4):
    """
    Adds a Sjonabok pattern as background to matrix where the pattern is provided as an absolute path to a txt file as background_file-path.
    matrix_background_color is the background color of matrix. If border=True a border with color border_color is added around the main feature of the image,
    i.e. no background is added there.
    background_color_0 is the lighter shade of the sjonabok pattern and background_color_1 is the darker shade.
    The function goes through the backround of matrix with flood-fill from each corner of the matrix to find the main feature (i.e. not background).
    For custom starts of the flood-fill let background_starts be a list of tuples (i,j) of matrix indexes where the algorithm should start the flood-fill.
    """
    n,m = matrix.shape
    #make bakground matrix (same size as matrix)
    background_smallest = np.loadtxt(os.path.expanduser(background_file_path),dtype=int)
    background_smallest = background_smallest[:-1,:-1]
    background_smallest[background_smallest==1] = 11
    background_smallest[background_smallest==0] = 10
    background_smallest_n,background_smallest_m = background_smallest.shape

    #multiply vertical wise
    whole_multiples = n//background_smallest_n
    background = np.vstack([background_smallest]*whole_multiples)
    remaining_background_height = n - background.shape[0]
    if remaining_background_height > 0:
        background = np.vstack((background,background[:remaining_background_height,:]))

    #multiply horizontal wise
    #
    #breakpoint()
    whole_multiples = m//background_smallest_m
    background = np.hstack([background]*whole_multiples) 
    remaining_background_lenght = m - background.shape[1]
    if remaining_background_lenght > 0:
            background = np.hstack((background,background[:,:remaining_background_lenght]))
    
  
    #flood fill background of matrix with matrix, starting in top left corner
    if background_starts:
        to_visit = background_starts
    else:
        to_visit = [(0,0),(n-1,0),(0,m-1),(n-1,m-1)]
    
    border_encountered = 0 #border of main image
    non_border_colors = [matrix_background_color,10,11,13]
    while to_visit:
        current = to_visit[0] #cross we are searching from
        to_visit = to_visit[1:]
    #searching up
        if (current[0]-1) >= 0: #assuring we are not going out of matrix range
            searching_idx = (current[0]-1,current[1])
            if matrix[searching_idx]==matrix_background_color and searching_idx not in to_visit:
                to_visit.append(searching_idx)
            if matrix[searching_idx] not in non_border_colors:
                border_encountered = 1
            
        #searching down
        if (current[0]+1) < n:
            searching_idx = (current[0]+1,current[1])
            if matrix[searching_idx]==matrix_background_color and searching_idx not in to_visit:
                to_visit.append(searching_idx)
            if matrix[searching_idx] not in non_border_colors:
                border_encountered = 1

        #searching left
        if (current[1]+1) < m:
            searching_idx=(current[0],current[1]+1)
            if matrix[searching_idx]==matrix_background_color and searching_idx not in to_visit:
                to_visit.append(searching_idx)
            if matrix[searching_idx] not in non_border_colors:
                border_encountered = 1
            
        #searching right
        if current[1] - 1 >= 0:
            searching_idx=(current[0],current[1]-1)
            if matrix[searching_idx]==matrix_background_color and searching_idx not in to_visit:
                to_visit.append(searching_idx)
            if matrix[searching_idx] not in non_border_colors:
                border_encountered = 1
        """
        #search for background_color diagonally 1 from current    
        top_left_idx =     (current[0]-1,current[1]-1)
        bottom_left_idx =  (current[0]+1,current[1]-1)
        top_right_idx =    (current[0]-1,current[1]+1)
        bottom_right_idx = (current[0]+1,current[1]+1)
        if top_left_idx[0] >= 0 and top_left_idx[1] >= 0 and matrix[top_left_idx]==matrix_background_color and top_left_idx not in to_visit:
                to_visit.append(top_left_idx)
            
        if bottom_left_idx[0] < n and bottom_left_idx[1] >= 0 and matrix[bottom_left_idx]==matrix_background_color and bottom_left_idx not in to_visit:
                to_visit.append(bottom_left_idx)
            
        if top_right_idx[0] >= 0 and top_right_idx[1] < m and matrix[top_right_idx]==matrix_background_color and top_right_idx not in to_visit:
                to_visit.append(top_right_idx)

        if bottom_right_idx[0] < n and bottom_right_idx[1] < m and matrix[bottom_right_idx]==matrix_background_color and bottom_right_idx not in to_visit:
                to_visit.append(bottom_right_idx)
        """
        if border and border_encountered:
            matrix[current] = 13
        else:
            matrix[current] = background[current]
        border_encountered = 0

    matrix[matrix==11] = background_color_1
    matrix[matrix==10] = background_color_0
    if border:
        matrix[matrix==13] = border_color

    return matrix

            


def add_background_seamless(matrix, background_file_path="empty", matrix_background_color=1, background_starts=None, 
                   border=True, border_color=1, background_color_0=1, background_color_1=4, 
                   shift_background=None):
    """
    shift_background shifts background from top to bottom
    """
    n, m = matrix.shape
    
    # Load and process the background
    background_smallest = np.loadtxt(os.path.expanduser(background_file_path), dtype=int)
    background_smallest = background_smallest[:-1, :-1]
    background_smallest[background_smallest == 1] = 11
    background_smallest[background_smallest == 0] = 10
    background_smallest_n, background_smallest_m = background_smallest.shape

    if shift_background:
        background_smallest = np.roll(background_smallest, shift=-shift_background, axis=0)
   
    # Create background
    #multiply vertical wise
    whole_multiples = n//background_smallest_n
    background = np.vstack([background_smallest]*whole_multiples)
    remaining_background_height = n - background.shape[0]
    if remaining_background_height > 0:
        background = np.vstack((background,background[:remaining_background_height,:]))

    #multiply horizontal wise

    whole_multiples = m//background_smallest_m
    background = np.hstack([background]*whole_multiples) 
    remaining_background_lenght = m - background.shape[1]
    if remaining_background_lenght > 0:
            background = np.hstack((background,background[:,:remaining_background_lenght]))
    background = background[:n, :m]

    # Shift the background to start at the custom start point
    #breakpoint()
    #background = np.roll(background, shift=(start_y, start_x), axis=(0, 1))

    # Initialize the BFS search from the corners or provided start points
    if background_starts is None:
        to_visit = [(0, 0), (n-1, 0), (0, m-1), (n-1, m-1)]
    else:
        to_visit = background_starts

    non_border_colors = {matrix_background_color, 10, 11, 13}

    while to_visit:
        x, y = to_visit.pop(0)
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # Up, Down, Left, Right

        border_encountered = False

        for nx, ny in neighbors:
            if 0 <= nx < n and 0 <= ny < m:
                if matrix[nx, ny] == matrix_background_color and (nx, ny) not in to_visit:
                    to_visit.append((nx, ny))
                if matrix[nx, ny] not in non_border_colors:
                    border_encountered = True

        if border and border_encountered:
            matrix[x, y] = 13
        else:
            matrix[x, y] = background[x, y]

    # Replace temporary colors with final background colors
    matrix[matrix == 11] = background_color_1
    matrix[matrix == 10] = background_color_0
    if border:
        matrix[matrix == 13] = border_color

    return matrix


def get_background_cutoff_row_number(image_rows, background_rows, last_image_background_cutoff_row_number):
    """
    image_to_shift_rows is the number of rows in the image that is to be shifted
    background_rows is the number of rows in background file
    last_image_background_cutoff is b in last_image_rows = a*n+b where n is background rows
    """
    #last_image_rows = a*n+b (b=last_image_background_cutoff_line_number, n=background_rows)
    #this_image_rows = c*n+b
    #this_image_roll = n-b
    #this_image_cutoff_line_number = d-(n-b) (if d-n+b<0 then cutoff_line_number = d-n+b+n = d+b)
    n = background_rows
    d = image_rows%n
    b = last_image_background_cutoff_row_number
    cutoff_line_number = d-n+b
    if cutoff_line_number < 0:
        cutoff_line_number = d+b
    return cutoff_line_number



def get_background_shift(image_rows, background_rows, last_image_background_cutoff_row_number):
    return background_rows - get_background_cutoff_row_number(image_rows, background_rows, last_image_background_cutoff_row_number)



