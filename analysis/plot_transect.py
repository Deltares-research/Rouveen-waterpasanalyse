import pandas as pd
import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def set_xaxis_datelabels(ax):

    # maj_loc = mdates.MonthLocator(bymonth=np.arange(1,12,6))
    maj_loc = mdates.AutoDateLocator(minticks=3, maxticks=7)
    ax.xaxis.set_major_locator(maj_loc)

    # horizontal labels
    ax.xaxis.set_tick_params(rotation=0)

    for label in ax.get_xticklabels():
        label.set_horizontalalignment("center")

    zfmts = ["", "%b\n%Y", "%b", "%b-%d", "%H:%M", "%H:%M"]
    maj_fmt = mdates.ConciseDateFormatter(
        maj_loc, zero_formats=zfmts, show_offset=False
    )

    ax.xaxis.set_major_formatter(maj_fmt)
    ax.figure.autofmt_xdate(rotation=0, ha="center")

    # ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_locator(mdates.MonthLocator())


# these are all the farmers
trans = {
    "01": "01-Bouwman",
    # "02": "02-DalFsen",
    # "05": "05-Kronenberg",
    # "06": "06-DenUyl",
    # "07": "07-Post",
    # "08": "08-Brandhof",
    # "09": "09-Visscher",
    # "11": "11-Petter",
}

transects = ["1", "2", "3", "4"]
# transects = ["1", "2", "3"]
transect_colors = {
    "1": "#1f77b4",
    "2": "#ff7f0e",
    "3": "#2ca02c",
    "4": "#d62728",
    "5": "#9467bd",
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
            transect_mean.index = pd.to_datetime(transect_mean.index)

            if tov_t0:
                transect_mean -= transect_mean.iloc[0]

            # plot the transect / add the transect to the plot
            transect_mean.plot(
                ax=ax,
                label=f"transect {transect}",
                linewidth=0.5,
                color=transect_colors[transect],
            )

            ax.scatter(
                x=transect_mean.index,
                y=transect_mean.values,
                color=transect_colors[transect],
            )

        ax.set_xlim(
            waterpas_data.columns[0],
            waterpas_data.columns[-1],
        )

        if tov_t0:
            ax.set_ylabel("Maaiveld hoogte \n t.o.v. eerste meeting (m)")
        else:
            ax.set_ylabel("Maaiveld hoogte \n t.o.v. NAP (m)")
        ax.set_xlabel("Datum")
        ax.set_title("Perceel " + farmer_name.split("-")[0])
        set_xaxis_datelabels(ax)

        ax.grid()

        ax.legend(
            bbox_to_anchor=(0.10, -0.12),
            ncols=3,
            loc="upper left",
            frameon=False,
            fontsize=12,
            # title="Maaiveldhoogtes",
        )

        # plt.legend()

        savefig_path = rf'N:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}/heights_transect_{"_".join(str(i) for i in transects)}_{plot}_'
        if tov_t0:
            savefig_path = savefig_path + "tov_t0"
        else:
            savefig_path = savefig_path + "tov_NAP"
        plt.savefig(savefig_path + ".png", dpi=400, bbox_inches="tight")
        plt.close()
