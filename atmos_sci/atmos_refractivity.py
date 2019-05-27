#Atmospheric Refractivity functions

def N_eq(P,T,e): #refractivity of the atmosphere
    #P is the atmospheric pressure; hPa or mb
    #T is the absolute temperature; K
    #e is the partial pressure of water vapor in the atmosphere; hPa or mb
    return 77.6*P/T + 3.73*10**5*e/T**2

def M_eq(N,z): #modified refractivity of the atmosphere; assumes the earth is flat
    #N is the refractivity
    #z is the vertical height
    return N + .157*z