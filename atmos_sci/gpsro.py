
import numpy as np

class Layer: #class to store a compressed layer from radiosonde
    
    def __init__(self,z_bottom,z_top,T_bottom,T_top,slope,intercept):
        self.z_bottom = z_bottom #layer bottom height
        self.z_top = z_top #layer top height
        self.T_bottom = T_bottom #temperature at layer bottom
        self.T_top = T_top #temperature at layer top
        self.slope = slope #slope of the compressed layer linear fit
        self.intercept = intercept #intercept point of the compressed layer linear fit
        
class Inversion: #class to store temperature inversion information

    def __init__(self,inv_bottom,inv_top,temp_bottom,temp_top,layer):
        self.inv_bottom = inv_bottom #inversion bottom
        self.inv_top = inv_top #inversion top
        self.temp_bottom = temp_bottom #temperature at the inversion bottom
        self.temp_top = temp_top #temperature at the inversion top
        self.layer = layer #elevated or surface based inversion
    
def layer_fitting(z,T,error):

    def layer_fit(z,T,beg,end,error):

        def temp_fit(x,y):
            p = np.polyfit(np.array([x[0],x[x.size-1]]),np.array([y[0],y[y.size-1]]),1)
            y_fit = np.poly1d(p)(x)
            e_fit = np.linalg.norm(y_fit-y)
            return e_fit,p
            
        e = 1
        l = end+1
        while e >= error and l-beg > 1:
            l -= 1
            e,p = temp_fit(z[beg:l+1],T[beg:l+1])
        return p,l
        
    layers = []
#    z = z[~np.isnan(T)] #removing nans
#    T = T[~np.isnan(T)] #removing nans
    beg = 0
    end = z.size-1
    while end-beg >= 1:
        z_bottom = z[beg]
        T_bottom = T[beg]
        poly,beg = layer_fit(z,T,beg,end,error) #beg is now the returned endpoint
        z_top = z[beg]
        T_top = T[beg]
        slope = poly[0]
        intercept = poly[1]
        layer = Layer(z_bottom,z_top,T_bottom,T_top,slope,intercept)
        layers.append(layer)
    return layers
    
def get_inversions(layers):
    
    inversions = []
    n = 0
    m = 1
    for i in range(0,len(layers)-1):
        if np.sign(layers[i].slope) == -1:
            n = n + 1
        if np.sign(layers[i].slope) == 1 and np.sign(layers[i+1].slope) == -1:
            inv_bottom = layers[n].z_bottom
            inv_top = layers[i].z_top
            temp_bottom = layers[n].T_bottom
            temp_top = layers[i].T_top
            if n == 0:
                layer = 'surfased based inversion'
            else:
                layer = 'elevated inversion ' + str(m)
                m += 1
            n = i + 1
            inversion = Inversion(inv_bottom,inv_top,temp_bottom,temp_top,layer)
            inversions.append(inversion)
    return inversions

def ntom(n,y,a):
    return n*(y/a+1)

def Nton(N):
    return N * 10e-6 + 1

def kfunc(y,n):
    return np.gradient(np.log(n),y)