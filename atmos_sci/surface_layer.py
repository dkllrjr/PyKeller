# Surface Layer functions

import numpy as np

def potential_temperature(temp,pressure):
    return temp*(101300/pressure)**(2/7)

def obukhov_length(u_prime,v_prime,w_prime,pot_temp,pot_temp_prime):
    k = .41
    return - friction_velocity(u_prime,v_prime,w_prime)**3 * pot_temp / (k * 9.81 * np.mean(w_prime*pot_temp_prime))
    
def obukhov_stability(z,L):
    return z/L

def friction_velocity(u_prime,v_prime,w_prime):
    return (np.mean(u_prime*w_prime)**2 + np.mean(v_prime*w_prime)**2)**(1/4)