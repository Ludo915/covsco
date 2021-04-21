#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Imports #%%
# =============================================================================
#part| #%%
import sys
import datetime
from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr
from datetime import timedelta
import re
from tqdm import tqdm
from operator import itemgetter
import itertools
from datetime import date
from os import listdir
from os.path import isfile, join
import os
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset
import csv
from zipfile import ZipFile
from utilities import download_url
import subprocess
import time
from compute_engineered_features import Compute_Engineered_Features_for_df
from process_population_historical_data import process_population_hist
from download_covid_hist_data import download_covid_hist_data
from process_covid_historical_data import process_covid_historical_data
from download_cams_forecast import download_cams_forecast
from process_cams_forecast_data import process_cams_forecast_data
from process_mobility_historical_data import process_mobility_historical_data
from process_covid_positive_test_historical_data import process_covid_positive_test_historical_data
from process_hist_vaccination_data import process_hist_vaccination_data
from process_comorbidities import process_comorbidities_data
from process_smokers_data import process_smokers_data
from process_variants_hist_data import process_variants_hist_data
from process_minority_data import process_minority_data
from process_population_rectified import process_population_rectified
from process_low_income import process_low_income
from compute_polution_levels import compute_pollution_levels

# =============================================================================
# Merge data #%%
# =============================================================================

print('Processing Population data ... ', flush=True, end='')
GetPopulationData = process_population_hist()
GetPopulationData.get_data()

print('Processing Covid data ... ', flush=True, end='')
CovidHistData = download_covid_hist_data()
CovidHistData.GetData()
ProcessCovidHistoricalData = process_covid_historical_data()
ProcessCovidHistoricalData.process_covid_hist_data()

print('Downloading Cams Forecast Data')
CamsHistForecasts = download_cams_forecast()
CamsHistForecasts.download()

print('Processing Cams Forecast Data')
ProcessCams = process_cams_forecast_data()
ProcessCams.process_cams()

print("Processing Mobility indices data ...")
ProcessMobility = process_mobility_historical_data()
ProcessMobility.process_mobility()

print("Processing Covid Positive Tests (Previous day) ...")
ProcessCovidPositiveTests = process_covid_positive_test_historical_data()
ProcessCovidPositiveTests.process_covid_positive_test()

print("Processing Vaccination historical data ...")
ProcessVaccination = process_hist_vaccination_data()
ProcessVaccination.process_hist_vaccination()

print("Processing Comorbidities Data...")
ProcessComorbidities = process_comorbidities_data()
ProcessComorbidities.process_comorbidities()

print("Processing Smokers Data...")
ProcessSmokers = process_smokers_data()
ProcessSmokers.process_smokers()

print("Processing Variants data ...")
ProcessVariantsHistoricalData = process_variants_hist_data()
ProcessVariantsHistoricalData.process_variants()

print("Processing minority data...")
ProcessMinority = process_minority_data()
ProcessMinority.process_minority()

print("Reprocessing population data...")
ProcessPopRectified = process_population_rectified()
ProcessPopRectified.process_population_rect()

print("Processing low_income data")
ProcessLowIncome = process_low_income()
ProcessLowIncome.process_li()

print("Computing the engineered Features")
Engineered_Features = Compute_Engineered_Features_for_df()
Engineered_Features.get_data()
Engineered_Features.max_normalize_data()
Engineered_Features.compute_dictionnaries()
Engineered_Features.compute_Engineered_features_assign_to_df()

print("Computing pm2.5 Pollutions levels")
ComputePollutionLevels = compute_pollution_levels()
ComputePollutionLevels.compute_levels()