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


import csv
import os
from tabulate import tabulate


def main():
    """Check the results and make sure the data is usable."""
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
        "GAT1",
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
            with open(file, "r", newline="", encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                for i, row in enumerate(csv_reader, start=1):
                    germination += float(row["48hr %"])
                    spores += int(row["Total"])
                    treatment = row["Treatment"]
                    if i % block_size == 0:
                        germination_avg = int(round(germination / block_size, 0))
                        spore_avg = int(round(spores / block_size, 0))
                        # Control/SHAM wells must have at least 50% germination
                        # QoI tolerant isolates must have sufficient germination in those treatments also
                        if germination_avg < 50:
                            if treatment == ("Control" or "SHAM 100 μg/mL") or (
                                isolate in g143a_mutants and "strobin" in treatment
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
            else:
                keepers.append([isolate, plate])
    if keepers:
        keepers.sort()
        print(f"\nThe following {len(keepers)} assay runs are keepers:")
        print(tabulate(keepers, headers=["Isolate", "Plate ID"]))


if __name__ == "__main__":
    main()
