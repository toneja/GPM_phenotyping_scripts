#!/usr/bin/python3
#
# This file is part of the GPM phenotyping scripts.
#
# Copyright (c) 2025 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Define treatment maps for fungicides in a 96-well plate."""

# Definitions of fungicide treatments; 1 μg/mL = 1 ppm
# Controls
CNTL = "Control"
SHAM = "SHAM 100 μg/mL"
# FRAC 11: Quinone Outside Inhibitors
AZX1 = "Azoxystrobin 10 μg/mL"
MDS1 = "Mandestrobin 10 μg/mL"
PYL1 = "Pyraclostrobin 10 μg/mL"
TFX1 = "Trifloxystrobin 10 μg/mL"
# FRAC 7: Succinate Dehydrogenase Inhibitors
BOS1 = "Boscalid 0.01 μg/mL"
BOS2 = "Boscalid 0.1 μg/mL"
BOS3 = "Boscalid 1 μg/mL"
BOS4 = "Boscalid 10 μg/mL"
BOS5 = "Boscalid 100 μg/mL"
FLU1 = "Fluopyram 0.01 μg/mL"
FLU2 = "Fluopyram 0.1 μg/mL"
FLU3 = "Fluopyram 1 μg/mL"
FLU4 = "Fluopyram 10 μg/mL"
FLU5 = "Fluopyram 100 μg/mL"
# FRAC 13: Azanaphtalenes
QXF0 = "Quinoxyfen 0.0001 μg/mL"
QXF1 = "Quinoxyfen 0.001 μg/mL"
QXF2 = "Quinoxyfen 0.01 μg/mL"
QXF3 = "Quinoxyfen 0.1 μg/mL"
QXF4 = "Quinoxyfen 1 μg/mL"
QXF5 = "Quinoxyfen 10 μg/mL"
QXF6 = "Quinoxyfen 100 μg/mL"
# Definitions of UV-C treatments
UVC1 = "Speed 1"
UVC2 = "Speed 2"
UVC3 = "Speed 3"
UVC4 = "Speed 4"
UVC5 = "Speed 5"


# maps of treatment blocks
def get_treatments(plate, block):
    """Returns the treatment in its corresponding well."""
    # Handle batches, eg. plate1a-1, plate1a-2, ...
    plate = plate.split("-")[0]
    # plate IDs 1-6 are deprecated and have been removed from this branch
    # plate IDs 7-20: treatments = QOI + Quinoxfen
    # plate IDs 21-28: treatments = SDHI
    if plate == "plate7":
        treatments = [
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
            PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5, CNTL,
        ]
    elif plate == "plate8":
        treatments = [
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
            CNTL, PYL1, QXF4, QXF1, SHAM, MDS1, QXF3, AZX1, QXF2, QXF6, TFX1, QXF5,
        ]
    elif plate == "plate9":
        treatments = [
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
            AZX1, PYL1, QXF2, QXF4, SHAM, QXF3, CNTL, TFX1, MDS1, QXF6, QXF5, QXF1,
        ]
    elif plate == "plate10":
        treatments = [
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
            MDS1, QXF4, AZX1, QXF6, QXF1, SHAM, QXF3, CNTL, TFX1, PYL1, QXF2, QXF5,
        ]
    elif plate == "plate11":
        treatments = [
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
            AZX1, TFX1, QXF5, PYL1, QXF6, QXF4, CNTL, QXF1, QXF2, SHAM, MDS1, QXF3,
        ]
    elif plate == "plate12":
        treatments = [
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
            QXF4, CNTL, MDS1, SHAM, QXF5, QXF1, QXF3, QXF6, QXF2, PYL1, TFX1, AZX1,
        ]
    elif plate == "plate13":
        treatments = [
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
            MDS1, QXF1, QXF2, TFX1, QXF6, QXF4, QXF3, SHAM, CNTL, AZX1, PYL1, QXF5,
        ]
    elif plate == "plate14":
        treatments = [
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
            PYL1, MDS1, CNTL, QXF1, AZX1, QXF5, QXF2, SHAM, TFX1, QXF3, QXF4, QXF6,
        ]
    elif plate == "plate15":
        treatments = [
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
            QXF6, QXF2, PYL1, CNTL, QXF4, AZX1, QXF1, QXF3, TFX1, MDS1, QXF5, SHAM,
        ]
    elif plate == "plate16":
        treatments = [
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
            QXF4, QXF5, QXF6, TFX1, QXF1, QXF2, MDS1, SHAM, CNTL, AZX1, PYL1, QXF3,
        ]
    elif plate == "plate17":
        treatments = [
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
            CNTL, MDS1, SHAM, QXF2, AZX1, TFX1, QXF5, QXF3, QXF1, QXF4, PYL1, QXF6,
        ]
    elif plate == "plate18":
        treatments = [
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
            QXF1, QXF3, QXF5, AZX1, QXF6, TFX1, PYL1, MDS1, CNTL, SHAM, QXF4, QXF2,
        ]
    elif plate == "plate19":
        treatments = [
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
            PYL1, MDS1, SHAM, AZX1, CNTL, TFX1, QXF0, QXF2, QXF5, QXF3, QXF1, QXF4,
        ]
    elif plate == "plate20":
        treatments = [
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
            TFX1, PYL1, CNTL, MDS1, AZX1, SHAM, QXF1, QXF0, QXF2, QXF3, QXF4, QXF5,
        ]
    elif plate == "plate21":
        treatments = [
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
            BOS4, CNTL, FLU3, BOS3, FLU1, BOS2, SHAM, BOS5, BOS1, FLU2, FLU4, FLU5,
        ]
    elif plate == "plate22":
        treatments = [
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
            FLU4, BOS2, BOS5, FLU1, BOS3, BOS4, SHAM, FLU5, FLU3, BOS1, CNTL, FLU2,
        ]
    elif plate == "plate23":
        treatments = [
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
            FLU2, FLU3, FLU5, FLU1, CNTL, BOS1, BOS3, BOS2, BOS5, BOS4, FLU4, SHAM,
        ]
    elif plate == "plate24":
        treatments = [
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
            SHAM, FLU5, BOS5, FLU2, FLU4, BOS1, FLU1, CNTL, BOS2, BOS3, BOS4, FLU3,
        ]
    elif plate == "plate25":
        treatments = [
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU5, FLU4, BOS5, BOS4, BOS3, FLU3, BOS2, FLU1, SHAM, BOS1, CNTL, FLU2,
        ]
    elif plate == "plate26":
        treatments = [
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
            FLU3, BOS2, FLU1, FLU5, SHAM, BOS3, BOS4, BOS1, BOS5, CNTL, FLU2, FLU4,
        ]
    elif plate == "plate27":
        treatments = [
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
            BOS3, FLU2, FLU1, BOS5, FLU3, FLU5, FLU4, BOS2, BOS4, SHAM, BOS1, CNTL,
        ]
    elif plate == "plate28":
        treatments = [
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
            FLU3, BOS4, BOS5, BOS2, FLU5, BOS3, FLU4, FLU1, SHAM, BOS1, CNTL, FLU2,
        ]
    elif plate == "plateUVCControl":
        treatments = [CNTL]
    elif plate == "plateUVC1":
        # B, A, D, E, F, C
        treatments = [
            UVC2, UVC1, UVC4, CNTL, UVC5, UVC3,
            UVC5, UVC3, UVC1, CNTL, UVC4, UVC2,
            UVC3, UVC2, CNTL, UVC1, UVC4, UVC5,
            UVC4, CNTL, UVC2, UVC5, UVC3, UVC1,
        ]
    elif plate == "plateUVC2":
        # F, D, B, E, A, C
        treatments = [
            CNTL, UVC1, UVC5, UVC4, UVC2, UVC3,
            UVC2, UVC3, UVC1, UVC4, UVC5, CNTL,
            UVC3, CNTL, UVC4, UVC1, UVC5, UVC2,
            UVC5, UVC4, CNTL, UVC2, UVC3, UVC1,
        ]
    elif plate == "plateUVC3":
        # C, E, A, B, F, D
        treatments = [
            UVC2, CNTL, UVC1, UVC3, UVC4, UVC5,
            UVC4, UVC5, CNTL, UVC3, UVC1, UVC2,
            UVC5, UVC2, UVC3, CNTL, UVC1, UVC4,
            UVC1, UVC3, UVC2, UVC4, UVC5, CNTL,
        ]
    elif plate == "plateUVC4":
        # D, E, B, A, C, F
        treatments = [
            UVC1, UVC2, CNTL, UVC4, UVC3, UVC5,
            UVC3, UVC5, UVC2, UVC4, CNTL, UVC1,
            UVC5, UVC1, UVC4, UVC2, CNTL, UVC3,
            CNTL, UVC4, UVC1, UVC3, UVC5, UVC2,
        ]
    elif plate == "plateUVC5":
        # B, E, D, F, A, C
        treatments = [
            UVC3, UVC1, UVC4, CNTL, UVC2, UVC5,
            UVC2, UVC5, UVC1, CNTL, UVC4, UVC3,
            UVC5, UVC3, CNTL, UVC1, UVC4, UVC2,
            UVC4, CNTL, UVC3, UVC2, UVC5, UVC1,
        ]
    elif plate == "plateUVC6":
        # F, A, D, C, E, B
        treatments = [
            CNTL, UVC3, UVC4, UVC1, UVC5, UVC2,
            UVC5, UVC2, UVC3, UVC1, UVC4, CNTL,
            UVC2, CNTL, UVC1, UVC3, UVC4, UVC5,
            UVC4, UVC1, CNTL, UVC5, UVC2, UVC3,
        ]
    elif plate == "plateUVC7":
        # B, D, F, C, A, E
        treatments = [
            UVC4, UVC3, UVC5, CNTL, UVC2, UVC1,
            UVC2, UVC1, UVC3, CNTL, UVC5, UVC4,
            UVC1, UVC4, CNTL, UVC3, UVC5, UVC2,
            UVC5, CNTL, UVC4, UVC2, UVC1, UVC3,
        ]
    elif plate == "plateUVC8":
        # B, D, E, A, C, F
        treatments = [
            UVC1, UVC2, UVC5, CNTL, UVC3, UVC4,
            UVC3, UVC4, UVC2, CNTL, UVC5, UVC1,
            UVC4, UVC1, CNTL, UVC2, UVC5, UVC3,
            UVC5, CNTL, UVC1, UVC3, UVC4, UVC2,
        ]
    elif plate == "plateUVC9":
        # E, A, D, C, B, F
        treatments = [
            UVC1, UVC3, UVC4, UVC2, UVC5, CNTL,
            UVC5, CNTL, UVC3, UVC2, UVC4, UVC1,
            CNTL, UVC1, UVC2, UVC3, UVC4, UVC5,
            UVC4, UVC2, UVC1, UVC5, CNTL, UVC3,
        ]
    elif plate == "plateUVC10":
        # D, B, C, E, A, F
        treatments = [
            UVC1, UVC4, CNTL, UVC5, UVC2, UVC3,
            UVC2, UVC3, UVC4, UVC5, CNTL, UVC1,
            UVC3, UVC1, UVC5, UVC4, CNTL, UVC2,
            CNTL, UVC5, UVC1, UVC2, UVC3, UVC4,
        ]
    elif plate == "plateUVC11":
        # F, A, E, D, C, B
        treatments = [
            CNTL, UVC2, UVC3, UVC1, UVC5, UVC4,
            UVC5, UVC4, UVC2, UVC1, UVC3, CNTL,
            UVC4, CNTL, UVC1, UVC2, UVC3, UVC5,
            UVC3, UVC1, CNTL, UVC5, UVC4, UVC2,
        ]
    elif plate == "plateUVC12":
        # F, C, B, D, A, E
        treatments = [
            CNTL, UVC5, UVC3, UVC4, UVC2, UVC1,
            UVC2, UVC1, UVC5, UVC4, UVC3, CNTL,
            UVC1, CNTL, UVC4, UVC5, UVC3, UVC2,
            UVC3, UVC4, CNTL, UVC2, UVC1, UVC5,
        ]
    return treatments[block]
