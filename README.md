# GPM_phenotyping_scripts
Python scripts for use with *Erysiphe necator* fungicide efficacy assay

Usage:
1) Place 0hr and 48hr csv files with results from ImageJ into this directory.
2) Run analyze_results.py with the plate number and isolate name as arguments.\
	e.g.: ./analyze_results.py plate6a napa05-pb
3) The results of the analysis will be outputted to the screen.

TODO:
- add additional plate maps
- tighten up ROI comparisons, don't rely only on area and perimeter increases
- add docstrings and better code comments
- move code in analyze_results.py into its own function
- use py2exe or similar method to allow drag-and-drop analysis of results
