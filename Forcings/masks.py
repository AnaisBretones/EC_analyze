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

import make_plot
import loading


var = 'MeltedIce'			# sal, runoff, albedo, downHF
option = 'Coupled'		# Coupled, Uncoupled
y1 = 1950
y2 = 2100

basin ='around_greenland'		# arctic_ocean, BS_and_KS, undefined
lat_min = 66.34 		#IF basin = 'undefined'
                                #ex: 66.34 for polar circle

comparison = 'no'
y1_compa = 1950
y2_compa = 2000

if var == 'IceC':
   y1 = 1950


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
        self.output_file = str(var)+'_TimeSerie_'+str(sufix)
     elif compa == 'yes':
        self.output_file = str(var)+'_TimeSerieAnomaly_'+str(sufix)

     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/Forcings_'+str(option)+'.nc' 

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
       elif var == 'runoff':
        self.vmin = 0               	                                                #//
        self.vmax = 30	                	                                        #//
       elif var == 'downHF':
        self.vmin = 0                                                                   #//
        self.vmax = 30		                                                        #//
       elif var == 'albedo':
        self.vmin = 0                                                                   #//
        self.vmax = 10		                                                        #//
       elif var == 'MeltedIce':
        self.vmin = 0                                                                   #//
        self.vmax = 10		                                                        #//
     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////

m1 = 'arctic_mediterranean'
m2 = 'greenland_sea'
m3 = 'BS_and_KS'
m4 = 'around_greenland'
m5 = 'arctic_ocean'

simu = From1950to2100(option,var,y1,y2,comparison,lat_min,basin) 
yr, xr, time = loading.extracting_coord_2D(simu.path)


mask1 = loading.latitudinal_band_mask(yr,lat_min,90)
mask2 = loading.Ocean_mask(xr,yr,m2)
mask3 = loading.Ocean_mask(xr,yr,m3)
mask4 = loading.Ocean_mask(xr,yr,m4)
mask5 = loading.Ocean_mask(xr,yr,m5)

make_plot.masks_on_map(var,xr[mask1],yr[mask1],m1, \
                        xr[mask2],yr[mask2],m2, \
                        xr[mask3],yr[mask3],m3, \
                        xr[mask4],yr[mask4],m4, \
                        xr[mask5],yr[mask5],m5 )
                          



