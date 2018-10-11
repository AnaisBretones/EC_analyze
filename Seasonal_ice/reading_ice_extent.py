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
#import make_plot
import loading

# This script is made to read the sea ice extent in September and March (created thanks to the 'Seasonal_ice/time_serie_ice_extent.py')
# So far I wrote time series for the Sept and March sea ice for the Arctic Ocean from 1950 to 2300. Here you will plot both time series
# on top of each other. You can choose to reduce the time period by changing y1p and y2p ('plot') 
# OR you can 1- create new time series (with a different basin, different period) but then you should modify y1f,y2f and also 'basin'

# can be run with python3

var = 'IceC'			

y1f = 1950
y2f = 2300

y1p = 1950
y2p = 2300

basin ='arctic_ocean'		# arctic_ocean, (BS_and_KS, undefined.. not yet!)
lat_min = 66.34 		#IF basin = 'undefined'
                                #ex: 66.34 for polar circle
if basin == 'undefined':
  output_name = 'Ice_extent_March_September_'+str(y1p)+'-'+str(y2p)+'_'+str(lat_min)
else:
  output_name = 'Ice_extent_March_September_'+str(y1p)+'-'+str(y2p)+'_'+str(basin)

def var_fc_time_2(var,var2,variable_name,t,first_year_file,lat_min,name_outfile,month1,month2):

  index1 = 2018-t[0]
  seasonal_ice1_t = [t[index1], t[index1]]
  seasonal_ice1_thick = [var2[index1]-0.08*1E12, var[index1]+0.17*1E12]
  index2 = 2080-t[0]
  seasonal_ice2_t = [t[index2], t[index2]]
  seasonal_ice2_thick = [var2[index2]-0.12*1E12, var[index2]+0.15*1E12]

  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  #plt.xlim([first_year_file+np.min(t),first_year_file+np.max(t)])
  
  plt.plot(t,var,label=str(month1))
  plt.plot(t,var2,label=str(month2))
  plt.plot(seasonal_ice1_t,seasonal_ice1_thick,color='green',linewidth=5,label='seasonal variation')
  plt.plot(seasonal_ice2_t,seasonal_ice2_thick,color='green',linewidth=5)
  plt.ylabel('Sea ice extent (m$^{2}$)',fontsize=18)
  plt.xlabel('time',fontsize=18)
  ax.legend()
  plt.savefig(str(variable_name)+'/'+str(name_outfile)+'.png')
  return



Ice_Sept = loading.extract_sea_ice_ext(y1f,y2f,'Sept',basin)
Ice_March = loading.extract_sea_ice_ext(y1f,y2f,'March',basin)
#Ice_all,time_everyMonth = loading.extract_sea_ice_ext_ALL(y1f,y2f,'ALL',basin)

time = np.arange(y1f,y2f-1,1)

index_y1 = y1p-y1f
index_y2 = y2p-y1f

#index_y1p = np.min(np.where(time_everyMonth[:]>y1p))
#index_y2p = np.min(np.where(time_everyMonth[:]>y2p))

var_fc_time_2(Ice_Sept[index_y1:index_y2+1],Ice_March[index_y1:index_y2+1],var,time[index_y1:index_y2+1],0,lat_min,output_name,'September','March')
#make_plot.var_fc_time_3(var,Ice_Sept[index_y1:index_y2+1],Ice_March[index_y1:index_y2+1],time[index_y1:index_y2+1],\
#                       Ice_all[index_y1p:index_y2p+1],time_everyMonth[index_y1p:index_y2p+1],lat_min,output_name,'September','March','yearly variations')

