#from  mpl_toolkits.basemap import Basemap
import mpl_toolkits
import matplotlib.pyplot as py
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec
import scipy
import netCDF4
import gsw 

from pylab import *
from netCDF4 import Dataset

from scipy.interpolate import Rbf
import os
import sys
import numpy as np

#import make_plot
import loading

option = 'coupled'
year = 2100
comparison = 'no'


#//////////////////////////////////////////////////////////////////////////////////////////
class yearly_LongPeriod():                                                               #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var):                                                      #//
      self.first_year = 1950                                                            #//
      self.last_year = 2100
      self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/PISMhis_1950_yearly.nc'
      #self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/classic_yearlyMeans_'\
      #            +str(option)+'.nc'                                                    #//
      self.max_depth = 1000                                                             #//
      if var == 'temp':                                                                 #//
        self.vmin = -5                                                                  #//
        self.vmax = 10                                                                  #//
      elif var == 'sal':                                                                #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
      elif var == 'ML':
        self.vmin = 0
        self.vmax = 300
      self.output_file = str(var)+'_ymeans_'+str(option)                                #//
                                                                                        #//
      return                                                                            #//
                                                                                        #//
#//////////////////////////////////////////////////////////////////////////////////////////

#//////////////////////////////////////////////////////////////////////////////////////////
class yearlyAnomaly_LongPeriod():                                                       #//
                                                                                        #//
  #_____________________________________                                                #//
  def __init__(self, option, var):                                                      #//
      self.first_year = 1950                                                            #//
      self.last_year = 2100
      self.path_ref = '../'+str(var)+'TimeMean_'+str(option)+'.nc'                      #//
      self.path = '../'+str(var)+'_from'+str(self.first_year)+'to'\
                  +str(self.last_year)+'_'+str(option)+'.nc'                            #//
      self.max_depth = 1000                                                             #//
      if var == 'temp':                                                                 #//
        self.vmin = -5                                                                  #//
        self.vmax = 10                                                                  #//
      elif var == 'sal':                                                                #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86                                                               #//
      elif var == 'ML':
        self.vmin = 0
        self.vmax = 300
      self.output_file = str(var)+'_ymeans_'+str(option)                                #//
                                                                                        #//
      return                                                                            #//
                                                                                        #//
#//////////////////////////////////////////////////////////////////////////////////////////



if comparison == 'no':
   simu = yearly_LongPeriod(option,'ML')
elif comparison == 'yes':
   simu = yearlyAnomaly_LongPeriod(option,var)
   VarArray_ref = loading.extracting_var(simu.path_ref, var)

yr, xr, time, depth = loading.extracting_coord(simu.path)

VarArray_simuT = loading.extracting_var(simu.path, 'temp')
VarArray_simuS = loading.extracting_var(simu.path, 'sal')

p = gsw.p_from_z(-depth,90)
ni = np.size(VarArray_simuT[:,0,0,0])
nj = np.size(VarArray_simuT[0,:,0,0])
nz = np.size(VarArray_simuT[0,0,:,0])
SA = np.zeros((ni,nj,nz))
CT = np.zeros((ni,nj,nz))
rho = np.zeros((ni,nj,nz))
ML = np.zeros((ni,nj))

for i in range(0,10):#ni):
  for j in range(0,10):#nj):
    SA[i,j,:] = gsw.SA_from_SP(VarArray_simuS[i,j,:,0],p,xr[i,j],yr[i,j])
    CT[i,j,:] = gsw.CT_from_t(SA[i,j],VarArray_simuT[i,j,:,0],p)
    rho[i,j,:] = gsw.rho(SA[i,j,:],CT[i,j,:],p)
    a=np.where(rho[i,j,:]-rho[i,j,0]>0.03)
    if np.size(a) != 0:
       print(np.min(a))
    #ML[i,j] = np.min(np.where(rho[i,j,:]-rho[i,j,0]>30))
'''
if comparison == 'no':
   index_y = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>year))
   make_plot.plot_map(xr,yr,VarArray_sim[:,:,index_y] ,var,year,'mean',simu.output_file,simu.vmin,simu.vmax)
elif comparison == 'yes':
   make_plot.plot_map(xr,yr,np.mean(VarArray_sim[:,:,0,-11:-1],axis=2)-VarArray_ref[:,:,0,0] ,var,'2090-2100','surface',simu.output_file,simu.vmin,simu.vmax)
'''
