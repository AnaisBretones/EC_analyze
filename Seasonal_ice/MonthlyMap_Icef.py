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

# WHAT SUBSET OF DATA ? \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

computer = 'home'
scenario = 'RCP8'	# 'CO2' 'RCP8'
ttype = 'monthly'	#'yearly', 'monthly'
option = 'Uncoupled'	# Coupled, Uncoupled
region = 'W'		# W or NH (here only W)

if scenario == 'CO2': 
  first_year = 1850
  last_year = 2000
  y1h = 1850 
  y2h = 1860
  y1f = 1870 
  y2f = 1880 
elif scenario == 'RCP8':
  first_year = 1950
  last_year = 2100
  y1h = 2010 
  y2h = 2020
  y1f = 2080 
  y2f = 2090 
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# CHARGING THE FILE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#var='Icef'
var='salt'

if computer=='home':
  pre_path = '/Volumes'
else:
  pre_path = '/media/fig010'

path = str(pre_path)+'/LACIE SHARE/EC_data/'+str(ttype) \
       +str(first_year)+'-'+str(last_year)+'/'         \
       +str(var)+'_'+str(ttype)+'Means_'+str(scenario)+str(option)+'_'+str(region)+'.nc'
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# OPTION OF ANALYSIS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

filtre = 'Positif'
#filtre = ''

max_depth = 1000
basin = 'arctic_ocean'
#basin = 'Siberian_seas'
#basin = 'greenland_sea'  # arctic_ocean, Siberian_seas
#basin = 'undefined'
lat_min=60

if var == 'Icef' and scenario == 'CO2':
  vmin = -2
  vmax = 2
elif var == 'salt' and scenario == 'CO2':
  vmin = -1E11
  vmax = 1E11
elif var == 'salt' and scenario == 'RCP8':
  vmin = -5E11
  vmax = 5E11
elif  var == 'Icef' and scenario == 'RCP8':
  vmin = -2
  vmax =2

#colorbar='RColorbar'
colorbar=''


if basin == 'undefined':
   output_file = str(var)+str(filtre)+str(ttype)+'_' \
                 +str(scenario)+str(option)+'_'+str(lat_min)+'N'
else:
   output_file = str(var)+str(filtre)+str(ttype)+'_' \
                 +str(scenario)+str(option)+'_'+str(basin)
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# STARTING ANALYSIS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
yr, xr, time = loading.extracting_coord_2D(path)

time = first_year+time[:]/(3600*24*364.5)
index_y1h = np.min(np.where(time>y1h))
index_y1f = np.min(np.where(time>y1f))
   
IceF1 = loading.extracting_var(path, var)
IceF1[np.where(IceF1>1E10)]=0
if filtre == 'Positif':
  IceF1[np.where(IceF1<0)] = 0
else:
  IceF1[np.where(IceF1<-1E10)] = 0

if var == 'Icef':
  IceF = 1E2*IceF1	# in cm
elif var == 'salt':
  path_grid = '/media/fig010/LACIE SHARE/EC_data/CERFACS_cell_area.nc'
  area = loading.reading_grid(path_grid)
  IceF = area*IceF1.transpose(2, 0,1)
  IceF = IceF.transpose(1,2,0)
  #IceF = IceF1*np.mean(area)
'''
hist = np.zeros((last_year-first_year))
for i in range(0,last_year-first_year):
   if ttype == 'monthly':
      hist[i] = np.nansum(IceF_int[i*12:i*12+12,:], axis=(0,1))*3600*24*30.5
      new_time = np.arange(first_year,last_year,1)
   else:
      hist = np.nansum(IceF_int, axis=1)*3600*24*364.5
      new_time = time

if var == 'Icef':
  hist = 1E-2*hist/np.nansum(area[mask])	# in cm
'''


#array_to_plotH = np.nansum(IceExt[:,:,index_y1h:index_y1h+10*12],axis=2)
array_to_plotH = np.zeros_like(IceF[:,:,0])
for i in range(0,np.size(IceF[:,0,0])):
   for j in range(0,np.size(IceF[0,:,0])):
      array_to_plotH[i,j] = np.nansum(IceF[i,j,index_y1h:index_y1h+10*12])/10


title= str(y1h)+'-'+str(y2h)
IceF[np.where(IceF==0)]=np.nan
array_to_plotH = np.ma.masked_invalid(array_to_plotH)
make_plot.plot_map(xr,yr,array_to_plotH,var,title,str(output_file)+'_present',vmin,vmax,colorbar)
array_to_plotH[array_to_plotH==np.nan] = 0


#array_to_plotF = np.nansum(IceExt[:,:,index_y1f:index_y1f+10*12],axis=2)
array_to_plotF = np.zeros_like(IceF[:,:,0])
for i in range(0,np.size(IceF[:,0,0])):
   for j in range(0,np.size(IceF[0,:,0])):
      array_to_plotF[i,j] = np.nansum(IceF[i,j,index_y1h:index_y1f+10*12])/10

array_to_plotC = array_to_plotF - array_to_plotH
array_to_plotC[array_to_plotC==0] = np.nan
#array_to_plotC[array_to_plotC<-16] = np.nan
array_to_plotC = np.ma.masked_invalid(array_to_plotC)

make_plot.plot_map_ano(xr,yr,array_to_plotC,var,y1f,'future-current','MapAno'+str(output_file),vmin,vmax,colorbar)

