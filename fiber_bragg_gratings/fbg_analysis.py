# By: mach
# Created: Sun Mar 31 21:59:57 2019

import numpy as np
import sys
sys.path.append('/home/mach/Documents/Programming/Python/Atmospheric Science')
import pycuda_wavelets as py_wv
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#from scipy import signal

def find_a_b(wt):
    b = np.where(wt[0,:]==max(wt[0,:]))[0][0]
    a = np.where(wt[:,b]==max(wt[:,b]))[0][0]
    return a, b

def rel_norm(power):
    power -= min(power)
    power /= max(power)
    return power

def wav_trans_fbg(wavelength,power):
    res = np.mean(np.diff(wavelength))
    a = np.arange(3*res, 1 + res, res)
    power = rel_norm(power)
    wt = py_wv.sgwwt(power,wavelength,a,wavelength,1,.01)
    
    f,n = find_a_b(wt)
#    plt.plot(wt[:,n])
#    plt.plot(f,wt[f,n],'x')
#    plt.show()
    
    print('------')
    print(a[f])
    
#    fig = plt.figure()
#    ax = plt.axes(projection='3d')
#    x,y = np.meshgrid(wavelength,a)
#    ax.plot_surface(x,y,wt,cmap='viridis')
#    plt.show()
    return a,wt