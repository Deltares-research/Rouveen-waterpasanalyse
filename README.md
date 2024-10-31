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
     The scripts furthermore write statistics of the spirit levelling measurements to new csv files.
