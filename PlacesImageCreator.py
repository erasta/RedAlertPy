import json
from random import randrange
import contextily as cx
import matplotlib.pyplot as plt
import geopandas
import pandas
from shapely.geometry import shape
from geopy.geocoders import Nominatim

from Alert import Alert


class PlacesImageCreator:
    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent="red-alert-erasta-" + str(randrange(10000)))
        coords_df = pandas.read_csv("places_coords.csv")
        self.coords_gdf = geopandas.GeoDataFrame(
            coords_df, geometry=geopandas.points_from_xy(coords_df.long, coords_df.lat), crs="EPSG:4326"
        )

    @staticmethod
    def stretch_gdf_plot(gdf, ax, meters):
        xmin, ymin, xmax, ymax = gdf.total_bounds
        # print(xmin, ymin, xmax, ymax)
        dx, dy = xmax - xmin, ymax - ymin
        side = max(dx, dy) + meters / 111139
        xmarg, ymarg = (side - dx) / 2, (side - dy) / 2
        ax.set_xlim(xmin - xmarg, xmax + xmarg)
        ax.set_ylim(ymin - ymarg, ymax + ymarg)

    def location_to_geom(self, name):
        # TODO cache locations by name in json 
        loc = self.geolocator.geocode(name, geometry="geojson", timeout=10)
        if loc is not None:
            poly = loc.raw["geojson"]
            return shape(poly)
        point = self.coords_gdf[self.coords_gdf["loc"].isin([name])]
        if len(point) > 0:
            return point["geometry"].iloc[0]
        return None

    def places_to_gdf(self, names):
        geoms = [self.location_to_geom(n) for n in names]
        geoms_filtered = [g for g in geoms if g is not None]
        gdf = geopandas.GeoDataFrame({"geometry": geoms_filtered}, crs="EPSG:4326")
        places_not_geolocated = [n for g, n in zip(geoms, names) if g is None]
        print("not found:", Alert.reverse_if_needed(places_not_geolocated))

        return gdf

    def places_to_image(self, names, add_title=False):
        gdf = self.places_to_gdf(names)
        fig = self.gdf_to_image(gdf)
        if add_title:
            fig.get_axes()[0].set_title("".join(reversed(" ".join(names))))
        return fig

    def gdf_to_image(self, gdf, add_title=False):
        fig = plt.figure(dpi=300)
        if gdf.empty:
            im, bbox = cx.bounds2img(
                34.159707, 31.208131, 34.694511, 31.636780, ll=True, source=cx.providers.OpenStreetMap.Mapnik
            )
            plt.imshow(im)
            ax = fig.get_axes()[0]
        else:
            ax = gdf.plot(facecolor="none", edgecolor="red", linewidth=1, ax=plt.gca())
            self.stretch_gdf_plot(gdf, ax, 10000)
            cx.add_basemap(
                ax=ax,
                crs=gdf.crs.to_string(),
                source=cx.providers.OpenStreetMap.Mapnik,
                attribution=False,
            )
        ax.set_title("")
        ax.axis("off")
        return fig

    @staticmethod
    def savefig(fig, filename, also_show=False):
        fig.savefig(filename, bbox_inches="tight")
        if also_show:
            fig.get_axes()[0].set_title("".join(reversed(" ".join(names))))
            plt.draw()
            plt.waitforbuttonpress(0)
            plt.close()


if __name__ == "__main__":
    names = ["אזור עוטף עזה", "כרם שלום", "שדרות", "תל אביב", "אזור תעשייה הדרומי אשקלון", "אזור מערב לכיש"]
    # names = ["אזור עוטף עזה"]
    creator = PlacesImageCreator()
    # fig = creator.gdf_to_image(creator.coords_gdf)
    # creator.savefig(fig, "coords.png", False)
    fig = creator.places_to_image(names, True)
    creator.savefig(fig, "a.png", False)
