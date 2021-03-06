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


var = 'runoff'
option = 'Uncoupled'		# Coupled, Uncoupled
y1 = 1950
y2 = 2100
month = 'april'                  #Sept or April
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
  def __init__(self,option,var,y1,y2,compa,lat_min,basin,month):				#//
     self.max_depth = 1000	                                                        #//
     self.first_year = 1950
     self.y1 = y1 	                                                                #//
     self.y2 = y2
     if basin == 'undefined':								#//
        sufix = str(self.y1)+'to'+str(self.y2)+'_'+str(lat_min)+'_'+str(option)
     else: 
        sufix = str(self.y1)+'to'+str(self.y2)+'_'+str(basin)+'_'+str(option)

     if compa == 'no':									#//
        self.output_file = str(var)+'extent_TimeSerie_'+str(sufix)
     elif compa == 'yes':
        self.output_file = str(var)+'extent_TimeSerieAnomaly_'+str(sufix)

     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/Forcings_'\
                  +str(option)+'.nc' 

     if compa == 'yes':
        self.vmin = -1                                                                   #//
        self.vmax = 2.6                                                                 #//

     elif compa =='no':
        self.vmin = -3*1E14                                                               #//
        self.vmax = 3*1E14                                                              #//

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
  plt.plot(first_year_file+t,var)
  plt.ylabel('FWF (kg.s$^{-1}$)',fontsize=18)
  plt.xlabel('time',fontsize=18)
  if ocean == 'undefined':
      plt.title('Arctic mediterranean seas ($>$'+str(lat_min)+'$^{o}$N)')
  else:
      plt.title(str(ocean.replace("_"," ")))
  plt.savefig(str(variable_name)+'/'+str(name_outfile.replace(".",""))+'.png')
  return


def time_serie_Arctic_2D(path,var_name,lat_min,basin):
  yr, xr, time = loading.extracting_coord_2D(path)
  VAR = loading.extracting_var(path, var_name)
  S = loading.extracting_var(path,'sal')
  VAR[np.where( S[:,:,0,:]==0. )] = 0#np.nan
  VAR[np.where(VAR>1E10)]=0#np.nan

  if basin =='undefined':
     mask = loading.latitudinal_band_mask(yr,lat_min,90)
  else:
     mask = loading.Ocean_mask(xr,yr,basin)

  VAR[np.where(VAR==0)]=np.nan

  area = size_each_bins(xr,yr)

  FWF = area[mask]*VAR[mask,:].transpose(1, 0)*1E6
  mean_FWF = np.nansum(FWF,axis=1)


  return time, mean_FWF



def time_serie(path,var,lat_min,basin):
  yr, xr, time = loading.extracting_coord_2D(path)
  melted_ice = loading.extracting_var(path, var)
  S = loading.extracting_var(path,'sal')

  if basin =='undefined':
     mask = loading.latitudinal_band_mask(yr,lat_min,90)
  else:
     mask = loading.Ocean_mask(xr,yr,basin)
  area = size_each_bins(xr,yr)

  FWF = area[mask]*melted_ice[mask].transpose(1, 0)*1E6
  mean_FWF = np.nansum(FWF,axis=1)
  return time, mean_FWF

def var_fc_time_2(var,var2,variable_name,t,first_year_file,lat_min,name_outfile,ocean):
  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  t = t/(3600*24*365.)
  plt.xlim([first_year_file+np.min(t),first_year_file+np.max(t)])
  #plt.ylim([0.,0.75])
  plt.plot(first_year_file+t,var, label = 'Uncoupled')
  plt.plot(first_year_file+t,var2, label = 'Coupled')
  if variable_name == 'IceC':
     plt.ylabel('Ice cover',fontsize=18)
  elif variable_name=='MeltedIce' or variable_name =='runoff':
     plt.ylabel('FWF (kg.s$^{-1}$)')

  plt.xlabel('time',fontsize=18)
  if ocean == 'undefined':
      plt.title('Arctic Mediterranean ($>$'+str(lat_min)+'$^{o}$N)')
  else:
      plt.title(str(ocean.replace("_"," ")))

  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * 0.3,
                 box.width, box.height * 0.7])
  h, l = ax.get_legend_handles_labels()
  ax.legend(h, l,  bbox_to_anchor=(-.5,-.05, 2,-0.15), loc=9,
           ncol=1)
  plt.savefig(str(variable_name)+'/'+str(name_outfile.replace(".",""))+'.png')
  return

  

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

simu = From1950to2100(option,var,y1,y2,comparison,lat_min,basin,month) 
time, FWF_region = time_serie_Arctic_2D(simu.path,var,lat_min,basin)

simu_c = From1950to2100('Coupled',var,y1,y2,comparison,lat_min,basin,month) 
time, FWF_region_c = time_serie_Arctic_2D(simu_c.path,var,lat_min,basin)


index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))
 
var_fc_time_2(FWF_region[index_y1:index_y2+1],FWF_region_c[index_y1:index_y2+1],var,time[index_y1:index_y2+1],simu.first_year,lat_min,simu.output_file,basin)
