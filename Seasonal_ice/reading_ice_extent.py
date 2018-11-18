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
scenario='CO2'
run='Coupled'

y1f = 1950
y2f = 2300

y1p = 1950
y2p = 2300

if scenario=='CO2':
  y1p=1850
  y1f=1850
  y2f=2000
  y2p=2000
  suf='_'+str(scenario)+str(run)
else:
  suf=''

basin ='arctic_ocean'		# arctic_ocean, (BS_and_KS, undefined.. not yet!)
#basin='undefined'
lat_min = 66.34 		#IF basin = 'undefined'
#deg='1deg'                        #ex: 66.34 for polar circle
#deg='diff'
deg = 'grid'
#deg='gsw'

if basin == 'undefined':
  output_name = 'Ice_extent_March_September_'+str(y1p)+'-'+str(y2p)+'_'+str(lat_min)+'_'+str(deg)+str(suf)
else:
  output_name = 'Ice_extent_March_September_'+str(y1p)+'-'+str(y2p)+'_'+str(basin)+'_'+str(deg)+str(suf)

def var_fc_time_2(var,var2,variable_name,t,first_year_file,lat_min,name_outfile,month1,month2,basin):
  '''
  index1 = 2018-t[0]
  seasonal_ice1_t = np.linspace(t[index1],t[index1+10],20)
  seasonal_ice1_thick = np.zeros_like(seasonal_ice1_t)
  for i in range(0,10):
    seasonal_ice1_thick[2*i] = var2[index1+i]
    seasonal_ice1_thick[2*i+1] = var[index1+i] 

  index2 = 2080-t[0]
  seasonal_ice2_t = np.linspace(t[index2],t[index2+10],20)
  seasonal_ice2_thick = np.zeros_like(seasonal_ice2_t)
  for i in range(0,10):
    seasonal_ice2_thick[2*i] = var2[index2+i]
    seasonal_ice2_thick[2*i+1] = var[index2+i] 
  '''

  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  
  plt.plot(t,var[0:-1],label=str(month1))
  plt.plot(t,var2[0:-1],label=str(month2))
  if basin=='undefined':
    plt.ylabel('Sea ice extent (km$^{2}$)',fontsize=18)
  else:
    plt.ylabel('Sea ice extent (m$^{2}$)',fontsize=18)
  plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
  plt.xlabel('time',fontsize=18)
  ax.legend()
  plt.savefig(str(variable_name)+'/'+str(name_outfile)+'.png')
  return


if scenario =='CO2':
  Ice_Sept = loading.extract_sea_ice_ext(y1f,y2f,'Sept',basin,'_'+str(run),deg)
  Ice_March = loading.extract_sea_ice_ext(y1f,y2f,'March',basin,'_'+str(run),deg)
else:
  Ice_Sept = loading.extract_sea_ice_ext(y1f,y2f,'Sept',basin,'',deg)
  Ice_March = loading.extract_sea_ice_ext(y1f,y2f,'March',basin,'',deg)

time = np.arange(y1f,y2f-1,1)

index_y1 = y1p-y1f
index_y2 = y2p-y1f


var_fc_time_2(Ice_Sept[index_y1:index_y2+1],Ice_March[index_y1:index_y2+1],var,time[index_y1:index_y2+1],0,lat_min,output_name,'September','March',basin)

