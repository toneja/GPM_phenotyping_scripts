# GPM_phenotyping_scripts
Python scripts for use with *Erysiphe necator* fungicide efficacy assay

Usage:
1) Install the required dependencies:\
    Windows: Run setup/InstallDependencies.bat\
    Linux: Run setup/InstallDependencies.sh\
    Mac: Untested/Unsupported
2) Place 0hr and 48hr csv files with results from ImageJ into this directory.
3) Run analyze_results.py with the name of one of your results csv files as
    the argument.\
    e.g.: python3 ./analyze_results.py Results_plate6a_napa05-pb_0hr.csv\
    OR\
    Run gui.py, use the file menu to open the results csv files, then click\
    the "Process Files" button to run the analysis.
4) The results of the analysis will be outputted to the screen and into a\
    "FinalResults" csv file, e.g.: "FinalResults_plate6a_napa05-pb.csv".
5) Finally, either run the compile_results.py script or click the "Compile\
    Workbook" button in the gui program to compile the FinalResults csv files\
    into an Excel workbook.

TODO:
- add docstrings and better code comments
- handle possible exceptions
