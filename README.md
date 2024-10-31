The code in this repository uses spirit levelling data, which measures the movement of the subsurface. It then calculates changes in measurements with respect to Normaal Amsterdams Peil (NAP).
The data is collected for location Rouveen.

There are two folders:
1. pre-processing
   - This folder contains python scripts to write raw data to interim files for spirit leveling and groundwater levels.
     Reading data from these interim files is faster than for raw data, and speeds up the time it takes to make the figures (including small adjustments to those figures).
2. analysis
   - This folder contains python scripts to plot (changes in) spirit levelling measurements.
     The scripts furthermore writes statistics of the spirit levelling measurements to a new csv file.
