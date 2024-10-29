import numpy as np
from scipy.stats import linregress


def calculate_trendline(h_mean, winter_indices, tov_t0=False):

    # x pakt alleen de tijdstippen van de waterpasmetingen in de winter
    x = h_mean[winter_indices].reset_index()["index"]

    # dit zijn de waardes van de waterpasmetingen op die tijdstippen
    y = h_mean[winter_indices]["gem. hoogte"].values

    if tov_t0:
        y -= h_mean["gem. hoogte"].values[0]

    # create an array with days counted from the start date
    start_date = x[0]
    x_numeric = np.array([(d - start_date).days for d in x])

    slope, intercept, r_value, p_value, std_err = linregress(x_numeric, y)
    r_squared = r_value**2

    regression_line = slope * x_numeric + intercept

    text = f"R$^2$ = {r_squared:.2f} \nslope = {slope*365*1000:.0f} (mm/jr)"

    return x, regression_line, text
