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
import gsw
import loading

var='brine'
#var='saltf'

option = 'Coupled'
specificity = ''

#basin = 'arctic_ocean'
basin = 'Siberian_seas'
#basin = 'greenland_sea'  # arctic_ocean, Siberian_seas
#basin = 'undefined'
lat_min=60

month = 'March'
y1p = 1950          #first year in the data
y2p = 2300          #last year in the data

colorbar='RColorbar'
#colorbar=''

#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,var,y1,y2,colorbar,basin):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1h = 2010 #1950                                                                       #//
     self.y2h = 2020
     self.y1f = 2080 #2090
     self.y2f = 2090     
     self.path = '/media/fig010/LACIE SHARE/EC_data/monthly'+str(y1)+'-'+str(y2)+'/'\
                  'monthlysalt_'+str(y1)+'-'+str(y2)+'_from_icemod.nc'
     #self.path = '/media/fig010/LACIE SHARE/EC_data/monthly'+str(y1)+'-'+str(y2)+'/monthlysalt_'+str(y1)+'-'+str(y2)+'.nc'
     #self.path_S = '/media/fig010/LACIE SHARE/EC_data/March'+str(y1)+'-'+str(y2)+'/'\
     #             'icefSept_1950-2100.nc'



     if basin != 'undefined':
       self.output_fileC = str(var)+'_'+str(basin)+'_'+str(y1p)+'-'+str(y2p)                                #//
     else:
       self.output_fileC = str(var)+'Flux_'+str(y1p)+'-'+str(y2p)+'.nc'                              #//

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////

def size_bin(x0, x1, x2, y0, y1, y2):
  x = gsw.distance([x2, x0] , [y1, y1],[0,0])/2.
  y = gsw.distance([x1, x1] , [y2, y0],[0,0])/2.
  area = x*y
  return area

def size_each_bins(xr,yr):

  area = np.zeros_like((xr))
  for i in range(1,np.size(xr[:,0])-1):
    for j in range(1,np.size(xr[0,:])-1):
      area[i,j] = size_bin(xr[i-1,j], xr[i,j], xr[i+1,j], yr[i,j-1], yr[i,j], yr[i,j+1])
  return area


vmin=0
vmax=0

simu = From1950to2100(option,var,y1p,y2p,colorbar,basin)
   
yr, xr, time = loading.extracting_coord_2D(simu.path)
area = size_each_bins(xr,yr)
time = simu.first_year+time[:]/(3600*24*364.5)
   
IceFM = loading.extracting_var(simu.path, var)
IceFM[np.where(IceFM>1E10)]=0
IceFM[np.where(IceFM<0)] = 0
  
if basin =='undefined':
   mask = loading.latitudinal_band_mask(yr,lat_min,90)
else:
   mask = loading.Ocean_mask(xr,yr,basin)

a = IceFM[mask].transpose(1, 0)
brine = area[mask]*IceFM[mask,:].transpose(1, 0) 


index_y1h = np.min(np.where(time>simu.y1h))
index_y1f = np.min(np.where(time>simu.y1f))

IceFM[~mask] = np.nan
#IceFS[~mask] = np.nan
sub = IceFM
sub[np.where(sub==0)]=np.nan

hist = np.zeros((y2p-1950))
for i in range(0,y2p-1950):
   #hist[i] = np.nansum(sub[:,:,i*12:i*12+12])/12.
   hist[i] = np.nansum(brine[i*12:i*12+12,:]*3600*24*30.5)

time2=np.arange(1950,y2p,1)


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.figure(figsize=(10,6))
fig,ax=plt.subplots()
  
plt.plot(time2,hist)
#plt.ylabel('Annual brine production (kg.m$^{-2}$.s$^{-1}$)',fontsize=18)
plt.ylabel('Annual brine production (kg)',fontsize=18)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.xlabel('time',fontsize=18)
plt.savefig(str(var)+'/'+str(simu.output_fileC)+'.png')

