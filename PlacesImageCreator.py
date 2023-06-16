import contextily as cx
import matplotlib.pyplot as plt
import geopandas
from shapely.geometry import shape
from geopy.geocoders import Nominatim

from Alert import revstr


class PlacesImageCreator:
    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent="red-alert-erasta")

    @staticmethod
    def stretch_gdf_plot(gdf, ax, meters):
        xmin, ymin, xmax, ymax = gdf.total_bounds
        # print(xmin, ymin, xmax, ymax)
        dx, dy = xmax - xmin, ymax - ymin
        side = max(dx, dy) + meters / 111139
        xmarg, ymarg = (side - dx) / 2, (side - dy) / 2
        ax.set_xlim(xmin - xmarg, xmax + xmarg)
        ax.set_ylim(ymin - ymarg, ymax + ymarg)

    def places_to_gdf(self, names):
        locations = [self.geolocator.geocode(n, geometry="geojson") for n in names]
        if any([l is None for l in locations]):
            print("not geolocated:", [revstr(n) for l, n in zip(locations, names) if l is None])
        polys = [l.raw["geojson"] for l in locations if l is not None]
        geom = [shape(i) for i in polys]
        gdf = geopandas.GeoDataFrame({"geometry": geom}, crs="EPSG:4326")
        return gdf

    def places_to_image(self, names, add_title=False, dpi=300, meters_buf=10000):
        gdf = self.places_to_gdf(names)
        # print(gdf)

        fig = plt.figure(dpi=300)
        ax = gdf.plot(facecolor="none", edgecolor="red", linewidth=1, ax=plt.gca())
        self.stretch_gdf_plot(gdf, ax, 10000)

        cx.add_basemap(
            ax=ax,
            crs=gdf.crs.to_string(),
            source=cx.providers.OpenStreetMap.Mapnik,
            attribution=False,
        )
        if add_title:
            ax.set_title("".join(reversed(" ".join(names))))
        else:
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
    creator = PlacesImageCreator()
    fig = creator.places_to_image(names)
    creator.savefig(fig, "a.png", False)
