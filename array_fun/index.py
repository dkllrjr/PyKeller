import numpy as np
import xarray as xr
import PyKeller.array_fun.area as afa

def xr_near(xa,val):
    npa = np.array(xa)
    npa_abs = np.abs(npa - val)
    return np.where(npa_abs==np.min(npa_abs))

def lat_lon_near(lat_lon,loc):
    E_r = 6371000 #Earth's radius
    dist = []
    for i in range(len(lat_lon)):
        dist.append(afa.dist_sphere_deg(E_r,lat_lon[i][1],lat_lon[i][0],E_r,loc[1],loc[0]))
    ind = np.where(np.array(dist)==np.min(np.array(dist)))[0]
    return np.array(lat_lon)[ind]
