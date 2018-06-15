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

def find_right_path(year,model,number,file_type):
  if year>2006:
     scenario = 'DR8'
  else:
     scenario = 'DHI'
  path = 'data/'+str(scenario)+str(number)+'_'+str(model)+'_'+str(year)+'/'+str(model)+'_MM_'+str(year)+'_'+str(file_type)
  return path

def extracting_var(path, variable_name):
  nc = Dataset(path)
  print(nc.variables.keys())
  if variable_name == 'temp':
    var = Forder(nc.variables['votemper'][:])
  elif variable_name =='sal':
    var = Forder(nc.variables['vosaline'][:])
  elif variable_name == 'ice':
    var = Forder(nc.variables['iicethic'][:])
  elif variable_name == 'u':
    var = Forder(nc.variables['vozocrtx'][:])
    #var = Forder(nc.variables['vozoeivu'][:])
  elif variable_name == 'v':
    var = Forder(nc.variables['vomecrty'][:])
  elif variable_name == 'ML':
    var = Forder(nc.variables['somxl010'][:])
  nc.close()
  return var

def extracting_coord2(path):
  nc = Dataset(path)
  xr = Forder(nc.variables['nav_lat'][:])
  yr = Forder(nc.variables['nav_lon'][:])
  time = Forder(nc.variables['time_counter'][:])
  nc.close()
  return xr, yr, time

def extracting_coord(path):
  nc = Dataset(path)
  xr = Forder(nc.variables['nav_lat'][:])
  yr = Forder(nc.variables['nav_lon'][:])
  time = Forder(nc.variables['time_counter'][:])
  depth = Forder(nc.variables['deptht'][:])
  nc.close()
  return xr, yr, time, depth

def extracting_coord_only(path):
  nc = Dataset(path)
  xr = Forder(nc.variables['nav_lat'][:])
  yr = Forder(nc.variables['nav_lon'][:])
  nc.close()
  return xr, yr


def regional_subset(var,yr,lat_min,lat_max):
  ni = np.size(var[:,0,0,0])
  nj = np.size(var[0,:,0,0])
  nt = np.size(var[0,0,0,:])
  nz = np.size(var[0,0,:,0])
  var_region = np.zeros((nz,nt,np.size(var[:,:,0,0])))
  n=0
  for j in range(0,nj):
    for i in range(0,ni):
       if yr[i,j]>lat_min and yr[i,j]<lat_max:
          var_region[:,:,n] = var[i,j,:,:]
          n = n+1
  print(n)
  return var_region[:,:,0:n-1]


'''
month = 'sept'
max_depth = 250
layer = 's'
z = 0

months = ['jan','feb','march','apr','mai','june','july','aug','sept','oct','nov','dec']
i_month = months.index(month)



model = 'ORCA1'
scenario = 'DHI'
number = 'n01'
year = np.arange(1850,2101,1)

file_T = 'grid_T.nc'

k=-1
path = find_right_path(year[k], model,number, 'icemod.nc')
ice = extracting_var(path, 'ice')  
yr, xr = extracting_coord_only(path)

make_plot.plot_map(xr,yr,ice[:,:,i_month],'ice',year[k],month,layer,'yes')
k=0

path = find_right_path(year[k], model, number,file_T)
yr, xr, time, depth = extracting_coord(path)



for reading_file in range(0,2):

  path = find_right_path(year[k], model, number,file_T)
  T = extracting_var(path, 'temp')
  S = extracting_var(path, 'sal')  

  
  #make_plot.plot_map(xr,yr,S[:,:,0,0],'sal',year[k],'jan')
  #make_plot.plot_map(xr,yr,np.mean(T[:,:,:,0],axis=2),'temp',year[k],'jan')

  nt = np.size(T[0,0,0,:])
  nz = np.size(T[0,0,:,0])
  narctic = int(np.size(np.where(yr>66.34)[0]))
  print narctic
  T_Arctic = np.zeros((nz,nt,narctic))
  S_Arctic = np.zeros((nz,nt,narctic))
  n = 0
  S[np.where(S==0)] = np.nan
  T[np.where(T==0)] = np.nan
  for j in range(0,np.size(yr[0,:])):
    for i in range(0,np.size(yr[:,0])):
       if yr[i,j]>66.34:
          T_Arctic[:,:,n] = T[i,j,:,:]
          S_Arctic[:,:,n] = S[i,j,:,:]  
          n = n+1
 
  T_mean_Arctic = np.zeros((nz,nt))
  S_mean_Arctic = np.zeros((nz,nt))
  for t in range(0,nt):
      for z in range(0,nz):
         T_mean_Arctic[z,t] = T_Arctic[z,t,~np.isnan(T_Arctic[z,t,:])].mean()
         S_mean_Arctic[z,t] = S_Arctic[z,t,~np.isnan(S_Arctic[z,t,:])].mean()
  
  make_plot.time_serie(T_mean_Arctic,'temp',time,depth,year[k])
  make_plot.time_serie(S_mean_Arctic,'sal',time,depth,year[k])
  
  k=-1
'''  
