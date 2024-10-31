# Spirit levelling in Rouveen
The code in this repository uses spirit levelling data, which measures the movement of the subsurface with respect to Normaal Amsterdams Peil (NAP).
The data is collected for location Rouveen.

# Folder structure
There are two folders:
1. pre-processing
   - This folder contains python scripts to write raw data for spirit leveling and groundwater levels to interim files.
     Reading data from these interim files is faster than for raw data, and speeds up the time it takes to make figures.
2. analysis
   - This folder contains python scripts to plot (changes in) spirit levelling measurements.
     Further, some scripts in this folder write statistics of the spirit levelling measurements to new csv files.

#### Parameter selection
Scripts in the analysis folder starting with 'write' or 'plot' have a seperate section at the beginning of the script to set the parameters to be plotted or written.
The possible parameters are already listed in each script and can be several of the following:
- farmers, to decide for which farmers a figure is made
- plots, to decide the plot type. Possible values are "R" for referentieperceel or "D" for maatregelenperceel.
- seasons, to set the season ('winter', 'spring', 'summer', 'autumn')
- years, to set the year (2018, 2019, 2020, 2021, 2022 etc)
- transects, to set the transect of the plots. This is a value between 1 and 4 for all farmers except farmer 05. This plots of this farmer also has a fifth transect.
- tov_t0, set to True or False, if tov_t0=True

All parameters except tov_t0 are presented in list form, so that multiple options can be run at the same time. 

For example:
Set farmers = ['01'] to make a figure for farmer 01. But this can be changed to farmer = ["02", "03"] to make figures for farmer 02 en 03.
The other parameters work in a similar way, so ["2019"] can be extended to ["2019", "2020", "2021"] etc.
