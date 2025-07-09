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
import re
import warnings
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt


def extract_ed50(value):
    match = re.match(r"(\d+)", str(value))
    return int(match.group(1)) if match else None


def extract_timepoint(plate_id):
    matches = re.findall(r"(\d+)(?i:hr)", str(plate_id))
    return int(matches[0]) if matches else 1


def tukey_hsd(anova_df, test):
    tukey = pairwise_tukeyhsd(
        endog=anova_df["ED50"], groups=anova_df["Isolate"], alpha=0.05
    )
    print(f"\n*** TUKEY HSD SUMMARY: {test} ***")
    print(tukey.summary().as_text())
    if any(x in test for x in ("Inter", "Manual")):
        ylabel = "Isolates"
    else:
        ylabel = "Timepoints"
    tukey.plot_simultaneous(ylabel=ylabel)
    plt.title(f"Tukey's Honestly Significant Difference Test ({test})")
    plt.xlabel("Mean ED50 (J/m$^2$) + 95% Confidence Interval")
    plt.show()
    plt.close()


def oneway_anova(x, y, test):
    warnings.filterwarnings("ignore")
    anova_df = pd.DataFrame({"Isolate": x, "ED50": y})
    model = ols("ED50~Isolate", data=anova_df)
    results = model.fit()
    anova_table = sm.stats.anova_lm(results, typ=2)
    p_value = anova_table["PR(>F)"]["Isolate"]
    print(f"*** ANOVA TABLE: {test} ***")
    print(results.summary().as_text())
    print("=" * 91)
    if p_value < 0.05:
        tukey_hsd(anova_df, test)


def main(prompt=True, x=pd.Series(), y=pd.Series()):
    os.chdir(os.path.dirname(__file__))
    workbook_file = "GPMPhenotypingAssay_Workbook.xlsx"
    if os.path.exists(workbook_file):
        xls = pd.ExcelFile(workbook_file)
        if "Assay Data" in xls.sheet_names:
            df = xls.parse("Assay Data")
            # Only include runs that passed the quality filter
            keeper_df = df[df["Quality Check"] == "PASS"].copy()
            if x.empty or y.empty:
                # Perform ANOVA test between isolates
                x = keeper_df["Isolate"].values
                y = keeper_df["ED50 (J/m^2)"].apply(extract_ed50).values
                oneway_anova(x, y, "Inter-Isolate")
                # Perform ANOVA test between timepoints
                keeper_df["Timepoint"] = keeper_df["Plate ID"].apply(extract_timepoint)
                # Get unique isolate names
                isolates = set(x)
                for isolate in isolates:
                    isolate_df = keeper_df[keeper_df["Isolate"] == isolate]
                    x = (isolate_df["Timepoint"]).values
                    y = isolate_df["ED50 (J/m^2)"].apply(extract_ed50).values
                    oneway_anova(x, y, f"Intra-Isolate: {isolate}")
            else:
                # Compare manually selected assay runs
                y = y.apply(extract_ed50).values
                oneway_anova(x, y, "Manual Selections")
        else:
            print("Missing Assay Data sheet in workbook.")
    else:
        print("Missing workbook file: GPMPhenotypingAssay_Workbook.xlsx")
    if prompt:
        input("\nTests complete. Press ENTER to quit.\n")


if __name__ == "__main__":
    main(True, pd.Series(), pd.Series)
