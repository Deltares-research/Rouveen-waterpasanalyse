# this script writes the waterpas values from the excel file to a .csv,
# which is much faster to load

import pandas as pd

import os
from pathlib import Path

from load_gws_data import load_grondwater_data

dir_path = Path(
    r"N:\Projects\11202500\11202992\B. Measurements and calculations\Waterpassingen"
)

path_to_groundwater_data = os.path.join(
    dir_path, "Waterpassing bodemdaling Rouveen 2018-2023.xlsx"
)

#####################################################
# parameters - for which farmers do we want to update the data
#####################################################

farmers = ["07", "08", "09", "11"]
plots = ["R", "D"]

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

# plot = "R"
plots = ["R", "D"]
plot_names = {"R": "referentieperceel", "D": "maatregelenperceel"}

for farmer in farmers:

    farmer_name = trans[farmer]
    print(f"Reading data for plot {farmer}")

    outputdir_path = Path(
        rf"n:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/2-interim/{farmer_name}"
    )

    for plot in plots:

        plot_name = plot_names[plot]

        # load the groundwater data
        groundwater_data = load_grondwater_data(path_to_groundwater_data, farmer, plot)

        if not os.path.exists(outputdir_path):
            os.makedirs(outputdir_path)

        path_to_csv = os.path.join(
            outputdir_path, f"{farmer_name}_groundwaterlevel_{plot_name}.csv"
        )

        groundwater_data = pd.DataFrame.from_dict(groundwater_data)

        groundwater_data.to_csv(path_to_csv)
