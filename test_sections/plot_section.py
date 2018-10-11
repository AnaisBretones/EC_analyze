import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.basemap import Basemap
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



def Forder(var):
   return np.asfortranarray(var.T,dtype=np.float64)

def extracting_coord_1D(path):
  nc = Dataset(path)
  xr = Forder(nc.variables['nav_lat'][:])
  yr = Forder(nc.variables['nav_lon'][:])
  time = Forder(nc.variables['time_counter'][:])
  depth = Forder(nc.variables['deptht'][:])
  X = Forder(nc.variables['X'][:])
  nc.close()
  return xr, yr, time, depth, X

def points_on_map(xr,yr,variable_name,name):
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=70, lat_1=89.9999, lat_2=50,
            width=1.E7, height=0.9E7)
   x,y = m(xr, yr)

   plt.figure(figsize=(10, 6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   fig, ax = plt.subplots()

   m.drawcoastlines(linewidth=0.5)
   m.fillcontinents(color='0.8')
   m.drawparallels(np.linspace(0, 90, 10))
   m.drawmeridians(np.linspace(-180, 180, 10))
   # Add Colorbar
   cs = m.scatter(x,y,marker='o', color='r',s=1)


   plt.savefig(str(name)+'.png')
   plt.close(fig)
   return

path = '/media/fig010/LACIE SHARE/EC_data/test/section.nc'
name = 'section_CC'

yr, xr, time, depth, X = extracting_coord_1D(path)

points_on_map(xr,yr,var,name)
