from  mpl_toolkits.basemap import Basemap
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

var='brine'

option = 'Coupled'
specificity = ''

#basin = 'Siberian_seas'
#basin = 'arctic_ocean'
#basin = 'greenland_sea'  # arctic_ocean, Siberian_seas
basin = 'undefined'
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
     if var == 'brine':                                                                  #//
        self.path = '/media/fig010/LACIE SHARE/EC_data/March'+str(y1)+'-'+str(y2)+'/'\
                  'Marchsalt_'+str(y1)+'-'+str(y2)+'.nc'

     if basin != 'undefined':
       self.output_fileC = str(var)+'_March_'+str(basin)+'_10yAnomaly_'+str(self.y1h)+'-'+str(self.y1f)+'_'+str(colorbar)                                #//
       self.output_fileH = str(var)+'_March_'+str(basin)+'_'+str(self.y1h)+'-'+str(self.y2h)+'_'+str(colorbar)                                #//
       self.output_fileF = str(var)+'_March_'+str(basin)+'_'+str(self.y1f)+'-'+str(self.y2f)+'_'+str(colorbar)                                #//
     else:
       self.output_fileC = str(var)+'_March_10yAnomaly_'+str(self.y1h)+'-'+str(self.y1f)+'_'+str(colorbar)                                #//
       self.output_fileH = str(var)+'_March_'+str(self.y1h)+'-'+str(self.y2h)+'_'+str(colorbar)                                #//
       self.output_fileF = str(var)+'_March_'+str(self.y1f)+'-'+str(self.y2f)+'_'+str(colorbar)                                #//
       #self.output_fileC = str(var)+'flux_March_10yAnomaly_'+str(self.y1h)+'-'+str(self.y1f)+'_'+str(colorbar)                                #//
       #self.output_fileH = str(var)+'flux_March_'+str(self.y1h)+'-'+str(self.y2h)+'_'+str(colorbar)                                #//
       #self.output_fileF = str(var)+'flux_March_'+str(self.y1f)+'-'+str(self.y2f)+'_'+str(colorbar)                                #//

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////



simu = From1950to2100(option,var,y1p,y2p,colorbar,basin)
   
yr, xr, time = loading.extracting_coord_2D(simu.path)
time = simu.first_year+time[:]/(3600*24*364.5)
   
IceExt = loading.extracting_var(simu.path, var)
IceExt[np.where(IceExt>1E10)]=np.nan
IceExt[np.where(IceExt<0)] = np.nan

  
if basin =='undefined':
   mask = loading.latitudinal_band_mask(yr,lat_min,90)
else:
   mask = loading.Ocean_mask(xr,yr,basin)

 
index_y1h = np.min(np.where(time>simu.y1h))
index_y1f = np.min(np.where(time>simu.y1f))

array_to_plotH = np.nanmean(IceExt[:,:,index_y1h:index_y1h+10],axis=2)
array_to_plotH[array_to_plotH==np.nan] = 0

array_to_plotF = np.nanmean(IceExt[:,:,index_y1f:index_y1f+10],axis=2)
array_to_plotF[array_to_plotF==np.nan] = 0


array_to_plotC = array_to_plotF - array_to_plotH
array_to_plotC[array_to_plotC==0] = np.nan
array_to_plotC[~mask] = np.nan
array_to_plotC = np.ma.masked_invalid(array_to_plotC)

array_to_plotH[array_to_plotH<=0] = np.nan
array_to_plotH[~mask] = np.nan
array_to_plotH = np.ma.masked_invalid(array_to_plotH)

array_to_plotF[array_to_plotF<=0] = np.nan
array_to_plotF[~mask] = np.nan
array_to_plotF = np.ma.masked_invalid(array_to_plotF)

if var == 'brine':
  vmin = -0.001#-0.002
  vmax = 0.007
title= str(simu.y1h)+'-'+str(simu.y2h)
make_plot.plot_map(xr,yr,array_to_plotH,var,title,simu.output_fileH,vmin,vmax,colorbar)
title= str(simu.y1f)+'-'+str(simu.y2f)
make_plot.plot_map(xr,yr,array_to_plotF,var,title,simu.output_fileF,vmin,vmax,colorbar)
make_plot.plot_map_ano(xr,yr,array_to_plotC,var,simu.y1f,'future-current',simu.output_fileC,vmin,vmax,colorbar)


