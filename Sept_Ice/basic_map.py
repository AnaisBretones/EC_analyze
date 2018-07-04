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

var = 'IceC'
option = 'Coupled'
specificity = ''
y1 = 2090
y2 = 2100

comparison = 'yes'

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
     if compa == 'no':                                                                  #//
        self.output_file = str(var)+str(specificity)+'_map_'+str(self.y1)+'to'\
                           +str(self.y2)+'_'+str(option)                                #//
     elif compa == 'yes':
        self.output_file = str(var)+'_map_'+str(self.y1)+'to'\
                           +str(self.y2)+'AnoTo90s_'+str(option)                                #//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/Sept_Ice_'+str(option)+'.nc'

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = 1                                                                   #//
        self.vmax = 7                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -2                                                               #//
        self.vmax = 2                                                                #//
      elif var == 'ML':
        self.vmin = -20
        self.vmax = 20
      elif var == 'IceC':
        self.vmin = -1
        self.vmax = 0.

     elif compa =='no':
      if var == 'IceC':
	self.vmin = 0
        self.vmax = 1
      elif var == 'ML':
        self.vmin = 12
        self.vmax = 70
      elif var == 'temp':                                                                #//
        self.vmin = -1.2                                                               #//
        self.vmax = 15                                                               #//
      elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////


#//////////////////////////////////////////////////////////////////////////////////////////
class yearly1950to2100():                                                               #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var,y1,y2,compa):                                                      #//
      self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/classic_YearlyMeans_'+str(option)+'.nc' 
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



#months = ['jan','feb','mars','apr','mai','june','july','aug','sept','oct','nov','dec']
#i_month = months.index(month)

simu = From1950to2100(option,specificity,var,y1,y2,comparison)

if var == 'ML' or var == 'IceC':
  yr, xr, time = loading.extracting_coord_2D(simu.path)
else:
  yr, xr, time, depth = loading.extracting_coord(simu.path)

print(np.shape(time),np.shape(xr))
VarArray_simu = loading.extracting_var(simu.path, var)

index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))


if comparison == 'no':
   if var == 'ML' or var == 'IceC':
     make_plot.plot_map(xr,yr,np.mean(VarArray_simu[:,:,index_y1:index_y2+1],axis=2) ,var,title_plot,simu.output_file,simu.vmin,simu.vmax)
   else:
     make_plot.plot_map(xr,yr,np.mean(VarArray_simu[:,:,0,index_y1:index_y2+1],axis=2) ,var,title_plot,simu.output_file,simu.vmin,simu.vmax)
elif comparison == 'yes':
   index_y1c = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1_compa))
   index_y2c = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2_compa))
   if var == 'ML' or var == 'IceC':
     make_plot.plot_map(xr,yr,np.mean(VarArray_simu[:,:,index_y1:index_y2+1],axis=2)-np.mean(VarArray_simu[:,:,index_y1c:index_y2c+1],axis=2) ,var,title_plot,simu.output_file,simu.vmin,simu.vmax)
   else:
     make_plot.plot_map(xr,yr,np.mean(VarArray_simu[mask,0,index_y1:index_y2+1],axis=2)-np.mean(VarArray_simu[mask,0,index_y1c:index_y2c+1],axis=2) ,var,title_plot,simu.output_file,simu.vmin,simu.vma)


          
