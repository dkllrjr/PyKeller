# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 19:58:41 2018

@author: Doug
"""

import numpy as np
import collections
import math as m

def moving_mean(f,N):
    mm = np.zeros(f.size)
    
    for i in range(f.size):
        if i < N:
            m = []
            for j in range(i+N+1):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.mean(m)
        elif i+N > f.size-1:
            m = []
            for j in range(i-N,f.size):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.mean(m)
        else:
            mm[i] = np.mean(f[i-N:i+N+1][np.where(np.isfinite(f[i-N:i+N+1]))[0]])
        
    return mm

def moving_median(f,N):
    mm = np.zeros(f.size)
    
    for i in range(f.size):
        if i < N:
            m = []
            for j in range(i+N+1):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.median(m)
        elif i+N > f.size-1:
            m = []
            for j in range(i-N,f.size):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.median(m)
        else:
            mm[i] = np.median(f[i-N:i+N+1][np.where(np.isfinite(f[i-N:i+N+1]))[0]])
        
    return mm

def super_sample(f,x):
    x_ss = []
    dx = np.diff(x)
    for i in range(x.size-1):
        x_ss.append(x[i])
        x_ss.append(x[i]+dx[i]/2)
    x_ss.append(x[-1])
    x_ss = np.array(x_ss)
    f_ss = np.interp(x_ss,x,f)
    return f_ss, x_ss

def multi_super_sample(f,x,runs):
    for i in range(runs):
        f,x = super_sample(f,x)
    return f,x

def mode(f):
    
    def counts(f):
        table = collections.Counter(iter(f)).most_common()
        if not table:
            return table
        maxfreq = table[0][1]
        for i in range(1, len(table)):
            if table[i][1] != maxfreq:
                table = table[:i]
                break
        return table
    
    table = counts(f)
    return table[0][0]

def curvature(f,x):
    dy = derivative(f,x,1)
#    ddy = derivative(dy,x)
    ddy = derivative(f,x,2)
    k = np.zeros_like(f)
    for i in range(f.size):
        k[i] = abs(ddy[i])/(1 + dy[i]**2)**1.5
    return k

def derivative(f,x,n):
    dy = f
    for i in range(n):
        dy = np.gradient(dy)/np.gradient(x)
    return dy

def norm_erf(arr,side):
    #side = 1 or -1
    x = np.linspace(-np.pi, np.pi, arr.size)
    x_erf = np.zeros_like(arr)
    for i in range(arr.size):
        x_erf[i] = (m.erf(x[i])+1)/2*arr[i*side]
    return x_erf

def norm_sup_gauss(arr,a,n):
    x = np.linspace(-np.pi**(1/n), np.pi**(1/n), arr.size)
    x_sg = np.zeros_like(arr)
    for i in range(arr.size):
        x_sg[i] = np.exp(-.5*(x[i]/a)**(2*n)) * arr[i]
    return x_sg