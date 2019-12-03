import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import PyKeller.data.model as PKdm

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
    Psl = Psl.loc[time]
    
    uas_np = np.array(uas)
    vas_np = np.array(vas)
    X = np.array(uas.nav_lon_grid_M)
    Y = np.array(uas.nav_lat_grid_M)
    
    density = 1
    uas_np = PKdm.reduce_density(uas_np,density)
    vas_np = PKdm.reduce_density(vas_np,density)
    X = PKdm.reduce_density(X,density)
    Y = PKdm.reduce_density(Y,density)
    
    vec_scale = float(np.max(uas))*15
    
    ##########################################################################
    # Setting up the plot
    
    plt.figure(figsize=(7,7))
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    europe_land_10m = cfeature.NaturalEarthFeature('physical','land','10m',edgecolor='black',facecolor='none')
    ax.add_feature(europe_land_10m)    
    Psl.plot.contourf('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='rainbow',levels=30);
    plt.quiver(X,Y,uas_np,vas_np,transform=ccrs.PlateCarree(),scale=vec_scale,width=.0025);
    ax.set_extent([1,9.5,40,45.5],crs=ccrs.PlateCarree());
    plt.show()