# this script writes the waterpas values from the excel file to a .csv,
# which is much faster to load

import pandas as pd

import os
from pathlib import Path

from select_waterpas_data import select_waterpas_data

dir_path = Path(
    r"N:\Projects\11202500\11202992\B. Measurements and calculations\Waterpassingen"
)

path_to_metadata = os.path.join(dir_path, "Overzicht XY meetlijnen Rouveen 50m.xlsx")
path_to_waterpas_data = os.path.join(
    dir_path, "Waterpassing bodemdaling Rouveen 2018-2023.xlsx"
)

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


waterpas_data = pd.read_excel(
    path_to_waterpas_data, sheet_name="Hoogte tov NAP", header=8
)

for farmer in trans:

    farmer_name = trans[farmer]
    print(f"Loading and plotting data for plot {farmer}")

    # read the metadata
    metadata = pd.read_excel(path_to_metadata, sheet_name=farmer_name, header=3)

    outputdir_path = Path(
        rf"n:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/2-interim/{farmer_name}"
    )

    for plot in plots:

        plot_name = plot_names[plot]

        # select waterpas data
        waterpas_data_selection = select_waterpas_data(
            waterpas_data, metadata, farmer, plot
        )

        if not os.path.exists(outputdir_path):
            os.makedirs(outputdir_path)

        path_to_csv = os.path.join(
            outputdir_path, f"{farmer_name}_waterpasdata_{plot_name}.csv"
        )

        waterpas_data_selection.to_csv(path_to_csv)
