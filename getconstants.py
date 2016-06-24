# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:38:45 2016

@author: Ent00002
"""

# the function below must be called with the following libraries imported:
# import numpy as np
# from netCDF4 import Dataset, and the global variable: invariant_data

def getconstants(latnrs,lonnrs,lake_mask,Dataset,invariant_data,np): # def getconstants in Python is the same as function in MATLAB. 
    
    # load the latitude and longitude from the invariants file
    latitude = Dataset(invariant_data, mode = 'r').variables['latitude'][latnrs] # [degrees north]
    longitude = Dataset(invariant_data, mode = 'r').variables['longitude'][lonnrs] # [degrees east]

    # Create land-sea-mask (in this model lakes are considered part of the land)
    lsm = np.squeeze(Dataset(invariant_data, mode = 'r').variables['lsm'][0,latnrs,lonnrs]) # 0 = sea, 1 = land
    
    for n in range(len(lake_mask[:,0])):
        lsm[lake_mask[n,0],lake_mask[n,1]] = 1

    lsm[0,:] = 0 # the northern boundary is always oceanic = 0
    lsm[-1,:] = 0 # the southern boundary is always oceanic = 0
    
    # Constants 
    g = 9.80665 # [m/s2] from ERA-interim archive
    density_water = 1000 # [kg/m3]
    dg = 111089.56 # [m] length of 1 degree latitude
    timestep = 6*3600 # [s] timestep in the ERA-interim archive (watch out! P & E have 3 hour timestep)
    
    # Semiconstants
    gridcell = np.abs(latitude[1] - latitude[0]) # [degrees] grid cell size
    A_gridcell = np.vstack(np.zeros((len(latitude))))
    for i in range(len(latitude)):
        A_gridcell[i] = (gridcell * dg) * (gridcell * np.cos(latitude[i] * np.pi / 180.0) * dg) # [m2] area size of grid cell
    L_N_gridcell = gridcell * np.cos((latitude + gridcell / 2.0) * np.pi / 180.0) * dg # [m] length northern boundary of a cell
    L_S_gridcell = gridcell * np.cos((latitude - gridcell / 2.0) * np.pi / 180.0) * dg # [m] length southern boundary of a cell
    L_EW_gridcell = gridcell * dg # [m] length eastern/western boundary of a cell 
    
    return latitude , longitude , lsm , g , density_water , timestep , A_gridcell , L_N_gridcell , L_S_gridcell , L_EW_gridcell , gridcell
