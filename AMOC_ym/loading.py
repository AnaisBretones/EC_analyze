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
  elif variable_name == 'v':
    var = Forder(nc.variables['vomecrty'][:])
  elif variable_name == 'ML':
    var = Forder(nc.variables['somxl010'][:])
  elif variable_name == 'temps':
    var = Forder(nc.variables['sosstsst'][:])
  elif variable_name =='sals':
    var = Forder(nc.variables['sosaline'][:])
  elif variable_name =='IceC':
    var = Forder(nc.variables['soicecov'][:])
  nc.close()
  return var

def extracting_coord_2D(path):
  nc = Dataset(path)
  xr = Forder(nc.variables['nav_lat'][:])
  yr = Forder(nc.variables['nav_lon'][:])
  time = Forder(nc.variables['time_counter'][:])
  nc.close()
  return xr, yr, time

def extracting_coord(path,var):
  nc = Dataset(path)
  xr = Forder(nc.variables['nav_lat'][:])
  yr = Forder(nc.variables['nav_lon'][:])
  time = Forder(nc.variables['time_counter'][:])
  if var == 'v':
    depth = Forder(nc.variables['depthv'][:])
  else:
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

def AtlOcean_mask(salinity,x,y):
  ni = np.size(salinity[:,0,0])
  nj = np.size(salinity[0,:,0])
  nz = np.size(salinity[0,0,:])

  mask = np.zeros_like((salinity))
  mask[salinity != 0] = 1
  mask[ np.where(y<66.3),: ] = 0

  mask2 = np.zeros((ni,nj,nz))
  mask2[ np.where(np.abs(x-(270+105)/2.)<(270-105)/2.),:] = 1
  mask2[ np.where(y>=66.3),:] = 1
 
  mask = mask * mask2

  return mask

