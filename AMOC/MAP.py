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

var = 'moc'
option = 'Coupled'
specificity = ''

y1p = 1950          #first year in the data
y2p = 2100          #last year in the data


#//////////////////////////////////////////////////////////////////////////////////////////
class From1950to2100():                                                                 #//
                                                                                        #//
  #___________________                                                                  #//
  def __init__(self,option,var,y1,y2):                                            #//
     self.max_depth = 1000                                                              #//
     self.first_year = 1950
     self.y1h = 2010 #1950                                                                       #//
     self.y2h = 2020
     self.y1f = 2080 #2090
     self.y2f = 2090                                                                       #//
     self.path = '/media/fig010/LACIE SHARE/EC_data/yearly'+str(y1)+'-'+str(y2)+'/moc.nc'

     #self.path_thickness = '/media/fig010/LACIE SHARE/EC_data/'+str(month)+str(y1)+'-'\
     #                       '2100/icef'+str(month)+'_'+str(y1)+'-2100.nc'
     self.output_fileH = str(var)+'_'+str(self.y1h)+'-'+str(self.y2h)                                #//
     self.output_fileF = str(var)+'_'+str(self.y1f)+'-'+str(self.y2f)                                #//
     self.output_fileC = str(var)+'Anomaly_'+str(self.y1h)+'-'+str(self.y1f)                                #//

     return                                                                             #//
#//////////////////////////////////////////////////////////////////////////////////////////



simu = From1950to2100(option,var,y1p,y2p)
   
yr, xr, time,depth = loading.extracting_coord_moc(simu.path)
time = simu.first_year+time[:]/(3600*24*364.5)
   
moc = loading.extracting_var(simu.path, var)
moc[np.where(moc==0.000)]=np.nan   

index_y1h = np.min(np.where(time>simu.y1h))
   
index_y1f = np.min(np.where(time>simu.y1f))
'''
array_to_plotH = np.nanmean(moc[:,:,0,index_y1h:index_y1h+10],axis=2)
array_to_plotH[array_to_plotH==0] = np.nan
array_to_plotH = np.ma.masked_invalid(array_to_plotH)

array_to_plotF = np.nanmean(moc[:,:,0,index_y1f:index_y1f+10],axis=2)
array_to_plotF[array_to_plotF==0] = np.nan
array_to_plotF = np.ma.masked_invalid(array_to_plotF)

print(np.nanmin(array_to_plotH),np.nanmax(array_to_plotF))
print(array_to_plotH)

make_plot.plot_map_s(xr,yr,array_to_plotH,var,simu.y1h,'',simu.output_fileH)
make_plot.plot_map_s(xr,yr,array_to_plotF,var,simu.y1f,'',simu.output_fileF)
'''
colorbar='undefined'
array_to_plotH = np.nanmean(moc[0,:,:,index_y1h:index_y1h+10],axis=2)
array_to_plotF = np.nanmean(moc[0,:,:,index_y1f:index_y1f+10],axis=2)
X = yr[0,:]
minline=-0.1
maxline=0.1

array_to_plotF = np.ma.masked_invalid(array_to_plotF)
array_to_plotH = np.ma.masked_invalid(array_to_plotH)

#make_plot.one_sec(array_to_plotH.transpose(),var,X,-depth,simu.max_depth,simu.y1h,simu.output_fileH,minline,maxline,str(simu.y1h)+'-'+str(simu.y2h),colorbar)
#make_plot.one_sec(array_to_plotF.transpose(),var,X,-depth,simu.max_depth,simu.y1f,simu.output_fileF,minline,maxline,str(simu.y1f)+'-'+str(simu.y2f),colorbar)
make_plot.one_sec(array_to_plotH.transpose(),array_to_plotF.transpose(),var,X,-depth,simu.max_depth,simu.y1h,simu.output_fileC,minline,maxline,'current and future',colorbar)

