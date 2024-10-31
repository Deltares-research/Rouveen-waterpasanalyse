import pandas as pd
import os
from pathlib import Path
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime


def calculate_distance_along_transect(transect_data):
    x0 = waterpas_data_transect["x"].iloc[0]
    y0 = waterpas_data_transect["y"].iloc[0]
    distance = np.sqrt(
        (waterpas_data_transect["x"] - x0) ** 2
        + (waterpas_data_transect["y"] - y0) ** 2
    )
    transect_data.insert(2, "s", distance)

    return transect_data


#####################################################
# parameters
#####################################################

farmers = ["01"]  # , "02", "05", "06", "07", "08", "09", "11"]
plot = "R"  # R voor referentieperceel of D voor maatregelenperceel
transect = "1"
season = "autumn"  # options are "winter" "spring" "summer" "autumn"

#####################################################
# code to create the plot
#####################################################

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

plot_names = {"R": "referentieperceel", "D": "maatregelenperceel"}

season_months = {
    "winter": "-01-|-02-|-03-",
    "spring": "-04-|-05-|-06-",
    "summer": "-07-|-08-|-09-",
    "autumn": "-10-|-11-|-12-",
}

colors = {
    "2018": "#000000",
    "2019": "#000000",
    "2020": "#000000",
    "2021": "#000000",
    "2022": "#000000",
    "2023": "#000000",
    "2024": "#000000",
}

# add the viridis colormap colors to each year
cmap = plt.get_cmap("viridis", len(colors))
for i, year in enumerate(colors):
    rgba = cmap(i)
    colors[year] = matplotlib.colors.rgb2hex(rgba)


xloc_text = {"R": 0.05, "D": 0.35}

for farmer in farmers:

    farmer_name = trans[farmer]
    print(f"Working on plot {farmer}")

    inputdir_path = Path(
        rf"n:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/2-interim/{farmer_name}"
    )

    outputdir_path = Path(
        rf"n:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}"
    )

    plot_name = plot_names[plot]

    path_to_waterpas_data = os.path.join(
        inputdir_path, f"{farmer_name}_waterpasdata_{plot_name}.csv"
    )

    # load the csv data
    waterpas_data = pd.read_csv(path_to_waterpas_data)
    waterpas_data = waterpas_data[waterpas_data["x"].notnull()]
    waterpas_data = waterpas_data.set_index(["metingnr"])  # , "x", "y"])

    fig, ax = plt.subplots(figsize=(8.27, 11.69 / 3))

    # check if row is in one of the transects
    mask = waterpas_data.index.str.contains(f"{farmer}{plot}{transect}")

    # select only the rows of that transect
    waterpas_data_transect = waterpas_data[mask]

    # calculate distance along transect
    waterpas_data_transect = calculate_distance_along_transect(waterpas_data_transect)

    waterpas_data_transect = waterpas_data_transect.reset_index()
    waterpas_data_transect = waterpas_data_transect.drop(columns=["metingnr", "x", "y"])
    waterpas_data_transect = waterpas_data_transect.set_index(["s"])

    waterpas_data_transect = waterpas_data_transect.filter(regex=season_months[season])

    for column in waterpas_data_transect:
        column_year = column.split("-")[0]
        ax.plot(
            waterpas_data_transect.index,
            waterpas_data_transect[column],
            linewidth=0.5,
            color=colors[column_year],
            label=column,
        )
        ax.scatter(
            waterpas_data_transect.index,
            waterpas_data_transect[column],
            color=colors[column_year],
            s=20,
        )

    ax.set_xlim(
        waterpas_data_transect.index.min(),
        waterpas_data_transect.index.max(),
    )

    ax.set_ylabel("Maaiveld hoogte \n t.o.v. NAP (m)", fontsize=12)
    ax.set_xlabel("Afstand langs transect (m)", fontsize=12)
    ax.set_title(f"Perceel  {farmer} - transect {transect}")

    ax.tick_params(axis="both", which="major", labelsize=12)

    ax.grid()

    ax.legend(
        bbox_to_anchor=(0.09, -0.18),
        ncols=3,
        loc="upper left",
        frameon=False,
        fontsize=12,
        title="Meting gedaan op",
        title_fontsize=12,
    )

    savefig_path = rf"N:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}/heights_transect_{transect}_{plot}_compare_years_{season}"
    plt.savefig(savefig_path + ".png", dpi=400, bbox_inches="tight")
    plt.close()
