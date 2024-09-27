import numpy as np
import os
import requests
import matplotlib.pyplot as plt
from ProcessPatternsForMachine import *
from ImageToPattern import *
from AddBackgroundAndBorder import *

path = "~/absolute/path/to/image.png"
background_path = "~/absolute/path/to/Islensk-Sjonabok/3_þjms6950/npy_txt/þjms6950_326.txt"

stitches = 100 #number of stitches to cast on for knitting pattern

matrix = ImageToMatrix(path,stitches,num_colors=4)
matrix = removeSinglePixels(matrix, matrix_background_color=1)
matrix = add_background(matrix,background_path,background_color_0 = 2,background_color_1=3, border=True, border_color=1)

#preview of knitting pattern
viewColoredMatrix(matrix,"#f7e35e","#d14f90","#215215","#592222")


#processing before sending to machine
pattern = separateColors(matrix)
start = -60

#post request for passapE6000
"""
r = requests.post('http://localhost:3000'), json={
    "start":start,
    "pattern":pattern
})
"""








