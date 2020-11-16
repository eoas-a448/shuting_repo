# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from matplotlib import pyplot as plt
import pandas as pd
import netCDF4
import numpy as np
from mpl_toolkits.basemap import Basemap
import datetime as dt
from netCDF4 import num2date, date2num

# %%
fp='amip.nc'
amip = netCDF4.Dataset(fp)
plt.show()
print(amip)

# %%
for var in amip.variables.values():
    print(var)

# %%
lat_amip = amip['lat'][:]
lon_amip = amip['lon'][:]
time_amip=amip['time'][:]
time_amip_units=amip['time'].units
pr_amip_var=amip['pr'][0,:,:]
pr_amip_units=amip['pr'].units

print(time_amip_units)
print(pr_amip_units)

# %%
time_amip_units=amip['time'].units
time_amip_cal = amip['time'].calendar
print(time_amip_cal)

dates = num2date(time_amip[:],units=time_amip_units,calendar=time_amip_cal)
print("dates corresponding to time values:\n{}".format(dates))


# %%
prmm=pr_amip_var*86400
print(np.squeeze(prmm))

# %%
m=Basemap(projection='mill',lat_ts=10, \
  llcrnrlon=lon_amip.min(),urcrnrlon=lon_amip.max(), \
  llcrnrlat=lat_amip.min(),urcrnrlat=lat_amip.max(), \
  resolution='c')

Lon, Lat = np.meshgrid(lon_amip,lat_amip)
x, y = m(Lon,Lat)

cs = m.pcolormesh(x,y,np.squeeze(prmm),shading='flat', \
  cmap=plt.cm.jet)

m.drawcoastlines()
#m.fillcontinents()
#m.drawmapboundary()
m.drawstates()
m.drawcountries()
m.drawparallels(np.arange(-90.,120.,30.), \
  labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.), \
  labels=[0,0,0,1])

m.colorbar(cs)
plt.title('Amip precipitation(mm/day)')
plt.show()


# %%
fp='hist1950_2020.nc'
hist = netCDF4.Dataset(fp)
plt.show()
lat_hist = hist['lat'][:]
lon_hist = hist['lon'][:]
time_hist=hist['time'][:]
pr_hist_var=hist['pr'][0,:,:]
pr_hist_units=hist['pr'].units
pr_hist_mm=pr_hist_var*86400

m=Basemap(projection='mill',lat_ts=10, \
  llcrnrlon=lon_hist.min(),urcrnrlon=lon_hist.max(), \
  llcrnrlat=lat_hist.min(),urcrnrlat=lat_hist.max(), \
  resolution='c')

Lon_hist, Lat_hist = np.meshgrid(lon_hist,lat_hist)
x_hist, y_hist = m(Lon_hist,Lat_hist)

cs = m.pcolormesh(x_hist,y_hist,np.squeeze(pr_hist_mm),shading='flat', \
  cmap=plt.cm.jet)

m.drawcoastlines()
#m.fillcontinents()
#m.drawmapboundary()
m.drawstates()
m.drawcountries()
m.drawparallels(np.arange(-90.,120.,30.), \
  labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.), \
  labels=[0,0,0,1])

m.colorbar(cs)
plt.title('Historical precipitation(mm/day)')
plt.show()



# %%
#stroing the lat and lon of Beijing
lat_Beijing=39.916668
lon_Beijing=116.383331

#square difference of lat and lon
sq_diff_lat=(lat_amip-lat_Beijing)**2
sq_diff_lon=(lon_amip-lon_Beijing)**2

#identifying the index of minimum value for lat and lon
min_index_lat=sq_diff_lat.argmin()
min_index_lon=sq_diff_lon.argmin()

#creating a pandas dataframe
dates = num2date(time_amip[:],units=time_amip_units)
starting_date=amip['time'].units[11:0]+'1979-01-16'
ending_date=amip['time'].units[11:0]+'2014-12-07'
date_range=pd.date_range(start=starting_date,end=ending_date,freq='30D')

df=pd.DataFrame(0,columns=['Precipitation'],index=date_range)
dt=np.arange(0,amip['time'].size)

for time_index in dt:
    df.iloc[time_index]=prmm[time_index,min_index_lat,min_index_lon]

# %%
print(starting_date)
print(ending_date)
print(dates[-1])
print(date_range)
print(dates.size)
print(df.iloc[1])

# %%
for var in hist.variables.values():
    print(var)

# %%
time_hist_units=hist['time'].units
time_hist_cal = hist['time'].calendar
print(time_hist_cal)

dates = num2date(time_hist[:],units=time_hist_units)
#print("dates corresponding to time values:\n{}".format(dates))
print(dates)

# %%
dates_hist = num2date(time_hist[:],units=time_hist_units)
starting_date_hist=hist['time'].units[11:0]+'1950-01-16'
ending_date_hist=hist['time'].units[11:0]+'2000-12-03'
date_range_hist=pd.date_range(start=starting_date_hist,end=ending_date_hist,freq='30D')
print(starting_date_hist)
print(ending_date_hist)
print(date_range_hist)
print(dates_hist.size)

# %%
