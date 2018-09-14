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


var = 'sal'			# sal, temp, Uorth Utang density
option = 'Coupled'		# Coupled, Uncoupled

y1 = 2200
y2 = y1+10

lat_min = 50 #66.34 		#IF basin = 'undefined'
                                #ex: 66.34 for polar circle
if y1>=2000 and y1<=2090:
  period='2000_2100'
elif y1>=2100 and y1<=2190:
  period='2100_2200'
elif y1>=2200 and y1<=2290:
  period='2200_2300'
comparison = 'no'
y1_compa = 1950
y2_compa = 2000
area = '' 


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():									#//
        										#//
  #___________________									#//
  def __init__(self,option,var,y1,y2,compa,lat_min,period,area):				#//
     self.max_depth = 1000	                                                        #//
     if period=='2100_2200':
       self.first_year = 2100
     elif period=='2000_2100':
       self.first_year = 2000
     elif period=='2200_2300':
       self.first_year = 2200

     self.y1 = y1 	                                                                #//
     self.y2 = y2
     sufix = str(self.y1)+'to'+str(self.y2)+'_'+str(lat_min)+'_'+str(option)

     if compa == 'no':									#//
        self.output_file = str(var)+'_'+str(sufix)+str(period)

     #self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/2300/'+str(period)+'/section_FSBSO.nc' \
     #self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/2300/'+str(period)+'/sectionW.nc' \
     if area !='':
        self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/2300/'+str(period)+'/section'+str(area)+'.nc' 

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = -1                                                                   #//
        self.vmax = 2.6                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -1.08                                                               #//
        self.vmax = 0.15	                                                        #//

     elif compa =='no':
       if var == 'temp':                                                                #//
           self.vmin = 0
           self.vmax = 7

       elif var == 'sal':                                                               #//
          self.vmin = 32
          self.vmax = 35                                                        #//
       elif var == 'density':                                                                #//
        self.vmin = 20.                                                               #//
        self.vmax = 27.5                                                                 #//
       elif var == 'Uorth':                                                                #//
        self.vmin = -7                                                              #//
        self.vmax = 7                                                                 #//

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////


simuW = From1950to2100(option,var,y1,y2,comparison,lat_min,period,'W') 
yr, xr, time, depthW, XW = loading.extracting_coord_1D(simuW.path)

VARW = loading.extracting_var(simuW.path, var)

S = loading.extracting_var(simuW.path,'sal')
VARW[ S==0 ] = np.nan

simuE = From1950to2100(option,var,y1,y2,comparison,lat_min,period,'E') 
yr, xr, time, depthE, XE = loading.extracting_coord_1D(simuE.path)

VARE = loading.extracting_var(simuE.path, var)

S = loading.extracting_var(simuE.path,'sal')
VARE[ S==0 ] = np.nan

#make_plot.points_on_map(xr,yr,var,area)

index_y1 = np.min(np.where(simuW.first_year+time[:]/(3600*24*364.5)>simuW.y1))
#index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))'''
if var=='Uorth':
  make_plot.one_sec_greenwich(100*np.nanmean(VARW[:,:,index_y1:index_y1+10],axis=2).transpose(),100*np.nanmean(VARE[:,:,index_y1:index_y1+10],axis=2).transpose(),var,XW,XE,depthW,simuW.max_depth,y1,simuW.output_file,simuW.vmin,simuW.vmax,'FSBSO')
else:
  make_plot.one_sec_greenwich(np.nanmean(VARW[:,:,index_y1:index_y1+10],axis=2).transpose(),np.nanmean(VARE[:,:,index_y1:index_y1+10],axis=2).transpose(),var,XW,XE,depthW,simuW.max_depth,y1,simuW.output_file,simuW.vmin,simuW.vmax,'FSBSO')
#make_plot.one_sec(100*np.mean(VAR[:,:,index_y1:index_y2],axis=2).transpose(),var,X,depth,simu.max_depth,y1,simu.output_file,simu.vmin,simu.vmax,'FSBSO')
#make_plot.one_sec(100*VARW[:,:,0].transpose(),var,XW,depthW,simuW.max_depth,y1,simuW.output_file,simuW.vmin,simuW.vmax,'FSBSO')
#make_plot.one_sec_greenwich(100*VARW[:,:,0].transpose(),100*VARE[:,:,0].transpose(),var,XW,XE,depthW,simuW.max_depth,y1,simuW.output_file,simuW.vmin,simuW.vmax,'FSBSO')
