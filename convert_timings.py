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
        if "UVC" not in file:
            continue
        if file.endswith(".csv"):
            plate = file.split("_")[1]
            isolate = file.split(".")[0].split("_")[2]
            file = os.path.join("results", file)
            timings_file = f"ECHO Images/{plate}_{isolate}_48hr/_timings.csv"
            if os.path.exists(timings_file):
                timings = {}
                with open(timings_file, "r", encoding="utf-8") as in_file:
                    reader = csv.reader(
                        in_file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC
                    )
                    for i, row in enumerate(reader, start=1):
                        # take the average time from 3 runs
                        exposure_time = sum(row) / 3
                        # convert measured timings to measured lamp length
                        # 0.25m (timed distance) -> 0.385m (length of lamp)
                        exposure_time *= 0.385 / 0.25
                        # measured lamp output in W/m2
                        Wperm2 = 20.6385
                        # calculate UV-C dose based on exposure time
                        uvc_dose = int(round(Wperm2 * exposure_time, 0))
                        timings[f"Speed {i}"] = f"{uvc_dose} J/m2"
                with open(file, "r", encoding="utf-8") as out_file:
                    content = out_file.read()
                    for key, value in timings.items():
                        content = content.replace(key, str(value))
                with open(file, "w", encoding="utf-8") as out_file:
                    out_file.write(content)


if __name__ == "__main__":
    main()
