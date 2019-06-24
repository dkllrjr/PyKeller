#Atmospheric Refractivity functions

import numpy as np
from scipy.interpolate import interp1d

def N_eq(P,T,e): #refractivity of the atmosphere
    #P is the atmospheric pressure; hPa or mb
    #T is the absolute temperature; K
    #e is the partial pressure of water vapor in the atmosphere; hPa or mb
    return 77.6*P/T + 3.73*10**5*e/T**2

def M_eq(N,z): #modified refractivity of the atmosphere; assumes the earth is flat
    #N is the refractivity
    #z is the vertical height
    return N + .157*z

def snell_ny_forward_propagation(x0,y0,theta0,dx,ny,y):
    #x0 is the initial light ray x point
    #y0 is the initial light ray y point
    #theta0 is the initial light ray angle
    #n0 is the initial medium refractive index

    dy = np.tan(theta0)*dx
    x1 = x0 + dx
    y1 = y0 + dy
    n0 = snell_ny(ny,y,y0)
    n1 = snell_ny(ny,y,y1)
    theta1 = np.arcsin(n0*np.sin(theta0)/n1)
    
    return x1, y1, theta1
    
def snell_ny(ny_arr,y_arr,y):
    
    ny = interp1d(y_arr,ny_arr)

    return ny(y)