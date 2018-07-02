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

#import make_plot
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
year = 2100				# a year between 1950 and 2100
comparison = 'no'
#----------------------------------

#//////////////////////////////////////////////////////////////////////////////////////////
class yearly_LongPeriod():                                                               #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var):                                                      #//
      self.first_year = 1950                                                            #//
      self.last_year = 2100
      self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/sig0_'\
                  +str(option)+'.nc'                                                    #//
      self.max_depth = 1000                                                             #//
      if var == 'temp':                                                                 #//
        self.vmin = -5                                                                  #//
        self.vmax = 10                                                                  #//
      elif var == 'sal':                                                                #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
      elif var == 'ML':
        self.vmin = 0
        self.vmax = 300
      self.output_file = str(var)+'_ymeans_'+str(option)                                #//
                                                                                        #//
      return                                                                            #//
                                                                                        #//
#//////////////////////////////////////////////////////////////////////////////////////////



if comparison == 'no':
   simu = yearly_LongPeriod(option,'ML')
elif comparison == 'yes':
   simu = yearlyAnomaly_LongPeriod(option,var)
   VarArray_ref = loading.extracting_var(simu.path_ref, var)

yr, xr, time, depth = loading.extracting_coord(simu.path)

VarArray_simuRho = loading.extracting_var(simu.path, 'rho')   # Practical Salinity

index_y = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>year))



def vertical_profile(var,variable_name,z,zmax,name_file,option):

   i_zmax = np.max(np.where(z<zmax))
   fig = plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   plt.plot(var[0:i_zmax+1],z[0:i_zmax+1])
   plt.gca().invert_yaxis()
   plt.ylabel(r'Depth (m)')
   if variable_name == 'temp':
     plt.xlabel(r'Temperature ($^{o}$C)')
   elif variable_name == 'density':
     plt.xlabel(r'Density')
   plt.xlim([24.5,28])
   plt.ylim([z[i_zmax],0])
   plt.title(str(option))
   plt.savefig(str(variable_name)+'/'+str(name_file)+'.png')
   plt.close(fig)
   return

name_file = 'density_profile0_'+str(year)

VarArray_simuRho[np.where(VarArray_simuRho==0)] = np.nan
vertical_profile(np.nanmean(VarArray_simuRho[:,:,:,index_y],axis=(0,1)),'density',depth,2000,name_file,'Arctic')



