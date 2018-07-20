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


var = 'temp'			# sal, temp, Uorth Utang density
option = 'Coupled'		# Coupled, Uncoupled

y1 = 2100
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
        sufix = str(self.y1)+'_'+str(basin)+'_'+str(option)

     if compa == 'no':									#//
        self.output_file = str(var)+'_'+str(sufix)
     elif compa == 'yes':
        self.output_file = str(var)+'Sept_TimeSerieAnomaly_'+str(sufix)

     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/test/section.nc'#section/section_' \
                 # +str(basin)+'_'+str(option)+'.nc'  

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = -1                                                                   #//
        self.vmax = 2.6                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -1.08                                                               #//
        self.vmax = 0.15	                                                        #//

     elif compa =='no':
       if var == 'temp':                                                                #//
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

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////


simu = From1950to2100(option,var,y1,y2,comparison,lat_min,basin) 
yr, xr, time, depth, X = loading.extracting_coord_1D(simu.path)

VAR = loading.extracting_var(simu.path, var)

if var == 'sal':
  VAR[np.where( VAR < 32. )] = np.nan
elif var == 'density':
  VAR[np.where( VAR < 24)] =np.nan
else:
  S = loading.extracting_var(simu.path,'sal')
  VAR[ S==0 ] = np.nan
print(np.nanmin(VAR))

make_plot.points_on_map(xr,yr,var,basin)


index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))
print(np.shape(VAR), np.shape(depth), np.shape(X))
make_plot.one_sec(VAR[:,:,index_y1].transpose(),var,X,depth,simu.max_depth,y1,simu.output_file,simu.vmin,simu.vmax,basin)
