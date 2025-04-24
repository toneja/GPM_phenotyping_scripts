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


def main():
    os.chdir(os.path.dirname(__file__))
    for file in os.listdir("results"):
        if file.endswith(".csv"):
            file = os.path.join("results", file)
            data = pd.read_csv(file)
            controls = data[data["Treatment"].str.contains("Control")]
            control_avg = sum(controls["48hr %"].values) / len(controls)
            # Normalize data to the average germination rate of the controls
            df = pd.DataFrame(data)
            for index, row in df.iterrows():
                if row["Treatment"] != "Control":
                    actual_germination = row["48hr %"]
                    normalized_germination = min(
                        round(actual_germination / control_avg * 100, 2), 100
                    )
                    df.at[index, "48hr %"] = normalized_germination
            df.to_csv(file, index=False)


if __name__ == "__main__":
    main()
