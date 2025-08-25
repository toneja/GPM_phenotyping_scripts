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

"""docstring goes here"""


import os
import re
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def extract_ed50(value):
    """docstring goes here"""
    match = re.match(r"(\d+)", str(value))
    return int(match.group(1)) if match else 0


def extract_timepoint(plate_id):
    """docstring goes here"""
    matches = re.compile(r"(\d+(?:\.\d+)?)(?i:hr)").search(plate_id)
    return float(matches.group(1)) if matches else 1.0


def tukey_hsd(anova_df, test):
    """docstring goes here"""
    tukey = pairwise_tukeyhsd(
        endog=anova_df["ED50"], groups=anova_df["Group"], alpha=0.05
    )
    print(f"\n*** TUKEY HSD SUMMARY: {test} ***")
    print(tukey.summary().as_text())
    tukey.plot_simultaneous(
        ylabel="Isolates" if "Inter" in test else "Hours Since Sunset"
    )
    plt.title(f"Tukey's Honestly Significant Difference Test ({test})")
    plt.xlabel("Mean ED50 (J/m$^2$) + 95% Confidence Interval")
    plt.show()
    plt.close()


def oneway_anova(x, y, test):
    """docstring goes here"""
    warnings.filterwarnings("ignore")
    anova_df = pd.DataFrame({"Group": x, "ED50": y})
    model = ols("ED50~Group", data=anova_df)
    results = model.fit()
    sm.stats.anova_lm(results, typ=2)
    print(f"*** ANOVA TABLE: {test} ***")
    print(results.summary().as_text())
    print("=" * 91)
    tukey_hsd(anova_df, test)


def compare_isolates(df):
    """Perform ANOVA test between isolates."""
    x = df["Isolate"].values
    y = df["ED50 (J/m^2)"].apply(extract_ed50).values
    oneway_anova(x, y, "Inter-Isolate")


def compare_timepoints(df):
    """Perform ANOVA test between timepoints."""
    df["Timepoint"] = df["Plate ID"].apply(extract_timepoint)
    # Get unique isolate names
    isolates = set(df["Isolate"].values)
    for isolate in isolates:
        isolate_df = df[df["Isolate"] == isolate]
        x = isolate_df["Timepoint"].values
        y = isolate_df["ED50 (J/m^2)"].apply(extract_ed50).values
        oneway_anova(x, y, f"Intra-Isolate: {isolate}")


def main(prompt=True):
    """docstring goes here"""
    os.chdir(os.path.dirname(__file__))
    workbook_file = "GPMPhenotypingAssay_Workbook.xlsx"
    if os.path.exists(workbook_file):
        xls = pd.ExcelFile(workbook_file)
        if "Assay Data" in xls.sheet_names:
            df = xls.parse("Assay Data")
            # Only include runs that passed the quality filter
            keeper_df = df[df["Quality Check"] == "PASS"].copy()
            # Perform ANOVA test between isolates
            compare_isolates(keeper_df)
            # Perform ANOVA test between timepoints
            compare_timepoints(keeper_df)
        else:
            print("Missing Assay Data sheet in workbook.")
    else:
        print("Missing workbook file: GPMPhenotypingAssay_Workbook.xlsx")
    if prompt:
        input("\nTests complete. Press ENTER to quit.\n")


if __name__ == "__main__":
    main(True)
