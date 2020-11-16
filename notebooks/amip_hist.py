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

# %%
fp='amip_hist.nc'
nc = netCDF4.Dataset(fp)
plt.show()
print(nc)

# %%
print(nc.__dict__)

# %%
for dim in nc.dimensions.values():
    print(dim)

# %%
for var in nc.variables.values():
    print(var)

# %%
lat = nc['lat'][:]
lon = nc['lon'][:]
rlutcs_var=nc['rlutcs'][0,:,:]
rlutcs_units=nc['rlutcs'].units
#time_var = nc['time'][:]
#time_units = nc['time'].units
#dtime = netCDF4.num2date(time_var[:],time_units)
print(rlutcs_units)

# %%

# %%
print (lon.min(),lon.max())

# %%
print (lat.min(),lat.max())

# %%
lon_0 = lon.mean()
lat_0 = lat.mean()
m = Basemap(width=5000000,height=3500000,
            resolution='l',projection='stere',\
            lat_ts=40,lat_0=lat_0,lon_0=lon_0)

# %%
lon, lat = np.meshgrid(lon, lat)
xi, yi = m(lon, lat)

# %%
# Plot Data
cs = m.pcolor(xi,yi,np.squeeze(rlutcs_var))

# Add Grid Lines
m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(rlutcs_units)

# Add Title
plt.title('Outgoing longwave flux')

plt.show()

# %%
