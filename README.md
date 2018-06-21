# EC-Earth analysis 
This repository aims: 
- to store bash and python scripts, used to read EC-Earth outputs
- to display the plots resulting from the aforementionned scripts
- to keep track of what I have done so far and what I am working on now
It is divided into folders corresponding to different subset of data, hence different goals.
ex: **EC\_start** works with temperature, salinity, MLD and sea ice cover, -yearly means in the NH

Each folders contains one bash script (the script that was used to exctract the subset of data), 
a certain number of python scripts, and folders named after the studied variables containing plots.
Ex: **EC\_start** contains the folder **temp**, **sal**, **IceC**, **MLD**

## About the different subsets:

### **EC\_start**
data: yearly means from 1950 to 2100, y>15°N. Temperature (temp), salinity (sal), ice cover (IceC),
mixed layer depth (MLD)
plots: time series from 2000 to 2100 and time serie anomalies WRT 90s + 10y mean maps and anomalies


### **AMOC\_yearly**

###

## How to reproduce the plots
1. Download this repository
Create the folder **EC\_Earth** 
```
cd EC_Earth
git clone git@github.com:AnaisBretones/EC_analysis.git
``` 
Create the folder **EC\_data** where you will store the data. 
 
2. Download the data
To do so, you need to have access to nird, and more specifically to the project NS4659K. If it is not the
case yet, you can apply [here](https://www.metacenter.no/user/application/form/norstore/).
```
scp "username" @login.nird.sigma2.no:/nird/projects/NS4659K/anais/cdo_work/ "name_of_subset" /*.nc ~/Desktop/EC_Earth/EC_data
```


## Creating a new subset
Log in to nird:
```
ssh "username" @login.nird.sigma2.no
```
Open the folder **cdo\_work**:
```
 cd /nird/projects/NS4659K/anais/cdo_work
```
The compressed data (one folder per year containing 5 files with montlhy values for different variables) are
stored in **anais/EC\_data**. You can edit a new bash script, run it ($bash your\_script) and copy the resulting
netCDF file to your computer.
