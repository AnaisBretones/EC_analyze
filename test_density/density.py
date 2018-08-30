import mpl_toolkits
#from  mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as py
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec
import scipy
import netCDF4
import gsw 

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
      self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/density/rcp8.5_PISM_2300_yearly.nc'
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

#//////////////////////////////////////////////////////////////////////////////////////////
class yearlyAnomaly_LongPeriod():                                                       #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var):                                                      #//
      self.first_year = 1950                                                            #//
      self.last_year = 2100
      self.path_ref = '../'+str(var)+'TimeMean_'+str(option)+'.nc'                      #//
      self.path = '../'+str(var)+'_from'+str(self.first_year)+'to'\
                  +str(self.last_year)+'_'+str(option)+'.nc'                            #//
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

VarArray_simuT = loading.extracting_var(simu.path, 'temp')   # Practical Salinity
VarArray_simuS = loading.extracting_var(simu.path, 'sal')    # In situ temperature

ni = np.size(VarArray_simuT[:,0,0,0])
nj = np.size(VarArray_simuT[0,:,0,0])
nz = np.size(VarArray_simuT[0,0,:,0])

SA = np.zeros((ni,nj,nz))
CT = np.zeros((ni,nj,nz))
rho_ref = np.zeros((ni,nj,nz))

print(np.shape(VarArray_simuT))

k=0
for i in range(0,ni):
  for j in range(0,nj):
    # if we are on the mask (S=0,T=0) 
    if VarArray_simuS[i,j,0] == 0 or VarArray_simuT[i,j,0] == 0:
       rho_ref[i,j,:] = np.nan
    else:
      p = gsw.p_from_z(-depth,yr[i,j])
      #SA[i,j,:] = gsw.SA_from_SP(VarArray_simuS[i,j,:,0],p,xr[i,j],yr[i,j]) #VarArray_simuS[i,j,:,0]
      #CT[i,j,:] = gsw.CT_from_t(SA[i,j],VarArray_simuT[i,j,:,0],p) #VarArray_simuT[i,j,:,0]
      rho_ref[i,j,:] = gsw.rho(VarArray_simuS[i,j,:,0],VarArray_simuT[i,j,:,0],0) 
      #rho_ref[i,j,:] = gsw.rho(SA[i,j,:],CT[i,j,:],0)
      rho_ref[i,j,np.where(rho_ref[i,j,:]<1000)]=np.nan

def vertical_profile(var,variable_name,z,zmax,name_file,option):

   i_zmax = np.max(np.where(z<zmax))
   fig = plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   plt.plot(var[0:i_zmax+1]-1000,z[0:i_zmax+1])
   plt.gca().invert_yaxis()
   plt.ylabel(r'Depth (m)')
   if variable_name == 'temp':
     plt.xlabel(r'Temperature ($^{o}$C)')
   elif variable_name == 'density':
     plt.xlabel(r'Density')
   plt.xlim([22,27])
   plt.ylim([450,0])
   plt.title(str(option))
   plt.savefig(str(variable_name)+'/'+str(name_file)+'.png')
   plt.close(fig)
   return

name_file = 'density_profile_changeS'+str(year)
vertical_profile(np.nanmean(rho_ref,axis=(0,1)),'density',depth,2000,name_file,'Arctic')



