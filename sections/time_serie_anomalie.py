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


var = 'temp'			# sal, temp, IceC, ML
option = 'Coupled'		# Coupled, Uncoupled
y1 = 1950
y2 = 2100

basin ='SiberianOrth'           # GSR, SiberianOrth

comparison = 'no'
y1_compa = 1950
y2_compa = 2000

if var == 'IceC':
   y1 = 1950

#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():									#//
        										#//
  #___________________									#//
  def __init__(self,option,var,y1,y2,compa,basin):				#//
     self.max_depth = 1000	                                                        #//
     self.first_year = 1950
     self.y1 = y1 	                                                                #//
     self.y2 = y2
     self.zmax = 800

     self.output_file = 'mean'+str(var)+'_'+str(basin)+'_TimeSerie_'+str(option)
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/section/section_'+str(basin)+'_'+str(option)+'.nc' #section_FS_'+str(option)+'.nc' 

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = -1                                                                   #//
        self.vmax = 2.6                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -1.08                                                               #//
        self.vmax = 0.15	                                                        #//

     elif compa =='no':
       if var == 'temp':                                                                #//
        self.vmin = 4                                                               #//
        self.vmax = 14                                                               #//
       elif var == 'sal':                                                               #//
        self.vmin = 30.15                                                               #//
        self.vmax = 34.86	                                                        #//
       elif var == 'IceC':                                                                #//
        self.vmin = 0.                                                               #//
        self.vmax = 0.95                                                                 #//

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////

def time_serie_Arctic(path,var):

  yr, xr, time, depth = loading.extracting_coord(path)
  TorS = loading.extracting_var(path, var)
  make_plot.points_on_map(xr,yr,var,basin)

  S = loading.extracting_var(path,'sal')
  TorS[np.where( S==0. )] = np.nan
  i_zmax = np.max(np.where(depth<simu.zmax))
  print(np.shape(TorS))


  mean_Arctic = np.mean(np.nanmean(TorS[:,0:i_zmax,:],axis=0),axis=0)

  return time, depth, mean_Arctic


def time_serie_Arctic_2D(path,var,lat_min,basin):
  yr, xr, time = loading.extracting_coord_2D(path)
  ice = loading.extracting_var(path, var)
  S = loading.extracting_var(path,'sal')
  ice[np.where( S[:,:,0,:]==0. )] = np.nan

  if basin =='undefined':
     mask = loading.latitudinal_band_mask(yr,lat_min,90)
  else:
     mask = loading.Ocean_mask(xr,yr,basin)
     #make_plot.points_on_map(xr[mask],yr[mask],var,basin)

  arctic = ice[mask,:]
  mean_Arctic = np.nanmean(arctic,axis=0)
  return time, mean_Arctic



 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


simu = From1950to2100(option,var,y1,y2,comparison,basin) 
time, depth, mean_Arctic_simu = time_serie_Arctic(simu.path,var)

sea_ice_extent = loading.extract_sea_ice_ext(y1,y2,option)

index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))

print(mean_Arctic_simu[index_y1:index_y2])
# JUST ONE TIME SERIE PLOT
#make_plot.var_fc_time(mean_Arctic_simu[index_y1:index_y2],var,time[index_y1:index_y2],simu.first_year, 0,simu.output_file,basin,simu.zmax)

make_plot.var_fc_time_two_axis(mean_Arctic_simu[index_y1:index_y2],var,time[index_y1:index_y2],simu.first_year,sea_ice_extent,\
                       depth,simu.zmax,simu.first_year,simu.output_file,simu.vmin,simu.vmax,basin,simu.output_file)

