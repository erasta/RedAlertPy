import contextily as cx
import matplotlib.pyplot as plt
import geopandas

# data_url = "https://ndownloader.figshare.com/files/20232174"
# db = geopandas.read_file(data_url)
# ax = db.plot(color="red", figsize=(9, 9))
# cx.add_basemap(ax, crs=db.crs.to_string())

# madrid = cx.Place("כרם שלום")
# print(1)
# ax = madrid.plot()
# plt.show()

# for a in cx.providers:
#     print(a)
# cx.Place('כרם שלום')
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="red-alert-erasta")
# location = geolocator.geocode("כרם שלום")
# location = geolocator.geocode("תל אביב")
# for v in location:
#     print(v)
# print(location.address)
# print((location.latitude, location.longitude))
# print(location.raw)

# print(location.point)
location = geolocator.geocode("כרם שלום", geometry='geojson')
# print(location.raw['geojson'])

from shapely.geometry import shape
# geom = [shape(i) for i in polys]
gdf = geopandas.GeoDataFrame({'geometry':[shape(location.raw['geojson'])]}, crs='EPSG:4326')

# place = cx.Place(location, source=cx.providers.OpenStreetMap.Mapnik)
# geolocator.reverse(place)
# place = cx.Place(location, source=cx.providers.OpenStreetMap.Mapnik)
# print(place)
# place = cx.Place(location, source=cx.providers.OpenStreetMap.Mapnik)
# print(2)
ax = gdf.plot(facecolor='none', edgecolor='red', lw=1)
cx.add_basemap(ax=ax, crs=gdf.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik)
plt.title("")
plt.axis('off')
plt.savefig("a.png", bbox_inches="tight")
