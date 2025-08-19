"""
This script is for reference plot and measures plot together
"""

import pandas as pd
import datetime as datetime
import matplotlib.pyplot as plt

import os
from pathlib import Path

from make_figs import add_trendline_and_groundwater
from calc_stats import calculate_trendline

start_time = datetime.datetime.now()

# these are all the farmers
trans = {
    # "01": "01-Bouwman",
    # "02": "02-DalFsen",
    # "05": "05-Kronenberg",
    # "06": "06-DenUyl",
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

    # here initialize the figure already
    # as well as the amount of subplots, as this will always be 2
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8.27, 11.69 / 1.5), sharex=True)

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

    gw_ylim_bot = []
    gw_ylim_top = []
    maaiveld_yvalues = []

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

        regression_data = pd.Series(index=x, data=regression_line)

        # load the groundwater csv data
        path_to_groundwater_data = os.path.join(
            inputdir_path, f"{farmer_name}_groundwaterlevel_{plot_name}.csv"
        )
        groundwater_data = pd.read_csv(path_to_groundwater_data, index_col=0)
        groundwater_data.index = pd.to_datetime(groundwater_data.index)

        gw_ylim_bot.append(groundwater_data[f"GW-{farmer}"].min() - 0.1)
        gw_ylim_top.append(groundwater_data[f"GW-{farmer}"].max() + 0.1)

        maaiveld_yvalues.append(h_mean.max().item())

        axs = add_trendline_and_groundwater(
            groundwater_data[f"GW-{farmer}"],
            h_mean,
            winter_indices,
            farmer_name,
            # plot,
            regression_data,
            stats_text,
            xloc_text[plot],
            colors=colors[plot],
            label=plot_name,
            axs=axs,
            tov_t0=tov_t0,
        )

    axs[1].text(
        x=h_mean.index.values[-1]
        - pd.Timedelta(
            10, "d"
        ),  # datetime.date(2023, 8, 15),  # turn this into index location
        y=max(maaiveld_yvalues) + 0.02,
        s="Maaiveld",
        color="black",
        va="bottom",
        ha="right",
        # transform=axs[1].transAxes,
        fontsize=9,
    )

    axs[1].set_ylim(min(gw_ylim_bot), max(gw_ylim_top))

    # save
    fpath = f"N:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}/Gem_maaiveldhoogte_referentie_en_maatregel_"
    if tov_t0:
        fpath = fpath + "tov_t0_met_grondwater"
    else:
        fpath = fpath + "tov_NAP_met_groundwater"

    plt.savefig(fpath + ".png", dpi=400, bbox_inches="tight")
    plt.close()

end_time = datetime.datetime.now()

elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time.seconds, "Seconds")
