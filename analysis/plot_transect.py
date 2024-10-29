import pandas as pd
import os
from pathlib import Path

import matplotlib.pyplot as plt

# these are all the farmers
trans = {
    # "01": "01-Bouwman",
    # "02": "02-DalFsen",
    "05": "05-Kronenberg",
    # "06": "06-DenUyl",
    # "07": "07-Post",
    # "08": "08-Brandhof",
    # "09": "09-Visscher",
    # "11": "11-Petter",
}

transects = ["1", "2"]

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

    for plot in plots:

        plot_name = plot_names[plot]

        path_to_waterpas_data = os.path.join(
            inputdir_path, f"{farmer_name}_waterpasdata_{plot_name}.csv"
        )

        # load the csv data
        waterpas_data = pd.read_csv(path_to_waterpas_data)
        waterpas_data = waterpas_data.set_index(["metingnr", "x", "y"])

        # use single index for selecting
        waterpas_data.index = waterpas_data.index.get_level_values("metingnr")

        fig, ax = plt.subplots(figsize=(8.27, 11.69 / 2))

        for transect in transects:
            # check if row is in one of the transects
            mask = waterpas_data.index.str.contains(f"{farmer}{plot}{transect}")

            # select only the rows of that transect
            waterpas_data_transect = waterpas_data[mask]

            # average over measurements in the transect
            transect_mean = waterpas_data_transect.mean()

            # plot the transect / add the transect to the plot
            transect_mean.plot(ax=ax, label=f"transect {transect}")

            ax.scatter(x=transect_mean.index, y=transect_mean.values)

        plt.legend()

        savefig_path = rf'N:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}/heights_transect_{"_".join(str(i) for i in transects)}_{plot}'
        plt.savefig(savefig_path + ".png", dpi=400, bbox_inches="tight")
        plt.close()
