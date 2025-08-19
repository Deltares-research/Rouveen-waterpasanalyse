import pandas as pd
import os
import xlsxwriter
from pathlib import Path

#####################################################
# parameters
#####################################################

# farmers = ["01", "02", "05", "06", "07", "08", "09", "11"]
farmers = ["08"]
plots = ["R", "D"]  # R voor referentieperceel of D voor maatregelenperceel

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
colors = {
    "R": ["#CAE0AB", "#4EB265", "royalblue"],
    "D": ["#F6C141", "#E8601C", "turquoise"],
}
xloc_text = {"R": 0.05, "D": 0.35}

for farmer in farmers:

    dh_mean_and_std = pd.DataFrame()

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

        column_names = list(range(len(waterpas_data.columns)))
        waterpas_data.columns = column_names

        if (farmer == "08") and (plot == "R"):
            waterpas_data = waterpas_data.drop(columns=[22])

        # statistics for average height change
        # hoogteverandering van campagne naar campagne
        delta_h = waterpas_data.diff(axis=1).dropna(
            axis=1, how="all"
        )  # negatief is daling
        delta_h_mean = delta_h.mean(axis=0).to_frame("gem. hoogteverschil")
        delta_h_std = delta_h.std(axis=0).to_frame("Standaard deviatie")

        if dh_mean_and_std.empty:
            dh_mean_and_std = pd.concat([delta_h_mean, delta_h_std], axis=1)
        else:
            dh_mean_and_std = pd.concat(
                [dh_mean_and_std, delta_h_mean, delta_h_std], axis=1
            )

    # zorg dat de meting nrs op volgorde staan
    dh_mean_and_std = dh_mean_and_std.sort_index()

    fpath = f"N:/Projects/11204000/11204108/B. Measurements and calculations/Ruimtelijke analyse waterpassingen/data/3-output/{farmer_name}/statistieken_hoogteverschil_{farmer_name}"

    header = ",Referentie perceel,,Maatregelen perceel,\n "
    with open(fpath + ".csv", "w") as fp:
        fp.write(header)

    dh_mean_and_std.to_csv(
        fpath + ".csv",
        header=[
            "Gem. hoogteverschil",
            "Standaard deviatie",
            "Gem. hoogteverschil",
            "Standaard deviatie",
        ],
        index_label="Meting nummer",
        mode="a",
    )

    # # prepare Excel file
    writer = pd.ExcelWriter(fpath + ".xlsx", engine="xlsxwriter")
    dh_mean_and_std.to_excel(
        writer, sheet_name=r"Statistieken", index_label="Meting nummer", startrow=1
    )

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Statistieken"]

    # write the headers
    worksheet.write(0, 1, "Referentie perceel")
    worksheet.write(0, 3, "Maatregelen perceel")

    for i, width in enumerate([24, 22, 22, 22, 22]):
        writer.sheets["Statistieken"].set_column(i, i, width)

    writer.close()

## other statistics ##
# # plot afwijking hoogteverschil
# dev_delta_h = delta_h - delta_h.mean()
# delta_h.var()
