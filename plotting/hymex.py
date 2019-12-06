import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import PyKeller.data.model as PKdm
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plotting_genoa_wrforch(Psl):
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    Psl.plot.contourf('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='rainbow',levels=30,vmin=98000,vmax=105000);
    ax.coastlines();
#    ax.set_extent([-2,20,37,50],crs=ccrs.PlateCarree());
    plt.show()
    
def plotting_genoa_winds_wrforch(uas,vas,Psl,time):
    uas = uas.loc[time]
    vas = vas.loc[time]
    Psl = Psl.loc[time]
    
    uas_np = np.array(uas)
    vas_np = np.array(vas)
    X = np.array(uas.nav_lon_grid_M)
    Y = np.array(uas.nav_lat_grid_M)
    
    density = 2
    uas_np = PKdm.reduce_density(uas_np,density)
    vas_np = PKdm.reduce_density(vas_np,density)
    X = PKdm.reduce_density(X,density)
    Y = PKdm.reduce_density(Y,density)
    
    vec_scale = float(np.max(uas))*25
    
    plt.figure(figsize=(7,7))
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    Psl.plot.contourf('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='rainbow',levels=25);
    plt.quiver(X,Y,uas_np,vas_np,transform=ccrs.PlateCarree(),scale=vec_scale,width=.001);
    ax.coastlines();
    ax.set_extent([-3,20,35,51],crs=ccrs.PlateCarree());
    plt.show()
    
def plotting_mistral_wrforch(uas,vas,Psl,time):
    ##########################################################################
    # Setting up the data
    uas = uas.loc[time]
    vas = vas.loc[time]
    Psl = Psl.loc[time]/100
    
    i = np.arange(58,110)
    j = np.arange(91,172)
    uas_np = np.array(uas[i,j])
    vas_np = np.array(vas[i,j])
    X = np.array(uas.nav_lon_grid_M[i,j])
    Y = np.array(uas.nav_lat_grid_M[i,j])
    Psl = Psl[i,j]
    
    density = 1
    uas_np = PKdm.reduce_density(uas_np,density)
    vas_np = PKdm.reduce_density(vas_np,density)
    X = PKdm.reduce_density(X,density)
    Y = PKdm.reduce_density(Y,density)
    
    ##########################################################################
    # Setting up the plot

    europe_land_10m = cfeature.NaturalEarthFeature('physical','land','10m',edgecolor='black',facecolor='none') 
    
    plt.figure(figsize=(8,8))
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    ax.add_feature(europe_land_10m)
   
    fig = Psl.plot.contourf('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='rainbow',levels=20); 
    plt.quiver(X,Y,uas_np,vas_np,transform=ccrs.PlateCarree(),width=.001);
    ax.set_extent([0,16,36.5,44],crs=ccrs.PlateCarree());
    
    fig.colorbar.remove()
    plt.colorbar(fig,fraction=0.030,pad=0.04,label='Sea Level Pressure [hPa]')
    plt.title(time[0:10])
    
    plt.show()
    plt.close()
