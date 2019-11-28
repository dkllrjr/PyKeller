import numpy as np

def dist_sphere(r0,the0,phi0,r1,the1,phi1):
    return (r0**2 + r1**2 - 2*r0*r1*(np.sin(the0)*np.sin(the1)*np.cos(phi0-phi1) + np.cos(the0)*np.cos(the1)))**.5

def dist_sphere_deg(r0,the0,phi0,r1,the1,phi1):
    the0 = np.radians(the0)
    phi0 = np.radians(phi0)
    the1 = np.radians(the1)
    phi1 = np.radians(phi1)
    return dist_sphere(r0,the0,phi0,r1,the1,phi1)
