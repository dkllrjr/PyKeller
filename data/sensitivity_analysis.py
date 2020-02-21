import numpy as np

def linear_threshold_filter(x,xth,a):
    
    return xth + a * (x - xth)

def conserve_direction(v,u):
    
    return v/u

def wind_magnitude(u,v,w):

    return (u**2+v**2+w**2)**.5

def wind_direction(u,v):
    
    return np.arctan2(v,u)