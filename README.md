# GPM phenotyping scripts
This project is composed of Python scripts and ImageJ macros for use with
the high throughput *Erysiphe necator* fungicide and UV-C efficacy assays
developed by Alexander Wong, Eliza Allen, and Jason Toney.

## License
This project is licensed under the GNU General Public License v3.0.
For more details, please see the LICENSE file.

## Installation
1) Install Python 3.9 or 3.10.
2) Install the additional required dependencies:\
    Windows: Run setup/InstallDependencies.bat\
    Linux: Untested/Unsupported\
    Mac: Untested/Unsupported

## Usage
1) Place image albums into the "ECHO Images" directory.
2) Run batch_process.py to process the image albums. The results will be\
    compiled into an Excel workbook named GPMFungicideAssay_Workbook.xlsx\
    found in this directory. The results of the analysis will also be\
    outputted to the screen.

## TODO
- improve code style and readability
