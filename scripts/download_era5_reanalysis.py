#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created by  : Niclas Rieger
# Created on  : Wed Nov 13 16:23:24 2019
# =============================================================================
""" Download ERA5 variables from ECMWF """
# =============================================================================
# Imports
# =============================================================================
import os
import numpy as np
import datetime as dt
import cdsapi
import yaml

work_dir = os.path.dirname(os.path.abspath(__file__))
save_to = os.path.join(work_dir, '../data/train/era5/fr/reanalysis')
if not os.path.exists(save_to):
    os.makedirs(save_to)

# get personal directory of cdsapi
try:
    with open('.cdsapirc_dir', 'r') as file:
        dir_cams_api = file.readline().rstrip()
except FileNotFoundError:
    raise FileNotFoundError("""cdsapirc file cannot be found. Write the
        directory of your personal .cdsapirc file in a local file called
        `.cdsapirc_dir` and place it in this git directory.""")

# Download CAMS
# -----------------------------------------------------------------------------
print('Download data from ERA ...', flush=True)

with open(dir_cams_api, 'r') as f:
    credentials = yaml.safe_load(f)

c = cdsapi.Client(url=credentials['url'], key=credentials['key'])

# =============================================================================
# Choose Download Parameters
# =============================================================================
dataset 	= 'cams-global-reanalysis-eac4'
# reanalysis-era5-land,
# reanalysis-era5-land-monthly-means,
# reanalysis-era5-single-levels,
# reanalysis-era5-single-levels-monthly-means,
# reanalysis-era5-single-levels-monthly-means-preliminary-back-extension

variable 	= [
	#'10m_u_component_of_wind'
	#,'10m_v_component_of_wind'
	 '2m_temperature'
    , '2m_dewpoint_temperature'
	#, 'land_sea_mask'
	#, 'leaf_area_index_high_vegetation'
	#, 'leaf_area_index_low_vegetation'
	#, 'mean_sea_level_pressure'
	#, 'orography'
	#, 'sea_surface_temperature'
	#, 'surface_pressure'
	#, 'total_precipitation'
	# 'volumetric_soil_water_layer_1'
	#, 'volumetric_soil_water_layer_2'
	#, 'volumetric_soil_water_layer_3'
	#, 'volumetric_soil_water_layer_4'
	#, 'evaporation'
	#, 'instantaneous_moisture_flux'
	#, 'snow_cover'
]

productType = 'reanalysis'
# """
# monthly_averaged_reanalysis,
# reanalysis
# reanalysis-monthly-means-of-daily-means
# """
years 		= np.arange(2020,2022).tolist()
months 		= np.arange(1,13).tolist()
days 		= np.arange(1,32).tolist()
# time steps are often only '00:00' for daily accumulated or monthly means
times 		= [dt.time(i).strftime('%H:00') for i in range(24)]
grid 		= [0.01, 0.01]
# options: eg. 0.25, 0.5, 1.0
area = [51.75, -5.83, 41.67,11.03] # choose entire region of Europe
# full globe: [90, -180, -90, 180]

grid_str    	= 'x'.join([str(r) for r in grid])
file_name 	= '_'.join(['era5',str(years[0]),'hourly','europe',grid_str])
file_name     	= file_name + '.nc'
output    	= os.path.join(save_to, file_name)
# =============================================================================
# Download CDS data
# =============================================================================
#%%

import cdsapi

c = cdsapi.Client()



c = cdsapi.Client()
c.retrieve(
    dataset,
    {
        'format'		: 'netcdf',
        'variable'		: variable,
        'year'			: years,
        'month'         : months,
        'day' 			: days,
        'time'		    : times,
        'grid'          : grid,
        'area'          : area
    },
    output
)

print('Download finished.', flush=True)
