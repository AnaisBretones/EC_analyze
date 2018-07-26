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
y1 = 2020#+140
y2 = y1+12

month = 'Sept'
comparison = 'yes'

output_file = str(var)+str(month)+'_plaquette_'+str(y1)+'To'+str(y2)+'_'+str(option)                                #//

#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,specificity,var,y1,y2,compa,month):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1 = y1                                                                       #//
     self.y2 = y2                                                                       #//
     self.y1_compa = y1+1
     self.y2_compa = 2042
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/'+str(month)+'_Ice_'+str(option)+'.nc'

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
        self.vmin = -1.2                                                               #//
        self.vmax = 15                                                               #//
      elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////

m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=85, lat_1=89.999, lat_2=50,
            width=1.E7, height=0.9E7)
   #m = Basemap(projection='ortho',lat_0=60,lon_0=-20,resolution='l')

fig = plt.figure(figsize=(10, 6))
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


fig.subplots_adjust(hspace=0.2, wspace=0.000001)

for i in range(1,13):
   y1 = y1+1   
   ax = plt.subplot(3, 4, i)
   ax.set_title(str(y1),color='r')
   title_plot =  str(specificity)+' '+str(y1)+' to '+str(y1+1)

   simu = From1950to2100(option,specificity,var,y1,y2,comparison,month)
   
   yr, xr, time = loading.extracting_coord_2D(simu.path)
   
   x,y = m(xr, yr)
   m.drawcoastlines(linewidth=0.5)
   m.fillcontinents(color='0.8')
   
   VarArray_simu = loading.extracting_var(simu.path, var)
   
   index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
   
   
   index_y1c = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1_compa))
   array_to_plot = VarArray_simu[:,:,index_y1c]-VarArray_simu[:,:,index_y1]
   array_to_plot[array_to_plot==0] = np.nan
   array_to_plot = np.ma.masked_invalid(array_to_plot)
   #make_plot.plot_map_with_ice_extent(xr,yr,array_to_plot ,var,VarArray_simu[:,:,index_y1],y1,VarArray_simu[:,:,index_y1c],simu.y1_compa,title_plot,simu.output_file,simu.vmin,simu.vmax)

   cs = m.pcolor(x,y,array_to_plot,vmin=simu.vmin,vmax=simu.vmax)
   cs2=m.contour(x, y, VarArray_simu[:,:,index_y1], [0.15],colors='r')
   cs3=m.contour(x, y, VarArray_simu[:,:,index_y1c], [0.15],colors='b')
plt.savefig(str(var)+'/'+str(output_file)+'.png',format='png')          
