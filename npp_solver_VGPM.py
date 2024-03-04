import datetime
import numpy as np
from netCDF4 import Dataset
import netCDF4
import pandas as pd
import os

####User defined file paths needed, uncomment with appropriate file name
####chl a data folder
#chl_dir = folder path and name
####PAR data folder
#par_dir = folder path and name
####SST data folder
#SST_dir = folder path and name
####Bathymetry data
#bathy_dir = folder path and name
####Day length data
#day_dir = folder path and name
####NPP_out
#npp_dir = folder path and name

####create folder to store solved NPP
if not os.path.exists(npp_dir):
   os.makedirs(npp_dir)

####call in bathymetry
etopodata = Dataset(bathy_dir,'r')
topoin = np.around(etopodata.variables['z'][:],decimals=1,out=None)*(-1)
lon_og = np.around(etopodata.variables['lon'][:],decimals=3,out=None)
lat_og = np.around(etopodata.variables['lat'][:],decimals=3,out=None)
topoin = np.flip(topoin,axis=0)
topoin_df = pd.DataFrame(topoin)

#get file names
chl_files = os.listdir(chl_dir)
for j in chl_files:
    if j[0] == '.':
        chl_files.remove(j)
chl_files = np.sort(chl_files)

#get file names
PAR_files = os.listdir(par_dir)
for j in PAR_files:
    if j[0] == '.':
        PAR_files.remove(j)
PAR_files = np.sort(PAR_files)

#get file names
SST_files = os.listdir(SST_dir)
for j in SST_files:
    if j[0] == '.':
        SST_files.remove(j)
SST_files = np.sort(SST_files)

#get file names
light_files = os.listdir(day_dir)
for j in light_files:
    if j[0] == '.':
        light_files.remove(j)
light_files = np.sort(light_files)

for j in range(0,len(SST_files)):
    SST_full = Dataset(os.path.join(SST_dir,SST_files[j]))
    SST_full_ar = np.array(SST_full.variables['sst'][:][:])
    SST_full_ar = np.where(SST_full_ar < SST_full.data_minimum, np.nan, SST_full_ar)
    SST_full_ar = np.where(SST_full_ar > SST_full.data_maximum, np.nan, SST_full_ar)
    SST_full_df = pd.DataFrame(SST_full_ar)
    SST_full_df = SST_full_df[topoin_df>0]

    pbopt = ((-3.27E-8)*(SST_full_df**7))+((3.4132E-6)*(SST_full_df**6))-((1.348E-4)*(SST_full_df**5))+((2.462E-3)*(SST_full_df**4))-((0.0205)*(SST_full_df**3))+((0.0617)*(SST_full_df**2))+((0.2749)*(SST_full_df))+1.2956
    pbopt_temp = np.where(SST_full_df<-10,0,np.nan)
    pbopt_temp = np.where((SST_full_df<-1)&(SST_full_df>-10),1.13,pbopt_temp)
    pbopt_temp = np.where((SST_full_df>28.5),4,pbopt_temp)
    pbopt_temp = np.where((SST_full_df>-1)&(SST_full_df<28.5),pbopt,pbopt_temp)
    pbopt = pbopt_temp

    chl_full = Dataset(os.path.join(chl_dir,chl_files[j]))
    chl_full_ar = np.array(chl_full.variables['chlor_a'][:][:])
    lat = np.array(chl_full.variables['lat'][:])
    lon = np.array(chl_full.variables['lon'][:])
    chl_full_ar = np.where(chl_full_ar < chl_full.data_minimum, np.nan, chl_full_ar)
    chl_full_ar = np.where(chl_full_ar > chl_full.data_maximum, np.nan, chl_full_ar)
    chl_full_df = pd.DataFrame(chl_full_ar)
    chl_full_df = chl_full_df[topoin_df>0]

    chl_tot_u = 40.2*(chl_full_df**0.507)
    chl_tot_l = 38*(chl_full_df**0.425)
    chl_tot = np.where(chl_full_df<=1,chl_tot_l,chl_tot_u)
    chl_tot_df = pd.DataFrame(chl_tot)	

    zeu = 200*(chl_tot_df**(-0.293))
    zeu = np.where(zeu <= 102, (568.2*(chl_tot_df**(-0.746))), zeu)
    zeu2 = pd.DataFrame(np.where(topoin_df < zeu, topoin_df, zeu))

    par_full = Dataset(os.path.join(par_dir,PAR_files[j]))
    par_full_ar = np.array(par_full.variables['par'][:][:])
    par_full_ar = np.where(par_full_ar < par_full.data_minimum, np.nan, par_full_ar)
    par_full_ar = np.where(par_full_ar > par_full.data_maximum, np.nan, par_full_ar)
    par_full_df = pd.DataFrame(par_full_ar)
    par_full_df = par_full_df[topoin_df>0]

    vol_func = 0.66125*(par_full_df/(par_full_df+4.1))

    for k in range(0,len(light_files)):
        ####pick appropriate day length file by month
        if float(light_files[k][-6:-4]) == float(SST_files[j][15:17]):
            daylight = np.load(os.path.join(day_dir,light_files[k]))
    npp = chl_full_df * pbopt * pd.DataFrame(daylight) * vol_func * zeu2
    npp = np.where(npp<0,np.nan,npp)

    with Dataset(os.path.join(npp_dir, chl_files[j][:-3]+'_NPP.nc'),'w','NETCDF4') as ncout:
        ncout.createDimension('lat', len(lat));
        ncout.createDimension('lon', len(lon));
        latvar = ncout.createVariable('lat','float32',('lat',));
        lonvar = ncout.createVariable('lon','float32',('lon',));
        myvar = ncout.createVariable('npp','float32',('lat','lon'));
        latvar[:] = lat;
        lonvar[:] = lon;
        myvar[:,:] = npp[:,:];
        myvar.coordinates = 'lat lon'



