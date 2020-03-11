import numpy as np

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