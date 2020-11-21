
import random
import numpy as np
import math
import operator
from sympy import symbols, diff

"""Defining intensity function and calculating intensity at all locations on wall
Function to calculate intensity at a specific point (x_wall,y_wall) on the wall"""
def Intensity(x1,y1,x2,y2,x3,y3,z0,x_wall,y_wall):
  I=p1/(4*math.pi*math.sqrt(math.pow((x_wall-x1),2)+math.pow((y_wall-y1),2)+math.pow((z0-1),2)))+p2/(4*math.pi*math.sqrt(math.pow((x_wall-x2),2)+math.pow((y_wall-y2),2)+math.pow((z0-1),2)))+p3/(4*math.pi*math.sqrt(math.pow((x_wall-x3),2)+math.pow((y_wall-y3),2)+math.pow((z0-1),2)))
  return I

#The function Intensity_Grid returns a 2D array with the intensity values at all points on the wall.
def Intensity_Grid(x1,y1,x2,y2,x3,y3,z0):
  intensity = [[0 for i in range(num_grid_points)] for j in range(num_grid_points)]
  for i in range(0,num_grid_points):
    for j in range(0,num_grid_points):
      intensity[i][j]=Intensity(x1,y1,x2,y2,x3,y3,z0,xw[i],yw[j])
  return intensity


"""Function to calculate standard deviation of intensities at the points on the grid"""
def stddev(intensity, num_grid_points):
  sum=0
  sum_s=0
  for i in range(0,num_grid_points):
    for j in range(0,num_grid_points):
      sum+=intensity[i][j]
  mean=sum/100
  for i in range(0,num_grid_points):
    for j in range(0,num_grid_points):
      sum_s+=math.pow(intensity[i][j]-mean,2)
  J=math.sqrt(sum_s/100)
  return J
