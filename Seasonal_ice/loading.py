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

def reading_grid(path):
  nc = Dataset(path)
  var = Forder(nc.variables['Cell_area'][:])
  nc.close()
  return var

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
  elif variable_name =='rho':
    var = Forder(nc.variables['vosigma0'][:])
  elif variable_name =='iicethic':
    var = Forder(nc.variables['iicethic'][:])
  elif variable_name =='brine':
    var = Forder(nc.variables['iocesafl'][:])
  elif variable_name =='saltf':
    var = Forder(nc.variables['sosalflx'][:])
  elif variable_name =='ice_f':
    var = Forder(nc.variables['iiceprod'][:])
  elif variable_name =='ileadfra':
    var = Forder(nc.variables[variable_name][:])
   
  nc.close()
  return var

def extracting_coord_2D(path):
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
  var_region = np.zeros((nz,nt,ni*nj))

  n=0
  for j in range(0,nj):
    for i in range(0,ni):
       if yr[i,j]>lat_min and yr[i,j]<lat_max:
          var_region[:,:,n] = var[i,j,:,:]
          n = n+1
  return var_region[:,:,0:n-1]

def regional_subset_2D(var,yr,lat_min,lat_max):
  ni = np.size(var[:,0,0])
  nj = np.size(var[0,:,0])
  nt = np.size(var[0,0,:])
  var_region = np.zeros((nt,ni*nj))

  n=0
  for j in range(0,nj):
    for i in range(0,ni):
       if yr[i,j]>lat_min and yr[i,j]<lat_max:
          var_region[:,n] = var[i,j,:]
          n = n+1
  
  return var_region[:,0:n-1]

# ._._._._._._._._._._._._._._._._._._._._._._._._._._._.

def latitudinal_band_mask(y,lat_min,lat_max):
  mask = ((y>lat_min) & (y<lat_max))
  return mask

def land_mask(salinity):
  mask = salinity != 0
  return mask

def Ocean_mask(x,y,basin):
  if basin == 'arctic_ocean':
     mask = (y>81) | ((y>66.3) & ((x>105)|(x<-90) )) 
  elif basin == 'BS_and_KS':
     mask = ((y<80)&(y>68)&(x<105)&(x>20))
  elif basin == 'greenland_sea':
     mask = ( (y<80) & (((y>65)&(x>-25)&(x<-15)) | ((y>76)&(x>0)&(x<20)) | ((x>-15)&(x<0)&(y>76+11*x/15.))))
  elif basin == 'section_ESS':
     mask = ((x>140) & (x<150) & (y>75) & (y<80))
  elif basin == 'Siberian_seas':
     mask = ((x>110) & (x<180) & (y>60) & (y<85-5*(x-110)/(180-110.)))
  return mask


def extract_sea_ice_ext(y1,y2,month,basin,option,deg):
   #if basin=='undefined':
   txt_file = '/media/fig010/LACIE SHARE/EC_data/'+str(month)+str(y1)+'-'+str(y2)+'/sea_ice_extent_'+str(basin)+'_'+str(deg)+str(option)+'.txt'
   #else:
   #  txt_file = '/media/fig010/LACIE SHARE/EC_data/'+str(month)+str(y1)+'-'+str(y2)+'/sea_ice_extent_'+str(basin)+'.txt'

   ice_ext_array = np.zeros((y2-y1))
   with open(txt_file, "r") as f:
     tab = []
     for line in range(0,y2-y1-1):
         tab.append(f.readline().split())
     ice_ext = np.array([float(x[0]) for x in tab])
     for i in range(0,y2-y1-1):
       ice_ext_array[i] = str(ice_ext[i])
   return ice_ext_array


def extract_sea_ice_ext_ALL(y1,y2,month,basin):
   txt_file = '/media/fig010/LACIE SHARE/EC_data/monthly'+str(y1)+'-'+str(y2)+'/sea_ice_extent_'+str(basin)+'.txt'
   txt_file2 = '/media/fig010/LACIE SHARE/EC_data/monthly'+str(y1)+'-'+str(y2)+'/time_'+str(basin)+'.txt'
   ice_ext_array = np.zeros((y2-y1-1))
   time_array = np.zeros((y2-y1-1))

   with open(txt_file, "r") as f:
     tab = []
     for line in range(0,y2-y1-1):
         tab.append(f.readline().split())
     ice_ext = np.array([float(x[0]) for x in tab])

   with open(txt_file2, "r") as f2:
     tab2 = []
     for line in range(0,y2-y1-1):
         tab2.append(f2.readline().split())
     time = np.array([float(x[0]) for x in tab2])

   for i in range(0,y2-y1-1):
       ice_ext_array[i] = str(ice_ext[i])
       time_array[i] = str(time[i])

   return ice_ext_array,time



