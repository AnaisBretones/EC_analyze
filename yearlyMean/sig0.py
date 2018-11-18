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
y1 = 1950				# a year between 1950 and 2100
y2 = 2100
var = 'temp'

comparison = 'no'

basin ='Siberian_seas'          # arctic_ocean, BS_and_KS, greenland_sea, undefined
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
      if var =='density':
        self.path = '/media/fig010/LACIE SHARE/EC_data/yearly'+str(y1)+'-'+str(y2)+'/sig0.nc'
      elif var =='sal' or var=='temp':
        self.path = '/media/fig010/LACIE SHARE/EC_data/yearly'+str(y1)+'-'+str(y2)+'/T.nc'
 
      '''if basin == 'undefined':                                                           #//
        sufix = str(lat_min)+'_'+str(option)
      else:
        sufix = str(basin)+'_'+str(option)
      '''
      self.y1 = y1
      self.y2 = y2
      self.max_depth = 2000                                                             #//

      self.y1h = 2010 #1950                                                                       #//
      self.y2h = 2020
      self.y1f = 2080 #2090
      self.y2f = 2090   

      if var == 'temp':                                                                 #//
        self.vmin = -2                                                                  #//
        self.vmax = 6                                                                  #//
      elif var == 'sal':                                                                #//
        self.vmin = 31                                                               #//
        self.vmax = 35                                                              #//
      elif var == 'density':
        self.vmin = 25
        self.vmax = 28.1
      self.output_fileH =  str(var)+'_10yearmean_'+str(self.y1h)+'-'+str(self.y2h)
      self.output_fileF =  str(var)+'_10yearmean_'+str(self.y1f)+'-'+str(self.y2f)
                                                                                        #//
      return                                                                            #//
                                                                                        #//
#//////////////////////////////////////////////////////////////////////////////////////////

def vertical_profile(var1,var2,var3,y1,l1,l2,l3,variable_name,vmin,vmax,z,zmax,ocean,lat_min,name_file):
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   i_zmax = np.max(np.where(z<zmax))

   #z2 = np.zeros_like(z[0:i_zmax+1])
   #z2[:] = 1000

   plt.figure(figsize=(7,15))
   fig,ax = plt.subplots()
   ax.plot(var1[0:i_zmax+1],z[0:i_zmax+1],color = 'b',label=str(l1.replace("_"," ")))
   #ax.plot(var2[0:i_zmax+1],z[0:i_zmax+1],label=str(l2.replace("_"," ")))
   ax.plot(var3[0:i_zmax+1],z[0:i_zmax+1],color = 'r',label=str(l3.replace("_"," ")))
   #ax.plot(var3[0:i_zmax+1],z2,'k-')

   plt.gca().invert_yaxis()
   plt.ylabel(r'Depth (m)',fontsize=15)
   if variable_name == 'temp':
     plt.xlabel(r'Temperature ($^{o}$C)',fontsize=18)
   elif variable_name == 'density':
     plt.xlabel(r'Density (kg.m$^{-3}$',fontsize=18)
   elif variable_name == 'sal':
     plt.xlabel(r'Salinity (PSU)',fontsize=18)
     plt.xticks([32,33,34,35])
   plt.yticks([500, 1000,1500])
   plt.xlim([vmin,vmax])
   plt.ylim([z[i_zmax],0])
   plt.xticks(size = 20)
   plt.yticks(size = 20)

   if y1<2050:
     plt.title('PRESENT ('+str(y1)+')',fontsize=18)#str(y1)+'-'+str(y1+10))
   else:
     plt.title('FUTURE ('+str(y1)+')',fontsize=18)#str(y1)+'-'+str(y1+10))

   box = ax.get_position()
   ax.set_position([box.x0*1.2, box.y0 + box.height * 0.3,
                 box.width, box.height * 0.7])
   h, l = ax.get_legend_handles_labels()
   ax.legend(h, l,  bbox_to_anchor=(-.5,-.05, 2,-0.35), loc=9,
           ncol=1)

   plt.savefig(str(variable_name)+'/'+str(name_file.replace(".",""))+'.png')

   plt.close(fig)
   return


simu = yearly_LongPeriod(option,var,y1,y2,basin,lat_min)

yr, xr, time, depth = loading.extracting_coord(simu.path)

VarArray_simuRho = loading.extracting_var(simu.path, var)   # Practical Salinity


if var =='temp':
  S = loading.extracting_var(simu.path, 'sal')   # Practical Salinity
  VarArray_simuRho[np.where(S==0)] = np.nan
else:
  VarArray_simuRho[np.where(VarArray_simuRho==0)] = np.nan
index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1h))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1f))

b1='arctic_ocean'
b2='Siberian_seas'
b3='BS_and_KS'

'''
if basin =='undefined':
   mask = loading.latitudinal_band_mask(yr,lat_min,90)
else:
   mask = loading.Ocean_mask(xr,yr,basin)
   make_plot.points_on_map(xr[mask],yr[mask],var,basin)
'''

mask1=loading.Ocean_mask(xr,yr,b1)
mask2=loading.Ocean_mask(xr,yr,b2)
mask3=loading.Ocean_mask(xr,yr,b3)

r1 = VarArray_simuRho[mask1,:,:]
r2 = VarArray_simuRho[mask2,:,:]
r3 = VarArray_simuRho[mask3,:,:]
mean_region1 = np.nanmean(r1,axis=0)
mean_region2 = np.nanmean(r2,axis=0)
mean_region3 = np.nanmean(r3,axis=0)


vertical_profile(np.nanmean(mean_region1[:,index_y1:index_y1+10],axis=1),\
          np.nanmean(mean_region2[:,index_y1:index_y1+10],axis=1),\
          np.nanmean(mean_region3[:,index_y1:index_y1+10],axis=1),simu.y1h,b1,b2,b3,var,simu.vmin, \
          simu.vmax,depth,simu.max_depth,basin,lat_min,simu.output_fileH)

vertical_profile(np.nanmean(mean_region1[:,index_y2:index_y2+10],axis=1),\
          np.nanmean(mean_region2[:,index_y2:index_y2+10],axis=1),\
          np.nanmean(mean_region3[:,index_y2:index_y2+10],axis=1),simu.y1f,b1,b2,b3,var,simu.vmin, \
          simu.vmax,depth,simu.max_depth,basin,lat_min,simu.output_fileF)

'''
MEAN = np.zeros_like((mean_region[:,0]))
MEAN2 = np.zeros_like((mean_region[:,0]))
sig = np.zeros_like(mean_region[:,0])

MEAN = np.nanmean(mean_region,axis=1)
MEAN2 = np.nanmean(mean_region**2,axis=1)
#for i in range(0,np.size(MEAN2[0,:])):
sig = np.sqrt(MEAN2-MEAN**2)

make_plot.vertical_profile3(MEAN,MEAN-sig,MEAN+sig,y1,y2,var,simu.vmin,simu.vmax,depth,simu.max_depth,basin,lat_min,simu.output_file2)
'''                                                                                                                                    

