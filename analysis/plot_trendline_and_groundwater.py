import pandas as pd
import datetime as datetime

import os
from pathlib import Path

from make_figs import plot_trendline_and_groundwater
from calc_stats import calculate_trendline

start_time = datetime.datetime.now()

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

plots = ["R"]  # , "D"]
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

    if not os.path.exists(outputdir_path):
        os.makedirs(outputdir_path)

    for plot in plots:

        plot_name = plot_names[plot]

        path_to_waterpas_data = os.path.join(
            inputdir_path, f"{farmer_name}_waterpasdata_{plot_name}.csv"
        )

        # load the csv data
        waterpas_data = pd.read_csv(path_to_waterpas_data)
        waterpas_data = waterpas_data.set_index(["metingnr", "x", "y"])

        h_mean = waterpas_data.mean(axis=0).to_frame("gem. hoogte")
        h_mean.index = pd.to_datetime(h_mean.index)

        # dit is een mask voor de winter maanden
        winter_indices = h_mean.index.month.isin([1, 2])

        x, regression_line, stats_text = calculate_trendline(
            h_mean, winter_indices, tov_t0=tov_t0
        )

        # load the groundwater csv data
        path_to_groundwater_data = os.path.join(
            inputdir_path, f"{farmer_name}_groundwaterlevel_{plot_name}.csv"
        )
        groundwater_data = pd.read_csv(path_to_groundwater_data, index_col=0)
        groundwater_data.index = pd.to_datetime(groundwater_data.index)

        plot_trendline_and_groundwater(
            groundwater_data[f"GW-{farmer}"],
            h_mean,
            winter_indices,
            farmer_name,
            plot,
            x,
            regression_line,
            stats_text,
            xloc_text[plot],
            colors=colors[plot],
            label=plot_name,
            tov_t0=tov_t0,
        )

end_time = datetime.datetime.now()

elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time.seconds, "Seconds")
