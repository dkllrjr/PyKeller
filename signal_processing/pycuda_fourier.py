#Fourier Analysis and Transform functions written with PyCuda

import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule

def reduce_exp(t,w,exp): #use this function to parallel reduce summate wavelet integrals
  
    mod = SourceModule(source = """
                                __global__ void reduce(float *exp, float *ft){
                                extern __shared__ float temp[];
                                
                                int index = threadIdx.x + blockDim.x * blockIdx.x;

                                temp[threadIdx.x] = exp[index];

                                __syncthreads();
                                
                                for(int t = 1; t < blockDim.x; t *= 2){
                                        if(threadIdx.x % (2 * t) == 0){
                                                temp[threadIdx.x] += temp[threadIdx.x + t];
                                        }
                                        __syncthreads();
                                }
                                        
                                if(threadIdx.x == 0){
                                        ft[blockIdx.x] = temp[0];
                                        
                                }
                                
                                } 
                                """)
    
    reduce = mod.get_function("reduce")
    
    ft = np.zeros(w.size,dtype=np.float32)
    y = int(np.ceil(np.log(t.size)/np.log(2)))
    
    reduce(drv.In(exp), drv.Out(ft), block = (t.size,1,1), grid = (w.size,1,1), shared = (4*2**y))
    
    return ft

def ft(s,t): #runs the fourier transform
    
    t = np.array(t).astype(np.float32)
    s = np.array(s).astype(np.float32)
    Ts = t[1] - t[0]
    w = np.linspace(0,1/(2*Ts),s.size,dtype=np.float32)*2*np.pi

    exp_real, exp_imag = fill_ft(s,t,w)
    ft_real = reduce_exp(t,w,exp_real)
    ft_imag = reduce_exp(t,w,exp_imag)
    
    ft = ft_real + ft_imag * 1j
    
    return ft, w

def fill_ft(s,t,w): #use this function to multiply the function by the euler identity function

    mod = SourceModule(source = """
                                __global__ void fill(float *s, float *t, float *w, float *exp_real, float *exp_imag){
                                int index = threadIdx.x + blockDim.x * blockIdx.x;
                                exp_real[index] = s[threadIdx.x] * cos(w[blockIdx.x] * t[threadIdx.x]);
                                exp_imag[index] = s[threadIdx.x] * -sin(w[blockIdx.x] * t[threadIdx.x]);
                                }
                                """)
    
    fill = mod.get_function("fill")
    
    exp_real = np.zeros(w.size*t.size).astype(np.float32)
    exp_imag = np.zeros(w.size*t.size).astype(np.float32)
      
    fill(drv.In(s), drv.In(t), drv.In(w), drv.Out(exp_real), drv.Out(exp_imag), block = (t.size,1,1), grid = (w.size,1,1))

    return exp_real, exp_imag