import xarray as xr
from matplotlib.colors import LogNorm

path = 'D://thesisdata/nutrients/'
file = 'global-reanalysis-bio-001-029-monthly_1622729430962.nc'
ds = xr.open_dataset(path+file)

list(ds.variables)
ds = ds['fe'].sel(time='2009-09')

ds.plot(vmin=0.0000001)

ds
