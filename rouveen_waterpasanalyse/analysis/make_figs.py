import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as datetime

import copy


def plot_spatial(data, column, title, cmap, vmin, vmax, label_cbar, fpath):

    x = data.index.get_level_values("x")
    y = data.index.get_level_values("y")

    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(x, y, c=data[column].values, vmin=vmin, vmax=vmax, cmap=cmap)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.ticklabel_format(axis="both", style="plain", useOffset=False)
    cax = fig.add_axes([1, 0.1, 0.03, 0.8])
    ax_cbar = fig.colorbar(sc, cax=cax)
    ax_cbar.set_label(label_cbar)
    plt.savefig(fpath + ".png", dpi=400, bbox_inches="tight")
    plt.close()


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


def plot_trendline(
    waterpas_data,
    winter_indices,
    farmer_name,
    plot,
    x,
    regression_line,
    stats_text,
    xloc_text,
    colors,
    label,
    savefig=True,
    tov_t0=False,
):

    if tov_t0:
        waterpas_data -= waterpas_data.iloc[0]

    fig = plt.figure(figsize=(8.27, 11.69 / 1.5))
    ax = fig.add_subplot(211)

    # plot the measurements
    waterpas_data.reset_index().plot.line(
        ax=ax,
        x="index",
        y="gem. hoogte",
        color=colors[1],
        linewidth=0.5,
        label="_",
        zorder=1,
    )
    waterpas_data[~winter_indices].reset_index().plot.scatter(
        ax=ax,
        x="index",
        y="gem. hoogte",
        color=colors[1],
        zorder=2,
        label=label.title(),
    )
    waterpas_data[winter_indices].reset_index().plot.scatter(
        ax=ax,
        x="index",
        y="gem. hoogte",
        color=colors[0],
        zorder=2,
        label=f"{label.title()} - wintermeting",
    )

    # plot the regression line
    ax.plot(
        x,
        regression_line,
        color=colors[0],
        linestyle="--",
        label=f"Lineare trend {label}",
    )
    ax.text(
        x=xloc_text,
        y=0.05,
        s=stats_text,
        color=colors[1],
        va="bottom",
        ha="left",
        fontsize=9,
        transform=ax.transAxes,
    )

    ax.set_xlim(
        waterpas_data.reset_index()["index"].min(),
        waterpas_data.reset_index()["index"].max(),
    )

    if tov_t0:
        ax.set_ylabel("Maaiveld hoogte \n t.o.v. eerste meeting (m)")
    else:
        ax.set_ylabel("Maaiveld hoogte \n t.o.v. NAP (m)")

    ax.set_ylim(
        [
            waterpas_data.mean(axis=None).item() - 0.09,
            waterpas_data.mean(axis=None).item() + 0.09,
        ]
    )

    ax.set_title("Perceel " + farmer_name.split("-")[0])
    # ax.set_title(farmer_name)
    ax.set_xlabel("Datum")
    set_xaxis_datelabels(ax)
    ax.grid()

    if savefig:

        ax.legend(
            bbox_to_anchor=(0, -0.15),
            ncols=2,
            loc="upper left",
            frameon=False,
            fontsize=10,
            title="Maaiveldhoogtes",
        )

        # save
        fpath = f"N:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}/Gem_maaiveldhoogte_{label}_"

        if tov_t0:
            fpath = fpath + "tov_t0"
        else:
            fpath = fpath + "tov_NAP"

        plt.savefig(fpath + ".png", dpi=400, bbox_inches="tight")
        plt.close()
    else:
        return fig, ax


def plot_trendline_and_groundwater(
    groundwater_data,
    waterpas_data,
    winter_indices,
    farmer_name,
    plot,
    x,
    regression_line,
    stats_text,
    xloc_text,
    colors,
    label,
    tov_t0=False,
):

    fig, ax = plot_trendline(
        copy.deepcopy(waterpas_data),
        winter_indices,
        farmer_name,
        plot,
        x,
        regression_line,
        stats_text,
        xloc_text,
        colors,
        label,
        savefig=False,
        tov_t0=tov_t0,
    )

    ax2 = fig.add_subplot(212, sharex=ax)

    waterpas_data.reset_index().plot.line(
        ax=ax2,
        x="index",
        y="gem. hoogte",
        color=colors[1],
        linewidth=0.5,
        label=f"Maaiveld - {label}",
    )

    ax2.plot(
        groundwater_data,
        linewidth=0.8,
        c=colors[2],
        alpha=0.6,
        linestyle="-",
        label=label.title(),
    )

    ax2.set_ylim(
        groundwater_data.min(axis=None) - 0.1, groundwater_data.max(axis=None) + 0.1
    )
    ax2.text(
        x=waterpas_data.index.values[
            -1
        ],  # datetime.date(2023, 8, 15),  # turn this into index location
        y=waterpas_data.iloc[-2].values + 0.03,
        s="Maaiveld",
        color="black",
        va="bottom",
        ha="right",
        fontsize=9,
    )

    ax2.set_ylabel("Hoogte t.o.v. NAP (m)")
    ax2.set_xlabel("Datum")
    set_xaxis_datelabels(ax2)
    ax2.grid()
    ax2.legend(
        bbox_to_anchor=(0.6, -0.15),
        loc="upper left",
        frameon=False,
        fontsize=10,
        title="Grondwaterstanden",
    )

    ax.legend(
        bbox_to_anchor=(0, -1.35),
        loc="upper left",
        frameon=False,
        fontsize=10,
        title="Maaiveldhoogtes",
    )

    # save
    fpath = f"N:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/4-visualisation/{farmer_name}/Gem_maaiveldhoogte_{label}_"
    if tov_t0:
        fpath = fpath + "tov_t0_with_groundwater"
    else:
        fpath = fpath + "tov_NAP_with_groundwater"

    plt.savefig(fpath + ".png", dpi=400, bbox_inches="tight")
    plt.close()


def add_trendline(
    waterpas_data,
    winter_indices,
    farmer_name,
    regression_data,
    stats_text,
    xloc_text,
    colors,
    label,
    ax,
    tov_t0=False,
):

    if tov_t0:
        waterpas_data -= waterpas_data.iloc[0]

    # plot the measurements
    waterpas_data.reset_index().plot.line(
        ax=ax,
        x="index",
        y="gem. hoogte",
        color=colors[1],
        linewidth=0.5,
        label="_",
        zorder=1,
    )
    waterpas_data[~winter_indices].reset_index().plot.scatter(
        ax=ax,
        x="index",
        y="gem. hoogte",
        color=colors[1],
        zorder=2,
        label=label.title(),
    )
    waterpas_data[winter_indices].reset_index().plot.scatter(
        ax=ax,
        x="index",
        y="gem. hoogte",
        color=colors[0],
        zorder=2,
        label=f"{label.title()} - wintermeting",
    )

    # plot the regression line
    regression_data.plot(
        ax=ax,
        color=colors[0],
        linestyle="--",
        label=f"Lineare trend {label}",
    )

    ax.text(
        x=xloc_text,
        y=0.05,
        s=stats_text,
        color=colors[1],
        va="bottom",
        ha="left",
        fontsize=9,
        transform=ax.transAxes,
    )

    ax.set_xlim(
        waterpas_data.reset_index()["index"].min(),
        waterpas_data.reset_index()["index"].max(),
    )

    if tov_t0:
        ax.set_ylabel("Maaiveld hoogte \n t.o.v. eerste meeting (m)")
    else:
        ax.set_ylabel("Maaiveld hoogte \n t.o.v. NAP (m)")

    ax.set_ylim(
        [
            waterpas_data.mean(axis=None).item() - 0.09,
            waterpas_data.mean(axis=None).item() + 0.09,
        ]
    )

    ax.set_title("Perceel " + farmer_name.split("-")[0])
    # ax.set_title(farmer_name)
    ax.set_xlabel("Datum")
    set_xaxis_datelabels(ax)
    ax.grid()

    return ax


def add_trendline_and_groundwater(
    groundwater_data,
    waterpas_data,
    winter_indices,
    farmer_name,
    regression_data,
    stats_text,
    xloc_text,
    colors,
    label,
    axs,
    tov_t0=False,
):

    axs[0] = add_trendline(
        copy.deepcopy(waterpas_data),
        winter_indices,
        farmer_name,
        regression_data,
        stats_text,
        xloc_text,
        colors,
        label,
        ax=axs[0],
        tov_t0=tov_t0,
    )

    waterpas_data.reset_index().plot.line(
        ax=axs[1],
        x="index",
        y="gem. hoogte",
        color=colors[1],
        linewidth=0.5,
        label=f"Maaiveld - {label}",
    )

    groundwater_data.plot(
        ax=axs[1],
        linewidth=0.8,
        c=colors[2],
        alpha=0.6,
        linestyle="-",
        label=label.title(),
    )

    axs[1].set_ylabel("Hoogte t.o.v. NAP (m)")
    axs[1].set_xlabel("Datum")
    set_xaxis_datelabels(axs[1])
    axs[1].grid()
    axs[1].legend(
        bbox_to_anchor=(0.6, -0.15),
        loc="upper left",
        frameon=False,
        fontsize=10,
        title="Grondwaterstanden",
    )

    axs[0].legend(
        bbox_to_anchor=(0, -1.35),
        loc="upper left",
        frameon=False,
        fontsize=10,
        title="Maaiveldhoogtes",
    )

    return axs
