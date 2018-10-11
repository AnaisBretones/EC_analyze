#from  mpl_toolkits.basemap import Basemap
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


var = 'sal'			# sal, temp, Uorth Utang density
option = 'Coupled'		# Coupled, Uncoupled

y1 = 2000
y2 = 2100

basin ='SiberianOrth'		# GSR, SiberianOrth
lat_min = 50 #66.34 		#IF basin = 'undefined'
                                #ex: 66.34 for polar circle

comparison = 'no'
y1_compa = 1950
y2_compa = 2000



#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():									#//
        										#//
  #___________________									#//
  def __init__(self,option,var,y1,y2,compa,lat_min,basin):				#//
     self.max_depth = 1000	                                                        #//
     self.first_year = 1950
     self.y1 = y1 	                                                                #//
     self.y2 = y2
     if basin == 'undefined':								#//
        sufix = str(self.y1)+'to'+str(self.y2)+'_'+str(lat_min)+'_'+str(option)
     else: 
        sufix = str(self.y1)+'_30ymean_'+str(basin)+'_'+str(option)

     if compa == 'no':									#//
        self.output_file = str(var)+'_'+str(sufix)
     elif compa == 'yes':
        self.output_file = str(var)+'Sept_TimeSerieAnomaly_'+str(sufix)

     self.pathW = '/media/fig010/LACIE SHARE/EC_data/test/sectionW.nc'
     self.pathE = '/media/fig010/LACIE SHARE/EC_data/test/sectionE.nc'

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = -1                                                                   #//
        self.vmax = 2.6                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -1.08                                                               #//
        self.vmax = 0.15	                                                        #//

     elif compa =='no':
       if var == 'temp':                                                                #//
        if basin == 'SiberianOrth':
         if y1 >2050:
           self.vmin = -0.6
           self.vmax = 1.7
         else:
           self.vmin = -1.8
           self.vmax = -0.60

        else:
          self.vmin = -2                                                               #//
          if y1 > 2050:
             self.vmax = 16
          else:
             self.vmax = 14                                                               #//
       elif var == 'sal':                                                               #//
        if y1>2050:
          self.vmin = 31.95                                                               #//
          self.vmax = 36.2	
        else:
          self.vmin = 32.5
          self.vmax = 35.4                                                        #//
       elif var == 'density':                                                                #//
        self.vmin = 25.                                                               #//
        self.vmax = 28.                                                                 #//
       elif var == 'Uorth':                                                                #//
        self.vmin = -0.024                                                              #//
        self.vmax = 0.024                                                                 #//

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////


simu = From1950to2100(option,var,y1,y2,comparison,lat_min,basin) 
yrE, xrE, time, depth, XE = loading.extracting_coord_1D(simu.pathE)
yrW, xrW, time, depth, XW = loading.extracting_coord_1D(simu.pathW)

VARE = loading.extracting_var(simu.pathE, var)
VARW = loading.extracting_var(simu.pathW, var)

if var == 'sal':
  VARE[np.where( VARE < 32. )] = np.nan
  VARW[np.where( VARW < 32. )] = np.nan
elif var == 'density':
  VARE[np.where( VARE < 24)] =np.nan
  VARW[np.where( VARW < 24)] =np.nan
else:
  SE = loading.extracting_var(simu.pathE,'sal')
  VARE[ SE==0 ] = np.nan
  SW = loading.extracting_var(simu.pathW,'sal')
  VARW[ SW==0 ] = np.nan

xr = np.concatenate((xrW,xrE))
yr = np.concatenate((yrW,yrE))
make_plot.points_on_map(xr,yr,var,basin)

var_to_plot = np.hstack((VARW[:,:,0].transpose(),VARE[:,:,0].transpose()))
X_to_plot = np.concatenate((XW,XE+XW[-1]),axis=0)
print(np.shape(VARE),np.shape(VARW),np.shape(var_to_plot))
print(np.shape(XW))
print(np.shape(X_to_plot))
make_plot.one_sec(var_to_plot,var,X_to_plot,depth,simu.max_depth,y1,simu.output_file,simu.vmin,simu.vmax,basin)
