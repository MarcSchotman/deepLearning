# -*- coding: utf-8 -*-
"""
Created on Mon May 21 17:58:35 2018

@author: Taeke
"""
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os.path

def plot_stations(stations, lattitudeCenter, longitudeCenter, radius):
    imagePath = os.path.join('fig', 'basemap')
    
    m = Basemap(width=5000 * radius, height=5000 * radius, projection='lcc', # hammer
                resolution='i', lat_1=lattitudeCenter - 20, 
                lat_2=lattitudeCenter + 20, lat_0=lattitudeCenter, 
                lon_0=longitudeCenter)
    # m = Basemap(projection='hammer',lon_0=0, lon_1=-20.,lon_2=20 ,resolution='i')  #width=12000000, height=9000000, 
    #(projection = 'merc', llcrnrlat=30, urcrnrlat=90, llcrnrlon=-30, urcrnrlon=-35)
    
    m.drawstates()
    m.drawcoastlines()
    m.fillcontinents (color='lightgray', lake_color='lightblue')
    # m.drawparallels(np.arange(-90.,91.,30.))
    # m.drawmeridians(np.arange(-180.,181.,60.))
    m.drawmapboundary(fill_color='aqua')
    
    m.drawcountries(linewidth=0.6, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
    x, y = m(stations['LON'],stations['LAT'])
    m.plot(x,y, marker ='o', markersize=5, markerfacecolor='red', linewidth=0)
    #
    plt.title('Selected stations')
    plt.show()    
    
    plt.savefig(imagePath + '.eps')