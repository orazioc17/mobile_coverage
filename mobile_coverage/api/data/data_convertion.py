import pandas as pd
import geopandas as gpd
from pyproj import Transformer

from api.utils.constants import OPERATEURS


def get_datasheet_with_long_lat():
    df = pd.read_csv("lambert93_mobile_coverage.csv", sep=";")

    # Converting Lambert93 to WGS84 using vectorized transform
    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    df["lon"], df["lat"] = transformer.transform(df["x"].values, df["y"].values)

    gdf_points = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326"
    )

    communes = gpd.read_file("communes.gpkg", layer="COMMUNE")
    communes = communes.to_crs("EPSG:4326")

    # Spatial join to find city for each point
    joined = gpd.sjoin(
        gdf_points,
        communes[["geometry", "nom_officiel"]],
        how="left",
        predicate="within",
    )

    joined = joined.drop(columns=["x", "y", "geometry", "index_right"])
    joined.rename(columns={"nom_officiel": "city"}, inplace=True)
    del joined["lon"], joined["lat"]

    joined.drop_duplicates(inplace=True, subset=["Operateur", "city"], keep="first")

    joined["Operateur"] = joined["Operateur"].astype(str)
    joined["Operateur"] = joined["Operateur"].apply(lambda x: OPERATEURS.get(x))
    joined["city"] = joined["city"].str.lower()
    joined.rename(columns={"Operateur": "operator"}, inplace=True)

    joined.dropna(inplace=True)

    joined.to_csv("city_mobile_coverage.csv", sep=";", index=False)
