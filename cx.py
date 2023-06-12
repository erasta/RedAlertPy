import contextily as cx
import matplotlib.pyplot as plt
import geopandas
from shapely.geometry import shape
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="red-alert-erasta")
location = geolocator.geocode("כרם שלום", geometry='geojson')
gdf = geopandas.GeoDataFrame({'geometry':[shape(location.raw['geojson'])]}, crs='EPSG:4326')
ax = gdf.plot(facecolor='none', edgecolor='red', linewidth=2)
plt.margins(2)
cx.add_basemap(ax=ax, crs=gdf.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik)
plt.title("")
plt.axis('off')
plt.savefig("a.png", bbox_inches="tight")
