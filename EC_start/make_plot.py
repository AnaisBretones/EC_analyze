import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.basemap import Basemap
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors

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

def points_on_map(xr,yr,variable_name,ocean):
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=70, lat_1=89.99999, lat_2=50,
            width=1.E7, height=0.9E7)
   #m = Basemap(projection='ortho',lat_0=60,lon_0=-20,resolution='l')
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


   plt.title(str(ocean.replace("_"," ")),size=20)
   plt.savefig(str(variable_name)+'/domain_'+str(ocean)+'.png')
   plt.close(fig)
   return



def plot_map(xr,yr,variable,variable_name,title,option,vmin,vmax):
   # map all Atlantic and Arctic Ocean
   # colorbar under the map: 
   # Ice thickness, Temperature or Salinity
   # year: age of the data
   # time: month? yearly mean? 
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=90, lat_1=89.999999, lat_2=50,
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
   elif variable_name=='IceC':
      cbar.ax.set_xlabel('Ice cover (concentration)')
   

   plt.title(str(title),size=20)
   plt.savefig(str(variable_name)+'/'+str(option.replace(".",""))+'.png')
   plt.close(fig)
   return

def map_velocity(xr,yr,u,v,variable_name,title,option,name_file):
   # map all Atlantic and Arctic Ocean
   # colorbar under the map: 
   # Ice thickness, Temperature or Salinity
   # year: age of the data
   # time: month? yearly mean? 
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=90, lat_1=89.999, lat_2=50,
            width=0.4E7, height=0.4E7)
 
   x,y = m(xr, yr)

   plt.figure(figsize=(10, 6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   fig, ax = plt.subplots()

   m.drawcoastlines(linewidth=0.5)
   m.fillcontinents(color='0.8')

   yy = np.arange(0, y.shape[0], 4)
   xx = np.arange(0, x.shape[1], 4)

   points = np.meshgrid(yy, xx)
   speed = np.sqrt(u**2 + v**2)
   m.quiver(x[points], y[points],\
    u[points], v[points], speed[points],\
    cmap=plt.cm.autumn, scale=1)

   plt.savefig(str(variable_name)+'/'+str(name_file.replace(".",""))+'.png')
   plt.close(fig)
   return

   
def vertical_profile(var1,var2,variable_name,vmin,vmax,z,zmax,ocean,lat_min,name_file):

   i_zmax = np.max(np.where(z<zmax))
   fig = plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   plt.plot(var1[0:i_zmax+1],z[0:i_zmax+1])
   plt.plot(var2[0:i_zmax+1],z[0:i_zmax+1])
   plt.gca().invert_yaxis()
   plt.ylabel(r'Depth (m)')
   if variable_name == 'temp':
     plt.xlabel(r'Temperature ($^{o}$C)')
   elif variable_name == 'density':
     plt.xlabel(r'Density')
   plt.xlim([vmin,vmax])
   if ocean == 'BS_and_KS':
      plt.ylim([420,0])
   else:
      plt.ylim([z[i_zmax],0])
   plt.title(str(ocean.replace("_"," ")))
   if ocean == 'undefined':
      plt.title('Mean Arctic ($>$'+str(lat_min)+'$^{o}$N)')
   else:
      plt.title(str(ocean.replace("_"," ")))
   plt.savefig(str(variable_name)+'/'+str(name_file.replace(".",""))+'.png')
   plt.close(fig)
   return

def vertical_profile3(var1,var2,var3,y1,y2,variable_name,vmin,vmax,z,zmax,ocean,lat_min,name_file):

   i_zmax = np.max(np.where(z<zmax))
   plt.figure(figsize=(7,15))
   fig,ax = plt.subplots()
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   ax.plot(var1[0:i_zmax+1],z[0:i_zmax+1],label=str(y1))
   ax.plot(var2[0:i_zmax+1],z[0:i_zmax+1],color='grey')
   ax.plot(var3[0:i_zmax+1],z[0:i_zmax+1],color='grey')
   '''
   ax.fill_between(z[0:i_zmax+1],var3[0:i_zmax+1], var2[0:i_zmax+1], color = 'lightgrey',label = 'standard error')
   lineA,=ax.plot(var1[0:i_zmax+1],z[0:i_zmax+1],linewidth=2.5, color='darkslategray',label=str(lat_min))
   blue_patch = patches.Patch(color='lightgrey', label='standard error')
   ax.legend(handles = [lineA, blue_patch], \
          prop={'size':11},bbox_to_anchor=(1.1, 1.05))
   '''
   plt.gca().invert_yaxis()
   plt.ylabel(r'Depth (m)')
   if variable_name == 'temp':
     plt.xlabel(r'Temperature ($^{o}$C)')
   elif variable_name == 'density':
     plt.xlabel(r'Density')
   plt.xlim([vmin,vmax])
   plt.ylim([z[i_zmax],0])
   plt.title(str(ocean.replace("_"," ")))
   if ocean == 'undefined':
      plt.title('Arctic mediterranean seas ($>$'+str(lat_min)+'$^{o}$N)')
   else:
      plt.title(str(ocean.replace("_"," ")))
   plt.savefig(str(variable_name)+'/'+str(name_file.replace(".",""))+'.png')
   plt.close(fig)
   return



def time_serie(var,variable_name,t,ML,z,zmax,year,option,vmin,vmax,ocean):

   i_zmax = np.max(np.where(z<zmax))

   plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   fig, ax = plt.subplots()
   if variable_name == 'temp':
      plt.contourf(year+t/(24*3600*365.),z[0:i_zmax+1],var[0:i_zmax+1,:],40,vmin=vmin,vmax=vmax)
   elif variable_name == 'sal':
      plt.contourf(year+t/(24*3600*365.),z[0:i_zmax+1],var[0:i_zmax+1,:],40,vmin=vmin,vmax=vmax)#,vmin=31.76,vmax=34.02)
   plt.plot(year+t/(24*3600*365.),ML)

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

   if ocean == 'undefined':
      plt.title('Mean Arctic ($>$66.34$^{o}$N)')
   else:
      plt.title(str(ocean.replace("_"," ")),size=20)

   plt.savefig(str(variable_name)+'/'+str(option.replace(".",""))+'.png')
   plt.close(fig)
   return


def time_serie_two_axis(var,variable_name,t,ice_ext,z,zmax,year,option,vmin,vmax,ocean):

   i_zmax = np.max(np.where(z<zmax))

   fig = plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   ax1 = fig.add_subplot(111)
   #fig, ax1 = plt.subplots()
   if variable_name == 'temp':
      mappable = ax1.contourf(year+t/(24*3600*365.),z[0:i_zmax+1],var[0:i_zmax+1,:],40,vmin=vmin,vmax=vmax)
   elif variable_name == 'sal':
      mappable = ax1.contourf(year+t/(24*3600*365.),z[0:i_zmax+1],var[0:i_zmax+1,:],40,vmin=vmin,vmax=vmax)#,vmin=31.76,vmax=34.02)
   elif variable_name == 'BruntVF':
      mappable = ax1.contourf(year+t/(24*3600*365.),z[0:i_zmax+1],var[0:i_zmax+1,:],40)#,vmin=31.76,vmax=34.02)
   if ocean == 'BS_and_KS':
      plt.ylim([np.min(z),420])
   else:
      plt.ylim([np.min(z),z[i_zmax]])
   plt.ylabel(r'Depth (m)')
   plt.gca().invert_yaxis()
   cbar = fig.colorbar(mappable, pad=0.15)
   if variable_name == 'temp':
    cbar.set_label(r'Temperature ($^{o}$C)',fontsize=18)
   elif variable_name == 'sal':
    cbar.set_label(r'Salinity (PSU)',fontsize=18)
   elif variable_name == 'BruntVF':
    cbar.set_label(r'Brunt Vaisala frequency',fontsize=18)
    cbar.formatter.set_powerlimits((0, 0))
    cbar.update_ticks()   
   ax2 = ax1.twinx()
   ax2.plot(year+t/(24*3600*365.),ice_ext,linewidth=3,color="black")

   plt.ylabel(r'Sea ice extent (m$^{2}$)',fontsize=18)
   # rotate and align the tick labels so they look better
   fig.autofmt_xdate()
   #plt.xticks(tick_locs,tick_lbls)
   plt.xlim([np.min(year+t[0]/(24*3600*365.)), np.max(year+t[-1]/(24*3600*365.)) ])
   if ocean == 'undefined':
      plt.title('Mean Arctic ($>$66.34$^{o}$N)')
   else:
      plt.title(str(ocean.replace("_"," ")),size=20)

   plt.savefig(str(variable_name)+'/'+str(option.replace(".",""))+'.png')
   plt.close(fig)
   return


def var_fc_time(var,variable_name,t,first_year_file,lat_min,name_outfile,ocean):
  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  t = t/(3600*24*365.)
  plt.xlim([first_year_file+np.min(t),first_year_file+np.max(t)])
  plt.ylim([0.,0.75])
  if variable_name == 'IceC':
     plt.plot(first_year_file+t,var)
     plt.ylabel('Ice cover',fontsize=18)
  plt.xlabel('time',fontsize=18)
  if ocean == 'undefined':
      plt.title('Mean Arctic ($>$'+str(lat_min)+'$^{o}$N)')
  else:
      plt.title(str(ocean.replace("_"," ")),size=20)
  plt.savefig(str(variable_name)+'/'+str(name_outfile.replace(".",""))+'.png')
  return




