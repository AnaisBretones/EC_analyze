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

#//////////////////////////////////////////////////////////////////////////////////////////
class hisfrom1950():                                                                    #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var):                                                      #//
      self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/classic_YearlyMeans.nc'   #//
      self.max_depth = 1000                                                             #//
      self.first_year = 1950                                                            #//
      if var == 'temp':                                                                 #//
        self.vmin = -5                                                                  #//
        self.vmax = 10                                                                  #//
      elif var == 'sal':                                                                #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
      elif var == 'ML':
        self.vmin = -100
        self.vamx = 0
      self.output_file = str(var)+'_'+str(option)+'_surface_10ymean'		        #//
                                                                                        #//
      return                                                                            #//
                                                                                        #//
#//////////////////////////////////////////////////////////////////////////////////////////

#//////////////////////////////////////////////////////////////////////////////////////////
class anomaly_to_1950():                                                                #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,var):                                                        #//
     self.path_ref = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/classic_YearlyMeans.nc' #//
     self.max_depth = 1000                                                              #//
     if option == 'Coupled':                                                            #//
       self.first_year = 2007                                                           #//
     elif option == 'Uncoupled':                                                        #//
       self.first_year = 2006                                                           #//
                                                                                        #//
     self.output_file = str(var)+'Anomaly_'+str(option)+'_surface_10ymean'	        #//
     self.path = 'futurefrom'+str(self.first_year)+'_'+str(option)+'.nc'                #//
     if var == 'temp':                                                                  #//
        self.vmin = 0                                                                   #//
        self.vmax = 9                                                                   #//
     elif var == 'sal':                                                                 #//
        self.vmin = -4                                                                  #//
        self.vmax = 4                                                                   #//
     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////

#//////////////////////////////////////////////////////////////////////////////////////////
class yearly1950to2100():                                                               #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var):                                                      #//
      self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/classic_YearlyMeans'+str(option)+'.nc' #/
      self.max_depth = 1000                                                             #//
      self.first_year = 1950                                                            #//
      self.last_year = 2100
      if var == 'temp':                                                                 #//
        self.vmin = -5                                                                  #//
        self.vmax = 10                                                                  #//
      elif var == 'sal':                                                                #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
      elif var == 'ML':
        self.vmin = 0
        self.vmax = 300
      self.output_file = str(var)+'_ymeans_'+str(option)                                #//
                                                                                        #//
      return                                                                            #//
                                                                                        #//
#//////////////////////////////////////////////////////////////////////////////////////////


var = 'temp'
option = 'Coupled'
year = 2100
comparison = 'no'

#months = ['jan','feb','mars','apr','mai','june','july','aug','sept','oct','nov','dec']
#i_month = months.index(month)

if comparison == 'no':
   simu = yearly1950to2100(option,var)
elif comparison == 'yes':
   simu = Anomaly_to1950(option,var)
   VarArray_ref = loading.extracting_var(simu.path_ref, var)

if var == 'ML' or var == 'IceC':
  yr, xr, time = loading.extracting_coord2(simu.path)
else:
  yr, xr, time, depth = loading.extracting_coord(simu.path)

print(np.shape(time),np.shape(xr))
VarArray_simu = loading.extracting_var(simu.path, var)


if comparison == 'no':
   index_y = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>year))
   make_plot.plot_map(xr,yr,VarArray_simu[:,:,index_y] ,var,year,'mean',simu.output_file,simu.vmin,simu.vmax)
elif comparison == 'yes':
   make_plot.plot_map(xr,yr,np.mean(VarArray_sim[:,:,0,-11:-1],axis=2)-VarArray_ref[:,:,0,0] ,var,'2090-2100','surface',simu.output_file,simu.vmin,simu.vmax)




