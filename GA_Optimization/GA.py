# -*- coding: utf-8 -*-

import random
import numpy as np
import math
import operator
from sympy import symbols, diff
import matplotlib.pyplot as plt
#from Helper Intensity, stddev
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--num_grid_points", type=int, help="size of grid")
parser.add_argument("--num_iter", type=int, default=40, help="number of iterations")
parser.add_argument("--intensity_lim", type=float, default=20, help="minimum intensity")
parser.add_argument("--penalty_stiffness", type=float, default=0.6, help="Penalty Stiffness")
parser.add_argument("--p1", type=float, default=100, help="Power of bulb 1")
parser.add_argument("--p2", type=float, default=100, help="Power of bulb 2")
parser.add_argument("--p3", type=float, default=100, help="Power of bulb 3")
opt = parser.parse_args()
print("Args passed")
print(opt)

"""Defining intensity function and calculating intensity at all locations on wall
Function to calculate intensity at a specific point (x_wall,y_wall) on the wall"""
def Intensity(x1,y1,x2,y2,x3,y3,z0,x_wall,y_wall):
  I=opt.p1/(4*math.pi*math.sqrt(math.pow((x_wall-x1),2)+math.pow((y_wall-y1),2)+math.pow((z0-1),2)))+opt.p2/(4*math.pi*math.sqrt(math.pow((x_wall-x2),2)+math.pow((y_wall-y2),2)+math.pow((z0-1),2)))+opt.p3/(4*math.pi*math.sqrt(math.pow((x_wall-x3),2)+math.pow((y_wall-y3),2)+math.pow((z0-1),2)))
  return I

#The function Intensity_Grid returns a 2D array with the intensity values at all points on the wall.
def Intensity_Grid(x1,y1,x2,y2,x3,y3,z0):
  intensity = [[0 for i in range(opt.num_grid_points)] for j in range(opt.num_grid_points)]
  for i in range(0,opt.num_grid_points):
    for j in range(0,opt.num_grid_points):
      intensity[i][j]=Intensity(x1,y1,x2,y2,x3,y3,z0,xw[i],yw[j])
  return intensity


"""Function to calculate standard deviation of intensities at the points on the grid"""
def stddev(intensity):
  sum=0
  sum_s=0
  for i in range(0,opt.num_grid_points):
    for j in range(0,opt.num_grid_points):
      sum+=intensity[i][j]
  mean=sum/100
  for i in range(0,opt.num_grid_points):
    for j in range(0,opt.num_grid_points):
      sum_s+=math.pow(intensity[i][j]-mean,2)
  J=math.sqrt(sum_s/100)
  return J


"""Genetic Algorithm"""

"""Generate_initial_gen()
Function for initialising a generation"""
def Generate_initial_gen():
  new_gen=[[0 for i in range(14)] for j in range(14)];
  for i in range(0,14):
    for j in range(0,14):
      new_gen[i][j]=random.randint(0,9)
  return new_gen;

#Parent_pool(new_gen[14][14])"""

xw=np.linspace(0,1,opt.num_grid_points)        #Dividing points on the wall in a opt.num_grid_points*opt.num_grid_points grid with z coordinate of wall=1
yw=np.linspace(0,1,opt.num_grid_points)
zw=1

"""Function for getting the new set of 'better' parents from the current generation"""
def Parent_pool(new_gen):
  avg_J=0
  J=[0 for i in range(14)]
  for i in range(0,14):
    intensity0 = [[0 for j in range(opt.num_grid_points)] for k in range(opt.num_grid_points)]
    for j in range(0,opt.num_grid_points):
      for k in range(0,opt.num_grid_points):
        intensity0[j][k]=Intensity(new_gen[i][0]*0.1+new_gen[i][1]*0.01,new_gen[i][2]*0.1+new_gen[i][3]*0.01,new_gen[i][4]*0.1+new_gen[i][5]*0.01,new_gen[i][6]*0.1+new_gen[i][7]*0.01,new_gen[i][8]*0.1+new_gen[i][9]*0.01,new_gen[i][10]*0.1+new_gen[i][11]*0.01,new_gen[i][12]*0.1+new_gen[i][13]*0.01,xw[j],yw[k])
    J[i] = stddev(intensity0)
    avg_J= avg_J+J[i]
    min_intensity=(np.array(intensity0)).min()
    if min_intensity<opt.intensity_lim:
      J[i]=J[i]+opt.penalty_stiffness*(opt.intensity_lim-min_intensity)
  t=0;
  Parents = [[0 for j in range(14)] for k in range(7)] ####
  for i in range(0,14,2):
    if J[i]>J[i+1]:
      for j in range(0,14):
        Parents[t][j]=new_gen[i+1][j];
      t=t+1;
    else:
      for j in range(0,14):
        Parents[t][j]=new_gen[i][j];
      t=t+1;
  # print (avg_J/14)
  return Parents;


"""mate(parent1, parent2)
Function for mating between two parents (to generate two offsprings)"""
def mate(parent1, parent2):
  for i in range(0,14):
    x=random.random();
    if x>0.5:
      temp=parent1[i]
      parent1[i]=parent2[i]
      parent2[i]=temp
  return parent1, parent2

"""Generate_new_gen(parents[7][14])
Function for generating a new set of parents (after mating) from the current set of parents"""
def Generate_new_gen(Parents):
  new_gen=[[0 for i in range(14)] for j in range(14)]; ####
  b=1
  for i in range(0,7):
    index=0;
    while (b):
      index=random.randint(0,6);
      b=bool(index==i);
    child1, child2=mate(Parents[i],Parents[index])
    for k in range(0,14):
        new_gen[2*i][k]=child1[k]
        new_gen[2*i+1][k]=child2[k]
  return new_gen

"""Function to get the best individual from the final set of parents"""
def best(parent_set):
  J=[0 for i in range(7)]
  for i in range(0,7):
    intensity0 = [[0 for j in range(opt.num_grid_points)] for k in range(opt.num_grid_points)]
    for j in range(0,opt.num_grid_points):
      for k in range(0,opt.num_grid_points):
        intensity0[j][k]=Intensity(new_gen[i][0]*0.1+new_gen[i][1]*0.01,new_gen[i][2]*0.1+new_gen[i][3]*0.01,new_gen[i][4]*0.1+new_gen[i][5]*0.01,new_gen[i][6]*0.1+new_gen[i][7]*0.01,new_gen[i][8]*0.1+new_gen[i][9]*0.01,new_gen[i][10]*0.1+new_gen[i][11]*0.01,new_gen[i][12]*0.1+new_gen[i][13]*0.01,xw[j],yw[k])
    J[i] = stddev(intensity0)
  best_parent = np.argmin(J)
  return best_parent


"""Main Code:"""

new_gen=Generate_initial_gen();
current_iter=0
while (current_iter<opt.num_iter):
  parents=Parent_pool(new_gen);
  new_gen=Generate_new_gen(parents);
  current_iter=current_iter+1;
ans= best(parents)
print ("Bulb 1 at x = %f,y = %f,z = %f" % (parents[ans][0]*0.1+parents[ans][1]*0.01,parents[ans][2]*0.1+parents[ans][3]*0.01,parents[ans][12]*0.1+parents[ans][13]*0.01))
print ("Bulb 2 at x = %f,y = %f,z = %f" % (parents[ans][4]*0.1+parents[ans][5]*0.01,parents[ans][6]*0.1+parents[ans][7]*0.01,parents[ans][12]*0.1+parents[ans][13]*0.01))
print ("Bulb 3 at x = %f,y = %f,z = %f" % (parents[ans][8]*0.1+parents[ans][9]*0.01,parents[ans][10]*0.1+parents[ans][11]*0.01,parents[ans][12]*0.1+parents[ans][13]*0.01))

print("Successfully executed Genetic Algorithm")
