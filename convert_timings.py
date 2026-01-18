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

import openpyxl
import pandas as pd


def calculate_exposure(row, cols):
    sampled_len = 250
    exposure_time = row[cols].mean()
    exposure_time *= row["Lamp Length (mm)"] / sampled_len
    uvc_dose = int(round(exposure_time * row["Irradiance (W/m2)"], 0))
    return uvc_dose


def main():
    os.chdir(os.path.dirname(__file__))
    workbook = "GPMPhenotypingAssay_Workbook.xlsx"
    if os.path.exists(workbook):
        uvc_workbook = openpyxl.load_workbook(workbook)
        if "Assay Data" in uvc_workbook.sheetnames:
            sheet = uvc_workbook["Assay Data"]
        else:
            return
        uvc_df = pd.DataFrame(sheet.values)
        uvc_df.columns = uvc_df.iloc[0]
        for _, row in uvc_df[1:].iterrows():
            plate = row["Plate ID"]
            isolate = row["Isolate"]
            doses = {}
            for index in range(1, 5 + 1):
                cols = uvc_df.filter(like=f"Time {index}").columns
                doses[
                    f"Speed {index}"
                ] = f"{calculate_exposure(row, cols)} J/m2"
            results_file = f"results/FinalResults_plate{plate}_{isolate}.csv"
            if os.path.exists(results_file):
                assay_data = pd.read_csv(results_file)
                assay_df = pd.DataFrame(assay_data)
                for key, value in doses.items():
                    assay_df.replace(key, value, inplace=True)
                assay_df.to_csv(results_file, index=False)


if __name__ == "__main__":
    main()
