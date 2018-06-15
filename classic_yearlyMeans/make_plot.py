import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
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

def plot_map(xr,yr,variable,variable_name,year,time,option,vmin,vmax):
   # map all Atlantic and Arctic Ocean
   # colorbar under the map: 
   # Ice thickness, Temperature or Salinity
   # year: age of the data
   # time: month? yearly mean? 
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=70, lat_1=89, lat_2=50,
            width=1.E7, height=0.9E7)
   #m = Basemap(projection='ortho',lat_0=60,lon_0=-20,resolution='l')
   x,y = m(xr, yr)

   plt.figure(figsize=(10, 6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   fig, ax = plt.subplots()

   m.drawcoastlines(linewidth=0.5)
   m.fillcontinents(color='0.8')

   # Add Colorbar
   cs = m.pcolor(x,y,variable,vmin=vmin,vmax=vmax)
   cbar = m.colorbar(cs, location='bottom')
   if variable_name=='icet':
      cbar.ax.set_xlabel('Ice Thickness (m)')
   elif variable_name == 'sal':
      cbar.ax.set_xlabel('Salinity (PSU)')
   elif variable_name =='temp':
      cbar.ax.set_xlabel('Temperature ($^{o}$C)')
   elif variable_name=='ML':
      cbar.ax.set_xlabel('Mixed layer depth (m)')


   plt.title(str(year)+','+str(time),size=20)
   plt.savefig(str(variable_name)+'/'+str(option)+'.png')
   plt.close(fig)
   return

def vertical_profile(var,variable_name,t,z,zmax,year,option):

   i_zmax = np.max(np.where(z<zmax))
   fig = plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   plt.plot(var[0:i_zmax+1],z[0:i_zmax+1])
   plt.gca().invert_yaxis()
   plt.ylabel(r'Depth (m)')
   plt.xlabel(r'Temperature ($^{o}$C)')
   plt.title('Mean Arctic ($>$66.34$^{o}$N)')
   plt.savefig(str(variable_name)+'/'+str(option)+'.png')
   plt.close(fig)
   return


def time_serie(var,variable_name,t,z,zmax,year,option,vmin,vmax):

   i_zmax = np.max(np.where(z<zmax))

   plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   fig, ax = plt.subplots()
   if variable_name == 'temp':
      plt.contourf(year+t/(24*3600*365.),z[0:i_zmax+1],var[0:i_zmax+1,:],40,vmin=vmin,vmax=vmax)
   elif variable_name == 'sal':
      plt.contourf(year+t/(24*3600*365.),z[0:i_zmax+1],var[0:i_zmax+1,:],40,vmin=vmin,vmax=vmax)#,vmin=31.76,vmax=34.02)
   plt.ylim([np.min(z),z[i_zmax]])
   plt.ylabel(r'Depth (m)')
   plt.gca().invert_yaxis()
   # rotate and align the tick labels so they look better
   fig.autofmt_xdate()
   #plt.xticks(tick_locs,tick_lbls)
   cbar = plt.colorbar()
   cbar.ax.get_yaxis().labelpad = 15
   if variable_name == 'temp':
    cbar.set_label(r'Temperature ($^{o}$C)',fontsize=18)
   elif variable_name == 'sal':
    cbar.set_label(r'Salinity (PSU)',fontsize=18)
   plt.title('Mean Arctic ($>$66.34$^{o}$N)')
   plt.savefig(str(variable_name)+'/'+str(option)+'.png')
   plt.close(fig)
   return

def time_serie_one_year(var,variable_name,z,t,year):
  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  t = t/(3600*24*365.)
  if variable_name == 'temp':
     plt.pcolor(t,z,var,vmin=vmin,vmax=vmax,cmap='RdBu')#,vmin=np.min(var),vmax=np.max(var))
  elif variable_name == 'sal':
     plt.pcolormesh(t,z,var,vmin=33.66,vmax=34.50)#,cmap='YlGnBu')

  plt.ylim([np.min(z),600])
  plt.xlim([t[0],t[-1]])
  tick_locs = [t[1],t[3],t[5],t[7]]
  tick_lbls = ['feb','ap','jun','aug']
  plt.xticks(tick_locs,tick_lbls)
  plt.gca().invert_yaxis()

  cbar = plt.colorbar()
  if variable_name == 'temp':
    cbar.set_label(r'Temperature ($^{o}$C)',fontsize=18)
  elif variable_name == 'sal':
    cbar.set_label(r'Salinity (PSU)',fontsize=18)
  plt.title('Mean Arctic',fontsize=20)
  plt.xlabel(r'time',fontsize=18)
  plt.ylabel(r'depth',fontsize=18)
  plt.savefig('plots/'+str(variable_name)+'/Arctic_'+str(variable_name)+'_'+str(year)+'.png')
  plt.close(fig)
  return



'''
model = 'ORCA1'
scenario = 'DHI'
number = 'n01'
year = np.arange(1850,2101,1)


file_ice = 'icemod.nc'
path = str(scenario)+str(number)+'_'+str(model)+'_'+str(year[0])+'/'+str(model)+'_MM_'+str(year[0])+'_'+str(file_ice)

nc_ice = Dataset(path)
ice = Forder(nc_ice.variables['iicethic'][:])
xr = Forder(nc_ice.variables['nav_lat'][:])
yr = Forder(nc_ice.variables['nav_lon'][:])

nc_ice.close()


file_ice = 'icemod.nc'
scenario = 'DR8'
path = str(scenario)+str(number)+'_'+str(model)+'_'+str(year[-1])+'/'+str(model)+'_MM_'+str(year[-1])+'_'+str(file_ice)

nc_ice = Dataset(path)
ice2 = Forder(nc_ice.variables['iicethic'][:])
xr = Forder(nc_ice.variables['nav_lat'][:])
yr = Forder(nc_ice.variables['nav_lon'][:])

nc_ice.close()




m = Basemap(projection='ortho',lat_0=60,lon_0=-20,resolution='l')
x,y = m(yr,xr)
plot_map(x,y,np.mean(ice,axis=2),'ice',year[0],'yearlymean')

plot_map(x,y,np.mean(ice2,axis=2),'ice',year[-1],'yearlymean')
'''

