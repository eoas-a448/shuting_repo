# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
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

# %%
import warnings
import intake
import xarray as xr 
import proplot as plot 
import matplotlib.pyplot as plt 
import pandas as pd
warnings.filterwarnings('ignore')


# %%
df = pd.read_csv("cmip6-zarr-consolidated-stores.csv")

# %% [markdown]
# ## First show all BCC historical runs

# %%
import gcsfs
import xarray as xr
pr=df.query("activity_id=='CMIP' & institution_id == 'BCC' & table_id=='Amon'"
            "& experiment_id == 'historical' & variable_id=='pr'")

# %%
pr

# %% [markdown]
# ## Limit to 1 run of the earth system model (ESM)

# %%
pr=df.query("activity_id=='CMIP' & institution_id == 'BCC' & table_id=='Amon'"
            "& experiment_id == 'historical' & variable_id=='pr'"
            "& source_id=='BCC-ESM1' & member_id == 'r1i1p1f1'")
pr

# %% [markdown]
# ## Read the file into a zarr dataset

# %%
pr_zarr = pr.iloc[0]['zstore']
fs = gcsfs.GCSFileSystem(project="my_project")

# %%
gcsmap = fs.get_mapper(pr_zarr)
dset = xr.open_zarr(gcsmap)

# %%
dset

# %% [markdown]
# ## Plot the first timestep

# %%
dset['time'][0]

# %%
fig, ax = plot.subplots(axwidth=4.5, tight=True,
                        proj='robin', proj_kw={'lon_0': 90},
                       figsize=(15,10))
# format options
ax.format(land=False, coast=True, innerborders=True, borders=True,
          labels=True, geogridlinewidth=0,)
map1 = ax.pcolormesh(dset['lon'], dset['lat'], dset['pr'][0,:,:]*1.e3,
                   cmap='IceFire', extend='both')
ax.colorbar(map1, loc='b', shrink=0.5, extendrect=True)
plt.show()

# %%

# %%
