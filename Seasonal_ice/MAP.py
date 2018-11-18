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

var = 'IceC'
option = 'Coupled'
specificity = ''

month = 'Sept'
y1p = 1950          #first year in the data
y2p = 2300          #last year in the data


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,var,y1,y2,month):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1h = 2010 #1950                                                                       #//
     self.y2h = 2020
     self.y1f = 2080 #2090
     self.y2f = 2090                                                                       #//
     self.path = '/media/fig010/LACIE SHARE/EC_data/'+str(month)+str(y1)+'-'+str(y2)+'/'\
                  +str(month)+'_Ice_'+str(option)+'.nc'

     self.path_thickness = '/media/fig010/LACIE SHARE/EC_data/'+str(month)+str(y1)+'-'\
                            '2100/icef'+str(month)+'_'+str(y1)+'-2100.nc'
     self.output_fileH = str(var)+str(month)+'_'+str(self.y1h)+'-'+str(self.y2h)                                #//
     self.output_fileF = str(var)+str(month)+'_'+str(self.y1f)+'-'+str(self.y2f)                                #//

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////



simu = From1950to2100(option,var,y1p,y2p,month)
   
yr, xr, time = loading.extracting_coord_2D(simu.path)
time = simu.first_year+time[:]/(3600*24*364.5)
   
IceExt = loading.extracting_var(simu.path, var)
   
index_y1h = np.min(np.where(time>simu.y1h))
   
index_y1f = np.min(np.where(time>simu.y1f))

array_to_plotH = np.nanmean(IceExt[:,:,index_y1h:index_y1h+10],axis=2)
array_to_plotH[array_to_plotH==0] = np.nan
array_to_plotH = np.ma.masked_invalid(array_to_plotH)

array_to_plotF = np.nanmean(IceExt[:,:,index_y1f:index_y1f+10],axis=2)
array_to_plotF[array_to_plotF==0] = np.nan
array_to_plotF = np.ma.masked_invalid(array_to_plotF)

IceThick = loading.extracting_var(simu.path_thickness, 'iicethic')
IceThick_to_ploth = np.nanmean(IceThick[:,:,index_y1h:index_y1h+10],axis=2)
IceThick_to_ploth[IceThick_to_ploth==0] = np.nan
IceThick_to_ploth = np.ma.masked_invalid(IceThick_to_ploth)

IceThick_to_plotF = np.nanmean(IceThick[:,:,index_y1f:index_y1f+10],axis=2)
IceThick_to_plotF[IceThick_to_plotF==0] = np.nan
IceThick_to_plotF = np.ma.masked_invalid(IceThick_to_plotF)


if month =='March':
  title_plot = 'WINTER'
  vmin = 0 
  vmax = 6
elif month =='Sept':
  vmin = 0
  vmax = 5.5
  title_plot = 'SUMMER'
make_plot.plot_map_with_ice_extent(xr,yr,IceThick_to_ploth,var,array_to_plotH,simu.y1h,title_plot,simu.output_fileH,vmin,vmax)
make_plot.plot_map_with_ice_extent(xr,yr,IceThick_to_plotF,var,array_to_plotF,simu.y1f,title_plot,simu.output_fileF,vmin,vmax)

