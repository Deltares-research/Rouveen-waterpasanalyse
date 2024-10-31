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
- Scripts in the analysis folder starting with 'write' or 'plot' have a seperate section at the beginning of the script to set the parameters to be plotted or written.
- Among other parameters, a list with farmers is present in this section. You can decide for which farmers you want to make the figure.
- The type of plot can be set with keyword plot. Possible values are "R" for referentieperceel or "D" for maatregelenperceel.
- Other possible parameters in this section are season, year, transect. These are only present in some scripts for plotting.
- All parameters are presented in list form, so that multiple can be chosen. For example, currently farmers = ['01'] to make a figure for farmer 01. But this can be changed to farmer = ["02", "03"] to make figures for farmer 02 en 03.
The other parameters work in a similar way, so ["2019"] can be extended to ["2019", "2020", "2021"] etc.
- The only exception is the keyword tov_t0. This is just set to True or False.
