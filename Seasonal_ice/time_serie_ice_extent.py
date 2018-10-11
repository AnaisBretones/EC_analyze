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
import gsw
#import make_plot
import loading


var = 'IceC'			# sal, temp, IceC, ML
option = 'Coupled'		# Coupled, Uncoupled
period = '1950-2300'

y1 = 1950
y2 = 2300
month = 'ALL'                  #Sept or March or ALL
basin ='arctic_ocean'		# arctic_ocean, BS_and_KS, undefined
lat_min = 66.34 		#IF basin = 'undefined'
                                #ex: 66.34 for polar circle



#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():									#//
        										#//
  #___________________									#//
  def __init__(self,option,var,y1,y2,lat_min,basin,month):				#//
     self.max_depth = 1000	                                                        #//
     self.first_year = 1950
     self.y1 = y1 	                                                                #//
     self.y2 = y2
  
     if month == 'ALL':
        self.path = '/media/fig010/LACIE SHARE/EC_data/monthly'+str(period)+'/IceC_MonthlyMeans.nc'
     else:
        self.path = '/media/fig010/LACIE SHARE/EC_data/'+str(month)+str(period)+'/'+str(month)+'_Ice_'\
                  +str(option)+'.nc' 



     self.vmin = 0.                                                               #//
     self.vmax = 1E6                                                                #//

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////


def time_serie_sea_ice_ext(path,var,lat_min,basin,path_salinity):
  yr, xr, time = loading.extracting_coord_2D(path)
  ice = loading.extracting_var(path, var)
  #S = loading.extracting_var(path_salinity,'sal')

  if basin =='undefined':
     mask = loading.latitudinal_band_mask(yr,lat_min,90)
  else:
     mask = loading.Ocean_mask(xr,yr,basin)
  area = size_each_bins(xr,yr)
  ice[np.where(ice<0.15)]=0.
  ice[np.where(ice>0.15)]=1.

  ice_extent = area[mask]*ice[mask].transpose(1, 0) 
  mean_ice_ext = np.nansum(ice_extent,axis=1)
  return time, mean_ice_ext

  

 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
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
 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

path_salinity = '/media/fig010/LACIE SHARE/EC_data/Sept'+str(period)+'/Sept_Ice_Coupled.nc' 

simu = From1950to2100(option,var,y1,y2,lat_min,basin,month) 
time, ice_extent = time_serie_sea_ice_ext(simu.path,var,lat_min,basin,path_salinity)

time = simu.first_year+time/(3600*24*364.5)
print(time)
index_y1 = np.min(np.where(time[:]>simu.y1))
index_y2 = np.min(np.where(time[:]>simu.y2))
print(np.shape(time),index_y1,index_y2)


if month != 'ALL':
  file = open('/media/fig010/LACIE SHARE/EC_data/'+str(month)+str(period)+'/sea_ice_extent_'+str(basin)+'.txt','w')
  for i in range(0,index_y2-index_y1+1):
      file.write(str(ice_extent[index_y1+i])+'\n')
  file.close()
else:
  file = open('/media/fig010/LACIE SHARE/EC_data/monthly'+str(period)+'/sea_ice_extent_'+str(basin)+'.txt','w')
  file2 =  open('/media/fig010/LACIE SHARE/EC_data/monthly'+str(period)+'/time_'+str(basin)+'.txt','w')
  for i in range(0,index_y2-index_y1+1):
      file.write(str(ice_extent[index_y1+i])+'\n')
      file2.write(str(time[index_y1+i])+'\n')
  file.close()
  file2.close()



