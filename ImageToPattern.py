import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os



def findNearestColor(value, colors):
    """
    Use: nearest = findNearestColor(value, colors)
    Pre: value is any number and colors is a list of numbers
    Post: nearest is the number in colors that value is closest to
    """
    return colors[np.argmin(np.abs(colors - value))]



def ImageToMatrix(path, stitches, num_colors = 4):
    """
    Resize first and then decrease colors

    Use: Matrix = ImageToMatrix(path, stitches, num_colors)
    Pre: path is the absolute path to an image that is to be converted in a string.
         stitches is the number of columns to be in Matrix, num_colors is an integer
         either 3 or 4 and represents how many colors are the be in Matrix
    Post: Matrix is a matrix of integers from 1-3 or 1-4 depending on num_colors with the
          lightest color in the gray scale being 1 and the darkest the highest number. Matrix
          represents the image from path where it has been shrunken so that the number of
          columns are equal to stitches. The Floyd-Steinberg algorithm is used to decrease the
          number of colors.
    """
    img = Image.open(os.path.expanduser(path))
    img = img.convert("L")
    original_width,original_height = img.size
    heightLengthRatio = original_height/original_width
    rows = round(stitches*heightLengthRatio)

    img.thumbnail((stitches, rows), Image.ANTIALIAS) # resizes image in-place

    img_array = np.array(img) #image to numpy array
    img_array = img_array/255.0 #skala gratona bilid

    if img_array.shape[1] != stitches:
        stitches = img_array.shape[1] 


    if num_colors == 3:
        colors = np.array([0, 0.5, 1])
    elif num_colors == 4:
        colors = np.array([0, 0.33, 0.66, 1])
    else:
        raise ValueError(f"num cols is {num_colors}. num_colors must be either 3 or 4.")
    

    # Error diffusion dithering (w Floyd-Steinberg algorithm)
    for y in range(rows):
        for x in range(stitches):
            old_pixel = img_array[y, x]
            new_pixel = findNearestColor(old_pixel, colors)
            img_array[y, x] = new_pixel
            quant_error = old_pixel - new_pixel
            
            if x + 1 < stitches:
                img_array[y, x + 1] += quant_error *  7/ 16
            if y + 1 < rows:
                if x - 1 >= 0:
                    img_array[y + 1, x - 1] += quant_error * 3 / 16
                img_array[y + 1, x] += quant_error * 5 / 16
                if x + 1 < stitches:
                    img_array[y + 1, x + 1] += quant_error * 1 / 16

    #plt.imshow(img_array,cmap="grey")
    #plt.show()
    
    #set knitting pattern colors
    if num_colors==3:
        img_array[img_array==0.5] = 2
        img_array[img_array==0] = 3

    else:
        img_array[img_array==0.66] = 2
        img_array[img_array==0.33] = 3
        img_array[img_array==0.] = 4
    

    return img_array.astype(int)




def ImageToMatrix2(path, stitches, num_colors=4):
    """
    Works the same is ImageToMatrix but 
    decreases colors first and then resizes
    """
    image = Image.open(os.path.expanduser(path))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    original_width,original_height = image.size
    heightLengthRatio = original_height/original_width
    rows = round(stitches*heightLengthRatio)
    result.thumbnail((stitches, rows), Image.ANTIALIAS) # resizes image in-place
    img_array = np.array(result) #image to numpy array
    img_array[img_array==3] = 4
    img_array[img_array==2] = 3
    img_array[img_array==1] = 2
    img_array[img_array==0] = 1
    return img_array.astype(int)





def removeSinglePixels(img_array, background_starts=None, matrix_background_color=1):
    """
    If a non background pixel only has background pixels up,down,left and right of it, 
    it is changed to matrix_background_color.
    The function goes through the backround with flood-fill from each corner of the matrix.
    For custom starts of the flood-fill let background_starts be a list of tuples (i,j) of 
    the img_array indexes where the algorithm should start searching for single pixels.
    """
    matrix = np.copy(img_array)
    n, m = matrix.shape
    
    if background_starts:
        to_visit = set(background_starts)
    else:
        to_visit = {(0, 0), (n-1, 0), (0, m-1), (n-1, m-1)}
    
    non_background_pixels = []
    non_border_colors = {matrix_background_color, 13,11}
    
    while to_visit:
        current = to_visit.pop()
        x, y = current
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                searching_idx = (nx, ny)
                if matrix[searching_idx] == matrix_background_color and searching_idx not in to_visit:
                    to_visit.add(searching_idx)
                elif matrix[searching_idx] not in non_border_colors:
                    non_background_pixels.append(searching_idx)
                    matrix[current] = 13  # Mark it temporarily as part of the border
        matrix[current] = 11
    indices = matrix == 11 
    matrix[indices] = matrix_background_color

    while non_background_pixels:
        current = non_background_pixels.pop(0)
        x, y = current
        
        non_background_pixel_encountered = False
        
        #for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if matrix[(nx, ny)] != matrix_background_color:
                    non_background_pixel_encountered = True
                    break
        
        if not non_background_pixel_encountered:
            matrix[current] = matrix_background_color
    
    indices = matrix == 13
    matrix[indices] = img_array[indices]

    return matrix







def viewColoredMatrix(matrix, color_1, color_2, color_3, color_4):
    """
    Use: viewColoredMatrix(patternMatrix, col_1, col_2, col_3, col_4)
    col_1,col_2,col_3,col_4 are strings of hex colors
    Post: a preview of the patternmatrix matrix win the hex colors
          col_1 is the lightest shade of color while color_4 is the darkest.
    """
    #get RGB colors from hex
    h1 = color_1.lstrip('#')
    rgb1 = tuple(int(h1[i:i+2], 16) for i in (0, 2, 4))
    h2 = color_2.lstrip('#')
    rgb2 = tuple(int(h2[i:i+2], 16) for i in (0, 2, 4))
    h3 = color_3.lstrip('#')
    rgb3 = tuple(int(h3[i:i+2], 16) for i in (0, 2, 4))
    h4 = color_4.lstrip('#')
    rgb4 = tuple(int(h4[i:i+2], 16) for i in (0, 2, 4))
    
    rgb_colors = [rgb1, rgb2, rgb3, rgb4]
    
    # Create a new matrix with RGB values
    rgb_matrix = []
    for row in matrix:
        rgb_row = [rgb_colors[val - 1] for val in row]
        rgb_matrix.append(rgb_row)
    
    # Convert to numpy array
    rgb_matrix_np = np.array(rgb_matrix, dtype=np.uint8)
    
    plt.imshow(rgb_matrix_np)
    plt.show()


