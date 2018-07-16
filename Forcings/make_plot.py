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

def points_on_map(xr,yr,variable_name,ocean):
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=70, lat_1=89.999, lat_2=50,
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

def fmt(x, pos):
   a, b = '{:.2e}'.format(x).split('e')
   b = int(b)
   return r'${} \times 10^{{{}}}$'.format(a, b)


def plot_map(xr,yr,variable,variable_name,title,option,vmin,vmax):
   # map all Atlantic and Arctic Ocean
   # colorbar under the map: 
   # Ice thickness, Temperature or Salinity
   # year: age of the data
   # time: month? yearly mean? 
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=90, lat_1=89.9999, lat_2=50,
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
   #cbar.ax.set_yticklabels(['{:.000f}'.format(x) for x in np.arange(vmin, vmax, 5)])
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
   elif variable_name=='MeltedIce':
      cbar.formatter.set_powerlimits((0, 0))
      cbar.update_ticks()
      cbar.ax.set_xlabel('FWF ice to ocean (kg.m$^{-2}$.s$^{-1}$)')
   elif variable_name=='runoff':
      cbar.formatter.set_powerlimits((0, 0))
      cbar.update_ticks()
      cbar.ax.set_xlabel('Runoff (kg.m$^{-2}$.s$^{-1}$)')
    
    

   plt.title(str(title),size=20)
   plt.savefig(str(variable_name)+'/'+str(option.replace(".",""))+'.png')
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
   plt.ylim([z[i_zmax],0])
   plt.title(str(ocean.replace("_"," ")))
   if ocean == 'undefined':
      plt.title('Mean Arctic ($>$'+str(lat_min)+'$^{o}$N)')
   else:
      plt.title(str(ocean.replace("_"," ")))
   plt.savefig(str(variable_name)+'/'+str(name_file.replace(".",""))+'.png')
   plt.close(fig)
   return



def time_serie(var,variable_name,t,z,zmax,year,option,vmin,vmax,ocean):

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

   if ocean == 'undefined':
      plt.title('Mean Arctic ($>$66.34$^{o}$N)')
   else:
      plt.title(str(ocean.replace("_"," ")),size=20)

   plt.savefig(str(variable_name)+'/'+str(option.replace(".",""))+'.png')
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

def var_fc_time(var,variable_name,t,first_year_file,lat_min,name_outfile,ocean):
  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  t = t/(3600*24*365.)
  plt.xlim([first_year_file+np.min(t),first_year_file+np.max(t)])
  #plt.ylim([0.,0.75])
  plt.plot(first_year_file+t,var)
  if variable_name == 'IceC':
     plt.ylabel('Ice cover',fontsize=18)
  plt.xlabel('time',fontsize=18)
  plt.title('basins')
  plt.savefig(str(variable_name)+'/all_basins.png')
  return


def var_fc_time_2(var,var2,variable_name,t,first_year_file,lat_min,name_outfile,ocean):
  plt.figure(figsize=(10,6))
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  fig,ax=plt.subplots()
  t = t/(3600*24*365.)
  plt.xlim([first_year_file+np.min(t),first_year_file+np.max(t)])
  #plt.ylim([0.,0.75])
  plt.plot(first_year_file+t,var, label = 'Uncouled')
  plt.plot(first_year_file+t,var2, label = 'Coupled')
  if variable_name == 'IceC':
     plt.ylabel('Ice cover',fontsize=18)
  plt.xlabel('time',fontsize=18)
  if ocean == 'undefined':
      plt.title('Mean Arctic ($>$'+str(lat_min)+'$^{o}$N)')
  else:
      plt.title(str(ocean.replace("_"," ")),size=20)

  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * 0.3,
                 box.width, box.height * 0.7])
  h, l = ax.get_legend_handles_labels()
  ax.legend(h, l,  bbox_to_anchor=(-.5,-.05, 2,-0.15), loc=9,
           ncol=1)
  plt.savefig(str(variable_name)+'/'+str(name_outfile.replace(".",""))+'.png')
  return


def masks_on_map(variable_name,xr1,yr1,m1, xr2,yr2,m2, xr3,yr3,m3, xr4,yr4,m4, xr5,yr5,m5):
   m = Basemap(projection='lcc', resolution='l',
            lon_0=-20, lat_0=70, lat_1=89.99999999, lat_2=50,
            width=1.E7, height=0.9E7)
   #m = Basemap(projection='ortho',lat_0=60,lon_0=-20,resolution='l')
   x1,y1 = m(xr1, yr1)
   x2,y2 = m(xr2, yr2)
   x3,y3 = m(xr3, yr3)
   x4,y4 = m(xr4, yr4)
   x5,y5 = m(xr5, yr5)

   plt.figure(figsize=(15, 6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   fig, ax = plt.subplots()

   m.drawcoastlines(linewidth=0.5)
   m.fillcontinents(color='0.8')
   m.drawparallels(np.linspace(0, 90, 10))
   m.drawmeridians(np.linspace(-180, 180, 10))
   # Add Colorbar
   cs = m.scatter(x1,y1,marker='o', color='b',s=5, label='Arctic mediterranean')
   cs = m.scatter(x2,y2,marker='o', color='k',s=0.4, label=str(m2.replace("_"," ")))
   cs = m.scatter(x3,y3,marker='o', color='r',s=0.5, label=str(m3.replace("_"," ")))
   cs = m.scatter(x4,y4,marker='o', color='y',s=0.2, label=str(m4.replace("_"," ")))
   cs = m.scatter(x5,y5,marker='o', color='m',s=0.5, label=str(m5.replace("_"," ")))

   box = ax.get_position()
   ax.set_position([box.x0, box.y0 + box.height * 0.15,
                 box.width, box.height * 0.9])
   h, l = ax.get_legend_handles_labels()
   ax.legend(h, l,  bbox_to_anchor=(-.5,0.1, 2,-0.15), loc=9,
           ncol=2)


   plt.title('basins')
   plt.savefig(str(variable_name)+'/all_basins.png')
   plt.close(fig)
   return
