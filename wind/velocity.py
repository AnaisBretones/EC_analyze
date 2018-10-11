from  mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as py
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec
import scipy
import netCDF4

from pylab import *
from netCDF4 import Dataset

from scipy.interpolate import Rbf
import os
import sys
import numpy as np

import make_plot
import loading

# This script compute (and map) 10 year mean velocity field 

var = 'svelocity'           #ice_velocity or wind_stress or svelocity
option = 'Coupled'
specificity = ''

first_year = 2100
y1=np.copy(first_year)

if y1>=1950 and y1<=2090:
  period='2000_2100'
elif y1>=2100 and y1<=2190:
  period='2100_2200'
elif y1>=2200 and y1<=2290:
  period='2200_2300'

_comparison_ = 'no'


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,nb,specificity,var,y1,y2,period):                                            #//
     self.max_depth = 1000                                                              #//
     self.y1 = y1                                                                       #//
     self.y2 = y2                                                                       #//
     #self.output_file = 'map_'+str(var)+'_'+str(self.y1)+'to'+str(self.y2)+'-'+str(nb)   #//
     self.output_file = 'map_'+str(var)+'-'+str(nb)   #//

     if var == 'svelocity':
        self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/100velocity/'+str(period)+'/vita.nc'
     elif var == 'ice_velocity' or var == 'wind_stress':
        self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/100velocity/'+str(period)+'/tau_Coupled.nc'


nb=10
while y1 <= first_year+100-10:
  y2 = y1+10

  simu = From1950to2100(nb,specificity,var,y1,y2,period)
  
  yr, xr, time = loading.extracting_coord_2D(simu.path)
  
  if var=='ice_velocity':
    U = loading.extracting_var(simu.path, 'iicevelu')
    V = loading.extracting_var(simu.path, 'iicevelv')
  elif var=='wind_stress':
    U = loading.extracting_var(simu.path, 'iocestru')
    V = loading.extracting_var(simu.path, 'iocestrv')
  elif var=='svelocity':
    U = loading.extracting_var(simu.path, 'sovitua')
    V = loading.extracting_var(simu.path, 'sovitva')

  index_y1 = np.min(np.where(first_year+time[:]/(3600*24*364.5)>simu.y1))
  index_y2 = np.min(np.where(first_year+time[:]/(3600*24*364.5)>simu.y2))
  
  mask = (xr>85) | (xr<-105)
  U[mask,:]=-U[mask,:]
  V[mask,:]=-V[mask,:]
  
  title=str(y1)+'-'+str(y2)
  print(title)
  make_plot.map_velocity(xr,yr,np.mean(U[:,:,index_y1:index_y2+1],axis=2),np.mean(V[:,:,index_y1:index_y2+1],axis=2),var,title,option,simu.output_file)
  y1=y1+10

  nb=nb+1

