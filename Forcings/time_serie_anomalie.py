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


var = 'MeltedIce'			# sal, runoff, albedo, downHF
option = 'Coupled'		# Coupled, Uncoupled
y1 = 1950
y2 = 2100

basin ='around_greenland'		# arctic_ocean, BS_and_KS, undefined
lat_min = 66.34 		#IF basin = 'undefined'
                                #ex: 66.34 for polar circle

comparison = 'no'
y1_compa = 1950
y2_compa = 2000

if var == 'IceC':
   y1 = 1950


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
        sufix = str(self.y1)+'to'+str(self.y2)+'_'+str(basin)+'_'+str(option)

     if compa == 'no':									#//
        self.output_file = str(var)+'_TimeSerie_'+str(sufix)
     elif compa == 'yes':
        self.output_file = str(var)+'_TimeSerieAnomaly_'+str(sufix)

     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/Forcings_'+str(option)+'.nc' 

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = -1                                                                   #//
        self.vmax = 2.6                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -1.08                                                               #//
        self.vmax = 0.15	                                                        #//

     elif compa =='no':
       if var == 'temp':                                                                #//
        self.vmin = -1.23                                                               #//
        self.vmax = -0.04                                                               #//
       elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86	                                                        #//
       elif var == 'runoff':
        self.vmin = 0               	                                                #//
        self.vmax = 30	                	                                        #//
       elif var == 'downHF':
        self.vmin = 0                                                                   #//
        self.vmax = 30		                                                        #//
       elif var == 'albedo':
        self.vmin = 0                                                                   #//
        self.vmax = 10		                                                        #//
       elif var == 'MeltedIce':
        self.vmin = 0                                                                   #//
        self.vmax = 10		                                                        #//
     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////

def time_serie_Arctic(path,var,lat_min,basin):

  yr, xr, time, depth = loading.extracting_coord(path)
  TorS = loading.extracting_var(path, var)
  
  S = loading.extracting_var(path,'sal')
  TorS[np.where( S==0. )] = np.nan

  if basin =='undefined':
     mask = loading.latitudinal_band_mask(yr,lat_min,90)
  else:
     mask = loading.Ocean_mask(xr,yr,basin)
     make_plot.points_on_map(xr[mask],yr[mask],var,basin)

  arctic = TorS[mask,:,:]
  arctic[np.where(arctic==0)]=np.nan
  mean_Arctic = np.nanmean(arctic,axis=0)

  return time, depth, mean_Arctic


def time_serie_Arctic_2D(path,var,lat_min,basin):
  yr, xr, time = loading.extracting_coord_2D(path)
  ice = loading.extracting_var(path, var)
  print(np.max(ice),np.min(ice))
  S = loading.extracting_var(path,'sal')
  ice[np.where( S[:,:,0,:]==0. )] = np.nan

  if basin =='undefined':
     mask = loading.latitudinal_band_mask(yr,lat_min,90)
  else:
     mask = loading.Ocean_mask(xr,yr,basin)
     make_plot.points_on_map(xr[mask],yr[mask],var,basin)

  arctic = ice[mask,:]
  arctic[np.where(arctic==0)]=np.nan
  mean_Arctic = np.nansum(arctic,axis=0)
  return time, mean_Arctic

 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


simu = From1950to2100(option,var,y1,y2,comparison,lat_min,basin) 
if var == 'IceC' or var =='albedo' or var =='downHF' or var =='runoff' or var =='MetledIce':
  time, mean_Arctic_simu = time_serie_Arctic_2D(simu.path,var,lat_min,basin)
else:
  time, depth, mean_Arctic_simu = time_serie_Arctic(simu.path,var,lat_min,basin)

index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))

# JUST ONE TIME SERIE PLOT
if comparison == 'no':
   if var == 'IceC' or var =='albedo' or var =='downHF' or var =='runoff' or var =='MeltedIce':
     print(np.max(mean_Arctic_simu))
     print(np.shape(mean_Arctic_simu))
     print(mean_Arctic_simu)
     make_plot.var_fc_time(mean_Arctic_simu[index_y1:index_y2],var,time[index_y1:index_y2],simu.first_year, lat_min,simu.output_file,basin)
     
   else:
     make_plot.time_serie(mean_Arctic_simu[:,index_y1:index_y2],var,time[index_y1:index_y2],\
                       depth,simu.max_depth,simu.first_year,simu.output_file,simu.vmin,simu.vmax,basin)
else:
   index_y1c =np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>y1_compa))
   index_y2c =np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>y2_compa))
   np.shape(mean_Arctic_simu[:,index_y1c:index_y2c])
   ref = np.reshape( np.mean(mean_Arctic_simu[:,index_y1c:index_y2c],axis=1) ,[42,1])
   make_plot.time_serie(mean_Arctic_simu[:,index_y1:index_y2]- ref,var,\
                       time[index_y1:index_y2],depth,simu.max_depth,simu.first_year,\
                       simu.output_file,simu.vmin,simu.vmax,basin)

