---
jupytext:
  cell_metadata_filter: all
  notebook_metadata_filter: all,-language_info
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
import warnings
import intake
import xarray as xr 
import proplot as plot 
import matplotlib.pyplot as plt 
import pandas as pd
warnings.filterwarnings('ignore')
```

```{code-cell} ipython3
df = pd.read_csv("cmip6-zarr-consolidated-stores.csv")
```

## First show all BCC historical runs

```{code-cell} ipython3
import gcsfs
import xarray as xr
pr=df.query("activity_id=='CMIP' & institution_id == 'BCC' & table_id=='Amon'"
            "& experiment_id == 'historical' & variable_id=='pr'")
```

```{code-cell} ipython3
pr
```

## Limit to 1 run of the earth system model (ESM)

```{code-cell} ipython3
pr=df.query("activity_id=='CMIP' & institution_id == 'BCC' & table_id=='Amon'"
            "& experiment_id == 'historical' & variable_id=='pr'"
            "& source_id=='BCC-ESM1' & member_id == 'r1i1p1f1'")
pr
```

## Read the file into a zarr dataset

```{code-cell} ipython3
pr_zarr = pr.iloc[0]['zstore']
fs = gcsfs.GCSFileSystem(project="my_project")
```

```{code-cell} ipython3
gcsmap = fs.get_mapper(pr_zarr)
dset = xr.open_zarr(gcsmap)
```

```{code-cell} ipython3
dset
```

## Plot the first timestep

```{code-cell} ipython3
dset['time'][0]
```

```{code-cell} ipython3
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
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
