#Created: Wed May 29 20:46:29 2019
#By: mach

function [turb,wind]=turb_calc(sonic,periodo)
%% Input here is the structure containing information from the sonic anemometer
%% ---outputs are turb components and mean wind parameters
turb=[];
wind=[];
%-----calculate uprime, vprime, wprime, thetaprime and the wind speed and
%wind direction
%INPUT: jd: julian day in UTC and sonic:structure containing the sonic
%anemometers data
jd=sonic.jd;
u=sonic.u;
v=sonic.v;
w=sonic.w;
T=sonic.ts;
%



class Velocity:
    
    def __init__(self,u,v,w,time):
        self.time = time
        self.u = u
        self.v = v
        self.w = w
        
        
        
        
class Turbulence:
    
    def __init__(self,u,v,w,t,period):
        u_mean, u_prime, t_mean, t_prime = reynolds_decomposition(u,t,period)
        v_mean, v_prime, _, _ = reynolds_decomposition(u,t,period)
        w_mean, w_prime, _, _ = reynolds_decomposition(u,t,period)
        self.period = period
        self.u_mean = u_mean
        self.u_prime = u_prime
        self.v_mean = v_mean
        self.v_prime = v_prime
        self.w_mean = w_mean
        self.w_prime = w_prime     
    
def reynolds_decomposition(x,t,period):
    #period is in minutes, assuming t is in seconds
    Ts = t[1] - t[0]
    L = period*60/Ts
    t_mean = []
    t_prime = []
    x_mean = []
    x_prime = []
    for i in range(t.size//L):
        x_mean.append(np.nanmean(x[i*L:i*L+L+1]))
        x_prime.append(x[i*L:i*L+L+1]-x_mean[-1])
        t_mean.append(np.nanmean(t[i*L:i*L+L+1]))
        t_prime.append(t[i*L:i*L+L+1])
    x_mean = np.array(x_mean)
    x_prime = np.array(x_prime)
    t_mean = np.array(t_mean)
    t_prime = np.array(t_prime)
    return x_mean, x_prime, t_mean, t_prime

L=floor(length(jd)/periodo);
disp('Number of periods ...')
disp(L);

#%----shrinking vectors to an integer number of periods for EC calculation

u=u(1:L*periodo);
v=v(1:L*periodo);
w=w(1:L*periodo);
T=T(1:L*periodo);
jd=jd(1:L*periodo);

#%----wind direction 

wdir = 180/pi*atan2(v,u);

#%-----reshaping the temporal series into matrices to start processing

u1 = reshape(u,periodo,L);
v1 = reshape(v,periodo,L);
w1 = reshape(w,periodo,L);
T1 = reshape(T,periodo,L);
jd1= reshape(jd,periodo,L);
wdir1= reshape(wdir,periodo,L);
T3 = T1;
T3 = mean(T3);















%-----------------------
%----Correction for tilt in u,v,w-After this step w and v will have zero-mean
%and the WS=sqrt(u^2+v^2) wil be equal to u
u2=[];v2=[];w2=[];
for k=1:L
    [u2(:,k),v2(:,k),w2(:,k)]=tilt_correction(u1(:,k),v1(:,k),w1(:,k));
end
%----Detrend temperature
%----Detrending the series
 for k=1:L,
    %[p,s] = polyfit(jd1(:,k),u1(:,k),1);
    %u1(:,k) = u1(:,k)-(p(1)*jd1(:,k)+p(2));
    %[p,s] = polyfit(jd1(:,k),v1(:,k),1);
    %v1(:,k) = v1(:,k)-(p(1)*jd1(:,k)+p(2));
    %[p,s] = polyfit(jd1(:,k),w1(:,k),1);
    %w1(:,k) = w1(:,k)-(p(1)*jd1(:,k)+p(2));
    [p,s] = polyfit(jd1(:,k),T1(:,k),1);
    T1(:,k) = T1(:,k)-(p(1)*jd1(:,k)+p(2));
 end

%----Calculate Tprime & up by substracting means by blocks and wind speed module
%TM = mean(T1);
%UM = mean(u2);
Tp = [];
ws = [];
for k=1:L
    Tp(:,k) = T1(:,k) - mean(T1(:,k));
    ws(:,k) = sqrt(u2(:,k).^2+v2(:,k).^2);
    uc(:,k) = u2(:,k) - mean(u2(:,k));
end
%Outputs turbulent variables matrices to vectors
jd = reshape(jd1,periodo*L,1);
uc = reshape(uc,periodo*L,1); 
vc = reshape(v2,periodo*L,1); 
wc = reshape(w2,periodo*L,1); 
Tc= reshape(Tp,periodo*L,1); 
%output mean wind components
ws = mean(ws); 
wdir= mean(wdir1);
jd1=mean(jd1);
%----generating output structures
turb.jd=jd;
turb.up=uc;
turb.vp=vc;
turb.wp=wc;
turb.tp=Tc;
wind.jd = jd1;
wind.ws = ws;
wind.wd = wdir;
wind.T = T3;
%---------------------END------------------------------

function [u2,v2,w2]=tilt_correction(u,v,w)
%u,v,w are the three wind components LEV1 form the sonic anemometer at
%one-height half hour data only
%rotation around the horizontal axis into the mean wind direction
vm = mean(v);
um = mean(u);
wm = mean(w);
theta = atan(vm / um);
%theta-Rotation 
u1 = u * cos(theta) + v * sin(theta);
v1 = -u * sin(theta) + v * cos(theta);
w1 = w;
%phi-Rotation
%once the y-axis is compensated (mean =0) we rotates around it to reduce
%the mean vertical wind component
u1m = mean(u1);
phi = atan(wm / u1m);
u2 = u1 * cos(phi) + w1 * sin(phi);
v2 = v1; 
w2 = -u1 * sin(phi) + w1 * cos(phi);