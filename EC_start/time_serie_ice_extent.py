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
option = 'Uncoupled'		# Coupled, Uncoupled
y1 = 1950
y2 = 2100
basin ='undefined'		# arctic_ocean, BS_and_KS, undefined
lat_min = 66.34 		#IF basin = 'undefined'
                                #ex: 66.34 for polar circle

comparison = 'no'
y1_compa = 1950
y2_compa = 2000

#if var == 'IceC':
#{   y1 = 1950


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
        self.output_file = str(var)+'extent__TimeSerie_'+str(sufix)
     elif compa == 'yes':
        self.output_file = str(var)+'extent__TimeSerieAnomaly_'+str(sufix)

     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/EC_start_'\
                  +str(option)+'.nc' 

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
       elif var == 'IceC':                                                                #//
        self.vmin = 0.                                                               #//
        self.vmax = 1E6                                                                #//

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////
def var_fc_time(var,variable_name,t,first_year_file,lat_min,name_outfile,ocean):
  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  t = t/(3600*24*365.)
  plt.xlim([first_year_file+np.min(t),first_year_file+np.max(t)])
  #plt.ylim([0.,0.75])
  if variable_name == 'IceC':
     plt.plot(first_year_file+t,var)
     plt.ylabel('Sea ice extent (m$^{2}$)',fontsize=18)
  plt.xlabel('time',fontsize=18)
  if ocean == 'undefined':
      plt.title('Arctic mediterranean seas ($>$'+str(lat_min)+'$^{o}$N)')
  else:
      plt.title(str(ocean.replace("_"," ")))
  plt.savefig(str(variable_name)+'/'+str(name_outfile.replace(".",""))+'.png')
  return


def time_serie_sea_ice_ext(path,var,lat_min,basin):
  yr, xr, time = loading.extracting_coord_2D(path)
  ice = loading.extracting_var(path, var)
  S = loading.extracting_var(path,'sal')

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


simu = From1950to2100(option,var,y1,y2,comparison,lat_min,basin) 
time, ice_extent = time_serie_sea_ice_ext(simu.path,var,lat_min,basin)
index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))

var_fc_time(ice_extent[index_y1:index_y2+1],var,time[index_y1:index_y2+1],simu.first_year,lat_min,simu.output_file,basin)