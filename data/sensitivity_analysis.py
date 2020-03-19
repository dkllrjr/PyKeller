import numpy as np
import xarray as xr
import pickle

def conserve_direction(v,u):
    
    return v/u

def wind_magnitude(u,v,w):

    return (u**2+v**2+w**2)**.5

def wind_direction(u,v):
    
    return np.arctan2(v,u)

def wind_filter(u,uth,a):

    return np.where(np.abs(u) < uth, u , np.sign(u)*(uth + a*(np.abs(u) - uth)))
    
def threshold(u,v,c):
    return c/(1+(v/u)**2)**.5

def wind_field_filter(ug,vg,c,a):
    
    uth = threshold(ug,vg,c)
    un = wind_filter2(ug,uth,a)
    vn = vg/ug * un
    
    return un,vn

def wind_filter2(u,uth,a):
    
    return np.where(np.abs(u) < uth, u , np.sign(u)*(uth + a*(np.abs(u) - uth)))

def stratification_index(N,z):
    
    return np.trapz(N*z,z)

def nemo_stratification_index(N):
    # N really equals N^2
    d = N['depthw']
    h_i = np.where(d<=1000)[0]
    si = []
    date = []
    lat = []
    lon = []
    
    for t in range(len(N['time_counter'])):
        print(N['time_counter'][0][0:10],t)
        for x in range(len(N['x_grid_W'])):
            for y in range(len(N['y_grid_W'])):
                temp_N = N.isel(time_counter=t,x_grid_W=x,y_grid_W=y)
                temp_N = temp_N[h_i]
                nan_i = np.where(temp_N!=np.nan)[0]
                if nan_i.size != 0:
                    temp_d = d[nan_i]
                    date.append(str(temp_N['time_counter'].values))
                    lat.append(np.float32(temp_N['nav_lat_grid_W'].values))
                    lon.append(np.float32(temp_N['nav_lon_grid_W'].values))
                    si.append(stratification_index(temp_N.values,temp_d.values))
                    
    SI = {'stratification_index':si,'latitude':lat,'longitude':lon,'date':date,'units':'m^2/s^2','description':'stratification index of the Gulf of Lion from a NEM0MED12 simulation'}
    
    return SI
    
def mp_N(rho_path,save_path):

    rho = xr.open_dataset(rho_path) # vodensity, vovaisala
    
    print('Loaded ',rho_path)
    
    N = rho['vovaisala'].isel(y_grid_W=slice(151,210,1),x_grid_W=slice(165,208,1))
        
    SI = nemo_stratification_index(N)
    
    save_file_path = save_path + rho_path[-27:-6] + 'SI.pickle'
    
    with open(save_file_path,'wb') as file:
        pickle.dump(SI,file)