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

_var_ = 'velocity'
_option_ = 'Coupled'
_specificity_ = ''
_y1_ = 2190

_comparison_ = 'no'


#//////////////////////////////////////////////////////////////////////////////////////////
class _From1950to2100_():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,specificity,var,y1,y2,compa):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 2200#2100
     self.y1 = y1                                                                       #//
     self.y2 = y2                                                                       #//
     self.y1_compa = 1950
     self.y2_compa = 2000
     self.output_file = 'map_'+str(self.y1)+'to'+str(self.y2)+'_'+str(option)+'_mod'   #//
     #self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/2300/vita.nc'#_'+str(option)+'.nc'
     #self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/2300/2200_2300/vita.nc'#_'+str(option)+'.nc'
     self.path = '/Volumes/LACIE SHARE/EC_Earth/EC_data/2300/2200_2300/vita.nc'
     #self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/2300/2090/vita.nc'#_'+str(option)+'.nc'



while _y1_<2291:
  _y1_=_y1_+10
  _y2_ = _y1_+10

  simu = _From1950to2100_(_option_,_specificity_,_var_,_y1_,_y2_,_comparison_)
  
  yr, xr, time, depth = loading.extracting_coord(simu.path)
  
  U = loading.extracting_var(simu.path, 'sovitua')
  V = loading.extracting_var(simu.path, 'sovitva')
  index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
  index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))
  
  mask = (xr>85) | (xr<-105)
  U[mask,:]=-U[mask,:]
  V[mask,:]=-V[mask,:]
  
  title=str(_y1_)+'-'+str(_y2_)
  print(title)
  make_plot.map_velocity(xr,yr,np.mean(U[:,:,index_y1:index_y2+1],axis=2),np.mean(V[:,:,index_y1:index_y2+1],axis=2),_var_,title,_option_,simu.output_file)

