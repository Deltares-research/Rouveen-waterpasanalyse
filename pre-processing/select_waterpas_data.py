import pandas as pd
from math import sqrt
from datetime import datetime


def find_coords(p1, p2, nr_of_points=25):

    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
    length = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    nb_points = nr_of_points
    distance = length / (nb_points)

    p = [p1]
    if p1[0] < p2[0]:
        for i in range(0, nb_points):
            p.append([p[i][0] + dx(distance, slope), p[i][1] + dy(distance, slope)])

    elif p1[0] > p2[0]:
        for i in range(0, nb_points):
            p.append([p[i][0] + dx(distance, slope), p[i][1] + dy(distance, slope)])

    coordinates_dataframe = pd.DataFrame(p, columns=["x", "y"])
    return coordinates_dataframe


def dy(distance, slope):
    return slope * dx(distance, slope)


def dx(distance, slope):
    return sqrt((distance**2) / (slope**2 + 1))


def select_waterpas_data(data, metadata, sheet, plot):

    # print(sheet)

    if sheet == "05":
        lines = ["1", "2", "3", "4", "5"]
    else:
        lines = ["1", "2", "3", "4"]

    df_final = pd.DataFrame()
    for line in lines:
        if plot == "D":
            if sheet == "05":
                sel = metadata.iloc[0:10, :]
            else:
                sel = metadata.iloc[0:8, :]
        elif plot == "R":
            if sheet == "05":
                sel = metadata.iloc[13:, :]
            else:
                sel = metadata.iloc[11:, :]

        # print(sel)

        # this is for the coordinates of the measurement
        p1 = sel[sel["Code"].str.endswith(line, na=False)].iloc[0, 1:].to_list()
        p2 = sel[sel["Code"].str.endswith(line, na=False)].iloc[1, 1:].to_list()

        # print(p1)
        # print(p2)

        # select the measurements for the relevant parcel
        data_plot = data[data["metingnr"].str.startswith((sheet + plot), na=False)]

        # print(data_plot)

        # set each column name equal to the date of the measurements
        column_names = data.iloc[data_plot.index[0] - 3]

        # below we only select 25 data rows, for every serie points (e.g. 01R200, 01R202 for line=2 etc)
        if line == "1":
            data_line = data_plot[
                data_plot["metingnr"].str.contains((plot + line), na=False)
            ].iloc[1:]
        else:
            data_line = data_plot[
                data_plot["metingnr"].str.contains((plot + line), na=False)
            ]

        # print(data_line)

        # set the column names and convert to datetime dates
        data_line.columns = column_names
        data_line.columns = [
            i.strftime("%Y-%m-%d") if isinstance(i, datetime) else i
            for i in data_line.columns
        ]

        # rename the 'datum' column to 'metingnr'
        data_line = data_line.rename(columns={"datum": "metingnr"})

        # reset the index of the measurement
        # data_line = data_line.reset_index().iloc[:, 2:] # this line also omits the metingnr
        data_line = data_line.reset_index().iloc[:, 1:]

        # print(data_line)

        # print(data_line)

        if line == "5":
            if plot == "D":
                number_of_points = 20
            elif plot == "R":
                number_of_points = 17
        else:
            number_of_points = 25

        p = find_coords(p1, p2, nr_of_points=number_of_points)

        # print(p)

        # print(p)

        # dataframe with x,y coords and the waterpas measurement
        df = pd.concat([p, data_line], axis=1).dropna(axis=1, how="all")
        df = df.set_index(["metingnr", "x", "y"])
        df = df.astype(float)

        # append the waterpas measurements of a single series (or line)
        # to the final dataframe
        df_final = pd.concat([df_final, df])

    # print(df_final)

    return df_final
