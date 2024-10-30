import pandas as pd
import numpy as np

import os
from pathlib import Path

from make_figs import plot_spatial

#####################################################
# parameters
#####################################################

farmers = ["01", "02", "05", "06", "07", "08", "09", "11"]
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

plot_names = {"R": "referentieperceel", "D": "maatregelenperceel"}

for farmer in farmers:

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
        waterpas_data = waterpas_data.set_index(["metingnr", "x", "y"])

        dates = waterpas_data.columns
        waterpas_data_diff = waterpas_data.diff(axis=1)
        waterpas_data_diff_dev = waterpas_data_diff - waterpas_data_diff.mean()

        for i in range(1, len(dates)):
            title = (
                f"Afwijking hoogteverandering {plot_name}\n {dates[i-1]} - {dates[i]}"
            )

            vmin = -0.02
            vmax = 0.02
            fpath = os.path.join(
                outputdir_path,
                f"Afwijking_hoogteverandering_{plot_name}_{dates[i]}.png",
            )
            plot_spatial(
                waterpas_data_diff_dev,
                dates[i],
                title,
                "RdYlGn_r",
                vmin,
                vmax,
                "afwijking t.o.v. gem. hoogteverandering (m)",
                fpath,
            )
