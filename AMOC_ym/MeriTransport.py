#from  mpl_toolkits.basemap import Basemap
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

#import make_plot
import loading
import gsw

var = 'AMOC'
option = 'Coupled'
y1 = 1950
y2 = 2100

comparison = 'no'
y1_compa = 1950
y2_compa = 2000


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():									#//
        										#//
  #___________________									#//
  def __init__(self,option,var,y1,y2,compa):						#//
     self.max_depth = 1000	                                                        #//
     self.first_year = 1950
     self.y1 = y1 	                                                                #//
     self.y2 = y2									#//
     if compa == 'no':									#//
        self.output_file = str(var)+'_'+str(self.y1)+'to'\
                           +str(self.y2)+'_'+str(option)				#//
     elif compa == 'yes':
        self.output_file = str(var)+'_Anomaly_'+str(self.y1)+'to'\
                           +str(self.y2)+'_'+str(option)				#//
     self.path = '/media/fig010/LACIE SHARE/EC_Earth/EC_data/V_AtlSection_YearlyMeans_'+str(option)+'.nc' 

     if compa == 'yes':
      if var == 'temp':                                                                 #//
        self.vmin = 0                                                                   #//
        self.vmax = 3.8                                                                 #//
      elif var == 'sal':                                                                #//
        self.vmin = -1.08                                                               #//
        self.vmax = 0.15	                                                        #//

     elif compa =='no':
      if y2<2010:
       if var == 'temp':                                                                #//
        self.vmin = -1.23                                                               #//
        self.vmax = -0.04                                                               #//
       elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86	                                                        #//
      elif y1>1999:
       if var == 'temp':                                                                #//
        self.vmin = -0.9                                                                #//
        self.vmax = 2.8                                                                 #//
       elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86	                                                        #//
      else:
       if var == 'temp':                                                                #//
        self.vmin = -1.2                                                                #//
        self.vmax = 2.5                                                                 #//
       elif var == 'sal':                                                               #//
        self.vmin = 31.92                                                               #//
        self.vmax = 34.86	                                                        #//

     return										#//
#//////////////////////////////////////////////////////////////////////////////////////////

def V_zonal_mean_one_depth(xr,yr,depth,v):
   p = gsw.p_from_z(-depth,yr[0])
   nx = np.size(xr)
   V = np.zeros((nx))
   for i in range(0,nx-1):
    if xr[i]>270 or xr[i]<90:
     d = gsw.distance([xr[i],xr[i+1]],[yr[i],yr[i+1]],[p,p])
     if v[i]==0 or v[i+1]==0:
        V[i] = np.nan
     else:
        V[i] = d*(v[i]+v[i+1])/2
    else:
     V[i] = np.nan
   return np.nansum(V)

 # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
year = 2000


simu = From1950to2100(option,var,y1,y2,comparison) 
yr, xr, time, depth = loading.extracting_coord(simu.path,'v')
v = loading.extracting_var(simu.path, 'v')

mask = loading.AtlOcean_mask(v[:,:,:,0],xr,yr)

index_y = np.min(np.where(1950+time[:]/(3600*24*364.5)>year))
ny = np.size(yr[0,:])
nz = np.size(depth)
VT = np.zeros((nz,ny))

for j in range(0,ny):
  for k in range(0,nz):
     VT[k,j] = V_zonal_mean_one_depth(xr[:,j],yr[:,j],depth[k],v[:,j,k,index_y])

def Meridional_section(var,yr,variable_name,z,zmax,year,option,vmin,vmax):

   i_zmax = np.max(np.where(z<zmax))

   plt.figure(figsize=(10,6))
   plt.rc('text', usetex=True)
   plt.rc('font', family='serif')
   fig, ax = plt.subplots()
   plt.contourf(yr,z[0:i_zmax+1],var[0:i_zmax+1,:],40)#,vmin=vmin,vmax=vmax)
   plt.ylim([np.min(z),z[i_zmax]])
   plt.ylabel(r'Depth (m)')
   plt.gca().invert_yaxis()
   # rotate and align the tick labels so they look better
   fig.autofmt_xdate()
   #plt.xticks(tick_locs,tick_lbls)
   cbar = plt.colorbar()
   cbar.ax.get_yaxis().labelpad = 15
   cbar.set_label(r'Meridional transport',fontsize=18)
   plt.title('')
   plt.savefig(str(variable_name)+'/'+str(option)+'.png')
   plt.close(fig)
   return

name_outfile = 'MT'
vmin = 50
vmax = 30
Meridional_section(VT,yr[0,:],'MT',depth,2000,year,name_outfile,vmin,vmax)

'''
index_y1 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y1))
index_y2 = np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>simu.y2))

# JUST ONE TIME SERIE PLOT
if comparison == 'no':
   make_plot.time_serie(mean_Arctic_simu[:,index_y1:index_y2],var,time[index_y1:index_y2],\
                       depth,simu.max_depth,simu.first_year,simu.output_file,simu.vmin,simu.vmax)
else:
   index_y1c =np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>y1_compa))
   index_y2c =np.min(np.where(simu.first_year+time[:]/(3600*24*364.5)>y2_compa))
   np.shape(mean_Arctic_simu[:,index_y1c:index_y2c])
   ref = np.reshape( np.mean(mean_Arctic_simu[:,index_y1c:index_y2c],axis=1) ,[42,1])
   make_plot.time_serie(mean_Arctic_simu[:,index_y1:index_y2]\
                       - ref,var,\
                       time[index_y1:index_y2],depth,simu.max_depth,simu.first_year,\
                       simu.output_file,simu.vmin,simu.vmax)


one_time, depth2, mean_Arctic_ref = time_serie_Arctic(simu.path_ref,var)

nt = np.size(mean_Arctic_simu[0,:])
nz = np.size(mean_Arctic_simu[:,0])

anomaly = np.zeros((nz,nt)) 

for z in range(0,nz):
   anomaly[z,:] = mean_Arctic_simu[z,:] - mean_Arctic_ref[z,0]

make_plot.time_serie(anomaly,var,time,depth,simu.max_depth,simu.first_year,simu.output_file,simu.vmin,simu.vmax)

#make_plot.plot_map(xr,yr,np.mean(T1[:,:,0,-11:-1],axis=2)-T2[:,:,0,0] ,var,'2090-2100','surface',option,'')
#make_plot.vertical_profile(np.mean(T_mean_Arctic1,axis=1),'temp',month,depth,max_depth,year[k1],'')
#make_plot.vertical_profile(np.mean(T_mean_Arctic2,axis=1),'temp',month,depth,max_depth,year[k2],'')'''
