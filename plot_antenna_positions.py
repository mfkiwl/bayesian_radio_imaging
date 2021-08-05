import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from astropy.coordinates import EarthLocation
from astropy import units as u
from cartopy.io.img_tiles import MapQuestOpenAerial
import numpy as np

def plot_antenna_positions(ant_p):

    ant_pos = [EarthLocation.from_geocentric(a[0], a[1], a[2], unit=u.meter) for a in ant_p]
    
    ant_deg = [ { 'lat': float(pos.lat/u.deg), 'lon': float(pos.lon/u.deg) } for pos in ant_pos]
    
    ant_lat = np.array([ float(pos.lat/u.deg) for pos in ant_pos])
    ant_lon = np.array([ float(pos.lon/u.deg) for pos in ant_pos])

    ant_num = np.arange(len(ant_pos))
    # Find the centroid
    
    center_lon = np.mean(ant_lon)
    center_lat = np.mean(ant_lat)


    dlat = np.max(ant_lat) - center_lat
    dlon = np.max(ant_lon) - center_lon

    fig = plt.figure(figsize=(9,9))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=center_lon, central_latitude=center_lat))
    #ax.set_extent([center_lon-dlon, center_lon+dlon, center_lat+dlat, center_lat-dlat], crs=ccrs.PlateCarree())
    data_crs = ccrs.PlateCarree()

    # define the coordinate system that the grid lons and grid lats are on
    for i, lat, lon in zip(ant_num, ant_lat, ant_lon):
        plt.plot(lat, lon, '.', color='k', alpha=0.2)
        plt.annotate(f'{i}', (lat, lon), fontsize=4, va="center", ha="center")


    #ax.coastlines()
    ax.add_image(MapQuestOpenAerial(), 2)
    #ax.add_image(cartopy.io.img_tiles.GoogleTiles(cache=True))
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.left_labels = False


    plt.title(r"Meerkat Antenna Positions", fontsize=16, color='k')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig('meerkat_antennas.pdf')
    plt.tight_layout()

    plt.show()

    
