# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     notebook_metadata_filter: all,-language_info,-toc,-latex_envs
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Setting your toolbox

# %% [markdown]
# Sources
#
# https://github.com/willyhagi/climate-data-science.git
#
# https://towardsdatascience.com/a-quick-introduction-to-cmip6-e017127a49d3
#
# https://pangeo-data.github.io/pangeo-cmip6-cloud/
#
# https://pangeo-data.github.io/pangeo-cmip6-cloud/accessing_data.html#manually-searching-the-catalog
#
# https://storage.cloud.google.com/cmip6/cmip6-zarr-consolidated-stores.csv  -- 50 Mbytes
#
# Pandas:  https://github.com/wesm/pydata-book
# Beijing model:  https://gmd.copernicus.org/articles/12/1573/2019/
#
#
# https://hub.binder.pangeo.io/user/pangeo-data-pan--cmip6-examples-7bc6tlcw/lab
#
# https://journals.ametsoc.org/jcli/article/30/15/5985/98054/Climatological-Characteristics-of-Typical-Daily
#
# https://pangeo-data.github.io/pangeo-cmip6-cloud/
#
# https://es-doc.org/cmip6-experiments/
#
# Pandas:  https://github.com/wesm/pydata-book
# Beijing model:  https://gmd.copernicus.org/articles/12/1573/2019/
#
#
# https://hub.binder.pangeo.io/user/pangeo-data-pan--cmip6-examples-7bc6tlcw/lab
#
# https://journals.ametsoc.org/jcli/article/30/15/5985/98054/Climatological-Characteristics-of-Typical-Daily
#
# https://pangeo-data.github.io/pangeo-cmip6-cloud/
#
# https://es-doc.org/cmip6-experiments/
#
# https://esgf-node.llnl.gov/search/cmip6/

# %%
import warnings
import intake
import xarray as xr 
import proplot as plot 
import matplotlib.pyplot as plt 
import pandas as pd


warnings.filterwarnings('ignore')

# %%
cat = intake.open_catalog("https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml")

# %%
out=cat.search('cmip6')
list(out)

# %%
from intake import open_catalog

cat = open_catalog("https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/climate.yaml")
ds  = cat.cmip6_gcs()

# %%
ds

# %%
# download this from https://storage.cloud.google.com/cmip6/cmip6-zarr-consolidated-stores.csv
df = pd.read_csv("cmip6-zarr-consolidated-stores.csv")

# %%
import gcsfs
import xarray as xr
tas=df.query("activity_id=='CMIP' & institution_id == 'BCC' & table_id=='Amon' & variable_id=='tas'")
tas_zarr=tas.loc[15437]['zstore']
dir(gcsfs)
fs = gcsfs.GCSFileSystem(project="my_project")
gcsmap = fs.get_mapper(tas_zarr)
dset = xr.open_zarr(gcsmap)
#mapper = gcsfs.get_mapper(tas)

# %%
dset.keys()

# %%
dset['tas']

# %%
fig, ax = plot.subplots(axwidth=4.5, tight=True,
                        proj='robin', proj_kw={'lon_0': 180},)
# format options
ax.format(land=False, coast=True, innerborders=True, borders=True,
          labels=True, geogridlinewidth=0,)
map1 = ax.pcolormesh(dset['lon'], dset['lat'], dset['tas'][0,:,:],
                   cmap='IceFire', extend='both')
ax.colorbar(map1, loc='b', shrink=0.5, extendrect=True)
plt.show()

# %%
print(len(df))
out = df.query("activity_id=='CMIP' & institution_id == 'BCC'")
print(len(out))
set(out['variable_id'])

# %%
