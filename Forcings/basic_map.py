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

var = 'runoff'		#sal, runoff, albedo, downHF
option = 'Uncoupled'
specificity = ''
y1 = 2050
y2 = 2100
control = 'Uncoupled'   # Uncoupled or historic

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
                           +str(self.y2)                                #//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/Forcings_'+str(option)+'.nc'

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
      elif var == 'runoff':
        self.vmin = -1E20
        self.vmax = 1E20

     elif compa =='no':
       if var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
       elif var == 'runoff':
        self.vmin = 1*1E8                                                                   #//
        self.vmax = 1E20                                                                  #//
       elif var == 'downHF':
        self.vmin = 0                                                                   #//
        self.vmax = 30                                                                  #//
       elif var == 'albedo':
        self.vmin = 0                                                                   #//
        self.vmax = 10 

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////



simu = From1950to2100(option,specificity,var,y1,y2,comparison)

if var == 'ML' or var == 'runoff':
  yr, xr, time = loading.extracting_coord_2D(simu.path)
else:
  yr, xr, time, depth = loading.extracting_coord(simu.path)


VarArray_simu = loading.extracting_var(simu.path, var)
index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))


if comparison == 'no':
   array_to_plot = np.mean(VarArray_simu[:,:,index_y1:index_y2+1],axis=2)
   print(np.nanmax(array_to_plot))
   array_to_plot[array_to_plot==0] = np.nan
   array_to_plot = np.ma.masked_invalid(array_to_plot)
   make_plot.plot_map(xr,yr,array_to_plot ,var,title_plot,simu.output_file,simu.vmin,simu.vmax)
elif comparison == 'yes':
   if control == 'Uncoupled':
     path2 = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/Forcings_Coupled.nc'
     Coupled_array = loading.extracting_var(path2, var)
     out = str(simu.output_file)+'CvsUC'
     array_to_plot = np.mean(Coupled_array[:,:,index_y1:index_y2+1],axis=2)-np.mean(VarArray_simu[:,:,index_y1:index_y2+1],axis=2)
   else: 
     out = str(simu.output_file)+'AnoTo90s_'+str(option)
     index_y1c = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1_compa))
     index_y2c = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2_compa))
     array_to_plot = np.mean(VarArray_simu[:,:,index_y1:index_y2+1],axis=2)-np.mean(VarArray_simu[:,:,index_y1c:index_y2c+1],axis=2)

   array_to_plot[array_to_plot==0] = np.nan
   array_to_plot = np.ma.masked_invalid(array_to_plot)
   make_plot.plot_map(xr,yr,array_to_plot,var,title_plot,out,simu.vmin,simu.vmax)


          
