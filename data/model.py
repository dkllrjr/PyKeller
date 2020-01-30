import numpy as np
#import xarray as xr

def dist_sphere(r0,the0,phi0,r1,the1,phi1):
#    (r0**2 + r1**2 - 2*r0*r1*(np.sin(the0)*np.sin(the1)*np.cos(phi0-phi1) + np.cos(the0)*np.cos(the1)))**.5
    a = r0**2 + r1**2
    b = 2*r0*r1
    c = np.sin(the0)*np.sin(the1)*np.cos(phi0-phi1) + np.cos(the0)*np.cos(the1)
    d = (a - b*c)
    return d**.5

def dist_sphere_deg(r0,the0,phi0,r1,the1,phi1):
    the0 = np.deg2rad(the0)
    phi0 = np.deg2rad(phi0)
    the1 = np.deg2rad(the1)
    phi1 = np.deg2rad(phi1)
    return dist_sphere(r0,the0,phi0,r1,the1,phi1)

def xr_near(xa,val):
    npa = np.array(xa)
    npa_abs = np.abs(npa - val)
    return np.where(npa_abs==np.min(npa_abs))

def lat_lon_near(lat_lon,loc):
    E_r = 6371000 #Earth's radius
    dist = []
    for i in range(len(lat_lon)):
        print(i,len(lat_lon))
        dist.append(dist_sphere_deg(E_r,lat_lon[i][1],lat_lon[i][0],E_r,loc[1],loc[0]))
    ind = np.where(np.array(dist)==np.min(np.array(dist)))[0]
    return np.array(lat_lon)[ind]

def lat_lon2nparray(xrvar):
    lat = np.array(xrvar.nav_lat_grid_M)
    lon = np.array(xrvar.nav_lon_grid_M)
    lat_lon = []
    for i in range(lat.shape[0]):
        for j in range(lat.shape[1]):
            lat_lon.append([lat[i,j],lon[i,j]])
    lat_lon_np = np.array(lat_lon)
    lat_lon_np = lat_lon_np.reshape(lat.shape[0],lat.shape[1],2)
    return lat_lon_np

def stringify_dates(xarr):
    dates = []
    for i in xarr:
        dates.append(str(np.array(i['time_counter'])))
    return dates

def both_dates(dates1,dates2):
    return list(set(dates1).intersection(dates2))

def dates2indices(xarr,dates):
    ind = []
    xr_dates = stringify_dates(xarr)
    for i in range(len(xr_dates)):
        if xr_dates[i] in dates:
            ind.append(i)
    return ind

def reduce_density(arr,i):
    return arr[::i,::i]