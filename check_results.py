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

import csv
import os


def main():
    os.chdir(os.path.dirname(__file__))
    for file in os.listdir("results"):
        if file.endswith(".csv"):
            plate = file.split("_")[1].upper()
            isolate = file.split(".")[0].split("_")[2].upper()
            if "UVC" in plate:
                block_size = 4
            else:
                block_size = 8
            file = os.path.join("results", file)
            germination, spores = 0, 0
            with open(file, "r", newline="", encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                for i, row in enumerate(csv_reader, start=1):
                    germination += float(row["48hr %"])
                    spores += int(row["Total"])
                    treatment = row["Treatment"]
                    if i % block_size == 0:
                        germination_avg = round(germination / block_size, 2)
                        spore_avg = round(spores / block_size, 2)
                        if germination_avg < 50 and treatment == (
                            "Control" or "SHAM 100 μg/mL"
                        ):
                            print(
                                f"{isolate}: {plate}: {treatment}: Poor germination: {germination_avg}%"
                            )
                        if spore_avg < 10:
                            print(
                                f"{isolate}: {plate}: {treatment}: Poor spore deposition: {spore_avg}"
                            )
                        germination, spores = 0, 0


if __name__ == "__main__":
    main()
