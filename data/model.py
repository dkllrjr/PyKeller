import numpy as np
import xarray as xr

def dist_sphere(r0,the0,phi0,r1,the1,phi1):
    return (r0**2 + r1**2 - 2*r0*r1*(np.sin(the0)*np.sin(the1)*np.cos(phi0-phi1) + np.cos(the0)*np.cos(the1)))**.5

def dist_sphere_deg(r0,the0,phi0,r1,the1,phi1):
    the0 = np.radians(the0)
    phi0 = np.radians(phi0)
    the1 = np.radians(the1)
    phi1 = np.radians(phi1)
    return dist_sphere(r0,the0,phi0,r1,the1,phi1)

def xr_near(xa,val):
    npa = np.array(xa)
    npa_abs = np.abs(npa - val)
    return np.where(npa_abs==np.min(npa_abs))

def lat_lon_near(lat_lon,loc):
    E_r = 6371000 #Earth's radius
    dist = []
    for i in range(len(lat_lon)):
        dist.append(dist_sphere_deg(E_r,lat_lon[i][1],lat_lon[i][0],E_r,loc[1],loc[0]))
    ind = np.where(np.array(dist)==np.min(np.array(dist)))[0]
    return np.array(lat_lon)[ind]