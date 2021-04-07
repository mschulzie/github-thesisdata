import xarray as xr

file = 'D://thesisdata/soil_moisture/ERA5-Land_hourly.nc'
ds = xr.open_dataset(file)
ds.variables
for var in ds:
    print(var+': '+ds[var].long_name)

print('~~~~~~~~~~~~~~~~')

ds['lai_lv'][0,...].plot()
