import pandas as pd
import geopandas as gpd
from pyproj import Transformer

OPERATEURS = {
    '20801': 'Orange',
    '20810': 'SFR',
    '20815': 'Free',
    '20820': 'Bouygue'
}

def get_datasheet_with_long_lat():
    # 1. Load your CSV
    df = pd.read_csv('lambert93_mobile_coverage.csv', sep=';')

    # 2. Convert Lambert93 to WGS84 using vectorized transform
    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    df["lon"], df["lat"] = transformer.transform(df["x"].values, df["y"].values)

    # 3. Convert to GeoDataFrame
    gdf_points = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.lon, df.lat),
        crs="EPSG:4326"
    )

    # 4. Load French city boundaries (communes)
    communes = gpd.read_file("COMMUNES.geojson")
    communes = communes.to_crs("EPSG:4326")         # Make sure CRS matches

    # 5. Spatial join to find city for each point
    joined = gpd.sjoin(gdf_points, communes[["geometry", "nom"]], how="left", predicate="within")

    # 6. Rename and export
    joined = joined.drop(columns=["x", "y", "geometry", "index_right"])
    joined.rename(columns={"nom": "city"}, inplace=True)
    del joined['lon'], joined['lat']

    joined.drop_duplicates(
        inplace=True, 
        subset=['Operateur', 'city'], 
        keep='first'
    )

    joined['Operateur'] = joined['Operateur'].astype(str)
    joined['Operateur'] = joined['Operateur'].apply(lambda x: OPERATEURS.get(x))
    joined['city'] = joined['city'].str.lower()
    joined.rename({'Operateur': 'operator'}, inplace=True)

    joined.dropna(inplace=True)

    joined.to_csv("city_mobile_coverage.csv", sep=";", index=False)
