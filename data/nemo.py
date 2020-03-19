##############################################################################
# Python3
# laplace
# Tue Mar  3 12:14:20 2020
##############################################################################

import numpy as np
import PyKeller.data.model as PKdm

def lat_lon2nparray(xrvar):
    lat = np.array(xrvar.nav_lat)
    lon = np.array(xrvar.nav_lon)
    lat_lon = []
    for i in range(lat.shape[0]):
        for j in range(lat.shape[1]):
            lat_lon.append([lat[i,j],lon[i,j]])
    lat_lon_np = np.array(lat_lon)
    lat_lon_np = lat_lon_np.reshape(lat.shape[0],lat.shape[1],2)
    return lat_lon_np

def find_loc(var,loc):
    # loc needs to be a list of lists => [[lat,lon],[lat,lon]]
    
    lat = np.array(var.nav_lat)
    lon = np.array(var.nav_lon)
    lat_lon = []
    
    for i in range(lat.shape[0]):
        for j in range(lat.shape[1]):
            lat_lon.append([lat[i,j],lon[i,j]])
    
    ind_loc = []
    
    for i in range(len(loc)):
        ind_loc.append(PKdm.lat_lon_near_angle(lat_lon,loc[i]))
    
    lat_lon_np = np.array(lat_lon)
    lat_lon_np = lat_lon_np.reshape(lat.shape[0],lat.shape[1],2)
    ind_loc_np = np.array(ind_loc)
    ind_loc_np = ind_loc_np.reshape(len(loc),2)
    
    ind = []
    
    for k in range(ind_loc_np.shape[0]):
        for i in range(lat_lon_np.shape[0]):
            for j in range(lat_lon_np.shape[1]):
                if tuple(lat_lon_np[i,j]) == tuple(ind_loc_np[k]):
                    ind.append([i,j])
    
    ind = np.array(ind)
    
    return ind

def find_loc_SI(SI,loc):
    # loc needs to be a list of lists => [[lat,lon],[lat,lon]]
    
    lat = SI['latitude']
    lon = SI['longitude']
    date = SI['date']
    
    i = 0
    ind_date = [0]
    while i < len(date) - 1:
        if date[i] < date[i+1]:
            ind_date.append(i+1)
        i += 1
    ind_date.append(i+1)
    
    lat_lon = []
    for i in range(len(lat)):
        lat_lon.append([lat[i],lon[i]])
        
    ind_loc = []
    for i in range(len(loc)):
        ind_loc.append(PKdm.lat_lon_near_angle(lat_lon,loc[i]))
        
#    return ind_loc,ind_date

    ind = []
    
    for i in range(len(ind_loc)):
        ind.append([])
        for j in range(len(ind_loc[i])):
            for k in range(ind_date[j],ind_date[j+1]):
#                print(tuple(lat_lon[k]),tuple(ind_loc[i][j]))
                if tuple(lat_lon[k]) == tuple(ind_loc[i][j]):
                    ind[i].append(k)
                    
        ind[i] = np.array(ind[i])
    
    return ind