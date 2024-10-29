import pandas as pd


def load_grondwater_data(filename_wareco, farmer, plot, period="D"):

    name = f"GW-{farmer}"
    # print(f'Loading groundwater data for {name}_{plot}.')

    # for name in names:
    if name in ["GW-01", "GW-02", "GW-09", "GW-11"]:
        if plot == "R":  # referentie perceel
            excel_cols = "A:B"
        elif plot == "D":  # maatregelen perceel
            excel_cols = "E:F"
    elif name in ["GW-05", "GW-06", "GW-07", "GW-08"]:
        if plot == "R":  # referentie perceel
            excel_cols = "E:F"
        elif plot == "D":  # maatregelen perceel
            excel_cols = "A:B"

    if name in ["GW-01"]:
        rows_to_skip = 6
    else:
        rows_to_skip = 5

    # initialize dictionaries
    gwstand = {}
    gwstand_wareco = {}

    gwstand_wareco[f"{name}"] = (
        pd.read_excel(
            filename_wareco,
            sheet_name=name,
            index_col=0,
            skiprows=rows_to_skip,
            usecols=excel_cols,
        )
        .resample(period)
        .mean()
        .squeeze()
    )

    gwstand_wareco[f"{name}"] *= 100  # to convert from m to cm

    gwstand_wareco[f"{name}"].columns = ["Waterstand (m NAP)"]
    gwstand_wareco[f"{name}"].index.names = ["Datum"]

    # for farmer 05, we can use NOBV groundwater data after July 2020
    if name == "GW-05":

        filename_nobv_basedir = r"N:/Projects/11204000/11204108/B. Measurements and calculations/Meetlocaties/Info_per_locatie/Rouveen/Grondwater/BACKUP_Grondwaterstandmetingen/Per meetpunt"

        gwstand_nobv = {}

        if plot == "R":
            filename_nobv = filename_nobv_basedir + "/ROV_RF_11.xlsx"
        elif plot == "D":
            filename_nobv = filename_nobv_basedir + "/ROV_MS_1.xlsx"

        gwstand_nobv[f"{name}"] = (
            pd.read_excel(
                filename_nobv,
                sheet_name="meetgegevens",
                index_col=0,
                parse_dates=True,
                usecols=["Datum", "Waterstand"],
            )
            .resample(period)
            .mean()
            .squeeze()
        )

        # gwstand_nobv[f'{name}_RF'] = pd.read_excel(filename_nobv_rf,
        #                         sheet_name = 'meetgegevens',  index_col=0, parse_dates=True, usecols = ['Datum', 'Waterstand'],
        #                         ).resample(period).mean().squeeze()

        # gwstand_nobv[f'{name}_MP'] = pd.read_excel(filename_nobv_mp,
        #                         sheet_name = 'meetgegevens',  index_col=0, parse_dates=True, usecols = ['Datum', 'Waterstand'],
        #                         ).resample(period).mean().squeeze()

        gwstand_nobv = pd.DataFrame.from_dict(gwstand_nobv)
        # gwstand_nobv[f'{name}_RF'].columns = ['Waterstand']
        # gwstand_nobv[f'{name}_MP'].columns = ['Waterstand']
        gwstand_nobv = gwstand_nobv.dropna()

        gwstand[f"{name}"] = pd.concat(
            [gwstand_wareco[f"{name}"], gwstand_nobv[f"{name}"]]
        )
        gwstand[f"{name}"] = gwstand[f"{name}"][
            ~gwstand[f"{name}"].index.duplicated(keep="last")
        ]
        gwstand[f"{name}"] = gwstand[f"{name}"].sort_index()

        # gwstand[f'{name}_RF'] = pd.concat([gwstand_wareco[f'{name}_RF'], gwstand_nobv[f'{name}_RF']])
        # gwstand[f'{name}_MP'] = pd.concat([gwstand_wareco[f'{name}_MP'], gwstand_nobv[f'{name}_MP']])
        ## gwstand = pd.DataFrame.from_dict(gwstand)# .drop_duplicates()
        # gwstand[f'{name}_RF'] = gwstand[f'{name}_RF'][~gwstand[f'{name}_RF'].index.duplicated(keep='last')]
        # gwstand[f'{name}_MP'] = gwstand[f'{name}_MP'][~gwstand[f'{name}_MP'].index.duplicated(keep='last')]
        # gwstand[f'{name}_RF'] = gwstand[f'{name}_RF'].sort_index()
        # gwstand[f'{name}_MP'] = gwstand[f'{name}_MP'].sort_index()
    else:
        gwstand = gwstand_wareco

    gwstand[f"{name}"] /= 100

    # gwstand[f'{name}_RF'] /= 100
    # gwstand[f'{name}_MP'] /= 100

    # return data
    # return gwstand_wareco, gwstand_nobv
    return gwstand
