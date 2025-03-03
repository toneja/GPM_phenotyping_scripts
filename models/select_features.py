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

"""
Usage: select_features.py <csv_filename>
"""

import os
import sys
import pandas as pd
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression


def select_features(file):
    df = pd.read_csv(file)
    X = df.drop(columns=["X", "Y", "Angle", "FeretX", "FeretY", "FeretAngle", "class"])
    y = df["class"]
    model = LogisticRegression(solver="newton-cg", max_iter=1000)
    sfs = SequentialFeatureSelector(
        model, n_features_to_select="auto", direction="forward"
    )
    sfs.fit(X, y)
    print(f"Selected features: {', '.join(X.columns[sfs.get_support()])}")
    return sfs.get_support()


def main(file):
    select_features(file)
    input("Feature selection complete. Press ENTER to close.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        os.chdir(os.path.dirname(__file__))
        main("model_training_data.csv")
