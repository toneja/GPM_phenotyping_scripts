# GPM phenotyping scripts
This project is composed of Python scripts and ImageJ macros for use with
the high throughput *Erysiphe necator* fungicide efficacy assay developed
by Alexander Wong and Jason Toney.

## License
This project is licensed under the GNU Affero General Public License v3.0.
For more details, please see the LICENSE file.

## Installation
1) Install Python 3.9 or 3.10.
2) Install the additional required dependencies:\
    Windows: Run setup/InstallDependencies.bat\
    Linux: Run setup/InstallDependencies.sh\
    Mac: Untested/Unsupported

## Usage
1) Place 0hr and 48hr image albums into the "ECHO Images" directory.
2) Run ImageJ/batch_process.py to process the image albums.
3) Run gui.py, then click the "Process Files" button to run the analysis.
4) Click the "Compile Workbook" button to compile the results into an Excel\
    workbook named GPMFungicideAssay_Workbook.xlsx in the results directory.\
	The results of the analysis will also be outputted to the screen.

## TODO
- add docstrings and better code comments
- handle possible exceptions
