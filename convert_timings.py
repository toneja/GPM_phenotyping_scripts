#!/usr/bin/env python3
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

import os
import pandas as pd


def calculate_exposure(row, first, last):
    sampled_len = 250
    exposure_time = sum(row[first:last]) / 3
    exposure_time *= row["Lamp Length (mm)"] / sampled_len
    uvc_dose = int(round(exposure_time * row["Irradiance (W/m2)"], 0))
    return uvc_dose


def main():
    os.chdir(os.path.dirname(__file__))
    if os.path.exists("__UVC_assay-data.csv"):
        uvc_data = pd.read_csv("__UVC_assay-data.csv")
        uvc_df = pd.DataFrame(uvc_data)
        for i, row in uvc_df.iterrows():
            plate = row["Plate ID"]
            isolate = row["Isolate"]
            doses = {}
            col = 4
            for index in range(1, 5 + 1):
                doses[f"Speed {index}"] = f"{calculate_exposure(row, col, col + 3)} J/m2"
                col += 3
            results_file = f"results/FinalResults_plate{plate}_{isolate}.csv"
            if os.path.exists(results_file):
                assay_data = pd.read_csv(results_file)
                assay_df = pd.DataFrame(assay_data)
                for key, value in doses.items():
                    assay_df.replace(key, value, inplace=True)
                assay_df.to_csv(results_file, index=False)


if __name__ == "__main__":
    main()
