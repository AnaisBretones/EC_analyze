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

var = 'density'		#sal, temp, density, Uorth
option = 'Coupled'
specificity = ''
y1 = 2040#+140
y2 = y1+12
basin ='SiberianOrth'           # GSR, SiberianOrth


comparison = 'no'
output_file = str(var)+'_'+str(basin)+'_plaquette_'+str(y1)+'To'+str(y2)+'_'+str(option)                                #//


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,var,y1,y2,compa,basin):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1 = y1                                                                       #//
     self.y2 = y2                                                                       #//
     self.y1_compa = y1+1
     self.y2_compa = 2042
     self.output_file = str(var)+'_plaquette_'+str(self.y1)+'To'+str(self.y2)+'_'+str(option)                                #//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/section/section_'+str(basin)+'_'+str(option)+'.nc'
     self.zmax = 800
     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = 1                                                                   #//
        self.vmax = 7                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -2                                                               #//
        self.vmax = 2                                                                #//
      elif var == 'ML':
        self.vmin = -20
        self.vmax = 20
      elif var == 'IceC':
        self.vmin = -1
        self.vmax = 1.

     elif compa =='no':
      if var == 'IceC':
	self.vmin = 0
        self.vmax = 0.15
      elif var == 'ML':
        self.vmin = 12
        self.vmax = 70
      elif var == 'temp':                                                                #//
        self.vmin = -1.6                                                               #//
        self.vmax = 0.25                                                               #//
      elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
      elif var == 'density':                                                               #//
        self.vmin = 25                                                               #//
        self.vmax = 28                                                               #//
      elif var == 'Uorth':                                                                #//
        self.vmin = -0.04                                                              #//
        self.vmax = 0.018           

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////


fig = plt.figure(figsize=(10, 6))
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


fig.subplots_adjust(hspace=0.4, wspace=0.000001)

for i in range(1,13):
   ax = plt.subplot(3, 4, i)
   ax.set_title(str(y1),color='r')
   simu = From1950to2100(option,var,y1,y2,comparison,basin)
   yr, xr, time, depth, X = loading.extracting_coord_1D(simu.path)

   VAR = loading.extracting_var(simu.path, var)

   if var == 'sal':
     VAR[np.where( VAR < 32. )] = np.nan
   elif var == 'density':
     VAR[np.where( VAR < 24)] =np.nan
   else:
     S = loading.extracting_var(simu.path,'sal')
     VAR[ S==0 ] = np.nan

   index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>y1))

   i_zmax = np.max(np.where(depth<simu.zmax))
   print(np.nanmax(VAR[:,0:i_zmax+1,index_y1].transpose()), np.shape(VAR[:,:,:]))
   im = plt.contourf(X,depth[0:i_zmax+1],VAR[:,0:i_zmax+1,index_y1].transpose(),40,vmin=simu.vmin,vmax=simu.vmax)#,vmin=31.76,vmax=34.02)
   plt.xticks([250,500])
   plt.yticks([200,400,600])
   plt.ylim([np.min(depth),depth[i_zmax]])
   plt.ylabel(r'Depth (m)')
   plt.gca().invert_yaxis()
 
   #plt.xticks(tick_locs,tick_lbls)
   '''cbar = plt.colorbar()
   cbar.ax.get_yaxis().labelpad = 15
   '''
   
   y1 = y1+1
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
if var == 'temp':
  cbar.set_label(r'Temperature ($^{o}$C)',fontsize=18)
elif var == 'sal':
  cbar.set_label(r'Salinity (PSU)',fontsize=18)
elif var == 'density':
  cbar.set_label(r'Potential density',fontsize=18)
elif var == 'Uorth':
  cbar.set_label(r'Velocity ortho to section (m/s)',fontsize=18)
plt.savefig(str(var)+'/'+str(output_file)+'.png',format='png')          
