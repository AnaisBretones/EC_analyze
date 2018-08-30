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

var = 'velocity'
option = 'Coupled'
specificity = ''
y1 = 2070
y2 = 2100

comparison = 'no'

title_plot =  str(specificity)+' '+str(y1)+' to '+str(y2)

#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,specificity,var,y1,y2,compa):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1 = y1                                                                       #//
     self.y2 = y2                                                                       #//
     self.y1_compa = 1950
     self.y2_compa = 2000
     self.output_file = 'map_'+str(self.y1)+'to'+str(self.y2)+'_'+str(option)+'_mod'   #//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/section/vita_'+str(option)+'.nc'




#months = ['jan','feb','mars','apr','mai','june','july','aug','sept','oct','nov','dec']
#i_month = months.index(month)

simu = From1950to2100(option,specificity,var,y1,y2,comparison)

yr, xr, time, depth = loading.extracting_coord(simu.path)

U = loading.extracting_var(simu.path, 'sovitua')
V = loading.extracting_var(simu.path, 'sovitva')
index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))

mask = (xr>85) | (xr<-105)
#mask = (xr>90) | (xr<-90)
print( mask)
U[mask,:]=-U[mask,:]
V[mask,:]=-V[mask,:]

title=''
make_plot.map_velocity(xr,yr,np.mean(U[:,:,index_y1:index_y2+1],axis=2),np.mean(V[:,:,index_y1:index_y2+1],axis=2),var,title,option,simu.output_file)
