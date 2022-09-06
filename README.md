# GPM_phenotyping_scripts
Python scripts for use with *Erysiphe necator* fungicide efficacy assay

Usage:
1) Place 0hr and 48hr csv files with results from ImageJ into this directory.
2) Run analyze_results.py with either the plate number and isolate name or the\
	name of your results csv file as arguments.\
	e.g.: ./analyze_results.py plate6a napa05-pb\
	or\
	e.g.: ./analyze_results.py Results_plate6a_napa05-pb_0hr.csv
3) The results of the analysis will be outputted to the screen.

TODO:
- add additional plate maps
- tighten up ROI comparisons, don't rely only on area, perimeter, and roundness changes
- add docstrings and better code comments
- merge scripts and ImageJ macros into single repository
- handle possible exceptions
- write output into a standard file format (csv, xls, etc)
- implement numpy handling of csv inputs
