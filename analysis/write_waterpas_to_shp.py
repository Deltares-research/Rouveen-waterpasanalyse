import pandas as pd

import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point


def convert_to_gdf(df):
    x = df.index.get_level_values("x")
    y = df.index.get_level_values("y")

    geometry = [Point(xy) for xy in zip(x, y)]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:28992")

    return gdf


# these are all the farmers
trans = {
    "01": "01-Bouwman",
    "02": "02-DalFsen",
    "05": "05-Kronenberg",
    "06": "06-DenUyl",
    "07": "07-Post",
    "08": "08-Brandhof",
    "09": "09-Visscher",
    "11": "11-Petter",
}

plots = ["R", "D"]
plot_names = {"R": "referentieperceel", "D": "maatregelenperceel"}
colors = {
    "R": ["#CAE0AB", "#4EB265", "royalblue"],
    "D": ["#F6C141", "#E8601C", "turquoise"],
}
xloc_text = {"R": 0.05, "D": 0.35}
tov_t0 = True

for farmer in trans:

    farmer_name = trans[farmer]
    print(f"Working on plot {farmer}")

    inputdir_path = Path(
        rf"n:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/2-interim/{farmer_name}"
    )

    outputdir_path = Path(
        rf"n:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}"
    )

    for plot in plots:

        plot_name = plot_names[plot]

        path_to_waterpas_data = os.path.join(
            inputdir_path, f"{farmer_name}_waterpasdata_{plot_name}.csv"
        )

        # load the csv data
        waterpas_data = pd.read_csv(path_to_waterpas_data)
        waterpas_data = waterpas_data.drop(columns="metingnr")
        waterpas_data = waterpas_data.set_index(["x", "y"])
        waterpas_data.columns = [
            f"T{i}" for i in range(len(waterpas_data.columns))
        ]  # column names

        # difference with previous time point
        waterpas_data_diff = waterpas_data.diff(axis=1).dropna(axis=1, how="all")
        column_names = []
        for i in range(1, len(waterpas_data.columns)):
            column_names.append(
                f"{waterpas_data.columns[i]}-{waterpas_data.columns[i-1]}"
            )
        waterpas_data_diff.columns = column_names

        # difference with first time point
        waterpas_data_diff_t0 = waterpas_data.sub(
            waterpas_data[waterpas_data.columns[0]], axis=0
        )
        waterpas_data_diff_t0 = waterpas_data_diff_t0.drop(columns="T0")
        column_names = []
        for i in range(1, len(waterpas_data.columns)):
            column_names.append(
                f"{waterpas_data.columns[i]}-{waterpas_data.columns[0]}"
            )
        waterpas_data_diff_t0.columns = column_names

        h_final = pd.concat(
            [waterpas_data, waterpas_data_diff, waterpas_data_diff_t0], axis=1
        )

        h_final = h_final.loc[:, ~h_final.columns.duplicated()].copy()

        # gdf_h = convert_to_gdf(waterpas_data.copy())
        gdf_h = convert_to_gdf(h_final.copy())

        # write waterpas data to a shapefile
        path_for_shapefile = rf"N:/Projects/11202500/11202992/B. Measurements and calculations/Waterpasmetingen_shapefiles/{farmer_name}_{plot}.shp"
        gdf_h.to_file(path_for_shapefile)
