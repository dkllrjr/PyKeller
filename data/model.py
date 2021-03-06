import numpy as np

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

def central_angle(lon0,lon1,lat0,lat1):
    return np.arccos(np.sin(lon0)*np.sin(lon1)+np.cos(lon0)*np.cos(lon1)*np.cos(lat1-lat0))

def central_angle_deg(lon0,lon1,lat0,lat1):
    lon0 = np.deg2rad(lon0)
    lon1 = np.deg2rad(lon1)
    lat0 = np.deg2rad(lat0)
    lat1 = np.deg2rad(lat1)
    return central_angle(lon0,lon1,lat0,lat1)
    
def xr_near(xa,val):
    npa = np.array(xa)
    npa_abs = np.abs(npa - val)
    return np.where(npa_abs==np.min(npa_abs))

def lat_lon_near(lat_lon,loc):
    E_r = 6371000 #Earth's radius
    dist = []
    for i in range(len(lat_lon)):
        # print(i,len(lat_lon))
        dist.append(dist_sphere_deg(E_r,lat_lon[i][1],lat_lon[i][0],E_r,loc[1],loc[0]))
    ind = np.where(np.array(dist)==np.min(np.array(dist)))[0]
    return np.array(lat_lon)[ind]

def lat_lon_near_angle(lat_lon,loc):
    dist = []
    for i in range(len(lat_lon)):
        dist.append(central_angle_deg(lat_lon[i][1],loc[1],lat_lon[i][0],loc[0]))
    ind = np.where(np.array(dist)==np.min(np.array(dist)))[0]
    return np.array(lat_lon)[ind]

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

#def datetime2datetime64(t):
#    if len(str(t.day)) < 2:
#        d = '0' + str(t.day)
#    else:
#        d = str(t.day)
#    if len(str(t.month)) < 2:
#        m = '0' + str(t.month)
#    else:
#        m = str(t.month)
#    if len(str(t.hour)) < 2:
#        h = '0' + str(t.hour)
#    else:
#        h = str(t.hour)
#    if len(str(t.minute)) < 2:
#        mn = '0' + str(t.minute)
#    else:
#        mn = str(t.minute)
#    if len(str(t.second)) < 2:
#        s = '0' + str(t.second)
#    else:
#        s = str(t.second)
#        
#    ndate = str(t.year) + '-' + m + '-' + d + 'T' + h + ':' + mn + ':' + s
#    
#    return np.datetime64(ndate)

def datetime2datetime64(t):
    return np.datetime64(t)