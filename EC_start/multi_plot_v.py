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

var = 'velocity'
option = 'Coupled'
specificity = ''
y1 = 2000
y2 = 2030

comparison = 'no'

title_plot =  str(specificity)+' '+str(y1)+' to '+str(y2)

#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,specificity,var,y1,y2,compa):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1 = y1                                                                       #//
     self.y2 = y2                                                                       #//
     self.y1_compa = 1950
     self.y2_compa = 2000
     self.output_file = 'multimaps_'+str(self.y1)+'to'+str(self.y2)+'_'+str(option)   #//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/section/vita_'+str(option)+'.nc'




#months = ['jan','feb','mars','apr','mai','june','july','aug','sept','oct','nov','dec']
#i_month = months.index(month)


m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=90, lat_1=89.999, lat_2=50,
            width=0.4E7, height=0.4E7)

fig = plt.figure(figsize=(10, 6))
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


fig.subplots_adjust(hspace=0.2, wspace=0.0001)

for i in range(1,2):
   y1 = y1+1
   ax = plt.subplot(3, 4, 1)
   ax.set_title(str(y1),color='r')
   title_plot =  str(specificity)+' '+str(y1)+' to '+str(y1+1)

   simu = From1950to2100(option,specificity,var,y1,y2,comparison)
   
   yr, xr, time, depth = loading.extracting_coord(simu.path)
   
   x,y = m(xr, yr)
   m.drawcoastlines(linewidth=0.5)
   m.fillcontinents(color='0.8')
   
   U = loading.extracting_var(simu.path, 'sovitua')
   '''V = loading.extracting_var(simu.path, 'sovitva')
   
   index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
   yy = np.arange(0, y.shape[0], 4)
   xx = np.arange(0, x.shape[1], 4)
   
   u = U[:,:,0,index_y1]
   v = V[:,:,0,index_y1]
   points = np.meshgrid(yy, xx)
   speed = np.sqrt(u*u + v**2)
   cs = m.quiver(x[points], y[points],\
    u[points], v[points], speed[points],\
    cmap=plt.cm.autumn, scale=1)
   '''
plt.savefig(str(var)+'/'+str(simu.output_file.replace(".",""))+'.png')
plt.close(fig)                                                                                                


