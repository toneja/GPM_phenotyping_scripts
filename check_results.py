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

"""This script checks the results for proper germination and spore deposition."""


import os
import warnings

import openpyxl
import pandas as pd
from tabulate import tabulate


def main():
    """Check the results and make sure the data is usable."""
    # Ignore warnings
    warnings.filterwarnings("ignore")
    os.chdir(os.path.dirname(__file__))
    print("Quality checking phenotyping data...")
    keepers = []
    g143a_mutants = [
        "ARC-2A",
        "ARC-2B",
        "BPP-3",
        "BPP-5",
        "CAT1",
        "CL9-3",
        "QR1-2",
    ]
    for file in os.listdir("results"):
        if file.endswith(".csv"):
            plate = file.split("_")[1].upper()
            isolate = file.split(".")[0].split("_")[2].upper()
            discard_reasons = []
            if "UVC" in plate:
                block_size = 4
                spore_min = 50
            else:
                block_size = 8
                spore_min = 10
            file = os.path.join("results", file)
            germination, spores = 0, 0
            data = pd.read_csv(file)
            df = pd.DataFrame(data)
            for i, row in df.iterrows():
                germination += float(row["48hr %"])
                spores += int(row["Total"])
                treatment = row["Treatment"]
                if (i + 1) % block_size == 0:
                    germination_avg = int(round(germination / block_size, 0))
                    spore_avg = int(round(spores / block_size, 0))
                    # Control/SHAM wells must have at least 50% germination
                    # QoI tolerant isolates must have sufficient germination in those treatments also
                    if germination_avg < 50:
                        if (
                            treatment == "Control"
                            or treatment == "SHAM 100 μg/mL"
                            or (isolate in g143a_mutants and "strobin" in treatment)
                        ):
                            discard_reasons.append(
                                [
                                    f"{treatment}",
                                    f"Poor germination: {germination_avg}%",
                                ]
                            )
                    # Each treatment must average at least a minimum number of spores per well
                    if spore_avg < spore_min:
                        discard_reasons.append(
                            [f"{treatment}", f"Poor spore deposition: {spore_avg}"]
                        )
                    germination, spores = 0, 0
            if discard_reasons:
                print(f"\n{isolate}: {plate}: is not usable:")
                print(
                    tabulate(
                        discard_reasons, headers=["Treatment", "Reason for Discarding"]
                    )
                )
                # Delete bad results output, keep the data out of the workbook
                os.remove(file)
                check_result = f"FAIL: {discard_reasons}"
            else:
                keepers.append([isolate, plate])
                check_result = "PASS"
            # Add QC info to the master spreadsheet
            workbook = "GPMPhenotypingAssay_Workbook.xlsx"
            if os.path.exists(workbook):
                uvc_workbook = openpyxl.load_workbook(workbook)
                if "Assay Data" in uvc_workbook.sheetnames:
                    sheet = uvc_workbook["Assay Data"]
                    assay_df = pd.DataFrame(sheet.values)
                    assay_df.columns = assay_df.iloc[0]
                    for index, row in assay_df[1:].iterrows():
                        if (
                            row["Isolate"] == isolate
                            and row["Plate ID"].upper() == plate.split("PLATE")[1]
                        ):
                            assay_df.at[index, "Quality Check"] = check_result
                    with pd.ExcelWriter(
                        workbook, engine="openpyxl", mode="a", if_sheet_exists="overlay"
                    ) as writer:
                        assay_df.to_excel(
                            writer, sheet_name="Assay Data", header=False, index=False
                        )
    if keepers:
        keepers.sort()
        print(f"\nThe following {len(keepers)} assay runs are keepers:")
        print(tabulate(keepers, headers=["Isolate", "Plate ID"]))


if __name__ == "__main__":
    main()
