import mpl_toolkits
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


# This script is made to extract (in situ..) salinity and temperature so as to compute
# potential density rho(Absolute salinity, conservative temperature, P_ref = 0db)
# The potential density is then used to compute the mixed layer depth (with the surface-
# density-difference of 0.03kg.m-3 criterion, cf [Sallee, Speer, Rintoul 2010])
# This is done for one time step (one year..) and is plotted on a map
# > PB1: we should consider interpolating the densities every meter because this method
#        overestimate the MLD (if the density difference is at z=12m, given we only have
#        data at z=10 and z=20, we would conclude MLD=20m in this case
# > PB2: need to be careful about the fact that T,P=0 on lands / below the ocean bottom...
# > PB3: seems like we get issues when the mixed-layer is deeper than the bottom...so far
#        when the script does not find the MLD, it is set to zero.
 
# WHAT THE USER CAN CHANGE:--------
option = 'Coupled'			# Coupled or Uncoupled
y1 = 2000				# a year between 1950 and 2100
y2 = 2100
var = 'density'

comparison = 'no'

basin ='undefined'          # arctic_ocean, BS_and_KS, greenland_sea, undefined
lat_min = 60#66.34                 #IF basin = 'undefined'
                                #ex: 66.34 for polar circle

#----------------------------------

#//////////////////////////////////////////////////////////////////////////////////////////
class yearly_LongPeriod():                                                               #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var,y1,y2,basin,lat_min):                                                      #//
      self.first_year = 1950                                                            #//
      self.last_year = 2100
      self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/density/sig0.nc'
      if basin == 'undefined':                                                           #//
        sufix = str(lat_min)+'_'+str(option)
      else:
        sufix = str(basin)+'_'+str(option)

      self.y1 = y1
      self.y2 = y2
      self.max_depth = 500                                                             #//
      if var == 'temp':                                                                 #//
        self.vmin = -5                                                                  #//
        self.vmax = 10                                                                  #//
      elif var == 'sal':                                                                #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
      elif var == 'density':
        self.vmin = 22
        self.vmax = 27
      self.output_file =  str(var)+'_yearmean'+str(self.y1)+'_'+str(sufix)
      self.output_file2 =  str(var)+'_'+str(self.y1)+'_'+str(self.y2)+'mean_'+str(sufix)
                                                                                        #//
      return                                                                            #//
                                                                                        #//
#//////////////////////////////////////////////////////////////////////////////////////////



simu = yearly_LongPeriod(option,var,y1,y2,basin,lat_min)

yr, xr, time, depth = loading.extracting_coord(simu.path)

VarArray_simuRho = loading.extracting_var(simu.path, 'rho')   # Practical Salinity

print(np.shape(VarArray_simuRho))
VarArray_simuRho[np.where(VarArray_simuRho==0)] = np.nan
MEAN = np.nanmean(np.nanmean(VarArray_simuRho[:,:,:,0],axis=0),axis=0)
print(MEAN)
make_plot.vertical_profile(MEAN,MEAN,var,simu.vmin,simu.vmax,depth,simu.max_depth,basin,lat_min,simu.output_file)

sig=0.1
make_plot.vertical_profile3(MEAN,MEAN-sig,MEAN+sig,y1,y2,var,simu.vmin,simu.vmax,depth,simu.max_depth,basin,lat_min,simu.output_file2)
                                                                                                                                       

