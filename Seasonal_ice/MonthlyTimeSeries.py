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

import gsw
import loading

# WHAT SUBSET OF DATA ? \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

scenario = 'CO2'	# 'CO2' 'RCP8'
ttype = 'yearly'	#'yearly', 'monthly'
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

var='Icef'
#var='salt'

path = '/media/fig010/LACIE SHARE/EC_data/'+str(ttype) \
       +str(first_year)+'-'+str(last_year)+'/'         \
       +str(var)+'_'+str(ttype)+'Means_'+str(scenario)+str(option)+'_'+str(region)+'.nc'
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# OPTION OF ANALYSIS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#filtre = 'Positif'
filtre = ''

max_depth = 1000
basin = 'arctic_ocean'
#basin = 'Siberian_seas'
#basin = 'greenland_sea'  # arctic_ocean, Siberian_seas
#basin = 'undefined'
lat_min=60

vmin=0
vmax=0

colorbar='RColorbar'
#colorbar=''


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
path_grid = '/media/fig010/LACIE SHARE/EC_data/CERFACS_cell_area.nc'
area = loading.reading_grid(path_grid)
time = first_year+time[:]/(3600*24*364.5)
index_y1h = np.min(np.where(time>y1h))
index_y1f = np.min(np.where(time>y1f))
   
IceF = loading.extracting_var(path, var)
IceF[np.where(IceF>1E10)]=0
if filtre == 'Positif':
  IceF[np.where(IceF<0)] = 0
else:
  IceF[np.where(IceF<-1E10)] = 0


if basin =='undefined':
   mask = loading.latitudinal_band_mask(yr,lat_min,90)
else:
   mask = loading.Ocean_mask(xr,yr,basin)

a = IceF[mask].transpose(1, 0)
IceF_int = area[mask]*IceF[mask,:].transpose(1, 0) 


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


IceF[~mask] = np.nan
sub = IceF
sub[np.where(sub==0)]=np.nan


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.figure(figsize=(10,6))
fig,ax=plt.subplots()
  
plt.plot(new_time,hist)

if var == 'salt':
  plt.ylabel('Annual brine production (kg)',fontsize=18)
  plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
elif var == 'Icef':
  plt.ylabel('yearly ice formation over '+str(basin.replace("_"," "))+' (cm)',fontsize=18)
plt.xlabel('time',fontsize=18)
plt.savefig(str(var)+'/TimeSeries'+str(output_file)+'.png')

