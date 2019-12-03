import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs

def plotting_genoa(Psl):
    ax = plt.axes(projection=ccrs.Orthographic(8.9558,43.555));
    Psl.plot.contourf('nav_lon_grid_M','nav_lat_grid_M',ax=ax,transform=ccrs.PlateCarree(),cmap='rainbow',levels=30,vmin=98000,vmax=105000);
    ax.coastlines();
#    ax.set_extent([-2,20,37,50],crs=ccrs.PlateCarree());
    plt.show()