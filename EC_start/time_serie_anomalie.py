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


var = 'IceC'
option = 'Coupled'
y1 = 1950
y2 = 2100
lat_min = 50#66.34 #66.34 polar circle

comparison = 'no'
y1_compa = 1950
y2_compa = 2000


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():									#//
        										#//
  #___________________									#//
  def __init__(self,option,var,y1,y2,compa,lat_min):					#//
     self.max_depth = 1000	                                                        #//
     self.first_year = 1950
     self.y1 = y1 	                                                                #//
     self.y2 = y2									#//
     if compa == 'no':									#//
        self.output_file = str(var)+'_TimeSerie_'+str(self.y1)+'to'\
                           +str(self.y2)+'_'+str(lat_min)+'_'+str(option)		#//
     elif compa == 'yes':
        self.output_file = str(var)+'_TimeSerieAnomaly_'+str(self.y1)+'to'\
                           +str(self.y2)+'_'+str(option)				#//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/EC_start_'+str(option)+'.nc' 

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = 0                                                                   #//
        self.vmax = 3.8                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -1.08                                                               #//
        self.vmax = 0.15	                                                        #//

     elif compa =='no':
      if y2<2010:
       if var == 'temp':                                                                #//
        self.vmin = -1.23                                                               #//
        self.vmax = -0.04                                                               #//
       elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86	                                                        #//
      elif y1>1999:
       if var == 'temp':                                                                #//
        self.vmin = -0.9                                                                #//
        self.vmax = 2.8                                                                 #//
       elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86	                                                        #//
      else:
       if var == 'temp':                                                                #//
        self.vmin = -1.2                                                                #//
        self.vmax = 2.5                                                                 #//
       elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86	                                                        #//

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////

def time_serie_Arctic(path,var,lat_min):

  yr, xr, time, depth = loading.extracting_coord(path)
  TorS = loading.extracting_var(path, var)
  Arctic_values = loading.regional_subset(TorS,yr,lat_min,90)
  Arctic_values[np.where(Arctic_values ==0.)] = np.nan
  nt = np.size(TorS[0,0,0,:])
  nz = np.size(TorS[0,0,:,0])
  mean_Arctic = np.zeros((nz,nt))

  for t in range(0,nt):
       for z in range(0,nz):
         mean_Arctic[z,t] = Arctic_values[z,t,~np.isnan(Arctic_values[z,t,:])].mean()

  return time, depth, mean_Arctic

def time_serie_Arctic_2D(path,var,lat_min):
  yr, xr, time = loading.extracting_coord_2D(path)
  TorS = loading.extracting_var(path, var)
  Arctic_values = loading.regional_subset_2D(TorS,yr,lat_min,90)

  Arctic_values[np.where(Arctic_values ==0.)] = np.nan

  nt = np.size(TorS[0,0,:])
  mean_Arctic = np.zeros((nt))

  for t in range(0,nt):
     mean_Arctic[t] = Arctic_values[t,~np.isnan(Arctic_values[t,:])].mean()

  return time, mean_Arctic

 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


simu = From1950to2100(option,var,y1,y2,comparison,lat_min) 
if var == 'IceC':
  time, mean_Arctic_simu = time_serie_Arctic_2D(simu.path,var,lat_min)
else:
  time, depth, mean_Arctic_simu = time_serie_Arctic(simu.path,var,lat_min)
index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))

# JUST ONE TIME SERIE PLOT
if comparison == 'no':
   if var == 'IceC':
     print('ok')
     make_plot.var_fc_time(mean_Arctic_simu[index_y1:index_y2],var,time[index_y1:index_y2],simu.first_year, lat_min,simu.output_file)
   else:
     make_plot.time_serie(mean_Arctic_simu[:,index_y1:index_y2],var,time[index_y1:index_y2],\
                       depth,simu.max_depth,simu.first_year,simu.output_file,simu.vmin,simu.vmax)
else:
   index_y1c =np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>y1_compa))
   index_y2c =np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>y2_compa))
   np.shape(mean_Arctic_simu[:,index_y1c:index_y2c])
   ref = np.reshape( np.mean(mean_Arctic_simu[:,index_y1c:index_y2c],axis=1) ,[42,1])
   make_plot.time_serie(mean_Arctic_simu[:,index_y1:index_y2]\
                       - ref,var,\
                       time[index_y1:index_y2],depth,simu.max_depth,simu.first_year,\
                       simu.output_file,simu.vmin,simu.vmax)

'''
one_time, depth2, mean_Arctic_ref = time_serie_Arctic(simu.path_ref,var)

nt = np.size(mean_Arctic_simu[0,:])
nz = np.size(mean_Arctic_simu[:,0])

anomaly = np.zeros((nz,nt)) 

for z in range(0,nz):
   anomaly[z,:] = mean_Arctic_simu[z,:] - mean_Arctic_ref[z,0]

make_plot.time_serie(anomaly,var,time,depth,simu.max_depth,simu.first_year,simu.output_file,simu.vmin,simu.vmax)

#make_plot.plot_map(xr,yr,np.mean(T1[:,:,0,-11:-1],axis=2)-T2[:,:,0,0] ,var,'2090-2100','surface',option,'')
#make_plot.vertical_profile(np.mean(T_mean_Arctic1,axis=1),'temp',month,depth,max_depth,year[k1],'')
#make_plot.vertical_profile(np.mean(T_mean_Arctic2,axis=1),'temp',month,depth,max_depth,year[k2],'')'''
