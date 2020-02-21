import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import PyKeller.data.model as PKdm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def genoa_wrforch(Psl):
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    Psl.plot.contourf('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='rainbow',levels=30,vmin=98000,vmax=105000);
    ax.coastlines();
#    ax.set_extent([-2,20,37,50],crs=ccrs.PlateCarree());
    plt.show()
    
def genoa_winds_wrforch(uas,vas,Psl,time):
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
    
def mistral_wrforch(uas,vas,Psl,time,save=False):
    ##########################################################################
    # Setting up the data
    uas = uas.loc[time]
    vas = vas.loc[time]
    Psl = Psl.loc[time]/100
    
#    i = np.arange(58,110)
#    j = np.arange(91,172)
    i = np.arange(58,132)
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
#    ax.set_extent([0,16,36.5,44],crs=ccrs.PlateCarree());
    ax.set_extent([0,16,36.5,48],crs=ccrs.PlateCarree());
    
    fig.colorbar.remove()
    plt.colorbar(fig,fraction=0.030,pad=0.04,label='Sea Level Pressure [hPa]')
    plt.title(time[0:10])
    if save:
        pic_path = '/homedata/dkeller/ClimServ/python/looking_for_Mistrals/wind_vector_pics/'
        plt.savefig(pic_path+'wind_pres_'+time[0:10]+'.png')
    plt.show()
    plt.close()
    
def mistral_isobar(uas,vas,Psl,time,fname_path=None,wind_min=None,wind_max=None):
    ##########################################################################
    # Setting up the data
    uas = uas.loc[time]
    vas = vas.loc[time]
    Psl = Psl.loc[time]/100
    
    i = np.arange(57,132)
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
    
    wind_mag = (uas_np**2 +  vas_np**2)**.5
    
    ##########################################################################
    # Setting up the plot

    europe_land_10m = cfeature.NaturalEarthFeature('physical','land','10m',edgecolor='black',facecolor='none') 
    
    plt.figure(figsize=(8,8))
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    ax = plt.axes(projection=ccrs.Mercator());
    ax.add_feature(europe_land_10m)
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=.75, color='black', alpha=0.35, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlocator = mticker.FixedLocator([-90,2,6,10,14,90])
    gl.ylocator = mticker.FixedLocator([0,38,41,44,47,60])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
   
    cs = Psl.plot.contour('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='black',levels=20,linewidths=1);
    fig = plt.contourf(X,Y,wind_mag,transform=ccrs.PlateCarree(),cmap='rainbow',levels=30,vmin=wind_min,vmax=wind_max);
    plt.quiver(X,Y,uas_np,vas_np,transform=ccrs.PlateCarree(),width=.001);
    ax.set_extent([0,16,36,48],crs=ccrs.PlateCarree());
    
    if wind_min != None:
        cbar = plt.cm.ScalarMappable(cmap='rainbow')
        cbar.set_array(wind_mag)
        cbar.set_clim(wind_min,wind_max)
        plt.colorbar(cbar,fraction=0.030,pad=0.04,label='Wind Magnitude [m/s]',boundaries=np.linspace(wind_min,wind_max,30))
    else:
        plt.colorbar(fig,fraction=0.030,pad=0.04,label='Wind Magnitude [m/s]')

    plt.clabel(cs,fontsize=6,fmt='%1.1f')
    
    plt.title(time[0:10]+' Wind/Pressure Plot')
    if fname_path != None:
        plt.savefig(fname_path+'mistral_isobar_'+time[0:10]+'.png')
    
    plt.show()
    plt.close()

def mediterranean_isobar(uas,vas,Psl,time,fname_path=None,wind_min=None,wind_max=None,save=False):
    ##########################################################################
    # Setting up the data
    uas = uas.loc[time]
    vas = vas.loc[time]
    Psl = Psl.loc[time]/100
    
    print(uas.nav_lat_grid_M)
    i = np.arange(0,192)
    j = np.arange(0,300)
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
    
    wind_mag = (uas_np**2 +  vas_np**2)**.5
    
    ##########################################################################
    # Setting up the plot

    europe_land_10m = cfeature.NaturalEarthFeature('physical','land','10m',edgecolor='black',facecolor='none') 
    
    plt.figure(figsize=(8,8))
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    ax = plt.axes(projection=ccrs.Mercator());
    ax.add_feature(europe_land_10m)
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=.75, color='black', alpha=0.35, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlocator = mticker.FixedLocator([-90,2,6,10,14,90])
    gl.ylocator = mticker.FixedLocator([0,38,41,44,47,60])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
   
    cs = Psl.plot.contour('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='black',levels=20,linewidths=1); 
    fig = plt.contourf(X,Y,wind_mag,transform=ccrs.PlateCarree(),cmap='rainbow',levels=30);
    plt.quiver(X,Y,uas_np,vas_np,transform=ccrs.PlateCarree(),width=.001);
#    ax.set_extent([0,16,36,48],crs=ccrs.PlateCarree());
    
    if wind_min != None:
        cbar = plt.cm.ScalarMappable(cmap='rainbow')
        cbar.set_array(wind_mag)
        cbar.set_clim(wind_min,wind_max)
        plt.colorbar(cbar,fraction=0.030,pad=0.04,label='Wind Magnitude [m/s]',boundaries=np.linspace(wind_min,wind_max,30))
    else:
        plt.colorbar(fig,fraction=0.030,pad=0.04,label='Wind Magnitude [m/s]')
        
    plt.clabel(cs,fontsize=6,fmt='%1.1f')
    
    plt.title(time[0:10]+' Wind/Pressure Plot')
    
    if save:
        plt.savefig(fname_path+'mistral_isobar_'+time[0:10]+'.png')
    
    plt.show()
    plt.close()
    
def wind_time_series(wm,t,file_path):
    
    plt.figure(figsize=(24,4),dpi=200)
    plt.plot(t,wm)
    plt.yticks(fontsize=12)
    plt.xticks(t[::146],fontsize=12)
    plt.xlim([t[0],t[-1]])
    plt.xlabel('Time',fontsize=14)
    plt.ylabel('Wind Speed (m/s)',fontsize=14)
    plt.tight_layout()
    plt.savefig(file_path)
    