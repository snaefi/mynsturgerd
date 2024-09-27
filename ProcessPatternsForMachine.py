import numpy as np
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
    

    
def duplicateLines(matrix):
    """
    duplicates all rows of a matrix
    """
    matrix = np.array(matrix)
    matrix = np.repeat(matrix, 2, axis=0)
    return matrix




def separateColors(A):
    """ 
    The function takes in a pattern matrix A that consists only
    of integers 1-4 and separates each color in each
    row into a list of lists, with each row twice. 
    example: if A = [[1,2,3,4],[2,2,2,1]] (A is a numpy array) 
    then the return value of the function is:
        [[1,0,0,0],[1,0,0,0],[0,2,0,0],[0,2,0,0],[0,0,3,0],[0,0,3,0],[0,0,0,4],[0,0,0,4],
         [0,0,0,1],[0,0,0,1],[2,2,2,0],[2,2,2,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    """
    res = []
    n, m = A.shape
    max = np.max(A)
    for row in A:
        lists = {i: [0]*m for i in range(1, max+1)}
        for idx, value in enumerate(row):
            lists[value][idx] = int(value)
        for i in range(1, max+1):
            #if any(lists[i]):
                res.extend([lists[i], lists[i]])  # Add each list twice
    return res



def patternMatrixToJson(A,start,file):
    """
    The function takes in a pattern matrix A and writes out a json object
    that is compatable with the pattern format that are sent with 
    passAPI to the passapE6000 knitting machine.
    A must have <= 180 columns and can only contain integers 0-4.
    start is the start position on the needlebed from -90:90
    file is the name and path of the output json file, 
     ex: /path/to/file/myPattern.json
    """
    n,m = A.shape
    if not isPatternMatrix(A):
        raise ValueError(f"Your matrix doesn't fullfill the requirements of being a pattern matrix. The matrix must have <= 180 columns and > 1 and only consist of integers 1-4. Your matrix has {m} columns")
    if start + m > 90:
        raise ValueError(f"The start position is too far to the right. Your matrix has {m} stitches and start position at {start}, {start+m-90} stitches would be missing")
    
    separatedColors = separateColors(A)
    pattern = {"start":start, "pattern":separatedColors}

    json_object = json.dumps(pattern, cls=NpEncoder)
    with open(file, "w") as outfile:
        outfile.write(json_object)
    return pattern




def isPatternMatrix(A):
    """
    The function returns true if A fulfills requirements of being a pattern matrix
    i.e. has <= 180 columns and > 1 and consists only of the integers 0-4.
    """
    n,m = A.shape
    if m <=1 or m >180:
        return False
    
    validValues = [0, 1, 2, 3, 4]
    return np.all(np.isin(A, validValues))
