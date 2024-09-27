import os
import requests
import matplotlib.pyplot as plt
from ProcessPatternsForMachine import *
from ImageToPattern import *
from AddBackgroundAndBorder import *

path =  "~/absolute/path/to/image.jpg"
stitches = 70 #number of stitches to cast on for knitting pattern
matrix = ImageToMatrix(path,stitches,num_colors=4)

#add border to image
p = "~/absolute/path/to/border/pattern/.../Islensk-Sjonabok/8_þjms2008-14/npy_txt/þjms2008-14_548/þjms2008-14_548_smallest_repeat_2.txt"
matrix = add_border(matrix = matrix,side = [1,1,1,1], size = [2,2,2,2], border_background_shade=4)  #adds empty border to image
matrix = add_border(matrix = matrix,border_file_path = p, side = [1,1,1,1],border_dark_shade= 4, border_background_shade=1) #adds pattern border to image


#preview of knitting pattern with hex colors
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
