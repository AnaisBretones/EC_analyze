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


var = 'temp'			# sal, temp, Uorth Utang density
option = 'Coupled'		# Coupled, Uncoupled

y1 = 1950
y2 = 2100

                                #ex: 66.34 for polar circle

y1_compa = 1950
y2_compa = 2000
#Colorbar='unchanged'
Colorbar=''

#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():									#//
        										#//
  #___________________									#//
  def __init__(self,option,var,y1,y2):				#//
     self.max_depth = 1000	                                                        #//
     self.first_year = 1950
     self.y1 = y1 	                                                                #//
     self.y2 = y2
     
     self.y1h = 2010 #1950                                                                       #//
     self.y2h = 2020
     self.y1f = 2080 #2090
     self.y2f = 2090 
     sec='CC'
     self.pathE = '/media/fig010/LACIE SHARE/EC_data/yearly'+str(self.y1)+'-'+str(self.y2)+'/sectionE_'+str(sec)+'.nc'

     sec='AOtoBS'
     #sec='FS'
     self.pathW = '/media/fig010/LACIE SHARE/EC_data/yearly'+str(self.y1)+'-'+str(self.y2)+'/sectionW_'+str(sec)+'.nc'

     self.output_fileH = str(var)+'_'+str(self.y1h)+'-'+str(self.y2h)+'_'+str(sec)                                #//
     self.output_fileF = str(var)+'_'+str(self.y1f)+'-'+str(self.y2f)+'_'+str(sec)                                #//
     self.output_fileC = str(var)+'Anomaly_'+str(self.y1h)+'-'+str(self.y1f)+'_'+str(sec)                                #//
 
     if var == 'temp':
        if sec =='FS':
          self.vmin = -1.                                                                   #//
          self.vmax = 4                                                                #//
        elif sec=='CC' or sec=='AOtoBS':
          self.vmin = -1.3                                                                   #//
          self.vmax = 6                                                                #//
     
        self.vminC = 0.6                                                                   #//
        self.vmaxC = 5                                                                #//
                                                                      #//
        self.lmin = -1.8                                                                   #//
        self.lmax = 7                                                                #//
        self.lminC = 2.5                                                                   #//
        self.lmaxC = 5                                                                #//

     elif var == 'sal':                                                                #//
        self.lmin = 30                                                              #//
        self.lmax = 35                                                                #//
        self.lminC = -0.5                                                              #//
        self.lmaxC = 0.5                                                              #//
        self.vmin =30 
        self.vmax = 35.2
        self.vminC = -0.75
        self.vmaxC=1.25
     else:
        self.vmin = 0
        self.vmax = 0
        self.vminC=0
        self.vmaxC=0

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////


simu = From1950to2100(option,var,y1,y2) 
yrE, xrE, time, depth, XE = loading.extracting_coord_1D(simu.pathE)
yrW, xrW, time, depth, XW = loading.extracting_coord_1D(simu.pathW)

VARE = loading.extracting_var(simu.pathE, var)
VARW = loading.extracting_var(simu.pathW, var)

time = simu.y1+time[:]/(3600*24*364.5)
index_y1h = np.min(np.where(time>simu.y1h))

index_y1f = np.min(np.where(time>simu.y1f))

print(index_y1h,index_y1f)

if var == 'sal':
  VARE[np.where( VARE < 30. )] = np.nan
  VARW[np.where( VARW < 30. )] = np.nan
elif var == 'density':
  VARE[np.where( VARE < 24)] =np.nan
  VARW[np.where( VARW < 24)] =np.nan
else:
  SE = loading.extracting_var(simu.pathE,'sal')
  VARE[ SE==0 ] = np.nan
  SW = loading.extracting_var(simu.pathW,'sal')
  VARW[ SW==0 ] = np.nan



var_to_plot = np.hstack((np.nanmean(VARW[:,:,index_y1h:index_y1h+10],axis=2).transpose(),np.nanmean(VARE[:,:,index_y1h:index_y1h+10],axis=2).transpose()))
X_to_plot = np.concatenate((XW,XE+XW[-1]),axis=0)
X_to_plot = np.ma.masked_invalid(X_to_plot)

make_plot.one_sec(var_to_plot,var,X_to_plot,depth,simu.max_depth,y1,simu.output_fileH,simu.lmin,simu.lmax,str(simu.y1h)+'-'+str(simu.y2h),Colorbar,simu.vmin,simu.vmax)

var_to_plot2 = np.hstack((np.nanmean(VARW[:,:,index_y1f:index_y1f+10],axis=2).transpose(),np.nanmean(VARE[:,:,index_y1f:index_y1f+10],axis=2).transpose()))
make_plot.one_sec(var_to_plot2,var,X_to_plot,depth,simu.max_depth,y1,simu.output_fileF,simu.lmin,simu.lmax,str(simu.y1f)+'-'+str(simu.y2f),Colorbar,simu.vmin,simu.vmax)

make_plot.one_sec(var_to_plot2-var_to_plot,var,X_to_plot,depth,simu.max_depth,y1,simu.output_fileC,simu.lminC,simu.lmaxC,'future-current',Colorbar,simu.vminC,simu.vmaxC)
