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
option = 'Uncoupled'
specificity = ''
y1 = 2040#+140
y2 = 2060#+140

month = 'Sept'
comparison = 'yes'


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,specificity,var,y1,y2,compa,month):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1 = y1                                                                       #//
     self.y2 = y2                                                                       #//
     self.y1_compa = y1+1
     self.y2_compa = 2042
     if compa == 'no':                                                                  #//
        self.output_file = str(var)+str(month)+'_map_'+str(self.y1)+'to'\
                           +str(self.y2)+'_'+str(option)                                #//
     elif compa == 'yes':
        self.output_file = str(var)+str(month)+'_map_Ano'+str(self.y1)+'To'+str(self.y1_compa)+'_'+str(option)                                #//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/'+str(month)+'_Ice_'+str(option)+'.nc'

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
        self.vmax = 1.

     elif compa =='no':
      if var == 'IceC':
	self.vmin = 0
        self.vmax = 0.15
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


   
for i in range(0,20):
   y1 = y1+1   
   title_plot =  str(specificity)+' '+str(y1)+' to '+str(y1+1)
   simu = From1950to2100(option,specificity,var,y1,y2,comparison,month)
   
   if var == 'ML' or var == 'IceC':
     yr, xr, time = loading.extracting_coord_2D(simu.path)
   else:
     yr, xr, time, depth = loading.extracting_coord(simu.path)
   
   VarArray_simu = loading.extracting_var(simu.path, var)
   
   index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
   
   
   if comparison == 'no':
      if var == 'ML' or var == 'IceC':
        mask = (VarArray_simu[:,:,index_y1]>0.15)
        make_plot.plot_map(xr,yr,VarArray_simu[mask,index_y1] ,var,title_plot,simu.output_file,simu.vmin,simu.vmax)
      else:
        make_plot.plot_map(xr,yr,np.mean(VarArray_simu[:,:,0,index_y1:index_y2+1],axis=2) ,var,title_plot,simu.output_file,simu.vmin,simu.vmax)
   elif comparison == 'yes':
      index_y1c = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1_compa))
      if var == 'ML' or var == 'IceC':
        array_to_plot = VarArray_simu[:,:,index_y1c]-VarArray_simu[:,:,index_y1]
        array_to_plot[array_to_plot==0] = np.nan
        array_to_plot = np.ma.masked_invalid(array_to_plot)
        make_plot.plot_map_with_ice_extent(xr,yr,array_to_plot ,var,VarArray_simu[:,:,index_y1],y1,VarArray_simu[:,:,index_y1c],simu.y1_compa,title_plot,simu.output_file,simu.vmin,simu.vmax)
      else:
        make_plot.plot_map(xr,yr,np.mean(VarArray_simu[mask,0,index_y1:index_y2+1],axis=2)-np.mean(VarArray_simu[mask,0,index_y1c:index_y2c+1],axis=2) ,var,title_plot,simu.output_file,simu.vmin,simu.vma)


          
